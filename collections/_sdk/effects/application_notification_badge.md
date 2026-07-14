---
title: "Application Notification Badge"
slug: "effect-application-notification-badge"
excerpt: "Display and update a notification badge count on an application icon."
hidden: false
---

Notification badges let your plugin surface a count on an
[application](/sdk/handlers-applications/) icon — the small number that
indicates, for example, how many unread items are waiting. Badges are shown for
applications scoped [`global`](/sdk/handlers-applications/#application-scopes) or
[`patient_specific`](/sdk/handlers-applications/#application-scopes) — on their
icon in the app drawer, or, when the application sets `show_in_panel`, on the panel
alongside the other panel buttons — and for
[`provider_menu_item`](/sdk/handlers-applications/#application-scopes) applications,
next to their label in the provider menu. Applications in other scopes
(`full_chart`, `portal_menu_item`, and the Provider Companion scopes) do not
display badges.

There are two ways a badge is set:

- **On load** — override `compute_notification_badge()` on your `Application`
  handler to provide the initial count shown when Canvas loads applications. See
  [Notification Badges](/sdk/handlers-applications/#notification-badges) on the
  Applications handler page.
- **Live updates** — emit an `ApplicationNotificationBadge` effect from any event
  handler to update the count in real time, without the user reloading the page.
  This is what the rest of this page covers.

## Setting a badge

`ApplicationNotificationBadge` is a fluent builder. Construct it with the target
application's identifier, optionally `.filter(...)` to target patients, then call
`.broadcast(...)` to produce the effect.

| Method / Attribute       |          | Type        | Description                                                                                                                                                |
| ------------------------ | -------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `application_identifier` | required | String      | Passed to the constructor. Must match the application's `class` string declared in `CANVAS_MANIFEST.json` — the `<module path>:<ClassName>` value (identical to the handler's `identifier`). An unknown identifier raises a validation error. |
| `count`                  | required | Integer     | Passed to `.broadcast()`. The badge value to display. Must be `>= 0`; a count of `0` clears the badge.                                                      |
| `staff_ids`              | optional | list[String] | Passed to `.broadcast()`. [Staff](/sdk/data-staff/) keys that should see the update.                                                                       |
| `patient_ids`            | optional | list[String] | Passed to `.filter()`. [Patient](/sdk/data-patient/) keys whose chart context the update applies to.                                                       |

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
ApplicationNotificationBadge("my_plugin.apps.inbox:InboxApp").broadcast(count=3, staff_ids=["staff-key"])
```

## Targeting

`staff_ids` and `patient_ids` control who sees the update. An empty list means
"all" on that axis:

| `staff_ids` | `patient_ids` | Who sees the badge                                                                       |
| ----------- | ------------- | ---------------------------------------------------------------------------------------- |
| set         | empty         | The listed staff, on any patient (and on global views).                                  |
| empty       | set           | Staff currently viewing the listed patients' charts.                                     |
| set         | set           | The listed staff, but only while viewing the listed patients' charts.                    |
| empty       | empty         | All staff, all patients (a system-wide update).                                          |

Patients are never subscribers themselves — `patient_ids` scopes the badge to a
patient's chart, where staff viewing that chart will see it.

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
    patient_ids=["patient-key"]
).broadcast(count=5)

# Combine: only the on-call provider, and only on this patient's chart.
ApplicationNotificationBadge("my_plugin.apps.patient_labs:PatientLabsApp").filter(
    patient_ids=["patient-key"]
).broadcast(count=1, staff_ids=["staff-key"])
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

ApplicationNotificationBadge("my_plugin.apps.inbox:InboxApp").broadcast(count=0, staff_ids=["staff-key"])
```

> **Note:** To set the badge value shown when applications first load (rather than
> in response to an event), override `compute_notification_badge()` on your
> `Application` handler. See
> [Notification Badges](/sdk/handlers-applications/#notification-badges).
