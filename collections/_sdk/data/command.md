---
title: "Command"
slug: "data-command"
excerpt: "Canvas SDK Command"
hidden: false
---

## Introduction

The `Command` model represents a [command](/sdk/commands/) in a note.

## Basic usage

To get a command by identifier, use the `get` method on the `Command` model manager:

```python
from canvas_sdk.v1.data.command import Command

command = Command.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

## Filtering

Commands can be filtered by any attribute that exists on the model.

Filtering for commands is done with the `filter` method on the `Command` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.command import Command

commands = Command.objects.filter(state="committed")
```

## Attributes

### Command
| Field Name         | Type                                  |
|--------------------|---------------------------------------|
| id                 | UUID                                  |
| dbid               | Integer                               |
| created            | DateTime                              |
| modified           | DateTime                              |
| originator         | CanvasUser                            |
| committer          | CanvasUser                            |
| entered_in_error   | CanvasUser                            |
| state              | String                                |
| patient            | [Patient](/sdk/data-patient/#patient) |
| note_id            | Integer                               |
| schema_key         | Text                                  |
| data               | JSON                                  |
| origination_source | String                                |
