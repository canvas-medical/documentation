---
title: "CommandTypeSetting"
slug: "data-command-type-setting"
excerpt: "Canvas SDK CommandTypeSetting"
hidden: false
---

## Introduction

The `CommandTypeSetting` model holds one row per command type and whether it is turned on for the instance. An administrator turns command types on and off in Canvas. Use it to leave out commands a provider cannot add, for example to skip suggesting a follow-up when the follow-up command is turned off.

## Basic usage

To read whether one command type is turned on, use the `get` method on the `CommandTypeSetting` model manager with its schema key:

```python
from canvas_sdk.v1.data import CommandTypeSetting

follow_up = CommandTypeSetting.objects.get(schema_key="followUp")
if follow_up.active:
    ...
```

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
