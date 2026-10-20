---
title: "Document Review Delegation"
slug: "data-document-review-delegation"
excerpt: "Canvas SDK Document Review Delegation"
hidden: false
---

## Introduction

The `DocumentReviewDelegation` model records each step of the send-for-signature flow on a reviewable document: a Lab, Imaging, Consult/Referral, or Uncategorized review. Staff prepare a form by marking where the signature and date go, then select **SEND FOR SIGNATURE** to send it to a provider. Canvas records a delegation to that provider, with the sender as `on_behalf_of`. When the provider selects **SIGN FORM**, Canvas stamps the provider's own saved signature and the date into the form and returns it to the sender. That return is recorded as a route-back delegation, and `is_route_back` is `True`.

Each document has at most one **active** delegation (`is_active`). Earlier delegations stay in the table as inactive rows. The active delegation ends when the document changes hands any other way, when its review command is committed, or when it's marked as not needing review.

Each staff member places only their own signature, so `signature_consent` doesn't let anyone apply another person's signature. To see the document's full timeline, including reassignments, comments, and signatures, use [DocumentHistoryEvent](/sdk/data-document-history-event/).

## Basic usage

To get a delegation by identifier, use the `get` method on the `DocumentReviewDelegation` model manager:

```python
from canvas_sdk.v1.data import DocumentReviewDelegation

delegation = DocumentReviewDelegation.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")
```

Each reviewable document exposes its delegations through the `delegations` and `active_delegation` accessors. [LabReport](/sdk/data-labs/#delegations), [ImagingReport](/sdk/data-imaging/#delegations), [ReferralReport](/sdk/data-referral/#delegations), and [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/#delegations) all provide them:

```python
from canvas_sdk.v1.data import LabReport

lab_report = LabReport.objects.get(id="7c9e6679-7425-40de-944b-e07fc1f90ae7")

# The full delegation history, oldest first.
history = lab_report.delegations

# The active delegation, or None when no delegation is in effect.
current = lab_report.active_delegation
if current and not current.is_route_back:
    provider = current.delegated_to_staff  # the provider asked to sign
    sender = current.on_behalf_of  # who sent the form for signature
```

## Filtering

Delegations can be filtered by any attribute that exists on the model.

### Active delegations

```python
from canvas_sdk.v1.data import DocumentReviewDelegation

active = DocumentReviewDelegation.objects.filter(is_active=True)
```

### Documents waiting on a provider's signature

```python
from canvas_sdk.v1.data import DocumentReviewDelegation, Staff

provider = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")

awaiting_signature = DocumentReviewDelegation.objects.filter(
    is_active=True, delegated_to_staff=provider
).exclude(on_behalf_of=provider)
```

## Route-back

Use the `is_route_back` property to tell whether a delegation returned the signed document to whoever sent it, rather than sending it to a provider to sign:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument

document = UncategorizedClinicalDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

delegation = document.active_delegation
if delegation and delegation.is_route_back:
    ...  # the signed form is back with its sender
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
| delegated_by       | [Staff](/sdk/data-staff/#staff) (who sent the form, or the provider returning it signed) |
| delegated_to_staff | [Staff](/sdk/data-staff/#staff) (the provider asked to sign, or the sender a signed form returns to) |
| delegated_to_team  | [Team](/sdk/data-team/#team) (recipient team, on delegations recorded before send for signature) |
| on_behalf_of       | [Staff](/sdk/data-staff/#staff) (who sent the form for signature) |
| signature_consent  | Boolean (grants nothing; each staff member places only their own signature) |
| comment            | String (the comment left with the request)                      |
| is_active          | Boolean (the delegation is still in effect)                     |

## The delegated document

`content_type` and `object_id` form a generic link to the delegated document: `content_type` identifies the linked model, and `object_id` is that record's `dbid`. A delegation can point at any of the four reviewable document types:

| Document | `content_type.app_label` | `content_type.model` |
|----------|--------------------------|----------------------|
| [LabReport](/sdk/data-labs/#labreport) | `api` | `labreport` |
| [ImagingReport](/sdk/data-imaging/#imagingreport) | `api` | `imagingreport` |
| [ReferralReport](/sdk/data-referral/#referralreport) | `api` | `referralreport` |
| [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/) | `api` | `uncategorizedclinicaldocument` |

To find every delegation for one document type, resolve the [ContentType](/sdk/data-content-type/) at runtime from its stable `app_label` and `model`. Never hardcode the content type `dbid`, which differs per environment:

```python
from canvas_sdk.v1.data import ContentType, DocumentReviewDelegation

imaging_report_ct = ContentType.objects.get(app_label="api", model="imagingreport")

imaging_delegations = DocumentReviewDelegation.objects.filter(content_type=imaging_report_ct)
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

Exactly one of `delegated_to_staff` and `delegated_to_team` is set on a delegation. Send for signature always sets `delegated_to_staff`; `delegated_to_team` appears only on delegations recorded before send for signature existed.
