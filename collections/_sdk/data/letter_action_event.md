---
title: "LetterActionEvent"
slug: "data-letter-action-event"
excerpt: "Canvas SDK LetterActionEvent"
hidden: false
---

## Introduction

The `LetterActionEvent` model represents occurrences of a letter being printed or faxed within Canvas. LetterActionEvents are associated with a [Letter](/sdk/data-letter/).

## Basic Usage

### Retrieve a specific letter action event

To get a letter action event by identifier, use the `get` method on the `LetterActionEvent` model manager:

```python
from canvas_sdk.v1.data.letter import LetterActionEvent

letterActionEvent = LetterActionEvent.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")
```

### Find a letter action event for a specific letter

If you have a letter object, you can access its associated letter_action_events using the `letter_action_events` attribute:

```python
from canvas_sdk.v1.data.letter import Letter

letter = Letter.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
letter_action_events = letter.letter_action_events
```

## Filtering

LetterActionEvents can be filtered by any attribute that exists on the model.

### By attribute

Filtering for letter action events is done with the `filter` method on the `LetterActionEvent` model manager:

```python
from canvas_sdk.v1.data.letter import LetterActionEvent

# Find all successful deliveries
delivered_letters = LetterActionEvent.objects.filter(delivered_by_fax=True)

# Find letter action events with a specific send_fax_id
letter_action_events = LetterActionEvent.objects.filter(send_fax_id="a1b2c3d4e5f6")
```

## Attributes

### LetterActionEvent

| Field Name       | Type                             | Notes                                           |
|------------------|----------------------------------|-------------------------------------------------|
| id               | UUID                             |                                                 |
| dbid             | Integer                          |                                                 |
| created          | DateTime                         |                                                 |
| modified         | DateTime                         |                                                 |
| event_type       | [EventType](#event-type)         | The type of the event                           |
| send_fax_id      | String                           | The id of the sent fax                          |
| received_by_fax  | Boolean                          | The isSuccess status of the received by fax     |
| delivered_by_fax | Boolean                          | The isSuccess status of the delivered by fax    |
| fax_result_msg   | str                              | The fax result message                          |
| letter           | [Letter](/sdk/data-letter/)      | The letter this action event is associated with |
| originator       | [User](/sdk/canvasuser)          | The user who created the letter (nullable)      |


## Enumeration types

### Event Type

| Value                | Label   |
|----------------------|---------|
| PRINTED              | Printed |
| FAXED                | Faxed   |
