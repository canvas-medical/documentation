---
title: "Document Review Delegation"
slug: "data-document-review-delegation"
excerpt: "Canvas SDK Document Review Delegation"
hidden: false
---

## Introduction

The `DocumentReviewDelegation` model records a signature release on a reviewable document. A staff member can select **Release my signature** when reassigning a Lab, Imaging, Consult/Referral, or Uncategorized review. Canvas then stores a delegation that lets the recipients apply the releaser's signature while annotating the document. The recipients can be a staff member, a team, or both. Only staff with a provider or licensed role type can release their signature.

A reassign without a release writes no delegation. It also ends any active release on the document, so a release reaches only its direct recipients. Each document has at most one **active** delegation (`is_active`). Earlier delegations stay in the table as inactive rows.

`on_behalf_of` identifies the staff member whose signature the recipients may apply. To see the full reassignment and comment timeline for a document, use [DocumentHistoryEvent](/sdk/data-document-history-event/).

## Basic usage

To get a delegation by identifier, use the `get` method on the `DocumentReviewDelegation` model manager:

```python
from canvas_sdk.v1.data import DocumentReviewDelegation

delegation = DocumentReviewDelegation.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")
```

If you have an [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/), its delegations are available through the `delegations` and `active_delegation` accessors. For other document types, filter by `content_type` and `object_id`, as described in [The delegated document](#the-delegated-document).

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument

document = UncategorizedClinicalDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

# The full delegation history, oldest first.
history = document.delegations

# The active delegation, or None when no signature is currently released.
current = document.active_delegation
if current and current.signature_consent:
    signer = current.on_behalf_of  # whose signature the recipients may apply
```

## Filtering

Delegations can be filtered by any attribute that exists on the model.

### Active delegations

```python
from canvas_sdk.v1.data import DocumentReviewDelegation

active = DocumentReviewDelegation.objects.filter(is_active=True)
```

### Delegations that granted signature consent

```python
from canvas_sdk.v1.data import DocumentReviewDelegation

with_consent = DocumentReviewDelegation.objects.filter(is_active=True, signature_consent=True)
```

## Attributes

### DocumentReviewDelegation

| Field Name         | Type                                                             |
|--------------------|-----------------------------------------------------------------|
| id                 | UUID                                                            |
| dbid               | Integer                                                         |
| created            | DateTime                                                        |
| modified           | DateTime                                                        |
| content_type       | [ContentType](/sdk/data-content-type/) (the document's type)    |
| object_id          | Integer (the document's `dbid`)                                 |
| delegated_by       | [Staff](/sdk/data-staff/#staff) (who released their signature)  |
| delegated_to_staff | [Staff](/sdk/data-staff/#staff) (recipient staff member, if any) |
| delegated_to_team  | [Team](/sdk/data-team/#team) (recipient team, if any)           |
| on_behalf_of       | [Staff](/sdk/data-staff/#staff) (whose signature was released)  |
| signature_consent  | Boolean (may the recipients apply the released signature)       |
| comment            | String (the comment left with the reassignment)                 |
| is_active          | Boolean (the release is still in effect)                        |

## The delegated document

`content_type` and `object_id` form a generic link to the document the signature was released on: `content_type` identifies the linked model, and `object_id` is that record's `dbid`. A delegation can point at any of the four reviewable document types:

| Document | `content_type.app_label` | `content_type.model` |
|----------|--------------------------|----------------------|
| [LabReport](/sdk/data-labs/#labreport) | `api` | `labreport` |
| [ImagingReport](/sdk/data-imaging/#imagingreport) | `api` | `imagingreport` |
| [ReferralReport](/sdk/data-referral/#referralreport) | `api` | `referralreport` |
| [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/) | `api` | `uncategorizedclinicaldocument` |

An [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/) exposes its delegations directly through its `delegations` and `active_delegation` accessors:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument

document = UncategorizedClinicalDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

current = document.active_delegation   # the active DocumentReviewDelegation, or None
history = document.delegations         # every delegation recorded for the document
```

For the other document types, resolve the [ContentType](/sdk/data-content-type/) at runtime from its stable `app_label` and `model`, and filter by the report's `dbid`. Never hardcode the content type `dbid`, which differs per environment:

```python
from canvas_sdk.v1.data import ContentType, DocumentReviewDelegation, LabReport

lab_report = LabReport.objects.get(id="7c9e6679-7425-40de-944b-e07fc1f90ae7")
lab_report_ct = ContentType.objects.get(app_label="api", model="labreport")

active_release = DocumentReviewDelegation.objects.filter(
    content_type=lab_report_ct, object_id=lab_report.dbid, is_active=True
).first()
```

To go the other way, from a delegation to its document, read `content_type` to learn which model `object_id` refers to, then resolve it:

```python
from canvas_sdk.v1.data import DocumentReviewDelegation, ImagingReport, LabReport, ReferralReport, UncategorizedClinicalDocument

DOCUMENT_MODELS = {
    "labreport": LabReport,
    "imagingreport": ImagingReport,
    "referralreport": ReferralReport,
    "uncategorizedclinicaldocument": UncategorizedClinicalDocument,
}

delegation = DocumentReviewDelegation.objects.get(id="b3e6f74c-2a1b-4c8d-9f2e-31842ae7d3b9")

model = DOCUMENT_MODELS.get(delegation.content_type.model)
if delegation.content_type.app_label == "api" and model:
    document = model.objects.get(dbid=delegation.object_id)
```

At least one of `delegated_to_staff` and `delegated_to_team` is set on a delegation. Both are set when the signature was released to a person and a team together.
