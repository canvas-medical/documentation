---
title: "Payment Processor"
slug: "payment-processor-effect"
excerpt: "Effects returned by custom payment processors."
hidden: false
---

These effects are returned from a custom [Payment Processor](/sdk/handlers-payment-processors/) handler in response to the `REVENUE__PAYMENT_PROCESSOR__*` [events](/sdk/events/#payment-processor-events). Each effect is the handler's reply to a specific stage of a payment workflow — advertising the processor, rendering a form, charging a card, or managing a patient's saved payment methods.

All of the classes below are importable from `canvas_sdk.effects.payment_processor`.

## PaymentProcessorMetadata

Advertises a payment processor to Canvas in response to `REVENUE__PAYMENT_PROCESSOR__LIST`. Canvas uses it to discover which processors are installed and to route later events (charge, add card, etc.) to the right handler.

**You normally never construct this yourself.** The base `PaymentProcessor` handler builds and returns it automatically through its `metadata()` method, which fills in:

* `identifier` — a stable, unique id derived from your handler class (its module path and class name), exposed as `self.identifier`. Canvas includes this `identifier` in every subsequent payment processor event so your handler knows the event is meant for it.
* `type` — the processor's `TYPE` class attribute (for example, `CardPaymentProcessor` sets this to `CARD`).

Because the base handler already responds to `REVENUE__PAYMENT_PROCESSOR__LIST` with this effect, you only need to construct it directly in advanced cases where you override that default behavior.

| Attribute  |          | Type                                          | Description                                                                      |
|------------|----------|-----------------------------------------------|----------------------------------------------------------------------------------|
| identifier | required | String                                        | Unique identifier of the payment processor. Generated automatically per handler. |
| type       | required | [PaymentProcessorType](#paymentprocessortype) | The kind of processor. Currently only `CARD` is supported.                       |

### PaymentProcessorType

| Value  | Description             |
|--------|-------------------------|
| `CARD` | A card-based processor. |

## PaymentProcessorForm

Returns the HTML form used to collect and tokenize card details, in response to `REVENUE__PAYMENT_PROCESSOR__SELECTED`. The `content` is rendered as inner HTML inside Canvas and must implement the [Form Workflow](/sdk/handlers-payment-processors/#form-workflow).

| Attribute |          | Type   | Description                                              |
|-----------|----------|--------|----------------------------------------------------------|
| intent    | required | String | The purpose of the form. One of `"pay"` or `"add_card"`. |
| content   | required | String | The HTML content to render inside Canvas.                |

```python
from canvas_sdk.effects.payment_processor import PaymentProcessorForm
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data import Patient


def payment_form(self, patient: Patient | None = None) -> PaymentProcessorForm:
    content = render_to_string("templates/payment_form.html")
    return PaymentProcessorForm(intent="pay", content=content)
```

## CardTransaction

Returns the result of charging a card, in response to `REVENUE__PAYMENT_PROCESSOR__CHARGE`.

| Attribute      |          | Type           | Description                                                    |
|----------------|----------|----------------|----------------------------------------------------------------|
| success        | required | Boolean        | Whether the charge succeeded.                                  |
| transaction_id | required | String \| None | The identifier of the transaction, if one was created.         |
| api_response   | required | Dictionary     | The raw response returned by the payment provider.             |
| error_code     | optional | String \| None | An error code describing why the charge failed, if applicable. |

```python
from decimal import Decimal
from typing import Any
from canvas_sdk.effects.payment_processor import CardTransaction
from canvas_sdk.v1.data import Patient


def charge(
    self, amount: Decimal, token: str, patient: Patient | None = None, **kwargs: Any
) -> CardTransaction:
    return CardTransaction(
        success=True,
        transaction_id="txn_123",
        api_response={"status": "succeeded"},
    )
```

## PaymentMethod

Represents a patient's saved payment method, returned in response to `REVENUE__PAYMENT_PROCESSOR__PAYMENT_METHODS__LIST`.

Canvas does not store these cards itself. Saved payment methods live with your third-party payment provider, and your processor is responsible for persisting them there when a card is added and deleting them when a card is removed. Canvas simply asks your handler for the current list each time it needs to display saved cards, so there is no internal payment method table to expose to the SDK — the values you return here are rendered directly.

| Attribute             |          | Type           | Description                                 |
|-----------------------|----------|----------------|---------------------------------------------|
| payment_method_id     | required | String         | The identifier of the saved payment method. |
| brand                 | required | String         | The card brand (e.g. `"Visa"`).             |
| card_holder_name      | required | String \| None | The name of the card holder.                |
| expiration_year       | required | Integer        | The card's expiration year.                 |
| expiration_month      | required | Integer        | The card's expiration month.                |
| card_last_four_digits | required | String         | The last four digits of the card number.    |
| postal_code           | optional | String \| None | The billing postal code.                    |
| country               | optional | String \| None | The billing country.                        |

```python
from canvas_sdk.effects.payment_processor import PaymentMethod
from canvas_sdk.v1.data import Patient


def payment_methods(self, patient: Patient | None = None) -> list[PaymentMethod]:
    return [
        PaymentMethod(
            payment_method_id="pm_1",
            brand="Visa",
            card_holder_name="John Doe",
            expiration_year=2030,
            expiration_month=12,
            card_last_four_digits="4242",
            postal_code="12345",
        )
    ]
```

## AddPaymentMethodResponse

Returns the result of adding a payment method, in response to `REVENUE__PAYMENT_PROCESSOR__PAYMENT_METHODS__ADD`.

| Attribute |          | Type    | Description                           |
|-----------|----------|---------|---------------------------------------|
| success   | required | Boolean | Whether the payment method was added. |

```python
from typing import Any
from canvas_sdk.effects.payment_processor import AddPaymentMethodResponse
from canvas_sdk.v1.data import Patient


def add_payment_method(self, token: str, patient: Patient, **kwargs: Any) -> AddPaymentMethodResponse:
    return AddPaymentMethodResponse(success=True)
```

## RemovePaymentMethodResponse

Returns the result of removing a payment method, in response to `REVENUE__PAYMENT_PROCESSOR__PAYMENT_METHODS__REMOVE`.

| Attribute |          | Type    | Description                             |
|-----------|----------|---------|-----------------------------------------|
| success   | required | Boolean | Whether the payment method was removed. |

```python
from canvas_sdk.effects.payment_processor import RemovePaymentMethodResponse
from canvas_sdk.v1.data import Patient


def remove_payment_method(self, token: str, patient: Patient) -> RemovePaymentMethodResponse:
    return RemovePaymentMethodResponse(success=True)
```
