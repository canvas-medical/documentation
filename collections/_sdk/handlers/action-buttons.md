---
title: "Action Buttons"
slug: "handlers-action-buttons"
excerpt: "Create and modify views in the Canvas UI."
hidden: false
---

Action buttons are UI elements that trigger specific actions when clicked in the Canvas UI. These buttons can be placed in different locations and can interact with runtime data to execute custom code.

## Overview
  
An `ActionButton` class allows you to define custom buttons that appear in different sections of the Canvas UI. When a user clicks the button, the action associated with the button is executed. Action buttons can be added to various locations in the UI, and you can control their visibility and behavior through effects in a handler class.

There are no limitations on the number of action buttons you can create. You can define multiple buttons in a single handler class or create separate classes for each button.

## Creating an action button

An action button is a [handler](/sdk/handlers-basehandler/). Subclass `ActionButton`, say
where it goes with `BUTTON_LOCATION`, and implement `handle()` to say what a click does:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.action_button import ActionButton


class PatientSummaryButton(ActionButton):
    BUTTON_TITLE = "Summary"
    BUTTON_KEY = "PATIENT_SUMMARY"
    BUTTON_LOCATION = ActionButton.ButtonLocation.CHART_PATIENT_HEADER

    def handle(self) -> list[Effect]:
        return [
            LaunchModalEffect(
                target=LaunchModalEffect.TargetType.DEFAULT_MODAL,
                content="<html>Your content here</html>",
            ).apply()
        ]
```

Then register the class under `handlers` in your `CANVAS_MANIFEST.json`:

```json
{
  "components": {
    "handlers": [
      {
        "class": "my_plugin.buttons.patient_summary:PatientSummaryButton",
        "description": "Shows a summary modal from the patient header."
      }
    ]
  }
}
```

### Class attributes

| Attribute                 | Required | Description                                                                                                                                              |
|---------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `BUTTON_TITLE`            | Required | The label shown on the button. Emoji are supported.                                                                                                      |
| `BUTTON_KEY`              | Required | A unique identifier for the button. Canvas routes the click back to your `handle()` by this value, so give each button its own.                           |
| `BUTTON_LOCATION`         | Required | Where the button appears, as a [`ButtonLocation`](#button-locations) value.                                                                               |
| `PRIORITY`                | Optional | Orders this button against others in the same location, lower first. Defaults to `0`, and buttons sharing a priority have no guaranteed order.            |
| `BUTTON_TEXT_COLOR`       | Optional | The label colour as a HEX value, for example `"#FF0000"`. Defaults to whichever of black or white contrasts with the background.                          |
| `BUTTON_BACKGROUND_COLOR` | Optional | The background colour as a HEX value, for example `"#4CAF50"`. Defaults to Canvas's grey button styling.                                                  |

### Methods

| Method      | Returns        | Required | Description                                                                                                                                                    |
|-------------|----------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `handle()`  | `list[Effect]` | Required | Runs when the button is clicked. Return the [effects](/sdk/effects/) the click should produce, or an empty list for none.                                        |
| `visible()` | `bool`         | Optional | Runs each time the button's location loads, to decide whether the button is shown. Defaults to `True`. See [Dynamic, state-responsive buttons](#dynamic-state-responsive-buttons). |

```python?partial=true
    def visible(self) -> bool:
        """Only offer the button on an encounter note."""
        note_id = self.event.context.get("note_id")
        note = Note.objects.filter(dbid=note_id).first()

        return note is not None and note.note_type_version.category == "encounter"
