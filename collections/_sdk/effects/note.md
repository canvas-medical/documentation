---
title: "Note Effects"
slug: "effect-notes"
excerpt: "Effects for creating notes, appointments, and schedule events."
hidden: false
---

# Note Effects

The Canvas SDK provides effects to facilitate creating, updating, and managing **visit notes**, **appointments**, and **schedule events**. Below you'll find detailed documentation for each effect type and their operations.

## Note Effect

The `Note` effect facilitates the creation and updating of visit notes for patients.

### Attributes

| Attribute              | Type                | Description                          | Required |
|------------------------|---------------------|--------------------------------------|----------|
| `note_type_id`         | `UUID` or `str`     | Identifier for the note type         | Yes      |
| `datetime_of_service`  | `datetime.datetime` | When the service was provided        | Yes      |
| `patient_id`           | `str`               | Identifier for the patient           | Yes      |
| `practice_location_id` | `UUID` or `str`     | Identifier for the practice location | Yes      |
| `provider_id`          | `str`               | Identifier for the provider          | Yes      |
| `title`                | `str` or `None`     | Optional title for the note          | No       |

### Implementation Details

- Validates that the note type exists and has an appropriate category
- Ensures the patient exists in the system
- Verifies that the practice location and provider are valid

### Example Usage

```python
import datetime

from canvas_sdk.effects.note.note import Note
from canvas_sdk.handlers.base import BaseHandler


class Protocol(BaseHandler):
    def compute(self):
        note_effect = Note(
            note_type_id="note-type-uuid",
            datetime_of_service=datetime.datetime.now(),
            patient_id="patient-uuid",
            practice_location_id="practice-location-uuid",
            provider_id="provider-uuid"
        )

        return [note_effect.create()]
```

### Update Note

Updates an existing note. Only certain fields can be modified after creation.

#### Attributes

| Attribute              | Type                | Description                          | Required | Updatable |
|------------------------|---------------------|--------------------------------------|----------|-----------|
| `instance_id`          | `UUID` or `str`     | Identifier of the note to update     | Yes      | No        |
| `title`                | `str` or `None`     | Updated title for the note           | No       | Yes       |
| `datetime_of_service`  | `datetime.datetime` | Updated service date/time            | No       | Yes       |
| `practice_location_id` | `UUID` or `str`     | Updated practice location            | No       | Yes       |
| `provider_id`          | `str`               | Updated provider                     | No       | Yes       |

**Note**: `patient_id` and `note_type_id` cannot be updated after creation.

#### Example Usage

```python
import datetime

from canvas_sdk.effects.note.note import Note
from canvas_sdk.handlers.base import BaseHandler


class Protocol(BaseHandler):
    def compute(self):
        note_effect = Note(instance_id="existing-note-uuid")
        note_effect.title = "Updated Consultation Notes"
        note_effect.datetime_of_service = datetime.datetime.now()

        return [note_effect.update()]
```

---

## ScheduleEvent Effect

The `ScheduleEvent` effect enables creating, updating, and deleting schedule events for providers, with optional patient association.

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
import datetime

from canvas_sdk.effects.note.appointment import ScheduleEvent
from canvas_sdk.handlers.base import BaseHandler


class Protocol(BaseHandler):
    def compute(self):
        schedule_event_effect = ScheduleEvent(
            note_type_id="schedule-event-note-type-uuid",
            patient_id="patient-uuid",  # Optional depending on note type
            description="Team meeting",  # Optional depending on note type
            start_time=datetime.datetime.now(),
            duration_minutes=30,
            practice_location_id="practice-location-uuid",
            provider_id="provider-uuid"
        )

        return [schedule_event_effect.create()]
```

### Update Schedule Event

Updates an existing schedule event by creating a new event and cancelling the original.

#### Attributes

| Attribute              | Type                                    | Description                          | Required |
|------------------------|-----------------------------------------|--------------------------------------|----------|
| `instance_id`          | `UUID` or `str`                         | Identifier of the event to update    | Yes      |
| `start_time`           | `datetime.datetime`                     | New start time                       | No       |
| `duration_minutes`     | `int`                                   | New duration in minutes              | No       |
| `description`          | `str` or `None`                         | Updated description                  | No       |
| `practice_location_id` | `UUID` or `str`                         | New practice location                | No       |
| `provider_id`          | `str`                                   | New provider                         | No       |
| `status`               | `AppointmentProgressStatus` or `None`   | Updated status                       | No       |

#### Example Usage

```python
import datetime

from canvas_sdk.effects.note.appointment import ScheduleEvent
from canvas_sdk.handlers.base import BaseHandler


class Protocol(BaseHandler):
    def compute(self):
        schedule_event_effect = ScheduleEvent(instance_id="existing-event-uuid")
        schedule_event_effect.start_time = datetime.datetime.now() + datetime.timedelta(days=1)
        schedule_event_effect.duration_minutes = 60
        schedule_event_effect.description = "Rescheduled team meeting"

        return [schedule_event_effect.update()]
```

### Delete Schedule Event

Marks a schedule event as cancelled.

#### Example Usage

```python
import datetime

from canvas_sdk.effects.note.appointment import ScheduleEvent
from canvas_sdk.handlers.base import BaseHandler


class Protocol(BaseHandler):
    def compute(self):
        schedule_event_effect = ScheduleEvent(instance_id="existing-event-uuid")

        return [schedule_event_effect.delete()]
```

---

## Appointment Effect

The `Appointment` effect facilitates creating, updating, and cancelling patient appointments with providers.

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
from canvas_sdk.effects.note.appointment import Appointment
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

### Update Appointment

Updates an existing appointment by creating a new appointment and cancelling the original. This maintains the appointment history and ensures proper tracking of rescheduled appointments.

#### Attributes

| Attribute                  | Type                                    | Description                          | Required |
|----------------------------|-----------------------------------------|--------------------------------------|----------|
| `instance_id`              | `UUID` or `str`                         | Identifier of appointment to update  | Yes      |
| `start_time`               | `datetime.datetime`                     | New start time                       | No       |
| `duration_minutes`         | `int`                                   | New duration in minutes              | No       |
| `meeting_link`             | `str` or `None`                         | Updated meeting link                 | No       |
| `practice_location_id`     | `UUID` or `str`                         | New practice location                | No       |
| `provider_id`              | `str`                                   | New provider                         | No       |
| `status`                   | `AppointmentProgressStatus` or `None`   | Updated status                       | No       |
| `external_identifiers`     | `list[AppointmentIdentifier]` or `None` | Updated external identifiers         | No       |

**Note**: `patient_id` cannot be updated after creation.

#### Example Usage

```python
from canvas_sdk.effects.note.appointment import Appointment

appointment_effect = Appointment(instance_id="existing-appointment-uuid")
appointment_effect.start_time = datetime.datetime.now() + datetime.timedelta(hours=2)
appointment_effect.duration_minutes = 45
appointment_effect.meeting_link = "https://new-meeting-link.com"

return appointment_effect.update()
```

### Cancel Appointment

Cancels an existing appointment and updates its status.

#### Example Usage

```python
from canvas_sdk.effects.note.appointment import Appointment

appointment_effect = Appointment(instance_id="existing-appointment-uuid")

return appointment_effect.cancel()
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
4. **Update Restrictions**: Certain fields cannot be modified after creation:
   - **Notes**: `patient_id` and `note_type_id` are immutable
   - **Appointments**: `patient_id` is immutable
   - **All Effects**: At least one field must be modified for an update operation to succeed
