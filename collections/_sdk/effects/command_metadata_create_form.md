---
title: "Command Metadata Create form"
slug: "command-metadata-create-form-effect"
excerpt: "Effect for dynamically displaying additional fields on a command"
hidden: false
---

The `CommandMetadataCreateFormEffect` allows developers to dynamically display additional fields with a command in a note. The values entered in these fields are stored as [command metadata](/sdk/data-command/#commandmetadata) against the target `command_uuid`.

Build a `CommandMetadataCreateFormEffect` with the [form fields](#formfield) to show, then return its `apply()` from a `COMMAND__FORM__GET_ADDITIONAL_FIELDS` handler.

## Methods

### apply() → Effect

Displays the form fields with the command.

- `command_uuid` and `form_fields` are required.
- `options` may only be set on fields whose `type` is `InputType.SELECT`; providing `options` on a `TEXT` or `DATE` field raises a validation error.
- Every `key` must be unique across `form_fields`. Duplicates raise a validation error per duplicated key.

## Attributes

| Attribute      | Type                                | Description                                                 | Required |
|----------------|-------------------------------------|-------------------------------------------------------------|----------|
| `command_uuid` | `str`                               | The id of the [command](/sdk/data-command/) these fields should be rendered on. | Yes      |
| `form_fields`  | `list[`[`FormField`](#formfield)`]` | List of fields.                                             | Yes      |

## FormField

| Attribute  | Type        | Description                                                  |
|------------|-------------|--------------------------------------------------------------|
| `key`      | `str`       | Unique identifier of the field; the command metadata key.    |
| `label`    | `str`       | The label displayed on the field.                            |
| `type`     | `InputType` | The type of the input: `TEXT`, `SELECT`, or `DATE`. Defaults to `TEXT`. |
| `required` | `bool`      | Whether the input is required. Defaults to `False`.          |
| `editable` | `bool`      | Whether the input can be edited. Defaults to `True`.         |
| `options`  | `list[str]` | Possible options when the input type is `SELECT`. Only allowed on `SELECT` fields. |
| `value`    | `str`       | Default value for the field. See [Default values](#default-values). |

## Example

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

## Default values

Set `value` on a `FormField` to give the field a default. When a command is originated, Canvas sends your handler a `COMMAND__FORM__GET_ADDITIONAL_FIELDS` event with the `purpose` `"form"` and saves each non-empty `value` in its response as command metadata for that key. The save happens before Canvas sends the `POST_COMMAND_ORIGINATE` event, so a handler for that event can read the defaults as [CommandMetadata](/sdk/data-command/#commandmetadata).

Once a key has a stored row, the stored value wins and `value` is ignored. This includes a value the user saves, even a cleared or empty one. If two plugins declare a default for the same key, Canvas saves only the first one it receives.

## Rendering on the printed note

The same `COMMAND__FORM__GET_ADDITIONAL_FIELDS` event fires when a command is rendered for printing (single-command print URL or full note printout). The platform uses the response to label and order the fields shown beneath each command in the printed output.

Two things differ from the chart-form render path:

- **Values come from stored command metadata, not from `FormField.value`.** The platform pairs each field declared in your effect with the matching `CommandMetadata` row by `key`. Whatever value is on `FormField` is ignored during print rendering. You do not need to populate `value` for print.
- **Fields with no stored value or a blank value are skipped.** Only fields with a stored value appear in the printout, including [defaults](#default-values) saved when the command was originated.
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
