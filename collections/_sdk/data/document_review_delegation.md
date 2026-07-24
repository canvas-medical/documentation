---
title: "DocumentReviewDelegation"
slug: "data-document-review-delegation"
excerpt: "Canvas SDK DocumentReviewDelegation"
hidden: false
---

## Introduction

The `DocumentReviewDelegation` model provides read-only access to a document's review-delegation log. It is an append-only log linked to a document — currently an [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/) — through a Django generic relation (`content_type` + `object_id`).

Each entry records a hand-off between exactly two parties: the document's owner delegates the review to a staff member or team, and that recipient can only route the document back to the owner — never on to a third party. Exactly one delegation per document is active at a time (`is_active`).

The model is read-only in the SDK — you cannot create or modify delegations through it. Prefer accessing it through the parent document's `active_delegation` and `delegations` accessors rather than querying the model directly.

## Basic Usage

The recommended way to reach a document's delegations is through the parent document:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument

document = UncategorizedClinicalDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

# The current active delegation for this document, or None if it is not delegated.
active_delegation = document.active_delegation

# The full delegation history for this document, oldest first.
delegation_history = document.delegations
```

You can also query the model directly:

```python
from canvas_sdk.v1.data import DocumentReviewDelegation

delegation = DocumentReviewDelegation.objects.get(id="9c3d1b2a-6f4e-4a1c-8b2d-7e5f0a1c2d3e")
```

## Filtering

Delegations can be filtered by any attribute that exists on the model. A common case is narrowing to the active row:

```python
from canvas_sdk.v1.data import DocumentReviewDelegation

active_delegations = DocumentReviewDelegation.objects.filter(is_active=True)
```

## Identifying a route-back

`is_route_back` is a computed property that is `True` only when `delegated_to_staff` equals `on_behalf_of` — the recipient is the document's original owner, so the document is being routed back rather than delegated onward:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocument

document = UncategorizedClinicalDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

active_delegation = document.active_delegation
if active_delegation and active_delegation.is_route_back:
    # The recipient is routing the document back to its original owner.
    original_owner = active_delegation.on_behalf_of
```

## Attributes

### DocumentReviewDelegation

| Field Name         | Type                                               |
|--------------------|----------------------------------------------------|
| id                 | UUID                                               |
| dbid               | Integer                                            |
| created            | DateTime                                           |
| modified           | DateTime                                           |
| content_type       | [ContentType](/sdk/data-content-type/#contenttype) |
| object_id          | Integer                                            |
| delegated_by       | [Staff](/sdk/data-staff/#staff)                    |
| delegated_to_staff | [Staff](/sdk/data-staff/#staff)                    |
| delegated_to_team  | [Team](/sdk/data-team/#team)                       |
| on_behalf_of       | [Staff](/sdk/data-staff/#staff)                    |
| signature_consent  | Boolean                                            |
| comment            | String                                             |
| is_active          | Boolean                                            |
| is_route_back      | Boolean (property)                                 |

- **object_id**: the `dbid` of the linked document.
- **delegated_to_staff / delegated_to_team**: a delegation targets either a staff member or a team; the unused field is null.
- **on_behalf_of**: the document's original owner. This is also the signature owner when `signature_consent` is `True`.
- **is_route_back**: a computed property (see [Identifying a route-back](#identifying-a-route-back) above) — `True` when the delegation returns the document to its original owner.

<br/>
<br/>
<br/>
