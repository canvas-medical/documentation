#!/usr/bin/env uv run

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
#     "beautifulsoup4",
#     "html2text",
# ]
# ///

"""Generate llms.txt, llms-full.txt, and per-page .md mirrors into _site/.

Run AFTER `jekyll build` (the _site/ directory must already exist). Reuses the
shared HTML->markdown extractor in context_extractor.py so the .md mirrors and
llms-full.txt match sdk-context.txt / fhir-context.txt exactly.

Outputs (all written into _site/, served statically by Amplify):
  - _site/<path>.md         a clean-markdown mirror of every built content page
  - _site/llms.txt          spec-compliant index (llmstxt.org), links to .md pages
  - _site/llms-full.txt     the core reference corpus concatenated as markdown

The .md mirrors are produced by walking the built HTML, so every page is covered
regardless of how its permalink is derived. The curated llms.txt index and
llms-full.txt corpus are driven by the collection front matter (titles, excerpts,
ordering), with release notes and FDB changelogs kept behind the droppable
`## Optional` section per the llmstxt.org convention.
"""

import sys
from dataclasses import dataclass

from context_extractor import (
    BASE_URL,
    REPO_ROOT,
    SITE_DIR,
    extract_content,
    frontmatter,
    url_path_for,
)

COLLECTIONS_DIR = REPO_ROOT / "collections"

# Core reference sections: rendered as required H2 lists in llms.txt and
# concatenated into llms-full.txt. (collection folder, url segment, heading).
CORE_SECTIONS = [
    ("_sdk", "sdk", "SDK"),
    ("_api", "api", "FHIR API"),
    ("_guides", "guides", "Guides"),
    ("_learn", "learn", "Learn"),
    ("_documentation", "documentation", "Other documentation"),
]

# Landing pages for the droppable `## Optional` section. Enumerating every
# release note / changelog would bloat the index; link the indexes instead.
OPTIONAL_LINKS = [
    (
        "Product release notes",
        "/product-updates/release-notes/",
        "Chronological feature, fix, and breaking-change log.",
    ),
    (
        "FDB changelogs",
        "/product-updates/fdb-changelogs/",
        "Weekly First Databank drug-database updates.",
    ),
]

SUMMARY = (
    "Canvas Medical's developer documentation: the server-side Python SDK, the FHIR "
    "API, and implementation guides for building EMR customizations. Patient and "
    "staff keys are UUIDs without dashes; other identifiers use standard dashed UUIDs."
)

INDEX_INTRO = (
    "This site documents how to extend and integrate with Canvas Medical, an EHR "
    "platform: the server-side Python SDK (plugins, data models, handlers, effects, "
    "commands), the FHIR API, and implementation guides. Every page is also available "
    "as clean markdown by appending `.md` to its URL. The full reference corpus is "
    f"concatenated at {BASE_URL}/llms-full.txt."
)


@dataclass
class PageMeta:
    url_path: str  # /sdk/data-patient/
    title: str
    excerpt: str

    @property
    def md_url(self) -> str:
        return f"{BASE_URL}/{self.url_path.strip('/')}.md"


def mirror_built_pages() -> dict[str, str]:
    """Write a .md mirror next to every built content page.

    Returns a {url_path: markdown} map so the index/corpus can reuse the
    extracted content without re-parsing the HTML.
    """
    contents: dict[str, str] = {}

    for html_path in sorted(SITE_DIR.rglob("index.html")):
        rel = html_path.parent.relative_to(SITE_DIR).as_posix()
        if rel == ".":
            continue  # site-root landing page has no article content

        content = extract_content(html_path)
        if not content:
            continue

        url_path = f"/{rel}/"
        contents[url_path] = content

        out = SITE_DIR / f"{rel}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f"> Canonical page: {BASE_URL}{url_path}\n\n{content}\n", encoding="utf-8")

    print(f"Wrote {len(contents)} .md mirrors")
    return contents


def collect_meta(collection_folder: str, url_segment: str) -> list[PageMeta]:
    """Read title/excerpt/url for every visible page in a collection."""
    coll_dir = COLLECTIONS_DIR / collection_folder
    pages: list[PageMeta] = []

    for md_path in sorted(coll_dir.rglob("*.md")):
        meta = frontmatter(md_path)
        if meta.get("hidden") is True:
            continue
        pages.append(
            PageMeta(
                url_path=url_path_for(md_path, url_segment),
                title=str(meta.get("title") or md_path.stem).strip(),
                excerpt=str(meta.get("excerpt") or "").strip(),
            )
        )

    pages.sort(key=lambda p: p.url_path)
    return pages


def main() -> None:
    if not SITE_DIR.exists():
        sys.exit("_site/ not found. Run `bundle exec jekyll build` first.")

    contents = mirror_built_pages()

    # Core sections: only pages that actually rendered article content.
    core = []
    for folder, segment, heading in CORE_SECTIONS:
        pages = [p for p in collect_meta(folder, segment) if p.url_path in contents]
        if pages:
            core.append((heading, pages))

    # llms.txt — the spec-compliant index (links point at the .md mirrors).
    lines = ["# Canvas Medical Developer Documentation", "", f"> {SUMMARY}", "", INDEX_INTRO, ""]
    for heading, pages in core:
        lines.append(f"## {heading}")
        for p in pages:
            bullet = f"- [{p.title}]({p.md_url})"
            if p.excerpt:
                bullet += f": {p.excerpt}"
            lines.append(bullet)
        lines.append("")

    lines.append("## Optional")
    for title, path, desc in OPTIONAL_LINKS:
        lines.append(f"- [{title}]({BASE_URL}{path}): {desc}")
    lines.append("")

    (SITE_DIR / "llms.txt").write_text("\n".join(lines), encoding="utf-8")
    core_count = sum(len(pages) for _heading, pages in core)
    print(f"Wrote llms.txt ({core_count} core links)")

    # llms-full.txt — the core reference corpus concatenated as markdown.
    full = ["# Canvas Medical Developer Documentation (Full Reference)", "", f"> {SUMMARY}", ""]
    for _heading, pages in core:
        for p in pages:
            full += [
                f"# {p.title}",
                "",
                f"Source: {BASE_URL}{p.url_path}",
                "",
                contents[p.url_path],
                "",
                "---",
                "",
            ]

    (SITE_DIR / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")
    print(f"Wrote llms-full.txt ({core_count} pages)")


if __name__ == "__main__":
    main()
