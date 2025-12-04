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

The most common use case for this effect will be with the [SimpleAPI](/sdk/handlers-simple-api-http/) handler.

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
    PATH = "/routes/post-claim-payment"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        return True

    def get_claim_line_item(self, claim: Claim, proc_code: str) -> ClaimLineItem | None:
        return claim.line_items.active().filter(proc_code=proc_code).first()

    def create_line_item_transactions(
        self, charge: dict, claim: Claim
    ) -> list[LineItemTransaction]:
        transactions = []
        if not (line_item := self.get_claim_line_item(claim, charge.get("proc_code"))):
            return transactions

        charged = Decimal(charge["charge"])
        payment = Decimal(charge["paid"])
        allowed = Decimal(charge["allowed"])
        adjustments = charge.get("adjustment", [])
        first_adjustment = adjustments[0]
        payment = LineItemTransaction(
            claim_line_item_id=line_item.id,
            charged=charged,
            payment=payment,
            allowed=allowed,
            adjustment=Decimal(first_adjustment["amount"]),
            adjustment_code=f"{first_adjustment['group']}-{first_adjustment['code']}",
            # replace with whatever logic needed for resolving remaining balance
            transfer_remaining_balance_to="patient"
            if first_adjustment["group"] == "PR"
            else None,
        )
        transactions.append(payment)

        additional_adjustments = adjustments[1:]
        for adj in additional_adjustments:
            transaction = LineItemTransaction(
                claim_line_item_id=line_item.id,
                adjustment=Decimal(adj["amount"]),
                adjustment_code=f"{adj['group']}-{adj['code']}",
            )
            transactions.append(transaction)

        return transactions

    def get_claim(
        self, account_number: str, clearinghouse_claim_id: str
    ) -> Claim | None:
        return (
            Claim.objects.filter(account_number=account_number).first()
            or Claim.objects.filter(
                submissions__clearinghouse_claim_id=clearinghouse_claim_id,
            ).first()
            or Claim.objects.filter(coverage__payer_icn=clearinghouse_claim_id).first()
        )

    def post_payment(
        self,
        claim_payment_info: dict,
        check_number: str,
        check_date: str,
        payer_id: str,
    ) -> Effect | None:
        account_number = claim_payment_info.get("pcn")
        clearinghouse_claim_id = claim_payment_info.get("payer_icn")
        if not (claim := self.get_claim(account_number, clearinghouse_claim_id)):
            return None
        insurance_number = claim_payment_info.get("ins_number")
        if not (coverage := claim.get_coverage_by_payer_id(payer_id, insurance_number)):
            return None

        line_item_transactions = []
        for c in claim_payment_info.get("charge", []):
            line_item_transactions.extend(self.create_line_item_transactions(c, claim))

        pmt = PostClaimPayment(
            check_date=date.fromisoformat(check_date),
            check_number=check_number,
            deposit_date=date.fromisoformat(check_date),
            method=PaymentMethod.CHECK,
            payment_description="Aetna 835 payment",
            claim=ClaimAllocation(
                claim_id=claim.id,
                claim_coverage_id=coverage.id,
                line_item_transactions=line_item_transactions,
            ),
        )
        return pmt.apply()

    def post(self) -> list[Response | Effect]:
        payment_info = self.request.json()
        check_number = payment_info.get("check_number")
        check_date = payment_info.get("paid_date")
        payer_id = payment_info.get("payerid")
        payments = [
            p
            for claim in payment_info.get("claim", [])
            if (p := self.post_payment(claim, check_number, check_date, payer_id))
        ]
        return payments + [JSONResponse({"message": "ok"})]
```

With the above plugin installed, an example call to the endpoint would look like this:

```
curl -X POST "https://<instance-name>.canvasmedical.com/plugin-io/api/post_claim_payment/routes/post-claim-payment" \
  -H "Content-Type: application/json" \
  -H "Authorization: <api-key>" \
  -d '{
    "paid_date": "2025-11-06",
    "eraid": "23853671",
    "check_number": "397547083-1662491258",
    "paid_amount": "346.00",
    "payerid": "60054",
    "claim": [
        {
            "pcn": "124974-1",
            "payer_icn": "TST397547083",
            "total_charge": "48",
            "from_dos": "20250827",
            "pat_name_f": "ETHYL",
            "ins_name_l": "BATES",
            "total_paid": "0",
            "thru_dos": None,
            "pat_name_l": "BATES",
            "ins_number": "412098745",
            "ins_name_f": "NORMAN",
            "charge": [
                {
                    "chgid": "221043771",
                    "from_dos": "20220827",
                    "adjustment": [{"amount": "48", "group": "OA", "code": "109"}],
                    "paid": "0",
                    "allowed": "0",
                    "proc_code": "99212",
                    "charge": "48",
                    "thru_dos": None,
                    "units": "1",
                }
            ],
        },
        {
            "pcn": "21830-1",
            "payer_icn": "TST397547094",
            "total_charge": "75",
            "from_dos": "20220827",
            "pat_name_f": "MARYLOU",
            "ins_name_l": "DENNIS",
            "total_paid": "45",
            "thru_dos": None,
            "pat_name_l": "DENNIS",
            "ins_number": "223444467",
            "ins_name_f": "ROBERT",
            "charge": [
                {
                    "chgid": "221043716",
                    "from_dos": "20220827",
                    "adjustment": [
                        {"amount": "15", "group": "CO", "code": "45"},
                        {"amount": "10", "group": "PR", "code": "2"},
                        {"amount": "5", "group": "PR", "code": "3"},
                    ],
                    "paid": "45",
                    "allowed": "60",
                    "proc_code": "99213",
                    "charge": "75",
                    "thru_dos": None,
                    "units": "1",
                }
            ],
        },
        {
            "pcn": "103756-1",
            "payer_icn": "TST397547101",
            "total_charge": "75",
            "from_dos": "20220827",
            "pat_name_f": "BRISTER",
            "ins_name_l": "GUNTHRIE",
            "total_paid": "45",
            "thru_dos": None,
            "pat_name_l": "GUNTHRIE",
            "ins_number": "412341611",
            "ins_name_f": "VIRGINIA",
            "charge": [
                {
                    "chgid": "221043755",
                    "from_dos": "20220827",
                    "adjustment": [
                        {"amount": "15", "group": "CO", "code": "45"},
                        {"amount": "10", "group": "PR", "code": "2"},
                        {"amount": "5", "group": "PR", "code": "3"},
                    ],
                    "paid": "45",
                    "allowed": "60",
                    "proc_code": "99213",
                    "charge": "75",
                    "thru_dos": None,
                    "units": "1",
                }
            ],
        },
    ],
}'
```

<br/>
<br/>
<br/>
