---
title: "Note Footer Configuration Effect"
slug: "effect-note-footer-configuration"
excerpt: "Configure a note's footer — for example, hide Canvas's default state-transition buttons."
hidden: false
---

The `NoteFooterConfiguration` effect configures the note footer at the note level (rather than per button). Its primary use is hiding Canvas's default state-transition buttons — Lock, Sign, Push charges, Delete, and so on — so that a plugin can supply its own footer buttons in their place, such as with [Note State Action Buttons](/sdk/handlers-action-buttons/#note-state-action-buttons).

Return this effect in response to the `NOTE_FOOTER__GET_CONFIGURATION` event, which fires when a note's footer is loaded. If your handler does not return a configuration, the default state-transition buttons remain visible.

---

## How it works

As a note's footer loads, Canvas fires `NOTE_FOOTER__GET_CONFIGURATION` targeting that note's external id. A handler subscribed to the event returns a `NoteFooterConfiguration` effect to configure the footer. If no plugin returns one, the footer keeps its default configuration.

### Event payload

| Property          | Value        | Description                                          |
|-------------------|--------------|------------------------------------------------------|
| `event.target.id` | `str` (UUID) | The external id of the [Note](/sdk/data-note/#note) whose footer is loading. |
| `event.actor`     | user         | The logged-in user viewing the note, when available. |
| `event.context`   | `{}`         | Empty — no additional context is provided.           |

### Attributes

| Field                        | Type   | Default | Description                                                         |
|------------------------------|--------|---------|---------------------------------------------------------------------|
| `hide_default_state_buttons` | `bool` | `False` | Hide Canvas's native footer state-transition buttons for this note. |

### Example

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note_footer_configuration import NoteFooterConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class HideDefaultStateButtons(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.NOTE_FOOTER__GET_CONFIGURATION)

    def compute(self) -> list[Effect]:
        return [NoteFooterConfiguration(hide_default_state_buttons=True).apply()]
```
