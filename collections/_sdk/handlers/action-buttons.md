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

- **`PRIORITY`**
  An optional integer that specifies the order in which the button should appear relative to other buttons in the same location. Lower values appear first. If not specified, no order is guaranteed.

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
                    payload=json.dumps({"command_uuid": str(command.id)}),
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
