---
title: "Patient Effect"
slug: "effect-patient"
excerpt: "Effects for patients"
hidden: false
---

The `Patient` effect enables the creation and updating of patient records within the Canvas system. This effect captures demographic information, contact details, and clinical associations necessary for patient registration and updates.

## Attributes

| Attribute                | Type                                        | Description                                 | Required |
| ------------------------ | ------------------------------------------- | ------------------------------------------- | -------- |
| `first_name`             | `str`                                       | Patient's first name                        | Yes      |
| `last_name`              | `str`                                       | Patient's last name                         | Yes      |
| `middle_name`            | `str` or `None`                             | Patient's middle name                       | No       |
| `birthdate`              | `datetime.date` or `None`                   | Patient's date of birth                     | No       |
| `prefix`                 | `str` or `None`                             | Name prefix (e.g., "Dr.", "Mr.")            | No       |
| `suffix`                 | `str` or `None`                             | Name suffix (e.g., "Jr.", "III")            | No       |
| `sex_at_birth`           | `PersonSex` or `None`                       | Patient's sex assigned at birth             | No       |
| `nickname`               | `str` or `None`                             | Patient's preferred name or nickname        | No       |
| `social_security_number` | `str` or `None`                             | Patient's SSN                               | No       |
| `administrative_note`    | `str` or `None`                             | Administrative notes about the patient      | No       |
| `clinical_note`          | `str` or `None`                             | Clinical notes about the patient            | No       |
| `default_location_id`    | `str` or `None`                             | ID of patient's default practice location   | No       |
| `default_provider_id`    | `str` or `None`                             | ID of patient's default healthcare provider | No       |
| `previous_names`         | `list[str]` or `None`                       | List of patient's previous names            | No       |
| `contact_points`         | `list[PatientContactPoint]` or `None`       | Patient's contact information               | No       |
| `external_identifiers`   | `list[PatientExternalIdentifier]` or `None` | Patient's external identifiers              | No       |
| `patient_id`             | `str` or `None`                             | Patient ID (required for updates only)      | No       |
| `addresses`              | `list[PatientAddress]` or `None`            | Patient's addresses                         | No       |
| `preferred_pharmacies`   | `list[PatientPreferredPharmacy]` or `None`  | Patient's preferred pharmacies              | No       |
| `preferred_pharmacies`   | `list[PatientMetadata]` or `None`           | Patient metadata                            | No       |

## PatientContactPoint

The `PatientContactPoint` dataclass represents various methods of contacting the patient.

### Attributes

| Attribute     | Type                 | Description                                                       | Required |
| ------------- | -------------------- | ----------------------------------------------------------------- | -------- |
| `system`      | `ContactPointSystem` | Type of contact (e.g., phone, email)                              | Yes      |
| `value`       | `str`                | The contact information value (e.g., phone number, email address) | Yes      |
| `use`         | `ContactPointUse`    | Purpose of the contact point (e.g., home, work)                   | Yes      |
| `rank`        | `int`                | Priority order of contact methods                                 | Yes      |
| `has_consent` | `bool` or `None`     | Whether consent has been given to use this contact method         | No       |

## PatientExternalIdentifier

The `PatientExternalIdentifier` dataclass represents an external identifier (ID) associated with the patient. An example would be the unique patient ID for a third party system integrated with Canvas EMR.

### Attributes

| Attribute | Type  | Description                                                                              | Required |
| --------- | ----- | ---------------------------------------------------------------------------------------- | -------- |
| `system`  | `str` | URL of the system of origin for the external ID (e.g., `http://hl7.org/fhir/sid/us-ssn`) | Yes      |
| `value`   | `str` | The external ID or membership number/value                                               | Yes      |

## PatientAddress

The `PatientAddress` dataclass represents a patient's address information.

### Attributes

| Attribute     | Type            | Description                     | Required |
| ------------- | --------------- | ------------------------------- | -------- |
| `line1`       | `str`           | Street address line 1           | Yes      |
| `line2`       | `str` or `None` | Street address line 2           | No       |
| `city`        | `str`           | City name                       | Yes      |
| `state_code`  | `str`           | State code (e.g., "CA", "NY")   | Yes      |
| `postal_code` | `str`           | Postal/ZIP code                 | Yes      |
| `country`     | `str`           | Country code                    | Yes      |
| `use`         | `AddressUse`    | Address type (e.g., home, work) | Yes      |

