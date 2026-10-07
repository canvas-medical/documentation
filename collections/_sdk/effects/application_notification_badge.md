---
title: "Application Notification Badge"
slug: "effect-application-notification-badge"
excerpt: "Display and update a notification badge count on an application icon."
hidden: false
---

Notification badges let your plugin show a count on an [application](/sdk/handlers-applications/), such as how many unread items are waiting.

Where the badge appears depends on the application's [scope](/sdk/handlers-applications/#application-scopes):

| Scope | Where the badge appears |
| --- | --- |
| `global` | On the application's icon in the app drawer. |
| `patient_specific` | On the application's icon in the app drawer, or on the panel when the application sets `show_in_panel`. |
| `provider_menu_item` | Next to the application's label in the provider menu. |
| `portal_menu_item` | Next to the application's label in the patient portal menu, for the patient who is logged in. |

Applications in other scopes, such as `full_chart` and the Provider Companion scopes, do not show badges.

There are two ways a badge is set:

- **On load** — override `compute_notification_badge()` on your `Application`
  handler to provide the initial count shown when Canvas loads applications. See
  [Notification Badges](/sdk/handlers-applications/#notification-badges) on the
  Applications handler page.
- **Live updates** — emit an `ApplicationNotificationBadge` effect from any event
  handler to update the count in real time, without the user reloading the page.
  This is what the rest of this page covers.

## Setting a badge

`ApplicationNotificationBadge` is a fluent builder. Construct it with the target application's identifier, optionally call `.filter(...)` to target patients, then return `.broadcast(...)` from your handler.

### Methods

#### filter(*, patient_ids: list[str] | None = None) → ApplicationNotificationBadge

Scopes the update to the listed patients: their charts, and their own patient portal. Returns the builder, so the call chains into `.broadcast(...)`.

#### broadcast(count: int, staff_ids: list[str] | None = None) → Effect

Sets the badge to `count` for the staff and patients you target. See [Targeting](#targeting).

- `count` is required and must be `>= 0`; a count of `0` clears the badge.
- The `application_identifier` passed to the constructor must match an installed application, or the effect raises a validation error.

### Attributes

| Attribute                | Type        | Description                                                                                                                                                | Required |
| ------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `application_identifier` | `str`       | Passed to the constructor. Must match the application's `class` string declared in [`CANVAS_MANIFEST.json`](/sdk/canvas_manifest/#applications), the `<module path>:<ClassName>` value (identical to the handler's `identifier`). | Yes      |
| `count`                  | `int`       | Passed to `.broadcast()`. The badge value to display.                                                                                                      | Yes      |
| `staff_ids`              | `list[str]` | Passed to `.broadcast()`. Ids of the [staff](/sdk/data-staff/) who should see the update.                                                                  | No       |
| `patient_ids`            | `list[str]` | Passed to `.filter()`. Ids of the [patients](/sdk/data-patient/) the update applies to: their charts, and their own patient portal.                        | No       |

The `application_identifier` is the application's `class` string from
`CANVAS_MANIFEST.json` (`<module path>:<ClassName>`). For example, an `InboxApp`
defined in `my_plugin/apps/inbox.py` and registered like this:

```json
"applications": [
  {
    "class": "my_plugin.apps.inbox:InboxApp",
    "name": "Inbox",
    "description": "Unread items inbox",
    "icon": "/assets/inbox.png",
    "scope": "global"
  }
]
```

is targeted by that same `class` string:

```python
from canvas_sdk.effects.application_notification_badge import ApplicationNotificationBadge

# Set a badge of 3 for a specific staff member.
ApplicationNotificationBadge("my_plugin.apps.inbox:InboxApp").broadcast(count=3, staff_ids=["staff-id"])
```

## Targeting

`staff_ids` and `patient_ids` control who sees the update. An empty list means
"all" on that axis:

| `staff_ids` | `patient_ids` | Who sees the badge                                                                       |
| ----------- | ------------- | ---------------------------------------------------------------------------------------- |
| set         | empty         | The listed staff, on any patient (and on global views).                                  |
| empty       | set           | Staff currently viewing the listed patients' charts, and the listed patients in the patient portal. |
| set         | set           | The listed staff, but only while viewing the listed patients' charts.                    |
| empty       | empty         | All staff, all patients (a system-wide update). The patient portal is not updated.       |

The patient portal receives an update only when you set `patient_ids` and leave
`staff_ids` empty. Each listed patient sees the new count on the matching
`portal_menu_item` application while they're logged in to the portal. Updates
that name staff, and system-wide updates, never reach the portal. A patient
only ever receives updates sent for their own id.

Because `patient_ids` reaches both audiences, the application's scope decides
where the badge appears. A `patient_specific` application shows it to staff on
the chart. A `portal_menu_item` application shows it to the patient in the
portal.

> **Note on "all patients" (empty `patient_ids`):** the update is delivered
> **live** only to charts a staff member currently has open. Other patients'
> charts reflect the new value the next time they're loaded, via
> `compute_notification_badge()`. So for a badge that should read the same across
> every patient, have `compute_notification_badge()` return a patient-independent
> count (ignore the patient in `self.event.context`). A push then keeps the
> open chart live, and the load-time hook covers the rest.

```python
from canvas_sdk.effects.application_notification_badge import ApplicationNotificationBadge

# Show a badge to staff viewing a specific patient's chart.
ApplicationNotificationBadge("my_plugin.apps.patient_labs:PatientLabsApp").filter(
    patient_ids=["patient-id"]
).broadcast(count=5)

# Show a badge to a patient in the patient portal (portal_menu_item application).
ApplicationNotificationBadge("my_plugin.apps.messages:PortalMessagesApp").filter(
    patient_ids=["patient-id"]
).broadcast(count=2)

# Combine: only the on-call provider, and only on this patient's chart.
ApplicationNotificationBadge("my_plugin.apps.patient_labs:PatientLabsApp").filter(
    patient_ids=["patient-id"]
).broadcast(count=1, staff_ids=["staff-id"])
```

## Reacting to events

The most common pattern is updating a badge in response to a domain event. Here a
handler recomputes a staff member's inbox count whenever a task is created and
pushes the new value live:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.application_notification_badge import ApplicationNotificationBadge
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.task import Task, TaskStatus


class InboxBadgeHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.TASK__CREATED)

    def compute(self) -> list[Effect]:
        task = Task.objects.get(id=self.event.target.id)
        assignee = task.assignee
        if not assignee:
            return []

        open_count = Task.objects.filter(assignee=assignee, status=TaskStatus.OPEN).count()

        return [
            ApplicationNotificationBadge("my_plugin.apps.inbox:InboxApp").broadcast(
                count=open_count,
                staff_ids=[assignee.id],
            )
        ]
```

## Clearing a badge

Broadcast a `count` of `0` to remove the badge from the icon:

```python
from canvas_sdk.effects.application_notification_badge import ApplicationNotificationBadge

ApplicationNotificationBadge("my_plugin.apps.inbox:InboxApp").broadcast(count=0, staff_ids=["staff-id"])
```

> **Note:** To set the badge value shown when applications first load (rather than
> in response to an event), override `compute_notification_badge()` on your
> `Application` handler. See
> [Notification Badges](/sdk/handlers-applications/#notification-badges).
