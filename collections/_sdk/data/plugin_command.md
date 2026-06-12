---
title: "PluginCommand"
slug: "data-plugin-command"
excerpt: "Canvas SDK PluginCommand"
hidden: false
---

## Introduction

The `PluginCommand` model provides read-only access to custom commands registered by plugins in `CANVAS_MANIFEST.json`. Use this model to retrieve command metadata such as `label` and `section` values instead of reconstructing display text from the camelCase `schema_key`.

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

### By schema key

To find a specific registered command by its schema key:

```python
from canvas_sdk.v1.data.plugin_command import PluginCommand

plugin_command = PluginCommand.objects.filter(schema_key="riskAssessment").first()
if plugin_command:
    print(f"Label: {plugin_command.label}")
    print(f"Section: {plugin_command.section}")
```

## Attributes

### PluginCommand

| Field Name | Type    |
|------------|---------|
| id         | UUID    |
| dbid       | Integer |
| name       | String  |
| schema_key | String  |
| label      | String  |
| section    | String  |

- **id**: The unique UUID identifier for the plugin command.
- **dbid**: The internal database primary key.
- **name**: The registered class name of the command (e.g., `RiskAssessment`).
- **schema_key**: The unique identifier for the command, as declared in the manifest (e.g., `riskAssessment`).
- **label**: The user-friendly display label for the command (e.g., `Risk Assessment`).
- **section**: The chart section where the command appears: `subjective`, `objective`, `assessment`, `plan`, `procedures`, `history`, or `internal`.

<br/>
<br/>
<br/>
