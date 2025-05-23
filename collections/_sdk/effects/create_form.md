---
title: "Patient Metadata Create form"
slug: "patient-metadata-create-form-effect"
excerpt: "Effect for dynamically displaying fields on patient profile"
hidden: false
---

## Overview

This allow developers to dynamically display additional fields to the patient profile.

```python
    PatientMetadataCreateFormEffect(form_fields=[
        FormField(
            key='status',
            label='Status',
            type=InputType.SELECT,
            required=False,
            editable=True,
            options=["open", "close"]
        ),
    ])
```

## Structure

### **FormField**

A FormField consists of the following properties:

#### Attributes

| Attribute          | Type   | Description                                                  |
|--------------------|--------|--------------------------------------------------------------|
| `key`              | `str`  | unique identifier of the field - patient metadata key        |
| `label`            | `str`  | the label that will be displayed on the field                |
| `type`             | `InputType`         | the type of the input - TEXT, SELECT, DATE.     |
| `required`         | `bool` | if the input is required. |
| `editable`         | `bool` | if the input can be editabled. |
| `options`          | `list[str]` | possible options for when the input type is set to "SELECT”  |


### **PatientMetadataCreateFormEffect**

A PatientMetadataCreateFormEffect consists of the following properties:

#### Attributes

| Attribute          | Type   | Description                                                  |
|--------------------|--------|--------------------------------------------------------------|
| `form_fields`      | `list[FormField]`                                                   | list of fields. |

