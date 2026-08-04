---
title: "Patient Portal"
slug: "patient-portal"
excerpt: "Patient portal configuration"
hidden: false
---

The Canvas SDK allows you to configure and extend the patient portal. This page is the technical reference for the portal's effects and events. For a decision-oriented overview of how much of the patient experience to build, see [Choosing Your Patient Experience](/guides/choosing-your-patient-experience/).

## Configure Portal Menu Items

Decide which items appear in the patient portal's menu with the `PatientPortalMenuConfiguration` effect, returned from a handler on the `PATIENT_PORTAL__MENU_CONFIGURATION` event. Unlike the account-wide page toggles managed by Canvas Support, this lets you show or hide menu items with your own logic (per patient, program, and so on).

The list you return **replaces** the built-in menu — include every built-in item you want shown, in the order you want them to appear (**the list order is the navigation order**), and omit any you want hidden.

An item only appears if its page is **also enabled in your portal settings** (the `PATIENT_APP_*` settings managed by Canvas Support — see [Managing the Patient Portal](https://canvas-medical.help.usepylon.com/articles/7348270931-managing-the-patient-portal)). This effect selects and orders among the *enabled* pages: it can hide or reorder them, but it can't surface a page that's turned off. Patient-portal [applications](/sdk/handlers-applications/) aren't part of this list — they're appended to the navigation after the built-in items through their own registration.

| Attribute | Type              | Description                                    |
|-----------|-------------------|------------------------------------------------|
| `items`   | list[`MenuItems`] | The built-in menu items to show, in navigation order (at least one). Replaces the default set — omit an item to hide it. |

**`MenuItems`** values:

| Member         | Value            | Menu item        |
|----------------|------------------|------------------|
| `APPOINTMENTS` | `"appointments"` | Appointments     |
| `MESSAGING`    | `"messaging"`    | Messaging        |
| `MY_HEALTH`    | `"my_health"`    | My Health        |
| `PAYMENTS`     | `"payments"`     | Payments         |
| `LABS`         | `"labs"`         | Lab results      |
| `CONTACT`      | `"contact"`      | Contact          |
| `RECORDS`      | `"records"`      | Health Records   |

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_portal_menu_configuration import PatientPortalMenuConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__MENU_CONFIGURATION)

    def compute(self) -> list[Effect]:
        return [
            PatientPortalMenuConfiguration(
                items=[
                    PatientPortalMenuConfiguration.MenuItems.APPOINTMENTS,
                    PatientPortalMenuConfiguration.MenuItems.MESSAGING,
                ]
            ).apply()
        ]
```

## Portal Landing Page Widgets

The `PortalWidget` class adds widgets to the patient portal landing page. Return `PortalWidget` effects from a handler on the `PATIENT_PORTAL__WIDGET_CONFIGURATION` event. You can fully customize a widget or use a ready-made one provided by Canvas (Appointments, Messaging).

The `PortalWidget` class has the following attributes:

| Attribute   | Type        | Description                                                                                                                            |
|-------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `url`       | `str`       | A URL to load within the widget.                                                                                                       |
| `content`   | `str`       | Content to display directly within the widget.                                                                                         |
| `component` | `Component` | A ready-made Canvas widget: `APPOINTMENTS` (upcoming appointments) or `MESSAGING` (quick messaging).                                    |
| `size`      | `Size`      | Widget width on the grid: `EXPANDED` (12 columns), `MEDIUM` (8 columns), or `COMPACT` (4 columns). All are 300px tall. Defaults to `EXPANDED`. |
| `priority`  | `int`       | Orders widgets within the portal; a lower number is higher priority. Defaults to `100`.                                                |

**Validation:** exactly one of `url`, `content`, or `component` must be set — providing more than one, or none, raises an error.

### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.widgets import PortalWidget
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__WIDGET_CONFIGURATION)

    def compute(self) -> list[Effect]:
        return [
            PortalWidget(
                url="https://example.com/info",
                size=PortalWidget.Size.COMPACT,
                priority=25,
            ).apply()
        ]
```

For a full walkthrough with examples, see the [Custom Landing Page guide](/guides/custom-landing-page/). Example plugins: [patient_portal_plugin](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_portal_plugin), and the MSF [urgent-care-self-scheduler](https://github.com/medical-software-foundation/canvas/tree/main/extensions/urgent-care-self-scheduler) (a "Need to be seen today?" widget).

## Customize Appointment Cards

Customize your patient appointment cards so patients can easily join their telehealth appointments, cancel or reschedule appointments.
Each appointment can be customized individually, allowing each one to have its own unique settings.

Each action is decided per appointment: Canvas fires a `PATIENT_PORTAL__APPOINTMENT_CAN_*` event for the appointment, and your handler returns the matching `PATIENT_PORTAL__APPOINTMENT_IS_*` (or `PATIENT_PORTAL__APPOINTMENT_SHOW_MEETING_LINK`) effect with a `{"result": <bool>}` payload — `False` hides the action; for the telehealth **Join** link, `True` shows it. Each action's exact event, effect, and payload are shown below.

MSF example: [portal_disable_cancel_appts](https://github.com/medical-software-foundation/canvas/tree/main/extensions/portal_disable_cancel_appts) hides the Cancel action.

### Hide 'Cancel' button

Respond to `PATIENT_PORTAL__APPOINTMENT_CAN_BE_CANCELED` and return a `PATIENT_PORTAL__APPOINTMENT_IS_CANCELABLE` effect with `{"result": False}` to hide the Cancel button.

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__APPOINTMENT_CAN_BE_CANCELED)


    def compute(self) -> list[Effect]:
        return [
          Effect(
            type=EffectType.PATIENT_PORTAL__APPOINTMENT_IS_CANCELABLE,
            payload=json.dumps({"result": False}))
        ]

```

### Hide 'Reschedule' button

Respond to `PATIENT_PORTAL__APPOINTMENT_CAN_BE_RESCHEDULED` and return a `PATIENT_PORTAL__APPOINTMENT_IS_RESCHEDULABLE` effect with `{"result": False}` to hide the Reschedule button.

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__APPOINTMENT_CAN_BE_RESCHEDULED)


    def compute(self) -> list[Effect]:
        return [
          Effect(
            type=EffectType.PATIENT_PORTAL__APPOINTMENT_IS_RESCHEDULABLE,
            payload=json.dumps({"result": False}))
        ]

```

### Hide 'Join' button

This button shows on telehealth appointments. Respond to `PATIENT_PORTAL__APPOINTMENT_CAN_SHOW_MEETING_LINK` and return a `PATIENT_PORTAL__APPOINTMENT_SHOW_MEETING_LINK` effect with `{"result": True}` to show the join link.

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__APPOINTMENT_CAN_SHOW_MEETING_LINK)


    def compute(self) -> list[Effect]:
        return [
          Effect(
            type=EffectType.PATIENT_PORTAL__APPOINTMENT_SHOW_MEETING_LINK,
            payload=json.dumps({"result": True}))
        ]
```

## Configuring the Patient Portal

Return a `PatientPortalApplicationConfiguration` effect from a handler on the `PATIENT_PORTAL__GET_APPLICATION_CONFIGURATION` event to set application-level portal options. Today this controls whether the self-scheduling entry points appear; pair it with [Shape Self-Scheduling](#shape-self-scheduling) to control *what* patients can book.

| Attribute                 | Type | Description                                                  |
|---------------------------|------|--------------------------------------------------------------|
| can_schedule_appointments | bool | If the patient is allowed to book or reschedule appointments |


```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_portal.application_configuration import PatientPortalApplicationConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__GET_APPLICATION_CONFIGURATION)


    def compute(self) -> list[Effect]:
        return [
          PatientPortalApplicationConfiguration(
            can_schedule_appointments=True
          ).apply()
        ]

