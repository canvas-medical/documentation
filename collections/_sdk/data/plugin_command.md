---
title: "PluginCommand"
slug: "data-plugin-command"
excerpt: "Canvas SDK PluginCommand"
hidden: false
---

## Introduction

The `PluginCommand` model provides read-only access to the custom commands a plugin registers in its `CANVAS_MANIFEST.json`. Use it to read back a registered command's `label` and `section` instead of reconstructing display text from its camelCase `command_key`.

## Basic usage

To get a plugin command by identifier, use the `get` method on the `PluginCommand` model manager:

```python
from canvas_sdk.v1.data.plugin_command import PluginCommand

plugin_command = PluginCommand.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

## Filtering

Plugin commands can be filtered by any attribute that exists on the model.

Filtering for plugin commands is done with the `filter` method on the `PluginCommand` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.plugin_command import PluginCommand

# Find all plugin commands in a specific chart section
plugin_commands = PluginCommand.objects.filter(section="assessment")
```

### By command key

To find a registered command by the `schema_key` declared in the manifest, filter on `command_key`:

```python
from canvas_sdk.v1.data.plugin_command import PluginCommand

plugin_command = PluginCommand.objects.filter(command_key="riskAssessment").first()
if plugin_command:
    print(f"Label: {plugin_command.label}")
    print(f"Section: {plugin_command.section}")
```

## Attributes

### PluginCommand

| Field Name  | Type    |
|-------------|---------|
| id          | UUID    |
| dbid        | Integer |
| name        | String  |
| command_key | String  |
| schema_key  | String  |
| label       | String  |
| section     | String  |
| plugin_name | String  |

- **id**: The unique UUID identifier for the plugin command.
- **dbid**: The internal database primary key.
- **name**: The registered name of the command (e.g., `RiskAssessment`).
- **command_key**: The command key declared in the plugin's manifest (e.g., `riskAssessment`). This identifies the logical command; multiple rows can share a `command_key`, one per content version.
- **schema_key**: The content-versioned identifier for this row, derived from the `command_key` and a hash of the command's `label` and `section`. Changing a command's label or section produces a new `schema_key` and a new row. This identifier is internal to the `PluginCommand` table; chart command lines store the bare `command_key` instead (see [`Command.schema_key`](/sdk/data-command/#command)), so a command always renders with its current label, and plugin authors query chart commands by the manifest key with `Command.objects.filter(schema_key="riskAssessment")`.
- **label**: The user-friendly display label for the command (e.g., `Risk Assessment`).
- **section**: The chart section where the command appears: `subjective`, `objective`, `assessment`, `plan`, `procedures`, `history`, or `internal`.
- **plugin_name**: The name of the plugin that registered the command.

<br/>
<br/>
<br/>
