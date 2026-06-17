---
title: "ChartSectionReview"
slug: "data-chart-section-review"
excerpt: "Canvas SDK ChartSectionReview"
hidden: false
---

## Introduction

The `ChartSectionReview` model represents a reviewed chart section captured on a note, with its pre-rendered content. When a provider reviews a chart section during a visit, Canvas stores a snapshot of that section's content at the time of review.

## Basic usage

To get a chart section review by identifier, use the `get` method on the `ChartSectionReview` model manager:

```python
from canvas_sdk.v1.data.chart_section_review import ChartSectionReview

review = ChartSectionReview.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")
```

If you have a patient object, the chart section reviews for a patient can be accessed with the `chart_section_reviews` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
reviews = patient.chart_section_reviews.all()
```

If you have a note object, the chart section reviews for that note can be accessed with the `chart_section_reviews` attribute on a `Note` object:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
reviews = note.chart_section_reviews.all()
```

## Filtering

Chart section reviews can be filtered by any attribute that exists on the model.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.chart_section_review import (
    ChartSectionReview,
    ChartSectionReviewSection,
)

# Get all reviews for the conditions section
condition_reviews = ChartSectionReview.objects.filter(
    section=ChartSectionReviewSection.CONDITIONS
)
```

### By patient and section

```python
from canvas_sdk.v1.data.chart_section_review import (
    ChartSectionReview,
    ChartSectionReviewSection,
)
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
medication_reviews = ChartSectionReview.objects.filter(
    patient=patient,
    section=ChartSectionReviewSection.MEDICATIONS
)
```

## Attributes

### ChartSectionReview

| Field Name | Type                                                      |
|------------|-----------------------------------------------------------|
| id         | UUID                                                      |
| dbid       | Integer                                                   |
| created    | DateTime                                                  |
| modified   | DateTime                                                  |
| deleted    | Boolean                                                   |
| patient    | [Patient](/sdk/data-patient/#patient)                     |
| note       | [Note](/sdk/data-note/#note)                              |
| section    | [ChartSectionReviewSection](#chartsectionreviewsection)   |
| entries    | Integer[] (array of entry IDs)                            |
| content    | String (newline-separated bullet items)                   |

## Enumeration types

### ChartSectionReviewSection

| Value            | Label            |
|------------------|------------------|
| conditions       | Conditions       |
| surgical_history | Surgical History |
| medications      | Medications      |
| family_histories | Family Histories |
| allergies        | Allergies        |
| immunizations    | Immunizations    |

