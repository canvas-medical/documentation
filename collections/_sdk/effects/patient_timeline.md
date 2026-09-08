---
title: "Patient Timeline"
slug: "effect-patient-timeline"
excerpt: "Configure which note types a patient's chart shows and offers."
hidden: false
---

The Canvas SDK allows you to configure which note types a patient's chart shows and which the **New Note** button offers.

Both are controlled by the `PatientTimelineEffect` class, returned in response to the `PATIENT_TIMELINE__GET_CONFIGURATION` event, which fires when a patient's chart is loaded.

## Excluding Note Types

### Attributes

| Attribute                |          | Type              | Description                                                                                                      |
| ------------------------ | -------- | ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| `excluded_note_types`    | optional | list[str]         | A list of [`NoteType.unique_identifier`](/sdk/data-note/#notetype) values (UUIDs) to exclude from the patient's timeline. Defaults to `[]`. |
| `allowed_new_note_types` | optional | list[str] \| None | An allow-list of [`NoteType.unique_identifier`](/sdk/data-note/#notetype) values the **New Note** button may offer. `None` (the default) means no constraint; `[]` offers nothing, which hides the button. See [Restricting note creation](#restricting-note-creation). |

The two attributes differ in scope, and you will usually want only one of them:

| | `excluded_note_types` | `allowed_new_note_types` |
| --- | --- | --- |
| direction | deny-list | allow-list |
| existing notes on the timeline | **hidden** | visible |
| timeline's note type filter | type removed | type still offered |
| **New Note** button | type removed | restricted to the list |
| direct permalink to such a note | permission error | unaffected |
| several plugins respond | **unioned** | **unioned** |

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

{% include alert.html type="info" content="<b>Chart Review notes cannot be excluded.</b> Even if a <code>CHART_REVIEW</code> note type is included in the <code>excluded_note_types</code> list, it will always be shown on the timeline. The system automatically removes it from any exclusion list." %}

- **Permalink access**: If a user tries to directly access a note whose type has been excluded, they will receive a permission error.
- **Multiple plugins**: If multiple plugins respond to the `PATIENT_TIMELINE__GET_CONFIGURATION` event, the excluded note types from all responses are combined.
- **Note creation**: An excluded note type is also removed from the patient chart's **New Note** button and from the timeline's note type filter, so users cannot pick that type when creating a note. This governs what the UI offers — it does not reject a note of an excluded type created directly through the API.

{% include alert.html type="info" content="<b>To restrict note creation without hiding existing notes:</b> <code>excluded_note_types</code> hides a patient's existing notes of that type <i>and</i> removes the type from the <b>New Note</b> button. If you only want to restrict what the button offers, while leaving the patient's history visible and filterable, use <code>allowed_new_note_types</code> instead." %}

## Restricting note creation

`allowed_new_note_types` is an **allow-list** of the note types the **New Note** button may offer. It affects note *creation* only: existing notes of a withheld type stay on the timeline, and the timeline's note type filter keeps offering that type, so a provider can still see and filter the history they are being stopped from adding to.

A common use is limiting which note types a given provider can originate. An organization might want only certain staff sending text messages to a patient, for example: the **New Note** button offers the Message type to those roles and withholds it from everyone else, while every provider can still read the messages already on the patient's chart and filter the timeline by them.

Inactive and deprecated note types are never offered, whether or not a plugin responds.

The example below allow-lists by the staff member's clinical role, so a nurse can send a message or log a phone call while only a physician is offered an office visit.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient.timeline import PatientTimelineEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.note import NoteType
from canvas_sdk.v1.data.staff import Staff

ALLOWED_BY_ROLE = {
    "MD": ["Office visit", "Phone call", "Message"],
    "RN": ["Phone call", "Message"],
}


class RestrictNewNoteTypes(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_TIMELINE__GET_CONFIGURATION)

    def compute(self) -> list[Effect]:
        staff = Staff.objects.filter(user__dbid=self.event.actor.id).first()
        role = staff.top_role_abbreviation if staff else None
        allowed_names = ALLOWED_BY_ROLE.get(role or "", ["Message"])

        note_types = NoteType.objects.filter(is_active=True, name__in=allowed_names)

        return [
            PatientTimelineEffect(
                allowed_new_note_types=[str(nt.unique_identifier) for nt in note_types]
            ).apply()
        ]
```

To hide the button entirely, return an empty allow-list:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient.timeline import PatientTimelineEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class HideNewNoteButton(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_TIMELINE__GET_CONFIGURATION)

    def compute(self) -> list[Effect]:
        return [PatientTimelineEffect(allowed_new_note_types=[]).apply()]
```

### Behavior

| What your plugin returns | Result |
| --- | --- |
| attribute omitted, or `None` | the full note type list, unchanged |
| `allowed_new_note_types=[...]` | only those note types are offered |
| `allowed_new_note_types=[]` | nothing is offered, so the **New Note** button is hidden entirely |

- **Multiple plugins**: allow-lists from all responses are combined, the same way exclusions are. Note the consequence: a second plugin returning an allow-list *widens* what a first one permits, so a restriction is only as tight as the most permissive plugin responding.
- **Combined with exclusions**: a note type excluded via `excluded_note_types` stays out of the button even if the allow-list names it. Exclusions win because they affect far more — the timeline, the note type filter and permalink access — so they are the safer outcome when a plugin names the same type in both.
- **Chart Review**: unlike exclusions, `CHART_REVIEW` is *not* force-allowed here. Force-allowing it would make "nothing available" unreachable and the button could never be hidden.
- **Plugin failures**: if the plugin runner cannot be reached, the note type list is left unconstrained rather than emptied.

{% include alert.html type="warning" content="<b>This is a workflow guardrail, not an access control.</b> It governs what the <b>New Note</b> button offers. It does not reject a note of a restricted type created directly through the API. Do not rely on it to enforce access to sensitive note types — see <a href='/sdk/effect-note-restrictions/'>Note Restrictions</a> for controlling access to notes." %}

{% include alert.html type="info" content="<b>Note types are configured per instance.</b> The names above are illustrative, so check what exists on your instance before matching on <code>name</code> — a name that does not exist simply matches nothing, silently shortening your allow-list. A <code>unique_identifier</code> is generated per instance too, so it cannot be hard-coded in a plugin meant to run on more than one; look the note types up at runtime and keep the mapping configurable. An identifier that does not exist raises a <code>ValidationError</code> rather than failing quietly." %}

### Validation

- All provided UUIDs, in either attribute, must correspond to existing [NoteType](/sdk/data-note/#notetype) records in the system. If a note type UUID does not exist, a `ValidationError` will be raised with a message indicating which note type was not found.
- Values that are not valid UUIDs will also raise a `ValidationError`.
