---
title: "Fax Effects"
slug: "effect-fax"
excerpt: "Effects for faxing a referral, imaging order, lab order or letter on its own."
hidden: false
---

The fax effects send one document to a fax recipient without the rest of its note. The recipient gets the same PDF that the document's own **Fax** action sends from Canvas. To fax a whole note, use [Fax Note](/sdk/effect-notes/#fax-note).

| Effect | Sends | Recipient when you don't name one |
| --- | --- | --- |
| `FaxReferralEffect` | The referral and its attachments, plus the visit note when the referral includes it | The referral's service provider |
| `FaxImagingOrderEffect` | The imaging order | The order's imaging center |
| `FaxLabOrderEffect` | The lab order's requisition form | None. A recipient is required. |
| `FaxLetterEffect` | The letter and its attachments | None. A recipient is required. |

## Attributes

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `referral_id`, `imaging_order_id`, `lab_order_id` or `letter_id` | `UUID` or `str` | Identifier of the document to fax. Each effect takes its own. | Yes |
| `recipient_name` | `str` | Name of the fax recipient. Give it together with `recipient_fax_number`. | Lab orders and letters |
| `recipient_fax_number` | `str` | Fax number of the recipient, including the country code. Give it together with `recipient_name`. | Lab orders and letters |
| `include_coversheet` | `bool` | Whether to include a coversheet with the fax | No |
| `subject` | `str` or `None` | Subject line for the coversheet (required if coversheet used) | No |
| `comment` | `str` or `None` | Additional comments for the coversheet (required if coversheet used) | No |
| `location_id` | `UUID` or `str` or `None` | Practice location ID (required if coversheet used) | No |

## Implementation Details

- Validates that the document exists.
- Give `recipient_name` and `recipient_fax_number` together. For a referral or imaging order, you can leave both out to fax the referral's service provider or the order's imaging center. If you give only one, nothing is faxed. If there is no service provider, or it has no fax number, nothing is faxed.
- A referral, imaging order or lab order must be committed and not entered in error, as for its own **Fax** action in Canvas. Otherwise nothing is faxed.
- If `include_coversheet` is `True`, `subject`, `comment` and `location_id` become required, as they do for [Fax Note](/sdk/effect-notes/#fax-note).
- The fax is recorded on the document as a [ReferralActionEvent](/sdk/data-fax/#referralactionevent), [ImagingOrderActionEvent](/sdk/data-fax/#imagingorderactionevent), [LabOrderActionEvent](/sdk/data-fax/#laborderactionevent) or [LetterActionEvent](/sdk/data-letter-action-event/), with Canvas Bot as its `originator`. It appears in the document's fax history in Canvas, and `delivered_by_fax` is updated when the faxing service reports the outcome. See [Faxes sent by a plugin](/sdk/data-fax/#faxes-sent-by-a-plugin).

## Example Usage

Fax each referral to its service provider when its Refer command is committed:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.fax import FaxReferralEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data import Command


class FaxReferralOnCommit(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.REFER_COMMAND__POST_COMMIT)

    def compute(self) -> list[Effect]:
        referral = Command.objects.get(id=self.event.target.id).anchor_object
        if referral is None:
            return []

        return [FaxReferralEffect(referral_id=referral.id).apply()]
```

Fax a lab order's requisition form to the lab, with a coversheet:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.fax import FaxLabOrderEffect
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        fax_effect = FaxLabOrderEffect(
            lab_order_id="existing-lab-order-uuid",
            recipient_name="Acme Labs",
            recipient_fax_number="15555550100",
            include_coversheet=True,
            subject="Lab requisition",
            comment="Requisition for the attached lab order.",
            location_id="practice-location-uuid",
        )

        return [fax_effect.apply()]
```
