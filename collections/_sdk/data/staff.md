---
title: "Staff"
slug: "data-staff"
excerpt: "Canvas SDK Staff"
hidden: false
---

## Introduction

The `Staff` model represents a staff member in a Canvas instance.

To get a `Staff` object by it's identifier, use the `get` method:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")
```

<!-- source: discussion #548 -->
To list every staff member, use `Staff.objects.all()`. When you need a stable cross-system mapping, prefer the immutable `dbid` (integer) and `id` (UUID) attributes over names, which can change:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.all()

staff_dbids = [s.dbid for s in staff]
staff_ids = [s.id for s in staff]
```

<!-- source: discussion #780 -->
A command's `committer` is a [`CanvasUser`](/sdk/data-canvasuser), not a `Staff` record, so its `dbid` is the user's `dbid` — not the staff `dbid`. To resolve a committer back to the `Staff` record, look it up by `user_id`, not `dbid`:

```python
from canvas_sdk.v1.data.staff import Staff

# command_instance.committer is a CanvasUser
staff = Staff.objects.get(user_id=command_instance.committer.dbid)
```

`Staff` objects are commonly used in related models, for example the `Task` model.
To see all of a staff member's assigned or created tasks, the following code can be used:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")

staff.assignee_tasks.all()
# <QuerySet [<Task: Task object (3)>]>

staff.creator_tasks.all()
# <QuerySet [<Task: Task object (7)>]>
```

To show a Staff member's contact points (email, phone, etc.), the `telecom` attribute can be used. For example:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")

[(t.system, t.value,) for t in staff.telecom.all()]
# [('phone', '8005551416'), ('email', 'support@canvasmedical.com')]
```

To show a `Staff` full name, credentialed name, the topmost clinical role or top role abbreviation use the properties `full_name`, `credentialed_name`, `top_clinical_role` or `top_role_abbreviation`.

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")
staff.full_name
# Larry Weed

staff.credentialed_name
# Larry Weed MD

staff.top_clinical_role.name
# Physician

staff.top_role_abbreviation
# MD
```

When a staff member holds more than one role, `top_clinical_role` looks only at roles in a clinical domain — those whose `domain` is `CLINICAL` or `HYBRID` — and returns the one with the highest `domain_privilege_level`. Administrative roles are never selected, even if they carry a higher privilege level. If the staff member has no clinical or hybrid roles, both `top_clinical_role` and `top_role_abbreviation` are `None`. Because `credentialed_name` appends `top_role_abbreviation`, it reflects the same highest-privilege clinical role.

To get `Staff` licenses. 

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")
staff.licenses.all()
# <QuerySet [<StaffLicense: CA License for Larry Weed>]>

```

## Accessing the staff signature

The `signature_url` property returns a presigned S3 URL for securely accessing the staff member's signature file, when one is on file. If no signature has been uploaded, the property returns `None`.

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")

