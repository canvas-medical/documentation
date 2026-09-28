---
title: "Fax"
slug: "data-fax"
excerpt: "Canvas SDK Fax and fax action events"
hidden: false
---

## Introduction

When a user faxes a note, referral, imaging order, lab order, letter, or integration task, Canvas records an action event on that document and a `Fax` record for the transmission. Plugins can read them to see whether a fax was delivered, who sent it, and which number it went to. Faxes Canvas receives are `Fax` records too, with their [status history](#status-history-of-a-fax) in `FaxStatusModel`.

Each document type has its own action event model:

| Document | Action event | Reverse accessor on the document |
| --- | --- | --- |
| [Note](/sdk/data-note/) | [NoteActionEvent](#noteactionevent) | `action_events` |
| [Referral](/sdk/data-referral/#referral) | [ReferralActionEvent](#referralactionevent) | `action_events` |
| [ImagingOrder](/sdk/data-imaging/#imagingorder) | [ImagingOrderActionEvent](#imagingorderactionevent) | `action_events` |
| [LabOrder](/sdk/data-labs/#laborder) | [LabOrderActionEvent](#laborderactionevent) | `action_events` |
| [IntegrationTask](/sdk/data-integration-task/#integrationtask) | [IntegrationTaskActionEvent](#integrationtaskactionevent) | `action_events` |
| [Letter](/sdk/data-letter/) | [LetterActionEvent](/sdk/data-letter-action-event/) | `letter_action_events` |

All six have the same [action event fields](#action-event-fields) and differ only in the document they point to. The models are read-only.

## Delivery status

Canvas submits a fax to the faxing service, and the service later reports whether it reached the recipient. `delivered_by_fax` on the action event holds that outcome:

| `delivered_by_fax` | Meaning |
| --- | --- |
| `None` | Submitted. The faxing service hasn't reported the outcome yet. |
| `True` | Delivered to the recipient. |
| `False` | Not delivered. `fax_result_msg` holds the reason the faxing service reported. |

A submission the faxing service rejects doesn't create an action event. So `received_by_fax` is `True` on every action event for a fax sent today, and `success` is `True` on every outbound `Fax`. Neither one tells you whether the fax was delivered.

## Basic usage

### Faxes of a document

Use the document's `action_events` accessor:

```python
from canvas_sdk.v1.data import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
faxes = note.action_events.filter(event_type="FAXED").select_related("fax")
```

### Failed faxes, with the sender and the number

`originator` is the [CanvasUser](/sdk/data-canvasuser/) who sent the fax, and `fax.to_fax_number` is the number it was sent to:

```python
from canvas_sdk.v1.data import ReferralActionEvent

failed = ReferralActionEvent.objects.filter(delivered_by_fax=False).select_related(
    "referral", "originator", "fax"
)
for event in failed:
    sender = event.originator
    failed_number = event.fax.to_fax_number if event.fax else None
```

### Faxes sent by a plugin

A fax sent with the [Fax Note effect](/sdk/effect-notes/#fax-note) is recorded as a `NoteActionEvent` on that note, attributed to the Canvas Bot user. To read its outcome, look it up by the note and the number it was sent to. Numbers are stored in E.164 format:

```python
from canvas_sdk.v1.data import NoteActionEvent

latest = (
    NoteActionEvent.objects.filter(
        note__id="89992c23-c298-4118-864a-26cb3e1ae822",
        fax__to_fax_number="+15555550100",
    )
    .order_by("-created")
    .first()
)
```

### From a fax

A `Fax` reaches its action events through `noteactionevent_set`, `referralactionevent_set`, `imagingorderactionevent_set`, `laborderactionevent_set`, `letteractionevent_set`, and `integrationtaskactionevent_set`:

```python
from canvas_sdk.v1.data import Fax

fax = Fax.objects.get(id="d2a6c1f4-7b3e-4c1a-9f5e-0a8b7c6d5e4f")
note_events = fax.noteactionevent_set.all()
```

### Status history of a fax

Canvas records a `FaxStatusModel` row when it receives a fax: `Received`, or `Error` if the fax couldn't be received. A fax's status rows are reachable through its `fax_statuses` accessor. Faxes sent from Canvas don't get status rows, so read a sent fax's outcome from `delivered_by_fax` on its action event.

```python
from canvas_sdk.v1.data import Fax, FaxDirection, FaxStatus

failed_inbound = Fax.objects.filter(
    direction=FaxDirection.INBOUND,
    fax_statuses__status=FaxStatus.ERROR,
)
```

## Attributes

### Fax

| Field Name      | Type                          | Notes                                                                         |
|-----------------|-------------------------------|-------------------------------------------------------------------------------|
| id              | UUID                          |                                                                               |
| dbid            | Integer                       |                                                                               |
| created         | DateTime                      |                                                                               |
| modified        | DateTime                      |                                                                               |
| fax_id          | String                        | The faxing service's id for the fax                                           |
| to_fax_number   | String                        | The number the fax was sent to, for example `+15555550100`                    |
| from_fax_number | String                        | The number the fax was sent from                                              |
| date_utc        | DateTime                      | When the faxing service accepted the fax                                      |
| fax_pages       | Integer                       | The number of pages                                                           |
| direction       | [FaxDirection](#faxdirection) |                                                                               |
| success         | Boolean                       | Whether the faxing service accepted the fax. See [Delivery status](#delivery-status). |

### FaxStatusModel

| Field Name | Type                    | Notes                         |
|------------|-------------------------|-------------------------------|
| id         | UUID                    |                               |
| dbid       | Integer                 |                               |
| created    | DateTime                | When the status was recorded  |
| modified   | DateTime                |                               |
| fax        | [Fax](#fax)             | The fax the status belongs to |
| status     | [FaxStatus](#faxstatus) |                               |

### Action event fields

These fields are on all six action event models.

| Field Name       | Type                                | Notes                                                                 |
|------------------|-------------------------------------|-----------------------------------------------------------------------|
| id               | UUID                                |                                                                       |
| dbid             | Integer                             |                                                                       |
| created          | DateTime                            |                                                                       |
| modified         | DateTime                            |                                                                       |
| event_type       | [EventType](#event-type)            |                                                                       |
| send_fax_id      | String                              | The faxing service's id for the fax                                   |
| received_by_fax  | Boolean                             | Whether the faxing service accepted the fax                           |
| delivered_by_fax | Boolean                             | The delivery outcome. See [Delivery status](#delivery-status).        |
| fax_result_msg   | String                              | The reason the faxing service gave for a failed delivery              |
| originator       | [CanvasUser](/sdk/data-canvasuser/) | The user who sent the fax                                             |
| fax              | [Fax](#fax)                         | The fax record, including the number it was sent to                   |

### NoteActionEvent

The [action event fields](#action-event-fields), plus:

| Field Name | Type                    |
|------------|-------------------------|
| note       | [Note](/sdk/data-note/) |

### ReferralActionEvent

The [action event fields](#action-event-fields), plus:

| Field Name | Type                                      |
|------------|-------------------------------------------|
| referral   | [Referral](/sdk/data-referral/#referral) |

### ImagingOrderActionEvent

The [action event fields](#action-event-fields), plus:

| Field Name    | Type                                              |
|---------------|---------------------------------------------------|
| imaging_order | [ImagingOrder](/sdk/data-imaging/#imagingorder) |

### LabOrderActionEvent

The [action event fields](#action-event-fields), plus:

| Field Name | Type                                  |
|------------|---------------------------------------|
| lab_order  | [LabOrder](/sdk/data-labs/#laborder) |

### IntegrationTaskActionEvent

The [action event fields](#action-event-fields), plus:

| Field Name       | Type                                                            |
|------------------|-----------------------------------------------------------------|
| integration_task | [IntegrationTask](/sdk/data-integration-task/#integrationtask) |

## Enumeration types

### FaxDirection

| Value | Label    |
|-------|----------|
| O     | Outbound |
| I     | Inbound  |

### FaxStatus

| Value | Label      |
|-------|------------|
| P     | Processing |
| S     | Sent       |
| R     | Received   |
| E     | Error      |

### Event Type

| Value   | Label   |
|---------|---------|
| PRINTED | Printed |
| FAXED   | Faxed   |
