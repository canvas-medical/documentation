---
title: "Patient"
slug: "effect-patient"
excerpt: "Effects for patients"
hidden: false
---

# Patient Effect

The `Patient` effect enables the creation of patient records within the Canvas system. This effect captures demographic information, contact details, and clinical associations necessary for patient registration.

## Attributes

| Attribute                | Type                                  | Description                                 | Required |
|--------------------------|---------------------------------------|---------------------------------------------|----------|
| `first_name`             | `str`                                 | Patient's first name                        | Yes      |
| `last_name`              | `str`                                 | Patient's last name                         | Yes      |
| `middle_name`            | `str` or `None`                       | Patient's middle name                       | No       |
| `birthdate`              | `datetime.date` or `None`             | Patient's date of birth                     | No       |
| `prefix`                 | `str` or `None`                       | Name prefix (e.g., "Dr.", "Mr.")            | No       |
| `suffix`                 | `str` or `None`                       | Name suffix (e.g., "Jr.", "III")            | No       |
| `sex_at_birth`           | `PersonSex` or `None`                 | Patient's sex assigned at birth             | No       |
| `nickname`               | `str` or `None`                       | Patient's preferred name or nickname        | No       |
| `social_security_number` | `str` or `None`                       | Patient's SSN                               | No       |
| `administrative_note`    | `str` or `None`                       | Administrative notes about the patient      | No       |
| `clinical_note`          | `str` or `None`                       | Clinical notes about the patient            | No       |
| `default_location_id`    | `str` or `None`                       | ID of patient's default practice location   | No       |
| `default_provider_id`    | `str` or `None`                       | ID of patient's default healthcare provider | No       |
| `previous_names`         | `list[str]` or `None`                 | List of patient's previous names            | No       |
| `contact_points`         | `list[PatientContactPoint]` or `None` | Patient's contact information               | No       |

## PatientContactPoint

The `PatientContactPoint` dataclass represents various methods of contacting the patient.

### Attributes

| Attribute     | Type                 | Description                                                       | Required |
|---------------|----------------------|-------------------------------------------------------------------|----------|
| `system`      | `ContactPointSystem` | Type of contact (e.g., phone, email)                              | Yes      |
| `value`       | `str`                | The contact information value (e.g., phone number, email address) | Yes      |
| `use`         | `ContactPointUse`    | Purpose of the contact point (e.g., home, work)                   | Yes      |
| `rank`        | `int`                | Priority order of contact methods                                 | Yes      |
| `has_consent` | `bool` or `None`     | Whether consent has been given to use this contact method         | No       |

## Implementation Details

- Validates that referenced practice locations exist in the system
- Verifies that referenced healthcare providers exist in the system
- Structures contact information through the `PatientContactPoint` dataclass

## Example Usage

```python
from canvas_sdk.effects.patient import Patient, PatientContactPoint
from canvas_sdk.v1.data.common import ContactPointSystem, ContactPointUse, PersonSex
import datetime

patient = Patient(
    first_name="Jane",
    last_name="Doe",
    middle_name="Marie",
    birthdate=datetime.date(1980, 1, 15),
    sex_at_birth=PersonSex.SEX_FEMALE,
    nickname="Janie",
    default_location_id="location-uuid",
    default_provider_id="provider-uuid",
    contact_points=[
        PatientContactPoint(
            system=ContactPointSystem.PHONE,
            value="555-123-4567",
            use=ContactPointUse.MOBILE,
            rank=1,
            has_consent=True
        ),
        PatientContactPoint(
            system=ContactPointSystem.EMAIL,
            value="jane.doe@example.com",
            use=ContactPointUse.WORK,
            rank=2,
            has_consent=True
        )
    ]
)

return patient.create()
```

## Validation

The effect performs validation before execution to ensure data integrity:

1. **Required Fields**: Validates that mandatory fields like `first_name` and `last_name` are provided
2. **Referenced Entity Validation**: Confirms that any referenced entities exist in the system:
   - Verifies that the specified default practice location exists
   - Ensures that the specified default provider exists
3. **Data Format Validation**: Ensures that provided values conform to expected formats:
   - Date fields must be valid dates
   - Enumerated types like `PersonSex`, `ContactPointSystem`, and `ContactPointUse` must contain valid values