# Returns a presigned S3 URL (valid for 1 hour) or None
url = staff.signature_url
```

## Attributes

### Staff

| Field Name                 | Type                                                            |
| -------------------------- | --------------------------------------------------------------- |
| id                         | UUID                                                            |
| dbid                       | Integer                                                         |
| created                    | DateTime                                                        |
| modified                   | DateTime                                                        |
| prefix                     | String                                                          |
| suffix                     | String                                                          |
| first_name                 | String                                                          |
| middle_name                | String                                                          |
| last_name                  | String                                                          |
| maiden_name                | String                                                          |
| nickname                   | String                                                          |
| previous_names             | JSON                                                            |
| birth_date                 | Date                                                            |
| sex_at_birth               | [PersonSex](/sdk/data-enumeration-types/#personsex)             |
| sexual_orientation_term    | String                                                          |
| sexual_orientation_code    | String                                                          |
| gender_identity_term       | String                                                          |
| gender_identity_code       | String                                                          |
| preferred_pronouns         | String                                                          |
| biological_race_codes      | Array[String]                                                   |
| biological_race_terms      | Array[String]                                                   |
| cultural_ethnicity_codes   | Array[String]                                                   |
| cultural_ethnicity_terms   | Array[String]                                                   |
| last_known_timezone        | TimeZone                                                        |
| active                     | Boolean                                                         |
| primary_practice_location  | [PracticeLocation](/sdk/data-practicelocation/)                 |
| npi_number                 | String                                                          |
| nadean_number              | String                                                          |
| group_npi_number           | String                                                          |
| bill_through_organization  | Boolean                                                         |
| tax_id                     | String                                                          |
| tax_id_type                | [TaxIDType](/sdk/data-enumeration-types/#taxidtype)             |
| spi_number                 | String                                                          |
| personal_meeting_room_link | URL                                                             |
| language                   | Language                                                        |
| language_secondary         | Language                                                        |
| schedule_column_ordering   | Integer                                                         |
| state                      | JSON                                                            |
| user                       | [CanvasUser](/sdk/data-canvasuser)                              |
| signature                  | String                                                          |
| supervising_team           | [Staff](#staff)[]                                               |
| default_supervising_provider | [Staff](#staff)                                               |
| notes                      | Note[]                                                          |
| supervised_notes           | Note[]                                                          |
| creator_tasks              | [Task](/sdk/data-task/#task)[]                                  |
| assignee_tasks             | [Task](/sdk/data-task/#task)[]                                  |
| comments                   | [TaskComment](/sdk/data-task/#taskcomment)[]                    |
| care_team_memberships      | [CareTeamMembership](/sdk/data-care-team/#careteammembership)[] |
| teams                      | [Team](/sdk/data-team/#team)[]                                  |
| telecom                    | [StaffContactPoint](#staffcontactpoint)[]                       |
| external_identifiers       | [StaffExternalIdentifier](#staffexternalidentifier)[]           |
| metadata                   | [StaffMetadata](#staffmetadata)[]                               |
| addresses                  | [StaffAddress](#staffaddress)[]                                 |
| photos                     | [StaffPhoto](#staffphoto)[]                                     |
| roles                      | [StaffRole](#staffrole)[]                                       |
| licenses                   | [StaffLicense](#stafflicense)[]                                 |
| letters                    | [Letter](/sdk/data-letter/#letter)[]                            |
| imaging_orders             | [ImagingOrder](/sdk/data-imaging/#imagingorder)[]               |
| immunizations_given        | [Immunization](/sdk/data-immunization/#immunization)[]          |
| supervising_prescriptions  | [Prescription](/sdk/data-prescription/#prescription)[]          |
| refill_requests            | [RefillRequest](/sdk/data-refill-request/#refillrequest)[]      |
| default_patients           | [Patient](/sdk/data-patient/#patient)[]                         |
| medication_history_responses | [MedicationHistoryResponse](/sdk/data-medication-history/#medicationhistoryresponse)[] |
| transmissions_delivered    | [MessageTransmission](/sdk/data-message/#messagetransmission)[] |
| integration_task_reviews   | [IntegrationTaskReview](/sdk/data-integration-task/#integrationtaskreview)[] |
| assignee_note_tasks        | [NoteTask](/sdk/data-task/#notetask)[]                          |
| appointment_set            | [Appointment](/sdk/data-appointment/#appointment)[]             |
| prescription_set           | [Prescription](/sdk/data-prescription/#prescription)[]          |
| note_set                   | [Note](/sdk/data-note/#note)[]                                  |

### StaffContactPoint

| Field Name | Type                                                                  |
| ---------- | --------------------------------------------------------------------- |
| id         | UUID                                                                  |
| dbid       | Integer                                                               |
| system     | [ContactPointSystem](/sdk/data-enumeration-types/#contactpointsystem) |
| value      | String                                                                |
| use        | String                                                                |
| use_notes  | String                                                                |
| rank       | Integer                                                               |
| state      | [ContactPointState](/sdk/data-enumeration-types/#contactpointstate)   |
| staff      | [Staff](#staff)                                                       |

### StaffAddress

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
| state       | String                                                  |
| staff       | [Staff](#staff)                                         |

### StaffLicense

| Field Name                          | Type                         |
|-------------------------------------|------------------------------|
| id                                  | UUID                         |      
| dbid                                | Integer                      |
| staff                               | [Staff](#staff)              |
| issuing_authority_long_name         | String                       |
| issuing_authority_url               | URL                          |
| license_or_certification_identifier | String                       |
| issuance_date                       | Date                         |
| expiration_date                     | Date                         |
| license_type                        | [LicenseType](#license-type) |
| primary                             | Boolean                      |
| state                               | String                       |

### StaffPhoto

| Field Name | Type            |
| ---------- | --------------- |
| dbid       | Integer         |
| created    | DateTime        |
| modified   | DateTime        |
| staff      | [Staff](#staff) |
| url        | String          |
| title      | String          |

### StaffRole

| Field Name             | Type                       |
| ---------------------- | -------------------------- |
| dbid                   | Integer                    |
| staff                  | [Staff](#staff)            |
| internal_code          | String                     |
| public_abbreviation    | String                     |
| domain                 | [RoleDomain](#role-domain) |
| name                   | String                     |
| domain_privilege_level | Integer                    |
| permissions            | JSON                       |
| role_type              | [RoleType](#role-type)     |

### StaffExternalIdentifier

| Field Name      | Type            |
| --------------- | --------------- |
| id              | UUID            |
| dbid            | Integer         |
| created         | DateTime        |
| modified        | DateTime        |
| staff           | [Staff](#staff) |
| use             | String          |
| identifier_type | String          |
| system          | String          |
| value           | String          |
| issued_date     | Date            |
| expiration_date | Date            |

```python
from canvas_sdk.v1.data.staff import Staff
from logger import log

