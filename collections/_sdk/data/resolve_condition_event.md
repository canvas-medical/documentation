---
title: "Resolve Condition Event"
slug: "data-resolve-condition-event"
excerpt: "Canvas SDK Resolve Condition Event"
hidden: false
---

## Introduction

The `ResolveConditionEvent` model represents a record of a condition being resolved — the anchor for the `resolve_condition` command.

## Basic usage

To get a resolve condition event by identifier, use the `get` method on the `ResolveConditionEvent` model manager:

```python?partial=true
from canvas_sdk.v1.data import ResolveConditionEvent

resolution = ResolveConditionEvent.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
```

If you have a patient object, the resolve condition events for a patient can be accessed with the `resolved_conditions` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
resolutions = patient.resolved_conditions.all()
```

You can also access the resolved condition with the `condition` attribute:

```python?partial=true
from canvas_sdk.v1.data import ResolveConditionEvent

resolution = ResolveConditionEvent.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
condition = resolution.condition
```

Or for a given condition, you can access all of its resolutions with the `resolutions` attribute:

```python
from canvas_sdk.v1.data import Condition

condition = Condition.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
resolutions = condition.resolutions.all()
```

## Committed records

The `committed` method returns resolve condition events that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import ResolveConditionEvent

committed_resolutions = ResolveConditionEvent.objects.committed()
```

## Attributes

### ResolveConditionEvent

| Field Name             | Type                                  |
| ---------------------- | ------------------------------------- |
| id                     | UUID                                  |
| dbid                   | Integer                               |
| created                | DateTime                              |
| modified               | DateTime                              |
| originator             | [CanvasUser](/sdk/data-canvasuser)    |
| committer              | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error       | [CanvasUser](/sdk/data-canvasuser)    |
| patient                | [Patient](/sdk/data-patient/#patient) |
| note                   | [Note](/sdk/data-note)                |
| condition              | [Condition](/sdk/data-condition)      |
| rationale              | String                                |
| show_in_condition_list | Boolean                               |

<br/>
<br/>
<br/>
