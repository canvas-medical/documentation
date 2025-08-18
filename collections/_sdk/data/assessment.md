---
title: "Assessment"
slug: "data-assessment"
excerpt: "Canvas SDK Assessment"
hidden: false
---

## Introduction

The `Assessment` model represents a cClinical assessment or evaluation of a patient's medical `Condition`.

## Basic usage

To get an assessment by identifier, use the `get` method on the `Assessment` model manager:

```python
from canvas_sdk.v1.data.assessment import Assessment

assessment = Assessment.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the assessments for a patient can be accessed with the `assessments` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
assessments = patient.assessments.all()
```


## Filtering

Assessments can be filtered by any attribute that exists on the model.

Filtering for assessments is done with the `filter` method on the `Assessment` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.assessment import Assessment, AssessmentStatus

assessments = Assessment.objects.filter(patient__id="1eed3ea2a8d546a1b681a2a45de1d790", status=AssessmentStatus.STATUS_IMPROVING)
```

## Attributes

### Assessment

| Field Name       | Type                                            |
|------------------|-------------------------------------------------|
| id               | UUID                                            |
| dbid             | Integer                                         |
| created          | DateTime                                        |
| modified         | DateTime                                        |
| originator       | [CanvasUser](/sdk/data-canvasuser)              |                                                                            |
| deleted          | Boolean                                         |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)              |
| committer        | [CanvasUser](/sdk/data-canvasuser)              |
| patient          | [Patient](/sdk/data-patient/#patient)           |
| note             | [Note](/sdk/data-note/#note)                    |
| condition        | [Condition](/sdk/data-condition/#condition)     |
| interview        | [Interview](/sdk/data-questionnaire/#interview) |
| status           | [AssessmentStatus](#assessmentstatus)           |
| narrative        | String                                          |
| background       | String                                          |
| care_team        | String                                          |

## Enumeration types

### Assessment Status

| Value                | Label        |
|----------------------|--------------|
| STATUS_IMPROVING     | Improved     |
| STATUS_STABLE        | Unchanged    |
| STATUS_DETERIORATING | Deteriorated |


<br/>
<br/>
<br/>
