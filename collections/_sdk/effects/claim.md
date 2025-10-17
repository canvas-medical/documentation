---
title: "Claim Effects"
slug: "effect-claims"
excerpt: "Effects for claims."
hidden: false
---

# Claim Effects

The Canvas SDK provides effects to manage claim labels, which includes creating, adding, and removing labels.

## AddClaimLabel

The `AddClaimLabel` effect facilitates adding a label to an existing claim, and optionally creating a new label before assigning it to the claim.

| Attribute      | Type            | Description                                                             | Required |
| -------------- | --------------- | ----------------------------------------------------------------------- | -------- |
| `claim_id`     | `UUID` or `str` | Identifier for the claim                                                | Yes      |
| `label_id`     | `UUID` or `str` | Identifier for the label                                                | No\*     |
| `label_values` | [Label](#label) | Values for creating a brand new label before assigning it to the claim. | No\*     |

\*Either `label_id` or `label_values` is required in order to apply this effect. If `label_values` is provided, a new label will be created; otherwise `label_id` is used.

## Label

The `Label` dataclass represents a new label to be created in Canvas.

### Attributes

| Attribute  | Type                                                | Description                                                                         | Required |
| ---------- | --------------------------------------------------- | ----------------------------------------------------------------------------------- | -------- |
| `color`    | [ColorEnum](/sdk/data-enumeration-types/#colorenum) | The color of the label in the UI                                                    | Yes      |
| `name`     | `str`                                               | The display name of the label                                                       | Yes      |
| `position` | `int`                                               | The position of the label relative to other labels on the same claim. Defaults to 0 | No       |

#### Implementation Details

- Validates `claim_id` is provided and that the associated claim exists
- Validates that `label_id` or `label_values` is provided.
- If `label_id` provided, validates that the associated label exists

#### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

from canvas_sdk.effects.claim_label import AddClaimLabel, Label
from canvas_sdk.v1.data import Note, TaskLabel
from canvas_sdk.v1.data.common import ColorEnum


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def compute(self) -> list[Effect]:
        """Creates and adds a new label the claim when charges are pushed.
        Adds the existing Urgent label when the note is locked."""
        note = Note.objects.get(id=self.event.context["note_id"])
        claim = note.get_claim()
        state = self.event.context["state"]
        if state == "PSH":
            add = AddClaimLabel(
                claim_id=claim.id,
                label_values=Label(color=ColorEnum.PINK, name="pushed not locked"),
            )
            return [add.apply()]
        elif state == "LKD":
            urgent_label = TaskLabel.objects.filter(name="Urgent").first()
            add_urgent = AddClaimLabel(claim_id=claim.id, label_id=urgent_label.id)
            return [add_urgent.apply()]

        return []
```

### RemoveClaimLabel

The `RemoveClaimLabel` effect removes an existing label from a claim.

#### Attributes

| Attribute  | Type            | Description              | Required |
| ---------- | --------------- | ------------------------ | -------- |
| `claim_id` | `UUID` or `str` | Identifier for the claim | Yes      |
| `label_id` | `UUID` or `str` | Identifier for the label | Yes      |

#### Implementation Details

- Validates `claim_id` is provided and that the associated claim exists
- Validates `label_id` is provided and that the associated label exists

#### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

from canvas_sdk.effects.claim_label import RemoveClaimLabel
from canvas_sdk.v1.data import Note, TaskLabel


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def compute(self) -> list[Effect]:
        """When note is locked, remove the 'pushed not locked' label from the claim."""
        note = Note.objects.get(id=self.event.context["note_id"])
        claim = note.get_claim()
        state = self.event.context["state"]
        if state == "LKD":
            if label := TaskLabel.objects.filter(name="pushed not locked").first():
                remove = RemoveClaimLabel(claim_id=claim.id, label_id=label.id)
                return [remove.apply()]
        return []
```
