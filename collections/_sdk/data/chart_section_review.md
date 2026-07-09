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

### Committed reviews

The `committed` method returns chart section reviews that have been committed and not entered in error:

```python
from canvas_sdk.v1.data.chart_section_review import ChartSectionReview

committed_reviews = ChartSectionReview.objects.committed()
```

## Working with entries

`entries` is a list of integer `dbid` values identifying the records that were reviewed in the section. Which model those `dbid`s belong to depends on the review's `section`:

| `section`          | Model(s) referenced by `entries`             |
|--------------------|----------------------------------------------|
| `conditions`       | [Condition](/sdk/data-condition/) (non-surgical) |
| `surgical_history` | [Condition](/sdk/data-condition/) (surgical) |
| `medications`      | [Medication](/sdk/data-medication/)          |
| `family_histories` | `FamilyHistory` (not currently exposed in the SDK data module) |
| `allergies`        | [AllergyIntolerance](/sdk/data-allergy-intolerance/) |
| `immunizations`    | [Immunization](/sdk/data-immunization/) and [ImmunizationStatement](/sdk/data-immunization/) |

If you only need to **see what was reviewed**, prefer the `content` field: it holds the pre-rendered text of the reviewed records (one line per entry, captured at review time), so it needs no entry resolution and avoids the ambiguity described below.

To work with the **record objects themselves**, filter the corresponding model by `dbid__in=review.entries`. Always scope the query to `review.patient` as well: a `dbid` is unique only within its own table, so scoping by patient avoids matching an unrelated record that happens to share the same integer (this is also why the `immunizations` section, which draws from two models, is resolved against both).

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance
from canvas_sdk.v1.data.chart_section_review import (
    ChartSectionReview,
    ChartSectionReviewSection,
)
from canvas_sdk.v1.data.condition import Condition
from canvas_sdk.v1.data.immunization import Immunization, ImmunizationStatement
from canvas_sdk.v1.data.medication import Medication

review = ChartSectionReview.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")

if review.section == ChartSectionReviewSection.CONDITIONS:
    records = Condition.objects.filter(
        patient=review.patient, dbid__in=review.entries, surgical=False
    )
elif review.section == ChartSectionReviewSection.SURGICAL_HISTORY:
    records = Condition.objects.filter(
        patient=review.patient, dbid__in=review.entries, surgical=True
    )
elif review.section == ChartSectionReviewSection.MEDICATIONS:
    records = Medication.objects.filter(patient=review.patient, dbid__in=review.entries)
elif review.section == ChartSectionReviewSection.ALLERGIES:
    records = AllergyIntolerance.objects.filter(patient=review.patient, dbid__in=review.entries)
elif review.section == ChartSectionReviewSection.IMMUNIZATIONS:
    # entries may reference either model, so resolve against both.
    records = [
        *Immunization.objects.filter(patient=review.patient, dbid__in=review.entries),
        *ImmunizationStatement.objects.filter(patient=review.patient, dbid__in=review.entries),
    ]
```

> **Note on the `immunizations` section:** `entries` stores bare `dbid` integers with no indication of which model each one came from. Because `Immunization` and `ImmunizationStatement` are separate tables with independent `dbid` sequences, the same integer can be a valid `dbid` in both. If a patient has an `Immunization` and an `ImmunizationStatement` that share a `dbid` and only one was reviewed, resolving against both models (as above) will return both records — there is no way to disambiguate them from `entries` alone. Treat the immunizations result as a best-effort superset, not an exact match. If you only need to know what was reviewed, use `content` instead: it captured the rendered text of the actual reviewed items at review time.

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
| entries    | Integer[] (`dbid`s of the reviewed records — see [Working with entries](#working-with-entries)) |
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

