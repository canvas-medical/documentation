---
title: "Fax Effects"
slug: "effect-fax"
excerpt: "Effects for faxing a note, referral, imaging order, lab order or letter."
hidden: false
---

The Canvas SDK includes effects to fax a note, or to fax a referral, imaging order, lab order or letter without the rest of its note. The recipient gets the same PDF that the document's own **Fax** action sends from Canvas.

| Effect | Sends | Recipient when you don't name one |
| --- | --- | --- |
| [`FaxNoteEffect`](#fax-a-note) | The note | None. A recipient is required. |
| [`FaxReferralEffect`](#fax-a-referral) | The referral and its attachments, plus the visit note when the referral includes it | The referral's service provider, when it has a fax number |
| [`FaxImagingOrderEffect`](#fax-an-imaging-order) | The imaging order | The order's imaging center, when it has a fax number |
| [`FaxLabOrderEffect`](#fax-a-lab-order) | The lab order's requisition form | None. A recipient is required. |
| [`FaxLetterEffect`](#fax-a-letter) | The letter and its attachments | None. A recipient is required. |

## Fax a Note

To fax a note, build a `FaxNoteEffect` and return its `apply()` from your handler. This effect is also documented under [Fax Note](/sdk/effect-notes/#fax-note) on the Note Effects page.

### Methods

#### apply() → Effect

Faxes the note.

- Validates that the note exists.
- If `include_coversheet` is `True`, `subject`, `comment` and `location_id` become required, and the practice location must exist.

### Attributes

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `note_id` | `UUID` or `str` | Identifier of the note to fax. | Yes |
| `recipient_name` | `str` | Name of the fax recipient. | Yes |
| `recipient_fax_number` | `str` | Fax number of the recipient, including the country code. | Yes |
| `include_coversheet` | `bool` | Whether to include a coversheet with the fax. | No |
| `subject` | `str` or `None` | Subject line for the coversheet (required if coversheet used). | No |
| `comment` | `str` or `None` | Additional comments for the coversheet (required if coversheet used). | No |
| `location_id` | `UUID` or `str` or `None` | Practice location ID (required if coversheet used). | No |

### Example

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.fax import FaxNoteEffect
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        fax_effect = FaxNoteEffect(
            note_id="existing-note-uuid",
            recipient_name="Dr. Jane Smith",
            recipient_fax_number="15551234567",
            include_coversheet=True,
            subject="Patient Referral - Follow-up Care",
            comment="Please review attached consultation notes for continuing care.",
            location_id="practice-location-uuid",
        )

        return [fax_effect.apply()]
```

## Fax a Referral

To fax a referral, build a `FaxReferralEffect` and return its `apply()` from your handler. The fax includes the referral's attachments, and the visit note when the referral includes it.

### Methods

#### apply() → Effect

Faxes the referral.

- Validates that the referral exists. It must be committed and not entered in error, as for its own **Fax** action in Canvas.
- Leave out both `recipient_name` and `recipient_fax_number` to fax the referral's service provider. Nothing is faxed if you give only one, if the referral has no service provider, or if the service provider has no fax number.

### Attributes

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `referral_id` | `UUID` or `str` | Identifier of the referral to fax. | Yes |
| `recipient_name` | `str` or `None` | Name of the fax recipient. Give it together with `recipient_fax_number`. | No |
| `recipient_fax_number` | `str` or `None` | Fax number of the recipient, including the country code. Give it together with `recipient_name`. | No |
| `include_coversheet` | `bool` | Whether to include a coversheet with the fax. | No |
| `subject` | `str` or `None` | Subject line for the coversheet (required if coversheet used). | No |
| `comment` | `str` or `None` | Additional comments for the coversheet (required if coversheet used). | No |
| `location_id` | `UUID` or `str` or `None` | Practice location ID (required if coversheet used). | No |

### Example

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

## Fax an Imaging Order

To fax an imaging order, build a `FaxImagingOrderEffect` and return its `apply()` from your handler.

### Methods

#### apply() → Effect

Faxes the imaging order.

- Validates that the imaging order exists. It must be committed and not entered in error, as for its own **Fax** action in Canvas.
- Leave out both `recipient_name` and `recipient_fax_number` to fax the order's imaging center. Nothing is faxed if you give only one, if the order has no imaging center, or if the imaging center has no fax number.

### Attributes

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `imaging_order_id` | `UUID` or `str` | Identifier of the imaging order to fax. | Yes |
| `recipient_name` | `str` or `None` | Name of the fax recipient. Give it together with `recipient_fax_number`. | No |
| `recipient_fax_number` | `str` or `None` | Fax number of the recipient, including the country code. Give it together with `recipient_name`. | No |
| `include_coversheet` | `bool` | Whether to include a coversheet with the fax. | No |
| `subject` | `str` or `None` | Subject line for the coversheet (required if coversheet used). | No |
| `comment` | `str` or `None` | Additional comments for the coversheet (required if coversheet used). | No |
| `location_id` | `UUID` or `str` or `None` | Practice location ID (required if coversheet used). | No |

### Example

Fax an imaging order to its imaging center:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.fax import FaxImagingOrderEffect
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        return [FaxImagingOrderEffect(imaging_order_id="existing-imaging-order-uuid").apply()]
```

## Fax a Lab Order

To fax a lab order's requisition form, build a `FaxLabOrderEffect` and return its `apply()` from your handler.

### Methods

#### apply() → Effect

Faxes the lab order's requisition form.

- Validates that the lab order exists. It must be committed and not entered in error, as for its own **Fax** action in Canvas.
- `recipient_name` and `recipient_fax_number` are required, because a lab order has no recipient on file.

### Attributes

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `lab_order_id` | `UUID` or `str` | Identifier of the lab order to fax. | Yes |
| `recipient_name` | `str` | Name of the fax recipient. | Yes |
| `recipient_fax_number` | `str` | Fax number of the recipient, including the country code. | Yes |
| `include_coversheet` | `bool` | Whether to include a coversheet with the fax. | No |
| `subject` | `str` or `None` | Subject line for the coversheet (required if coversheet used). | No |
| `comment` | `str` or `None` | Additional comments for the coversheet (required if coversheet used). | No |
| `location_id` | `UUID` or `str` or `None` | Practice location ID (required if coversheet used). | No |

### Example

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

## Fax a Letter

To fax a letter, build a `FaxLetterEffect` and return its `apply()` from your handler. The fax includes the letter's attachments.

### Methods

#### apply() → Effect

Faxes the letter.

- Validates that the letter exists.
- `recipient_name` and `recipient_fax_number` are required.

### Attributes

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `letter_id` | `UUID` or `str` | Identifier of the letter to fax. | Yes |
| `recipient_name` | `str` | Name of the fax recipient. | Yes |
| `recipient_fax_number` | `str` | Fax number of the recipient, including the country code. | Yes |
| `include_coversheet` | `bool` | Whether to include a coversheet with the fax. | No |
| `subject` | `str` or `None` | Subject line for the coversheet (required if coversheet used). | No |
| `comment` | `str` or `None` | Additional comments for the coversheet (required if coversheet used). | No |
| `location_id` | `UUID` or `str` or `None` | Practice location ID (required if coversheet used). | No |

### Example

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.fax import FaxLetterEffect
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        fax_effect = FaxLetterEffect(
            letter_id="existing-letter-uuid",
            recipient_name="Dr. Jane Smith",
            recipient_fax_number="15551234567",
        )

        return [fax_effect.apply()]
```

## Fax history

Each fax is recorded on its document with Canvas Bot as its `originator`, and appears in the document's fax history in Canvas. `delivered_by_fax` is updated when the faxing service reports the outcome. See [Faxes sent by a plugin](/sdk/data-fax/#faxes-sent-by-a-plugin).

| Effect | Recorded as |
| --- | --- |
| `FaxNoteEffect` | [NoteActionEvent](/sdk/data-fax/#noteactionevent), read through `note.action_events` |
| `FaxReferralEffect` | [ReferralActionEvent](/sdk/data-fax/#referralactionevent) |
| `FaxImagingOrderEffect` | [ImagingOrderActionEvent](/sdk/data-fax/#imagingorderactionevent) |
| `FaxLabOrderEffect` | [LabOrderActionEvent](/sdk/data-fax/#laborderactionevent) |
| `FaxLetterEffect` | [LetterActionEvent](/sdk/data-letter-action-event/) |
