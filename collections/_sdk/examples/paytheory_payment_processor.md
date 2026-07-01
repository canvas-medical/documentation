---
title: 'PayTheory Payment Processor'
slug: 'example-paytheory_payment_processor'
---

{% include alert.html type="github" content="<a href='https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/paytheory-payment-processor' target='_blank'>View the source</a> for this plugin on GitHub." %}

This Canvas EMR plugin integrates [Pay Theory](https://paytheory.com) as a custom credit card [payment processor](/sdk/handlers-payment-processors/), letting Canvas collect payments and manage a patient's saved cards through a third-party provider instead of the built-in Stripe integration.

## SDK Features

* Extends the [`CardPaymentProcessor`](/sdk/handlers-payment-processors/#cardpaymentprocessor) handler
* Responds to the [`REVENUE__PAYMENT_PROCESSOR__*` events](/sdk/events/#payment-processor-events)
* Renders tokenization forms with the [`PaymentProcessorForm`](/sdk/payment-processor-effect/#paymentprocessorform) effect and [Django templates](/sdk/layout-effect/#custom-html-and-django-templates)
* Charges cards and returns a [`CardTransaction`](/sdk/payment-processor-effect/#cardtransaction) effect
* Lists, adds, and removes saved cards with the [`PaymentMethod`](/sdk/payment-processor-effect/#paymentmethod), [`AddPaymentMethodResponse`](/sdk/payment-processor-effect/#addpaymentmethodresponse), and [`RemovePaymentMethodResponse`](/sdk/payment-processor-effect/#removepaymentmethodresponse) effects
* Reads configuration from plugin [secrets](/sdk/secrets/) and declares `url_permissions` for the Pay Theory JS SDK

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "paytheory_payment_processor",
    "description": "PayTheory credit card payment processor integration",
    "url_permissions": [
        {
            "url": "https://*.sdk.paytheory.com/index.js",
            "permissions": ["SCRIPTS"]
        }
    ],
    "components": {
        "protocols": [
            {
                "class": "paytheory_payment_processor.handlers.paytheory_payment_processor:PayTheoryPaymentProcessor",
                "description": "Handles credit card payments, tokenization, and payment method management via PayTheory",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": ["paytheory_merchant_id", "paytheory_public_key", "paytheory_secret_key", "paytheory_partner", "paytheory_environment"],
    "tags": {},
    "references": [],
    "license": "",
    "readme": "./README.md"
}
```

The `url_permissions` above are abbreviated — the full manifest lists every Pay Theory SDK, token-service, and tags-static URL across the production, sandbox, and lab environments.

## handlers/

### paytheory_payment_processor.py

**Purpose and Functionality**

This file defines `PayTheoryPaymentProcessor`, a subclass of `CardPaymentProcessor`. It implements the methods Canvas calls throughout a payment workflow: rendering the tokenization forms, charging a card, and listing/adding/removing a patient's saved cards. Card data is tokenized client-side by Pay Theory's JS SDK, so the plugin never handles raw card numbers.

**Core Logic**

- `payment_form` / `add_card_form` render the Pay Theory JS SDK form (via a Django template) for paying or saving a card.
- `charge` sends the tokenized payment method to Pay Theory's GraphQL API and maps the result onto a `CardTransaction`, treating `PENDING`/`SETTLED`/`SUCCESS`/`SUCCEEDED` statuses as successful.
- `payment_methods` maps a patient to a Pay Theory payor (via `canvas_patient_id` metadata) and returns their saved cards as `PaymentMethod` effects.
- `add_payment_method` / `remove_payment_method` save and disable cards for the patient's payor.

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


class PayTheoryPaymentProcessor(CardPaymentProcessor):
    """Custom payment processor for handling credit card payments with PayTheory."""

    def payment_form(self, patient: Patient | None = None) -> PaymentProcessorForm:
        content = render_to_string(
            "templates/form.html",
            {
                "intent": self.PaymentIntent.PAY,
                "public_api_key": self.public_api_key,
                "sdk_url": self.sdk_url,
            },
        )
        return PaymentProcessorForm(content=content, intent=self.PaymentIntent.PAY)

    def charge(
        self, amount: Decimal, token: str, patient: Patient | None = None, **kwargs: Any
    ) -> CardTransaction:
        transaction = self.api.create_transaction(
            TransactionInput(payment_method_id=token, amount=amount)
        )
        status = (transaction.get("status") or "").upper()
        return CardTransaction(
            success=status in SUCCESS_STATUSES,
            transaction_id=transaction["transaction_id"],
            api_response=transaction,
        )

    def payment_methods(self, patient: Patient | None = None) -> list[PaymentMethod]:
        if not patient:
            return []
        payor_id = self.get_or_create_payor_id(patient)
        if not payor_id:
            return []
        return [self._to_payment_method(m) for m in self.api.get_payment_methods(payor_id=payor_id)]

    def add_payment_method(
        self, token: str, patient: Patient, **kwargs: Any
    ) -> AddPaymentMethodResponse:
        return AddPaymentMethodResponse(success=True)

    def remove_payment_method(self, token: str, patient: Patient) -> RemovePaymentMethodResponse:
        result = self.api.disable_payment_method(payment_method_id=token)
        return RemovePaymentMethodResponse(success=result)
```

The excerpt above is abridged; see the [source on GitHub](https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/paytheory-payment-processor) for the full implementation, the Pay Theory API client, and the form template.

<br/>
<br/>
<br/>
