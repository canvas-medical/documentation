#!/usr/bin/env uv run

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
#     "beautifulsoup4",
#     "html2text",
# ]
# ///

"""Build Jekyll site, extract rendered HTML, and convert to markdown context files.

Produces two files:
  - sdk-context.txt: SDK docs + SDK-related guides
  - fhir-context.txt: FHIR API docs + FHIR-related guides

Requires: bundle exec jekyll build (run separately or via the JEKYLL_BUILD env var).
The _site/ directory must exist before running this script.
"""

import subprocess
import sys
from pathlib import Path

from context_extractor import (
    BASE_URL,
    REPO_ROOT,
    SITE_DIR,
    extract_content,
    html_path_for,
    url_path_for,
)

# Guides are classified by stem (filename without .md) into SDK or FHIR.
# Any guide not listed here is excluded (e.g., index.md landing page).
FHIR_GUIDE_STEMS = {
    "embedding-a-smart-on-fhir-application",
    "fhir-v2-migration-guide",
    "improve-hcc-coding-accuracy",
    "note-management-oauth",
    "staying-on-top-of-tasks",
    "submit-vitals-via-fhir",
}
SDK_GUIDE_STEMS = {
    "appointments-additional_fields",
    "creating-webhooks-with-the-canvas-sdk",
    "custom-landing-page",
    "customize-panel-buttons",
    "customize-search-results",
    "growth-charts",
    "patient-chart-group-items",
    "patient-portal-forms",
    "profile-additional-fields",
    "scribe-ai-parser",
    "set-default-homepage",
    "tailoring-the-chart-to-the-patient",
    "your-first-application",
    "your-first-plugin-with-claude-code",
    "your-first-plugin",
}


def build_jekyll() -> None:
    """Run Jekyll build if _site/ doesn't exist."""
    if SITE_DIR.exists():
        return

    print("Running bundle exec jekyll build ...")
    result = subprocess.run(
        ["bundle", "exec", "jekyll", "build"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(f"Jekyll build failed (exit {result.returncode})")


def collect_pages(collection: str) -> list[tuple[str, str]]:
    """Extract all pages from a collection, returning (url, content) pairs."""
    collection_name = collection.lstrip("_")
    collection_dir = REPO_ROOT / "collections" / collection
    pages: list[tuple[str, str]] = []

    for md_path in sorted(collection_dir.rglob("*.md")):
        url_path = url_path_for(md_path, collection_name)
        url = f"{BASE_URL}{url_path}"
        hp = html_path_for(url_path)

        if not hp.exists():
            print(f"  WARN: no HTML for {md_path.name} -> {hp}", file=sys.stderr)
            continue

        content = extract_content(hp)
        if content:
            pages.append((url, content))

    return pages


def write_context_file(path: Path, pages: list[tuple[str, str]]) -> None:
    """Write pages to a context file, sorted by URL."""
    pages.sort(key=lambda p: p[0])
    with open(path, "w", encoding="utf-8") as f:
        for url, content in pages:
            f.write(f"----- BEGIN PAGE {url}\n")
            f.write(content)
            f.write(f"\n----- END PAGE {url}\n\n\n")
    print(f"Wrote {len(pages)} pages to {path.name}")


def main() -> None:
    build_jekyll()

    if not SITE_DIR.exists():
        sys.exit("_site/ directory not found. Run: bundle exec jekyll build")

    # Collect pages for each output file from its primary collections
    sdk_pages: list[tuple[str, str]] = []
    fhir_pages: list[tuple[str, str]] = []

    for collection, target in [("_sdk", sdk_pages), ("_api", fhir_pages)]:
        target.extend(collect_pages(collection))

    # Route guides by stem classification
    guides_dir = REPO_ROOT / "collections" / "_guides"
    for md_path in sorted(guides_dir.rglob("*.md")):
        stem = md_path.stem
        if stem in SDK_GUIDE_STEMS:
            target = sdk_pages
        elif stem in FHIR_GUIDE_STEMS:
            target = fhir_pages
        else:
            continue

        url_path = url_path_for(md_path, "guides")
        url = f"{BASE_URL}{url_path}"
        hp = html_path_for(url_path)

        if not hp.exists():
            print(f"  WARN: no HTML for {md_path.name} -> {hp}", file=sys.stderr)
            continue

        content = extract_content(hp)
        if content:
            target.append((url, content))

    write_context_file(REPO_ROOT / "sdk-context.txt", sdk_pages)
    write_context_file(REPO_ROOT / "fhir-context.txt", fhir_pages)


if __name__ == "__main__":
    main()
