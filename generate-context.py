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

import re
import subprocess
import sys
from pathlib import Path

import html2text
import yaml
from bs4 import BeautifulSoup, Tag

REPO_ROOT = Path(__file__).resolve().parent
BASE_URL = "https://docs.canvasmedical.com"
SITE_DIR = REPO_ROOT / "_site"

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


FRONTMATTER_RE = re.compile(r"\A---\n(.+?)\n---\n?", re.DOTALL)

# Alert type → label for markdown conversion
ALERT_LABELS = {
    "alert__info": "Info",
    "alert__warning": "Warning",
    "alert__danger": "Danger",
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


def url_path_for(path: Path, collection: str) -> str:
    """Compute the URL path for a collection markdown file."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)

    if match:
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
    else:
        meta = {}

    slug = meta.get("slug")

    if slug is not None:
        slug = str(slug).strip()
        return f"/{collection}/" if slug == "/" else f"/{collection}/{slug}/"

    return f"/{collection}/{path.stem}/"


def html_path_for(url_path: str) -> Path:
    """Map a URL path to the built HTML file in _site/."""
    # /sdk/ -> _site/sdk/index.html
    # /sdk/commands/ -> _site/sdk/commands/index.html
    return SITE_DIR / url_path.strip("/") / "index.html"


def preprocess_code_blocks(soup: BeautifulSoup, container: Tag) -> None:
    """Convert Rouge-highlighted code blocks to markdown fenced blocks."""
    for div in container.find_all("div", class_="highlighter-rouge"):
        classes = div.get("class", [])
        lang = ""
        for cls in classes:
            if cls.startswith("language-"):
                lang = cls.removeprefix("language-")
                break

        code_tag = div.find("code")
        if not code_tag:
            continue

        code_text = code_tag.get_text()
        # Strip single trailing newline that Rouge adds
        if code_text.endswith("\n"):
            code_text = code_text[:-1]

        replacement = soup.new_tag("pre")
        replacement.string = f"```{lang}\n{code_text}\n```"
        div.replace_with(replacement)


def preprocess_alerts(soup: BeautifulSoup, container: Tag) -> None:
    """Convert alert aside elements to blockquote-style markdown."""
    for aside in container.find_all("aside", class_="alert"):
        classes = aside.get("class", [])
        label = "Note"
        for cls in classes:
            if cls in ALERT_LABELS:
                label = ALERT_LABELS[cls]
                break

        content_div = aside.find("div", class_="alert__content")
        if not content_div:
            continue

        # Get inner HTML so html2text can process links etc.
        inner_html = content_div.decode_contents()
        replacement = soup.new_tag("blockquote")
        replacement.append(BeautifulSoup(f"<p><strong>{label}:</strong> {inner_html}</p>", "html.parser"))
        aside.replace_with(replacement)


def preprocess_tabs(soup: BeautifulSoup, container: Tag) -> None:
    """Add tab labels before each tab content panel."""
    for tab_menu in container.find_all("ul", class_="tab"):
        tab_id = tab_menu.get("data-tab")
        if not tab_id:
            continue

        # Collect tab names
        tab_names = []
        for li in tab_menu.find_all("li", recursive=False):
            a = li.find("a")
            if a:
                tab_names.append(a.get_text(strip=True))

        # Find corresponding tab-content
        content_ul = container.find("ul", class_="tab-content", id=tab_id)
        if not content_ul:
            continue

        # Add a heading before each tab panel's content
        content_items = content_ul.find_all("li", recursive=False)
        for i, li in enumerate(content_items):
            name = tab_names[i] if i < len(tab_names) else f"Tab {i + 1}"
            label = soup.new_tag("p")
            label.string = f"**{name}**"
            li.insert(0, label)

        # Remove the tab menu (the labels are now inline)
        tab_menu.decompose()


def extract_content(html_path: Path) -> str | None:
    """Extract and convert the article content from a built HTML page."""
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    container = soup.find("div", class_="article__container__inner")
    if not container:
        return None

    # Remove unwanted elements
    for tag_name in ("header", "script", "style", "svg", "nav", "footer"):
        for el in container.find_all(tag_name):
            el.decompose()

    # Remove anchor links (the # links after headings)
    for a in container.find_all("a", class_="article__anchor"):
        a.decompose()

    # Pre-process special elements before html2text
    preprocess_code_blocks(soup, container)
    preprocess_alerts(soup, container)
    preprocess_tabs(soup, container)

    # Convert HTML to markdown
    h = html2text.HTML2Text()
    h.body_width = 0
    h.unicode_snob = False
    h.protect_links = False
    h.wrap_links = False
    h.mark_code = False
    h.ul_item_mark = "-"

    md = h.handle(str(container))

    # Replace smart quotes with plain ASCII equivalents
    md = md.translate(str.maketrans("\u2018\u2019\u201c\u201d", "''\"\""))

    # Strip blank lines to produce dense markdown
    dense = "\n".join(line for line in md.splitlines() if line.strip())

    return dense


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
