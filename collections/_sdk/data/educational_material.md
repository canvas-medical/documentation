---
title: "EducationalMaterial"
slug: "data-educational-material"
excerpt: "Patient educational material shared from a note via the Educational Material command."
hidden: false
---

# EducationalMaterial

The `EducationalMaterial` model represents patient educational material recorded on a note through the Educational Material command — the selected article, its title and abstract, and the languages it is available in.

## Basic Usage

`EducationalMaterial` records can be retrieved by their UUID `id`, their integer `dbid`, or through a patient.

```python
from canvas_sdk.v1.data import EducationalMaterial

# Get all educational material records
materials = EducationalMaterial.objects.all()

# Get a specific record by its UUID id
material = EducationalMaterial.objects.get(id="c9a7b1e2d4f34e6a8b5c0d1e2f3a4b5c")
```

If you have a `Patient` object, its educational material records can be accessed with the `educational_materials` reverse relation:

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
materials = patient.educational_materials.all()
```

## Filtering

### By attribute

```python
from canvas_sdk.v1.data import EducationalMaterial

materials = EducationalMaterial.objects.filter(selected_language="en-us")
```

### Committed records

The `committed` method returns records that have been committed and not entered in error:

```python
from canvas_sdk.v1.data import EducationalMaterial

committed = EducationalMaterial.objects.committed()
```

## Attributes

### EducationalMaterial

| Field Name        | Type                                  |
|-------------------|---------------------------------------|
| id                | UUID                                  |
| dbid              | Integer                               |
| created           | DateTime                              |
| modified          | DateTime                              |
| originator        | [CanvasUser](/sdk/data-canvasuser)    |
| committer         | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error  | [CanvasUser](/sdk/data-canvasuser)    |
| patient           | [Patient](/sdk/data-patient/#patient) |
| note              | [Note](/sdk/data-note/#note)          |
| article_id        | String                                |
| selected_language | String                                |
| title             | String                                |
| languages         | String[]                              |
| abstract          | String                                |