```

## Shape Self-Scheduling

When patients self-schedule, you can filter or reorder what they're offered *before they see it* — the open time slots, and the appointment-type, location, and provider options on the scheduling form. Each search step fires a `…PRE_SEARCH` event (before Canvas runs the search) and a `…POST_SEARCH` event (with the results). Respond to the `POST_SEARCH` event and return an effect **of the same name with a `_RESULTS` suffix**, carrying the results you want the patient to see. (A `…PRE_SEARCH` event is available for each step too, if you need to act before the search runs.)

Two example plugins put these together: [patient_portal_search_appointments_slots_plugin](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_portal_search_appointments_slots_plugin) (slots) and [patient_app_schedule](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_app_schedule) (appointment types, locations, and providers).

### Filter available slots

Respond to `PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH` and return `PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH_RESULTS`.

**Target:** `self.target` is the [Patient](/sdk/data-patient/#patient) id.

**Context:** `self.context["slots_by_provider"]` — a JSON string of `{provider: {date: [{"start", "end"}, ...]}}`, keyed by [Staff](/sdk/data-staff/#staff) id, where each `start`/`end` is an ISO-8601 datetime.

Example — enforce a 48-hour minimum lead time so patients can't self-book last minute:

```python
import json

import arrow

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler

# Patients must book at least this far ahead — no last-minute self-scheduling
MIN_LEAD_TIME_HOURS = 48