```

### Button locations

The `ActionButton` class defines several locations where the button can be placed. The location is defined using the `ButtonLocation` enum. Supported button locations include:

| **Location**                                | **Description**                                                                 |
|---------------------------------------------|---------------------------------------------------------------------------------|
| `NOTE_HEADER`                               | The button will appear in the header of each note.                              |
| `NOTE_FOOTER`                               | The button will appear in the footer of each note.                              |
| `NOTE_HEADER_DROPDOWN`                      | The button will appear in the note header dropdown.                             |
| `CHART_PATIENT_HEADER`                      | The button will appear in the patient header on both the chart and profile pages. |
| `CHART_SUMMARY_SOCIAL_DETERMINANTS_SECTION` | The button will appear in the Social Determinants section of the chart summary. |
| `CHART_SUMMARY_GOALS_SECTION`               | The button will appear in the Goals section of the chart summary.               |
| `CHART_SUMMARY_CONDITIONS_SECTION`          | The button will appear in the Conditions section of the chart summary.          |
| `CHART_SUMMARY_MEDICATIONS_SECTION`         | The button will appear in the Medications section of the chart summary.         |
| `CHART_SUMMARY_ALLERGIES_SECTION`           | The button will appear in the Allergies section of the chart summary.           |
| `CHART_SUMMARY_CARE_TEAMS_SECTION`          | The button will appear in the Care Teams section of the chart summary.          |
| `CHART_SUMMARY_VITALS_SECTION`              | The button will appear in the Vitals section of the chart summary.              |
| `CHART_SUMMARY_IMMUNIZATIONS_SECTION`       | The button will appear in the Immunizations section of the chart summary.       |
| `CHART_SUMMARY_SURGICAL_HISTORY_SECTION`    | The button will appear in the Surgical History section of the chart summary.    |
| `CHART_SUMMARY_FAMILY_HISTORY_SECTION`      | The button will appear in the Family History section of the chart summary.      |
| `CHART_SUMMARY_CODING_GAPS_SECTION`         | The button will appear in the Coding Gaps section of the chart summary.         |
| `NOTE_BODY_AUTOMATION`                      | The button appears as an entry in the note body's "/" (slash) command list while a clinician documents a note. |


## Dynamic, state-responsive buttons

Action buttons are not rendered once and cached. Canvas re-evaluates every `ActionButton` handler each time its location loads — and again whenever the location is [reloaded](#reloading-buttons). On each evaluation Canvas fires the [`SHOW_*_BUTTON`](/sdk/events/#action-buttons-events) event for that location and your handler's `visible()` method decides whether the button is included.

This is what makes buttons *dynamic*: because `visible()` runs against live data every time, the same button can appear, disappear, or change its title depending on the note, the patient, or the logged-in user.

### Reading the runtime context

Inside `visible()`, `compute()`, and `handle()` you can read the event context to make decisions. When responding to a [`SHOW_*_BUTTON`](/sdk/events/#action-buttons-events) event, the following are available:

| Accessor                        | Description                                                                                                                                    |
|---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `self.event.context["note_id"]` | The **database id** of the note the button is rendered for (note locations only). Look the note up with `Note.objects.filter(dbid=...)`.       |
| `self.event.context["user"]`    | The logged-in user, as `{"type": "Staff", "id": "<staff-id>"}`. Use `self.event.context["user"]["id"]` to compare against staff in your data. |
| `self.event.target.id`          | The id of the patient the button is rendered for.                                                                                             |

### Reloading buttons

Because visibility is computed from live data, Canvas needs to know *when* to re-evaluate it. A button's location is reloaded automatically after its own `handle()` runs, but you will often want to reload in response to something else changing — for example, recomputing the footer after a command is committed, or after the note transitions to a new state.

Return one of these [Reload Action Buttons](/sdk/effect-reload-action-buttons/) effects (imported from `canvas_sdk.effects.action_button`) from any handler's `handle()` or `compute()` to refresh a location's buttons:

| Effect                                            | Re-evaluates                               |
|---------------------------------------------------|--------------------------------------------|
| `ReloadNoteActionButtonsEffect(id=<note id>)`     | Every button bound to that note            |
| `ReloadPatientActionButtonsEffect(id=<patient id>)` | Every button bound to that patient       |

A reload re-fires the [`SHOW_*_BUTTON`](/sdk/events/#action-buttons-events) events, so every button recomputes `visible()` from scratch — the button set is rebuilt rather than patched. Any handler can emit a reload, not just an `ActionButton`; Example 4 below uses plain event handlers to keep the footer in sync as the note changes.


## Note body automations

A note body automation adds your plugin's own entry to the note body's "/" (slash) command list — the inline list clinicians use to insert commands while documenting a note. When the clinician selects your entry, your `handle()` runs and returns effects, just as a native slash command inserts commands.

This location exists so an automation can come from a plugin rather than only from Canvas. An entry here is an ordinary action button, so `handle()` may return any effects at all: launch a modal, write a log line, or return nothing. What it is intended for is originating [commands](/sdk/commands/), with one menu entry standing in for the several commands a workflow would otherwise have the clinician insert by hand. Either way, Canvas clears the line the trigger was typed on, so an entry that originates nothing simply leaves the note as it was.

Build one exactly as you build any other action button. Subclass `ActionButton`, set `BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_BODY_AUTOMATION`, and provide the [`BUTTON_TITLE`, `BUTTON_KEY` and `PRIORITY`](#class-attributes) attributes. Implement [`handle()`](#methods) to build and return the effects your entry produces, and override [`visible()`](#methods) to scope who sees the entry and where. Its [runtime context](#reading-the-runtime-context) carries the signed-in staff member alongside the note and the patient, so an entry can be limited to particular staff as well as to particular notes or patients.

`NOTE_BODY_AUTOMATION` reuses the generic `ActionButton` handler — a note body automation is a regular `ActionButton` subclass using this location, with no separate automation class. Canvas asks each plugin for its note body automation entries through the [`SHOW_NOTE_BODY_AUTOMATION_BUTTON`](/sdk/events/#action-buttons-events) event.

Canvas renders the "/" experience for the clinician. Your entry appears in the list after the native commands, marked with a plug icon that distinguishes it from Canvas's native automations, and sorted by `PRIORITY` then title. Canvas populates the list when the note loads — not on every keystroke — then filters it client-side by `BUTTON_TITLE` as the clinician types. Selecting your entry runs `handle()`.

To make an entry behave like a native slash command, return a [`BatchOriginateCommandEffect`](/sdk/effect-batch-originate/) with `replace_line=True` from `handle()`. In the note body "/" flow, Canvas supplies the trigger-line position and places the originated commands on the line the clinician typed the trigger on, replacing that line and leaving no trailing trigger text or blank-line padding. You don't set `line_number` for an automation — Canvas handles the placement, so `replace_line=True` is all `handle()` needs to set.

Use `BatchOriginateCommandEffect` whenever an entry originates **more than one** command. The batch updates the note body one time for the whole group, instead of one time per command. That is faster, and it also keeps the group together: separate originate effects each update the note on their own, so they can interleave with other writes and land out of order. An entry that originates a single command needs no batch — return that command's `originate()` instead.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.batch_originate import BatchOriginateCommandEffect
from canvas_sdk.commands import PlanCommand
from canvas_sdk.handlers.action_button import ActionButton
from canvas_sdk.v1.data.note import Note


class LipidPanelAutomation(ActionButton):
    BUTTON_TITLE = "Order lipid panel follow-up"
    BUTTON_KEY = "LIPID_PANEL_AUTOMATION"
    BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_BODY_AUTOMATION

    def visible(self) -> bool:
        # Scope the entry to the note's provider.
        note_id = self.event.context.get("note_id")
        user_id = (self.event.context.get("user") or {}).get("id")
        if not note_id or not user_id:
            return False

        note = Note.objects.filter(dbid=note_id).first()
        return note is not None and note.provider.id == user_id

    def handle(self) -> list[Effect]:
        note_id = self.event.context["note_id"]
        note = Note.objects.filter(dbid=note_id).first()
        if note is None:
            return []

        plan = PlanCommand()
        plan.note_uuid = note.id
        plan.narrative = "Order labs for lipid panel"

        return [
            BatchOriginateCommandEffect(
                commands=[plan],
                replace_line=True,
            ).apply()
        ]
```


