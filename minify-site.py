#!/usr/bin/env uv run

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "minify-html==0.18.1",
# ]
# ///

"""Minify every built HTML page in _site/ in place, including inline JS and CSS.

Run AFTER `jekyll build` and generate-llms.py, so the markdown mirrors are
extracted from the unminified HTML.
"""

import re
import sys
from pathlib import Path

import minify_html

SITE = Path(__file__).parent / "_site"
PRE_BLOCK = re.compile(r"<pre[\s>].*?</pre>", re.DOTALL)
TRAILING_SPACE = re.compile(r"[ \t]+\n")
SPACE_BEFORE_CLOSE = re.compile(r"\s+</pre>$")


def strip_code_trailing_space(html: str) -> str:
    """Drop trailing whitespace in code blocks, which minify-html keeps.

    Long trailing spaces wrap a line, and a newline right before </pre> renders a blank line.
    """

    def clean(match: re.Match[str]) -> str:
        return SPACE_BEFORE_CLOSE.sub("</pre>", TRAILING_SPACE.sub("\n", match.group(0)))

    return PRE_BLOCK.sub(clean, html)


def main() -> None:
    if not SITE.is_dir():
        sys.exit(f"{SITE} does not exist; run jekyll build first")

    pages = sorted(SITE.rglob("*.html"))
    before = after = 0
    for page in pages:
        html = page.read_text(encoding="utf-8")
        minified = minify_html.minify(
            strip_code_trailing_space(html),
            keep_closing_tags=True,
            keep_html_and_head_opening_tags=True,
            minify_css=True,
            minify_js=True,
        )
        page.write_text(minified, encoding="utf-8")
        before += len(html.encode())
        after += len(minified.encode())

    print(f"Minified {len(pages)} pages: {before / 1e6:.1f} MB -> {after / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
