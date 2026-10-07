---
title: "CreatePatientPreferredPharmacies"
slug: "effect-create-patient-preferred-pharmacies"
excerpt: "Effect to create preferred pharmacies for a patient."
hidden: false
---

Creates preferred pharmacies for a patient.

## Methods

### create() → Effect

Sets the patient's preferred pharmacies.

- `patient_id` and `pharmacies` are required, and `patient_id` must be the id of an existing patient.
- At most one pharmacy in `pharmacies` can be marked as the default.

## Attributes

| Attribute    | Type                                                       | Description                           | Required |
|--------------|------------------------------------------------------------|---------------------------------------|----------|
| `patient_id` | `str` or `UUID`                                            | The id of the [patient](/sdk/data-patient/). | Yes      |
| `pharmacies` | list[[PatientPreferredPharmacy](#patientpreferredpharmacy)] | List of pharmacies to create.         | Yes      |

## PatientPreferredPharmacy

The `PatientPreferredPharmacy` dataclass represents a patient's preferred pharmacy, and if it's their default pharmacy.

### Attributes

| Attribute  | Type   | Description                                          | Required                |
|------------|--------|------------------------------------------------------|-------------------------|
| `ncpdp_id` | `str`  | The NCPDC identifier of the pharmacy.                | Yes                     |
| `default`  | `bool` | Indicates if this is the patient's default pharmacy. Defaults to `False`. | No |

### Validation

When this effect is interpreted, Canvas validates the `ncpdp_id` before setting the preferred pharmacy. If the `ncpdp_id` is invalid or does not exist, the effect will fail.

To ensure the `ncpdp_id` exists before using this effect, you can verify it using Canvas's [pharmacy HTTP utility](/sdk/utils/#making-requests-to-the-pharmacy-service) to check the pharmacy beforehand.

## Example

```python
from canvas_sdk.effects.patient import CreatePatientPreferredPharmacies, PatientPreferredPharmacy
from canvas_sdk.v1.data import Patient as PatientModel

first_patient_id = PatientModel.objects.values_list("id", flat=True).first()

preferred_pharmacies_effect = CreatePatientPreferredPharmacies(
                                pharmacies=[PatientPreferredPharmacy(ncpdp_id="0586163", default=True)],
                                patient_id=first_patient_id
)

preferred_pharmacies_effect.create()
```

This effect will create a new preferred pharmacy for the specified patient.

Since the `default` attribute is set to `True`, it will mark this pharmacy as the patient's default preferred pharmacy.

<br/>
<br/>
<br/>