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

| Attribute  | Type                 | Description                                                                 | Required |
| ---------- | -------------------- | --------------------------------------------------------------------------- | -------- |
| `claim_id` | `UUID` or `str`      | Identifier for the claim                                                    | Yes      |
| `labels`   | `list[str or Label]` | List of label names and [Label](#label) dataclasses\* to apply to the claim | Yes      |

\*Labels passed in by name must currently exist as a Label in your Canvas instance. Labels passed in as a Label dataclass will be created in your Canvas instance, and then applied to the specified claim. However, if a label already exists with the same properties as the Label dataclass, it will add this existing label to the claim to avoid creating a duplicate.

## Label

The `Label` dataclass represents a new label to be created in Canvas.

### Attributes

| Attribute  | Type                                                | Description                                                                         | Required |
| ---------- | --------------------------------------------------- | ----------------------------------------------------------------------------------- | -------- |
| `color`    | [ColorEnum](/sdk/data-enumeration-types/#colorenum) | The color of the label in the UI                                                    | Yes      |
| `name`     | `str`                                               | The display name of the label                                                       | Yes      |
| `position` | `int`                                               | The position of the label relative to other labels on the same claim. Defaults to 0 | No       |

#### Implementation Details

- Validates `claim_id` is provided and that the associated claim exists.
- Validates that `labels` are provided.
- Validates that `labels` identified by name exist in your Canvas instance.

#### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

from canvas_sdk.effects.claim_label import AddClaimLabel, Label
from canvas_sdk.v1.data import Note
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
                labels=[Label(color=ColorEnum.PINK, name="pushed not locked")],
            )
            return [add.apply()]
        elif state == "LKD":
            add_urgent = AddClaimLabel(claim_id=claim.id, labels=["Urgent"])
            return [add_urgent.apply()]

        return []
```

### RemoveClaimLabel

The `RemoveClaimLabel` effect removes an existing label from a claim.

#### Attributes

| Attribute  | Type            | Description                               | Required |
| ---------- | --------------- | ----------------------------------------- | -------- |
| `claim_id` | `UUID` or `str` | Identifier for the claim                  | Yes      |
| `labels`   | `list[str]`     | List of label names to apply to the claim | Yes      |

#### Implementation Details

- Validates `claim_id` is provided and that the associated claim exists
- Validates `labels` is provided and that the associated labels exist

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
            remove = RemoveClaimLabel(claim_id=claim.id, labels=["pushed not locked"])
            return [remove.apply()]
        return []
```
