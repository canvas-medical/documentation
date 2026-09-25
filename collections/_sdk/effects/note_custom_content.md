---
title: "Note Custom Content Effect"
slug: "effect-note-custom-content"
excerpt: "Render your own HTML blocks inside a clinical note, above the note body or within the History, Exam, Assessment & Plan, or Internal sections."
hidden: false
---

The `NoteCustomContent` effect adds a custom content block to a clinical note. Use it to show plugin-generated information where clinicians already work in the note. For example, show a patient summary above the note body or a card inside a note section. A block can be an inline HTML string or the URL of a page your plugin serves.

Return this effect in response to the `NOTE__GET_CUSTOM_CONTENT` event. If no handler returns one, the note renders without custom content.

---

## How it works

When a note renders, Canvas fires `NOTE__GET_CUSTOM_CONTENT` targeting that note. `event.target.id` holds the note's id. A handler subscribed to the event returns one or more `NoteCustomContent` effects, and Canvas renders each block in the section it names.

- **Placement:** Set `section` to place a block at the top of that note section. Leave `section` unset to place the block above the note body.
- **Note views:** Blocks with a `section` appear only while the note is grouped into sections, and are hidden while their section is collapsed. When a user views the whole note instead, or sections are turned off for the instance, only blocks without a `section` appear.
- **Multiple blocks:** A handler can return several effects. Blocks returned for the same section stack in the order the handlers ran.
- **Frames:** Canvas renders each block in its own iframe, so one plugin's block can't reach another's.
- **Sections:** `section` names a section as the note renders it, not the clinical note section of a command. Canvas decides which commands each rendered section gathers, so a plugin that targets a rendered section keeps working if that grouping changes.

### Attributes

| Field     | Type                                  | Default | Description |
|-----------|---------------------------------------|---------|-------------|
| `section` | `NoteCustomContent.Section` or `None` | `None`  | The note section to render the block in. When unset, the block renders above the note body. |
| `url`     | `str`                                 | `None`  | The URL of a page to render in the block, such as a [SimpleAPI](/sdk/handlers-simple-api/) route your plugin serves. |
| `content` | `str`                                 | `None`  | An HTML string to render in the block. |

Set exactly one of `url` or `content`. The effect raises a validation error when both are set or when neither is set.

### Sections

`section` accepts a member of the `NoteCustomContent.Section` enum. Plain strings such as `"exam"` fail validation.

| Member                                      | Section            |
|---------------------------------------------|--------------------|
| `NoteCustomContent.Section.HISTORY`         | History            |
| `NoteCustomContent.Section.EXAM`            | Exam               |
| `NoteCustomContent.Section.ASSESSMENT_PLAN` | Assessment & Plan  |
| `NoteCustomContent.Section.INTERNAL`        | Internal           |

### Choose between `content` and `url`

Use `content` for a static block you can build as an HTML string inside the handler.

Use `url` for a block that updates itself after the note renders. Canvas renders inline `content` in a frame it manages, and a [WebSocket](/sdk/handlers-simple-api-websocket/) opened from that frame receives no messages. A page served from your plugin keeps its WebSocket connection open and can receive `Broadcast` messages. For example, a section card can update its command count when a command is added to the note.

### Permissions for URL blocks

A `url` block's frame receives the permissions your plugin registers for that URL in the `url_permissions` section of `CANVAS_MANIFEST.json`, such as `MICROPHONE` or `ALLOW_SAME_ORIGIN`. The format is the same as for [modals and widgets](/sdk/layout-effect/#additional-configuration). Inline `content` blocks receive no permissions.

### Frame height

Each frame starts 120 pixels tall. To fit the frame to your block, send a `RESIZE` message with the block's height over the message channel Canvas opens with the frame:

```html
<script>
  window.addEventListener('message', (event) => {
    if (event.data?.type !== 'INIT_CHANNEL' || !event.ports?.[0]) {
      return;
    }

    const port = event.ports[0];
    const reportHeight = () =>
      port.postMessage({ type: 'RESIZE', height: document.body.scrollHeight });

    reportHeight();
    new ResizeObserver(reportHeight).observe(document.body);
  });
</script>
```

### Examples

Return an inline block above the note body:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note_custom_content import NoteCustomContent
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class NoteReminder(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.NOTE__GET_CUSTOM_CONTENT)

    def compute(self) -> list[Effect]:
        return [
            NoteCustomContent(
                content="<p>Review the patient's care plan before signing.</p>",
            ).apply()
        ]
```

Return a block for each section, each pointing at a page the plugin serves. Here `/plugin-io/api/my_plugin/section` stands in for a SimpleAPI route in your plugin that returns the block's HTML:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note_custom_content import NoteCustomContent
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler

BASE_URL = "/plugin-io/api/my_plugin"


class SectionCards(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.NOTE__GET_CUSTOM_CONTENT)

    def compute(self) -> list[Effect]:
        note_id = self.event.target.id

        return [
            NoteCustomContent(
                section=section,
                url=f"{BASE_URL}/section?note_id={note_id}&section={section.value}",
            ).apply()
            for section in NoteCustomContent.Section
        ]
```

For a complete plugin that serves its blocks as pages and keeps them current over a WebSocket, see the [`note_custom_content` example plugin](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/note_custom_content).
