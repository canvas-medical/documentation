---
title: "StaffExternalIdentifier"
slug: "effect-staff-external-identifier"
excerpt: "Effect to create, update, or delete an external identifier on a staff member."
hidden: false
---

Manage external identifiers on a staff member from a plugin. `StaffExternalIdentifier` is a single effect class with three methods — `.create()`, `.update()`, and `.delete()` — and which fields are required depends on the operation.

## Attributes

| Name       | Type           | Description                                                                  |
|------------|----------------|------------------------------------------------------------------------------|
| `id`       | `str` / `UUID` | The identifier's existing UUID. Required for `update()` and `delete()`.      |
| `staff_id` | `str` / `UUID` | UUID of the [Staff](/sdk/data-staff/) record. Required for `create()`.       |
| `system`   | `str`          | The system the identifier belongs to (typically a URL).                      |
| `value`    | `str`          | The identifier value. Required for `create()`.                               |

## Methods

### create() → Effect

Creates a new external identifier on the specified staff member. Requires `staff_id` and `value`; `system` is optional but recommended.

### update() → Effect

Updates fields on an existing external identifier. Requires `id`. Any of `value` or `system` that you supply will be written; unset fields are left alone.

### delete() → Effect

Deletes the external identifier identified by `id`. Requires `id`.

## Examples

### Create

```python
from canvas_sdk.effects.staff import StaffExternalIdentifier

effect = StaffExternalIdentifier(
    staff_id="4150cd20de8a470aa570a852859ac87e",
    system="https://hr.example.com/",
    value="EMP-001234",
).create()
```

### Update

```python
from canvas_sdk.effects.staff import StaffExternalIdentifier

effect = StaffExternalIdentifier(
    id="00000000-0000-0000-0000-000000000001",
    value="EMP-005678",
).update()
```

### Delete

```python
from canvas_sdk.effects.staff import StaffExternalIdentifier

effect = StaffExternalIdentifier(
    id="00000000-0000-0000-0000-000000000001",
).delete()
```

## Defaults populated server-side

The SDK effect only exposes `value`, `system`, `staff_id`, and `id`. On `create()`, the home-app interpreter populates the remaining fields with these defaults:

- `use` → `"usual"`
- `issued_date` → `"1970-01-01"`
- `expiration_date` → `"2100-12-31"`

`update()` only mutates the fields you set on the effect; unset fields keep their existing values.

<br/>
<br/>
<br/>
