---
title: "Calendar Event Management"
slug: "calendar-event-management-effects"
excerpt: "Effects for creating, updating, and deleting calendar events"
hidden: false
---

## Overview

This allows developers to create, update, and delete calendar events for providers in Canvas. Events can be one-time or recurring, with support for daily and weekly recurrence patterns.

```python
from canvas_sdk.effects.calendar import CreateEvent, UpdateEvent, DeleteEvent, EventRecurrence, DaysOfWeek
from datetime import datetime

# Create a one-time event
CreateEvent(
    calendar_id="calendar-uuid",
    title="Patient Consultation",
    starts_at=datetime(2025, 1, 15, 9, 0),
    ends_at=datetime(2025, 1, 15, 10, 0)
)

# Create a recurring event
CreateEvent(
    calendar_id="calendar-uuid",
    title="Weekly Team Meeting",
    starts_at=datetime(2025, 1, 15, 14, 0),
    ends_at=datetime(2025, 1, 15, 15, 0),
    recurrence_frequency=EventRecurrence.Weekly,
    recurrence_interval=1,
    recurrence_days=[DaysOfWeek.Monday, DaysOfWeek.Wednesday],
    recurrence_ends_at=datetime(2025, 12, 31, 23, 59)
)

# Update an existing event
UpdateEvent(
    event_id="event-uuid",
    title="Updated Meeting Title",
    starts_at=datetime(2025, 1, 15, 15, 0),
    ends_at=datetime(2025, 1, 15, 16, 0)
)

# Delete an event
DeleteEvent(
    event_id="event-uuid"
)
```

## Structure

### **EventRecurrence**

An enumeration of recurrence frequency options:

| Value      | Description                        |
|------------|------------------------------------|
| `Daily`    | Event recurs daily                 |
| `Weekly`   | Event recurs weekly                |


### **DaysOfWeek**

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


### **CreateEvent**

A CreateEvent effect consists of the following properties:

#### Attributes

| Attribute              | Type                      | Description                                          |
|------------------------|---------------------------|------------------------------------------------------|
| `calendar_id`          | `str \| UUID`             | The calendar UUID where the event will be created. |
| `title`                | `str`                     | The title of the event. |
| `starts_at`            | `datetime`                | The start date and time of the event.|
| `ends_at`              | `datetime`                | The end date and time of the event.|
| `recurrence_frequency` | `EventRecurrence \| None` | The frequency of recurrence - either `EventRecurrence.Daily` or `EventRecurrence.Weekly`. |
| `recurrence_interval`  | `int \| None`             | The interval between recurrences (e.g., 1 for every week, 2 for every other week). |
| `recurrence_days`      | `list[DaysOfWeek] \| None` | List of days when the event should recur (used with weekly recurrence). |
| `recurrence_ends_at`   | `datetime \| None`        | The date and time when the recurrence pattern ends. |
| `allowed_note_types`   | `list[str] \| None`       | List of note types that are allowed for this event. |


### **UpdateEvent**

An UpdateEvent effect consists of the following properties:

#### Attributes

| Attribute              | Type                      | Description                                          |
|------------------------|---------------------------|------------------------------------------------------|
| `event_id`             | `str \| UUID`             | The event UUID to update. |
| `title`                | `str`                     | The title of the event. |
| `starts_at`            | `datetime`                | The start date and time of the event.|
| `ends_at`              | `datetime`                | The end date and time of the event.|
| `recurrence_frequency` | `EventRecurrence \| None` | The frequency of recurrence - either `EventRecurrence.Daily` or `EventRecurrence.Weekly`. |
| `recurrence_interval`  | `int \| None`             | The interval between recurrences (e.g., 1 for every week, 2 for every other week). |
| `recurrence_days`      | `list[DaysOfWeek] \| None` | List of days when the event should recur (used with weekly recurrence). |
| `recurrence_ends_at`   | `datetime \| None`        | The date and time when the recurrence pattern ends. |
| `allowed_note_types`   | `list[str] \| None`       | List of note types that are allowed for this event. |


### **DeleteEvent**

A DeleteEvent effect consists of the following properties:

#### Attributes

| Attribute  | Type          | Description                |
|------------|---------------|----------------------------|
| `event_id` | `str \| UUID` | The event UUID to delete. |
