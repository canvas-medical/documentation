---
title: "Note Footer Configuration"
slug: "effect-note-footer-configuration"
excerpt: "Control the visibility of Canvas's default note state-transition buttons in the note footer."
hidden: false
---

The `NoteFooterConfiguration` effect configures the note footer at the note level (rather than per button). Its primary use is hiding Canvas's default state-transition buttons — Lock, Sign, Push charges, Delete, and so on — so that a plugin can supply its own footer buttons in their place, such as with [Note State Action Buttons](/sdk/handlers-action-buttons/#note-state-action-buttons).

Return this effect in response to the `NOTE_FOOTER__GET_CONFIGURATION` event, which fires when a note's footer is loaded. If your handler does not return a configuration, the default state-transition buttons remain visible.

## Attributes

| Attribute                    | Type   | Description                                                                       | Required |
|------------------------------|--------|-----------------------------------------------------------------------------------|----------|
| `hide_default_state_buttons` | `bool` | When `True`, hides Canvas's default state-transition buttons in the note footer. Defaults to `False`. | No       |

## Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note_footer_configuration import NoteFooterConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class HideDefaultFooterButtons(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.NOTE_FOOTER__GET_CONFIGURATION)

    def compute(self) -> list[Effect]:
        return [NoteFooterConfiguration(hide_default_state_buttons=True).apply()]
```
