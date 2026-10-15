---
title: "Fax"
slug: "data-fax"
excerpt: "Canvas SDK Fax and fax action events"
hidden: false
---

## Introduction

Canvas creates a `Fax` record for every fax it sends or receives. `direction` tells the two apart.

- **Sent faxes:** when a user faxes a note, referral, imaging order, lab order, letter, or integration task, Canvas also records an action event on that document. Plugins can read them to see whether a fax was delivered, who sent it, and which number it went to.
- **Received faxes:** each one has a `Fax` record with the sender's number, the page count, and [whether it was received successfully](#faxes-canvas-receives).

Each document type has its own action event model:

| Document | Action event | Reverse accessor on the document |
| --- | --- | --- |
| [Note](/sdk/data-note/) | [NoteActionEvent](#noteactionevent) | `action_events` |
| [Referral](/sdk/data-referral/#referral) | [ReferralActionEvent](#referralactionevent) | `action_events` |
| [ImagingOrder](/sdk/data-imaging/#imagingorder) | [ImagingOrderActionEvent](#imagingorderactionevent) | `action_events` |
| [LabOrder](/sdk/data-labs/#laborder) | [LabOrderActionEvent](#laborderactionevent) | `action_events` |
| [IntegrationTask](/sdk/data-integration-task/#integrationtask) | [IntegrationTaskActionEvent](#integrationtaskactionevent) | `action_events` |
| [Letter](/sdk/data-letter/) | [LetterActionEvent](/sdk/data-letter-action-event/) | `letter_action_events` |

All six have the same [action event fields](#action-event-fields) and differ only in the document they point to.

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

```python?partial=true
from canvas_sdk.v1.data import ReferralActionEvent

failed = ReferralActionEvent.objects.filter(delivered_by_fax=False).select_related(
    "referral", "originator", "fax"
)
for event in failed:
    sender = event.originator
    failed_number = event.fax.to_fax_number if event.fax else None
```

### Faxes sent by a plugin

A fax sent with the [Fax Note effect](/sdk/effect-notes/#fax-note) is recorded as a `NoteActionEvent` on that note, with the Canvas Bot user as its `originator`. Canvas Bot's staff id is `5eede137ecfe4124b8b773040e33be14` on every instance. To read the outcome, look the event up by the note, the number it was sent to, and that originator, so faxes staff sent to the same number are left out. Numbers are stored in E.164 format:

```python?partial=true
from canvas_sdk.v1.data import NoteActionEvent

CANVAS_BOT_STAFF_ID = "5eede137ecfe4124b8b773040e33be14"

latest = (
    NoteActionEvent.objects.filter(
        note__id="89992c23-c298-4118-864a-26cb3e1ae822",
        fax__to_fax_number="+15555550100",
        originator__staff__id=CANVAS_BOT_STAFF_ID,
    )
    .order_by("-created")
    .first()
)
```

Every plugin's faxes are attributed to Canvas Bot, so this can't tell your plugin's faxes from another plugin's. If more than one plugin faxes the same note to the same number, compare `created` with when your plugin returned the effect.

### From a fax

A `Fax` reaches its action events through `noteactionevents`, `referralactionevents`, `imagingorderactionevents`, `laborderactionevents`, `letteractionevents`, and `integrationtaskactionevents`:

```python?partial=true
from canvas_sdk.v1.data import Fax

fax = Fax.objects.get(id="d2a6c1f4-7b3e-4c1a-9f5e-0a8b7c6d5e4f")
note_events = fax.noteactionevents.all()
```

### Faxes Canvas receives

Filter on `direction` to read received faxes. `success` is `False` when the faxing service reported a problem receiving the fax, such as a call that dropped partway through. Canvas still creates an integration task with the pages that arrived, so the document may be incomplete.

```python?partial=true
from canvas_sdk.v1.data import Fax, FaxDirection

received = Fax.objects.filter(direction=FaxDirection.INBOUND).order_by("-date_utc")
failed = received.filter(success=False)
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
| to_fax_number   | String                        | The number the fax was sent to, for example `+15555550100`. For a received fax, the Canvas number that received it |
| from_fax_number | String                        | The number the fax was sent from. For a received fax, the sender's number     |
| date_utc        | DateTime                      | When the faxing service accepted a sent fax, or finished receiving a received fax |
| fax_pages       | Integer                       | The number of pages                                                           |
| direction       | [FaxDirection](#faxdirection) | Whether Canvas sent or received the fax                                       |
| success         | Boolean                       | For a sent fax, whether the faxing service accepted it. See [Delivery status](#delivery-status). For a received fax, whether it was received successfully |
| noteactionevents            | QuerySet[[NoteActionEvent](#noteactionevent)]                      | The note faxes sent as this fax                |
| referralactionevents        | QuerySet[[ReferralActionEvent](#referralactionevent)]              | The referral faxes sent as this fax            |
| imagingorderactionevents    | QuerySet[[ImagingOrderActionEvent](#imagingorderactionevent)]      | The imaging order faxes sent as this fax       |
| laborderactionevents        | QuerySet[[LabOrderActionEvent](#laborderactionevent)]              | The lab order faxes sent as this fax           |
| letteractionevents          | QuerySet[[LetterActionEvent](/sdk/data-letter-action-event/)]      | The letter faxes sent as this fax              |
| integrationtaskactionevents | QuerySet[[IntegrationTaskActionEvent](#integrationtaskactionevent)] | The integration task faxes sent as this fax    |
| fax_statuses                | QuerySet[[FaxStatusModel](#faxstatusmodel)]                        | The status recorded when this fax was received |

### FaxStatusModel

Canvas records a status when it receives a fax: `Received`, or `Error` if the faxing service reported a problem receiving it. It's reachable through the fax's `fax_statuses` accessor and matches the fax's `success` value. Faxes sent from Canvas don't get one. Use [`success`](#fax) on the fax instead, which every received fax has.

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