class SlotFilter(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH)

    def compute(self) -> list[Effect]:
        # slots_by_provider maps each provider to {date: [{"start": ..., "end": ...}, ...]}
        slots_by_provider = json.loads(self.context.get("slots_by_provider") or "{}")
        cutoff = arrow.now().shift(hours=MIN_LEAD_TIME_HOURS)

        filtered = {}
        for provider, dates in slots_by_provider.items():
            # drop any slot starting before the cutoff
            kept = {
                date: [slot for slot in slots if arrow.get(slot["start"]) >= cutoff]
                for date, slots in dates.items()
            }
            # then drop empty dates, and providers left with no slots
            kept = {date: slots for date, slots in kept.items() if slots}
            if kept:
                filtered[provider] = kept

        return [
            Effect(
                type=EffectType.PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH_RESULTS,
                payload=json.dumps({"slots_by_provider": filtered}),
            )
        ]
```

### Filter appointment types

Respond to `PATIENT_PORTAL__APPOINTMENTS__FORM_APPOINTMENT_TYPES__POST_SEARCH` and return `PATIENT_PORTAL__APPOINTMENTS__FORM_APPOINTMENT_TYPES__POST_SEARCH_RESULTS`.

**Target:** `self.target` is the [Patient](/sdk/data-patient/#patient) id.

**Context:** `self.context["appointment_types"]` — a list of `{"id", "title"}` entries, where `id` is a [NoteType](/sdk/data-note/#notetype) id (its `unique_identifier`) and `title` is the note type's name.

Example — only let patients self-book a specific set of visit types (e.g. keep follow-ups and telehealth, hide new-patient intakes):

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler

# Visit types patients are allowed to self-book
PATIENT_BOOKABLE_TYPES = {"Follow-up", "Telehealth visit"}


class AppointmentTypeFilter(BaseHandler):
    RESPONDS_TO = EventType.Name(
        EventType.PATIENT_PORTAL__APPOINTMENTS__FORM_APPOINTMENT_TYPES__POST_SEARCH
    )

    def compute(self) -> list[Effect]:
        # each entry is {"id": ..., "title": ...}
        appointment_types = self.context.get("appointment_types", [])
        filtered = [t for t in appointment_types if t["title"] in PATIENT_BOOKABLE_TYPES]
        return [
            Effect(
                type=EffectType.PATIENT_PORTAL__APPOINTMENTS__FORM_APPOINTMENT_TYPES__POST_SEARCH_RESULTS,
                payload=json.dumps({"appointment_types": filtered}),
            )
        ]
```

### Filter locations

Respond to `PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH` and return `PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH_RESULTS`.

