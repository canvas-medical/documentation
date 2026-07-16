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

## Creating an Action Button

To implement a custom action button, you need to create a handler class that inherits from the `ActionButton` class. Your handler class must:

1. Define the constants `BUTTON_TITLE`, `BUTTON_KEY`, and `BUTTON_LOCATION`.
2. Implement the `handle()` method to specify the action that should be triggered when the button is clicked.
3. Optionally, implement the `visible()` method to control when the button should be shown.

### Required Constants

- **`BUTTON_TITLE`**  
  A string that defines the label of the button displayed in the Canvas UI. This is the text the user sees when interacting with the button.

- **`BUTTON_KEY`**  
  A unique identifier for your button. This key is used to route events, such as a click, to the appropriate handler method (`handle()`).

- **`BUTTON_LOCATION`**
  Specifies where the button will appear within the Canvas UI. The button can be placed in various locations, such as the note header or footer, or other areas within the chart summary.

### Optional Constants

- **`PRIORITY`**
  An integer that specifies the order in which the button should appear relative to other buttons in the same location. Lower values appear first. If not specified, no order is guaranteed.

- **`BUTTON_TEXT_COLOR`**
  A string that specifies the text color of the button, defined as a HEX color value (e.g., `"#FF0000"`). If not specified, the text color is automatically chosen to contrast with the background.

- **`BUTTON_BACKGROUND_COLOR`**
  A string that specifies the background color of the button, defined as a HEX color value (e.g., `"#4CAF50"`). If not specified, the button uses the default gray styling.

### Optional: Implement the `visible()` Method

By default, the `ActionButton` class assumes the button is always visible (`return True`). If you want the button to only be visible under certain conditions, you can override the `visible()` method. This method must return a boolean value (`True` to show the button, `False` to hide it).

### Implementing the `handle()` Method

The `handle()` method is called when the action button is clicked. Inside this method, you can define what action should occur. The `handle()` method must return a list of [`Effect`](/sdk/effects/) objects, which represent the actions to be executed when the button is clicked. If no action is required, you can return an empty list.

### Button Locations

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


## Dynamic, state-responsive buttons

Action buttons are not rendered once and cached. Canvas re-evaluates every `ActionButton` handler each time its location loads — and again whenever the location is [reloaded](#reloading-buttons). On each evaluation Canvas fires the `SHOW_*_BUTTON` event for that location and your handler's `visible()` method decides whether the button is included.

This is what makes buttons *dynamic*: because `visible()` runs against live data every time, the same button can appear, disappear, or change its title depending on the note, the patient, or the logged-in user.

### Reading the runtime context

Inside `visible()`, `compute()`, and `handle()` you can read the event context to make decisions. When responding to a `SHOW_*_BUTTON` event, the following are available:

| Accessor                        | Description                                                                                                                                    |
|---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `self.event.context["note_id"]` | The **database id** of the note the button is rendered for (note locations only). Look the note up with `Note.objects.filter(dbid=...)`.       |
| `self.event.context["user"]`    | The logged-in user, as `{"type": "Staff", "id": "<staff-key>"}`. Use `self.event.context["user"]["id"]` to compare against staff in your data. |
| `self.event.target.id`          | The key of the patient the button is rendered for.                                                                                             |

### Reloading buttons

Because visibility is computed from live data, Canvas needs to know *when* to re-evaluate it. A button's location is reloaded automatically after its own `handle()` runs, but you will often want to reload in response to something else changing — for example, recomputing the footer after a command is committed, or after the note transitions to a new state.

Return one of these [Reload Action Buttons](/sdk/effect-reload-action-buttons/) effects (imported from `canvas_sdk.effects.action_button`) from any handler's `handle()` or `compute()` to refresh a location's buttons:

- `ReloadNoteActionButtonsEffect(id=<note external id>)` — re-evaluates every button bound to that note.
- `ReloadPatientActionButtonsEffect(id=<patient id>)` — re-evaluates every button bound to that patient.

A reload re-fires the `SHOW_*_BUTTON` events, so every button recomputes `visible()` from scratch — the button set is rebuilt rather than patched. Any handler can emit a reload, not just an `ActionButton`; Example 4 below uses plain event handlers to keep the footer in sync as the note changes.


## Example Implementations

### Example 1: Log Information When Button is Clicked

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

### Example 2: Commit All Commands in a Note

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

### Example 3: Show Button in Vitals Section and render HTML on click

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

### Example 4: Drive a note through its lifecycle with `NoteStateActionButton`

Footer buttons that move a note through its states — Sign, Amend, Check in, and so on - are common enough that the SDK ships a specialized base class, `NoteStateActionButton`. Subclass it and set `STATE_ACTION` to the `NoteStates` value the button transitions the note into. With no further code, each button:

- appears **only when that transition is valid** from the note's current state - so the same button shows or hides automatically as the note moves through its lifecycle;
- derives its `BUTTON_TITLE` and `BUTTON_KEY` from the state (set `BUTTON_TITLE` explicitly to relabel it);
- on click, emits the effect that performs the transition and reloads the footer.

Locking and signing carry extra rules, so the SDK ships two `NoteStateActionButton` subclasses that encapsulate them. Use these instead of subclassing `NoteStateActionButton` directly for those two transitions:

- **`LockNoteActionButton`** — locks the note. Shown only for note types that **don't** require a signature.
- **`SignNoteActionButton`** — signs the note. Shown only for note types that **do** require a signature. It locks the note first when it isn't already locked, so a note can be signed repeatedly — including by multiple users — and is only re-locked after an amend. It also hides itself once the current user has signed since the note was last locked.

`Discharge` is shown only for inpatient note types; the base class applies that gate for you.

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

#### Replacing Canvas's default footer buttons

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

#### Customizing when a button appears

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

You can gate on anything in the [runtime context](#reading-the-runtime-context). For example, to show a button only to the note's provider, compare the logged-in user against the note's provider (`note.provider.id` and the user id are both Staff keys):

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

#### Keeping the footer in sync

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
