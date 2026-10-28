---
title: "CommandTypeSetting"
slug: "data-command-type-setting"
excerpt: "Canvas SDK CommandTypeSetting"
hidden: false
---

## Introduction

The `CommandTypeSetting` model has one row for each command type available on the instance, with whether it is turned on. An administrator turns command types on and off in Canvas. Use it to leave out commands a provider cannot add, for example to skip suggesting a follow-up when the follow-up command is turned off.

A command type that isn't available on the instance has no row. Treat a missing row the same as a command type that is turned off.

## Basic usage

To check whether one command type is turned on, filter on its schema key and `active`:

```python
from canvas_sdk.v1.data import CommandTypeSetting

follow_up_on = CommandTypeSetting.objects.filter(schema_key="followUp", active=True).exists()
if follow_up_on:
    ...
```

The check returns `False` both when the command type is turned off and when it has no row. A `get` call for a schema key with no row raises `CommandTypeSetting.DoesNotExist`.

## Filtering

Command type settings can be filtered by any attribute that exists on the model.

### Active command types

To get the schema keys of every command type turned on for the instance, in one query:

```python
from canvas_sdk.v1.data import CommandTypeSetting

active = set(
    CommandTypeSetting.objects.filter(active=True).values_list("schema_key", flat=True)
)
```

## Attributes

### CommandTypeSetting

| Field Name | Type    |
|------------|---------|
| dbid       | Integer |
| schema_key | String  |
| active     | Boolean |

- **dbid**: The internal database primary key.
- **schema_key**: The command type's schema key, the same value as [`Command.schema_key`](/sdk/data-command/#command) (e.g., `followUp`, `refer`, `prescribe`).
- **active**: Whether the command type is turned on for the instance.

<br/>
<br/>
<br/>
