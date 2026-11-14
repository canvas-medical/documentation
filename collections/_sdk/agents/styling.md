---
title: "Styling Agent Pages"
slug: "agents-styling"
excerpt: "Give an agent's chat or search page the shared agent look with the AGENT_UI_CSS stylesheet."
---

An agent's page, such as a chat or a search in the chart's right pane, is
HTML your plugin serves. `canvas_sdk.agents.ui` gives every agent page the
same look, so a clinician who has used one agent knows how to read the
next: the same panel, transcript, citation chips, and record cards, in the
chart's font and grays.

The module exports two values:

- `AGENT_UI_CSS`: one stylesheet holding the font import, the design
  tokens as `--adk-*` CSS custom properties, and the component classes.
  It is marked safe, so a template outputs it without escaping.
- `TOKENS`: the same token values as a mapping, for code that draws its
  own colors, such as a chart. A plugin can't change it.

## Add the stylesheet to a page

Pass `AGENT_UI_CSS` to the template that renders your page. This route
serves a chat page that a [`LaunchModalEffect`](/sdk/layout-effect/) can
load in the right chart pane:

```python
from http import HTTPStatus

from canvas_sdk.agents.ui import AGENT_UI_CSS
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import HTMLResponse, Response
from canvas_sdk.handlers.simple_api import SimpleAPI, StaffSessionAuthMixin, api
from canvas_sdk.templates import render_to_string


class ChatPage(StaffSessionAuthMixin, SimpleAPI):
    @api.get("/chat")
    def chat(self) -> list[Response | Effect]:
        html = render_to_string("templates/chat.html", {"agent_ui_css": AGENT_UI_CSS})
        return [HTMLResponse(html, status_code=HTTPStatus.OK)]
```

In the template, output the stylesheet in its own `<style>` element and
wrap the page in `adk-panel`:

{% raw %}

```html
<style>{{ agent_ui_css }}</style>
<style>/* Your plugin's own styles */</style>

<div class="adk-panel">
  <div class="adk-header">
    <div class="adk-title">Ask AI</div>
  </div>
  <div class="adk-body">
    <div class="adk-msg adk-msg-user">
      <div class="adk-msg-icon"><span class="adk-author">JD</span></div>
      <div class="adk-msg-body">What's this patient's A1c history?</div>
    </div>
    <div class="adk-msg adk-msg-agent">
      <div class="adk-msg-icon">●</div>
      <div class="adk-msg-body">
        <p>The last three results are trending down. <button class="adk-cite">1</button></p>
      </div>
    </div>
  </div>
</div>
```

{% endraw %}

The stylesheet starts with an `@import` of Lato, the chart's font. A
browser ignores an `@import` that follows any other rule in the same
stylesheet, which is why your own styles go in a separate `<style>`
element. The page loads in an iframe, so it doesn't inherit the fonts
the chart has already loaded.

`adk-panel` sets the font, text color, and background for everything
inside it, so put the rest of the page's markup inside that element.

## Components

Every class starts with `adk-` (Agent Development Kit), so none collides
with your plugin's own CSS.

| Component | Classes |
|---|---|
| Panel and tabs | `adk-panel`, `adk-header`, `adk-title`, `adk-tabs`, `adk-tab`, `adk-body`, `adk-section-label`, `adk-count` |
| Chat transcript | `adk-msg`, `adk-msg-user`, `adk-msg-agent`, `adk-msg-icon`, `adk-msg-body`, `adk-author`, `adk-answer` |
| Citation chip | `adk-cite` |
| Record card | `adk-records`, `adk-record`, `adk-record-head`, `adk-kind`, `adk-record-title`, `adk-record-state`, `adk-record-summary`, `adk-record-why`, `adk-record-details`, `adk-record-foot`, `adk-open` |
| Sources list | `adk-sources`, `adk-sources-head`, `adk-sources-chev` |
| Run status | `adk-thinking`, `adk-thinking-dot`, `adk-steps` with `adk-done` or `adk-running` on each item, `adk-status` with `adk-critical` or `adk-warning`, `adk-status-title`, `adk-status-sub`, `adk-status-actions` |
| Starter prompts | `adk-greet`, `adk-greet-title`, `adk-greet-sub`, `adk-starters`, `adk-starter`, `adk-starter-top`, `adk-starter-desc`, `adk-ico`, `adk-chips`, `adk-chip` |
| Input bar and actions | `adk-actions`, `adk-action`, `adk-input-area`, `adk-input-wrap`, `adk-input`, `adk-send`, `adk-disclaimer`, `adk-reply-actions`, `adk-icon-btn`, `adk-feedback-reason`, `adk-text-input` |
| Buttons | `adk-btn`, `adk-btn-primary`, `adk-btn-sm`, `adk-link-btn`, `adk-badge` |
| Keyword search | `adk-search-row`, `adk-field`, `adk-filters`, `adk-filter-label`, `adk-filter-grid`, `adk-toggle-chip`, `adk-results-bar`, `adk-empty`, `adk-empty-title` |
| Agent note | `adk-note`, `adk-note-agent` |
| Status text | `adk-good`, `adk-warning`, `adk-critical` |

Interactive states follow ARIA attributes rather than extra classes:

- `aria-selected="true"` on an `adk-tab` marks the open tab.
- `aria-current="true"` on an `adk-cite` or an `adk-record` marks the
  selected reference.
- `aria-pressed="true"` on an `adk-icon-btn` or an `adk-toggle-chip`
  shows it pressed.
- `aria-expanded="true"` on `adk-sources` turns its chevron to show the list as open. Showing and hiding the list is up to your page.

To color a person's initials in the transcript, set `--adk-author` inline
on their `adk-author` element, for example
`style="--adk-author: #4a5565"`. Without it, initials sit on gray.

The layout fits the right chart pane, which is a quarter of the page
(360px on a 1440px screen). When the panel is narrower than 400px, a
record card's title takes its own line, the quick actions wrap, and the
starter prompts stack in one column. The thinking dot and running steps
stop pulsing when the reader's system asks for reduced motion.

## What each color means

Each color has one meaning, so a reader can tell what the agent made from
what they can act on:

| Token | Value | Use it for |
|---|---|---|
| `agent` | `#8041d0` (purple) | What the agent made: its transcript dot, citation numbers, the thinking dot, a selected reference, an agent note |
| `action` | `#155dfc` (blue) | What the reader can act on or go to: links, **Open**, send, primary buttons, pressed controls |
| `good`, `warning`, `critical` | `#047857`, `#8a5a00`, `#b42323` | Status, always beside a word that says the status |
| `text`, `text-secondary`, `border`, and the `bg` tokens | Gray scale | Everything else |

Keep to that split in your own markup. A button or link in purple reads
as something the agent produced. Every text color in the stylesheet
meets WCAG AA contrast on the backgrounds it's paired with.

## Use the tokens in your own code

In CSS, refer to a token as `var(--adk-<name>)`, for example
`var(--adk-agent)` or `var(--adk-radius)`. In Python, read the same value
from `TOKENS`, for example to color a chart the page draws:

```python
from canvas_sdk.agents.ui import TOKENS

chart_spec = {
    "mark": {"type": "line", "color": TOKENS["agent"]},
    "config": {"font": TOKENS["font"], "axis": {"labelColor": TOKENS["text-secondary"]}},
}
```

`TOKENS` holds the font stacks (`font`, `mono`), font sizes (`font-size`,
`font-size-sm`, `font-size-xs`), corner radii (`radius-sm`, `radius`,
`radius-pill`), the colors in the table above with their `-fg` and
`-soft` variants, and two shadows (`shadow`, `shadow-raised`).
