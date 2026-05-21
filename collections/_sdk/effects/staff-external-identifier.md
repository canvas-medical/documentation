---
title: "StaffExternalIdentifier"
slug: "effect-staff-external-identifier"
excerpt: "Effect to create, update, or delete an external identifier on a staff member."
hidden: false
---

Manage external identifiers on a staff member from a plugin. `StaffExternalIdentifier` is a single effect class with three methods — `.create()`, `.update()`, and `.delete()` — and which fields are required depends on the operation.

## Methods

### create() → Effect

Creates a new external identifier on the specified staff member.

#### Attributes

| Attribute  | Type           | Required | Description                                             |
|------------|----------------|----------|---------------------------------------------------------|
| `staff_id` | `str` / `UUID` | Yes      | UUID of the [Staff](/sdk/data-staff/) record.           |
| `value`    | `str`          | Yes      | The identifier value (e.g. an employee ID).             |
| `system`   | `str`          | No       | The system the identifier belongs to (typically a URL). |

#### Validation

- `staff_id` must reference an existing Staff record, or the effect raises a descriptive error.
- `id` must not be set on `create()` — the UUID is assigned server-side. Supplying it fails validation.
- `value` and `staff_id` are required.

#### Server-side defaults

Canvas applies these defaults on `create()`:

- `use` → `"usual"`
- `issued_date` → `"1970-01-01"`
- `expiration_date` → `"2100-12-31"`

#### Example

```python
from canvas_sdk.effects.staff import StaffExternalIdentifier

effect = StaffExternalIdentifier(
    staff_id="4150cd20de8a470aa570a852859ac87e",
    system="https://hr.example.com/",
    value="EMP-001234",
).create()
```

### update() → Effect

Updates fields on an existing external identifier. Only the fields you set on the effect are written; unset fields keep their existing values.

#### Attributes

| Attribute | Type           | Required | Description                                     |
|-----------|----------------|----------|-------------------------------------------------|
| `id`      | `str` / `UUID` | Yes      | UUID of the identifier to update.               |
| `value`   | `str`          | No       | New identifier value. Only written if supplied. |
| `system`  | `str`          | No       | New system value. Only written if supplied.    |

#### Validation

- `id` is required and must reference an existing StaffExternalIdentifier record, or the effect raises a descriptive error.

#### Example

```python
from canvas_sdk.effects.staff import StaffExternalIdentifier

effect = StaffExternalIdentifier(
    id="00000000-0000-0000-0000-000000000001",
    value="EMP-005678",
).update()
```

### delete() → Effect

Deletes the external identifier identified by `id`.

#### Attributes

| Attribute | Type           | Required | Description                       |
|-----------|----------------|----------|-----------------------------------|
| `id`      | `str` / `UUID` | Yes      | UUID of the identifier to delete. |

#### Validation

- `id` is required and must reference an existing StaffExternalIdentifier record, or the effect raises a descriptive error.

#### Example

```python
from canvas_sdk.effects.staff import StaffExternalIdentifier

effect = StaffExternalIdentifier(
    id="00000000-0000-0000-0000-000000000001",
).delete()
```

<br/>
<br/>
<br/>
