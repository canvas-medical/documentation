---
title: "NoteMetadata Effect"
slug: "effect-note-metadata"
excerpt: "Effects for note metadata management"
hidden: false
---

The `NoteMetadata` effect provides a flexible key-value storage system for note-specific data within the Canvas
system.
This effect enables the creation and updating of custom metadata entries associated with note records, allowing for
extensible note information storage beyond standard note fields.

## Overview

Note metadata serves as a powerful extension mechanism for storing custom note-related information that doesn't
fit within the standard note data model.

## Attributes

| Attribute | Type          | Description                                                      | Required |
|-----------|---------------|------------------------------------------------------------------|----------|
| `note_id` | `str \| UUID` | Id of the note record to associate metadata with                 | Yes      |
| `key`     | `str`         | Unique identifier for the metadata entry within the note context | Yes      |

## Methods

### upsert(value: str) → Effect

Creates or updates a metadata entry for the specified note and key combination.

#### Parameters

| Parameter | Type  | Description                 | Required |
|-----------|-------|-----------------------------|----------|
| `value`   | `str` | The metadata value to store | Yes      |

#### Returns

An `Effect` object configured for upserting note metadata.

#### Behavior

- If a metadata entry with the specified key already exists for the note, it will be updated with the new value
- If no entry exists, a new metadata entry will be created
- The operation is idempotent - repeated calls with the same key and value will not create duplicate entries

## Implementation Details

### Validation

The effect performs comprehensive validation before execution:

1. **Note Existence Validation**: Verifies that the referenced note exists in the system

- Queries the note database to confirm the `note_id` corresponds to an existing note record
- Returns a descriptive error if the note is not found

2. **Field Validation**: Ensures all required fields are provided and properly formatted

- Both `note_id` and `key` must be non-empty strings
- The `value` parameter in the `upsert` method must be provided


## Example Usage

### Basic Usage

```python
from canvas_sdk.effects.note_metadata import NoteMetadata

# Create a metadata entry for note tracking
metadata = NoteMetadata(
  note_id="803ce56a-350e-49a4-abae-019d9f5f24b2",
  key="my_plugin:external_system_id"
)

# Upsert the metadata value
effect = metadata.upsert("EXT-12345")
```

### Note Integration Example

```python
import json
from canvas_sdk.effects.note_metadata import NoteMetadata
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.events import EventType


class NoteMetadataHandler(BaseHandler):
  """
  Adds metadata to notes when they are signed.
  """

  RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

  def compute(self):
    note_id = self.context["note"]["id"]
    state = self.context.get("note_state_change_event", {}).get("state")

    effects = []

    if state == "SGN":
      # Store signing source
      metadata = NoteMetadata(
        note_id=note_id,
        key="my_plugin:signing_source"
      )
      effects.append(metadata.upsert("protocol"))

      # Store additional context as JSON
      context_data = {
        "signed_by": self.context.get("actor", {}).get("id"),
        "protocol_version": "1.0"
      }
      context_metadata = NoteMetadata(
        note_id=note_id,
        key="my_plugin:signing_context"
      )
      effects.append(context_metadata.upsert(json.dumps(context_data)))

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
   # Storing JSON data
   import json
   from canvas_sdk.effects.note_metadata import NoteMetadata

   metadata = NoteMetadata(
       note_id="803ce56a-350e-49a4-abae-019d9f5f24b2",
       key="my_plugin:workflow_state"
   )
   complex_data = {"stage": "review", "approvers": ["user1", "user2"], "timestamp": "2025-01-15T10:30:00Z"}
   metadata.upsert(json.dumps(complex_data))
   ```

2. **Boolean Values**: Store as "true" or "false" strings for consistency
   ```python
   from canvas_sdk.effects.note_metadata import NoteMetadata

   needs_followup = True
   metadata = NoteMetadata(
       note_id="803ce56a-350e-49a4-abae-019d9f5f24b2",
       key="my_plugin:requires_followup"
   )
   metadata.upsert("true" if needs_followup else "false")
   ```

## Notes

- Metadata entries are note-specific and isolated - the same key can have different values for different notes
- There is no built-in versioning; updating a key overwrites the previous value
- The system does not enforce any schema on metadata values - validation is the responsibility of the implementing code

<br/>
<br/>
<br/>
