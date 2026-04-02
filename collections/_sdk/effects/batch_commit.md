---
title: "Batch Commit Commands"
slug: "effect-batch-commit"
excerpt: "Efficiently commit multiple commands in a single batch operation."
hidden: false
---

## Overview

The `BatchCommitCommandEffect` commits multiple commands at once. Use batch commit when you need to finalize many commands together instead of committing each one individually.

**Parameters:**

| Attribute  | Type   | Required | Description                                    |
|------------|--------|----------|------------------------------------------------|
| `commands` | `list` | `true`   | List of command instances to batch commit      |

**Returns:**

An `Effect` that can be applied to commit all commands in a single operation.


## How It Works

The batch commit effect processes multiple commands in a single operation:

1. **Command Preparation**: Each command in the list must have a valid `command_uuid` (i.e., it must have already been originated)
2. **Batch Processing**: All commands are committed together, minimizing database round-trips

This approach minimizes database round-trips and improves overall performance.

## Basic Usage

```python
from canvas_sdk.commands import (
    PlanCommand,
    AssessCommand,
    DiagnoseCommand
)
from canvas_sdk.effects.batch_commit import BatchCommitCommandEffect
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.events import EventType


class Handler(BaseHandler):

    def compute(self):
        # Commands that have already been originated and have command_uuid values
        plan = PlanCommand(command_uuid="existing-plan-uuid")
        assess = AssessCommand(command_uuid="existing-assess-uuid")
        diagnose = DiagnoseCommand(command_uuid="existing-diagnose-uuid")

        # Batch commit all commands
        commands_to_commit = [plan, assess, diagnose]
        return [BatchCommitCommandEffect(commands=commands_to_commit).apply()]
```

## Related Documentation

- [Commands Overview](/sdk/commands)
- [Batch Originate Commands](/sdk/effect-batch-originate/)
