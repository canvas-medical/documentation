---
title: "How to add additional profile fields"
guide_for:
- /sdk/events/
- /sdk/effects/
---

This guide explains how to create additional fields that will appear on the patient profile demographics form. With this, you can define custom fields, and the information will be stored as patient metadata.

## What you'll learn:

- Use the [`PatientMetadataCreateForm`](/sdk/patient-metadata-create-form-effect) effect to display additional fields on the patient profile.
- Use the [`FormField`](/sdk/create-form-effect/#formfield) class to create fields

## Patient Metadata Create form plugin

#### 1. FormField

To create the form, we need to specify which items will be included. For this, we use the [`FormField`](/sdk/create-form-effect/#formfield) class, where we can define our inputs and their attributes.

```python
    FormField(
        key='musicGenre',
        label='Preferred music genre',
        type=InputType.TEXT,
        required=False,
        editable=True,
    ),
```

#### 2. PatientMetadataCreateFormEffect

The next step is to add these fields to the effect so they can be used to build the form.

```python
PatientMetadataCreateFormEffect(form_fields=[
    FormField(
        key='musicGenre',
        label='Preferred music genre',
        type=InputType.TEXT,
        required=False,
        editable=True,
    ),
    ...
]
```

#### 3. The plugin

Here’s an example of a complete plugin showcasing the different input types.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_metadata_create_form import PatientMetadataCreateFormEffect, InputType, FormField
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


# Inherit from BaseHandler to properly get registered for events
class Protocol(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_METADATA__GET_ADDITIONAL_FIELDS)

    def compute(self) -> list[Effect]:
        form = PatientMetadataCreateFormEffect(form_fields=[
            FormField(
                key='musicGenre',
                label='Preferred music genre',
                type=InputType.TEXT,
                required=False,
                editable=True,
            ),
            FormField(
                key='occupation',
                label='Occupation',
                type=InputType.SELECT,
                required=False,
                editable=True,
                options=["Engineer", "Teacher", "Other"]
            ),
            FormField(
                key='date',
                label='Date',
                type=InputType.DATE,
                required=False,
                editable=True,
            ),
        ])

        return [form.apply()]

```

#### 4. The Output

And that’s it! Below, you can see how it will appear in the app — these fields will be stored as patient metadata.

<div style="max-width: 100%"><img style="max-width: 100%" src="/assets/images/additional-fields.png" alt="medication widget" /></div>
