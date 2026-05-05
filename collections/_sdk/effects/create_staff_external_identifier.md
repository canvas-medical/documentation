---
title: "CreateStaffExternalIdentifier"
slug: "effect-create-staff-external-identifier"
excerpt: "Effect to create a new external identifier for a staff member."
hidden: false
---

Creates a new external identifier for a staff member.

### Parameters

| Name     | Type   | Description                                            |
|----------|--------|--------------------------------------------------------|
| staff_id | UUID   | The unique identifier of the staff member.             |
| system   | String | The system for the external identifier (url).          |
| value    | String | The value of the external identifier.                  |

### Example

```python
from canvas_sdk.effects.staff import CreateStaffExternalIdentifier

effect = CreateStaffExternalIdentifier(
    staff_id="4150cd20de8a470aa570a852859ac87e",
    system="https://hr.example.com/",
    value="EMP-001234",
)

effect.create()
```

This effect creates a new external identifier on the specified staff member.

### Limitations

Only creation is supported via the SDK. There is no effect to update or delete an
existing `StaffExternalIdentifier` from a plugin — those changes must be made
through the Canvas UI or the FHIR API.

<br/>
<br/>
<br/>
