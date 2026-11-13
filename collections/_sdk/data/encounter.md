---
title: "Encounter"
slug: "data-encounter"
excerpt: "Canvas SDK Encounter"
hidden: false
---

## Introduction

The `Encounter` model represents a patient encounter connected to a Note in Canvas.

## Basic usage

To get an encounter by identifier, use the `get` method on the `Encounter` model manager:

```python
from canvas_sdk.v1.data import Encounter

encounter = Encounter.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

To get an encounter from a note, use the `encounter` attribute on the `Note` object:

```python
from canvas_sdk.v1.data import Note

note = Note.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
encounter = note.encounter
```

Keep in mind that not all notes have an associated encounter, so sometimes `note.encounter` will be `None`.

Similary, you can get a note from an `Encounter` object by using the `note` attribute:

```python
from canvas_sdk.v1.data import Encounter

encounter = Encounter.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
note = encounter.note
```

All encounters will have an associated note, which means `encounter.note` will never be `None`.

## Encounters and appointments

An [Appointment](/sdk/data-appointment/) has no direct link to an encounter. It reaches its encounter through its note: an appointment's encounter is the encounter whose note is the appointment's note.

```python
from canvas_sdk.v1.data import Appointment, Encounter

appointment = Appointment.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
encounter = None
if appointment.note:
    encounter = Encounter.objects.filter(note=appointment.note).first()
```

In SQL against the read replica, join on the note, not on the appointment's own id:

```sql
SELECT a.id AS appointment_id, e.id AS encounter_id, e.state
FROM canvas_sdk_data_api_appointment_001 a
LEFT JOIN canvas_sdk_data_api_encounter_001 e ON e.note_id = a.note_id;
```

How encounters are created for appointments:

- When an appointment is created with a note, Canvas creates a `PLANNED` encounter on that note with an empty `start_time`, or resets the note's existing encounter to `PLANNED` with an empty `start_time`.
- When an appointment is checked in, Canvas creates an encounter on its note if the note doesn't have one yet.
- An appointment with no note, such as a schedule event created without one, has no encounter.
- A rescheduled appointment points to the same note as the appointment it replaced, so several appointment rows can match one encounter.
- Cancelling an appointment or marking it a no-show doesn't remove its encounter.

Because the planned encounter is created when the appointment is first saved, an appointment whose note was attached later, or that was loaded without going through the normal appointment save, can have a note but no encounter until it is checked in. Treat the encounter as optional when reading appointments, and handle a missing one rather than assuming every appointment note has an encounter.

## Filtering

Encounters can be filtered by any attribute that exists on the model.

Filtering for encounters is done with the `filter` method on the `Encounter` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.encounter import Encounter, EncounterState

encounters = Encounter.objects.filter(state=EncounterState.CONCLUDED)
```

## Attributes

### Encounter

| Field Name | Type                                |
| ---------- | ----------------------------------- |
| id         | UUID                                |
| dbid       | Integer                             |
| created    | DateTime                            |
| modified   | DateTime                            |
| note       | [Note](/sdk/data-note/)             |
| state      | [EncounterState](#encounterstate)   |
| medium     | [EncounterMedium](#encountermedium) |
| start_time | DateTime                            |
| end_time   | DateTime                            |
| document_references | QuerySet[[DocumentReference](/sdk/data-document-reference/#documentreference)] |

## Enumeration types

### EncounterState

| Name      | Value |
| --------- | ----- |
| STARTED   | STA   |
| PLANNED   | PLA   |
| CONCLUDED | CON   |
| CANCELLED | CAN   |

### EncounterMedium

| Name    | Value   |
| ------- | ------- |
| VOICE   | voice   |
| VIDEO   | video   |
| OFFICE  | office  |
| HOME    | home    |
| OFFSITE | offsite |
| LAB     | lab     |

<br/>
<br/>
<br/>
