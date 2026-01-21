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

Return an `EventValidationError` from your protocol's `compute` method to block the event and show a message to the user. You can also return other effects alongside `EventValidatinoError`.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import Note
from canvas_sdk.v1.data.coverage import CoverageStack
from canvas_sdk.effects.validation import EventValidationError, ValidationError
from canvas_sdk.effects.banner_alert import AddBannerAlert, RemoveBannerAlert


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_PRE_CREATE)

    def handle_no_coverage(self, patient_id: str, note: Note) -> list[Effect]:
        """If the patient has no coverage, add banner alert and do not allow notes to be locked or charges pushed."""
        if note.patient.coverages.filter(stack=CoverageStack.IN_USE).count() == 0:
            return [
                EventValidationError(
                    errors=[
                        ValidationError(
                            message="Patient has no coverage. Do not send claim to billing department until coverage(s) have been added."
                        ),
                        ValidationError(message="test"),
                    ]
                ).apply(),
                AddBannerAlert(
                    patient_id=patient_id,
                    key="no_coverage",
                    narrative="Patient has no documented coverages.",
                    placement=[
                        AddBannerAlert.Placement.CHART,
                        AddBannerAlert.Placement.APPOINTMENT_CARD,
                    ],
                    intent=AddBannerAlert.Intent.ALERT,
                ).apply(),
            ]
        return [RemoveBannerAlert(patient_id=patient_id, key="no_coverage").apply()]

    def handle_no_billing_line_items(self, note: Note) -> Effect | None:
        """If the note has no billing line items, do not allow notes to be locked or charges pushed."""
        if note.billing_line_items.filter(status="active").count() > 0:
            return None

        val_effect = EventValidationError()
        val_effect.add_error(
            "Cannot lock or push charges for a note with no billing line items."
        )
        return val_effect.apply()

    def compute(self) -> list[Effect]:
        state = self.event.context["state"]
        if state not in ["PSH", "LKD"]:
            return []
        note = Note.objects.get(id=self.event.context["note_id"])
        patient_id = str(note.patient.id)
        effects = self.handle_no_coverage(patient_id=patient_id, note=note)
        if v := self.handle_no_billing_line_items(note=note):
            effects.append(v)

        return effects
```

## Implementation Details

- If an `EventValidationError` is returned, the event is aborted and the error message is shown in the UI (if initiated from the UI).
- This effect is typically used for pre-create validation of events, such as note state changes.
