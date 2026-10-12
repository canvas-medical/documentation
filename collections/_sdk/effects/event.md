---
title: "Calendar Event Management"
slug: "calendar-event-management-effects"
excerpt: "Effects for creating, updating, and deleting calendar events"
hidden: false
---

This allows developers to create, update, and delete calendar events for providers in Canvas. Events can be one-time or recurring, with support for daily and weekly recurrence patterns.

Build an `Event` with the [attributes](#attributes) you want to set, then return one of its methods from your handler: [`create()`](#create--effect), [`update()`](#update--effect), or [`delete()`](#delete--effect).

## Methods

### create() → Effect

Creates the event on a calendar.

- `calendar_id`, `title`, `starts_at`, and `ends_at` are required.

### update() → Effect

Updates an existing event.

- `event_id`, `title`, `starts_at`, and `ends_at` are required.

### delete() → Effect

Deletes an existing event.

- `event_id` is required.

## Attributes

| Attribute              | Type                                       | Description                                                                                         | Required                           |
|------------------------|--------------------------------------------|-----------------------------------------------------------------------------------------------------|------------------------------------|
| `calendar_id`          | `str \| UUID \| None`                      | The id of the calendar where the event will be created.                                             | For `create()`                     |
| `event_id`             | `str \| UUID \| None`                      | The id of the event to update or delete.                                                            | For `update()` and `delete()`      |
| `title`                | `str \| None`                              | The title of the event.                                                                             | For `create()` and `update()`      |
| `starts_at`            | `datetime \| None`                         | The start date and time of the event.                                                               | For `create()` and `update()`      |
| `ends_at`              | `datetime \| None`                         | The end date and time of the event.                                                                 | For `create()` and `update()`      |
| `recurrence_frequency` | [`EventRecurrence`](#eventrecurrence) `\| None` | The frequency of recurrence: `EventRecurrence.Daily` or `EventRecurrence.Weekly`.          | No                                 |
| `recurrence_interval`  | `int \| None`                              | The interval between recurrences (for example, 1 for every week, 2 for every other week).           | No                                 |
| `recurrence_days`      | `list[`[`DaysOfWeek`](#daysofweek)`] \| None` | List of days when the event should recur (used with weekly recurrence).                        | No                                 |
| `recurrence_ends_at`   | `datetime \| None`                         | The date and time when the recurrence pattern ends.                                                 | No                                 |
| `allowed_note_types`   | `list[str] \| None`                        | List of note types that are allowed for this event.                                                 | No                                 |

## EventRecurrence

An enumeration of recurrence frequency options:

| Value      | Description                        |
|------------|------------------------------------|
| `Daily`    | Event recurs daily                 |
| `Weekly`   | Event recurs weekly                |

## DaysOfWeek

An enumeration of days of the week for recurring events:

| Value | Description |
|-------|-------------|
| `MO`  | Monday      |
| `TU`  | Tuesday     |
| `WE`  | Wednesday   |
| `TH`  | Thursday    |
| `FR`  | Friday      |
| `SA`  | Saturday    |
| `SU`  | Sunday      |

## Example

```python
from canvas_sdk.effects.calendar import Event, EventRecurrence, DaysOfWeek
from datetime import datetime

# Create a one-time event
Event(
    calendar_id="calendar-uuid",
    title="Patient Consultation",
    starts_at=datetime(2025, 1, 15, 9, 0),
    ends_at=datetime(2025, 1, 15, 10, 0)
).create()

# Create a recurring event
Event(
    calendar_id="calendar-uuid",
    title="Weekly Team Meeting",
    starts_at=datetime(2025, 1, 15, 14, 0),
    ends_at=datetime(2025, 1, 15, 15, 0),
    recurrence_frequency=EventRecurrence.Weekly,
    recurrence_interval=1,
    recurrence_days=[DaysOfWeek.Monday, DaysOfWeek.Wednesday],
    recurrence_ends_at=datetime(2025, 12, 31, 23, 59),
    allowed_note_types=["100", "101"]
).create()

# Update an existing event
Event(
    event_id="event-uuid",
    title="Updated Meeting Title",
    starts_at=datetime(2025, 1, 15, 15, 0),
    ends_at=datetime(2025, 1, 15, 16, 0)
).update()

# Delete an event
Event(event_id="event-uuid").delete()
```
