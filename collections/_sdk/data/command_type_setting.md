---
title: "CommandTypeSetting"
slug: "data-command-type-setting"
excerpt: "Canvas SDK CommandTypeSetting"
hidden: false
---

## Introduction

The `CommandTypeSetting` model records whether each command type is turned on for the Canvas instance. Use it to check which command types are available before your plugin suggests or creates commands, so it doesn't offer one the instance has turned off.

Each record identifies a command type by its `schema_key`, the same value the [Command](/sdk/data-command/#command-types-and-data) model's `schema_key` field holds, such as `followUp` or `refer`. The model is read-only.

## Basic usage

To get the schema keys of every command type that is turned on, filter on `active`:

```python
from canvas_sdk.v1.data import CommandTypeSetting

active_schema_keys = CommandTypeSetting.objects.filter(active=True).values_list("schema_key", flat=True)
```

To check a single command type, filter on its `schema_key`:

```python
from canvas_sdk.v1.data import CommandTypeSetting

referrals_on = CommandTypeSetting.objects.filter(schema_key="refer", active=True).exists()
```

## Attributes

### CommandTypeSetting

| Field Name | Type    | Description                                                     |
|------------|---------|-----------------------------------------------------------------|
| dbid       | Integer | The record's database identifier.                               |
| schema_key | String  | The command type's schema key, such as `followUp` or `refer`.   |
| active     | Boolean | Whether the command type is turned on for the instance.         |

`CommandTypeSetting` has no `id` field. Use `dbid` or `schema_key` to identify a record.
