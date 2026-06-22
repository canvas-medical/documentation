---
title: "Reload Action Buttons Effect"
slug: "effect-reload-action-buttons"
excerpt: "Force a note's or patient's action buttons to be re-evaluated in real time."
hidden: false
---

`ReloadNoteActionButtonsEffect` and `ReloadPatientActionButtonsEffect` re-evaluate every [action button](/sdk/handlers-action-buttons/) bound to a note or a patient. Because a button's `visible()` method runs against live data each time its location loads, these effects let you refresh that location when something *else* changes — for example, after a command is committed or a note transitions to a new state.

Emit one from any handler's `compute()` or `handle()` — not only from an `ActionButton`. The effect re-fires the relevant `SHOW_*_BUTTON` events, so every button in that location recomputes `visible()` from scratch: the button set is rebuilt, not patched.

---

## ReloadNoteActionButtonsEffect

Re-evaluates every button bound to a note.

### Fields

| Field | Type  | Description                                                                                       |
|-------|-------|---------------------------------------------------------------------------------------------------|
| `id`  | `str` | The note's external id (`Note.id`). The note must exist, or the effect raises a validation error. |

> The `note_id` carried by a `SHOW_*_BUTTON` context is the note's **database id** (`dbid`), while this effect is keyed by the note's **external id**. Resolve between them through the `Note` data model — for example `Note.objects.filter(dbid=...).first().id`.

### Example

This handler reloads a note's footer whenever any command is committed, so a button that hides while the note has uncommitted commands reappears the moment the last one is committed:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.action_button import ReloadNoteActionButtonsEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.command import Command


class ReloadFooterOnCommandCommit(BaseHandler):
    RESPONDS_TO = [
        EventType.Name(value)
        for value in EventType.values()
        if EventType.Name(value).endswith("_COMMAND__POST_COMMIT")
    ]

    def compute(self) -> list[Effect]:
        command = Command.objects.filter(id=self.event.target.id).first()
        if not command or not command.note:
            return []
        return [ReloadNoteActionButtonsEffect(id=str(command.note.id)).apply()]
```

## ReloadPatientActionButtonsEffect

Re-evaluates every button bound to a patient — for example, buttons in the patient chart header or in chart-summary sections.

### Fields

| Field | Type  | Description                                                                       |
|-------|-------|-----------------------------------------------------------------------------------|
| `id`  | `str` | The patient's id. The patient must exist, or the effect raises a validation error. |

### Example

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.action_button import ReloadPatientActionButtonsEffect
from canvas_sdk.handlers.base import BaseHandler


class ReloadPatientButtons(BaseHandler):
    # Respond to whatever should refresh the patient's buttons.
    RESPONDS_TO: list[str] = []

    def compute(self) -> list[Effect]:
        patient_id = self.event.context.get("patient_id")
        if not patient_id:
            return []
        return [ReloadPatientActionButtonsEffect(id=patient_id).apply()]
```
