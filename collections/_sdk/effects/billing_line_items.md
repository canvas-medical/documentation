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
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Command, Assessment
from canvas_sdk.effects.billing_line_item import AddBillingLineItem


class MyHandler(BaseHandler):
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

You don't set the line item's description in your plugin. When the line item is created, Canvas matches the `cpt` to a [ChargeDescriptionMaster](/sdk/data-charge-description-master/) charge and populates the description from that charge's `short_name`, truncated to 255 characters. If no charge matches the `cpt`, the description is left empty.

<!-- source: discussion #1376 -->
### Adding billing codes from an external system

To populate diagnosis and CPT codes in a note footer from an external billing system, expose a [Simple API](/sdk/handlers-simple-api-http/) endpoint that accepts a payload (for example, a note id, a CPT code, units, and a list of ICD-10 codes), resolves the relevant note and assessments, and returns an `AddBillingLineItem` effect. The `assessment_ids` map to the note's assessments and act as the diagnosis pointers for the line item. A complete reference implementation is available in the [`cpt-billing-api` example plugin](https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/cpt-billing-api/cpt_billing_api).

```python?partial=true
from canvas_sdk.effects.billing_line_item import AddBillingLineItem

effect = AddBillingLineItem(
    note_id=note_id,
    cpt=cpt_code,
    units=units,
    assessment_ids=assessment_ids,
)
return [effect.apply(), json_response]
```

{% include alert.html type="warning" content="The billing line item is added to the note footer, not directly to a claim. As with any billing change, it must be applied before the note is locked (locking pushes charges to the claim). If the API call succeeds but nothing appears on the note, confirm the note is unlocked and that the <code>note_id</code> resolves to the intended note." %}

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
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Assessment, Command, BillingLineItem
from canvas_sdk.effects.billing_line_item import UpdateBillingLineItem


class MyHandler(BaseHandler):
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
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Command, BillingLineItem
from canvas_sdk.effects.billing_line_item import RemoveBillingLineItem


class MyHandler(BaseHandler):
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

For more information about the BillingLineItem data class, check out [this page](/sdk/data-billing-line-item).

<br/>
<br/>
<br/>