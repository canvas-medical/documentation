---
title: "Document History Event"
slug: "data-document-history-event"
excerpt: "Canvas SDK Document History Event"
hidden: false
---

## Introduction

The `DocumentHistoryEvent` model records the review history of a Lab, Imaging, Consult/Referral, or Uncategorized document. Canvas adds an entry each time staff reassign the document, add a comment, send it for signature, sign it, remove a signature, record the review, or enter the review in error. Together the entries form the timeline that the document's history view shows.

Each entry stores who acted (`actor`), who received the document, any comment, and, for signed and recorded entries, whose signatures the document carried.

## Basic usage

To get a history entry by identifier, use the `get` method on the `DocumentHistoryEvent` model manager:

```python?partial=true
from canvas_sdk.v1.data import DocumentHistoryEvent

event = DocumentHistoryEvent.objects.get(id="0f6b3c2e-8a51-4d7e-9c14-5b2e7a9d3f60")
```

## Getting a document's timeline

History entries link to their document through `content_type` and `object_id`, which is the document's `dbid`. Resolve the [ContentType](/sdk/data-content-type/) at runtime from its stable `app_label` and `model`, rather than hardcoding its `dbid`:

```python?partial=true
from canvas_sdk.v1.data import ContentType, DocumentHistoryEvent, ImagingReport

report = ImagingReport.objects.get(id="3a5d8e21-6b4f-4c9a-8e27-1d9f0b6c4a73")
report_ct = ContentType.objects.get(app_label="api", model="imagingreport")

timeline = DocumentHistoryEvent.objects.filter(
    content_type=report_ct, object_id=report.dbid
).order_by("created")
```

The `model` values for the four reviewable document types are `labreport`, `imagingreport`, `referralreport`, and `uncategorizedclinicaldocument`, all with the `app_label` `api`.

## Filtering

History entries can be filtered by any attribute that exists on the model.

### By event type

```python?partial=true
from canvas_sdk.v1.data import DocumentHistoryEvent, DocumentHistoryEventType

comments = DocumentHistoryEvent.objects.filter(event_type=DocumentHistoryEventType.COMMENTED)
```

### Signers of recorded documents

```python?partial=true
from canvas_sdk.v1.data import DocumentHistoryEvent, DocumentHistoryEventType

recorded = DocumentHistoryEvent.objects.filter(event_type=DocumentHistoryEventType.RECORDED)
for event in recorded:
    signer_names = [staff.full_name for staff in event.signers.all()]
```

## Entry types

| Event type | Written when | Populated fields |
|------------|--------------|------------------|
| `reassigned` | Staff reassign the document, including reviewer or team changes from the card's dropdowns. | `recipient_staff` and `recipient_team` hold the new assignment; `comment` holds any comment. `actor` is empty when the change came from an API client or a plugin. |
| `commented` | Staff add a comment without changing who holds the document. | `comment` |
| `sent_for_signature` | Staff send a prepared form to a provider to sign. The document keeps its team. | `recipient_staff` holds the provider and `recipient_team` the document's team; `comment` holds any comment. A [DocumentReviewDelegation](/sdk/data-document-review-delegation/) records the same request. |
| `signed` | The provider holding the document signs it with **SIGN FORM**. When the form goes back to whoever sent it, a `reassigned` entry follows. | `actor` and `signers` hold the provider. |
| `signature_removed` | Staff remove a signature from a signed form so they can edit it again. Canvas restores the version from just before signing. | `actor` |
| `recorded` | The document's review command is recorded. Recording again adds a new entry. | `signers`, `review_content_type`, and `review_object_id` |
| `entered_in_error` | The document's review command is entered in error. | `review_content_type` and `review_object_id` |

When a review is entered in error, its `recorded` entry stays in the timeline, but its comment is hidden: `deleted_at` is set and `comment_hidden` returns `True`.

## Attributes

### DocumentHistoryEvent

| Field Name          | Type                                                                                 |
|---------------------|--------------------------------------------------------------------------------------|
| id                  | UUID                                                                                 |
| dbid                | Integer                                                                              |
| created             | DateTime                                                                             |
| modified            | DateTime                                                                             |
| content_type        | [ContentType](/sdk/data-content-type/) (the document's type)                         |
| object_id           | Integer (the document's `dbid`)                                                      |
| event_type          | [DocumentHistoryEventType](#documenthistoryeventtype)                                |
| actor               | [Staff](/sdk/data-staff/#staff) (who acted, or empty for an API client or plugin)    |
| recipient_staff     | [Staff](/sdk/data-staff/#staff) (who received the document)                          |
| recipient_team      | [Team](/sdk/data-team/#team) (the team that received the document)                   |
| comment             | String                                                                               |
| review_content_type | [ContentType](/sdk/data-content-type/) (the review command's type)                   |
| review_object_id    | Integer (the review command's `dbid`)                                                |
| signers             | [Staff](/sdk/data-staff/#staff)[] (whose signatures the signed or recorded document carried) |
| deleted_at          | DateTime (when the comment was hidden)                                               |
| comment_hidden      | Boolean (`True` when `deleted_at` is set)                                            |

## Enumeration types

### DocumentHistoryEventType

| Value              | Label              |
|--------------------|--------------------|
| REASSIGNED         | Reassigned         |
| COMMENTED          | Commented          |
| SENT_FOR_SIGNATURE | Sent for signature |
| SIGNED             | Signed             |
| SIGNATURE_REMOVED  | Signature removed  |
| RECORDED           | Recorded           |
| ENTERED_IN_ERROR   | Entered in error   |
