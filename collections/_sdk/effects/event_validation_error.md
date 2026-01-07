---
title: "EventValidationError Effect"
slug: "effect-event-validation-error"
excerpt: "Effect for blocking event creation with a validation error message."
hidden: false
---

## Overview

The `EventValidationError` effect is used to block the creation of an event (such as a NoteStateChangeEvent create) when custom validation fails. If this effect is returned by a protocol in response to an event (e.g., `NOTE_STATE_CHANGE_EVENT_PRE_CREATE`), the event is aborted and the provided error message is surfaced to the user.

## Attributes

| Attribute | Type                  | Description                                       | Required |
| --------- | --------------------- | ------------------------------------------------- | -------- |
| errors    | list[ValidationError] | List of validation errors to display to the user. | Yes      |

### ValidationError dataclass

Each item in the `errors` list is a `ValidationError` dataclass with the following fields:

| Field   | Type   | Description                               |
| ------- | ------ | ----------------------------------------- |
| message | string | The error message to display to the user. |

## Example Usage

Return an `EventValidationError` from your protocol's `compute` method to block the event and show a message to the user:

```python
from canvas_sdk.effects.validation import EventValidationError, ValidationError
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_PRE_CREATE)

    def compute(self):
        if self.event.context.get("state") == "UND":
            error = ValidationError("Cannot undelete a note. Please create a new one instead.")
            return [EventValidationError(errors=[error]).apply()]
        return []
```

You can also return other effects alongside `EventValidationError`. For example:

```python
from canvas_sdk.effects.validation import EventValidationError, ValidationError
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.effects.claim_queue import MoveClaimToQueue
from canvas_sdk.v1.data import Note

class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_PRE_CREATE)

    def compute(self):
        effects = []
        error_effect = EventValidationError()
        if self.event.context.get("state") == "UND":
            error_effect.add_error("Cannot undelete a note. Please create a new one instead.")
            error_effect.add_error("Please also ensure that the claim was moved to Trash.")
            effects.append(error_effect.apply())

            claim_id = Note.objects.get(id=self.event.context.get("note_id")).get_claim().id
            effects.append(MoveClaimToQueue(claim_id=str(claim_id), queue="Trash").apply())
        return effects
```

## Implementation Details

- If an `EventValidationError` is returned, the event is aborted and the error message is shown in the UI (if initiated from the UI).
- This effect is typically used for pre-create validation of events, such as note state changes.