staff_id = "4150cd20de8a470aa570a852859ac87e"
staff = Staff.objects.get(id=staff_id)

for identifier in staff.external_identifiers.all():
    log.info(f"Staff external identifier: {identifier.system}, {identifier.value}")
    # https://www.example.com - employee-001
```

<!-- source: discussion #1684 -->
`StaffExternalIdentifier` is the supported way to store and read an external system's ID on a Staff/Practitioner record (the equivalent of `PatientExternalIdentifier` for staff). Plugins read it from this data module and write to it with the [`CreateStaffExternalIdentifier`](/sdk/effect-staff-external-identifier/) effect. Note that the FHIR `Practitioner.identifier[]` field is effectively NPI-only and is not a place to store an arbitrary external ID, so use `StaffExternalIdentifier` instead.

### StaffMetadata

| Field Name | Type            |
| ---------- | --------------- |
| id         | UUID            |
| dbid       | Integer         |
| created    | DateTime        |
| modified   | DateTime        |
| staff      | [Staff](#staff) |
| key        | String          |
| value      | String          |

```python
from canvas_sdk.v1.data.staff import Staff
from logger import log

staff_id = "4150cd20de8a470aa570a852859ac87e"
staff = Staff.objects.get(id=staff_id)

for metadata in staff.metadata.all():
    log.info(f"{metadata.key}={metadata.value}")
```

`StaffMetadata` is a free-form key/value store on a staff member, mirroring
`PatientMetadata`. The `(staff, key)` pair is unique, so a given key has at most
one value per staff member; use the [`StaffMetadata` effect](/sdk/effect-staff-metadata/)
to upsert it from a plugin.

## Enumeration types

### License Type

| Value         | Description   |
|---------------|---------------|
| CLIA          | CLIA          |
| DEA           | DEA           |
| PTAN          | PTAN          |
| STATE_LICENSE | State License |
| TAXONOMY      | Taxonomy      |
| SPI           | SPI           |
| OTHER         | Other         |

### Role Domain

| Value          | Abbreviation | Description    |
| -------------- | ------------ | -------------- |
| CLINICAL       | CLI          | Clinical       |
| ADMINISTRATIVE | ADM          | Administrative |
| HYBRID         | HYB          | Hybrid         |

### Role Type

| Value        | Description  |
| ------------ | ------------ |
| NON_LICENSED | Non-Licensed |
| LICENSED     | Licensed     |
| PROVIDER     | Provider     |



## Computed Properties

- `full_name`: The staff member's first and last name (for example, `Larry Weed`).
- `credentialed_name`: The staff member's full name suffixed with their topmost credential abbreviation (for example, `Larry Weed MD`).
- `top_clinical_role`: The staff member's highest-ranking clinical [StaffRole](#staffrole), selected by privilege level when they hold more than one, or `None` if they have no clinical role.
- `top_role_abbreviation`: The public credential abbreviation of the `top_clinical_role` (for example, `MD`), or `None` if there is no clinical role.
- `photo_url`: The URL of the staff member's photo, if available, or a placeholder image URL.
- `signature_url`: A presigned S3 URL for the staff member's signature file (valid for 1 hour), or `None` if no signature is on file.


<br/>
<br/>
<br/>
