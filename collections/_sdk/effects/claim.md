---
title: "Claim Effects"
slug: "effect-claims"
excerpt: "Effects for claims."
hidden: false
---

# Claim Effects

The Canvas SDK provides effects to:

- manage claim labels, which includes [creating, adding](#addclaimlabel), and [removing](#removeclaimlabel) labels.
- [update claim line items](#updateclaimlineitem)

## AddClaimLabel

The `AddClaimLabel` effect facilitates adding a label to an existing claim, and optionally creating a new label before assigning it to the claim.

| Attribute  | Type                 | Description                                                                 | Required |
| ---------- | -------------------- | --------------------------------------------------------------------------- | -------- |
| `claim_id` | `UUID` or `str`      | Identifier for the claim                                                    | Yes      |
| `labels`   | `list[str or Label]` | List of label names and [Label](#label) dataclasses\* to apply to the claim | Yes      |

\*Labels can be passed in by name or as a Label dataclass. If the label with the provided name or values does not exist in your Canvas instance, it will be created and then applied to the specified claim. However, if a label already exists with the provided name or properties, it will add this existing label to the claim.

## Label

The `Label` dataclass represents a label with specific properties, including color and name.

### Attributes

| Attribute | Type                                                | Description                      | Required |
| --------- | --------------------------------------------------- | -------------------------------- | -------- |
| `color`   | [ColorEnum](/sdk/data-enumeration-types/#colorenum) | The color of the label in the UI | Yes      |
| `name`    | `str`                                               | The display name of the label    | Yes      |

#### Implementation Details

- Validates `claim_id` is provided and that the associated claim exists.
- Validates that `labels` are provided and non-empty.

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

| Attribute  | Type            | Description                                  | Required |
| ---------- | --------------- | -------------------------------------------- | -------- |
| `claim_id` | `UUID` or `str` | Identifier for the claim                     | Yes      |
| `labels`   | `list[str]`     | List of label names to remove from the claim | Yes      |

#### Implementation Details

- Validates `claim_id` is provided and that the associated claim exists
- Validates `labels` is provided and non-empty

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

### UpdateClaimLineItem

The `UpdateClaimLineItem` effect allows you to update the `charge` field on a specified claim line item.

#### Attributes

| Attribute            | Type    | Description                                        | Required |
| -------------------- | ------- | -------------------------------------------------- | -------- |
| `claim_line_item_id` | `int`   | Identifier for the claim line item                 | Yes      |
| `charge`             | `float` | The charge amount to update on the claim line item | No       |

#### Implementation Details

- Validates `claim_line_item_id` is provided and that the associated claim line item exists

#### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import Note, ClaimLineItem
from canvas_sdk.effects.claim_line_item import UpdateClaimLineItem


class Protocol(BaseProtocol):
    """When a note is unlocked, update the associated claim's line items to have a charge of $0.00.
    When a note is locked, update the associated claim's line items to have a charge of $500.00."""
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def get_line_items(self) -> ClaimLineItem:
        note = Note.objects.get(id=self.event.context["note_id"])
        claim = note.get_claim()
        return claim.get_active_claim_line_items()

    def update_charge(self, id: int, charge: float) -> Effect:
        return UpdateClaimLineItem(claim_line_item_id=id, charge=charge).apply()

    def update_all_items(self, charge: float) -> list[Effect]:
        return [self.update_charge(line_item.dbid, 0.00) for line_item in self.get_line_items()]

    def compute(self) -> list[Effect]:
        if self.event.context["state"] == "ULK":
            return self.update_all_items(0.00)
        if self.event.context["state"] == "LKD":
            return self.update_all_items(500.00)
        return []
```
