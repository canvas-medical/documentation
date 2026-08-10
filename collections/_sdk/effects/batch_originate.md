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

1. **Command Preparation**: Each command in the list required all necessary fields for `originate`
2. **Note Update**: The note is updated once with all command UUIDs, rather than updating for each command individually

This approach minimizes database round-trips and improves overall performance.

## Commit behavior

`BatchOriginateCommandEffect` originates commands in the **uncommitted (draft)** state only. Unlike a single command's `originate(commit=True)`, the batch effect has no `commit` option — every command in the batch is inserted into the note body as a draft.

Batch originating commands in a committed state is **not supported**, by design. The performance benefit of batching comes from collapsing the note update for many draft insertions into a single operation. Committing is a separate, per-command action with no equivalent batch saving, so there would be no performance benefit over originating each command individually in a committed state.

Batch origination is the right tool when a plugin needs to originate many commands in the uncommitted (draft) state at once — that is exactly the case it is built for.

If you need commands committed on origination, originate them individually with `commit=True` instead:

```python?partial=true
# Commit at origination time, one command per effect
return [
    plan1.originate(commit=True),
    diagnose.originate(commit=True),
]
```

For **multiple** commands that all need to be committed in the same plugin, batch originate the drafts first — so the note is updated once — and then commit each command. Assign each command a `command_uuid` up front so it can be committed after it is originated:

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

For three commands this performs three originates, **one** note update, and three commits — whereas calling `originate(commit=True)` on each command updates the note once per command.

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
