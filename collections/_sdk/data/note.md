---
title: "Note"
slug: "data-note"
excerpt: "Canvas SDK Note"
hidden: false
---

## Introduction

The `Note` model represents clinical notes that appear on a patient's chart. A `Note` can contain multiple [commands](/sdk/data-command).

## Basic usage

### Retrieve a specific note

To get a note by identifier, use the `get` method on the `Note` model manager:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
```

### Find all notes for a patient

If you have a patient object, the notes for a patient can be found using the `notes` attribute on the `Patient` instance:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="fd2ecd87c26044a6a755287f296dd17f")
patient_notes = patient.notes.all()
```

### Retrieve the content of commands in a note

If you have a note object, the [commands](/sdk/data-command) for that note can be found using the `commands` attribute on the `Note` instance:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
note_commands = note.commands.all()
```

You can also filter commands by their state or other attributes:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")

# Get only committed commands
committed_commands = note.commands.filter(state="committed")

# Get commands by schema_key (e.g., prescriptions)
prescriptions = note.commands.filter(schema_key="prescribe")
```

To access the content of a command, use the `data` attribute which contains a JSON object with the command's data:

```python
import json
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")

for command in note.commands.all():
    # Get the command type
    command_type = command.schema_key

    # Get the command data as a dictionary
    command_data = command.data

    # Pretty print the command data
    print(f"Command Type: {command_type}")
    print(json.dumps(command_data, indent=2))
```

For more information about command types and their data structure, see the [Command](/sdk/data-command/) documentation.

### Understanding the note body structure

The `body` field of a note contains a JSON array that represents the structure and layout of the note. It intermixes text content with references to commands:

```python
import json
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")

# The body is an array of objects
print(json.dumps(note.body, indent=2))
```

The body array contains objects of two types:

1. **Text objects**: Represent free-form text content
   ```json
   {"type": "text", "value": "Patient reports feeling better"}
   ```

2. **Command objects**: Reference commands with their metadata
   ```json
   {
     "type": "command",
     "value": "reasonForVisit",
     "data": {
       "id": 1095,
       "command_uuid": "691123c4-6c7d-415b-880b-2beefab9f64a"
     }
   }
   ```

The `command_uuid` in a command object corresponds to the `id` field of the [Command](/sdk/data-command/) model, allowing you to retrieve the full command data:

```python
from canvas_sdk.v1.data.note import Note
from canvas_sdk.v1.data.command import Command

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")

# Find all command references in the note body
for item in note.body:
    if item.get("type") == "command":
        command_uuid = item["data"]["command_uuid"]
        command = Command.objects.get(id=command_uuid)
        print(f"Command type: {command.schema_key}")
        print(f"Command data: {command.data}")
```

### Retrieve the audit history for a note

