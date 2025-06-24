---
title: "Payment Processors"
slug: "handlers-payment-processors"
excerpt: "Framework for defining custom payment processors using the Canvas SDK."
---
The Canvas SDK provides a way to define custom payment processors that enables Canvas to:
* Handle payment-related workflows within the platform
* Integrate with third-party payment providers
* Manage payment methods for patients

Custom payment processors enable flexibility, allowing developers to replace Stripe with other payment providers. 
Currently, only credit card payment processors are supported.


## Payment Processor Handler

All payment processors are implemented as subclasses of the abstract `PaymentProcessor` handler. This defines the base contract for:

* Selecting a processor
* Charging payments
* Listing, adding, and removing payment methods

You can find it in:

```python
from canvas_sdk.handlers.payment_processors.base import PaymentProcessor
```

---

## CardPaymentProcessor

If your custom processor deals with card payments, extend the `CardPaymentProcessor`, which provides additional structure.

```python
from canvas_sdk.handlers.payment_processors.card import CardPaymentProcessor
```

In the plugin, this is implemented as:

```python
class PayTheoryPaymentProcessor(CardPaymentProcessor):
    ...  # Your implementation here
```

---

## Defining a `CardPaymentProcessor`

When implementing a `CardPaymentProcessor`, you must define how Canvas should display forms for adding and charging cards, how to process those payments, and how to manage saved payment methods.

In order to implement a `CardPaymentProcessor`, you should override and implement the following methods grouped into three main categories: 
* Displaying forms
* Charging a card
* Managing payment methods

### Displaying Forms

The forms you return via `PaymentProcessorForm` are rendered directly as **inner HTML** within the Canvas application. These forms must define a small contract of JavaScript behaviors to allow Canvas to communicate with them.

These methods define the HTML content that will be rendered inside Canvas to collect card data for payments or adding new cards. They must comply with the [Form Workflow](#form-workflow).

#### 1. Payment Form

Triggered when a user selects the credit card payment option. 
This method should return the HTML form used to collect and tokenize the payment details.

```python
def payment_form(self, patient: Patient | None = None) -> PaymentProcessorForm:
    content = render_to_string("templates/payment_form.html")
    return PaymentProcessorForm(intent="pay", content=content)
```

---

#### 2. Add Card Form

Triggered when a user initiates the process of adding a new card to a patient's saved payment methods. 
This method should return the HTML form used to collect and tokenize the new card information.

```python
def add_payment_method_form(self, patient: Patient | None = None) -> PaymentProcessorForm:
    content = render_to_string(
        "templates/add_card_form.html",
        {"payor_id": self.api.get_default_payor_id()},
    )
    return PaymentProcessorForm(intent="add_card", content=content)
```

---

### 3. Charge

Handles the actual payment. This method is triggered after tokenization and is responsible for charging the card:

```python
def charge(self, token: str, patient: Patient, amount: Decimal) -> CardTransaction:
    payload = {
        "token": token,
        "amount": int(amount * 100),
        "currency": "usd",
        "metadata": {"patient_id": patient.id},
    }
    result = self.api.charge(payload)

    return CardTransaction(
        transaction_id=result["transaction_id"],
        success=True,
        api_response=result,
    )
```

---

### 4. Managing Payment Methods

These methods define how Canvas lists, stores, and deletes saved cards associated with a patient.

#### 4.1 List

```python
def list_payment_methods(self, patient: Patient) -> list[PaymentMethod]:
   return [
            PaymentMethod(
                payment_method_id="pm_1",
                brand="Visa",
                expiration_year=2025,
                expiration_month=12,
                card_holder_name="John Doe",
                postal_code="12345",
                card_last_four_digits="1234",
            )
        ]
```

#### 4.2. Add

```python
def add_payment_method(self, token: str, patient: Patient) -> AddPaymentMethodResponse:
    return AddPaymentMethodResponse(success=success)
```

#### 4.3. Remove

```python
def remove_payment_method(self, payment_method_id: str, patient: Patient) -> RemovePaymentMethodResponse:
    return RemovePaymentMethodResponse(success=success)
```

---

## Form Workflow

Payment and Add Card forms are rendered as inner HTML inside Canvas. These forms must implement the following communication contract via JavaScript:

### 1. Notify readiness

This should be called once the form has fully loaded and is ready for user interaction. Canvas waits for this signal to show the form.

```js
window.parent.setFormIsReady();
````

### 2. Submit token after success

Once the card details are validated and tokenized, this method must be called to pass the token back to Canvas. 
This token will then be used to charge or store the card.

```js
window.parent.setToken("tok_123abc");
```

### 3. Report validation status

Call this every time the validity of the form changes (e.g., input becomes valid or invalid). 
Canvas uses this to enable or disable the ability to submit the form programmatically.

```js
window.parent.setFormIsValid(true); // or false
```

### 4. Handle errors

Call this to notify Canvas of any form-level errors (e.g., failed tokenization, invalid input). 
The message should help users understand what went wrong.

```js
window.parent.setError("Invalid card details");
```

### 5. Submit button

The HTML form must include a button with `id="submit"`. 
This button is required, should remain hidden from the user, and will be clicked programmatically by Canvas when the form is considered valid and ready to be submitted.

```html
<button type="submit" id="submit" hidden>Submit</button>
```

### 6. Define teardown function

This function will be called automatically when the form is unmounted or replaced. Use it to remove any event listeners or free up memory/resources.

```js
window.teardown = () => {
  // Cleanup listeners, state, etc.
};
```

---

## Tokenization Flow

Tokenization is the process where the sensitive card information is securely transformed into a token that can be safely used by Canvas to perform charges or save cards.

When implementing a payment processor, it's expected that your HTML forms integrate with your provider's frontend SDK to:

- Collect and validate card input
- Tokenize the card using the provider's secure API
- Call `window.parent.setToken(token)` with the result

Canvas does not handle raw card input. Tokenization **must** be handled entirely by the payment provider's frontend tools within the form.

Before building a plugin, ensure:

- Your provider offers secure frontend tokenization
- You can integrate with their JavaScript SDK
- You can submit token data from the form via `setToken`

---

## Paytheory Payment Plugin Implementation

A reference plugin that implements a custom payment processor using **PayTheory** is available [here]()
This plugin can serve as an example for building a custom processor that replaces the standard Stripe implementation.
