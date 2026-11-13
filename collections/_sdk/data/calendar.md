---
title: "Calendar"
slug: "data-calendar"
excerpt: "Canvas SDK Calendar"
hidden: false
---

## Introduction

The `Calendar` model represents a Calendar in Canvas. Calendars are used to organize events for providers and can be either Clinic or Administrative type.

When a calendar's `description` is its provider's staff id, Canvas links the calendar to the provider by that id. To [find a provider's calendar](#find-a-providers-calendar), filter by `description` rather than by `title`. The title contains the provider's name, so a title lookup stops finding the calendar after the provider is renamed.

Busy time that native Google Calendar sync imports for a provider isn't stored as calendar events. To read it, use the [Google Calendar](/sdk/data-google-calendar/) data models.

## Basic usage

To get a calendar by identifier, use the `get` method on the `Calendar` model manager:

```python
from canvas_sdk.v1.data.calendar import Calendar

calendar = Calendar.objects.get(id="f53626e4-0683-43ac-a1b7-c52815639ce2")
```

### Find a provider's calendar

To get a provider's calendars, filter by `description` with the provider's staff id:

```python
from canvas_sdk.v1.data.calendar import Calendar

provider_id = "4150cd20de8a470aa570a852859ac87e"  # The provider's staff id

calendars = Calendar.objects.filter(description=provider_id)
```

This finds calendars whose `description` was set to the staff id when they were created, as the [Calendar effect](/sdk/calendar-create-effect/) recommends. A calendar created with any other description doesn't match.

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

# Filter calendars by timezone
calendars = Calendar.objects.filter(timezone="America/New_York")
```

### By calendar name

To filter calendars by their exact title, use the `for_calendar_name` method. It builds the title from the provider name, calendar type, and location as `<provider_name>: <calendar_type>: <location>`, or `<provider_name>: <calendar_type>` with no location, and returns calendars with exactly that title:

```python
from canvas_sdk.v1.data.calendar import Calendar

calendars = Calendar.objects.for_calendar_name(
    provider_name="Dr. Smith",
    calendar_type="Clinic",
    location="Main Office"
)
```

{% include alert.html type="warning" content="A calendar's title keeps the provider's name from when the calendar was created. After the provider is renamed, <code>for_calendar_name</code> with the new name doesn't find the calendar. To find a provider's calendar, use <a href='#find-a-providers-calendar'>the provider's staff id</a> instead." %}

## Attributes

### Calendar

| Field Name    | Type     | Description                                      |
|---------------|----------|--------------------------------------------------|
| id            | UUID     | Unique identifier for the calendar               |
| dbid          | Integer  | Database identifier                              |
| created       | DateTime | When the record was created.                     |
| modified      | DateTime | When the record was last modified.               |
| title         | String   | The title of the calendar                        |
| timezone      | TimeZone | The timezone for the calendar (default: UTC)     |
| description   | String   | For a provider's calendar, the provider's staff id, which links the calendar to the provider. See [Find a provider's calendar](#find-a-providers-calendar). |
| events        | [Event](#event)[] | Events associated with this calendar    |

### Event

| Field Name               | Type                    | Description                                            |
|--------------------------|-------------------------|--------------------------------------------------------|
| id                       | UUID                    | Unique identifier for the event                        |
| dbid                     | Integer                 | Database identifier                                    |
| created                  | DateTime                | When the record was created.                           |
| modified                 | DateTime                | When the record was last modified.                     |
| title                    | String                  | The title of the event                                 |
| description              | String                  | Description of the event                               |
| calendar                 | [Calendar](#calendar)   | The calendar this event belongs to                     |
| starts_at                | DateTime                | The start date and time of the event                   |
| ends_at                  | DateTime                | The end date and time of the event                     |
| recurrence               | String                  | Recurrence rule for recurring events, as an iCalendar `RRULE` string such as `RRULE:FREQ=WEEKLY;UNTIL=20260828T000000Z;BYDAY=MO,TU`. The rule can leave out parts that have their default value, such as `INTERVAL=1`, so parse it rather than comparing its text. |
| recurrence_ends_at       | DateTime                | The date and time when the recurrence pattern ends. Empty for series with no end date. |
| recurring_parent_event   | [Event](#event)         | The parent event                                       |
| exceptions               | [Event](#event)[]       | Exception (override) events for this recurring parent event |
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
