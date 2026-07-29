---
title: "Document Review Delegation"
slug: "data-document-review-delegation"
excerpt: "Canvas SDK Document Review Delegation"
hidden: false
---

## Introduction

The `DocumentReviewDelegation` model records a hand-off of a document review from one staff member to another staff member or team. When a reviewer delegates an uncategorized clinical document, Canvas stores who delegated it, who received it, the original owner, whether the recipient may apply the owner's signature, and any instructions.

Delegations are an append-only log: a document has at most one **active** delegation at a time (`is_active`). Delegation is A↔B only — an owner delegates a document out, and the recipient may only route it back — so `on_behalf_of` always identifies the original owner and, when `signature_consent` is set, the staff member whose signature the recipient may apply while annotating the document.

## Basic usage

To get a delegation by identifier, use the `get` method on the `DocumentReviewDelegation` model manager:

```python
from canvas_sdk.v1.data import DocumentReviewDelegation

delegation = DocumentReviewDelegation.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")
```

If you have an [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/), its delegations are available through the `delegations` and `active_delegation` accessors:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument

document = UncategorizedClinicalDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

# The full delegation history, oldest first.
history = document.delegations

# The current active delegation, or None when the document is with its owner.
current = document.active_delegation
if current and current.signature_consent:
    signer = current.on_behalf_of  # whose signature the recipient may apply
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

## Route-back

Use the `is_route_back` property to tell whether an active delegation returned the document to its owner (as opposed to delegating it away):

```python
delegation = document.active_delegation
if delegation and delegation.is_route_back:
    ...  # the document is back with its owner
```

## Attributes

### DocumentReviewDelegation

| Field Name         | Type                                                             |
|--------------------|-----------------------------------------------------------------|
| id                 | UUID                                                            |
| dbid               | Integer                                                         |
| created            | DateTime                                                        |
| modified           | DateTime                                                        |
| content_type       | [ContentType](/sdk/data-content-type/) (the delegated document's type) |
| object_id          | Integer (the delegated document's `dbid`)                       |
| delegated_by       | [Staff](/sdk/data-staff/#staff) (who handed the document off)   |
| delegated_to_staff | [Staff](/sdk/data-staff/#staff) (recipient, if delegated to a person) |
| delegated_to_team  | [Team](/sdk/data-team/#team) (recipient, if delegated to a team) |
| on_behalf_of       | [Staff](/sdk/data-staff/#staff) (the original owner)            |
| signature_consent  | Boolean (may the recipient apply the owner's signature)         |
| comment            | String (instructions for the recipient)                         |
| is_active          | Boolean (the current delegation for the document)               |

## The delegated document

`content_type` and `object_id` form a generic link to the document whose review was delegated: `content_type` identifies the linked model, and `object_id` is that record's `dbid`. Review delegation is currently supported only for [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/) records, so `content_type` always resolves to that model and `object_id` is the document's `dbid`. The generic relation leaves room for additional document types in the future.

The most direct way to work with a document's delegations is from the document itself, through its `delegations` and `active_delegation` accessors:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument

document = UncategorizedClinicalDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

current = document.active_delegation   # the active DocumentReviewDelegation, or None
history = document.delegations         # every delegation hop recorded for the document
```

To go the other way — from a delegation to the document it points at — read `content_type` to learn which model `object_id` refers to, then resolve it. A [ContentType](/sdk/data-content-type/) is identified by its stable `app_label` and `model` (the lowercased model name), so branch on those rather than on the per-environment `dbid`. This keeps working if more document types become delegatable later:

```python
from canvas_sdk.v1.data import DocumentReviewDelegation, UncategorizedClinicalDocument

delegation = DocumentReviewDelegation.objects.get(id="b3e6f74c-2a1b-4c8d-9f2e-31842ae7d3b9")

content_type = delegation.content_type
# Today content_type is always api / uncategorizedclinicaldocument; object_id is its dbid.
if content_type.app_label == "api" and content_type.model == "uncategorizedclinicaldocument":
    document = UncategorizedClinicalDocument.objects.get(dbid=delegation.object_id)
```

You can also use `content_type` to find every delegation for a given document type. Resolve the [ContentType](/sdk/data-content-type/) at runtime from its stable `app_label` and `model` — never hardcode the `dbid`, which differs per environment:

```python
from canvas_sdk.v1.data import ContentType, DocumentReviewDelegation

document_ct = ContentType.objects.filter(app_label="api", model="uncategorizedclinicaldocument").first()

delegations = DocumentReviewDelegation.objects.filter(content_type=document_ct)
```

Exactly one of `delegated_to_staff` / `delegated_to_team` is set on a delegation.