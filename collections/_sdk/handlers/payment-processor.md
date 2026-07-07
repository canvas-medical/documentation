---
title: "Payment Processor"
slug: "handlers-payment-processor"
excerpt: "Integrate a third-party payment processor into Canvas revenue workflows."
hidden: false
---

The `PaymentProcessor` family of handlers lets you plug a third-party payment
processor (Stripe, Braintree, an in-house provider, etc.) into Canvas's
revenue workflows. When a user collects a payment from a patient in Canvas,
your handler renders the processor-specific form, charges the card, and
manages saved payment methods on file.

There are two handler classes in `canvas_sdk.handlers.payment_processors`:

- **`PaymentProcessor`** — abstract base class for any payment-processor type.
  It wires the six `REVENUE__PAYMENT_PROCESSOR__*` events to template
  methods and delegates the rest to a subclass. You will usually subclass
  `CardPaymentProcessor` instead.
- **`CardPaymentProcessor`** — concrete card-processor base. Implement its
  abstract methods to integrate a card processor.

## How payment processors fit in

Canvas emits six events across the payment-processor lifecycle. The base
class subscribes to all of them and dispatches to a method on your subclass:

| Event | Purpose | Subclass method |
|---|---|---|
| `REVENUE__PAYMENT_PROCESSOR__LIST` | Canvas asks every installed processor of a given type to identify itself. | `metadata()` (returns a `PaymentProcessorMetadata` effect by default) |
| `REVENUE__PAYMENT_PROCESSOR__SELECTED` | A user selected this processor and Canvas needs the form(s) to render. | `on_payment_processor_selected(intent)` |
| `REVENUE__PAYMENT_PROCESSOR__CHARGE` | Charge the card represented by `token` for `amount`. | `charge(amount, token, patient, **kwargs)` |
| `REVENUE__PAYMENT_PROCESSOR__PAYMENT_METHODS__LIST` | List saved payment methods for a patient. | `payment_methods(patient)` |
| `REVENUE__PAYMENT_PROCESSOR__PAYMENT_METHODS__ADD` | Add a new payment method (e.g. save a card on file). | `add_payment_method(token, patient, **kwargs)` |
| `REVENUE__PAYMENT_PROCESSOR__PAYMENT_METHODS__REMOVE` | Remove a saved payment method. | `remove_payment_method(token, patient)` |

Each event arrives with an `identifier` in `self.event.context`. The base
class filters events whose `identifier` doesn't match your processor's
identifier, so multiple processors can be installed side-by-side without
stepping on each other.

The `identifier` is computed automatically from the fully-qualified class
path (`{module}:{qualname}`, base64-encoded). You normally don't need to
override it.

## Creating a Card Payment Processor

To integrate a card processor, subclass `CardPaymentProcessor` and
implement all six abstract methods. Then register the handler in
`CANVAS_MANIFEST.json` like any other handler.

```python
from decimal import Decimal
from typing import Any

from canvas_sdk.effects.payment_processor import (
    AddPaymentMethodResponse,
    CardTransaction,
    PaymentMethod,
    PaymentProcessorForm,
    RemovePaymentMethodResponse,
)
from canvas_sdk.handlers.payment_processors.card import CardPaymentProcessor
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data import Patient


class MyCardProcessor(CardPaymentProcessor):
    """Integrate MyProvider's card payment API with Canvas."""

    def payment_form(self, patient: Patient | None = None) -> PaymentProcessorForm:
        return PaymentProcessorForm(
            content=render_to_string("forms/payment.html"),
            intent=CardPaymentProcessor.PaymentIntent.PAY,
        )

    def add_card_form(self, patient: Patient | None = None) -> PaymentProcessorForm:
        return PaymentProcessorForm(
            content=render_to_string("forms/add_card.html"),
            intent=CardPaymentProcessor.PaymentIntent.ADD_CARD,
        )

    def charge(
        self, amount: Decimal, token: str, patient: Patient | None = None, **kwargs: Any
    ) -> CardTransaction:
        # Call your processor's API and translate the response.
        response = my_provider.charge(amount=amount, source=token)
        return CardTransaction(
            success=response.ok,
            transaction_id=response.id,
            api_response=response.raw,
            error_code=response.error_code,
        )

    def payment_methods(self, patient: Patient | None = None) -> list[PaymentMethod]:
        if patient is None:
            return []
        return [
            PaymentMethod(
                payment_method_id=card.id,
                brand=card.brand,
                expiration_year=card.exp_year,
                expiration_month=card.exp_month,
                card_holder_name=card.holder_name,
                postal_code=card.postal_code,
                card_last_four_digits=card.last4,
            )
            for card in my_provider.cards_for(patient.id)
        ]

    def add_payment_method(
        self, token: str, patient: Patient, **kwargs: Any
    ) -> AddPaymentMethodResponse:
        result = my_provider.attach_card(patient_id=patient.id, source=token)
        return AddPaymentMethodResponse(success=result.ok)

    def remove_payment_method(
        self, token: str, patient: Patient
    ) -> RemovePaymentMethodResponse:
        result = my_provider.detach_card(patient_id=patient.id, source=token)
        return RemovePaymentMethodResponse(success=result.ok)
```

