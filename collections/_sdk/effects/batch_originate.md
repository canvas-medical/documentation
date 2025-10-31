---
title: "Batch Originate Commands"
slug: "effect-batch-originate"
excerpt: "Efficiently insert multiple commands in a single batch operation."
hidden: false
---

## Overview

The `BatchOriginateCommandEffect` provides an efficient way to insert multiple commands into a note simultaneously. When you need to create many commands at once, using batch originate significantly improves performance compared to individual originate operations.

**Parameters:**

| Attribute  | Type   | Required | Description                                    |
|------------|--------|----------|------------------------------------------------|
| `commands` | `list` | `true`   | List of command instances to batch originate   |

**Returns:**

An `Effect` that can be applied to originate all commands in a single operation.


## How It Works

The batch originate effect processes multiple commands in a single operation:

1. **Command Preparation**: Each command in the list is prepared for the batch insertion using its internal `_originate_for_batch()` method
2. **Note Update**: The note is updated once with all command UUIDs, rather than updating for each command individually

This approach minimizes database round-trips and improves overall performance.

## Basic Usage

```python
from canvas_sdk.commands import (
    PlanCommand,
    HistoryOfPresentIllnessCommand,
    QuestionnaireCommand,
    DiagnoseCommand
)
from canvas_sdk.effects.batch_originate import BatchOriginateCommandEffect
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Questionnaire, Note
from canvas_sdk.events import EventType


class Handler(BaseHandler):

    def compute(self):
        note_uuid = Note.objects.last().id

        # Create multiple commands
        plan1 = PlanCommand()
        plan1.narrative = "Order labs for lipid panel"
        plan1.note_uuid = note_uuid

        plan2 = PlanCommand()
        plan2.narrative = "Schedule follow-up in 3 months"
        plan2.note_uuid = note_uuid

        hpi = HistoryOfPresentIllnessCommand()
        hpi.narrative = "Annual wellness visit"
        hpi.note_uuid = note_uuid

        diagnose = DiagnoseCommand()
        diagnose.icd10_code = "E11.9"
        diagnose.note_uuid = note_uuid
        diagnose.background = "Type 2 diabetes mellitus"

        # Add a questionnaire
        questionnaire = QuestionnaireCommand()
        questionnaire.note_uuid = note_uuid
        questionnaire_id = Questionnaire.objects.filter(
            name="Patient Health Questionnaire"
        ).first()
        if questionnaire_id:
            questionnaire.questionnaire_id = str(questionnaire_id.id)

        # Batch originate all commands
        commands_to_originate = [plan1, plan2, hpi, diagnose, questionnaire]
        return [BatchOriginateCommandEffect(commands=commands_to_originate).apply()]
```

## Related Documentation

- [Commands Overview](/sdk/commands)
