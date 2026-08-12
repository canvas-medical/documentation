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

## Delegations

A document review can be delegated to another staff member or team. The delegations for a document are available through two accessors:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument

document = UncategorizedClinicalDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

# The full delegation history, oldest first.
history = document.delegations

# The current active delegation, or None when the document is with its owner.
current = document.active_delegation
```

See [DocumentReviewDelegation](/sdk/data-document-review-delegation/) for the delegation model and the `DOCUMENT_DELEGATED` event.

## Document codings

The `code` field comes from the document's type, which is drawn from a fixed list rather than set freely — either the type selected in Data Integration, or, when a document is created through the FHIR [DocumentReference](/api/documentreference/) endpoint, the LOINC code supplied in `type.coding`, which must match one of the codes below. Every coding uses the LOINC system (`http://loinc.org`). The document types stored as uncategorized clinical documents are:

| Document type                  | Code    | Display                                       |
|--------------------------------|---------|-----------------------------------------------|
| Care Management Documents      | 91983-7 | Care management note                          |
| Clinical Patient Intake Form   | 64285-0 | Medical history screening form                |
| Emergency Department Report    | 96335-5 | Emergency department Summary note             |
| External Medical Records       | 11503-0 | Medical records                               |
| Home Care Report               | 75503-3 | Patient’s home Note                           |
| Hospital Discharge Summary     | 34105-7 | Hospital Discharge summary                    |
| Hospital History and Physical  | 47039-3 | Hospital Admission history and physical note  |
| Nursing Home                   | 34113-1 | Nursing facility Note                         |
| Operative Report               | 11504-8 | Surgical operation note                       |
| Physical Exam Documents        | 51848-0 | Evaluation note                               |
| Prescription Refill Request    | 57833-6 | Prescription for medication                   |
| Rehabilitation Report          | 34823-5 | Physical medicine and rehab Note              |
| Uncategorized Clinical Document | 34109-9 | Note                                         |
| In Office Testing Documents    | —       | none                                          |

{% include alert.html type="warning" content="In Office Testing Documents have no coding assigned, so their <code>code</code> is <code>None</code>. Filtering on <code>code</code> silently excludes them, and because the FHIR endpoint identifies a document's type by its LOINC code, they can only be created through Data Integration." %}

Administrative document types are stored as [PatientAdministrativeDocument](/sdk/data-patient-administrative-document/) instead. Lab reports, imaging reports and specialist consult reports have their own models, so their codings never appear here.

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
| code               | [DocumentCoding](/sdk/data-patient-administrative-document/#documentcoding) |
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
| committer                    | [CanvasUser](/sdk/data-canvasuser)     |
| entered_in_error             | [CanvasUser](/sdk/data-canvasuser)     |
| internal_comment             | String                                 |
| message_to_patient           | String                                 |
| status                       | String                                 |
| patient                      | [Patient](/sdk/data-patient/#patient)  |
| patient_communication_method | String                                 |
| reports                      | QuerySet[[UncategorizedClinicalDocument](#uncategorizedclinicaldocument)] |
