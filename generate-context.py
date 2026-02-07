#!/usr/bin/env uv run

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
# ]
# ///

"""Read local markdown files and write them into coding-agent-context.txt."""

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent
COLLECTIONS = [
    "_sdk",
    "_guides",
    "_api",
]
BASE_URL = "https://docs.canvasmedical.com"
OUTPUT_FILE = REPO_ROOT / "coding-agent-context.txt"

FRONTMATTER_RE = re.compile(r"\A---\n(.+?)\n---\n?", re.DOTALL)


def parse_file(path: Path, collection: str) -> tuple[str, str] | None:
    """Return (canonical_url, body_markdown) or None on failure."""
    text = path.read_text(encoding="utf-8")

    match = FRONTMATTER_RE.match(text)

    if match:
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            meta = {}

        body = text[match.end() :]
    else:
        meta = {}
        body = text

    slug = meta.get("slug")

    if slug is not None:
        slug = str(slug).strip()

        url_path = f"/{collection}/" if slug == "/" else f"/{collection}/{slug}/"
    else:
        # derive from filename
        url_path = f"/{collection}/{path.stem}/"

    url = f"{BASE_URL}{url_path}"

    # Strip blank lines to produce dense markdown
    dense = "\n".join(line for line in body.splitlines() if line.strip())

    return url, dense


def main() -> None:
    pages: list[tuple[str, str]] = []

    for collection in COLLECTIONS:
        collection_dir = REPO_ROOT / "collections" / collection

        for md_path in sorted(collection_dir.rglob("*.md")):
            result = parse_file(md_path, collection.lstrip("_"))

            if result:
                pages.append(result)

    # Sort by URL for deterministic output
    pages.sort(key=lambda p: p[0])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for url, content in pages:
            f.write(f"----- BEGIN PAGE {url}\n")
            f.write(content)
            f.write(f"\n----- END PAGE {url}\n\n\n")

    print(f"Wrote {len(pages)} pages to {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
