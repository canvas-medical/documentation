---
title: "Action Buttons"
slug: "handlers-action-buttons"
excerpt: "Create and modify views in the Canvas UI."
hidden: false
---

# Action Buttons

Action buttons are buttons that appear in the Canvas UI that can be clicked to perform a custom action,
and can be added to the note header or footer.


## Adding an Action Button

To add an action button, import the `ActionButton` class and create an instance of it.
It must specify the `BUTTON_TITLE`, `BUTTON_KEY`, and `BUTTON_LOCATION` constants.

`BUTTON_LOCATION` can be one of the following:

- `ActionButton.ButtonLocation.NOTE_HEADER`
- `ActionButton.ButtonLocation.NOTE_FOOTER`

An example of adding an action button to the note footer, that commits all commands in a note:
  
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
