---
title: "CommandMetadata Effect"
slug: "effect-command-metadata"
excerpt: "Effects for command metadata management"
hidden: false
---

The `upsert_metadata` method on any command class provides a flexible key-value storage system for command-specific data within the Canvas system.
This method enables the creation and updating of custom metadata entries associated with command records, allowing for extensible command information storage beyond standard command fields.

## Overview

Command metadata serves as a powerful extension mechanism for storing custom command-related information that doesn't fit within the standard command data model. Metadata is managed through the `upsert_metadata` method available on all command effect classes.

## Method

### upsert_metadata(key: str, value: str) → Effect

Creates or updates a metadata entry for the specified command.

#### Parameters

| Parameter | Type  | Description                                                         | Required |
|-----------|-------|---------------------------------------------------------------------|----------|
| `key`     | `str` | Unique identifier for the metadata entry within the command context | Yes      |
| `value`   | `str` | The metadata value to store                                         | Yes      |

#### Prerequisites

The command effect must be initialized with a `command_uuid`. This can be either the UUID of an existing command or the UUID of a command being originated in the same effect list.

| Attribute      | Type  | Description                                        | Required |
|----------------|-------|----------------------------------------------------|----------|
| `command_uuid` | `str` | Id of the command record to associate metadata with | Yes      |

#### Returns

An `Effect` object configured for upserting command metadata.

#### Behavior

- If a metadata entry with the specified key already exists for the command, it will be updated with the new value
- If no entry exists, a new metadata entry will be created
- The operation is idempotent - repeated calls with the same key and value will not create duplicate entries
- Raises `ValueError` if `command_uuid` is not set on the command effect

## Implementation Details

### Validation

The effect performs validation at two stages:

1. **SDK Validation**: Ensures all required fields are provided before the effect is created

    - `command_uuid` must be set on the command effect
    - Both `key` and `value` must be provided

2. **Server-Side Validation**: When the effect is processed, the server verifies that the referenced command exists

    - Returns a descriptive error if the command is not found after all effects in the list have been processed

## Example Usage

### Basic Usage

```python
from canvas_sdk.commands import PlanCommand

plan = PlanCommand(command_uuid="63hdik")
effect = plan.upsert_metadata(key="my_plugin:priority", value="high")
```

### Example: Chaining with originate()

You can attach metadata to a command at the same time you originate it by returning both effects in the same list:

```python
import uuid

from canvas_sdk.commands import PlanCommand
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class OriginateWithMetadata(BaseHandler):
    """Originates a plan command with metadata attached in a single operation."""

    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART__SECTION__LOADED)

    def compute(self) -> list[Effect]:
        command_uuid = str(uuid.uuid4())
        plan = PlanCommand(
            note_uuid=self.context["note_id"],
            command_uuid=command_uuid,
            narrative="Follow up in 2 weeks",
        )
        return [
            plan.originate(),
            plan.upsert_metadata(key="my_plugin:source", value="auto_generated"),
        ]
```

### Example: Tagging a command on commit

```python
from canvas_sdk.commands import PlanCommand
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class TagPlanOnCommit(BaseHandler):
    """Tags a plan command with a workflow stage when it is committed."""

    RESPONDS_TO = EventType.Name(EventType.PLAN_COMMAND__POST_COMMIT)

    def compute(self) -> list[Effect]:
        plan = PlanCommand(command_uuid=self.event.target.id)
        return [plan.upsert_metadata(key="my_plugin:workflow_stage", value="committed")]
```

### Responding to metadata events

Once metadata is upserted, `COMMAND_METADATA_CREATED` and `COMMAND_METADATA_UPDATED` events are emitted and can be handled by plugins:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.command import CommandMetadata
from logger import log


class CommandMetadataListener(BaseHandler):
    """Reacts to command metadata changes."""

    RESPONDS_TO = [
        EventType.Name(EventType.COMMAND_METADATA_CREATED),
        EventType.Name(EventType.COMMAND_METADATA_UPDATED),
    ]

    def compute(self) -> list[Effect]:
        metadata = CommandMetadata.objects.get(id=self.event.target.id)
        log.info(f"Command {metadata.command.id}: {metadata.key}={metadata.value}")
        return []
```

## Best Practices

### Key Naming Conventions

1. **Use Descriptive Names**: Choose keys that clearly indicate the purpose of the metadata

    - Good: `workflow_stage`, `external_id`, `review_status`
    - Avoid: `data1`, `temp`, `misc`

2. **Namespace Your Keys**: Prefix keys with your plugin name to avoid collisions with other plugins

    - Example: `my_plugin:workflow_stage`, `my_plugin:external_id`

### Value Storage

**String Serialization**: All values are stored as strings. For complex data types, serialize to JSON:

   ```python
   import json
   from canvas_sdk.commands import DiagnoseCommand

   cmd = DiagnoseCommand(command_uuid="abc123")
   data = {"reviewer": "user-id", "approved_at": "2025-01-15T10:30:00Z"}
   cmd.upsert_metadata(key="my_plugin:review", value=json.dumps(data))
   ```

## Notes

- Metadata entries are command-specific — the same key can have different values for different commands
- There is no built-in versioning; updating a key overwrites the previous value
- The system does not enforce any schema on metadata values — validation is the responsibility of the implementing code
- The `key` field supports up to 256 characters

<br/>
<br/>
<br/>