## Examples

### Log information when a button is clicked

This example demonstrates a simple action button that logs some information when clicked. The button is visible only during the month of January.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.handlers.action_button import ActionButton
from datetime import datetime
from logger import log


class MyButton(ActionButton):
    BUTTON_TITLE = "🪵 Log Action"
    BUTTON_KEY = "LOG_ACTION"
    BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_HEADER

    def visible(self) -> bool:
        # Only show this button in January
        return datetime.now().month == 1

    def handle(self) -> list[Effect]:
        log.info("Button clicked!")
        log.info(self.event.context)
        log.info(self.event.target)

        return []
```

### Commit every command in a note

This example demonstrates an action button in the note footer that commits all commands within a note. The button is always visible since the `visible()` method is not overridden.

```python
import json

from canvas_sdk.effects import Effect
from canvas_sdk.handlers.action_button import ActionButton
from canvas_sdk.v1.data.command import Command
from canvas_sdk.effects.base import EffectType

# Define a mapping of schema_key to EffectType
schema_key_to_effect_type = {
    "allergy": EffectType.COMMIT_ALLERGY_COMMAND,
    "assess": EffectType.COMMIT_ASSESS_COMMAND,
    "changeMedication": EffectType.COMMIT_CHANGE_MEDICATION_COMMAND,
    "closeGoal": EffectType.COMMIT_CLOSE_GOAL_COMMAND,
    "diagnose": EffectType.COMMIT_DIAGNOSE_COMMAND,
    "familyHistory": EffectType.COMMIT_FAMILY_HISTORY_COMMAND,
    "goal": EffectType.COMMIT_GOAL_COMMAND,
    "instruct": EffectType.COMMIT_INSTRUCT_COMMAND,
    "hpi": EffectType.COMMIT_HPI_COMMAND,
    "medicalHistory": EffectType.COMMIT_MEDICAL_HISTORY_COMMAND,
    "medicationStatement": EffectType.COMMIT_MEDICATION_STATEMENT_COMMAND,
    "perform": EffectType.COMMIT_PERFORM_COMMAND,
    "plan": EffectType.COMMIT_PLAN_COMMAND,
    "questionnaire": EffectType.COMMIT_QUESTIONNAIRE_COMMAND,
    "reasonForVisit": EffectType.COMMIT_REASON_FOR_VISIT_COMMAND,
    "removeAllergy": EffectType.COMMIT_REMOVE_ALLERGY_COMMAND,
    "stopMedication": EffectType.COMMIT_STOP_MEDICATION_COMMAND,
    "surgicalHistory": EffectType.COMMIT_SURGICAL_HISTORY_COMMAND,
    "task": EffectType.COMMIT_TASK_COMMAND,
    "updateDiagnosis": EffectType.COMMIT_UPDATE_DIAGNOSIS_COMMAND,
    "updateGoal": EffectType.COMMIT_UPDATE_GOAL_COMMAND,
    "vitals": EffectType.COMMIT_VITALS_COMMAND,
}

