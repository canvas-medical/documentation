---
title: "ExternalEvent"
slug: "data-external-event"
excerpt: "Canvas SDK ExternalEvent"
hidden: false
---

## Introduction

The `ExternalEvent` and `ExternalVisit` models represent clinical events from external data sources such as ADT (Admission, Discharge, Transfer) feeds. These models enable tracking of patient encounters that occur outside of Canvas, such as hospital admissions, emergency room visits, or transfers between facilities.

An `ExternalVisit` groups related events for a single patient visit, while `ExternalEvent` represents individual events within that visit (e.g., admission, discharge, transfer).

## Basic usage

To get an external event by identifier, use the `get` method on the `ExternalEvent` model manager:

```python
from canvas_sdk.v1.data.external_event import ExternalEvent

event = ExternalEvent.objects.get(id="b4f8c3a1-2d5e-4f6a-8b9c-1a2b3c4d5e6f")
```

To get an external visit:

```python
from canvas_sdk.v1.data.external_event import ExternalVisit

visit = ExternalVisit.objects.get(id="a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d")
```

### Accessing related models

If you have an external event, you can access the associated visit and patient:

```python
from canvas_sdk.v1.data.external_event import ExternalEvent

event = ExternalEvent.objects.get(id="b4f8c3a1-2d5e-4f6a-8b9c-1a2b3c4d5e6f")

# Access the parent visit
visit = event.external_visit

# Access the patient
patient = event.patient
```

If you have an external visit, you can access all events within that visit:

```python
from canvas_sdk.v1.data.external_event import ExternalVisit

visit = ExternalVisit.objects.get(id="a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d")

# Get all events in this visit
events = visit.visit_events.all()
```

If you have a patient object, you can access their external events and visits:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")

# Get all external events for this patient
events = patient.patient_events.all()

# Get all external visits for this patient
visits = patient.patient_visits.all()
```

## Filtering

External events and visits can be filtered by any attribute that exists on the model.

### By patient

```python
from canvas_sdk.v1.data.external_event import ExternalEvent, ExternalVisit

# Get all events for a specific patient
events = ExternalEvent.objects.filter(patient__id="1eed3ea2a8d546a1b681a2a45de1d790")

# Get all visits for a specific patient
visits = ExternalVisit.objects.filter(patient__id="1eed3ea2a8d546a1b681a2a45de1d790")
```

### By event type

```python
from canvas_sdk.v1.data.external_event import ExternalEvent

# Get all admission events
admissions = ExternalEvent.objects.filter(event_type="ADT^A01")

# Get all discharge events
discharges = ExternalEvent.objects.filter(event_type="ADT^A03")
```

### By cancelled status

```python
from canvas_sdk.v1.data.external_event import ExternalEvent

# Get all non-cancelled events
active_events = ExternalEvent.objects.filter(event_cancelation_datetime__isnull=True)

# Get all cancelled events
cancelled_events = ExternalEvent.objects.filter(event_cancelation_datetime__isnull=False)
```

### By visit identifier

```python
from canvas_sdk.v1.data.external_event import ExternalVisit

visit = ExternalVisit.objects.get(visit_identifier="VISIT-12345")
```

### By facility

```python
from canvas_sdk.v1.data.external_event import ExternalVisit

visits = ExternalVisit.objects.filter(facility_name="General Hospital")
```

## Attributes

### ExternalEvent

| Field Name                   | Type                                        |
|------------------------------|---------------------------------------------|
| id                           | UUID                                        |
| dbid                         | Integer                                     |
| created                      | DateTime                                    |
| modified                     | DateTime                                    |
| external_visit               | [ExternalVisit](#externalvisit)             |
| patient                      | [Patient](/sdk/data-patient/#patient)       |
| message_control_id           | String                                      |
| message_datetime             | DateTime                                    |
| event_type                   | String                                      |
| event_datetime               | DateTime                                    |
| event_cancelation_datetime   | DateTime                                    |
| raw_message                  | String                                      |
| cancelled                    | Boolean (property)                          |

### ExternalVisit

| Field Name         | Type                                  |
|--------------------|---------------------------------------|
| id                 | UUID                                  |
| dbid               | Integer                               |
| created            | DateTime                              |
| modified           | DateTime                              |
| patient            | [Patient](/sdk/data-patient/#patient) |
| visit_identifier   | String                                |
| information_source | String                                |
| facility_name      | String                                |

## Common Event Types

External events typically use HL7 ADT event types:

| Event Type | Description                     |
|------------|---------------------------------|
| ADT^A01    | Admit/Visit Notification        |
| ADT^A02    | Transfer a Patient              |
| ADT^A03    | Discharge/End Visit             |
| ADT^A04    | Register a Patient              |
| ADT^A08    | Update Patient Information      |
| ADT^A11    | Cancel Admit/Visit Notification |
| ADT^A12    | Cancel Transfer                 |
| ADT^A13    | Cancel Discharge/End Visit      |

```python
from canvas_sdk.v1.data.external_event import ExternalEvent
from logger import log

# Get recent events for a patient and log their types
patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
events = ExternalEvent.objects.filter(patient__id=patient_id).order_by("-event_datetime")[:10]

for event in events:
    status = "CANCELLED" if event.cancelled else "ACTIVE"
    log.info(f"Event: {event.event_type} at {event.event_datetime} [{status}]")
```

<br/>
<br/>
<br/>