**Target:** `self.target` is the [Patient](/sdk/data-patient/#patient) id.

**Context:** `self.context["locations"]` — a list of `{"id", "title"}` entries, where `id` is a [PracticeLocation](/sdk/data-practicelocation/#practicelocation) id and `title` is its full name.

Example — only show locations where the patient has been seen before:

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Appointment


class LocationFilter(BaseHandler):
    RESPONDS_TO = EventType.Name(
        EventType.PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH
    )

    def compute(self) -> list[Effect]:
        locations = self.context.get("locations", [])
        seen_location_ids = {
            str(loc_id)
            for loc_id in Appointment.objects.filter(patient__id=self.target)
            .exclude(location__isnull=True)
            .values_list("location__id", flat=True)
        }
        filtered = [loc for loc in locations if loc["id"] in seen_location_ids]
        return [
            Effect(
                type=EffectType.PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH_RESULTS,
                payload=json.dumps({"locations": filtered}),
            )
        ]
```

### Filter providers

Respond to `PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH` and return `PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH_RESULTS`.

**Target:** `self.target` is the [Patient](/sdk/data-patient/#patient) id.

**Context:** `self.context["providers"]` — a list of `{"id", "title"}` entries, where `id` is a [Staff](/sdk/data-staff/#staff) id and `title` is the provider's name and roles.

Example — only offer the patient's own care-team providers:

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import CareTeamMembership
from canvas_sdk.v1.data.care_team import CareTeamMembershipStatus


class ProviderFilter(BaseHandler):
    RESPONDS_TO = EventType.Name(
        EventType.PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH
    )

    def compute(self) -> list[Effect]:
        providers = self.context.get("providers", [])
        care_team_ids = {
            str(staff_id)
            for staff_id in CareTeamMembership.objects.filter(
                patient__id=self.target, status=CareTeamMembershipStatus.ACTIVE
            ).values_list("staff__id", flat=True)
        }
        filtered = [p for p in providers if p["id"] in care_team_ids]
        return [
            Effect(
                type=EffectType.PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH_RESULTS,
                payload=json.dumps({"providers": filtered}),
            )
        ]
```

## Forms

Forms let you dynamically display questionnaires to patients in the portal based on your own criteria, and commit each response to the patient's chart as a Questionnaire Command when they submit. Because your handler runs on every portal page load, return only the forms that should currently appear.

{% include alert.html type="warning" content="Set <code>create_command=True</code> on almost every form. It's what puts the patient's response in the chart — as a committed Questionnaire Command in a note. Without it, the response is saved only as an Interview and never surfaces in the chart, so the care team won't see it. Leave it off only when you have a specific reason." %}

Respond to the `PATIENT_PORTAL__GET_FORMS` event and return a `FormResult` effect for each questionnaire to show.

| Attribute          | Type                      | Description                                                  |
|--------------------|---------------------------|--------------------------------------------------------------|
| `questionnaire_id` | `str` \| `UUID`           | The unique ID of the [Questionnaire](/sdk/data-questionnaire/#questionnaire) to show.                          |
| `create_command`   | `bool`                    | **Strongly recommended `True`.** Commits the response as a Questionnaire Command in a note so it appears in the chart. When `False` (the default), the response is saved only as an Interview and never appears in a note. |
| `note_id`          | `str` \| `UUID` \| `None` | The [Note](/sdk/data-note/#note) to place the command on. Only used when `create_command` is `True`; if omitted, Canvas creates and locks a new note for it. Has no effect on its own. |

**Example** — assign intake questionnaires when a patient has a confirmed upcoming visit, skipping any they've already completed:

```python
import arrow

from canvas_sdk.effects.patient_portal.form_result import FormResult
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Interview, Patient, Questionnaire
from canvas_sdk.v1.data.appointment import AppointmentProgressStatus

INTAKE_QUESTIONNAIRES = ["Insurance Details", "Preferred Pharmacy Details", "Social History"]
APPOINTMENT_NOTE_TYPES = ["Telehealth", "Office visit"]


class Handler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__GET_FORMS)

    def _upcoming_appointment_note_id(self, appointments):
        return appointments.filter(
            status=AppointmentProgressStatus.CONFIRMED,
            start_time__gt=arrow.now().date(),
            note_type__name__in=APPOINTMENT_NOTE_TYPES,
        ).values_list("note__id", flat=True).first()

    def compute(self):
        patient = Patient.objects.get(id=self.target)

        # Only assign intake forms when there's a confirmed upcoming visit
        note_id = self._upcoming_appointment_note_id(patient.appointments)
        if not note_id:
            return []

        # Which intake questionnaires are already completed *on this visit's note*.
        # committed() automatically drops entered-in-error and uncommitted interviews.
        # The same intake form is expected each visit, so scope the check to this note
        # rather than the whole patient.
        completed = set(
            Interview.objects.for_patient(patient.id)
            .committed()
            .filter(note_id=note_id, questionnaires__name__in=INTAKE_QUESTIONNAIRES)
            .values_list("questionnaires__name", flat=True)
        )

        missing = [name for name in INTAKE_QUESTIONNAIRES if name not in completed]
        missing_ids = Questionnaire.objects.filter(name__in=missing).values_list("id", flat=True)

        return [
            FormResult(questionnaire_id=qid, create_command=True, note_id=note_id).apply()
            for qid in missing_ids
        ]
```

**Best practices:**

- **Match questionnaires by name, not ID — it always resolves to the latest version.** When a questionnaire is updated, the previous version is archived with a `(v#)` suffix on its name (e.g. `Social History (v1)`) while the current version keeps the clean name. Filtering by the exact name therefore returns only the latest version, and (as a bonus) stays portable across instances, where IDs differ.
- **Prevent duplicates — but scope the check.** This logic runs on every page load, so check existing committed `Interview` responses before assigning a form again. Because the same intake form is typically expected at every visit, scope that check to the current appointment's `note_id` rather than the whole patient (use `.committed()` so entered-in-error responses are ignored automatically).
- **Don't let forms linger.** Return a questionnaire only while it should be shown; once it's completed or no longer relevant, stop returning it.
- **Always land responses in the chart.** Set `create_command=True` so each submission is committed as a Questionnaire Command; pass a `note_id` to target a specific note, or omit it to let Canvas create one. Without `create_command`, the response is only an Interview and the care team won't see it.

Real-world example: the MSF [patient-portal-forms](https://github.com/medical-software-foundation/canvas/tree/main/extensions/patient-portal-forms) extension assigns questionnaires (PHQ-9, GAD-7, ROS…) that patients complete in the portal, posting responses back to the chart.

## User Login

These effects manage a patient's portal **user account** — the login they use to access the portal. Invites and password resets are sent to the email or phone linked on the user, so make sure those contact points are actually **verified** before you invite a patient or rely on an updated value. Trigger a verification with the [Send Contact Verification](/sdk/effect-send-contact-verification/) effect.

### Update User

The `UpdateUserEffect` updates a portal user's phone number or email. In the future this may support additional attributes, but for now only these two are supported. It isn't tied to a specific portal event — emit it from whatever handler fits your workflow (a common one is keeping the portal user in sync in response to `PATIENT_CONTACT_POINT_UPDATED`, as below).

| Attribute      | Type            | Required | Description                              |
|----------------|-----------------|----------|------------------------------------------|
| `user_dbid`    | `int`           | `true`   | The `dbid` of the [CanvasUser](/sdk/data-canvasuser/#user) to update. |
| `phone_number` | `str`           | `false`* | The phone number to store.               |
| `email`        | `str`           | `false`* | The email to store.                      |

**Validation:** at least one of `phone_number` or `email` must be provided, and `user_dbid` must resolve to an existing user (otherwise the effect returns a `User does not exist` error).


```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.update_user import UpdateUserEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import PatientContactPoint
from canvas_sdk.v1.data.common import ContactPointSystem


class SyncPortalUser(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CONTACT_POINT_UPDATED)

    def compute(self) -> list[Effect]:
        contact_point = PatientContactPoint.objects.get(id=self.target)

        # Only sync verified contact points. last_verified is set once the patient
        # completes the verification challenge (see Send Contact Verification); until
        # then the value shouldn't be trusted as the account's login channel.
        if not contact_point.last_verified:
            return []

        user = contact_point.patient.user

        # Only update when the value actually changed. Emitting an effect that sets the
        # user to what it already is is a no-op — and can retrigger
        # PATIENT_CONTACT_POINT_UPDATED, causing an update loop.
        if contact_point.system == ContactPointSystem.EMAIL and user.email != contact_point.value:
            return [UpdateUserEffect(user_dbid=user.dbid, email=contact_point.value).apply()]

        if contact_point.system == ContactPointSystem.PHONE and user.phone_number != contact_point.value:
            return [UpdateUserEffect(user_dbid=user.dbid, phone_number=contact_point.value).apply()]

        return []
```

### Send Invite

The `SendInviteEffect` triggers a portal invitation that lets the patient register or activate their portal account. Because the invite is delivered to the patient's email or phone, only send it once that contact point is **verified** (`PatientContactPoint.last_verified` is set — see [Send Contact Verification](/sdk/effect-send-contact-verification/)) and the patient hasn't already registered (`CanvasUser.is_portal_registered`). Verification completes with a save that fires `PATIENT_CONTACT_POINT_UPDATED`, which makes it a natural trigger for the invite. Re-inviting someone who has already activated their account just sends a redundant email/SMS.

| Attribute   | Type  | Required | Description                              |
|-------------|-------|----------|------------------------------------------|
| `user_dbid` | `int` | `true`   | The `dbid` of the [CanvasUser](/sdk/data-canvasuser/#user) to invite. |

**Validation:** `user_dbid` must resolve to an existing user (otherwise the effect returns a `User does not exist` error).


```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.send_invite import SendInviteEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import PatientContactPoint


class InviteVerifiedPatient(BaseHandler):
    # Verification completes with a save that fires this event
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CONTACT_POINT_UPDATED)

    def compute(self) -> list[Effect]:
        contact_point = PatientContactPoint.objects.get(id=self.target)

        # Only invite once the contact point is actually verified — that's the
        # channel the invitation will be delivered to.
        if not contact_point.last_verified:
            return []

        user = contact_point.patient.user
        # Only invite once: skip if there's no portal user yet, or they've already registered
        if user is None or user.is_portal_registered:
            return []

        return [SendInviteEffect(user_dbid=user.dbid).apply()]
```

<br/>
<br/>
<br/>