{% include alert.html type="warning" content="Address updates are <b>replace-based</b>. When updating a patient's addresses, the provided address list will completely replace all existing addresses. If you provide an empty list, all existing addresses will be deleted." %}

## PatientPreferredPharmacy

The `PatientPreferredPharmacy` dataclass represents a patient's preferred pharmacy, and if it's their default pharmacy.

| Attribute  | Type   | Description                       | Required |
| ---------- | ------ | --------------------------------- | -------- |
| `ncpdp_id` | `str`  | The ncpdp ID of the pharmacy      | Yes      |
| `default`  | `bool` | True if it's the default pharmacy | Yes      |

## PatientMetadata

The `PatientMetadata` dataclass represents a custom key-value pair for a patient.

| Attribute | Type  | Description               | Required |
| --------- | ----- | ------------------------- | -------- |
| `key`     | `str` | The key of the metadata   | Yes      |
| `value`   | `str` | The value of the metadata | Yes      |

## Implementation Details

- **Creation**: Creates new patient records when `patient_id` is not provided
- **Updates**: Updates existing patient records when `patient_id` is provided
- Validates that referenced practice locations exist in the system
- Verifies that referenced healthcare providers exist in the system
- Structures contact information through the `PatientContactPoint` dataclass
- Structures external identifier through the `PatientExternalIdentifier` dataclass
- Structures address information through the `PatientAddress` dataclass
- Structures metadata through the `PatientMetadata` dataclass

## Example Usage

```python?partial=true
from canvas_sdk.effects.patient.base import (
    Patient,
    PatientAddress,
    PatientContactPoint,
    PatientExternalIdentifier,
    PatientMetadata,
    PatientPreferredPharmacy,
)
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.common import ContactPointSystem, ContactPointUse, PersonSex
import datetime


class Protocol(BaseHandler):
    def compute(self):
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
            ],
            external_identifiers=[
                PatientExternalIdentifier(
                    system="http://www.aaa.com",
                    value="pat_id_123456"
                )
            ],
            metadata = [
                PatientMetadata(key="source", value="plugin"),
                PatientMetadata(key="created_on", value=datetime.datetime.now().isoformat())
            ]
        )

        return [patient.create()]
```

# Patient Update Example

```python
from canvas_sdk.effects.patient import Patient, PatientAddress, PatientExternalIdentifier
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.common import AddressUse


class Protocol(BaseHandler):
    def compute(self):
        # Update an existing patient
        updated_patient = Patient(
            patient_id="existing-patient-uuid",
            first_name="Jane",
            last_name="Smith",  # Changed last name
            addresses=[
                PatientAddress(
                    line1="456 Updated Street",
                    line2="Suite 200",
                    city="Updated City",
                    state_code="CA",
                    postal_code="90210",
                    country="US",
                    use=AddressUse.HOME
                )
            ],
            external_identifiers=[
                PatientExternalIdentifier(
                    system="http://www.updated-system.com",
                    value="new_patient_id_789"
                )
            ]
        )

        return [updated_patient.update()]
```

## Validation

The effect performs validation before execution to ensure data integrity:

1. **Required Fields**:
   - For creation: Validates that mandatory fields like `first_name` and `last_name` are provided
   - For updates: Requires `patient_id` to be provided and verifies the patient exists in the database
2. **Referenced Entity Validation**: Confirms that any referenced entities exist in the system:
   - Verifies that the specified default practice location exists
   - Ensures that the specified default provider exists
3. **Data Format Validation**: Ensures that provided values conform to expected formats:
   - Date fields must be valid dates
   - Enumerated types like `PersonSex`, `ContactPointSystem`, and `ContactPointUse` must contain valid values
4. **Update-Specific Validation**:
   - Ensures `patient_id` is not provided during patient creation
   - Validates that the patient exists before attempting updates

<br/>
<br/>
<br/>