---
title: "Reload Action Buttons"
slug: "effect-reload-action-buttons"
excerpt: "Programmatically refresh the action buttons shown on a note or patient chart."
hidden: false
---

The reload action button effects let a plugin tell Canvas to recompute and re-render its [action buttons](/sdk/handlers-action-buttons/). This is useful after your plugin changes state that a button's `visible()` method depends on, so the displayed buttons reflect the new state without the user having to reload the page.

There are two effects, one for each scope:

- `ReloadNoteActionButtonsEffect` — reloads the action buttons for a single note.
- `ReloadPatientActionButtonsEffect` — reloads the action buttons for a patient.

## ReloadNoteActionButtonsEffect

Reloads the action buttons rendered for a note (for example, buttons in the `NOTE_HEADER` or `NOTE_FOOTER` locations).

### Attributes

| Attribute | Type  | Description                         | Required |
|-----------|-------|-------------------------------------|----------|
| `id`      | `str` | Identifier of the note to reload    | Yes      |

**Note**: `id` must be a valid, existing Note. Calling `apply()` raises a `ValidationError` if no note with that ID exists.

### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.action_button import ReloadNoteActionButtonsEffect
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        return [ReloadNoteActionButtonsEffect(id="existing-note-uuid").apply()]
```

## ReloadPatientActionButtonsEffect

Reloads the action buttons rendered for a patient (for example, buttons in the `CHART_PATIENT_HEADER` or chart summary section locations).

### Attributes

| Attribute | Type  | Description                          | Required |
|-----------|-------|--------------------------------------|----------|
| `id`      | `str` | Identifier of the patient to reload  | Yes      |

**Note**: `id` must be a valid, existing Patient. Calling `apply()` raises a `ValidationError` if no patient with that ID exists.

### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.action_button import ReloadPatientActionButtonsEffect
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        return [ReloadPatientActionButtonsEffect(id="existing-patient-uuid").apply()]
```