class CommitButtonHandler(ActionButton):
    BUTTON_TITLE = "Commit all commands"
    BUTTON_KEY = "COMMIT_ALL_COMMANDS"
    BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_FOOTER

    def handle(self) -> list[Effect]:
        note_id = self.context.get("note_id")

        effects = []
        for command in Command.objects.filter(note_id=note_id):
            effect_type = schema_key_to_effect_type.get(command.schema_key)
            if not effect_type:
                raise ValueError(f"No EffectType defined for schema key '{command.schema_key}'.")

            effects.append(
                Effect(
                    type=effect_type,
                    payload=json.dumps({"command": str(command.id)}),
                )
            )

        return effects
```

### Render HTML from a chart summary section

In this example, we place a button in the Vitals section and define an action where the button, when clicked,  displays custom HTML content to the user. 
For more info about `LaunchModalEffect`, check the [documentation](/sdk/layout-effect/#modals).

```python
from canvas_sdk.effects import Effect
from canvas_sdk.handlers.action_button import ActionButton
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from logger import log


class VitalsButtonHandler(ActionButton):
    BUTTON_TITLE = "📊 Show Vitals Info"
    BUTTON_KEY = "SHOW_VITALS_INFO"
    BUTTON_LOCATION = ActionButton.ButtonLocation.CHART_SUMMARY_VITALS_SECTION

    def handle(self) -> list[Effect]:
        # This method will be called when the button is clicked
        log.info("Vitals info button clicked!")

        # Custom HTML content to display
        custom_html = """
        <div style="padding: 20px; background-color: #f0f8ff; border-radius: 5px;">
            <h3>Vitals Information</h3>
            <p>Patient's latest vitals data:</p>
            <ul>
                <li>Heart Rate: 72 bpm</li>
                <li>Blood Pressure: 120/80 mmHg</li>
                <li>Respiratory Rate: 16 breaths/min</li>
                <li>Temperature: 98.6°F</li>
            </ul>
            <p>For more details, please refer to the full report.</p>
        </div>
        """

        # Return a LaunchModalEffect to show the custom HTML content in a modal
        return [LaunchModalEffect(
            target=LaunchModalEffect.TargetType.DEFAULT_MODAL,
            content=custom_html
        ).apply()]

    def visible(self) -> bool:
        # Optionally, make the button visible only under specific conditions
        return True
