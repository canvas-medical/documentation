---
title: "Note"
slug: "data-note"
excerpt: "Canvas SDK Note"
hidden: false
---

## Introduction

The `Note` model represents clinical notes that appear on a patient's chart. A `Note` can contain multiple [commands](/sdk/data-command).

## Basic usage

To get a note by identifier, use the `get` method on the `Note` model manager:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
```

If you have a patient object, the notes for a patient can be found using the `notes` attribute on the `Patient` instance:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="fd2ecd87c26044a6a755287f296dd17f")
patient_notes = patient.notes.all()
```

## Filtering

### By attribute

Notes can also be filtered by attribute. For example, to get all notes for a patient where the `datetime_of_service` is after a certain date, the following code can be used:

```python
import arrow

from canvas_sdk.v1.data.note import Note
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="fd2ecd87c26044a6a755287f296dd17f")
recent_notes = Note.objects.filter(
    patient=patient,
    datetime_of_service__gte=arrow.now().shift(weeks=-3).datetime
)
```

The `NoteType` model can also be used to find notes by type.

```python
from canvas_sdk.v1.data.note import NoteType
from canvas_sdk.v1.data.patient import Patient

note_type = NoteType.objects.get(name="Office visit")
patient = Patient.objects.get(id="fd2ecd87c26044a6a755287f296dd17f")
patient_office_visits = Note.objects.filter(patient=patient, note_type_version=note_type)
```

All of the [commands](/sdk/data-command) in a `Note` can be found by using the `commands` attribute:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
commands_in_note = Note.commands.all()
```

## Attributes

### Note

| Field Name          | Type                                  |
|---------------------|---------------------------------------|
| id                  | UUID                                  |
| dbid                | Integer                               |
| created             | DateTime                              |
| modified            | DateTime                              |
| patient             | [Patient](/sdk/data-patient/#patient) |
| note_type_version   | [NoteType](#notetype)                 |
| title               | String                                |
| body                | JSON                                  |
| originator          | [CanvasUser](/sdk/data-canvasuser)    |
| checksum            | String                                |
| billing_note        | String                                |
| related_data        | JSON                                  |
| datetime_of_service | DateTime                              |
| place_of_service    | String                                |

### NoteType

| Field Name                                  | Type                                      |
|---------------------------------------------|-------------------------------------------|
| dbid                                        | Integer                                   |
| created                                     | DateTime                                  |
| modified                                    | DateTime                                  |
| system                                      | String                                    |
| version                                     | String                                    |
| code                                        | String                                    |
| display                                     | String                                    |
| user_selected                               | Boolean                                   |
| name                                        | String                                    |
| icon                                        | String                                    |
| category                                    | [NoteTypeCategories](#notetypecategories) |
| rank                                        | Integer                                   |
| is_default_appointment_type                 | Boolean                                   |
| is_scheduleable                             | Boolean                                   |
| is_telehealth                               | Boolean                                   |
| is_billable                                 | Boolean                                   |
| defer_place_of_service_to_practice_location | Boolean                                   |
| available_places_of_service                 | Array[[PracticeLocationPOS](#practicelocationpos)]                |
| default_place_of_service                    | [PracticeLocationPOS](#practicelocationpos)                       |
| is_system_managed                           | Boolean                                   |
| is_visible                                  | Boolean                                   |
| is_active                                   | Boolean                                   |
| unique_identifier                           | UUID                                      |
| deprecated_at                               | DateTime                                  |
| is_patient_required                         | Boolean                                   |
| allow_custom_title                          | Boolean                                   |

## Enumeration types

### NoteTypeCategories

| Value          | Description          |
|----------------|----------------------|
| message        | Message              |
| letter         | Letter               |
| inpatient      | Inpatient Visit Note |
| review         | Chart Review Note    |
| encounter      | Encounter Note       |
| appointment    | Appointment Note     |
| task           | Task                 |
| data           | Data                 |
| ccda           | C-CDA                |
| schedule_event | Schedule Event       |

### PracticeLocationPOS

| Value | Description                                              |
|-------|----------------------------------------------------------|
| 01    | Pharmacy                                                 |
| 02    | Telehealth                                               |
| 03    | Education Facility                                       |
| 04    | Homeless Shelter                                         |
| 09    | Prison                                                   |
| 10    | Telehealth in Patient's Home                             |
| 11    | Office                                                   |
| 12    | Home                                                     |
| 13    | Asssisted Living Facility                                |
| 14    | Group Home                                               |
| 15    | Mobile Unit                                              |
| 17    | Walk-In Retail Health Clinic                             |
| 19    | Off-Campus Outpatient Hospital                           |
| 20    | Urgent Care Facility                                     |
| 21    | Inpatient Hospital                                       |
| 22    | On-Campus Outpatient Hospital                            |
| 23    | Emergency Room Hospital                                  |
| 24    | Ambulatory Surgery Center                                |
| 25    | Birthing Center                                          |
| 26    | Military Treatment Facility                              |
| 27    | Outreach Site / Street                                   |
| 31    | Skilled Nursing Facility                                 |
| 32    | Nursing Facility                                         |
| 33    | Custodial Care Facility                                  |
| 34    | Hospice                                                  |
| 41    | Ambulance Land                                           |
| 42    | Ambulance Air or Water                                   |
| 49    | Independent Clinic                                       |
| 50    | Federally Qualified Health Center                        |
| 51    | Inpatient Psychiatric Facility                           |
| 52    | Inpatient Psychiatric Facility - Partial Hospitalization |
| 53    | Community Mental Health Center                           |
| 54    | Intermediate Care Facility for Mentally Retarded         |
| 55    | Residential Substance Abuse Treatment Facility           |
| 56    | Psychiatric Residential Treatment Center                 |
| 57    | Non-Residential Substance Abuse Treatment Facility       |
| 60    | Mass Immunization Center                                 |
| 61    | Inpatient Rehabilitation Facility                        |
| 62    | Outpatient Rehabilitation Facility                       |
| 65    | End-Stage Renal Disease Treatment Facility               |
| 71    | State or Local Public Health Clinic                      |
| 72    | Rural Health Clinic                                      |
| 81    | Independent Laboratory                                   |
| 99    | Other Place of Service                                   |
