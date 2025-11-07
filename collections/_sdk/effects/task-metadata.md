---
title: "TaskMetadata Effect"
slug: "effect-task-metadata"
excerpt: "Effects for task metadata management"
hidden: false
---

The `TaskMetadata` effect provides a flexible key-value storage system for task-specific data within the Canvas
system.
This effect enables the creation and updating of custom metadata entries associated with task records, allowing for
extensible task information storage beyond standard task fields.

## Overview

Task metadata serves as a powerful extension mechanism for storing custom task-related information that doesn't
fit within the standard task data model.

## Attributes

| Attribute | Type  | Description                                                       | Required |
|-----------|-------|-------------------------------------------------------------------|----------|
| `task_id` | `str` | Id of the task record to associate metadata with                  | Yes      |
| `key`     | `str` | Unique identifier for the metadata entry within the task context  | Yes      |

## Methods

### upsert(value: str) → Effect

Creates or updates a metadata entry for the specified task and key combination.

#### Parameters

| Parameter | Type  | Description                 | Required |
|-----------|-------|-----------------------------|----------|
| `value`   | `str` | The metadata value to store | Yes      |

#### Returns

An `Effect` object configured for upserting task metadata.

#### Behavior

- If a metadata entry with the specified key already exists for the task, it will be updated with the new value
- If no entry exists, a new metadata entry will be created
- The operation is idempotent - repeated calls with the same key and value will not create duplicate entries

## Implementation Details

### Validation

The effect performs comprehensive validation before execution:

1. **Task Existence Validation**: Verifies that the referenced task exists in the system

- Queries the task database to confirm the `task_id` corresponds to an existing task record
- Returns a descriptive error if the task is not found

2. **Field Validation**: Ensures all required fields are provided and properly formatted

- Both `task_id` and `key` must be non-empty strings
- The `value` parameter in the `upsert` method must be provided

### Data Structure

The effect payload is structured as JSON with the following schema:

```json
{
  "data": {
    "task_id": "task-id",
    "key": "metadata-key",
    "value": "metadata-value"
  }
}
```

## Example Usage

### Basic Usage

```python
from canvas_sdk.effects.task import TaskMetadata

# Create a metadata entry for task tracking
metadata = TaskMetadata(
    task_id="550e8400e29b41d4a716446655440000",
    key="external_system_id"
)

# Upsert the metadata value
effect = metadata.upsert("EXT-12345")
```

### Task Integration Example

```python
import json
from canvas_sdk.effects.task import TaskMetadata
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.events import EventType


class TaskMetadataHandler(BaseHandler):
  """
  Adds metadata to tasks based on task properties.
  """

  RESPONDS_TO = EventType.Name(EventType.TASK_CREATED)

  def compute(self):
    task_id = self.context["task"]["id"]
    task_labels = self.context.get("task", {}).get("labels", [])

    effects = []

    # Store task creation source
    metadata = TaskMetadata(
      task_id=task_id,
      key="creation_source"
    )
    effects.append(metadata.upsert("protocol"))

    # Store label information as JSON
    if task_labels:
      labels_metadata = TaskMetadata(
        task_id=task_id,
        key="original_labels"
      )
      effects.append(labels_metadata.upsert(json.dumps(task_labels)))

    return effects
```

## Best Practices

### Key Naming Conventions

1. **Use Descriptive Names**: Choose keys that clearly indicate the purpose of the metadata

- Good: `external_system_id`, `workflow_stage`, `integration_source`
- Avoid: `data1`, `temp`, `misc`

2. **Namespace Your Keys**: When building integrations or modules, prefix keys to avoid collisions

- Example: `integration_task_id`, `workflow_current_stage`, `automation_trigger_id`

### Value Storage

1. **String Serialization**: All values are stored as strings. For complex data types:
   ```python
   # Storing JSON data
   import json
   from canvas_sdk.effects.task import TaskMetadata

   metadata = TaskMetadata(
       task_id="550e8400e29b41d4a716446655440000",
       key="workflow_state"
   )
   complex_data = {"stage": "review", "approvers": ["user1", "user2"], "timestamp": "2025-01-15T10:30:00Z"}
   metadata.upsert(json.dumps(complex_data))
   ```

2. **Boolean Values**: Store as "true" or "false" strings for consistency
   ```python
   from canvas_sdk.effects.task import TaskMetadata

   needs_followup = True
   metadata = TaskMetadata(
       task_id="550e8400e29b41d4a716446655440000",
       key="requires_followup"
   )
   metadata.upsert("true" if needs_followup else "false")
   ```

## Notes

- Metadata entries are task-specific and isolated - the same key can have different values for different tasks
- There is no built-in versioning; updating a key overwrites the previous value
- The system does not enforce any schema on metadata values - validation is the responsibility of the implementing code