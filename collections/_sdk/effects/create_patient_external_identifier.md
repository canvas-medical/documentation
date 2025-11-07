---
title: "CreatePatientExternalIdentifier"
slug: "effect-create-patient-external-identifier"
excerpt: "Effect to create a new external identifier for a patient."
hidden: false
---

Creates a new external identifier for a patient.

### Parameters

| Name      | Type   | Description                                 |
|-----------|--------|---------------------------------------------|
| patient_id| UUID   | The unique identifier of the patient.        |
| system    | String | The system for the external identifier (url).      |
| value     | String | The value of the external identifier.        |

### Example

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
