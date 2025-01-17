---
title: "Action Buttons"
slug: "handlers-action-buttons"
excerpt: "Create and modify views in the Canvas UI."
hidden: false
---

Action buttons appear in the Canvas UI and execute your provided code when
clicked. They can be added to the note header or the note footer.

## Implementing an Action Button

To add an action button, your handler class should inherit from  the `ActionButton` class.

Your class must specify the constants `BUTTON_TITLE`, `BUTTON_KEY`, and `BUTTON_LOCATION`,
as well as implement the `handle()` method. Your class can optionally
implement the `visible()` method, which allows you to make the button
conditionally appear.

### Setting the Required Constants

The `BUTTON_TITLE` constant sets the text that appears on your button in the
Canvas UI.

`BUTTON_KEY` is an identifier for your button used to route click events to
your `handle()` method.

`BUTTON_LOCATION` determines the placement of your button, and can be one of
the following:

- `ActionButton.ButtonLocation.NOTE_HEADER`
  - The button will appear in the header of each note.
- `ActionButton.ButtonLocation.NOTE_FOOTER`
  - The button will appear in the footer of each note.

### Implement the `handle()` method

When an action button is clicked, the `handle()` method is called. You have
access to runtime information like `self.event`, `self.context`, and
`self.secrets`. Your method must return a list of [Effect](/sdk/effects/)
objects, but that list can be empty of course.

### (Optional) Implement the `visible()` method

The `ActionButton` base class implements the `visible()` as `return True`,
meaning "always visible". If you want your button to appear conditionally, you
can implement the `visible()` method and return `True` or `False` based on
your criteria. You have access to runtime information like `self.event`,
`self.context`, and `self.secrets` to help make your determination. Your
method must return a boolean value.

## Examples

### Log When You Click

This example is concise to serve as an easy to interpret visual of the anatomy
of an action button. The button only shows during the month of January, and
when clicked it logs some information. This isn't particularly useful, but it
does show you how to control the visibility of the button, and some of the
data you have access to in your `handle()` method.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.handlers.action_button import ActionButton
from datetime import datetime
from logger import log


class MyButton(ActionButton):
    BUTTON_TITLE = "🪵"
    BUTTON_KEY = "LOG_STUFF"
    BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_HEADER

    def visible(self) -> bool:
        # Only show this button in January
        return datetime.now().month == 1

    def handle(self) -> list[Effect]:
        log.info("You clicked the button!!")
        log.info(self.event.context)
        log.info(self.event.target)

        return []
```

### Commit All Commands in a Note

This example may actually be useful. It adds an action button to the note footer
which commits all commands in a note. It shows on every note (default behavior
since `visible()` is not overridden in this class).
  
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

<br/>
<br/>
<br/>
<br/>
