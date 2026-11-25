---
title: "Calendar Create"
slug: "calendar-create-effect"
excerpt: "Effect for creating a calendar for a provider"
hidden: false
---

Create a Clinic or Administrative calendar for a provider, optionally for one location. Canvas titles the calendar from the provider's name, the calendar type, and the location name.

To keep the calendar linked to its provider after a name change, set [`description`](#attributes) to the provider's staff id.

Build a `Calendar` with the [attributes](#attributes) you want to set, then return its `create()` from your handler.

## Methods

### create() → Effect

Creates the calendar.

- `provider` and `type` are required.

## Attributes

| Attribute     | Type                         | Description                                                                          | Required |
|---------------|------------------------------|--------------------------------------------------------------------------------------|----------|
| `id`          | `str \| UUID \| None`        | Optional unique identifier for the calendar.                                         | No       |
| `provider`    | `str \| UUID`                | The id of the [provider](/sdk/data-staff/).                                          | Yes      |
| `type`        | [`CalendarType`](#calendartype) | The type of calendar: `CalendarType.Clinic` or `CalendarType.Administrative`.      | Yes      |
| `location`    | `str \| UUID \| None`        | The id of the [location](/sdk/data-practicelocation/) to associate with the calendar. | No       |
| `description` | `str \| None`                | The provider's staff id, the same value as `provider`. Canvas uses it to link the calendar to the provider. With any other value, Canvas matches the calendar by the provider name in its title, and that match stops working when the provider is renamed. | No, but strongly recommended |

{% include alert.html type="info" content="A plugin can't change a calendar's title or description after it creates the calendar. To find a provider's existing calendar, filter by its description, as in <a href='#find-a-providers-calendar'>Find a provider's calendar</a>, rather than by its title, so the lookup still finds the calendar after the provider is renamed." %}

## CalendarType

An enumeration of calendar types:

| Value             | Description                                    |
|-------------------|------------------------------------------------|
| `Clinic`          | Calendar for clinical appointments             |
| `Administrative`  | Calendar for administrative tasks              |

## Example

```python
from canvas_sdk.effects.calendar import Calendar, CalendarType

provider_id = "4150cd20de8a470aa570a852859ac87e"  # The provider's staff id

Calendar(
   provider=provider_id,
   type=CalendarType.Clinic,
   location="location-uuid",
   description=provider_id,
).create()
```

## Find a provider's calendar

To check whether a provider already has a calendar before you create one, filter the [Calendar](/sdk/data-calendar/) data model by `description`:

```python
from canvas_sdk.v1.data.calendar import Calendar

provider_id = "4150cd20de8a470aa570a852859ac87e"  # The provider's staff id

calendars = Calendar.objects.filter(description=provider_id)
```
