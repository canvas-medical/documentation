#!/usr/bin/env uv run

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
#     "beautifulsoup4",
#     "html2text",
# ]
# ///

"""Scrape the Canvas Help Center into two bundled, grep-able reference artifacts.

The Help Center (Pylon-hosted, https://help.canvasmedical.com) documents Canvas's
*native platform features*. Unlike the SDK/FHIR corpus, which reads the locally
built Jekyll `_site/`, the Help Center has no local build and serves no clean
markdown (`llms-full.txt` 404s; appending `.md` returns the article HTML
unchanged), so the only source is the article HTML, fetched over the network.

Produces two files at the repo root, both regenerated on the sync cron:

  - platform-context.txt : the full-body corpus. One `----- BEGIN PAGE <url>` /
    `----- END PAGE <url>` entry per article, sorted by URL, in the identical
    delimiter format as sdk-context.txt so the existing read/cite workflow works
    unchanged.
  - platform-index.txt : a compact discovery index. The Help Center's own
    category headings from llms.txt, a `- [Title](url)` bullet per article, and
    each article's <h2>/<h3> subsection outline as an indented sub-list.

An agent greps the small index for keywords, reads the one matching article's
body from the corpus by its URL, and cites that URL.
"""

import re
import sys
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from context_extractor import (
    REPO_ROOT,
    extract_content_from_html,
    extract_outline,
)

HELP_BASE_URL = "https://help.canvasmedical.com"
LLMS_INDEX_URL = f"{HELP_BASE_URL}/llms.txt"

# Pylon renders the article body server-side into this container (the class list
# carries `kb-article-body--ssr`), so the full prose and its <h1>/<h2>/<h3>
# headings are in the initial HTML -- no JS execution needed.
ARTICLE_CONTAINER_CLASS = "kb-article-body"

CONTEXT_FILE = REPO_ROOT / "platform-context.txt"
INDEX_FILE = REPO_ROOT / "platform-index.txt"

# llms.txt structure: `##`/`###`/`####` category headings and
# `- [Title](https://help.canvasmedical.com/articles/<id>-<slug>)` bullets.
HEADING_RE = re.compile(r"^(?P<hashes>#{2,4}) (?P<text>.+?)\s*$")
BULLET_RE = re.compile(
    r"^- \[(?P<title>.+?)\]"
    r"\((?P<url>https://help\.canvasmedical\.com/articles/[^)]+)\)\s*$"
)


@dataclass
class IndexNode:
    """One line of llms.txt worth keeping: a category heading or an article bullet."""

    kind: str  # "heading" | "article"
    raw: str  # the verbatim source line (headings/bullets are re-emitted as-is)
    url: str = ""  # article nodes only


def fetch(url: str) -> str:
    """Fetch a URL and return its decoded body (the default network fetcher)."""
    req = urllib.request.Request(url, headers={"User-Agent": "canvas-docs-context-generator"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (https only)
        return resp.read().decode("utf-8")


def parse_llms_index(text: str) -> list[IndexNode]:
    """Parse llms.txt into ordered category-heading and article-bullet nodes."""
    nodes: list[IndexNode] = []
    for line in text.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            nodes.append(IndexNode(kind="heading", raw=f"{heading['hashes']} {heading['text']}"))
            continue
        bullet = BULLET_RE.match(line)
        if bullet:
            nodes.append(IndexNode(kind="article", raw=line.rstrip(), url=bullet["url"]))
    return nodes


def write_context_entry(f, url: str, content: str) -> None:
    """Append one corpus entry, byte-for-byte matching generate-context.py's format."""
    f.write(f"----- BEGIN PAGE {url}\n")
    f.write(content)
    f.write(f"\n----- END PAGE {url}\n\n\n")


def write_index(
    path: Path,
    nodes: list[IndexNode],
    included: set[str],
    outlines: dict[str, list[tuple[int, str]]],
) -> None:
    """Write the discovery index: llms.txt headings + surviving bullets + outlines."""
    lines: list[str] = []
    for node in nodes:
        if node.kind == "heading":
            if lines:
                lines.append("")
            lines.append(node.raw)
        elif node.url in included:
            lines.append(node.raw)
            for level, text in outlines.get(node.url, []):
                lines.append(f"{'    ' * (level - 1)}- {text}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


@dataclass
class BuildStats:
    articles: int = 0  # distinct article URLs in llms.txt
    included: int = 0  # articles with a non-empty body (written to both files)
    empty: list[str] = field(default_factory=list)  # skipped (empty body / fetch miss)


def build(
    context_path: Path = CONTEXT_FILE,
    index_path: Path = INDEX_FILE,
    fetch_url: Callable[[str], str] = fetch,
    index_url: str = LLMS_INDEX_URL,
    container_class: str = ARTICLE_CONTAINER_CLASS,
) -> BuildStats:
    """Scrape the Help Center and write the corpus + index.

    An article appears in *both* outputs iff its body is non-empty; the two files
    therefore stay in sync (every index URL resolves to a corpus BEGIN PAGE
    block). A body that comes back empty is the signal that Pylon changed its
    markup, so it is logged and skipped rather than emitted blank.

    Bodies (the large data) are streamed to the corpus and flushed per article so
    a late crash keeps its progress; only the small per-article outlines are held
    in memory to assemble the index at the end.
    """
    nodes = parse_llms_index(fetch_url(index_url))
    urls = sorted({n.url for n in nodes if n.kind == "article"})

    outlines: dict[str, list[tuple[int, str]]] = {}
    included: set[str] = set()
    stats = BuildStats(articles=len(urls))

    with open(context_path, "w", encoding="utf-8") as cf:
        for i, url in enumerate(urls, 1):
            html = fetch_url(url)
            body = extract_content_from_html(html, container_class)
            if not body:
                print(f"  WARN: empty body, skipping {url}", file=sys.stderr)
                stats.empty.append(url)
                continue
            write_context_entry(cf, url, body)
            cf.flush()
            outlines[url] = extract_outline(html, container_class)
            included.add(url)
            print(f"  [{i}/{len(urls)}] {url}")

    write_index(index_path, nodes, included, outlines)
    stats.included = len(included)
    return stats


def main() -> None:
    stats = build()
    print(
        f"Wrote {stats.included}/{stats.articles} articles to "
        f"{CONTEXT_FILE.name} + {INDEX_FILE.name}"
    )
    if stats.empty:
        print(f"Skipped {len(stats.empty)} empty-body article(s):", file=sys.stderr)
        for url in stats.empty:
            print(f"  - {url}", file=sys.stderr)


if __name__ == "__main__":
    main()
