---
title: "Calendar Create"
slug: "calendar-create-effect"
excerpt: "Effect for creating a calendar for a provider"
hidden: false
---

This allows developers to create calendars for providers in Canvas. Calendars can be either Clinic or Administrative type and can optionally be associated with a location.

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
| `description` | `str \| None`                | Description of the calendar's purpose.                                               | No       |

## CalendarType

An enumeration of calendar types:

| Value             | Description                                    |
|-------------------|------------------------------------------------|
| `Clinic`          | Calendar for clinical appointments             |
| `Administrative`  | Calendar for administrative tasks              |

## Example

```python
from canvas_sdk.effects.calendar import Calendar, CalendarType

Calendar(
   provider="provider-uuid",
   type=CalendarType.Clinic,
   location="location-uuid",
   description="Primary clinic calendar"
).create()
```
