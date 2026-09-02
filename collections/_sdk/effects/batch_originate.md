---
title: "Batch Originate Commands"
slug: "effect-batch-originate"
excerpt: "Efficiently insert multiple commands in a single batch operation."
hidden: false
---

## Overview

The `BatchOriginateCommandEffect` provides an efficient way to insert multiple commands into a note simultaneously. When you need to create many commands at once, using batch originate significantly improves performance compared to individual originate operations.

**Parameters:**

| Attribute      | Type   | Required | Description                                    |
|----------------|--------|----------|------------------------------------------------|
| `commands`     | `list` | `true`   | List of command instances to batch originate   |
| `line_number`  | `int`  | `false`  | Which note line the commands land on. Defaults to `-1`, which inserts them at the bottom of the note; set a specific line to target that line instead. Combine with `replace_line=True` to also take over (replace the content of) that line. |
| `replace_line` | `bool` | `false`  | Replace the content of the target line (the one set by `line_number`) with the originated commands, instead of inserting them as new lines. Defaults to `False`. |

**Returns:**

An `Effect` that can be applied to originate all commands in a single operation.


## How It Works

The batch originate effect processes multiple commands in a single operation:

1. **Command Preparation**: Each command in the list required all necessary fields for `originate`
2. **Note Update**: The note is updated once with all command UUIDs, rather than updating for each command individually

This approach minimizes database round-trips and improves overall performance.

## Commit behavior

`BatchOriginateCommandEffect` originates commands in the **uncommitted (draft)** state only. The batch effect has no `commit` option — every command in the batch is inserted into the note body as a draft.

Batch originating commands in a committed state is **not supported**, by design. The performance benefit of batching comes from collapsing the note update for many draft insertions into a single operation, and committing is a separate, per-command action with no equivalent batch saving.

Whenever a plugin needs to originate more than one command — whether you want them left as drafts or committed — batch origination is the right tool. To end up with committed commands, batch originate the drafts first so the note is updated once, then commit each command individually. Assign each command a `command_uuid` up front so it can be committed after it is originated:

```python?partial=true
from uuid import uuid4

# Set command_uuid so each draft can be committed after batch origination
plan1.command_uuid = str(uuid4())
diagnose.command_uuid = str(uuid4())

# One note update for all drafts, followed by a commit per command
return [
    BatchOriginateCommandEffect(commands=[plan1, diagnose]).apply(),
    plan1.commit(),
    diagnose.commit(),
]
```

For three commands this performs three originates, **one** note update, and three commits. Collapsing the draft insertions into a single note update is where the performance benefit comes from.

## Note body automations

A [note body automation](/sdk/handlers-action-buttons/) is an entry a plugin adds to the note body's "/" command list. When a clinician selects the entry, the automation's `handle()` returns a `BatchOriginateCommandEffect` with `replace_line=True`. In this flow Canvas's note body "/" handling supplies the trigger-line position, so Canvas places the originated commands on the line the clinician typed the trigger on and replaces that line, rather than appending them to the note. The automation doesn't set `line_number` itself. If a plugin omits `replace_line`, it keeps its default of `False`, and the batch follows the effect's normal defaults: the originated commands insert at the bottom of the note (the `line_number=-1` default) rather than taking over the trigger line.

```python?partial=true
return [
    BatchOriginateCommandEffect(
        commands=[plan],
        replace_line=True,
    ).apply()
]
```

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
