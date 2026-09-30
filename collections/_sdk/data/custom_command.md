---
title: "CustomCommand"
slug: "data-custom-command"
excerpt: "Canvas SDK CustomCommand"
hidden: false
---

## Introduction

The `CustomCommand` model is the anchor for a [custom command](/sdk/commands-custom-command/): the plugin-defined, read-only HTML content a plugin inserts into a note. Use this data model to read back the custom commands recorded on a chart. To insert one, use the [Custom Command](/sdk/commands-custom-command/) command class instead.

## Basic usage

To get a custom command by identifier, use the `get` method on the `CustomCommand` model manager:

```python?partial=true
from canvas_sdk.v1.data import CustomCommand

custom_command = CustomCommand.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the custom commands for a patient can be accessed with the `custom_commands` attribute:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
custom_commands = patient.custom_commands.all()
```

The custom commands recorded on a note are reachable the same way, through the note's `custom_commands` attribute:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
custom_commands = note.custom_commands.all()
```

## Committed records

The `committed` method returns custom commands that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import CustomCommand

committed_commands = CustomCommand.objects.committed()
```

## Resolving the plugin registration

The `plugin_command` property returns the [`PluginCommand`](/sdk/data-plugin-command/) registration the command was created from, resolved through the anchoring command's `schema_key`. It is `None` when the anchor has no command, or when its `schema_key` is not a registered plugin command:

```python?partial=true
custom_command = CustomCommand.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

plugin_command = custom_command.plugin_command
if plugin_command:
    print(plugin_command.label)
```

## Reading the command data

The `data` property returns the anchoring [`Command`](/sdk/data-command/)'s `data`, a dictionary of the command's stored field values. It is `None` when there is no anchoring command:

```python?partial=true
custom_command = CustomCommand.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

data = custom_command.data
```

## Attributes

### CustomCommand

| Field Name       | Type                                  |
| ---------------- | ------------------------------------- |
| id               | UUID                                  |
| dbid             | Integer                               |
| created          | DateTime                              |
| modified         | DateTime                              |
| originator       | [CanvasUser](/sdk/data-canvasuser)    |
| committer        | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)    |
| patient          | [Patient](/sdk/data-patient/#patient) |
| note             | [Note](/sdk/data-note)                |
| plugin_command   | [PluginCommand](/sdk/data-plugin-command/) |
| data             | JSON                                  |

<br/>
<br/>
<br/>