Register the handler in `CANVAS_MANIFEST.json`. The `event` field is left
blank — the base class declares its own `RESPONDS_TO`, so you don't have
to.

```json
{
    "components": {
        "handlers": [
            {
                "class": "my_payment_processor.handlers.processor:MyCardProcessor",
                "description": "MyProvider card payment processor.",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
        ]
    }
}
```

## Required methods on `CardPaymentProcessor`

All six are abstract — your subclass must implement each one.

### `payment_form(patient)`

Return a `PaymentProcessorForm` whose `content` is the HTML to render when
the user is paying. `intent` should be
`CardPaymentProcessor.PaymentIntent.PAY`. The form typically posts a
tokenized payment method back to your processor.

### `add_card_form(patient)`

Return a `PaymentProcessorForm` whose `content` is the HTML to render when
the user is saving a new card on file. `intent` should be
`CardPaymentProcessor.PaymentIntent.ADD_CARD`.

When the `REVENUE__PAYMENT_PROCESSOR__SELECTED` event arrives without an
`intent`, the base class invokes both `payment_form()` and
`add_card_form()` and returns both forms. When an `intent` is supplied,
only the matching form is returned.

### `charge(amount, token, patient, **kwargs)`

Charge the card represented by `token` for `amount` (a `Decimal`). Return
a `CardTransaction` describing the result.

`additional_context` arrives in `**kwargs`. If the incoming event ships an
`additional_context` value, the base class tries to parse it as JSON;
when it's a JSON object, its keys are merged into `**kwargs`, otherwise
the raw value is passed through as `additional_context=...`.

### `payment_methods(patient)`

Return a list of `PaymentMethod` describing the cards saved on file for
the given patient. Return an empty list if no patient context is supplied
or none are saved.

### `add_payment_method(token, patient, **kwargs)`

Save the tokenized payment method on file for the given patient. Return
an `AddPaymentMethodResponse` with `success=True` if the save succeeded.
The base class skips this call entirely when no patient is supplied in
the event context.

The same `additional_context` parsing described under `charge()` applies
here.

### `remove_payment_method(token, patient)`

Remove the saved payment method identified by `token` for the given
patient. Return a `RemovePaymentMethodResponse`. As with
`add_payment_method`, the base class skips this call when no patient is
in the event context.

## Effects

These are the effect classes returned by the methods above. They live in
`canvas_sdk.effects.payment_processor`.

### `PaymentProcessorMetadata`

Returned by the base class in response to
`REVENUE__PAYMENT_PROCESSOR__LIST` to advertise this processor. Fields:

- `identifier` (str) — auto-populated from the handler's class path.
- `type` (`PaymentProcessorMetadata.PaymentProcessorType`) — currently
  only `CARD` is supported.

### `PaymentProcessorForm`

The HTML form to render when the user is paying or adding a card. Fields:

- `intent` (str) — `"pay"` or `"add_card"` (use the
  `CardPaymentProcessor.PaymentIntent` enum).
- `content` (str) — HTML body of the form.

### `CardTransaction`

The result of a charge attempt. Fields:

- `success` (bool) — whether the charge succeeded.
- `transaction_id` (str | None) — the processor's transaction id.
- `api_response` (dict) — the raw processor response, useful for
  reconciliation and debugging.
- `error_code` (str | None) — set when `success=False`.

### `PaymentMethod`

A card on file. Fields:

- `payment_method_id` (str)
- `card_holder_name` (str | None)
- `brand` (str) — e.g. `"Visa"`, `"Mastercard"`.
- `postal_code` (str | None)
- `country` (str | None)
- `expiration_year` (int)
- `expiration_month` (int)
- `card_last_four_digits` (str)

### `AddPaymentMethodResponse` / `RemovePaymentMethodResponse`

Each has a single `success` (bool) field.

## Tips

- The `identifier` is base64-encoded `{module}:{qualname}`. If you rename
  or move your handler class, its identifier changes, and previously
  saved payment methods will no longer route to it. Keep the class path
  stable once the integration is in production.
- A patient is not always present. `payment_form()`, `add_card_form()`,
  `charge()`, and `payment_methods()` accept `patient: Patient | None`.
  Plan for both cases.
- Store nothing sensitive yourself. Cards should be tokenized by your
  processor's client-side SDK before the token reaches `charge()` or
  `add_payment_method()`.
- For the list of related effect types and their event identifiers, see
  the [Revenue / Payment Processor](/sdk/effects/#revenue--payment-processor)
  section in the Effects module documentation.
