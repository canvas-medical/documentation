---
title: "Fax"
slug: "data-fax"
excerpt: "Canvas SDK Fax and the action events that record fax delivery for notes, referrals, imaging orders, lab orders, integration tasks, and letters."
hidden: false
---

## Introduction

When a document is faxed from Canvas, Canvas records an action event on that document. The action event tracks whether the fax was delivered, why it failed, and who sent it. It also links to a `Fax` record that holds the recipient's fax number and the page count. Plugins read these records to confirm delivery, attribute a failed fax to the user who sent it, and report which number failed.

Each faxable document type has its own action event model. All of them have the same [action event fields](#action-event-fields) and differ only in the document they point to.

| Document                                                 | Action event model           | Import from                              | Accessor on the document |
|----------------------------------------------------------|------------------------------|------------------------------------------|--------------------------|
| [Note](/sdk/data-note/#note)                             | `NoteActionEvent`            | `canvas_sdk.v1.data.note`                | `note.action_events`     |
| [Referral](/sdk/data-referral/#referral)                 | `ReferralActionEvent`        | `canvas_sdk.v1.data.referral`            | `referral.action_events` |
| [ImagingOrder](/sdk/data-imaging/#imagingorder)          | `ImagingOrderActionEvent`    | `canvas_sdk.v1.data.imaging`             | `imaging_order.action_events` |
| [LabOrder](/sdk/data-labs/#laborder)                     | `LabOrderActionEvent`        | `canvas_sdk.v1.data.lab`                 | `lab_order.action_events` |
| [IntegrationTask](/sdk/data-integration-task/#integrationtask) | `IntegrationTaskActionEvent` | `canvas_sdk.v1.data.integration_task`    | `integration_task.action_events` |
| [Letter](/sdk/data-letter/#letter)                       | [`LetterActionEvent`](/sdk/data-letter-action-event/) | `canvas_sdk.v1.data.letter` | `letter.letter_action_events` |

All of these models, along with `Fax` and `FaxDirection`, can also be imported from `canvas_sdk.v1.data`.

## Delivery status

An action event moves through these states after a document is faxed:

| `received_by_fax` | `delivered_by_fax` | Meaning |
|-------------------|--------------------|---------|
| `True`            | `None`             | The faxing service accepted the fax, and delivery is still in progress. |
| `True`            | `True`             | The fax was delivered. |
| `True`            | `False`            | The fax failed or was cancelled. `fax_result_msg` holds the reason. |

Use `delivered_by_fax` as the delivery signal. `Fax.success` isn't a delivery signal: it's `True` on every outbound fax, because Canvas creates the `Fax` record only after the faxing service accepts the send.

## Basic usage

### Read the result of a note fax

When a plugin faxes a note with [`FaxNoteEffect`](/sdk/effect-notes/#fax-note), Canvas records a `NoteActionEvent` on the note. To check the outcome, read the note's most recent fax event:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="4a6a5b2c-8c1e-4a2f-9b1d-3e5f7a9c0b12")

latest_fax = (
    note.action_events.filter(event_type="FAXED")
    .select_related("fax")
    .order_by("-created")
    .first()
)

if latest_fax is None:
    status = "not faxed"
elif latest_fax.delivered_by_fax is None:
    status = "in progress"
elif latest_fax.delivered_by_fax:
    status = f"delivered to {latest_fax.fax.to_fax_number}"
else:
    status = f"failed: {latest_fax.fax_result_msg}"
```

For a fax sent with `FaxNoteEffect`, the event's `originator` is the Canvas bot user rather than a staff member. For a fax sent from the Canvas UI, `originator` is the user who sent it.

### Find failed faxes

To list failed faxes with the sender and the number that failed, filter on `delivered_by_fax=False`:

```python
from canvas_sdk.v1.data.referral import ReferralActionEvent

failed_faxes = ReferralActionEvent.objects.filter(
    event_type="FAXED", delivered_by_fax=False
).select_related("referral", "originator", "fax")

for event in failed_faxes:
    sender = event.originator
    failed_number = event.fax.to_fax_number if event.fax else None
    reason = event.fax_result_msg
```

Swap in any other action event model to check a different document type.

### Find the document for a fax

A `Fax` reaches the action events that link to it through Django's default reverse accessors: `noteactionevent_set`, `referralactionevent_set`, `imagingorderactionevent_set`, `laborderactionevent_set`, `integrationtaskactionevent_set`, and `letteractionevent_set`.

```python
from canvas_sdk.v1.data.fax import Fax

fax = Fax.objects.get(id="9e2d4c1b-7a3f-4e8d-b6c5-1f0a2e3d4c5b")

for event in fax.noteactionevent_set.select_related("note"):
    note = event.note
```

## Attributes

### Fax

| Field Name      | Type                           | Notes |
|-----------------|--------------------------------|-------|
| id              | UUID                           |       |
| dbid            | Integer                        |       |
| created         | DateTime                       |       |
| modified        | DateTime                       |       |
| fax_id          | String                         | The faxing service's identifier for the fax |
| to_fax_number   | String                         | The recipient's fax number |
| from_fax_number | String                         | The sender's fax number |
| date_utc        | DateTime                       | When the faxing service created the fax |
| fax_pages       | Integer                        | The number of pages |
| direction       | [FaxDirection](#faxdirection)  | Whether the fax was sent or received |
| success         | Boolean                        | Whether the faxing service accepted the fax. Always `True` on outbound faxes; use the action event's `delivered_by_fax` to check delivery. |

### Action event fields

`NoteActionEvent`, `ReferralActionEvent`, `ImagingOrderActionEvent`, `LabOrderActionEvent`, `IntegrationTaskActionEvent`, and `LetterActionEvent` all have these fields:

| Field Name       | Type                                  | Notes |
|------------------|---------------------------------------|-------|
| id               | UUID                                  |       |
| dbid             | Integer                               |       |
| created          | DateTime                              |       |
| modified         | DateTime                              |       |
| event_type       | [EventType](#eventtype)               | Whether the document was printed or faxed |
| send_fax_id      | String                                | The faxing service's identifier for the sent fax |
| received_by_fax  | Boolean                               | Whether the faxing service accepted the fax |
| delivered_by_fax | Boolean                               | Whether the fax was delivered. `None` while delivery is in progress. See [Delivery status](#delivery-status). |
| fax_result_msg   | String                                | The reason a fax failed. Empty when the fax is in progress or delivered. |
| originator       | [CanvasUser](/sdk/data-canvasuser/)   | The user who printed or faxed the document (nullable) |
| fax              | [Fax](#fax)                           | The fax record, with the recipient's number (nullable) |

Each model also has a foreign key to its document:

| Model                        | Field              | Type |
|------------------------------|--------------------|------|
| `NoteActionEvent`            | note               | [Note](/sdk/data-note/#note) |
| `ReferralActionEvent`        | referral           | [Referral](/sdk/data-referral/#referral) |
| `ImagingOrderActionEvent`    | imaging_order      | [ImagingOrder](/sdk/data-imaging/#imagingorder) |
| `LabOrderActionEvent`        | lab_order          | [LabOrder](/sdk/data-labs/#laborder) |
| `IntegrationTaskActionEvent` | integration_task   | [IntegrationTask](/sdk/data-integration-task/#integrationtask) |
| `LetterActionEvent`          | letter             | [Letter](/sdk/data-letter/#letter) |

## Enumeration types

### FaxDirection

| Value | Label    |
|-------|----------|
| O     | Outbound |
| I     | Inbound  |

### EventType

| Value   | Label   |
|---------|---------|
| PRINTED | Printed |
| FAXED   | Faxed   |
