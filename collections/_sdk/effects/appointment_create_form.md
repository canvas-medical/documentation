---
title: "Appointment Metadata Create form"
slug: "appointment-metadata-create-form-effect"
excerpt: "Effect for dynamically displaying fields when scheduling an appointment"
hidden: false
---

## Overview

This allows developers to dynamically display additional fields when scheduling an appointment.

```python
from canvas_sdk.effects.appointments_metadata import (
    FormField,
    InputType,
    AppointmentsMetadataCreateFormEffect,
)

AppointmentsMetadataCreateFormEffect(form_fields=[
    FormField(
        key='status',
        label='Status',
        type=InputType.SELECT,
        required=False,
        editable=True,
        options=["open", "close"],
        value=""
    ),
])
```

## Structure

### **FormField**

A FormField consists of the following properties:

#### Attributes

| Attribute          | Type   | Description                                                 |
|--------------------|--------|-------------------------------------------------------------|
| `key`              | `str`  | unique identifier of the field - appointment metadata key   |
| `label`            | `str`  | the label that will be displayed on the field               |
| `type`             | `InputType`         | the type of the input - TEXT, SELECT, DATE.                 |
| `required`         | `bool` | if the input is required.                                   |
| `editable`         | `bool` | if the input can be editabled.                              |
| `options`          | `list[str]` | possible options for when the input type is set to "SELECT” |
| `value`            | `str`  | default value for the field                                 |


### **AppointmentsMetadataCreateFormEffect**

An AppointmentsMetadataCreateFormEffect consists of the following properties:

#### Attributes

| Attribute          | Type   | Description                                                  |
|--------------------|--------|--------------------------------------------------------------|
| `form_fields`      | `list[FormField]`                                                   | list of fields. |