The audit history for a note can be found using the [`NoteStateChangeEvent`](/sdk/data-note/#notestatechangeevent)
model. You can access this model directly or through the `state_history`
relation on the note object.

```python
from canvas_sdk.v1.data.note import Note, NoteStateChangeEvent

note = Note.objects.first()

# Use the state_history relation
option_1 = note.state_history.all()

# Use the note object to filter the QuerySet
option_2 = NoteStateChangeEvent.objects.filter(note=note)

# Use the note's UUID to filter the QuerySet, which joins to the note table
# where the note's dbid column is equal to the note_id column of the note
# state change event and the note's id column is equal to the note's UUID.
option_3 = NoteStateChangeEvent.objects.filter(note__id=note.id)

# Use the note's auto-increment database id to filter the QuerySet by the
# foreign key column without joining to the notes table.
option_4 = NoteStateChangeEvent.objects.filter(note_id=note.dbid)
```

In the above code sample, options 1, 2, and 4 produce identical SQL queries.

### Determine if a note is locked

To see if a note is presently locked, you can use the [`CurrentNoteStateEvent`](/sdk/data-note/#currentnotestateevent)
model to check if the current note state is 'Locked'. (See:
[NoteState](/sdk/data-note/#notestates) for an explanation of the different
note states you might encounter)

```python
from canvas_sdk.v1.data.note import Note, CurrentNoteStateEvent, NoteStates

note = Note.objects.first()

# You can retrieve the CurrentNoteStateEvent record for the note and check its
# state attribute.
if CurrentNoteStateEvent.objects.get(note=note).state == NoteStates.LOCKED:
    # This note is locked!
    pass

# You can skip retrieving the record by just checking if a
# CurrentNoteStateEvent record exists for that note with the state 'Locked'.
if CurrentNoteStateEvent.objects.filter(note=note, state=NoteStates.LOCKED).exists():
    # This note is locked!
    pass
```

### Find all open notes

You can find all open notes by retrieving the note records with a current
state which indicates it can be edited. (See list below)

```python
from canvas_sdk.v1.data.note import Note, CurrentNoteStateEvent, NoteStates

open_note_states = [
    NoteStates.NEW,
    NoteStates.PUSHED,
    NoteStates.CONVERTED,
    NoteStates.UNLOCKED,
    NoteStates.RESTORED,
    NoteStates.UNDELETED,
]

# This will execute one query per CurrentNoteStateEvent object returned
open_notes_via_list_comprehension = [event.note for event in CurrentNoteStateEvent.objects.filter(state__in=open_note_states)]

# This will always execute two queries: one to find the note ids of open
# notes, and a second query to fetch the note records by the ids returned in the
# first query
open_note_ids = CurrentNoteStateEvent.objects.filter(state__in=open_note_states).values_list('note_id', flat=True)
open_notes_via_multiple_queries = Note.objects.filter(dbid__in=open_note_ids)
```

### Get the current state of a given note

To get a note's current state, retrieve its
[`CurrentNoteStateEvent`](/sdk/data-note/#currentnotestateevent) and check the
`state` attribute. If you are trying to assess if the current note state represents
that note as being editable, you can call the `editable()` method on the
`CurrentNoteStateEvent` object.

```python
from canvas_sdk.v1.data.note import Note, CurrentNoteStateEvent

note = Note.objects.first()

current_note_state = CurrentNoteStateEvent.objects.get(note=note).state
is_editable = current_note_state.editable()
```

### Get the current claim of a given note

You can retrieve the current claim using the method `get_claim()` presented in the Note object.

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.first()
claim = note.get_claim()

```

### Get the NoteType of a given note

To get the note type for a specific note, use the `note_type_version` attribute which provides access to the related `NoteType` object:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")

# Get the note type name (e.g., "Office Visit")
note_type_name = note.note_type_version.name

# Access other note type attributes
note_type_display = note.note_type_version.display
note_type_code = note.note_type_version.code
note_type_system = note.note_type_version.system
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
from canvas_sdk.v1.data.note import Note
from canvas_sdk.v1.data.note import NoteType
from canvas_sdk.v1.data.patient import Patient

note_type = NoteType.objects.get(name="Office visit")
patient = Patient.objects.get(id="fd2ecd87c26044a6a755287f296dd17f")
patient_office_visits = Note.objects.filter(patient=patient, note_type_version=note_type)
```

## Attributes

### Note

| Field Name          | Type                                   | Notes                                                                                                                                                                                                |
|---------------------|----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id                  | UUID                                   |                                                                                                                                                                                                      |
| dbid                | Integer                                |                                                                                                                                                                                                      |
| created             | DateTime                               |                                                                                                                                                                                                      |
| modified            | DateTime                               |                                                                                                                                                                                                      |
| patient             | [Patient](/sdk/data-patient/#patient)  |                                                                                                                                                                                                      |
| note_type_version   | [NoteType](#notetype)                  |                                                                                                                                                                                                      |
| title               | String                                 |                                                                                                                                                                                                      |
| body                | JSON                                   | Array of objects representing the note structure. Each object has a `type` (either `"text"` or `"command"`) and a `value`. Command objects also include a `data` field with `id` and `command_uuid`. |
| originator          | [CanvasUser](/sdk/data-canvasuser)     |                                                                                                                                                                                                      |
| provider            | [Staff](/sdk/data-staff/#staff)        |                                                                                                                                                                                                      |
| checksum            | String                                 |                                                                                                                                                                                                      |
| billing_note        | String                                 |                                                                                                                                                                                                      |
| related_data        | JSON                                   | Can contain one key, `roomNumber`, if the Note is an inpatient stay.                                                                                                                                 |
| datetime_of_service | DateTime                               |                                                                                                                                                                                                      |
| place_of_service    | String                                 |                                                                                                                                                                                                      |
| encounter           | [Encounter](/sdk/data-encounter)       |                                                                                                                                                                                                      |
| commands            | QuerySet[[Command](/sdk/data-command)] | All commands associated with this note                                                                                                                                                               |
| note_tasks          | QuerySet[[NoteTask](/sdk/data-task)]   | All tasks associated with this note                                                                                                                                                                  |
| metadata            | QuerySet[[NoteMetadata](#notemetadata)] | All metadata key-value pairs associated with this note                                                                                                                                              |

### NoteType

| Field Name                                  | Type                                               |
| ------------------------------------------- | -------------------------------------------------- |
| dbid                                        | Integer                                            |
| created                                     | DateTime                                           |
| modified                                    | DateTime                                           |
| system                                      | String                                             |
| version                                     | String                                             |
| code                                        | String                                             |
| display                                     | String                                             |
| user_selected                               | Boolean                                            |
| name                                        | String                                             |
| icon                                        | String                                             |
| category                                    | [NoteTypeCategories](#notetypecategories)          |
| rank                                        | Integer                                            |
| is_default_appointment_type                 | Boolean                                            |
| is_scheduleable                             | Boolean                                            |
| is_telehealth                               | Boolean                                            |
| is_billable                                 | Boolean                                            |
| defer_place_of_service_to_practice_location | Boolean                                            |
| available_places_of_service                 | Array[[PracticeLocationPOS](#practicelocationpos)] |
| default_place_of_service                    | [PracticeLocationPOS](#practicelocationpos)        |
| is_system_managed                           | Boolean                                            |
| is_visible                                  | Boolean                                            |
| is_active                                   | Boolean                                            |
| unique_identifier                           | UUID                                               |
| deprecated_at                               | DateTime                                           |
| is_patient_required                         | Boolean                                            |
| allow_custom_title                          | Boolean                                            |

### NoteMetadata

| Field Name | Type              |
|------------|-------------------|
| id         | UUID              |
| dbid       | Integer           |
| note       | [Note](#note)     |
| key        | String            |
| value      | String            |

```python
from canvas_sdk.v1.data.note import Note
from logger import log

note_id = "89992c23-c298-4118-864a-26cb3e1ae822"
note = Note.objects.get(id=note_id)
note_metadata = note.metadata.all()

for metadata in note_metadata:
   log.info(f"Note metadata: {metadata.key}, {metadata.value}")
```

### NoteStateChangeEvent

| Field Name          | Type                                    |
| ------------------- | --------------------------------------- |
| id                  | UUID                                    |
| dbid                | Integer                                 |
| created             | DateTime                                |
| modified            | DateTime                                |
| note                | [Note](/sdk/data-note/)                 |
| originator          | [CanvasUser](/sdk/data-canvasuser)      |
| state               | [NoteState](/sdk/data-note/#notestates) |
| note_state_document | String                                  |
| note_state_html     | String                                  |

### CurrentNoteStateEvent

| Field Name | Type                                    |
| ---------- | --------------------------------------- |
| id         | UUID                                    |
| dbid       | Integer                                 |
| state      | [NoteState](/sdk/data-note/#notestates) |
| note       | [Note](/sdk/data-note/)                 |

## Enumeration types

### NoteStates

| Value | Description            | Notes                      |
| ----- | ---------------------- | -------------------------- |
| NEW   | Created                |                            |
| PSH   | Pushed the charges for |                            |
| LKD   | Locked                 |                            |
| ULK   | Unlocked               |                            |
| DLT   | Deleted                |                            |
| RLK   | Relocked               |                            |
| RST   | Restored               |                            |
| RCL   | Recalled               |                            |
| UND   | Undeleted              |                            |
| DSC   | Discharged             |                            |
| SCH   | Scheduling             | Used in appointment notes  |
| BKD   | Booked                 | Used in appointment notes  |
| CVD   | Converted              | Used in appointment notes  |
| CLD   | Canceled               | Used in appointment notes  |
| NSW   | No show                | Used in appointment notes  |
| RVT   | Reverted               | Used in appointment notes  |
| CNF   | Confirmed              | Used for CCDA import notes |

### NoteTypeCategories

| Value          | Description          |
| -------------- | -------------------- |
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
| ----- | -------------------------------------------------------- |
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
