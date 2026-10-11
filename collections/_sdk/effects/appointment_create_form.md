---
title: "Appointment Metadata Create form"
slug: "appointment-metadata-create-form-effect"
excerpt: "Effect for dynamically displaying fields when scheduling an appointment"
hidden: false
---

This allows developers to dynamically display additional fields when scheduling an appointment. For more guidance, see the ["How to add additional fields to the scheduling appointment fields" guide](/guides/appointments-additional_fields/).

Build an `AppointmentsMetadataCreateFormEffect` with the [form fields](#formfield) to show, then return its `apply()` from an `APPOINTMENT__FORM__GET_ADDITIONAL_FIELDS` handler.

## Methods

### apply() → Effect

Displays the form fields on the appointment form.

- `form_fields` is required.
- `options` may only be set on fields whose `type` is `InputType.SELECT`.

## Attributes

| Attribute     | Type                                | Description     | Required |
|---------------|-------------------------------------|-----------------|----------|
| `form_fields` | `list[`[`FormField`](#formfield)`]` | List of fields. | Yes      |

## FormField

| Attribute  | Type        | Description                                                  |
|------------|-------------|--------------------------------------------------------------|
| `key`      | `str`       | Unique identifier of the field; the appointment metadata key.    |
| `label`    | `str`       | The label displayed on the field.                            |
| `type`     | `InputType` | The type of the input: `TEXT`, `SELECT`, or `DATE`. Defaults to `TEXT`. |
| `required` | `bool`      | Whether the input is required. Defaults to `False`.          |
| `editable` | `bool`      | Whether the input can be edited. Defaults to `True`.         |
| `options`  | `list[str]` | Possible options when the input type is `SELECT`. Only allowed on `SELECT` fields. |
| `value`    | `str`       | Default value for the field.                                 |

## Example

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
]).apply()
```

<br/>
<br/>
<br/>
