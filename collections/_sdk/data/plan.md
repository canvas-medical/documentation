---
title: "Plan"
slug: "data-plan"
excerpt: "Canvas SDK Plan"
hidden: false
---

## Introduction

The `Plan` model represents a Plan (plan of care) recorded on a Note, and is always associated with a Note and a Patient. It is the data model behind the `plan` command.

## Basic usage

To get a plan by identifier, use the `get` method on the `Plan` model manager:

```python?partial=true
from canvas_sdk.v1.data.plan import Plan

plan = Plan.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, or note object, the plans for a patient or note can be accessed with the `plans` attribute on a `Patient` or `Note` object:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.note import Note

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
plans = patient.plans.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
plans = note.plans.all()
```

## Reading the narrative

The plan text is exposed through the read-only `narrative` property:

```python?partial=true
from canvas_sdk.v1.data.plan import Plan

plan = Plan.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
text = plan.narrative
```

`narrative` returns the plan's text whether it was created before the Commands SDK (stored as plain text) or after (stored as structured content), so callers only read one field.

## Filtering

Plans can be filtered by any attribute that exists on the model.

### Committed plans

The `committed` method returns plans that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data.plan import Plan

committed_plans = Plan.objects.committed()
```

## Attributes

### Plan

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
| narrative        | String                                |

<br/>
<br/>
<br/>
