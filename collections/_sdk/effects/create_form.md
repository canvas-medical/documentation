---
title: "Patient Metadata Create form"
slug: "patient-metadata-create-form-effect"
excerpt: "Effect for dynamically displaying fields in the patient profile"
hidden: false
---

This allows developers to dynamically display additional fields in the patient profile. For more guidance, see the ["How to add additional profile fields" guide](/guides/profile-additional-fields/).

Build a `PatientMetadataCreateFormEffect` with the [form fields](#formfield) to show, then return its `apply()` from a `PATIENT_METADATA__GET_ADDITIONAL_FIELDS` handler.

## Methods

### apply() → Effect

Displays the form fields in the patient profile.

- `form_fields` is required.
- `options` may only be set on fields whose `type` is `InputType.SELECT`.

## Attributes

| Attribute     | Type                              | Description     | Required |
|---------------|-----------------------------------|-----------------|----------|
| `form_fields` | `list[`[`FormField`](#formfield)`]` | List of fields. | Yes      |

## FormField

| Attribute  | Type        | Description                                                  |
|------------|-------------|--------------------------------------------------------------|
| `key`      | `str`       | Unique identifier of the field; the patient metadata key.    |
| `label`    | `str`       | The label displayed on the field.                            |
| `type`     | `InputType` | The type of the input: `TEXT`, `SELECT`, or `DATE`. Defaults to `TEXT`. |
| `required` | `bool`      | Whether the input is required. Defaults to `False`.          |
| `editable` | `bool`      | Whether the input can be edited. Defaults to `True`.         |
| `options`  | `list[str]` | Possible options when the input type is `SELECT`. Only allowed on `SELECT` fields. |

## Example

```python
from canvas_sdk.effects.patient_metadata import PatientMetadataCreateFormEffect, InputType, FormField

PatientMetadataCreateFormEffect(form_fields=[
    FormField(
        key='status',
        label='Status',
        type=InputType.SELECT,
        required=False,
        editable=True,
        options=["open", "close"]
    ),
]).apply()
```

<br/>
<br/>
<br/>
