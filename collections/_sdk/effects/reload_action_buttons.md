---
title: "Reload Action Buttons Effect"
slug: "effect-reload-action-buttons"
excerpt: "Force a note's or patient's action buttons to be re-evaluated in real time."
hidden: false
---

The reload action button effects let a plugin tell Canvas to recompute and re-render its [action buttons](/sdk/handlers-action-buttons/) without the user reloading the page. This is useful after your plugin changes state that a button's `visible()` method, title, or color depends on, so the displayed buttons reflect the new state.

There are two effects, one for each scope:

- `ReloadNoteActionButtonsEffect` — reloads the action buttons for a single note.
- `ReloadPatientActionButtonsEffect` — reloads the action buttons for a patient.

Emit one from any handler's `compute()` or `handle()` — not only from an `ActionButton`. The effect re-fires the relevant [`SHOW_*_BUTTON`](/sdk/events/#action-buttons-events) events, so every button in that location recomputes `visible()` from scratch: the button set is rebuilt, not patched.

## When to reload

A button's `visible()` result, its title, and its color are all computed from live data each time the location is evaluated. Reloading is how you push those changes to the footer or header without a full page refresh. Common cases:

- **The button has done its job.** Once a button is clicked and its action completes, it often no longer applies — reload so its `visible()` re-evaluates to `False` and the button drops out of the set instead of lingering as a stale, re-clickable control.
- **The label or color should change.** When a button reflects state — a title that shows a count of outstanding items, or a color that turns green once a task is complete — reload after that state changes so the button re-renders with its new title and color.
- **Data the button depends on changed elsewhere.** After a command is committed, a note transitions to a new state, or related records are updated by another handler, reload the location so every button recomputes against the current data.

---

## ReloadNoteActionButtonsEffect

Re-evaluates the note's action buttons in the `NOTE_HEADER`, `NOTE_FOOTER`, and `NOTE_HEADER_DROPDOWN` locations. It also re-reads the note's [footer configuration](/sdk/effect-note-footer-configuration/) (by re-firing `NOTE_FOOTER__GET_CONFIGURATION`), so a plugin that toggles `hide_default_state_buttons` can refresh whether Canvas's native footer buttons are hidden without a full page reload.

### Attributes

| Field | Type  | Description                                                                                       |
|-------|-------|---------------------------------------------------------------------------------------------------|
| `id`  | `str \| UUID` | The external id of a [Note](/sdk/data-note/#note) (`Note.id`). The note must exist, or the effect raises a validation error. |

{% include alert.html type="warning" content="The <code>note_id</code> carried by a <a href='/sdk/events/#action-buttons-events'><code>SHOW_*_BUTTON</code></a> context is the note's <b>database id</b> (<code>dbid</code>), while this effect is keyed by the note's <b>external id</b>. Resolve between them through the <a href='/sdk/data-note/#note'><code>Note</code></a> data model — for example <code>Note.objects.filter(dbid=...).first().id</code>." %}

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

Re-evaluates the patient's action buttons in the `CHART_PATIENT_HEADER` location.

### Attributes

| Field | Type  | Description                                                                       |
|-------|-------|-----------------------------------------------------------------------------------|
| `id`  | `str` | The id of a [Patient](/sdk/data-patient/#patient). The patient must exist, or the effect raises a validation error. |

### Example

This handler refreshes a patient's header buttons whenever one of their tasks changes, so a `CHART_PATIENT_HEADER` button that shows a live count of open tasks stays current as tasks are created or completed:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.action_button import ReloadPatientActionButtonsEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class ReloadPatientButtonsOnTaskChange(BaseHandler):
    RESPONDS_TO = [
        EventType.Name(EventType.TASK_CREATED),
        EventType.Name(EventType.TASK_UPDATED),
    ]

    def compute(self) -> list[Effect]:
        patient_id = (self.event.context.get("patient") or {}).get("id")
        if not patient_id:
            return []
        return [ReloadPatientActionButtonsEffect(id=patient_id).apply()]
```
