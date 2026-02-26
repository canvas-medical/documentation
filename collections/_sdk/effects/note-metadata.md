---
title: "NoteMetadata Effect"
slug: "effect-note-metadata"
excerpt: "Effects for note metadata management"
hidden: false
---

The `Note.upsert_metadata` method provides a flexible key-value storage system for note-specific data within the Canvas
system.
This method enables the creation and updating of custom metadata entries associated with note records, allowing for
extensible note information storage beyond standard note fields.

## Overview

Note metadata serves as a powerful extension mechanism for storing custom note-related information that doesn't
fit within the standard note data model. Metadata is managed through the `upsert_metadata` method on the `Note` effect class.

## Method

### upsert_metadata(key: str, value: str) → Effect

Creates or updates a metadata entry for the specified note.

#### Parameters

| Parameter | Type  | Description                                                      | Required |
|-----------|-------|------------------------------------------------------------------|----------|
| `key`     | `str` | Unique identifier for the metadata entry within the note context | Yes      |
| `value`   | `str` | The metadata value to store                                      | Yes      |

#### Prerequisites

The `Note` effect must be initialized with an `instance_id` corresponding to an existing note.

| Attribute     | Type            | Description                              | Required |
|---------------|-----------------|------------------------------------------|----------|
| `instance_id` | `UUID` or `str` | Id of the note record to associate metadata with | Yes      |

#### Returns

An `Effect` object configured for upserting note metadata.

#### Behavior

- If a metadata entry with the specified key already exists for the note, it will be updated with the new value
- If no entry exists, a new metadata entry will be created
- The operation is idempotent - repeated calls with the same key and value will not create duplicate entries
- Raises `ValueError` if `instance_id` is not set on the `Note` effect

## Implementation Details

### Validation

The effect performs comprehensive validation before execution:

1. **Note Existence Validation**: Verifies that the referenced note exists in the system

- Queries the note database to confirm the `instance_id` corresponds to an existing note record
- Returns a descriptive error if the note is not found

2. **Field Validation**: Ensures all required fields are provided and properly formatted

- `instance_id` must be set on the `Note` effect
- Both `key` and `value` must be provided


## Example Usage

### Basic Usage

```python
from canvas_sdk.effects.note.note import Note

# Create a metadata entry for note tracking
note = Note(instance_id="803ce56a-350e-49a4-abae-019d9f5f24b2")
effect = note.upsert_metadata(key="my_plugin:external_system_id", value="EXT-12345")
```

### Protocol Example

```python
import json
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note.note import Note
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class NoteMetadataHandler(BaseHandler):
  """
  Adds metadata to notes when a plan command is updated.
  """

  RESPONDS_TO = EventType.Name(EventType.PLAN_COMMAND__POST_UPDATE)

  def compute(self) -> list[Effect]:
    note_id = self.event.context["note"]["id"]
    command_id = self.event.target.id

    note = Note(instance_id=note_id)
    return [note.upsert_metadata(key="my_plugin:last_plan_update_command", value=str(command_id))]
```

### Storing Multiple Metadata Entries

```python
import json
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note.note import Note
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class SigningMetadataHandler(BaseHandler):
  """
  Adds metadata to notes when they are signed.
  """

  RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

  def compute(self) -> list[Effect]:
    note_id = self.event.context["note"]["id"]
    state = self.event.context.get("note_state_change_event", {}).get("state")

    effects: list[Effect] = []

    if state == "SGN":
      note = Note(instance_id=note_id)

      # Store signing source
      effects.append(note.upsert_metadata(key="my_plugin:signing_source", value="protocol"))

      # Store additional context as JSON
      context_data = {
        "signed_by": self.event.context.get("actor", {}).get("id"),
        "protocol_version": "1.0"
      }
      effects.append(note.upsert_metadata(key="my_plugin:signing_context", value=json.dumps(context_data)))

    return effects
```

## Best Practices

### Key Naming Conventions

1. **Use Descriptive Names**: Choose keys that clearly indicate the purpose of the metadata

- Good: `external_system_id`, `workflow_stage`, `signing_source`
- Avoid: `data1`, `temp`, `misc`

2. **Namespace Your Keys**: Prefix keys with your plugin name to avoid collisions with other plugins

- Example: `my_plugin:external_system_id`, `my_plugin:workflow_stage`, `my_plugin:signing_source`

### Value Storage

1. **String Serialization**: All values are stored as strings. For complex data types:
   ```python
   import json
   from canvas_sdk.effects.note.note import Note

   note = Note(instance_id="803ce56a-350e-49a4-abae-019d9f5f24b2")
   complex_data = {"stage": "review", "approvers": ["user1", "user2"], "timestamp": "2025-01-15T10:30:00Z"}
   note.upsert_metadata(key="my_plugin:workflow_state", value=json.dumps(complex_data))
   ```

2. **Boolean Values**: Store as "true" or "false" strings for consistency
   ```python
   from canvas_sdk.effects.note.note import Note

   needs_followup = True
   note = Note(instance_id="803ce56a-350e-49a4-abae-019d9f5f24b2")
   note.upsert_metadata(key="my_plugin:requires_followup", value="true" if needs_followup else "false")
   ```

## Notes

- Metadata entries are note-specific and isolated - the same key can have different values for different notes
- There is no built-in versioning; updating a key overwrites the previous value
- The system does not enforce any schema on metadata values - validation is the responsibility of the implementing code

<br/>
<br/>
<br/>
