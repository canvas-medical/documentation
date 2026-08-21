---
title: "Patient"
slug: "data-patient"
excerpt: "Canvas SDK Patient"
hidden: false
---

## Introduction

The `Patient` model represents an individual receiving care or other health-related services.

## Basic usage

To get a patient by identifier, use the `get` method on the `Patient` model manager:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")
```

## Filtering

Patients can be filtered by any attribute that exists on the model.

Filtering for patients is done with the `filter` method on the `Patient` model manager.

### By attribute

Specify attributes with `filter` to filter by those attributes:

```python
from canvas_sdk.v1.data.patient import Patient

patients = Patient.objects.filter(first_name="Bob", last_name="Loblaw", birth_date="1960-09-22")
```

## Accessing the patient photo

The `photo_url` property returns a presigned S3 URL for securely accessing the patient's uploaded avatar photo. If the patient has no uploaded avatar, the property returns a default avatar URL instead — so the value is always safe to render without a null check.

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="d7af3e356368446c85b40a5d6ff7288e")

# Returns a presigned S3 URL (valid for 1 hour), or the default avatar URL when no photo is on file
url = patient.photo_url
```

If you need the underlying [`PatientPhoto`](#patientphoto) record (for example, to read the original `url` or `title`), use the `photo` property:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="d7af3e356368446c85b40a5d6ff7288e")

photo = patient.photo  # PatientPhoto or None

if photo:
    print(photo.title)
```

## Accessing educational materials

If you have a `Patient` object, the educational materials recorded on their notes can be accessed with the `education_material` reverse relation:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="d7af3e356368446c85b40a5d6ff7288e")
educational_materials = patient.education_material.all()
```

## Attributes

### Patient

| Field Name               | Type                                                                      |
|--------------------------|---------------------------------------------------------------------------|
| id                       | String                                                                    |
| dbid                     | Integer                                                                   |
| first_name               | String                                                                    |
| last_name                | String                                                                    |
| birth_date               | Date                                                                      |
| sex_at_birth             | [SexAtBirth](#sexatbirth)                                                 |
| created                  | DateTime                                                                  |
| modified                 | DateTime                                                                  |
| prefix                   | String                                                                    |
| suffix                   | String                                                                    |
| middle_name              | String                                                                    |
| maiden_name              | String                                                                    |
| nickname                 | String                                                                    |
| sexual_orientation_term  | String                                                                    |
| sexual_orientation_code  | String                                                                    |
| gender_identity_term     | String                                                                    |
| gender_identity_code     | String                                                                    |
| preferred_pronouns       | String                                                                    |
| biological_race_codes    | Array[String]                                                             |
| cultural_ethnicity_codes | Array[String]                                                             |
| last_known_timezone      | String                                                                    |
| mrn                      | String                                                                    |
| active                   | Boolean                                                                   |
| deceased                 | Boolean                                                                   |
| deceased_datetime        | DateTime                                                                  |
| deceased_cause           | String                                                                    |
| deceased_comment         | String                                                                    |
| other_gender_description | String                                                                    |
| social_security_number   | String                                                                    |
| administrative_note      | String                                                                    |
| clinical_note            | String                                                                    |
| mothers_maiden_name      | String                                                                    |
| multiple_birth_indicator | Boolean                                                                   |
| birth_order              | Integer                                                                   |
| default_location_id      | Integer                                                                   |
| default_provider_id      | Integer                                                                   |
| addresses                | [PatientAddress](#patientaddress)[]                                       |
| allergy_intolerances     | [AllergyIntolerance](/sdk/data-allergy-intolerance/#allergyintolerance)[] |
| billing_line_items       | [BillingLineItem](/sdk/data-billing-line-item/)                           |
| business_line            | [BusinessLine](/sdk/data-business-line/)                                  |
| care_team_memberships    | [CareTeamMembership](/sdk/data-care-team/#careteammembership)[]           |
| change_medications       | [ChangeMedication](/sdk/data-change-medication/#changemedication)[]       |
| conditions               | [Condition](/sdk/data-condition/#condition)[]                             |
| coverages                | [Coverage](/sdk/data-coverage/#coverage)[]                                |
| dependent_coverages      | [Coverage](/sdk/data-coverage/#coverage)[]                                |
| detected_issues          | [DetectedIssue](/sdk/data-detected-issue/#detectedissue)[]                |
| devices                  | [Device](/sdk/data-device/#device)[]                                      |
| external_identifiers     | [PatientExternalIdentifier](#patientexternalidentifier)[]                 |
| identification_cards     | [PatientIdentificationCard](#patientidentificationcard)[]                 |
| imaging_orders           | [ImagingOrder](/sdk/data-imaging/#imagingorder)[]                         |
| imaging_results          | [ImagingReport](/sdk/data-imaging/#imagingreport)[]                       |
| imaging_reviews          | [ImagingReview](/sdk/data-imaging/#imagingreview)[]                       |
| interviews               | [Interview](/sdk/data-questionnaire/#interview)[]                         |
| lab_orders               | [LabOrder](/sdk/data-labs/#laborder)[]                                    |
| lab_reports              | [LabReport](/sdk/data-labs/#labreport)[]                                  |
| lab_reviews              | [LabReview](/sdk/data-labs/#labreview)[]                                  |
| medications              | [Medication](/sdk/data-medication/#medication)[]                          |
| metadata                 | [PatientMetadata](#patientmetadata)[]                                     |
| observations             | [Observation](/sdk/data-observation/#observation)[]                       |
| photos                   | [PatientPhoto](#patientphoto)[]                                           |
| preferred_pharmacy       | JSON                                                                      |
| preferred_pharmacies     | JSON                                                                      |
| protocol_overrides       | [ProtocolOverride](/sdk/data-protocol-override/#protocoloverride)[]       |
| settings                 | [PatientSetting](#patientsetting)                                         |
| subscribed_coverages     | [Coverage](/sdk/data-coverage/#coverage)[]                                |
| tasks                    | [Task](/sdk/data-task/#task)[]                                            |
| telecom                  | [PatientContactPoint](#patientcontactpoint)[]                             |
| contacts                 | [PatientContactPerson](#patientcontactperson)[]                           |
| related_contacts         | [PatientContactPerson](#patientcontactperson)[] — contacts on *other* patients that reference this one |
| user                     | [CanvasUser](/sdk/data-canvasuser/)[]                                     |
| patient_groups           | [PatientGroup](/sdk/data-patient-group/)[]                                |
| chart_section_reviews    | [ChartSectionReview](/sdk/data-chart-section-review/#chartsectionreview)[]|
| visual_exam_findings     | [VisualExamFinding](/sdk/data-visual-exam-finding/#visualexamfinding)[]   |
| assessments              | [Assessment](/sdk/data-assessment/#assessment)[]                          |
| patient_visits           | [ExternalVisit](/sdk/data-external-event/#externalvisit)[]                |
| patient_events           | [ExternalEvent](/sdk/data-external-event/#externalevent)[]                |
| medication_statements    | [MedicationStatement](/sdk/data-medication-statement/#medicationstatement)[] |
| diagnostic_reports       | DiagnosticReport[]        |
| medication_history_medications | [MedicationHistoryMedication](/sdk/data-medication-history/#medicationhistorymedication)[] |
| medication_history_responses | [MedicationHistoryResponse](/sdk/data-medication-history/#medicationhistoryresponse)[] |
| payments                 | [BulkPatientPosting](/sdk/data-posting/#bulkpatientposting)[]              |
| protocol_currents        | [ProtocolCurrent](/sdk/data-protocol-current/)[]           |
| stopped_medications      | [StopMedicationEvent](/sdk/data-stop-medication-event/#stopmedicationevent)[] |
| banner_alerts            | [BannerAlert](/sdk/data-banner-alert/#banneralert)[]                       |
| immunizations            | [Immunization](/sdk/data-immunization/#immunization)[]                     |
| immunization_statements  | [ImmunizationStatement](/sdk/data-immunization/#immunizationstatement)[]   |
| integration_tasks        | [IntegrationTask](/sdk/data-integration-task/#integrationtask)[]           |
| installment_plans        | [InstallmentPlan](/sdk/data-claim/#installmentplan)[]                      |
| uncategorized_clinical_document_reviews | [UncategorizedClinicalDocumentReview](/sdk/data-uncategorized-clinical-document/#uncategorizedclinicaldocumentreview)[] |
| patient_consent          | [PatientConsent](/sdk/data-patient-consent/#patientconsent)[]              |
| goals                    | [Goal](/sdk/data-goal/#goal)[]                                             |
| updategoals              | [UpdateGoal](/sdk/data-goal/#updategoal)[]                                 |
| instructions             | [Instruction](/sdk/data-instruction/#instruction)[]                        |
| appointments             | [Appointment](/sdk/data-appointment/#appointment)[]                        |
| notes                    | [Note](/sdk/data-note/#note)[]                                             |
| prescriptions            | [Prescription](/sdk/data-prescription/#prescription)[]                     |
| refill_requests          | [RefillRequest](/sdk/data-refill-request/#refillrequest)[]                 |
| referral_reviews         | [ReferralReview](/sdk/data-referral/#referralreview)[]                     |
| referral_reports         | [ReferralReport](/sdk/data-referral/#referralreport)[]                     |
| invoices                 | Invoice[]                                    |
| education_material       | [EducationalMaterial](/sdk/data-educational-material/#educationalmaterial)[]  |

### PatientAddress

| Field Name  | Type                                                    |
| ----------- | ------------------------------------------------------- |
| id          | UUID                                                    |
| dbid        | Integer                                                 |
| line1       | String                                                  |
| line2       | String                                                  |
| city        | String                                                  |
| district    | String                                                  |
| state_code  | String                                                  |
| postal_code | String                                                  |
| use         | [AddressUse](/sdk/data-enumeration-types/#addressuse)   |
| type        | [AddressType](/sdk/data-enumeration-types/#addresstype) |
| longitude   | Float                                                   |
| latitude    | Float                                                   |
| start       | Date                                                    |
| end         | Date                                                    |
| country     | String                                                  |
| state       | [AddressState](/sdk/data-enumeration-types/#addressstate) |
| patient     | [Patient](#patient)                                     |

```python
from canvas_sdk.v1.data.patient import Patient
from logger import log

patient_id = "d7af3e356368446c85b40a5d6ff7288e"
patient = Patient.objects.get(id=patient_id)
patient_addresses = patient.addresses.all()

for addr in patient_addresses:
  log.info(f"Patient address: {addr.city}, {addr.state_code}, {addr.postal_code}") # Seattle, WA, 98118
```

### PatientContactPoint

| Field Name         | Type                                                                  |
| ------------------ | --------------------------------------------------------------------- |
| id                 | UUID                                                                  |
| dbid               | Integer                                                               |
| system             | [ContactPointSystem](/sdk/data-enumeration-types/#contactpointsystem) |
| value              | String                                                                |
| use                | String                                                                |
| use_notes          | String                                                                |
| rank               | Integer                                                               |
| state              | [ContactPointState](/sdk/data-enumeration-types/#contactpointstate)   |
| patient            | Patient                                                               |
| has_consent        | Boolean                                                               |
| last_verified      | DateTime                                                              |
| verification_token | String                                                                |
| opted_out          | Boolean                                                               |

```python
from canvas_sdk.v1.data.patient import Patient
from logger import log

patient_id = "d7af3e356368446c85b40a5d6ff7288e"
patient = Patient.objects.get(id=patient_id)
patient_contacts = patient.telecom.all()

for contact in patient_contacts:
   log.info(f"Patient contact: {contact.system} - {contact.value}") # phone - 5555555555
```

### PatientExternalIdentifier

| Field Name      | Type                |
| --------------- | ------------------- |
| id              | UUID                |
| dbid            | Integer             |
| created         | DateTime            |
| modified        | DateTime            |
| patient         | [Patient](#patient) |
| use             | String              |
| identifier_type | String              |
| system          | String              |
| value           | String              |
| issued_date     | Date                |
| expiration_date | Date                |

```python
from canvas_sdk.v1.data.patient import Patient
from logger import log

patient_id = "d7af3e356368446c85b40a5d6ff7288e"
patient = Patient.objects.get(id=patient_id)
patient_external_identifiers = patient.external_identifiers.all()

for identifier in patient_external_identifiers:
   log.info(f"Patient external identifier: {identifier.system}, {identifier.value}")  # https://www.example.com - abc123
```

### PatientSetting

| Field Name | Type                |
| ---------- | ------------------- |
| dbid       | Integer             |
| created    | DateTime            |
| modified   | DateTime            |
| patient    | [Patient](#patient) |
| name       | String              |
| value      | JSON                |

### PatientMetadata

| Field Name | Type                |
| ---------- | ------------------- |
| id         | UUID                |
| dbid       | Integer             |
| created    | DateTime            |
| modified   | DateTime            |
| patient    | [Patient](#patient) |
| key        | String              |
| value      | String              |

```python
from canvas_sdk.v1.data.patient import Patient
from logger import log

patient_id = "d7af3e356368446c85b40a5d6ff7288e"
patient = Patient.objects.get(id=patient_id)
patient_metadata = patient.metadata.all()

for metadata in patient_metadata:
   log.info(f"Patient metadata: {metadata.key}, {metadata.value}") # favorite_color - red
```

### PatientPhoto

Represents a patient's uploaded avatar photo.

| Field Name | Type                |
|------------|---------------------|
| dbid       | Integer             |
| created    | DateTime            |
| modified   | DateTime            |
| patient    | [Patient](#patient) |
| url        | String              |
| title      | String              |

```python
from canvas_sdk.v1.data.patient import Patient
from logger import log

patient = Patient.objects.get(id="d7af3e356368446c85b40a5d6ff7288e")

for photo in patient.photos.all():
    log.info(f"Photo: {photo.title}, stored at: {photo.url}")
```

### PatientIdentificationCard

Represents a patient identification card image (e.g., driver's license, insurance card).

| Field Name | Type                      |
|------------|---------------------------|
| dbid       | Integer                   |
| created    | DateTime                  |
| modified   | DateTime                  |
| patient    | [Patient](#patient)       |
| image      | String                    |
| title      | String                    |
| active     | Boolean                   |
| image_url  | String (property) — presigned S3 URL |

```python
from canvas_sdk.v1.data.patient import Patient
from logger import log

patient = Patient.objects.get(id="d7af3e356368446c85b40a5d6ff7288e")

for card in patient.identification_cards.filter(active=True):
    log.info(f"ID card: {card.title}, URL: {card.image_url}")
```

### PatientFacilityAddress

| Field Name     | Type                              |
| -------------- | --------------------------------- |
| patientaddress | [PatientAddress](#PatientAddress) |
| facility       | [Facility](#facility)             |
| room_number    | String                            |

### PatientContactPerson

One of the patient's contacts — an emergency contact, next-of-kin, or other related person. A contact either holds the person's details directly, or references another Canvas patient through `related_patient`; when it does, that patient's own details supersede the values stored here.

`id` is the value the [Patient effect](/sdk/effect-patient/#managing-patient-contacts) takes as `contact_identifier` when modifying or removing a contact.

| Field Name      | Type                                                                 |
| --------------- | -------------------------------------------------------------------- |
| id              | UUID                                                                 |
| dbid            | Integer                                                              |
| created         | DateTime                                                             |
| modified        | DateTime                                                             |
| patient         | [Patient](#patient)                                                  |
| name            | String                                                               |
| phone_number    | String                                                               |
| email           | String                                                               |
| comments        | String                                                               |
| related_patient | [Patient](#patient)                                                  |
| categories      | [PatientContactCategory](#patientcontactcategory)[]                  |

```python
from canvas_sdk.v1.data import PatientContactPerson
from logger import log

contacts = PatientContactPerson.objects.filter(
    patient__id="d7af3e356368446c85b40a5d6ff7288e"
).select_related("related_patient").prefetch_related("categories__category")

for contact in contacts:
    who = contact.related_patient.first_name if contact.related_patient else contact.name
    codings = ", ".join(link.category.code for link in contact.categories.all())
    log.info(f"Contact: {who} ({codings})")  # Contact: Jane (EMC)
```

### PatientContactCategory

Links one of the patient's contacts to one of the category codings the instance defines.

| Field Name     | Type                                                |
| -------------- | --------------------------------------------------- |
| dbid           | Integer                                             |
| created        | DateTime                                            |
| modified       | DateTime                                            |
| contact_person | [PatientContactPerson](#patientcontactperson)       |
| category       | [ContactCategory](#contactcategory)                 |

### ContactCategory

A contact-category coding available in this Canvas instance — the set a contact's relationship can be drawn from.

Use this to look up a coding before writing it with the [Patient effect](/sdk/effect-patient/#patientcontactcategory). Writing a coding that does not appear here is rejected rather than created, so querying this model first is how you find out what the instance actually has.

| Field Name | Type    |
| ---------- | ------- |
| dbid       | Integer |
| name       | String  |
| code       | String  |
| system     | String  |
| protected  | Boolean |

```python
from canvas_sdk.v1.data import ContactCategory
from logger import log

for coding in ContactCategory.objects.order_by("code"):
    log.info(f"{coding.code} / {coding.system} — {coding.name}")  # EMC / INTERNAL — Emergency contact
```

## Enumeration types

### SexAtBirth

| Value             | Label   |
| ----------------- | ------- |
| F                 | female  |
| M                 | male    |
| O                 | other   |
| UNK               | unknown |
| "" (empty string) | ""      |

## Computed Properties

### Patient

- `full_name`: The full name of the patient, combining first, middle, and last names.
- `preferred_pharmacy`: The patient's preferred pharmacy for medication fulfillment.
- `preferred_full_name`: The patient's preferred full name, if different from the legal name.
- `preferred_first_name`: The patient's preferred first name, if different from the legal first name.
- `primary_phone_number`: The patient's primary contact number.
- `photo`: The patient's first uploaded avatar [PatientPhoto](#patientphoto), if any.
- `photo_url`: A presigned URL for the patient's avatar photo, or the default avatar URL when no photo is set.

<br/>
<br/>
<br/>