```

## Note state action buttons

`NoteStateActionButton` is a specialized `ActionButton` subclass for note footer buttons that transition a note from one state to another — locking, signing, pushing charges, deleting, and discharging, along with the appointment transitions check in, no show, cancel, and restore. It handles visibility, ordering, and the underlying state-transition effect for you, so a plugin can replace Canvas's default footer buttons with its own.

To create one, subclass `NoteStateActionButton` and set the `STATE_ACTION` class attribute to the target [`NoteStates`](/sdk/data-note/#notestates) value the button should transition the note into. Locking and signing carry extra rules, so the SDK also ships two ready-to-use subclasses — `LockNoteActionButton` and `SignNoteActionButton` — that you can register directly (or subclass) instead of setting `STATE_ACTION` yourself:

```python
from canvas_sdk.handlers.action_button import (
    LockNoteActionButton,
    NoteStateActionButton,
    SignNoteActionButton,
)
from canvas_sdk.v1.data.note import NoteStates


# Lock and Sign subclass the specialized bases — STATE_ACTION and their extra
# rules are already set on those classes.
class LockNoteButton(LockNoteActionButton):
    pass


class SignNoteButton(SignNoteActionButton):
    pass


# Every other transition subclasses NoteStateActionButton and sets STATE_ACTION.
class UnlockNoteButton(NoteStateActionButton):
    STATE_ACTION = NoteStates.UNLOCKED


class PushChargesNoteButton(NoteStateActionButton):
    STATE_ACTION = NoteStates.PUSHED


class CheckInAppointmentButton(NoteStateActionButton):
    STATE_ACTION = NoteStates.CONVERTED


class NoShowAppointmentButton(NoteStateActionButton):
    STATE_ACTION = NoteStates.NOSHOW


class CancelAppointmentButton(NoteStateActionButton):
    STATE_ACTION = NoteStates.CANCELLED


class RestoreAppointmentButton(NoteStateActionButton):
    STATE_ACTION = NoteStates.REVERTED


class DeleteNoteButton(NoteStateActionButton):
    STATE_ACTION = NoteStates.DELETED


class RestoreNoteButton(NoteStateActionButton):
    STATE_ACTION = NoteStates.UNDELETED


class DischargeNoteButton(NoteStateActionButton):
    STATE_ACTION = NoteStates.DISCHARGED
```

Register each button as a handler in your `CANVAS_MANIFEST.json`, exactly like any other `ActionButton`.

Each button is configured automatically from its `STATE_ACTION`, so a subclass normally
sets nothing else:

| Attribute         | Value                                                                                                              |
|-------------------|--------------------------------------------------------------------------------------------------------------------|
| `BUTTON_LOCATION` | Always `NOTE_FOOTER`. Not overridable.                                                                             |
| `BUTTON_TITLE`    | An imperative label for the target state, from the table below. Set it explicitly to override.                     |
| `BUTTON_KEY`      | `note_state_action__<state value>`, for example `note_state_action__LKD`. Set it explicitly to override.            |
| `visible()`       | Implemented by the base class, which shows the button only when the transition is permitted. See [Visibility](#visibility). |

These are the supported transitions:

| `STATE_ACTION`             | Subclass                  | Default title  | Default key                |
|----------------------------|---------------------------|----------------|----------------------------|
| `NoteStates.LOCKED`        | `LockNoteActionButton`    | `Lock`         | `note_state_action__LKD`   |
| `NoteStates.SIGNED`        | `SignNoteActionButton`    | `Sign`         | `note_state_action__SGN`   |
| `NoteStates.UNLOCKED`      | `NoteStateActionButton`   | `Unlock`       | `note_state_action__ULK`   |
| `NoteStates.PUSHED`        | `NoteStateActionButton`   | `Push charges` | `note_state_action__PSH`   |
| `NoteStates.DISCHARGED`    | `NoteStateActionButton`   | `Discharge`    | `note_state_action__DSC`   |
| `NoteStates.DELETED`       | `NoteStateActionButton`   | `Delete`       | `note_state_action__DLT`   |
| `NoteStates.UNDELETED`     | `NoteStateActionButton`   | `Restore`      | `note_state_action__UND`   |
| `NoteStates.CONVERTED`     | `NoteStateActionButton`   | `Check in`     | `note_state_action__CVD`   |
| `NoteStates.NOSHOW`        | `NoteStateActionButton`   | `No show`      | `note_state_action__NSW`   |
| `NoteStates.CANCELLED`     | `NoteStateActionButton`   | `Cancel`       | `note_state_action__CLD`   |
| `NoteStates.REVERTED`      | `NoteStateActionButton`   | `Restore`      | `note_state_action__RVT`   |

`Cancel` and `Restore` act on the note's appointment rather than on the note itself, so
they do nothing on a note that has no appointment. `Sign` locks the note first when it
is not already locked.

When a button is clicked, Canvas applies the transition's effect and reloads the footer
so it reflects the note's new state.

### Visibility

A `NoteStateActionButton` appears only when its `STATE_ACTION` is a permitted transition from the note's current state and note type, so you don't need to override `visible()` yourself. When several are visible at once, Canvas orders them to match the order it offers the transitions for the current state.

Three buttons carry extra gates on top of that, which the base class applies for you:

| Button                 | Also shown only when                                                                                   |
|------------------------|--------------------------------------------------------------------------------------------------------|
| `LockNoteActionButton` | The note type does **not** require a signature                                                          |
| `SignNoteActionButton` | The note type **does** require a signature, and the current user has not signed since the last lock     |
| `Discharge`            | The note type is an inpatient one                                                                       |

Lock and Sign are the same underlying transition, split by whether the note type requires
a signature. Because Sign hides itself only for the user who signed, a note can be signed
by several users in turn, and it is re-locked only after an amend.

### Replacing Canvas's default footer buttons

Your state buttons appear *alongside* Canvas's built-in state-transition buttons by default. To hide the native ones so yours replace them, answer the `NOTE_FOOTER__GET_CONFIGURATION` event with a [`NoteFooterConfiguration`](/sdk/effect-note-footer-configuration/) effect. Footer suppression is configured once per note (not per button):

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

### Customizing when a button appears

Override `visible()` to layer your own rules on top of the built-in checks — call `super().visible()` first so you keep everything the base already enforces, then add your conditions. Subclassing `SignNoteActionButton` means `super().visible()` still applies the sign-specific rules (signature-required, lock-first, and already-signed). This Sign button additionally hides itself while the note has staged (uncommitted) commands, because a note can't be signed until its commands are committed (reason-for-visit is auto-managed and doesn't block signing, so it's excluded):

```python
from canvas_sdk.handlers.action_button import SignNoteActionButton
from canvas_sdk.v1.data.command import Command


