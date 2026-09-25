---
title: "Note Custom Content"
slug: "note-custom-content-effect"
excerpt: "Effect for rendering custom content inside a note."
hidden: false
---

## Overview

The `NoteCustomContent` effect renders plugin-supplied content inside a note. Return it from a handler responding to `NOTE__GET_CUSTOM_CONTENT`, which Canvas fires once per note to ask what the note should show.

Content can be an inline HTML string or a URL to a hosted page, and is rendered in its own iframe. `section` names where in the note it belongs; leaving it unset places the content at the top of the note, above the body.

Canvas asks each handler once per note rather than once per section, so a handler returns everything it wants to place in one pass. Several handlers can contribute to the same section, and everything returned for a section stacks in the order the handlers ran. Each contribution gets its own iframe, so one plugin's content cannot reach another's.

```python
from canvas_sdk.effects.note_custom_content import NoteCustomContent
from canvas_sdk.templates import render_to_string


# At the top of the note
NoteCustomContent(content=render_to_string("templates/banner.html"))

# Inside one of the note's sections
NoteCustomContent(
    section=NoteCustomContent.Section.ASSESSMENT_PLAN,
    url="/plugin-io/api/my_plugin/risk-summary",
)
```

## Structure

### Attributes

| Attribute | Required                                | Type                | Description                                                                                          |
|-----------|-----------------------------------------|---------------------|------------------------------------------------------------------------------------------------------|
| `section` | optional                                | `Section` \| `None` | The section of the note to render the content in. Unset renders it at the top of the note.            |
| `content` | required (if `url` is not provided)     | `str` \| `None`     | Inline HTML to render. Mutually exclusive with `url`.                                                 |
| `url`     | required (if `content` is not provided) | `str` \| `None`     | URL of the page to load in the iframe. Mutually exclusive with `content`.                             |

### Sections

`section` names a section the note renders, not a command's clinical note section. Which commands a section gathers is Canvas's to decide, so a plugin targeting `ASSESSMENT_PLAN` keeps working whichever commands that section comes to hold.

| Member                     | Section        |
|----------------------------|----------------|
| `Section.HISTORY`          | History        |
| `Section.EXAM`             | Exam           |
| `Section.ASSESSMENT_PLAN`  | Assessment & Plan |
| `Section.INTERNAL`         | Internal       |

### Validation

Exactly one of `content` / `url` must be provided. Providing both or neither raises a `ValidationError`. `section`, when given, must be a `Section` member rather than a string.

### Permissions

Content served from a `url` is framed with the permissions the plugin registered for that URL in its `CANVAS_MANIFEST.json`, the same way a [custom chart section](/sdk/patient-chart-summary-custom-section-effect/) or an application is. Inline `content` has no origin, so it is granted none.

### Keeping content current

Canvas draws each contribution once. To keep it live, hold the state in the browser and push updates over a [WebSocket](/sdk/handlers-simple-api/) of your own with a [`Broadcast`](/sdk/effect-simple-api/) effect, rather than expecting Canvas to ask for the content again.

### Height

A frame starts at a default height and grows to whatever its content reports. To report a height, post a `RESIZE` message over the channel Canvas opens with the frame:

{% raw %}
```html
<script>
  window.addEventListener('message', event => {
    if (event.data?.type !== 'INIT_CHANNEL') {
      return;
    }

    const port = event.ports[0];
    const report = () =>
      port.postMessage({ type: 'RESIZE', height: document.body.scrollHeight });

    report();
    new ResizeObserver(report).observe(document.body);
  });
</script>
```
{% endraw %}

## Examples

### A banner above the note

The note's identifier arrives as `self.target`, and the logged-in user as `self.actor`.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note_custom_content import NoteCustomContent
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.templates import render_to_string


class NoteBanner(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.NOTE__GET_CUSTOM_CONTENT)]

    def compute(self) -> list[Effect]:
        return [NoteCustomContent(content=render_to_string("templates/banner.html")).apply()]
```

### Content in several sections at once

One handler places content wherever it likes in a single pass.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note_custom_content import NoteCustomContent
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data.note import Note


class VisitContext(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.NOTE__GET_CUSTOM_CONTENT)]

    def compute(self) -> list[Effect]:
        note = Note.objects.get(id=self.target)

        return [
            NoteCustomContent(
                section=NoteCustomContent.Section.HISTORY,
                content=render_to_string(
                    "templates/prior_visits.html",
                    {"patient_id": note.patient.id},
                ),
            ).apply(),
            NoteCustomContent(
                section=NoteCustomContent.Section.ASSESSMENT_PLAN,
                url="/plugin-io/api/my_plugin/risk-summary",
            ).apply(),
        ]
```
