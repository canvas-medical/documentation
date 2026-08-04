# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
#     "beautifulsoup4",
#     "html2text",
# ]
# ///

"""Shared helpers for turning the built Jekyll site into markdown.

Both generate-context.py (SDK/FHIR coding-agent context files) and
generate-llms.py (llms.txt, llms-full.txt, per-page .md) import from here so the
HTML->markdown extraction lives in exactly one place.
"""

import re
from pathlib import Path

import html2text
import yaml
from bs4 import BeautifulSoup, Tag

REPO_ROOT = Path(__file__).resolve().parent
BASE_URL = "https://docs.canvasmedical.com"
SITE_DIR = REPO_ROOT / "_site"

FRONTMATTER_RE = re.compile(r"\A---\n(.+?)\n---\n?", re.DOTALL)

# Alert type → label for markdown conversion
ALERT_LABELS = {
    "alert__info": "Info",
    "alert__warning": "Warning",
    "alert__danger": "Danger",
}


def frontmatter(path: Path) -> dict:
    """Parse the YAML frontmatter of a collection markdown file."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def url_path_for(path: Path, collection: str) -> str:
    """Compute the URL path for a collection markdown file."""
    slug = frontmatter(path).get("slug")

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
        replacement.append(
            BeautifulSoup(f"<p><strong>{label}:</strong> {inner_html}</p>", "html.parser")
        )
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
    md = md.translate(str.maketrans("‘’“”", "''\"\""))

    # Strip blank lines to produce dense markdown
    dense = "\n".join(line for line in md.splitlines() if line.strip())

    return dense
