---
title: "Command Metadata Create form"
slug: "command-metadata-create-form-effect"
excerpt: "Effect for dynamically displaying additional fields on a command"
hidden: false
---

## Overview

The `CommandMetadataCreateFormEffect` allows developers to dynamically display additional fields with a command in a note. The values entered in these fields are stored as [command metadata](/sdk/data-command/#commandmetadata) against the target `command_uuid`.

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
        # Only respond for plan commands.
        if self.event.context.get("schema_key") != "plan":
            return []

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

Once the user fills out these fields, their values are persisted as command metadata and can be read back through the SDK [command metadata](/sdk/data-command/#commandmetadata) table.

## Rendering on the printed note

The same `COMMAND__FORM__GET_ADDITIONAL_FIELDS` event fires when a command is rendered for printing (single-command print URL or full note printout). The platform uses the response to label and order the fields shown beneath each command in the printed output.

Two things differ from the chart-form render path:

- **Values come from stored command metadata, not from `FormField.value`.** The platform pairs each field declared in your effect with the matching `CommandMetadata` row by `key`. Whatever value is on `FormField` is ignored during print rendering. You do not need to populate `value` for print.
- **Fields with no stored value or a blank value are skipped.** Only fields the user actually filled in will appear in the printout.
- **Fields you do not declare are hidden.** A `CommandMetadata` row whose `key` is not in your response will not print, even if it exists in the database. This matches the chart UI: removing or renaming a key in your effect makes the prior data invisible.

### Branching on `purpose`

The event context carries a `purpose` key indicating which call site triggered the request:

| Value     | When                                                          |
|-----------|---------------------------------------------------------------|
| `"form"`  | Chart UI is rendering the command's edit form (default).      |
| `"print"` | Single-command printout or note printout is being generated.  |

Read it from the handler context to vary your response — for example, to omit internal fields from print, or shorten labels for a denser layout.

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
        if self.event.context.get("schema_key") != "plan":
            return []

        is_print = self.event.context.get("purpose") == "print"

        fields = [
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
            ),
        ]

        if not is_print:
            # Internal-only: visible on the form, hidden from printouts.
            fields.append(
                FormField(
                    key="reviewer_notes",
                    label="Reviewer notes",
                    type=InputType.TEXT,
                )
            )

        return [
            CommandMetadataCreateFormEffect(
                command_uuid=self.event.target.id,
                form_fields=fields,
            ).apply()
        ]
```

### Tips for the print path

- **Use clear, human-readable `label` values.** Whatever you put on `FormField.label` is what the printed output shows. The platform does not derive a label from the `key`.
- **Use the same `key` you used when persisting metadata.** The print path joins on `key`; mismatches mean nothing renders for that field.
- **`type`, `options`, and `required` are ignored at print time.** Only `key` and `label` shape the printout.
- **Need to retire a field?** Removing it from the print response hides it for all future prints — including for committed notes. If you need the historical value to keep showing on signed records, keep the field declared (or declare it only when `purpose == "print"`).

<br/>
<br/>
<br/>
