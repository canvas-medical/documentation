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
| allergy_intolerances     | [AllergyIntolerance](/sdk/data-allergy-intolerance/#allergyintolerance)[] |
| billing_line_items       | BillingLineItem[]                                                         |
| care_team_memberships    | [CareTeamMembership](/sdk/data-care-team/#careteammembership)[]           |
| conditions               | [Condition](/sdk/data-condition/#condition)[]                             |
| coverages                | [Coverage](/sdk/data-coverage/#coverage)[]                                |
| dependent_coverages      | [Coverage](/sdk/data-coverage/#coverage)[]                                |
| detected_issues          | [DetectedIssue](/sdk/data-detected-issue/#detectedissue)[]                |
| devices                  | [Device](/sdk/data-device/#device)[]                                      |
| imaging_orders           | [ImagingOrder](/sdk/data-imaging/#imagingorder)[]                         |
| imaging_reports          | [ImagingReport](/sdk/data-imaging/#imagingreport)[]                       |
| imaging_reviews          | [ImagingReview](/sdk/data-imaging/#imagingreview)[]                       |
| interviews               | [Interview](/sdk/data-questionnaire/#interview)[]                         |
| lab_orders               | [LabOrder](/sdk/data-labs/#laborder)[]                                    |
| lab_reports              | [LabReport](/sdk/data-labs/#labreport)[]                                  |
| lab_reviews              | [LabReview](/sdk/data-labs/#labreview)[]                                  |
| medications              | [Medication](/sdk/data-medication/#medication)[]                          |
| observations             | [Observation](/sdk/data-observation/#observation)[]                       |
| external_identifiers     | [PatientExternalIdentifier](#patientexternalidentifier)[]                 |
| preferred_pharmacy       | JSON                                                                      |
| protocol_overrides       | [ProtocolOverride](/sdk/data-protocol-override/#protocoloverride)[]       |
| settings                 | [PatientSetting](#patientsetting)                                         |
| subscribed_coverages     | [Coverage](/sdk/data-coverage/#coverage)[]                                |
| tasks                    | [Task](/sdk/data-task/#task)[]                                            |
| telecom                  | [PatientContactPoint](#patientcontactpoint)[]                             |
| user                     | [CanvasUser](/sdk/data-user/)[]                                                 |

### PatientAddress

| Field Name  | Type                                                    |
|-------------|---------------------------------------------------------|
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
| state       | String                                                  |
| patient     | [Patient](#patient)                                     |

### PatientContactPoint

| Field Name         | Type                                                                  |
|--------------------|-----------------------------------------------------------------------|
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

### PatientExternalIdentifier

| Field Name      | Type                |
|-----------------|---------------------|
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

### PatientSetting

| Field Name | Type                |
|------------|---------------------|
| dbid       | Integer             |
| created    | DateTime            |
| modified   | DateTime            |
| patient    | [Patient](#patient) |
| name       | String              |
| value      | JSON                |

## Enumeration types

### SexAtBirth

| Value             | Label   |
|-------------------|---------|
| F                 | female  |
| M                 | male    |
| O                 | other   |
| UNK               | unknown |
| "" (empty string) | ""      |

<br/>
<br/>
<br/>
