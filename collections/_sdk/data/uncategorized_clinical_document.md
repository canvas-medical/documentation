---
title: "Uncategorized Clinical Document"
slug: "data-uncategorized-clinical-document"
excerpt: "Canvas SDK Uncategorized Clinical Document"
hidden: false
---

## Introduction

The `UncategorizedClinicalDocument` and `UncategorizedClinicalDocumentReview` models represent uncategorized clinical documents and their reviews.

## Basic Usage

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument, UncategorizedClinicalDocumentReview

document = UncategorizedClinicalDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
review = UncategorizedClinicalDocumentReview.objects.get(id="c1a5a35a-4ee2-4a0e-85c0-21739dc8c4a8")
```

## Filtering

Uncategorized clinical documents and reviews can be filtered by any attribute that exists on the models.

### By review mode

Filter documents by their review mode:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument
from canvas_sdk.commands.commands.review import ReviewMode

documents_to_review = UncategorizedClinicalDocument.objects.filter(review_mode=ReviewMode.REVIEW_REQUIRED)
```

### Unreviewed documents

To get uncategorized documents that have not been reviewed yet and require a review:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument
from canvas_sdk.commands.commands.review import ReviewMode
from django.db.models import Q

unreviewed_documents = UncategorizedClinicalDocument.objects.filter(Q(review_mode=ReviewMode.REVIEW_REQUIRED), (Q(review__committer__isnull=True) | Q(review__entered_in_error__isnull=False)))

```

## Attributes

### UncategorizedClinicalDocument

| Field Name         | Type                                                                        |
|--------------------|-----------------------------------------------------------------------------|
| id                 | UUID                                                                        |
| dbid               | Integer                                                                     |
| created            | DateTime                                                                    |
| modified           | DateTime                                                                    |
| patient            | [Patient](/sdk/data-patient/#patient)                                       |
| originator         | [CanvasUser](/sdk/data-canvasuser)                                          |
| assigned_by        | [CanvasUser](/sdk/data-canvasuser)                                          |
| review             | [UncategorizedClinicalDocumentReview](#uncategorizedclinicaldocumentreview) |
| team               | [Team](/sdk/data-team/#team)                                                |
| name               | String                                                                      |
| review_mode        | [DocumentReviewMode](/sdk/data-enumeration-types/#documentreviewmode)       |
| junked             | Boolean                                                                     |
| requires_signature | Boolean                                                                     |
| assigned_date      | DateTime                                                                    |
| team_assigned_date | DateTime                                                                    |
| original_date      | Date                                                                        |
| comment            | String                                                                      |
| priority           | Boolean                                                                     |

### UncategorizedClinicalDocumentReview

| Field Name                   | Type                                   |
|------------------------------|----------------------------------------|
| id                           | UUID                                   |
| dbid                         | Integer                                |
| created                      | DateTime                               |
| modified                     | DateTime                               |
| originator                   | [CanvasUser](/sdk/data-canvasuser)     |
| deleted                      | Boolean                                |
| committer                    | [CanvasUser](/sdk/data-canvasuser)     |
| entered_in_error             | [CanvasUser](/sdk/data-canvasuser)     |
| internal_comment             | String                                 |
| message_to_patient           | String                                 |
| status                       | String                                 |
| patient                      | [Patient](/sdk/data-patient/#patient)  |
| patient_communication_method | String                                 |
