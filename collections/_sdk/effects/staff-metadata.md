---
title: "StaffMetadata Effect"
slug: "effect-staff-metadata"
excerpt: "Effects for staff metadata management"
hidden: false
---

The `StaffMetadata` effect provides a flexible key-value storage system for staff-specific data within the Canvas system. It mirrors the [`PatientMetadata` effect](/sdk/effect-patient-metadata/) but operates against staff records, letting plugins attach extensible information beyond the standard staff data model.

## Overview

`StaffMetadata` uses an `.upsert(value)` method to apply a value to the key attributed with the metadata effect object. The same key may be used across many staff members; the `(staff, key)` pair is unique per staff member.

## Attributes

| Attribute  | Type  | Description                                                       | Required |
|------------|-------|-------------------------------------------------------------------|----------|
| `staff_id` | `str` | Id of the [Staff](/sdk/data-staff/) record to associate metadata with | Yes      |
| `key`      | `str` | Unique identifier for the metadata entry within the staff context | Yes      |

## Methods

### upsert(value: str) → Effect

Creates or updates a metadata entry for the specified staff and key combination.

#### Parameters

| Parameter | Type  | Description                 | Required |
|-----------|-------|-----------------------------|----------|
| `value`   | `str` | The metadata value to store | Yes      |

#### Returns

An `Effect` object configured for upserting staff metadata.

#### Behavior

- If a metadata entry with the specified key already exists for the staff member, it will be updated with the new value.
- If no entry exists, a new metadata entry will be created.
- The operation is idempotent — repeated calls with the same key and value will not change the row.

## Implementation Details

### Validation

The effect performs validation before execution:

1. **Staff Existence Validation**: queries the staff database to confirm the `staff_id` corresponds to an existing staff record. Returns a descriptive error if the staff member is not found.
2. **Field Validation**: ensures all required fields are provided. `staff_id` and `key` must be non-empty strings, and the `value` parameter passed to `.upsert(...)` must be provided.

### Data Structure

The effect payload is structured as JSON:

```json
{
  "data": {
    "staff_id": "staff-id",
    "key": "metadata-key",
    "value": "metadata-value"
  }
}
```

## Example Usage

### Basic Usage

```python
from canvas_sdk.effects.staff_metadata import StaffMetadata

# Tag a provider with their primary department
metadata = StaffMetadata(
    staff_id="4150cd20de8a470aa570a852859ac87e",
    key="department",
)

effect = metadata.upsert("cardiology")
```

### Mirroring an HR System

```python
from canvas_sdk.effects.staff_metadata import StaffMetadata
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.events import EventType


class StaffHRSync(BaseHandler):
    """Sync select fields from an HR webhook payload onto Canvas staff."""

    RESPONDS_TO = EventType.Name(EventType.STAFF_UPDATED)

    def compute(self):
        staff_id = self.context["staff"]["id"]
        hr_record = self.context.get("fields", {}).get("hr_record", {})

        return [
            StaffMetadata(staff_id=staff_id, key=f"hr.{key}").upsert(str(value))
            for key, value in hr_record.items()
        ]
```

## Best Practices

### Key Naming Conventions

1. **Use descriptive names**. Choose keys that clearly indicate the purpose of the metadata.
   - Good: `department`, `cost_center`, `external_employee_id`
   - Avoid: `data1`, `temp`, `misc`
2. **Namespace your keys**. Prefix keys for integrations or modules to avoid collisions.
   - Example: `hr.employee_id`, `payroll.cost_center`

### Value Storage

1. **String serialization**. All values are stored as strings. For complex data:
   ```python
   import json
   from canvas_sdk.effects.staff_metadata import StaffMetadata

   metadata = StaffMetadata(
       staff_id="4150cd20de8a470aa570a852859ac87e",
       key="hr.profile",
   )
   complex_data = {"hire_date": "2020-01-15", "department": "cardiology"}
   metadata.upsert(json.dumps(complex_data))
   ```
2. **Boolean values**. Store as `"true"` or `"false"` strings for consistency.

## Notes

- Metadata entries are staff-specific and isolated — the same key can have different values for different staff members.
- There is no built-in versioning; upserting a key overwrites the previous value.
- The system does not enforce any schema on metadata values — validation is the responsibility of the implementing code.

<br/>
<br/>
<br/>
