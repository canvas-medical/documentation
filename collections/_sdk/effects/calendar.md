---
title: "Calendar Create"
slug: "calendar-create-effect"
excerpt: "Effect for creating a calendar for a provider"
hidden: false
---

## Overview

This allows developers to create calendars for providers in Canvas. Calendars can be either Clinic or Administrative type and can optionally be associated with a location.

```python
from canvas_sdk.effects.calendar import CreateCalendar, CalendarType

CreateCalendar(
   provider="provider-uuid",
   type=CalendarType.Clinic,
   location="location-uuid",
   description="Primary clinic calendar"
)
```

## Structure

### **CalendarType**

An enumeration of calendar types:

| Value             | Description                                    |
|-------------------|------------------------------------------------|
| `Clinic`          | Calendar for clinical appointments             |
| `Administrative`  | Calendar for administrative tasks              |


### **CreateCalendar**

A CreateCalendar effect consists of the following properties:

#### Attributes

| Attribute     | Type                  | Description                                                                         |
|---------------|-----------------------|-------------------------------------------------------------------------------------|
| `id`          | `str \| UUID \| None` | Optional unique identifier for the calendar.                                        |
| `provider`    | `str \| UUID`         | The provider UUID                                                                   |
| `type`        | `CalendarType`        | The type of calendar - either `CalendarType.Clinic` or `CalendarType.Administrative` |
| `location`    | `str \| UUID \| None` | location UUID to associate with the calendar. |
| `description` | `str \| None`         | description of the calendar's purpose.                                              |
