---
title: "Calendar"
slug: "data-calendar"
excerpt: "Canvas SDK Calendar"
hidden: false
---

## Introduction

The `Calendar` model represents a Calendar in Canvas. Calendars are used to organize events for providers and can be either Clinic or Administrative type.

## Basic usage

To get a calendar by identifier, use the `get` method on the `Calendar` model manager:

```python
from canvas_sdk.v1.data.calendar import Calendar

calendar = Calendar.objects.get(id="f53626e4-0683-43ac-a1b7-c52815639ce2")
```

## Events

The events associated with a calendar can be accessed with the `events` attribute on a `Calendar` object:

```python
from canvas_sdk.v1.data.calendar import Calendar

calendar = Calendar.objects.get(id="f53626e4-0683-43ac-a1b7-c52815639ce2")
events = calendar.events.all()
```

To get a specific event by identifier:

```python
from canvas_sdk.v1.data.calendar import Event

event = Event.objects.get(id="a1b2c3d4-5678-90ab-cdef-1234567890ab")
```


## Filtering

Calendars and events can be filtered by any attribute that exists on the model.

Filtering is done with the `filter` method on the model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.calendar import Calendar

# Filter calendars by title
calendars = Calendar.objects.filter(title__icontains="Clinic")
```

### By calendar name

To filter calendars by a specific provider name, calendar type, and location, use the `for_calendar_name` method:

```python
from canvas_sdk.v1.data.calendar import Calendar

calendars = Calendar.objects.for_calendar_name(
    provider_name="Dr. Smith",
    calendar_type="Clinic",
    location="Main Office"
)
```

## Attributes

### Calendar

| Field Name    | Type     | Description                                      |
|---------------|----------|--------------------------------------------------|
| id            | UUID     | Unique identifier for the calendar               |
| dbid          | Integer  | Database identifier                              |
| title         | String   | The title of the calendar                        |
| timezone      | TimeZone | The timezone for the calendar (default: UTC)     |
| description   | String   | Optional description of the calendar's purpose   |
| events        | [Event](#event)[] | Events associated with this calendar    |

### Event

| Field Name               | Type                    | Description                                            |
|--------------------------|-------------------------|--------------------------------------------------------|
| id                       | UUID                    | Unique identifier for the event                        |
| dbid                     | Integer                 | Database identifier                                    |
| title                    | String                  | The title of the event                                 |
| description              | String                  | Description of the event                               |
| calendar                 | [Calendar](#calendar)   | The calendar this event belongs to                     |
| starts_at                | DateTime                | The start date and time of the event                   |
| ends_at                  | DateTime                | The end date and time of the event                     |
| recurrence               | String                  | Recurrence rule for recurring events                   |
| recurrence_ends_at       | DateTime                | The date and time when the recurrence pattern ends     |
| recurring_parent_event   | [Event](#event)         | The parent event                                       |
| original_starts_at       | DateTime                | The original start time for recurring event exceptions |
| is_all_day               | Boolean                 | Whether this is an all-day event (default: false)      |
| is_cancelled             | Boolean                 | Whether this event has been cancelled (default: false) |
| allowed_note_types       | NoteType[]              | Note types that are allowed for this event             |

## Examples

### Working with calendar events

```python
from canvas_sdk.v1.data.calendar import Calendar
from datetime import datetime
from logger import log

calendar = Calendar.objects.get(id="f53626e4-0683-43ac-a1b7-c52815639ce2")

# Get all upcoming events
upcoming_events = calendar.events.filter(
    starts_at__gte=datetime.now(),
    is_cancelled=False
).order_by('starts_at')

for event in upcoming_events:
    log.info(f"Event: {event.title}")
    log.info(f"Starts at: {event.starts_at}")
    log.info(f"Ends at: {event.ends_at}")

    if event.recurrence:
        log.info(f"Recurrence: {event.recurrence}")
```

<br/>
<br/>
<br/>
