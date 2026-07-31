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
| `excluded_note_types`    | optional | list[str]         | A list of `NoteType.unique_identifier` values (UUIDs) to exclude from the patient's timeline. Defaults to `[]`. |
| `allowed_new_note_types` | optional | list[str] \| None | An allow-list of `NoteType.unique_identifier` values the **New Note** button may offer. `None` (the default) means no constraint; `[]` offers nothing, which hides the button. See [Restricting note creation](#restricting-note-creation). |

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

> 📘 Chart Review notes cannot be excluded
>
> Even if a `CHART_REVIEW` note type is included in the `excluded_note_types` list, it will always be shown on the timeline. The system automatically removes it from any exclusion list.

- **Permalink access**: If a user tries to directly access a note whose type has been excluded, they will receive a permission error.
- **Multiple plugins**: If multiple plugins respond to the `PATIENT_TIMELINE__GET_CONFIGURATION` event, the excluded note types from all responses are combined.
- **Note creation**: An excluded note type is also removed from the patient chart's **New Note** button and from the timeline's note type filter, so users cannot pick that type when creating a note. This governs what the UI offers — it does not reject a note of an excluded type created directly through the API.

> 📘 To restrict note creation without hiding existing notes
>
> `excluded_note_types` hides a patient's existing notes of that type *and* removes the type from the **New Note** button. If you only want to restrict what the button offers, while leaving the patient's history visible and filterable, use `allowed_new_note_types` instead.

## Restricting note creation

`allowed_new_note_types` is an **allow-list** of the note types the **New Note** button may offer. It affects note *creation* only: existing notes of a withheld type stay on the timeline, and the timeline's note type filter keeps offering that type, so a provider can still see and filter the history they are being stopped from adding to.

Inactive and deprecated note types are never offered, whether or not a plugin responds.

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

        note_types = NoteType.objects.filter(
            is_active=True, deprecated_at__isnull=True, name__in=allowed_names
        )

        return [
            PatientTimelineEffect(
                allowed_new_note_types=[str(nt.unique_identifier) for nt in note_types]
            ).apply()
        ]
```

To hide the button entirely, return an empty allow-list:

```python
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

> 🚧 This is a workflow guardrail, not an access control
>
> It governs what the **New Note** button offers. It does not reject a note of a restricted type created directly through the API. Do not rely on it to enforce access to sensitive note types — see [Note Restrictions](/sdk/effect-note-restrictions/) for controlling access to notes.

> 📘 Note type names are per-instance
>
> The names above are illustrative. Note types are configured per instance, so check what actually exists before matching on `name` — a name that does not exist simply matches nothing, silently shortening your allow-list. Matching on `unique_identifier` avoids this entirely.

For a full working implementation, see the [**new-note-type-restrictions**](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/new-note-type-restrictions) example plugin, which restricts by clinical role and reads its role mapping from a non-sensitive plugin variable rather than hard-coding it.

### Validation

- All provided UUIDs, in either attribute, must correspond to existing note types in the system. If a note type UUID does not exist, a `ValidationError` will be raised with a message indicating which note type was not found.
- Values that are not valid UUIDs will also raise a `ValidationError`.
