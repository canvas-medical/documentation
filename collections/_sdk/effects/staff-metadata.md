---
title: "StaffMetadata Effect"
slug: "effect-staff-metadata"
excerpt: "Effects for staff metadata management"
hidden: false
---

The `StaffMetadata` effect provides a flexible key-value storage system for staff-specific data within the Canvas system, letting plugins attach extensible information beyond the standard staff data model.

## Overview

`StaffMetadata` exposes `.upsert(value)` to write or replace a metadata entry, and `.delete()` to remove one. The same key may be used across many staff members; the `(staff, key)` pair is unique per staff member.

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

#### Behavior

- If a metadata entry with the specified key already exists for the staff member, it will be updated with the new value.
- If no entry exists, a new metadata entry will be created.
- Metadata entries are isolated per staff member — the same key can hold different values for different staff members.
- Values are stored as strings with no schema enforcement; the plugin is responsible for validating its own values.

#### Key Naming Conventions

1. **Use descriptive names**. Choose keys that clearly indicate the purpose of the metadata.
   - Good: `department`, `cost_center`, `external_employee_id`
   - Avoid: `data1`, `temp`, `misc`
2. **Namespace your keys**. Prefix keys for integrations or modules to avoid collisions.
   - Example: `hr.employee_id`, `payroll.cost_center`

#### Value Storage

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

#### Examples

```python
from canvas_sdk.effects.staff_metadata import StaffMetadata

# Tag a provider with their primary department
metadata = StaffMetadata(
    staff_id="4150cd20de8a470aa570a852859ac87e",
    key="department",
)

effect = metadata.upsert("cardiology")
```

Mirroring an HR system from a handler:

```python
from canvas_sdk.effects.staff_metadata import StaffMetadata
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.events import EventType


class StaffHRSync(BaseHandler):
    """Sync select fields from an HR webhook payload onto Canvas staff."""

    RESPONDS_TO = EventType.Name(EventType.STAFF_UPDATED)

    def compute(self):
        staff_id = self.event.context["staff"]["id"]
        hr_record = self.event.context.get("fields", {}).get("hr_record", {})

        return [
            StaffMetadata(staff_id=staff_id, key=f"hr.{key}").upsert(str(value))
            for key, value in hr_record.items()
        ]
```

### delete() → Effect

Removes the metadata entry identified by `(staff_id, key)`.

#### Behavior

- Removes the row that matches both `staff_id` and `key`. Returns success even if no row was present (idempotent).
- Does not affect other metadata entries for the same staff member with different keys.

#### Example

```python
from canvas_sdk.effects.staff_metadata import StaffMetadata

# Clear the department tag for a staff member
effect = StaffMetadata(
    staff_id="4150cd20de8a470aa570a852859ac87e",
    key="department",
).delete()
```

## Validation

The effect validates before execution:

- **Staff existence**: the `staff_id` must correspond to an existing Staff record, or the effect raises a descriptive error.
- **Required fields**: `staff_id` and `key` must be non-empty strings, and `.upsert(...)` requires a `value`.

<br/>
<br/>
<br/>
