---
title: "Billing Line Items"
slug: "effect-billing-line-items"
excerpt: "Billing codes in the note footer."
hidden: false
---

The Canvas SDK allows you to create, update, and remove Billing Line Items from the footer of a note.

## Adding a Billing Line Item

To add a billing line item to a note, import the `AddBillingLineItem` class, create an
instance of it, and return the `.apply()` method from compute.

| Attribute      |          | Type         | Description                                                                                                   |
| -------------- | -------- | ------------ | ------------------------------------------------------------------------------------------------------------- |
| note_id        | required | String       | The id of the [Note](/sdk/data-note/) where the line item should be associated.                               |
| cpt            | required | String       | The billing code to use for the line item.                                                                    |
| units          | optional | Integer      | The number of units to bill for the code. Defaults to `1` if not provided.                                    |
| assessment_ids | optional | list[String] | List of Assessment ids from the note that are relevant to the code, also referred to as "diagnosis pointers". |
| modifiers      | optional | list[Coding] | The modifiers to create with the billing code.                                                                |

**Example:**

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import Command, Assessment
from canvas_sdk.effects.billing_line_item import AddBillingLineItem


class Protocol(BaseProtocol):
    RESPONDS_TO = [
        EventType.Name(EventType.PERFORM_COMMAND__POST_ORIGINATE)
    ]

    def compute(self) -> list[Effect]:
        command_id = self.target
        command = Command.objects.get(id=command_id)
        note = command.note

        assessments = [
            str(i)
            for i in Assessment.objects.filter(note_id=note.dbid).values_list(
                "id", flat=True
            )
        ]

        b = AddBillingLineItem(
            note_id=str(note.id),
            cpt="99213",
            units=1,
            assessment_ids=assessments,
            modifiers=[
                {"code": "25", "system": "http://www.ama-assn.org/go/cpt"},
                {"code": "59", "system": "http://www.ama-assn.org/go/cpt"},
            ],
        )
        return [b.apply()]

```

## Updating a Billing Line Item

To update a billing line item to a note, import the `UpdateBillingLineItem` class, create an
instance of it, and return the `.apply()` method from compute.

| Attribute            |          | Type         | Description                                                                                                   |
| -------------------- | -------- | ------------ | ------------------------------------------------------------------------------------------------------------- |
| billing_line_item_id | required | String       | The id of the [BillingLineItem](/sdk/data-billing-line-item/) to update.                                      |
| cpt                  | optional | String       | The billing code to use for the line item.                                                                    |
| units                | optional | Integer      | The number of units to bill for the code.                                                                     |
| assessment_ids       | optional | list[String] | List of Assessment ids from the note that are relevant to the code, also referred to as "diagnosis pointers". |
| modifiers            | optional | list[Coding] | The modifiers to create with the billing code.                                                                |

**Example:**

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import Command, BillingLineItem
from canvas_sdk.effects.billing_line_item import UpdateBillingLineItem


class Protocol(BaseProtocol):
    RESPONDS_TO = [
        EventType.Name(EventType.PERFORM_COMMAND__POST_COMMIT)
    ]

    def compute(self) -> list[Effect]:
        command_id = self.target
        command = Command.objects.get(id=command_id)
        note = command.note

        cpt = command.data["perform"]["value"]

        b_ids = BillingLineItem.objects.filter(cpt="99213", note=note).values_list(
            "id", flat=True
        )
        assessment = Assessment.objects.filter(note_id=note.dbid).first()
        updates = [
            UpdateBillingLineItem(
                billing_line_item_id=str(b_id),
                cpt=cpt,
                units=1,
                assessment_ids=[str(assessment.id)],
                modifiers=[{"code": "47", "system": "http://www.ama-assn.org/go/cpt"}],
            )
            for b_id in b_ids
        ]
        return [update.apply() for update in updates]

```

## Removing a Billing Line Item

To remove a billing line item to a note, import the `RemoveBillingLineItem` class, create an
instance of it, and return the `.apply()` method from compute.

| Attribute            |          | Type   | Description                                                              |
| -------------------- | -------- | ------ | ------------------------------------------------------------------------ |
| billing_line_item_id | required | String | The id of the [BillingLineItem](/sdk/data-billing-line-item/) to update. |
|                      |

**Example:**

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import Command, BillingLineItem
from canvas_sdk.effects.billing_line_item import RemoveBillingLineItem


class Protocol(BaseProtocol):
    RESPONDS_TO = [
        EventType.Name(EventType.PERFORM_COMMAND__POST_ENTER_IN_ERROR)
    ]

    def compute(self) -> list[Effect]:
        command_id = self.target
        command = Command.objects.get(id=command_id)

        cpt = command.data["perform"]["value"]
        note_id = command.note.dbid
        b_ids = BillingLineItem.objects.filter(cpt=cpt, note_id=note_id).values_list(
            "id", flat=True
        )
        return [
            RemoveBillingLineItem(billing_line_item_id=str(b_id)).apply()
            for b_id in b_ids
        ]

```

For more information about the BillingLineItem data class, check out [this page](sdk/data-billing-line-item).
