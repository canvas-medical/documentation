---
title: "InpatientStay"
slug: "data-inpatient-stay"
excerpt: "Canvas SDK InpatientStay and InpatientFacility"
hidden: false
---

## Introduction

An `InpatientStay` records a patient's admission to an inpatient facility: the facility, the room, the medical record number (MRN) the facility assigned, and the admit and discharge times. The rounding notes written during the stay point to it through [Note](/sdk/data-note/#note)'s `inpatient_stay`, and the facility is an [InpatientFacility](#inpatientfacility).

## Basic usage

### Find a patient's inpatient stays

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")

stays = patient.inpatient_stays.order_by("-admit_time")
```

### Read a stay's facility and rounding notes

`inpatient_facility` can be `None`. `rounding_notes` returns the stay's notes in every state, deleted notes included, so exclude those by their [current state](/sdk/data-note/#currentnotestateevent):

```python
from canvas_sdk.v1.data import InpatientStay
from canvas_sdk.v1.data.note import NoteStates

stay = InpatientStay.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

facility_name = stay.inpatient_facility.name if stay.inpatient_facility else None

rounding_notes = stay.rounding_notes.exclude(current_state__state=NoteStates.DELETED)
```

To go the other way, read `inpatient_stay` on a note. It's `None` for a note that wasn't written during an inpatient stay.

## Filtering

### Stays still in progress

A stay that hasn't been discharged has no `discharge_time`:

```python
from canvas_sdk.v1.data import InpatientStay

current_stays = InpatientStay.objects.filter(
    patient__id="b80b1cdc2e6a4aca90ccebc02e683f35", discharge_time__isnull=True
)
```

### Stays at a facility

```python
from canvas_sdk.v1.data import InpatientFacility, InpatientStay

facility = InpatientFacility.objects.get(npi_number="1234567893")

stays = InpatientStay.objects.filter(inpatient_facility=facility)
```

## Attributes

### InpatientStay

| Field Name         | Type                                                 | Notes |
|--------------------|------------------------------------------------------|-------|
| id                 | UUID                                                 |       |
| dbid               | Integer                                              |       |
| patient            | [Patient](/sdk/data-patient/#patient)                |       |
| inpatient_facility | [InpatientFacility](#inpatientfacility)              | Null when no facility was recorded |
| room_number        | String                                               |       |
| external_mrn       | String                                               | The patient's MRN at the facility |
| referring_provider | String                                               | The referring provider's name, as entered |
| admit_time         | DateTime                                             |       |
| discharge_time     | DateTime                                             | Null until the patient is discharged |
| rounding_notes     | QuerySet[[Note](/sdk/data-note/#note)]               | Notes written during the stay, in every state |

### InpatientFacility

| Field Name      | Type                                  |
|-----------------|---------------------------------------|
| id              | UUID                                  |
| dbid            | Integer                               |
| name            | String                                |
| npi_number      | String                                |
| line1           | String                                |
| line2           | String                                |
| city            | String                                |
| state_code      | String                                |
| postal_code     | String                                |
| inpatient_stays | QuerySet[[InpatientStay](#inpatientstay)] |
