---
title: "Claim Effects"
slug: "effect-claims"
excerpt: "Effects for claims."
hidden: false
---

The Canvas SDK provides effects to:

- manage claim labels, which includes [creating, adding](#addclaimlabel), and [removing](#removeclaimlabel) labels
- [update claim line items](#updateclaimlineitem)
- [move a claim to a specific queue](#moveclaimtoqueue)
- [post an insurance or patient payment](#postclaimpayment) to a claim

## AddClaimLabel

The `AddClaimLabel` effect facilitates adding a label to an existing claim, and optionally creating a new label before assigning it to the claim.

| Attribute  | Type                 | Description                                                                 | Required |
| ---------- | -------------------- | --------------------------------------------------------------------------- | -------- |
| `claim_id` | `UUID` or `str`      | Identifier for the claim                                                    | Yes      |
| `labels`   | `list[str or Label]` | List of label names and [Label](#label) dataclasses\* to apply to the claim | Yes      |

\*Labels can be passed in by name or as a Label dataclass. If the label with the provided name or values does not exist in your Canvas instance, it will be created and then applied to the specified claim. However, if a label already exists with the provided name or properties, it will add this existing label to the claim.

### Label

The `Label` dataclass represents a label with specific properties, including color and name.

### Attributes

| Attribute | Type                                                | Description                      | Required |
| --------- | --------------------------------------------------- | -------------------------------- | -------- |
| `color`   | [ColorEnum](/sdk/data-enumeration-types/#colorenum) | The color of the label in the UI | Yes      |
| `name`    | `str`                                               | The display name of the label    | Yes      |

### Implementation Details

- Validates `claim_id` is provided and that the associated claim exists.
- Validates that `labels` are provided and non-empty.

### Example Usage

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

## RemoveClaimLabel

The `RemoveClaimLabel` effect removes an existing label from a claim.

### Attributes

| Attribute  | Type            | Description                                  | Required |
| ---------- | --------------- | -------------------------------------------- | -------- |
| `claim_id` | `UUID` or `str` | Identifier for the claim                     | Yes      |
| `labels`   | `list[str]`     | List of label names to remove from the claim | Yes      |

### Implementation Details

- Validates `claim_id` is provided and that the associated claim exists
- Validates `labels` is provided and non-empty

### Example Usage

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

## UpdateClaimLineItem

The `UpdateClaimLineItem` effect allows you to update the `charge` field on a specified claim line item.

### Attributes

| Attribute            | Type            | Description                                        | Required |
| -------------------- | --------------- | -------------------------------------------------- | -------- |
| `claim_line_item_id` | `UUID` or `str` | Identifier for the claim line item                 | Yes      |
| `charge`             | `float`         | The charge amount to update on the claim line item | No       |

### Implementation Details

- Validates `claim_line_item_id` is provided and that the associated claim line item exists

### Example Usage

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

    def update_charge(self, id: str, charge: float) -> Effect:
        return UpdateClaimLineItem(claim_line_item_id=id, charge=charge).apply()

    def update_all_items(self, charge: float) -> list[Effect]:
        return [self.update_charge(line_item.id, charge) for line_item in self.get_line_items()]

    def compute(self) -> list[Effect]:
        if self.event.context["state"] == "ULK":
            return self.update_all_items(0.00)
        if self.event.context["state"] == "LKD":
            return self.update_all_items(500.00)
        return []
```

## MoveClaimToQueue

The `MoveClaimToQueue` effect moves a specific claim to a queue.

### Attributes

| Attribute  | Type            | Description                                                                                            | Required |
| ---------- | --------------- | ------------------------------------------------------------------------------------------------------ | -------- |
| `claim_id` | `UUID` or `str` | Identifier for the claim                                                                               | Yes      |
| `queue`    | `str`           | The name of the queue to move the claim to, which must be a [valid name](/sdk/data-claim/#claimqueues) | Yes      |

### Implementation Details

- Validates `claim_id` is provided and that the associated claim exists
- Validates `queue` is provided and the [queue with that name exists](/sdk/data-claim/#claimqueues)

### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.effects.claim_queue import MoveClaimToQueue
from canvas_sdk.v1.data import Note


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def compute(self) -> list[Effect]:
        if self.event.context["state"] == "ULK":
            note = Note.objects.get(id=self.event.context["note_id"])
            claim = note.get_claim()
            move = MoveClaimToQueue(
                claim_id=str(claim.id), queue="NeedsClinicianReview"
            )
            return [move.apply()]

```

## PostClaimPayment

The `PostClaimPayment` effect posts a payment to a claim, specifying payment details and line item transactions. This effect supports payments from insurance or patient and allows you to specify payments, adjustments, transfers, and write-offs on individual claim line items.

### Attributes

| Attribute             | Type              | Description                                                                                                    | Required |
| --------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------- | -------- |
| `method`              | `PaymentMethod`   | The [PaymentMethod](#paymentmethod-enumeration-type) used (e.g., `cash`, `check`, `card`, `other`).            | Yes      |
| `check_date`          | `date`            | Date of the check (required if method is `check`).                                                             | No       |
| `check_number`        | `str`             | Check number (required if method is `check`).                                                                  | No       |
| `deposit_date`        | `date`            | Date the payment was deposited.                                                                                | No       |
| `payment_description` | `str`             | Description of the payment.                                                                                    | No       |
| `claim`               | `ClaimAllocation` | [ClaimAllocation](#claimallocation) specifying how the payment is distributed to the claim and its line items. | Yes      |

#### Validations and Implementation Details

- `check_number` and `check_date` are required if payment method is `check`

### ClaimAllocation

| Attribute                | Type                          | Description                                                                 | Required |
| ------------------------ | ----------------------------- | --------------------------------------------------------------------------- | -------- |
| `claim_id`               | `UUID` or `str`               | Identifier for the claim.                                                   | Yes      |
| `claim_coverage_id`      | `UUID`, `str`, or `'patient'` | Identifier for the coverage or the string `'patient'` for patient payments. | Yes      |
| `line_item_transactions` | `list[LineItemTransaction]`   | List of [LineItemTransactions](#lineitemtransaction) for claim line items.  | Yes      |
| `move_to_queue_name`     | `str`                         | Name of the queue to move the claim to after payment.                       | No       |
| `description`            | `str`                         | Description for the claim allocation.                                       | No       |

#### Validations and Implementation Details

- `claim_id` must correspond to a valid existing claim. for insurance payments, there are a few ways to help you identify the correct claim using the [Claim](/sdk/data-claim/#claim), [ClaimSubmission](/sdk/data-claim/#claimsubmission), [ClaimCoverage](/sdk/data-claim/#claimcoverage) data models:
  - `Claim.account_number` is the identifier that Canvas sends to the clearinghouse as a unique Canvas identifier for the claim.
  - `ClaimSubmission.clearinghouse_claim_id` is the identifier that the clearinghouse sends back to Canvas after they have accepted the claim, and is used for the clearinghouse's internal tracking of the claim.
  - `ClaimCoverage.payer_icn` is the identifier that the insurance company uses for their internal tracking of the claim, and is usually provided to Canvas via the clearinghouse.
- `claim_coverage_id` must be either the string `"patient"` or correspond to a valid and **active** [ClaimCoverage](/sdk/data-claim/#claimcoverage) for the Claim.
  - a helpful way to identify the correct claim coverage is to use the method `get_coverage_by_payer_id(payer_id: str, subscriber_number: str | None = None)` on the [Claim](/sdk/data-claim/#claim) data model, where `payer_id` is the standard id for the insurance company. You can optionally provide `subscriber_number` if its possible that the patient has multiple coverages from the same payer and you want to identify the correct coverage.
- `move_to_queue_name` must be a valid label from [ClaimQueue](/sdk/data-claim/#claimqueues), but is not required. the claim will move to this queue after payment is applied.

### LineItemTransaction

| Attribute                       | Type                          | Description                                             | Required |
| ------------------------------- | ----------------------------- | ------------------------------------------------------- | -------- |
| `claim_line_item_id`            | `UUID` or `str`               | Identifier for the claim line item.                     | Yes      |
| `charged`                       | `Decimal`                     | Charged amount for the line item.                       | No       |
| `allowed`                       | `Decimal`                     | Allowed amount for the line item.                       | No       |
| `payment`                       | `Decimal`                     | Payment amount for the line item.                       | No       |
| `adjustment`                    | `Decimal`                     | Adjustment amount for the line item.                    | No       |
| `adjustment_code`               | `str`                         | Code describing the adjustment.                         | No       |
| `transfer_remaining_balance_to` | `UUID`, `str`, or `'patient'` | Transfer remaining balance to another payer or patient. | No       |
| `write_off`                     | `bool`                        | Whether to write off the remaining balance.             | No       |

#### Validations and Implementation Details

- `claim_line_item_id` must be a valid and **active** line item for the claim. It is recommended to search for it using `.active()` and by `proc_code`, e.g. `claim.line_items.active().filter(proc_code="99215").first()`
- there can be many LineItemTransactions for the same `claim_line_item_id`, but the first LineItemTransaction for a claim line item must specify either a payment or an adjustment (or allowed amount); subsequent transactions require an adjustment.
- if an `adjustment` is specified, an `adjustment_code` must also be provided.
- if the adjustment code is for a transfer (code starts with "Transfer"), a valid `transfer_remaining_balance_to` must be provided, and it cannot be the same payer as the `claim_coverage_id` payer from the ClaimAllocation.
- `transfer_remaining_balance_to` can only be made to the patient (using the string `"patient"`) or to an **active** `claim_coverage_id` for the claim.
- adjustments cannot simultaneously write off and transfer the same amount; only one of `write_off` or `transfer_remaining_balance_to` should be set on LineItemTransactions where `adjustment` is present.
- adjustments and transfers are not allowed for COPAY charges, i.e. claim line items where the proc_code = `COPAY`. only payments are allowed for those line items.
- `payment` on COPAY line items must have a `claim_coverage_id` equal to `"patient"`.
- `allowed` should be empty or $0 if `claim_coverage_id` is equal to `"patient"`.

#### PaymentMethod Enumeration Type

| Enum    | Value |
| :------ | :---- |
| `CASH`  | cash  |
| `CHECK` | check |
| `CARD`  | card  |
| `OTHER` | other |

### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.v1.data import ClaimLineItem, Claim
from decimal import Decimal
from canvas_sdk.effects.payment import (
    PostClaimPayment,
    PaymentMethod,
    ClaimAllocation,
    LineItemTransaction,
)
from datetime import date
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/routes/post-claim-payment/<id>"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        return True

    def create_line_item_transaction(
        self, line_item: ClaimLineItem, is_patient: bool = False
    ) -> LineItemTransaction:
        if line_item.proc_code.startswith("99"):
            lit = LineItemTransaction(
                charged=line_item.charge,
                claim_line_item_id=line_item.id,
                payment=line_item.charge - Decimal(100.00),
                adjustment=line_item.charge - Decimal(150.00),
                adjustment_code="CW-0",
                write_off=True,
            )
            if not is_patient:
                lit.payment = Decimal(50.00)
                lit.allowed = line_item.charge
                lit.adjustment = line_item.charge - Decimal(50.00)
                lit.adjustment_code = "PR-2"
                lit.transfer_remaining_balance_to = "patient"
                lit.write_off = False
            return lit
        if line_item.proc_code.startswith("00"):
            lit = LineItemTransaction(
                claim_line_item_id=line_item.id,
                charged=line_item.charge,
                payment=Decimal(20.00),
            )
            if not is_patient:
                lit.allowed = line_item.charge
                lit.transfer_remaining_balance_to = self.claim.coverages.last().id
                lit.adjustment = line_item.charge - Decimal(40.00)
                lit.adjustment_code = "CO-A2"
            return lit
        lit = LineItemTransaction(
            claim_line_item_id=line_item.id,
            charged=line_item.charge,
            payment=Decimal(5.00),
        )
        if not is_patient:
            lit.adjustment = line_item.charge - Decimal(10.00)
            lit.adjustment_code = "CO-45"
            lit.write_off = True
        return lit

    def post_patient_payment(self) -> Effect:
        pmt = PostClaimPayment(
            deposit_date=date(2025, 11, 11),
            method=PaymentMethod.CASH,
            payment_description="patient responsibility",
            claim=ClaimAllocation(
                claim_id=self.claim.id,
                claim_coverage_id="patient",
                move_to_queue_name="ZeroBalance",
                description="this is a patient payment",
                line_item_transactions=[
                    self.create_line_item_transaction(c, is_patient=True)
                    for c in self.claim_line_items
                ],
            ),
        )
        return pmt.apply()

    def post_coverage_payment(self) -> Effect:
        pmt = PostClaimPayment(
            check_date=date(2025, 11, 10),
            check_number="123456789",
            deposit_date=date(2025, 11, 11),
            method=PaymentMethod.CHECK,
            payment_description="money moneyyyy",
            claim=ClaimAllocation(
                claim_id=self.claim.id,
                claim_coverage_id=self.claim.coverages.first().id,
                description="this is a coverage payment",
                move_to_queue_name="PatientBalance",
                line_item_transactions=[
                    self.create_line_item_transaction(c) for c in self.claim_line_items
                ],
            ),
        )
        return pmt.apply()

    def get(self) -> list[Response | Effect]:
        claim_dbid = self.request.path_params["id"]
        self.claim = Claim.objects.get(dbid=claim_dbid)
        self.claim_line_items = self.claim.get_active_claim_line_items()
        return [
            self.post_coverage_payment(),
            self.post_patient_payment(),
            JSONResponse({"message": "ok"}),
        ]
```

<br/>
<br/>
<br/>