class SignNoteButton(SignNoteActionButton):
    def visible(self) -> bool:
        if not super().visible():
            return False
        note_id = self.event.context.get("note_id")
        return not (
            Command.objects.filter(note_id=note_id, state="staged")
            .exclude(schema_key="reasonForVisit")
            .exists()
        )
```

You can gate on anything in the [runtime context](#reading-the-runtime-context). For example, to show a button only to the note's provider, compare the logged-in user against the note's provider (`note.provider.id` and the user id are both Staff ids):

```python?partial=true
    def visible(self) -> bool:
        if not super().visible():
            return False

        note_id = self.event.context.get("note_id")
        user_id = (self.event.context.get("user") or {}).get("id")
        if not note_id or not user_id:
            return False

        note = Note.objects.filter(dbid=note_id).first()
        return note is not None and note.provider.id == user_id
```

### Keeping the footer in sync

`visible()` is only re-evaluated when the footer is [reloaded](#reloading-buttons). A transition triggered by one of these buttons reloads the footer automatically, but changes from elsewhere don't — so pair the buttons with handlers that reload the footer when the note changes by another path. For example, reload whenever a command is committed (so the Sign button reappears the instant the last command is committed) and whenever the note's state changes:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.action_button import ReloadNoteActionButtonsEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.command import Command


class ReloadFooterOnCommandCommit(BaseHandler):
    """Reload the footer whenever any command is committed."""

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


class ReloadFooterOnNoteStateChange(BaseHandler):
    """Reload the footer whenever the note transitions to a new state."""

    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def compute(self) -> list[Effect]:
        note_id = self.event.context.get("note_id")
        if not note_id:
            return []
        return [ReloadNoteActionButtonsEffect(id=note_id).apply()]
```

## Reference plugin

A complete, working plugin that ties these patterns together is available as the [**note-lifecycle-example**](https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/note-lifecycle-example) plugin. It demonstrates:

- a full set of state-responsive footer buttons (Lock, Sign, Unlock, Push charges, Check in, No show, Cancel, Restore, Delete, Discharge), each appearing only when its transition is valid from the note's current state — Lock and Sign built on `LockNoteActionButton` and `SignNoteActionButton`, the rest on `NoteStateActionButton`;
- a `HideDefaultStateButtons` handler that hides Canvas's native footer buttons so the plugin's buttons replace them;
- `ReloadFooterOnCommandCommit` and `ReloadFooterOnNoteStateChange` handlers that keep the visible button set in sync as the note evolves.

Use it as a starting point for your own footer.
