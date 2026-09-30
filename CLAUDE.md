# Canvas Medical Documentation

Developer documentation site for Canvas Medical's SDK, FHIR API, implementation guides, and release notes.

**Production:** https://docs.canvasmedical.com

## Tech Stack

- **Site generator:** Jekyll 4.4 (Ruby 3.1)
- **Assets:** Webpack 5, SCSS, Babel
- **Python tooling:** uv, Python 3.11+ (code block validation, context generation)
- **Package managers:** Yarn 3.x (frontend), Bundler 2.x (Ruby), uv (Python)
- **Search:** Algolia
- **Hosting:** AWS Amplify

## Quick Start

```sh
# With Devbox (recommended)
devbox run dev

# Manual
yarn install && bundle install
yarn dev
```

Dev server runs on ports 4000 (Jekyll) and 4001 (Webpack).

## Project Structure

```text
collections/           # All content (Jekyll collections)
  _api/                # FHIR API resource docs (~60 files)
  _sdk/                # SDK docs (~140 files)
    data/              # Data models (Patient, DocumentReference, etc.)
    handlers/          # Handler types (CronTask, SimpleAPI, etc.)
    effects/           # SDK effects/operations
    commands/          # SDK commands
    clients/           # Third-party integrations
    examples/          # Reference implementations
  _guides/             # Implementation guides (~22 files)
  _release-notes/      # Product updates (~525 files, by year/quarter)
  _documentation/      # Misc docs
  _learn/              # Educational content
  _fdb-changelogs/     # FDB integration changelogs
_layouts/              # Jekyll layout templates
_includes/             # Reusable HTML partials
_data/
  menus.yml            # Navigation/sidebar structure
  globals.yml          # UI labels
  api-attributes.yml   # API doc metadata
_scss/                 # Style partials
_js/                   # JavaScript source
config/                # Webpack configs
```

## Content Conventions

### SDK data docs (`collections/_sdk/data/*.md`)

Frontmatter:
```yaml
---
title: "ModelName"
slug: "data-model-name"
excerpt: "Short description"
hidden: false
---
```

Content pattern: heading, intro paragraph, Basic Usage section with code, Filtering section, Attributes table. Code examples use Django-style ORM queries (`Model.objects.filter(...)`).

### Release notes (`collections/_release-notes/<date>-<version>.md`)

Frontmatter:
```yaml
---
title: 08.13.2026
layout: productupdates
tags: sdk ui
date: 2026-08-13
feed_summary: |          # optional — see below
  ...
---
```

Body: the intro line, then one `<span class="tag-sdk">sdk</span>` section per tag with its bullets. Keep a blank line before the first tag span, or markdown renders it inline with the intro.

**Check the feed digest before shipping.** `release-notes.xml` builds a plain-text `<summary>` from the note, because the Slack RSS app prefers `<summary>` over `<content>` and renders only about the first **490 bytes** of it — measured, not documented, so treat it as a ceiling that may move. Notes longer than ~340 characters of prose — most of them — get cut there, and the cut lands wherever it lands.

So for any release whose notes run past that, write a `feed_summary:` override that summarises the whole release inside the budget:

```yaml
feed_summary: |
  sdk

  • DocumentReference now exposes the record a document was generated from.
  • The Assess command rejects a condition belonging to another patient.

  ui

  • A tab left open through an update now offers to reload.
```

Use a YAML block scalar (`|`) so the newlines survive, and write plain text — markup is what gets cut open mid-tag. It is emitted verbatim, so keep it under ~400 characters — the rest of the ~490 bytes goes on the `See full notes:` trailer the feed appends. Over that, the built feed carries an XML comment saying so. Don't hand-wrap the lines: Slack soft-wraps, so your line breaks only spend budget. Confirm with `bundle exec jekyll build` and read the `<summary>` for the entry in `_site/release-notes.xml`.

### API docs (`collections/_api/*.md`)

Frontmatter uses a structured `sections` → `blocks` → `apidoc` format with `attributes`, `search_parameters`, `endpoints`, and example references. These are complex — read an existing file before editing.

### Navigation

Sidebar menus are defined in `_data/menus.yml`. Add entries there when creating new pages.

### Markdown features

- Code blocks: standard fenced blocks with language tag (` ```python `)
- Partial code blocks: ` ```python?partial=true ` — only imports are validated
- Alerts: `{% include alert.html type="warning" content="..." %}`
  - Types: `warning`, `info`, `danger`, `github`
- Tabs (API docs): `{% tabs block-id %}` / `{% tab block-id lang %}` / `{% endtab %}` / `{% endtabs %}`
- Internal links: `[text](/sdk/data-model-name/)`, `[text](/api/resource/)`

## Domain Knowledge

### Identifiers

- **Patient keys** and **staff keys** are UUIDs **without dashes** (e.g., `b80b1cdc2e6a4aca90ccebc02e683f35`). This is unlike most other Canvas identifiers which use standard UUID format with dashes.
- Other IDs (document references, encounters, etc.) use standard UUID format with dashes (e.g., `d2194110-5c9a-4842-8733-ef09ea5ead11`).

### SDK data model patterns

Models follow Django ORM conventions:
- `Model.objects.get(id="...")` — single object by ID
- `Model.objects.filter(field=value)` — queryset filtering
- `Model.objects.for_patient("patient_key")` — patient-scoped queries (key without dashes)
- Related models are linked via foreign keys with `/sdk/data-*` URLs

## Testing

Python code blocks in markdown are validated by `test-code-blocks.py`:
- Extracts fenced Python blocks from all `collections/**/*.md` files
- Validates imports and variable references via AST parsing
- Runs on every PR via GitHub Actions (Python 3.11, 3.12, 3.13)
- Unfenced or unlabeled code blocks are flagged as errors
- Mark blocks as `python?partial=true` if they intentionally omit imports

Run locally:
```sh
uv run ./test-code-blocks.py
```

## CI/CD

- **test-code-blocks.yml** — validates Python code examples on PRs
- **generate-context.yml** — builds AI context files (`sdk-context.txt`, `fhir-context.txt`) on push to main
- **update-algolia.yml** — updates search index
- **merge-release-branch.yml** — auto-merges release branches

## AI / LLM access

The site serves machine-readable copies of its docs for LLMs and coding agents (llmstxt.org convention):
- `/llms.txt` — curated index linking to the `.md` version of each core reference page; release notes and FDB changelogs sit under the droppable `## Optional` section.
- `/llms-full.txt` — the full SDK + FHIR API + guides corpus concatenated as one markdown file.
- `/<page>.md` — a clean-markdown mirror of every content page (append `.md` to any URL, e.g. `/sdk/data-patient.md`).

`generate-llms.py` produces all three into `_site/` after `jekyll build` (wired into `yarn build`, so Amplify emits them on every deploy; they are not committed). The HTML→markdown extraction is shared with `generate-context.py` via `context_extractor.py`.

The older `sdk-context.txt` / `fhir-context.txt` (used by the Canvas Plugin Assistant) are still generated and committed by `generate-context.py`.

## Build

```sh
yarn build          # Production build → _site/ (also emits llms.txt, llms-full.txt, .md mirrors)
yarn build:llms     # Regenerate llms.txt/llms-full.txt/.md mirrors from an existing _site/
yarn build:pwa      # With service worker + manifest
yarn serve:dist     # Serve built output locally
yarn clean:project  # Remove _site and generated assets
```

Algolia index update:
```sh
ALGOLIA_API_KEY='key' bundle exec jekyll algolia --config _config.yml,_config_apikeys.yml
```
