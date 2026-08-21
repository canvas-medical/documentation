---
title: "DiagnosticView"
slug: "data-diagnostic-view"
excerpt: "Canvas SDK DiagnosticView"
hidden: false
---

## Introduction

The `DiagnosticView` model represents a saved combination of lab tests and questionnaire codes configured on your instance. A diagnostic view has no patient of its own — it is a reusable definition. When a diagnostic view is embedded in a note with the [Reference](/sdk/commands/#reference) command, Canvas renders that patient's results for the view's codes as a timeseries.

Diagnostic views are configured by an administrator, so the set available to a plugin is whatever your instance has defined.

## Basic usage

To get a diagnostic view by identifier, use the `get` method on the `DiagnosticView` model manager:

```python
from canvas_sdk.v1.data import DiagnosticView

view = DiagnosticView.objects.get(id="dca3a3c5-0a8e-4f7b-9c6a-1b9bf3a6e5e0")
```

To list every diagnostic view on the instance:

```python
from canvas_sdk.v1.data import DiagnosticView

views = DiagnosticView.objects.all()
```

## Filtering

Diagnostic views can be filtered by any attribute that exists on the model.

### By name

Names are set by whoever configured the view, so match on the exact name you expect and handle the case where it is absent:

```python
from canvas_sdk.v1.data import DiagnosticView

a1c_view = DiagnosticView.objects.filter(name="Hemoglobin A1c").first()
```

### By search tag

`tags` is a single free-text string of search terms, not a list, so use a substring match:

```python
from canvas_sdk.v1.data import DiagnosticView

diabetes_views = DiagnosticView.objects.filter(tags__icontains="diabetes")
```

## Embedding a view in a note

Pass the view's `id` to the [Reference](/sdk/commands/#reference) command:

```python
from canvas_sdk.commands import ReferenceCommand
from canvas_sdk.v1.data import DiagnosticView

def compute():
    a1c_view = DiagnosticView.objects.filter(name="Hemoglobin A1c").first()
    if not a1c_view:
        return []

    reference = ReferenceCommand(
        note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
        diagnostic_view_id=a1c_view.id,
    )

    return [reference.originate(commit=True)]
```

## Attributes

### DiagnosticView

| Field Name | Type                                                     |
|------------|----------------------------------------------------------|
| id         | UUID                                                     |
| dbid       | Integer                                                  |
| created    | DateTime                                                 |
| modified   | DateTime                                                 |
| name       | String (up to 100 characters)                            |
| tags       | String (up to 500 characters; free-text search terms)    |
| originator | [CanvasUser](/sdk/data-canvasuser)                       |
