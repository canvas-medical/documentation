---
title: "VisualExamFinding"
slug: "data-visual-exam-finding"
excerpt: "Canvas SDK VisualExamFinding"
hidden: false
---

## Introduction

The `VisualExamFinding` model represents a visual exam finding captured on a note. Each finding consists of a titled image along with a narrative description of the clinical observation.

## Basic usage

To get a visual exam finding by identifier, use the `get` method on the `VisualExamFinding` model manager:

```python
from canvas_sdk.v1.data.visual_exam_finding import VisualExamFinding

finding = VisualExamFinding.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the visual exam findings for a patient can be accessed with the `visual_exam_findings` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
findings = patient.visual_exam_findings.all()
```

If you have a note object, the visual exam findings for that note can be accessed with the `visual_exam_findings` attribute on a `Note` object:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
findings = note.visual_exam_findings.all()
```

## Accessing image files

The `image_url` property returns a presigned S3 URL for securely accessing the image file. The URL is valid for 1 hour.

```python
from canvas_sdk.v1.data.visual_exam_finding import VisualExamFinding

finding = VisualExamFinding.objects.exclude(image="").first()

# Returns a presigned S3 URL (valid for 1 hour), or None if no image is set
url = finding.image_url
```

## Filtering

Visual exam findings can be filtered by any attribute that exists on the model.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.visual_exam_finding import VisualExamFinding

# Get all findings with a specific title
findings = VisualExamFinding.objects.filter(title="Left forearm")
```

### By patient

```python
from canvas_sdk.v1.data.visual_exam_finding import VisualExamFinding
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
findings = VisualExamFinding.objects.filter(patient=patient)
```

## Attributes

### VisualExamFinding

| Field Name | Type                                  |
|------------|---------------------------------------|
| id         | UUID                                  |
| dbid       | Integer                               |
| created    | DateTime                              |
| modified   | DateTime                              |
| patient    | [Patient](/sdk/data-patient/#patient) |
| note       | [Note](/sdk/data-note/#note)          |
| image      | String (S3 key)                       |
| title      | String                                |
| narrative  | String                                |
| image_url  | String (property) — presigned S3 URL  |

