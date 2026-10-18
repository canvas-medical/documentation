---
title: "Google Calendar"
slug: "data-google-calendar"
excerpt: "Canvas SDK Google Calendar busy blocks and connections"
hidden: false
---

## Introduction

When a provider connects their Google account through native Google Calendar sync, Canvas imports the busy time from their selected Google calendars. Canvas stores that busy time in its own records rather than as [appointments](/sdk/data-appointment/) or [calendar events](/sdk/data-calendar/), so a scheduling or booking plugin that works out availability only from `Appointment` and `Event` misses it.

The Google Calendar data models give plugins read-only access to that busy time and to the state of each provider's connection:

- `GoogleCalendarBusyBlock` is a period of busy time imported from Google for a provider.
- `GoogleCalendarConnection` is a provider's connection to their Google account.
- `GoogleCalendar` is a calendar on that connection.

Busy blocks carry only the time a provider is busy. They don't include the title or content of the Google event. These models have a `dbid` but no `id`.

## Busy blocks

A provider's busy blocks are available through the `google_calendar_busy_blocks` attribute on a [Staff](/sdk/data-staff/) object. When busy time is released, its busy block stays in the table with `active` set to `False`, so filter on `active=True` to get current busy time:

```python
from canvas_sdk.v1.data.staff import Staff

provider = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")
busy_blocks = provider.google_calendar_busy_blocks.filter(active=True)
```

A busy block records its start and its length in minutes, not an end time. A Google event that spans several days arrives as one busy block for each day.

### Find a provider's busy time for a day

This example lists a provider's current busy intervals that start on a given day, ordered by start time:

```python
import datetime

from canvas_sdk.v1.data.google_calendar import GoogleCalendarBusyBlock
from logger import log

day_start = datetime.datetime(2026, 10, 20, tzinfo=datetime.UTC)
day_end = day_start + datetime.timedelta(days=1)

busy_blocks = GoogleCalendarBusyBlock.objects.filter(
    provider__id="4150cd20de8a470aa570a852859ac87e",
    active=True,
    start_time__gte=day_start,
    start_time__lt=day_end,
).order_by("start_time")

for block in busy_blocks:
    block_end = block.start_time + datetime.timedelta(minutes=block.duration_minutes)
    log.info(f"Busy from {block.start_time} to {block_end} at {block.location.full_name}")
```

## Connections and calendars

A provider's Google connection is available through the `google_calendar_connection` attribute on a `Staff` object. A provider who hasn't connected a Google account has no connection, so filter on the `staff` field to get `None` back instead of an exception:

```python
from canvas_sdk.v1.data.google_calendar import GoogleCalendarConnection
from canvas_sdk.v1.data.staff import Staff

provider = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")
connection = GoogleCalendarConnection.objects.filter(staff=provider).first()
```

When `needs_reconnect` is `True`, the provider needs to reconnect their Google account in Canvas.

The calendars on a connection are available through its `calendars` attribute. Only selected calendars feed busy blocks. The calendar with `is_app_created` set to `True` is the one Canvas writes appointments to:

```python
from canvas_sdk.v1.data.google_calendar import GoogleCalendarConnection

connection = GoogleCalendarConnection.objects.filter(
    staff__id="4150cd20de8a470aa570a852859ac87e"
).first()

if connection is not None:
    busy_time_calendars = connection.calendars.filter(selected=True)
    canvas_calendar = connection.calendars.filter(is_app_created=True).first()
```

## Attributes

### GoogleCalendarBusyBlock

| Field Name       | Type                                            | Description                                                              |
|------------------|-------------------------------------------------|--------------------------------------------------------------------------|
| dbid             | Integer                                         | Database identifier                                                      |
| created          | DateTime                                        | When the record was created.                                             |
| modified         | DateTime                                        | When the record was last modified.                                       |
| provider         | [Staff](/sdk/data-staff/#staff)                 | The provider who is busy                                                 |
| location         | [PracticeLocation](/sdk/data-practicelocation/) | The practice location the busy block applies to                          |
| start_time       | DateTime                                        | When the busy time starts                                                |
| duration_minutes | Integer                                         | How long the busy time lasts, in minutes                                 |
| active           | Boolean                                         | Whether the block is current busy time; `False` once the time is released |

### GoogleCalendarConnection

| Field Name           | Type                                       | Description                                                       |
|----------------------|--------------------------------------------|-------------------------------------------------------------------|
| dbid                 | Integer                                    | Database identifier                                               |
| created              | DateTime                                   | When the record was created.                                      |
| modified             | DateTime                                   | When the record was last modified.                                |
| staff                | [Staff](/sdk/data-staff/#staff)            | The provider who owns the connection                              |
| google_account_email | String                                     | The email address of the connected Google account                 |
| needs_reconnect      | Boolean                                    | Whether the provider must reconnect their Google account          |
| calendars            | [GoogleCalendar](#googlecalendar)[]        | The Google calendars on this connection                           |

### GoogleCalendar

| Field Name     | Type                                                  | Description                                                    |
|----------------|-------------------------------------------------------|----------------------------------------------------------------|
| dbid           | Integer                                               | Database identifier                                            |
| created        | DateTime                                              | When the record was created.                                   |
| modified       | DateTime                                              | When the record was last modified.                             |
| connection     | [GoogleCalendarConnection](#googlecalendarconnection) | The connection the calendar belongs to                         |
| summary        | String                                                | The calendar's name in Google                                  |
| selected       | Boolean                                               | Whether the calendar's events feed busy blocks                 |
| is_app_created | Boolean                                               | Whether this is the calendar Canvas writes appointments to     |

<br/>
<br/>
<br/>
