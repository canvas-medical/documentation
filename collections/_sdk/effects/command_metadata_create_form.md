---
title: "Command Metadata Create form"
slug: "command-metadata-create-form-effect"
excerpt: "Effect for dynamically displaying additional fields on a command"
hidden: false
---

## Overview

This allows developers to dynamically display additional fields on a command. The values entered in these fields are stored as [command metadata](/sdk/data-command/#commandmetadata) against the target `command_uuid`.

The effect is returned from a handler that responds to the `COMMAND__FORM__GET_ADDITIONAL_FIELDS` event.

```python
from canvas_sdk.effects.command_metadata import (
    CommandMetadataCreateFormEffect,
    FormField,
    InputType,
)

CommandMetadataCreateFormEffect(
    command_uuid="command-uuid",
    form_fields=[
        FormField(
            key="reason",
            label="Reason",
            type=InputType.SELECT,
            options=["Routine", "Follow-up", "Other"],
        ),
    ],
)
```

## Structure

### **FormField**

A FormField consists of the following properties:

#### Attributes

| Attribute          | Type                 | Description                                                       |
|--------------------|----------------------|-------------------------------------------------------------------|
| `key`              | `str`                | unique identifier of the field - command metadata key             |
| `label`            | `str`                | the label that will be displayed on the field                     |
| `type`             | `InputType`          | the type of the input - TEXT, SELECT, DATE.                       |
| `required`         | `bool`               | if the input is required.                                         |
| `editable`         | `bool`               | if the input can be editabled.                                    |
| `options`          | `list[str]`          | possible options for when the input type is set to "SELECT”       |
| `value`            | `str`                | default value for the field                                       |


### **CommandMetadataCreateFormEffect**

A CommandMetadataCreateFormEffect consists of the following properties:

#### Attributes

| Attribute          | Type              | Description                                                       |
|--------------------|-------------------|-------------------------------------------------------------------|
| `command_uuid`     | `str`             | the UUID of the command these fields should be rendered on.       |
| `form_fields`      | `list[FormField]` | list of fields.                                                   |

## Validation

The effect validates inputs before it is applied:

- `command_uuid` is required.
- `options` may only be set on fields whose `type` is `InputType.SELECT`; providing `options` on a `TEXT` or `DATE` field raises a validation error.
- Every `key` must be unique across `form_fields`. Duplicates raise a validation error per duplicated key.

## Example Usage

The following handler declares two extra fields on every plan command when the platform requests additional fields for it:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.command_metadata import (
    CommandMetadataCreateFormEffect,
    FormField,
    InputType,
)
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class PlanCommandAdditionalFields(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.COMMAND__FORM__GET_ADDITIONAL_FIELDS)

    def compute(self) -> list[Effect]:
        form = CommandMetadataCreateFormEffect(
            command_uuid=self.event.target.id,
            form_fields=[
                FormField(
                    key="priority",
                    label="Priority",
                    type=InputType.SELECT,
                    options=["low", "medium", "high"],
                ),
                FormField(
                    key="follow_up_date",
                    label="Follow-up date",
                    type=InputType.DATE,
                    editable=True,
                ),
            ],
        )

        return [form.apply()]
```

Once the user fills out these fields, their values are persisted as command metadata and can be read back using the standard [command metadata](/sdk/data-command/#commandmetadata) APIs.

<br/>
<br/>
<br/>
