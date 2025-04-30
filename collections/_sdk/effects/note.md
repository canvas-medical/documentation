---
title: "Note Effects"
slug: "effect-notes"
excerpt: "Effects for creating notes, appointments, and schedule events."
hidden: false
---

# Note Effects

The Canvas SDK provides effects to facilitate creating **visit notes**, **appointments**, and **schedule events**. Below you'll find detailed documentation for each effect type.

## Note Effect

The `Note` effect facilitates the creation of visit notes for patients.

### Attributes

| Attribute              | Type                | Description                          | Required |
|------------------------|---------------------|--------------------------------------|----------|
| `note_type_id`         | `UUID` or `str`     | Identifier for the note type         | Yes      |
| `datetime_of_service`  | `datetime.datetime` | When the service was provided        | Yes      |
| `patient_id`           | `str`               | Identifier for the patient           | Yes      |
| `practice_location_id` | `UUID` or `str`     | Identifier for the practice location | Yes      |
| `provider_id`          | `str`               | Identifier for the provider          | Yes      |

### Implementation Details

- Validates that the note type exists and has an appropriate category
- Ensures the patient exists in the system
- Verifies that the practice location and provider are valid

### Example Usage

```python
from canvas_sdk.effects.note.note import Note
import datetime

note_effect = Note(
    note_type_id="note-type-uuid",
    datetime_of_service=datetime.datetime.now(),
    patient_id="patient-uuid",
    practice_location_id="practice-location-uuid",
    provider_id="provider-uuid"
)

return note_effect.create()
```

---

## ScheduleEvent Effect

The `ScheduleEvent` effect enables creating schedule events for providers, with optional patient association.

### Attributes

| Attribute              | Type                                    | Description                                                         | Required    |
|------------------------|-----------------------------------------|---------------------------------------------------------------------|-------------|
| `note_type_id`         | `UUID` or `str`                         | Identifier for the note type (must be of category `SCHEDULE_EVENT`) | Yes         |
| `patient_id`           | `str` or `None`                         | Identifier for the patient (if applicable)                          | Conditional |
| `description`          | `str` or `None`                         | Custom description for the event                                    | Conditional |
| `start_time`           | `datetime.datetime`                     | Start time of the event                                             | Yes         |
| `duration_minutes`     | `int`                                   | Duration of the event in minutes                                    | Yes         |
| `practice_location_id` | `UUID` or `str`                         | Identifier for the practice location                                | Yes         |
| `provider_id`          | `str`                                   | Identifier for the provider                                         | Yes         |
| `status`               | `AppointmentProgressStatus` or `None`   | Status of the event                                                 | No          |
| `external_identifiers` | `list[AppointmentIdentifier]` or `None` | External system identifiers                                         | No          |

### Implementation Details

- Validates that the note type exists and is of category `SCHEDULE_EVENT`
- Ensures patient is provided if the note type requires it
- Verifies that custom descriptions are only used for note types that allow them
- Validates that the practice location and provider exist

### Example Usage

```python
from canvas_sdk.effects.note.create_appointment import ScheduleEvent
import datetime

schedule_event_effect = ScheduleEvent(
    note_type_id="schedule-event-note-type-uuid",
    patient_id="patient-uuid",  # Optional depending on note type
    description="Team meeting",  # Optional depending on note type
    start_time=datetime.datetime.now(),
    duration_minutes=30,
    practice_location_id="practice-location-uuid",
    provider_id="provider-uuid"
)

return schedule_event_effect.create()
```

---

## Appointment Effect

The `Appointment` effect facilitates creating patient appointments with providers.

### Attributes

| Attribute                  | Type                                    | Description                                                                                 | Required |
|----------------------------|-----------------------------------------|---------------------------------------------------------------------------------------------|----------|
| `appointment_note_type_id` | `UUID` or `str`                         | Identifier for the appointment note type (must be of category `ENCOUNTER` and scheduleable) | Yes      |
| `patient_id`               | `str`                                   | Identifier for the patient                                                                  | Yes      |
| `meeting_link`             | `str` or `None`                         | Link for virtual appointments                                                               | No       |
| `start_time`               | `datetime.datetime`                     | Start time of the appointment                                                               | Yes      |
| `duration_minutes`         | `int`                                   | Duration of the appointment in minutes                                                      | Yes      |
| `practice_location_id`     | `UUID` or `str`                         | Identifier for the practice location                                                        | Yes      |
| `provider_id`              | `str`                                   | Identifier for the provider                                                                 | Yes      |
| `status`                   | `AppointmentProgressStatus` or `None`   | Status of the appointment                                                                   | No       |
| `external_identifiers`     | `list[AppointmentIdentifier]` or `None` | External system identifiers                                                                 | No       |

### Implementation Details

- Validates that the appointment note type exists, is of category `ENCOUNTER`, and is scheduleable
- Ensures the patient exists in the system
- Verifies that the practice location and provider exist

### Example Usage

```python
from canvas_sdk.effects.note.create_appointment import Appointment
import datetime

appointment_effect = Appointment(
    appointment_note_type_id="appointment-note-type-uuid",
    patient_id="patient-uuid",
    meeting_link="https://zoom.us/example-link",  # Optional
    start_time=datetime.datetime.now(),
    duration_minutes=60,
    practice_location_id="practice-location-uuid",
    provider_id="provider-uuid"
)

return appointment_effect.create()
```

---

## Validation

All effects perform comprehensive validation before execution:

1. **Entity Existence**: Validates that referenced entities (patients, providers, practice locations, note types) exist in the system
2. **Type Compatibility**: Ensures note types are appropriate for the intended operation:
   - Visit notes cannot use `APPOINTMENT`, `SCHEDULE_EVENT`, `MESSAGE`, or `LETTER` note types
   - Schedule events must use `SCHEDULE_EVENT` note types
   - Appointments must use `ENCOUNTER` note types that are scheduleable
3. **Field Requirement Enforcement**: The system validates conditional field requirements based on note type configurations:
   - **Patient Association Requirements**: For note types with `is_patient_required=True`, the system enforces that a valid patient ID is provided. This is particularly important for schedule events that may or may not be associated with specific patients.
   - **Custom Description Validation**: When a note type has `allow_custom_title=False`, the system prevents custom descriptions from being added. This ensures adherence to standardized naming conventions for certain types of appointments and events.
   - **Required Field Validation**: All required fields are checked for proper values and formats before the effect is executed.
