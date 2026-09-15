---
title: "Charge Stored Card"
slug: "effect-charge-stored-card"
excerpt: "Charge a patient's stored payment card on file."
hidden: false
---

The `ChargeStoredCard` effect charges a patient's stored payment card through the payment processor configured for your Canvas instance. The charge is processed server-side against the tokenized card, so no card data crosses the plugin boundary — you reference the card by an identifier the configured processor understands: the Canvas [PaymentCard](/sdk/data-payment-card/) id for the built-in Stripe processor, or a [custom payment processor](/sdk/handlers-payment-processors/)'s own reference, never the underlying processor token.

{% include alert.html type="warning" content="<b>You are responsible for obtaining patient consent before charging a stored card.</b> Canvas does not enforce consent for charges initiated through this effect." %}

## Charging a stored card

Import the `ChargeStoredCard` class, create an instance of it, and return its `.apply()` method from `compute`. When the effect is applied, Canvas confirms that the patient exists and, when a `claim_id` is supplied, that the claim exists. It raises a `ValidationError` if either check fails, or if `copay` is set without a `claim_id`. The card is not validated at this point: it is referenced by an identifier the configured processor understands — the Canvas PaymentCard id for the built-in Stripe processor, or a custom processor's own reference. That reference is resolved and validated server-side when the charge is processed, so a card reference the processor cannot resolve is rejected there rather than by `.apply()`.

