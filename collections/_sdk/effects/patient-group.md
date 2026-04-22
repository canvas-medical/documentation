---
title: "Patient Group"
slug: "effect-patient-group"
excerpt: "Effects for managing patient group membership"
hidden: false
---

The Canvas SDK provides effects for managing patient membership in groups. These effects are idempotent — adding a patient who is already a member or deactivating a patient who is not an active member will have no effect.

## PatientGroupEffect

An effect class for performing actions on a patient group. Instantiate it with a `group_id`, then call methods to add or deactivate members.

### Attributes

| Attribute  | Type      | Description                                              | Required |
| ---------- |-----------| -------------------------------------------------------- | -------- |
| `group_id` | `UUID`    | The id of the [patient group](/sdk/data-patient-group/)  | Yes      |

### Methods

#### `add_member(patient_ids: list[str]) -> Effect`

Ensures one or more patients are members of the group.

| Parameter     | Type         | Description                                                              |
| ------------- | ------------ | ------------------------------------------------------------------------ |
| `patient_ids` | `list[str]`  | List of [patient](/sdk/data-patient/) ids to add to the group            |

#### `deactivate_member(patient_ids: list[str]) -> Effect`

Ensures one or more patients are not active members of the group. If a patient is currently locked in the group, this effect will be ignored for that patient.

| Parameter     | Type         | Description                                                                    |
| ------------- | ------------ | ------------------------------------------------------------------------------ |
| `patient_ids` | `list[str]`  | List of [patient](/sdk/data-patient/) ids to deactivate from the group         |

### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_group import PatientGroupEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Patient, PatientGroup


class AddMemberHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self) -> list[Effect]:
        """Add patients to a group."""
        patient = Patient.objects.get(id=self.target)
        group = PatientGroup.objects.first()

        effect = PatientGroupEffect(group_id=str(group.id))
        return [effect.add_member(patient_ids=[str(patient.id)])]


class DeactivateMemberHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self) -> list[Effect]:
        """Deactivate a patient from a group."""
        patient = Patient.objects.get(id=self.target)
        group = PatientGroup.objects.first()

        effect = PatientGroupEffect(group_id=str(group.id))
        return [effect.deactivate_member(patient_ids=[str(patient.id)])]
```

<br/>
<br/>
<br/>
