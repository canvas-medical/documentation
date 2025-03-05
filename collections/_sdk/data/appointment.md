---
title: "Appointment"
slug: "data-appointment"
excerpt: "Canvas SDK Appointment"
hidden: false
---

## Introduction

The `Appointment` model represents a single scheduled meeting from a patient, that may be in the future or past.

## Basic usage

To get an appointment by identifier, use the `get` method on the `Appointment` model manager:

```python
from canvas_sdk.v1.data.appointment import Appointment

appointment = Appointment.objects.get(id="f53626e4-0683-43ac-a1b7-c52815639ce2")
```

If you have a patient object, the appointments for a patient can be accessed with the `appointments` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
appointments = patient.appointments.all()
```

## Filtering

Appointments can be filtered by any attribute that exists on the model.

Filtering for appointments is done with the `filter` method on the `Appointment` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.appointment import Appointments , AppointmentProgressStatus

appointments = Appointment.objects.filter(status=AppointmentProgressStatus.CONFIRMED)
```

### Filtering by External Identifiers

To query Appointments by external identifiers, the `external_identifiers` relation can be used with double-underscores to identify values stored on the [AppointmentExternalIdentifier](#appointmentexternalidentifier) model. For example:

```python
from canvas_sdk.v1.data.appointment import Appointment

appointment = Appointment.objects.filter(
    external_identifiers__system="COMPANY_IDENTIFIER",
    external_identifiers__value="ejNoTa5vKzoT9oSjg87MVB").first()
```

## Attributes

### Appointment

| Field Name                   | Type                                                              |
|------------------------------|-------------------------------------------------------------------|
| id                           | UUID                                                              |
| dbid                         | Integer                                                           |
| entered_in_error             | CanvasUser                                                        |
| patient                      | [Patient](/sdk/data-patient/#patient)                             |
| appointment_rescheduled_from | [Appointment](#appointment)                                       |
| provider                     | [Staff](#/sdk/data-staff/#staff)                                  |
| start_time                   | DateTime                                                          |
| duration_minutes             | Integer                                                           |
| comment                      | String                                                            |
| note_id                      | Integer                                                           |
| note_type_id                 | Integer                                                           |
| status                       | String                                                            |
| status                       | String                                                            |
| meeting_link                 | URL                                                               |
| telehealth_instructions_sent | Boolean                                                           |
| location                     | [PracticeLocation](#/sdk/data-practicelocation/#practicelocation) |
| description                  | String                                                            |
| external_identifiers         | [AppointmentExternalIdentifier](#appointmentexternalidentifier)[] |


### AppointmentExternalIdentifier

| Field Name      | Type                        |
|-----------------|-----------------------------|
| id              | UUID                        |
| dbid            | Integer                     |
| created         | DateTime                    |
| modified        | DateTime                    |
| use             | String                      |
| identifier_type | String                      |
| system          | String                      |
| value           | String                      |
| issued_date     | Date                        |
| expiration_date | Date                        |
| appointment     | [Appointment](#appointment) |

<br/>
<br/>
<br/>
