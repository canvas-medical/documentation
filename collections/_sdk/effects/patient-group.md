---
title: "Patient Group"
slug: "effect-patient-group"
excerpt: "Effects for managing patient group membership"
hidden: false
---

The Canvas SDK provides effects for managing patient membership in groups. These effects are idempotent — adding a patient who is already a member or deactivating a patient who is not an active member will have no effect.

## PatientGroupAddMember

Ensures one or more patients are members of a group.

### Attributes

| Attribute     | Type         | Description                                                              | Required |
| ------------- | ------------ | ------------------------------------------------------------------------ | -------- |
| `patient_ids` | `list[str]`  | List of [patient](/sdk/data-patient/) ids to add to the group            | Yes      |
| `group_id`    | `str`        | The id of the group to add the patients to                               | Yes      |

### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects.patient_group import PatientGroupAddMember
from canvas_sdk.v1.data.patient import Patient


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self) -> list[Effect]:
        """Add a patient to a group when their record is updated."""
        patient = Patient.objects.get(id=self.target)

        add_member = PatientGroupAddMember(
            patient_ids=[patient.id],
            group_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        )

        return [add_member.apply()]
```

## PatientGroupDeactivateMember

Ensures one or more patients are not active members of a group.

### Attributes

| Attribute     | Type         | Description                                                                    | Required |
| ------------- | ------------ | ------------------------------------------------------------------------------ | -------- |
| `patient_ids` | `list[str]`  | List of [patient](/sdk/data-patient/) ids to deactivate from the group         | Yes      |
| `group_id`    | `str`        | The id of the group to deactivate the patients from                            | Yes      |

### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects.patient_group import PatientGroupDeactivateMember
from canvas_sdk.v1.data.patient import Patient


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self) -> list[Effect]:
        """Remove a patient from a group when their record is updated."""
        patient = Patient.objects.get(id=self.target)

        deactivate_member = PatientGroupDeactivateMember(
            patient_ids=[patient.id],
            group_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        )

        return [deactivate_member.apply()]
```

<br/>
<br/>
<br/>
