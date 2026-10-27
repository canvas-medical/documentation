---
title: "CreatePatientExternalIdentifier"
slug: "effect-create-patient-external-identifier"
excerpt: "Effect to create a new external identifier for a patient."
hidden: false
---

Creates a new external identifier for a patient.

## Methods

### create() → Effect

Creates the external identifier on the patient.

- `value` and `patient_id` are required.

## Attributes

| Attribute    | Type   | Description                                    | Required |
|--------------|--------|------------------------------------------------|----------|
| `patient_id` | `str`  | The id of the [patient](/sdk/data-patient/).    | Yes      |
| `system`     | `str`  | The system for the external identifier (url).  | No       |
| `value`      | `str`  | The value of the external identifier.          | Yes      |

## Example


```python
from canvas_sdk.effects.patient import CreatePatientExternalIdentifier

effect = CreatePatientExternalIdentifier(
    patient_id="1eed3ea2a8d546a1b681a2a45de1d790",
    system="https://www.va.gov/",
    value="VET123456"
)

effect.create()
```

This effect will create a new external identifier for the specified patient.

<br/>
<br/>
<br/>