| Attribute         |          | Type      | Description                                                                                                                                            |
| ----------------- | -------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| patient_id        | required | String    | The Canvas [Patient](/sdk/data-patient/#patient) id to charge.                                                                                          |
| payment_card_id   | required | String    | A reference to the stored card that the configured processor resolves: the Canvas [PaymentCard](/sdk/data-payment-card/) id for the built-in Stripe processor, or a custom processor's own reference. |
| amount            | required | Decimal   | The amount to charge, in dollars, with up to two decimal places (for example, `Decimal("49.99")`). Must be greater than `0`.                            |
| idempotency_key   | required | UUID      | A key that makes the charge safe to retry. Reusing the same key for a retry guarantees the patient is not charged twice. See [Idempotency](#idempotency). |
| claim_id          | optional | UUID or String | A [Claim](/sdk/data-claim/) id to post the payment against. When omitted, the payment is allocated across the patient's outstanding balance. See [Payment allocation](#payment-allocation). |
| copay             | optional | Boolean   | Whether the charge is a copay. When `true`, the amount is posted to the claim's copay line item; requires `claim_id`. Defaults to `false`. See [Payment allocation](#payment-allocation). |
| description       | optional | String    | A free-text description to record with the payment.                                                                                                    |

**Example:**

```python
from decimal import Decimal
from uuid import uuid5, NAMESPACE_URL

from canvas_sdk.effects import Effect
from canvas_sdk.effects.payment import ChargeStoredCard
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Patient


class ChargeVisitCopay(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.APPOINTMENT_CREATED)]

    def compute(self) -> list[Effect]:
        patient = Patient.objects.get(id=self.target)
        card = patient.payment_cards.filter(is_default=True).first()
        if card is None:
            return []

        charge = ChargeStoredCard(
            patient_id=str(patient.id),
            payment_card_id=str(card.id),
            amount=Decimal("25.00"),
            idempotency_key=uuid5(NAMESPACE_URL, f"appointment-{self.target}-copay"),
            description="Visit copay",
        )
        return [charge.apply()]
```

## Idempotency

Every charge requires an `idempotency_key`. Reusing the same key on a retry guarantees the patient is not charged twice, so the key must be **stable across retries of the same logical charge**. Generate it deterministically from a stable identifier — for example `uuid5(namespace, f"appointment-{id}-charge")` — or persist a `uuid4` before emitting the effect. Do not generate a fresh key on each attempt.

## Payment allocation

The payment is always applied to the patient's account:

- **Outstanding balance (default).** When no `claim_id` is given, the payment is allocated across the patient's outstanding balance. The charge is rejected if the amount exceeds the total balance.
- **Against a specific claim.** When `claim_id` is given and `copay` is left `false` (the default), the payment pays down that claim's line-item balances. The charge is rejected if the claim has nothing to charge against.
- **As a copay on a claim.** When `claim_id` is given with `copay` set to `true`, the amount is recorded as a copay on that claim, posted to its copay line item. This is allowed even when the claim has no outstanding balance, so use it to collect a copay or prepayment against a claim.

## Reconciling the charge

Once the charge has been processed, Canvas emits a `REVENUE__STORED_CARD__CHARGE_RESPONSE` event carrying the outcome. The event targets the patient, and its context carries no card data or PHI. Handle it in a separate handler. Correlate each response with the charge that produced it using the `idempotency_key` you supplied on the request.

This handler records the result of each charge, reading `payment_intent_id` when it succeeds and the `error` object when it does not:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from logger import log


class ReconcileStoredCardCharge(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.REVENUE__STORED_CARD__CHARGE_RESPONSE)]

    def compute(self) -> list[Effect]:
        context = self.event.context
        idempotency_key = context["idempotency_key"]

        if context["success"]:
            payment_intent_id = context["payment_intent_id"]
            log.info(f"Charge {idempotency_key} succeeded: {payment_intent_id}")
        else:
            error = context["error"]
            log.error(f"Charge {idempotency_key} failed [{error['code']}]: {error['message']}")

        return []
```

### Response context

The event `context` is a sanitized JSON object with the following fields; values that are UUIDs or decimals on the request are echoed here as strings.

| Field             | Type            | Description                                                                                                                       |
| ----------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| success           | Boolean         | Whether the charge succeeded.                                                                                                      |
| payment_intent_id | String or null  | The processor's payment identifier on success — the Stripe PaymentIntent id, or a custom processor's transaction id. `null` on failure. |
| error             | Object or null  | `null` on success. On failure, `error` is an object with `code` and `message` fields. See [Error codes](#error-codes).             |
| idempotency_key   | String          | Echoed from the request. Correlate the response with the originating charge using this value.                                     |
| patient_id        | String          | Echoed from the request: the patient that was charged.                                                                            |
| payment_card_id   | String          | Echoed from the request: the stored card reference that was charged.                                                              |
| claim_id          | String or null  | Echoed from the request, or `null` when no claim was supplied.                                                                    |
| amount            | String          | Echoed from the request: the dollar amount that was submitted.                                                                    |

### Error codes

On failure, `error.code` names the condition that stopped the charge.

| `error.code`             | When it occurs                                                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `patient_not_found`      | The `patient_id` did not match a patient.                                                                                              |
| `card_not_found`         | The stored card was not found. For the built-in Stripe processor, this also covers a card that exists but is not owned by the patient; a custom processor may raise a different code for that case — check the processor's own documentation. |
| `claim_not_found`        | The `claim_id` did not match a claim owned by the patient.                                                                            |
| `no_outstanding_balance` | A charge with no `claim_id` was attempted, but the patient has no outstanding balance. The balance is checked before the card is charged. |
| `amount_exceeds_balance` | A charge with no `claim_id` exceeds the patient's outstanding balance. The amount is validated against the balance before the card is charged. |
| `nothing_to_charge`      | A per-claim charge with `copay` set to `false` was attempted, but the claim has no chargeable, non-copay balance. Set `copay` to `true` to record a copay or prepayment instead. |
| `charge_failed`          | An unexpected failure occurred while processing the charge. Retry using the same `idempotency_key`; the retry will not double-charge the patient. |

The payment processor's own decline codes also pass through in `error.code` — for example, `card_declined` from Stripe — and can arrive at charge time. Handle an unrecognized code gracefully rather than matching against a fixed set, since the processor can surface codes this list does not name.

## Imports

```python
from canvas_sdk.effects.payment import ChargeStoredCard
```

<br/>
<br/>
<br/>
