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
| `active`                 | `bool` or `None`                            | Whether the patient record is active        | No       |
| `deceased`               | `bool` or `None`                            | Whether the patient is deceased             | No       |
| `deceased_datetime`      | `datetime.datetime` or `None`               | Date and time of patient's death            | No       |
| `deceased_cause`         | `str` or `None`                             | Cause of patient's death                    | No       |
| `deceased_comment`       | `str` or `None`                             | Additional comments about patient's death   | No       |
| `biological_race_codes`  | `list[str]` or `None`                       | [CDC race codes](#setting-race-and-ethnicity) describing the patient's biological race (e.g., `"2106-3"`) | No       |
| `cultural_ethnicity_codes` | `list[str]` or `None`                     | [CDC ethnicity codes](#setting-race-and-ethnicity) describing the patient's cultural ethnicity (e.g., `"2186-5"`) | No       |
| `previous_names`         | `list[str]` or `None`                       | List of patient's previous names            | No       |
| `contact_points`         | `list[PatientContactPoint]` or `None`       | Patient's contact information               | No       |
| `external_identifiers`   | `list[PatientExternalIdentifier]` or `None` | Patient's external identifiers              | No       |
| `patient_id`             | `str` or `None`                             | Patient id. Required for updates. Optional on creation, where it must be a 32-character hex string (a UUID4 without hyphens) — see [Supplying a patient id on creation](#supplying-a-patient-id-on-creation). | No       |
| `addresses`              | `list[PatientAddress]` or `None`            | Patient's addresses                         | No       |
| `preferred_pharmacies`   | `list[PatientPreferredPharmacy]` or `None`  | Patient's preferred pharmacies              | No       |
| `metadata`               | `list[PatientMetadata]` or `None`           | Patient metadata                            | No       |

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

- **Creation**: Creates new patient records. By default the server generates the patient id, but you may supply your own `patient_id` — see [Supplying a patient id on creation](#supplying-a-patient-id-on-creation)
- **Updates**: Updates existing patient records when `patient_id` is provided
- Validates that referenced practice locations exist in the system
- Verifies that referenced healthcare providers exist in the system
- Structures contact information through the `PatientContactPoint` dataclass
- Structures external identifier through the `PatientExternalIdentifier` dataclass
- Structures address information through the `PatientAddress` dataclass
- Structures metadata through the `PatientMetadata` dataclass

## Example Usage

```python
from canvas_sdk.effects.patient import Patient, PatientContactPoint, PatientExternalIdentifier, PatientMetadata
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.common import ContactPointSystem, ContactPointUse, PersonSex
import datetime


class MyHandler(BaseHandler):
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

## Supplying a patient id on creation

By default, Canvas generates the patient id (`patient_id`) when you create a patient. You can supply your own instead by passing a 32-character hex string (a UUID4 with its hyphens removed) in the `patient_id` parameter of `Patient`. This lets your plugin generate the id up front and reuse it for follow-up, patient-scoped effects — such as notes or commands — in the same plugin execution, without reading the id back first. It works the same way Notes and Commands accept a pre-generated id.

A supplied id must be a well-formed patient id: a 32-character lowercase hex string, which is a UUID4 with its hyphens removed. Use `generate_patient_id()` to produce one rather than building the format by hand. An id in any other format — for example, a hyphenated or uppercase UUID — raises a validation error on `create()`, as does an id that already belongs to an existing patient. Since `generate_patient_id()` returns a fresh, well-formed id, it satisfies both requirements. If you omit `patient_id`, the server generates the id as before, so existing plugins are unaffected.

Because you generate the id up front, you can also return it to the caller from a [SimpleAPI](/sdk/handlers-simple-api-http/) endpoint — so a client creating the patient gets the id back in the response instead of having to look it up afterward. This example authenticates with the [`APIKeyAuthMixin`](/sdk/handlers-simple-api-http/), which expects a `simpleapi-api-key` secret declared in your manifest:

```python
from canvas_sdk.effects.patient import Patient, generate_patient_id
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPIRoute


class CreatePatientAPI(APIKeyAuthMixin, SimpleAPIRoute):
    PATH = "/patients"

    def post(self) -> list[Response]:
        body = self.request.json()
        new_patient_id = generate_patient_id()

        patient = Patient(
            patient_id=new_patient_id,
            first_name=body["first_name"],
            last_name=body["last_name"],
        )

        # `new_patient_id` can be reused for follow-up patient-scoped effects in
        # the same execution, and is returned so the caller has it immediately
        # without a follow-up lookup.
        return [
            patient.create(),
            JSONResponse({"patient_id": new_patient_id}, status_code=201),
        ]
```

# Patient Update Example

```python
from canvas_sdk.effects.patient import Patient, PatientAddress, PatientExternalIdentifier
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.common import AddressUse


class MyHandler(BaseHandler):
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

# Marking a Patient as Inactive or Deceased

```python
from canvas_sdk.effects.patient import Patient
from canvas_sdk.handlers.base import BaseHandler
import datetime


class MyHandler(BaseHandler):
    def compute(self):
        # Mark a patient as inactive
        inactive_patient = Patient(
            patient_id="existing-patient-uuid",
            active=False
        )

        return [inactive_patient.update()]


class DeceasedPatientHandler(BaseHandler):
    def compute(self):
        # Record a patient's death
        deceased_patient = Patient(
            patient_id="existing-patient-uuid",
            deceased=True,
            deceased_datetime=datetime.datetime(2025, 3, 14, 12, 0, 0),
            deceased_cause="Natural causes",
            deceased_comment="Pronounced at home."
        )

        return [deceased_patient.update()]
```

# Setting Race and Ethnicity

`biological_race_codes` and `cultural_ethnicity_codes` each accept a list of code strings drawn from the [CDC Race and Ethnicity CodeSystem (CDCREC)](https://hl7.org/fhir/us/core/STU3.1.1/CodeSystem-cdcrec.html) — the same code set used by the [FHIR Patient API](/api/patient/). You can set both fields when creating or updating a patient, and you can supply more than one code per field.

Canvas recognizes the full CDCREC code set — both the OMB top-level categories below and the more specific detailed codes that roll up to them (for example, the race code `2108-9` "European" rolls up to `2106-3` "White", and the ethnicity code `2148-5` "Mexican" rolls up to `2135-2` "Hispanic or Latino"). The categories below are the most common values; see the CodeSystem for the complete list of detailed codes.

**Race** (`biological_race_codes`) — OMB top-level categories:

| Code      | Description                               |
| --------- | ----------------------------------------- |
| `1002-5`  | American Indian or Alaska Native          |
| `2028-9`  | Asian                                     |
| `2054-5`  | Black or African American                 |
| `2076-8`  | Native Hawaiian or Other Pacific Islander |
| `2106-3`  | White                                     |
| `2131-1`  | Other Race                                |

**Ethnicity** (`cultural_ethnicity_codes`) — OMB top-level categories:

| Code      | Description            |
| --------- | ---------------------- |
| `2135-2`  | Hispanic or Latino     |
| `2186-5`  | Not Hispanic or Latino |

```python
from canvas_sdk.effects.patient import Patient
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self):
        patient = Patient(
            patient_id="existing-patient-uuid",
            biological_race_codes=["2106-3"],      # White
            cultural_ethnicity_codes=["2186-5"]    # Not Hispanic or Latino
        )

        return [patient.update()]
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
   - On creation, if `patient_id` is supplied it must be a well-formed patient id (a 32-character hex string); otherwise validation raises
   - On creation, a supplied `patient_id` must not already belong to an existing patient; a duplicate id raises a validation error
4. **Update-Specific Validation**:
   - Validates that the patient exists before attempting updates

<br/>
<br/>
<br/>
