---
title: "ScheduleDuration"
slug: "data-schedule-duration"
excerpt: "Canvas SDK ScheduleDuration"
hidden: false
---

## Introduction

The `ScheduleDuration` model represents a length of time that can be used for appointments or schedule events. Read it to offer the same duration choices your instance shows when scheduling.

## Basic usage

**List the durations offered for appointments**

```python
from canvas_sdk.v1.data import ScheduleDuration

appointment_durations = ScheduleDuration.objects.filter(
    is_appointment_duration_option=True
).order_by("duration")
print([d.duration.total_seconds() / 60 for d in appointment_durations])
```

## Attributes

### ScheduleDuration

| Field Name                     | Type                 |
| ------------------------------ | -------------------- |
| dbid                           | Integer              |
| created                        | DateTime             |
| modified                       | DateTime             |
| duration                       | Duration (timedelta) |
| is_appointment_duration_option | Boolean              |
