---
title: "CreatePatientPreferredPharmacies"
slug: "effect-create-patient-preferred-pharmacies"
excerpt: "Effect to create preferred pharmacies for a patient."
hidden: false
---

## CreatePatientPreferredPharmacies

Creates preferred pharmacies for a patient.

### Parameters

| Name       | Type                             | Description                           |
|------------|----------------------------------|---------------------------------------|
| patient_id | `str` or `UUID`                  | The unique identifier of the patient. |
| pharmacies | `list[PatientPreferredPharmacy]` | List of pharmacies to create.         |

### PatientPreferredPharmacy

The `PatientPreferredPharmacy` dataclass represents a patient's preferred pharmacy, and if it's their default pharmacy.

#### Attributes

| Attribute  | Type   | Description                                          | Required                |
|------------|--------|------------------------------------------------------|-------------------------|
| `ncpdp_id` | `str`  | The NCPDC identifier of the pharmacy.                | Yes                     |
| `default`  | `bool` | Indicates if this is the patient's default pharmacy. | No, defaults to `False` |

### Example

```python
from canvas_sdk.effects.patient import CreatePatientPreferredPharmacies
from canvas_sdk.v1.data import Patient as PatientModel

first_patient_id = PatientModel.objects.values_list("id", flat=True).first()
preferred_pharmacies_effect = CreatePatientPreferredPharmacies(
                                pharmacies=[PatientPreferredPharmacy(ncpdp_id="0586163", default=True)],
                                patient_id=first_patient_id
)

effect.create()
```

This effect will create a new preferred pharmacy for the specified patient. 
Since the `default` attribute is set to `True`, it will mark this pharmacy as the patient's default preferred pharmacy.
