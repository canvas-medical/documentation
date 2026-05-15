---
title: "Patient Timeline"
slug: "effect-patient-timeline"
excerpt: "Configure a patient's timeline by excluding specific note types."
hidden: false
---

The Canvas SDK allows you to configure a patient's timeline, such as hiding specific note types from view.

## Excluding Note Types

To exclude note types from a patient's timeline, import the `PatientTimelineEffect` class and create an instance of it. This effect is triggered in response to the `PATIENT_TIMELINE__GET_CONFIGURATION` event, which fires when a patient's timeline is loaded.

### Attributes

| Attribute             |          | Type           | Description                                                                                                      |
| --------------------- | -------- | -------------- | ---------------------------------------------------------------------------------------------------------------- |
| `excluded_note_types` | required | list[str]   | A list of `NoteType.unique_identifier` values (UUIDs) to exclude from the patient's timeline. |

### Example Usage

The `excluded_note_types` list must contain `unique_identifier` values from the `NoteType` model. Each `NoteType` has a `unique_identifier` (UUID) that you can look up by querying the model:

```python
from canvas_sdk.v1.data.note import NoteType

# Find the unique_identifier for a note type by name
note_type = NoteType.objects.get(name="Office visit")
note_type.unique_identifier  # e.g. UUID("a3b9c1d2-...")

# Or list all note types with their unique_identifiers
for nt in NoteType.objects.all():
    print(f"{nt.name}: {nt.unique_identifier}")
```

Then use those `unique_identifier` values in the effect:

```python
from canvas_sdk.effects.patient.timeline import PatientTimelineEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.note import NoteType


class MyHandler(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_TIMELINE__GET_CONFIGURATION)]

    def compute(self):
        # Use unique_identifier
        office_visit = NoteType.objects.get(name="Office visit", is_active=True)
        lab_visit = NoteType.objects.get(name="Lab visit", is_active=True)

        effect = PatientTimelineEffect(
            excluded_note_types=[
                str(office_visit.unique_identifier),
                str(lab_visit.unique_identifier),
            ]
        )

        return [effect.apply()]
```

### Behavior

> 📘 Chart Review notes cannot be excluded
>
> Even if a `CHART_REVIEW` note type is included in the `excluded_note_types` list, it will always be shown on the timeline. The system automatically removes it from any exclusion list.

- **Permalink access**: If a user tries to directly access a note whose type has been excluded, they will receive a permission error.
- **Multiple plugins**: If multiple plugins respond to the `PATIENT_TIMELINE__GET_CONFIGURATION` event, the excluded note types from all responses are combined.

### Validation

- All provided UUIDs must correspond to existing note types in the system. If a note type UUID does not exist, a `ValidationError` will be raised with a message indicating which note type was not found.
- Values that are not valid UUIDs will also raise a `ValidationError`.
