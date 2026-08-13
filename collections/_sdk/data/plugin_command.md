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

To find a registered command by the key declared in the manifest, filter on `command_key` — or on `schema_key`, which holds the same value:

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
- **command_key**: The command key declared in the plugin's manifest (e.g., `riskAssessment`). There is exactly one row per `command_key`: reinstalling or upgrading the plugin updates that row in place, so a command always carries its current `label` and `section`.
- **schema_key**: Always equal to `command_key`. It exists as its own field because chart command lines use the same name — see [`Command.schema_key`](/sdk/data-command/#command), which plugin authors query with `Command.objects.filter(schema_key="riskAssessment")`. Two installed plugins cannot declare the same key; the second install fails with a validation error.
- **label**: The user-friendly display label for the command (e.g., `Risk Assessment`).
- **section**: The chart section where the command appears: `subjective`, `objective`, `assessment`, `plan`, `procedures`, `history`, or `internal`.
- **plugin_name**: The name of the plugin that registered the command.

<br/>
<br/>
<br/>
