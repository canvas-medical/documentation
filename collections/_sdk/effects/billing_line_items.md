---
title: "Billing Line Items"
slug: "effect-billing-line-items"
excerpt: "Billing codes in the note footer."
hidden: false
---

The Canvas SDK allows you to create, update, and remove Billing Line Items from the footer of a note.

## Adding a Billing Line Item

To add a billing line item to a note, build an `AddBillingLineItem` and return its `apply()` from your handler.

### Methods

#### apply() → Effect

Adds the billing line item to the note's footer.

- `note_id` and `cpt` are required.
- `units` defaults to `1`.

### Attributes

| Attribute | Type | Description | Required |
|---|---|---|---|
| note_id | String | The id of the [Note](/sdk/data-note/) where the line item should be associated. | Yes |
| cpt | String | The billing code to use for the line item. | Yes |
| units | Integer | The number of units to bill for the code. Defaults to `1` if not provided. | No |
| assessment_ids | list[String] | List of Assessment ids from the note that are relevant to the code, also referred to as "diagnosis pointers". | No |
| modifiers | list[Coding] | The modifiers to create with the billing code. | No |

### Example

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

To populate diagnosis and CPT codes in a note footer from an external billing system, expose a [SimpleAPI](/sdk/handlers-simple-api-http/) endpoint that the system can call. The endpoint receives the note, CPT code, units, and ICD-10 codes, matches the ICD-10 codes to the note's assessments, and returns an `AddBillingLineItem` effect whose `assessment_ids` act as the line item's diagnosis pointers. This example authenticates with [`APIKeyAuthMixin`](/sdk/handlers-simple-api-http/#authentication-mixins), which checks requests against a plugin secret named `simpleapi-api-key`:

```python
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.billing_line_item import AddBillingLineItem
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPIRoute
from canvas_sdk.v1.data.assessment import Assessment


class BillingAPI(APIKeyAuthMixin, SimpleAPIRoute):
    PATH = "/billing/add-line-item"

    def post(self) -> list[Response | Effect]:
        # {"note_id": "...", "cpt_code": "99213", "units": 1, "icd10_codes": ["E119", "I10"]}
        body = self.request.json()
        note_id = body["note_id"]
        icd10_codes = {code.upper().replace(".", "") for code in body.get("icd10_codes", [])}

        # Use each of the note's assessments whose condition carries a requested ICD-10 code
        assessment_ids = [
            str(assessment.id)
            for assessment in Assessment.objects.filter(note__id=note_id).select_related("condition")
            if assessment.condition
            and any(
                coding.system == "ICD-10" and coding.code.upper().replace(".", "") in icd10_codes
                for coding in assessment.condition.codings.all()
            )
        ]

        effect = AddBillingLineItem(
            note_id=note_id,
            cpt=body["cpt_code"],
            units=body.get("units", 1),
            assessment_ids=assessment_ids,
        )

        return [
            effect.apply(),
            JSONResponse(
                {"message": "Billing line item sent to Canvas", "assessment_ids": assessment_ids},
                status_code=HTTPStatus.CREATED,
            ),
        ]
```

The [`cpt-billing-api` example plugin](https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/cpt-billing-api/cpt_billing_api) builds on this with request validation, a check that the CPT code is active in the charge description master, and a response listing which ICD-10 codes matched.

{% include alert.html type="warning" content="The billing line item is added to the note footer, not directly to a claim. As with any billing change, it must be applied before the note is locked, because locking pushes the note's charges to the claim. To apply it to the claim right away instead of at lock time, follow it with the Note effect's <a href='/sdk/effect-notes/#push-charges'><code>push_charges()</code></a> on the same note. If the API call succeeds but nothing appears on the note, confirm the note is unlocked and that the <code>note_id</code> resolves to the intended note." %}

## Updating a Billing Line Item

To update a billing line item, build an `UpdateBillingLineItem` and return its `apply()` from your handler.

### Methods

#### apply() → Effect

Updates the billing line item.

- `billing_line_item_id` is required.
- Only the attributes you set on the effect are changed. Attributes you leave unset keep their current values.

### Attributes

| Attribute | Type | Description | Required |
|---|---|---|---|
| billing_line_item_id | String | The id of the [BillingLineItem](/sdk/data-billing-line-item/) to update. | Yes |
| cpt | String | The billing code to use for the line item. | No |
| units | Integer | The number of units to bill for the code. | No |
| assessment_ids | list[String] | List of Assessment ids from the note that are relevant to the code, also referred to as "diagnosis pointers". | No |
| modifiers | list[Coding] | The modifiers to create with the billing code. | No |

### Example

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

To remove a billing line item, build a `RemoveBillingLineItem` and return its `apply()` from your handler.

When a Perform command is entered in error, Canvas removes the billing line item that the command added to the note footer. You don't need a plugin to remove it.

### Methods

#### apply() → Effect

Removes the billing line item from the note's footer.

- `billing_line_item_id` is required.

### Attributes

| Attribute | Type | Description | Required |
|---|---|---|---|
| billing_line_item_id | String | The id of the [BillingLineItem](/sdk/data-billing-line-item/) to remove. | Yes |

### Example

When a Perform command is entered in error, this handler removes every billing line item on the note that has the command's CPT code. That includes matching line items that came from other sources, such as another plugin, which Canvas doesn't remove on its own.

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