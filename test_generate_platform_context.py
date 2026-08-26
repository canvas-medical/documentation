#!/usr/bin/env uv run --script

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pytest",
#     "pyyaml",
#     "beautifulsoup4",
#     "html2text",
# ]
# ///

"""Tests for generate-platform-context.py (the Help Center scraper).

Runs offline against small stubbed fixtures via an injected fetcher:

    uv run ./test_generate_platform_context.py
"""

import importlib.util
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))


def _load(module_name: str, filename: str):
    """Import a repo-root module by path (the generator's filename is hyphenated)."""
    spec = importlib.util.spec_from_file_location(module_name, REPO_ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


gen = _load("generate_platform_context", "generate-platform-context.py")

# --- Fixtures: a stub llms.txt index + a handful of stub article HTML pages ---

U1 = "https://help.canvasmedical.com/articles/1001-managing-appointments"
U2 = "https://help.canvasmedical.com/articles/1002-canvas-chat"
U3 = "https://help.canvasmedical.com/articles/1003-processing-payments"
U4 = "https://help.canvasmedical.com/articles/1004-broken"  # empty body -> dropped

STUB_LLMS = f"""# Canvas Medical Help Center


## Getting Started


### Onboarding & Setup

- [Managing Patient Appointments]({U1})
- [Canvas Chat and Bot]({U2})

## Revenue & Billing

- [Processing Payments]({U3})
- [Broken Article]({U4})
"""

# Article with a title <h1> (dropped from the index outline) plus nested
# <h2>/<h3> subsections and a curly apostrophe (must be ASCII-normalized).
PAGE_1001 = """<html><body>
<div class="kb-article-body kb-article-body--ssr">
<h1>Managing Patient Appointments</h1>
<p>Manage a patient’s visits in Canvas.</p>
<h2>Scheduling Appointments</h2>
<p>How to schedule an appointment.</p>
<h3>Recurring Appointments</h3>
<p>Set up recurring visits.</p>
<h2>Rescheduling &amp; Cancelling</h2>
<p>Move or cancel a booking.</p>
<h2>Appointment Reminders</h2>
<p>Canvas sends a single org-wide reminder.</p>
</div>
</body></html>"""

# Non-empty body with no subsections: keeps its index bullet, gets no sub-list.
PAGE_1002 = """<html><body>
<div class="kb-article-body kb-article-body--ssr">
<h1>Canvas Chat and Bot</h1>
<p>Chat helps staff communicate.</p>
</div>
</body></html>"""

PAGE_1003 = """<html><body>
<div class="kb-article-body kb-article-body--ssr">
<h1>Processing Payments</h1>
<p>Take payments in Canvas.</p>
<h2>Payment Methods</h2>
<p>Cards and saved methods.</p>
<h2>Refunds</h2>
<p>Issue a refund.</p>
</div>
</body></html>"""

# No kb-article-body container -> extract returns empty -> skipped from both files.
PAGE_1004 = """<html><body>
<div class="some-other-class"><h1>Broken</h1></div>
</body></html>"""

PAGES = {U1: PAGE_1001, U2: PAGE_1002, U3: PAGE_1003, U4: PAGE_1004}


def _fake_fetch(url: str) -> str:
    if url == gen.LLMS_INDEX_URL:
        return STUB_LLMS
    return PAGES[url]


def _corpus_block(corpus: str, url: str) -> str:
    """Return the body between this URL's BEGIN/END markers."""
    begin = f"----- BEGIN PAGE {url}\n"
    end = f"----- END PAGE {url}"
    start = corpus.index(begin) + len(begin)
    return corpus[start : corpus.index(end, start)]


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("platform")
    context_path = out / "platform-context.txt"
    index_path = out / "platform-index.txt"
    stats = gen.build(
        context_path=context_path,
        index_path=index_path,
        fetch_url=_fake_fetch,
    )
    return {
        "stats": stats,
        "context": context_path.read_text(encoding="utf-8"),
        "index": index_path.read_text(encoding="utf-8"),
    }


def test_format_begin_end_pairs_sorted_and_ascii(built):
    corpus = built["context"]
    begins = re.findall(r"^----- BEGIN PAGE (\S+)$", corpus, re.M)
    ends = re.findall(r"^----- END PAGE (\S+)$", corpus, re.M)
    assert begins == ends  # matched pairs, in the same order
    assert begins == sorted(begins)  # entries sorted by URL
    assert begins == [U1, U2, U3]  # empty-body article excluded
    for url in begins:
        assert _corpus_block(corpus, url).strip()  # bodies non-empty
    assert "’" not in corpus and "“" not in corpus  # ASCII-normalized


def test_heading_hierarchy_preserved(built):
    block = _corpus_block(built["context"], U1)
    i_h1 = block.index("# Managing Patient Appointments")
    i_h2 = block.index("## Scheduling Appointments")
    i_h3 = block.index("### Recurring Appointments")
    assert i_h1 < i_h2 < i_h3  # nested #/##/### in document order


def test_index_structure(built):
    index = built["index"]
    # Help Center category headings preserved
    assert "## Getting Started" in index
    assert "### Onboarding & Setup" in index
    assert "## Revenue & Billing" in index
    # one verbatim bullet per non-empty article
    assert f"- [Managing Patient Appointments]({U1})" in index
    assert f"- [Canvas Chat and Bot]({U2})" in index
    assert f"- [Processing Payments]({U3})" in index
    # subsections as an indented sub-list (h2 -> 4 spaces, h3 -> 8 spaces)
    assert "\n    - Scheduling Appointments\n" in index
    assert "\n        - Recurring Appointments\n" in index
    assert "\n    - Rescheduling & Cancelling\n" in index
    # the duplicated <h1> is dropped from the outline
    assert "    - Managing Patient Appointments" not in index
    # a subsection-less article keeps its bullet with no sub-list under it
    lines = index.splitlines()
    chat_idx = lines.index(f"- [Canvas Chat and Bot]({U2})")
    assert not lines[chat_idx + 1].startswith("    ")


def test_two_tier_round_trip(built):
    index_lines = built["index"].splitlines()
    # 1. grep the index for a keyword -> land on a subsection line
    sub_idx = next(
        i
        for i, ln in enumerate(index_lines)
        if ln.startswith("    ") and "scheduling" in ln.lower()
    )
    # 2. its parent bullet carries the article URL to read
    url = next(
        gen.BULLET_RE.match(index_lines[j])["url"]
        for j in range(sub_idx, -1, -1)
        if gen.BULLET_RE.match(index_lines[j])
    )
    assert url == U1
    # 3. read that one article's body from the corpus and find the subsection
    assert "## Scheduling Appointments" in _corpus_block(built["context"], url)


def test_non_empty_and_index_corpus_in_sync(built):
    corpus, index = built["context"], built["index"]
    assert corpus.strip() and index.strip()  # both non-empty
    corpus_urls = set(re.findall(r"^----- BEGIN PAGE (\S+)$", corpus, re.M))
    index_urls = {
        gen.BULLET_RE.match(ln)["url"]
        for ln in index.splitlines()
        if gen.BULLET_RE.match(ln)
    }
    assert corpus_urls == index_urls  # every index URL resolves to a corpus block
    assert corpus.count("----- BEGIN PAGE ") == built["stats"].included
    # the empty-body article is dropped from both, keeping the two files in sync
    assert U4 not in corpus_urls
    assert U4 not in index


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
