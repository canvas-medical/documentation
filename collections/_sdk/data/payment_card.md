---
title: "PaymentCard"
slug: "data-payment-card"
excerpt: "Canvas SDK PaymentCard"
hidden: false
---

## Introduction

The `PaymentCard` model represents a patient's stored payment card on file. Cards are tokenized and stored by Canvas's payment processor, and this model exposes only the non-sensitive card metadata — brand, last four digits, expiration, cardholder name, and whether the card is the patient's default. The underlying processor token is never exposed through the SDK.

Reference a `PaymentCard` by its Canvas `id` when charging a patient's card on file with the [Charge Stored Card](/sdk/effect-charge-stored-card/) effect.

## Basic usage

Each `PaymentCard` is linked to a [Patient](/sdk/data-patient/#patient). Access a patient's stored cards through the `payment_cards` reverse relation:

```python
>>> from canvas_sdk.v1.data import Patient
>>> patient = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> cards = patient.payment_cards.all()
>>> print([(card.brand, card.card_last_four_digits, card.is_default) for card in cards])
[('visa', '4242', True), ('mastercard', '5555', False)]
```

To retrieve the patient's default card:

```python
>>> from canvas_sdk.v1.data import Patient
>>> patient = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> default_card = patient.payment_cards.filter(is_default=True).first()
```

## Attributes

### PaymentCard

| Field Name            | Type                                  |
| --------------------- | ------------------------------------- |
| id                    | UUID                                  |
| dbid                  | Integer                               |
| created               | DateTime                              |
| modified              | DateTime                              |
| patient               | [Patient](/sdk/data-patient/#patient) |
| brand                 | String                                |
| card_last_four_digits | String                                |
| expiration_month      | String                                |
| expiration_year       | String                                |
| card_holder_name      | String                                |
| postal_code           | String                                |
| is_default            | Boolean                               |

<br/>
<br/>
<br/>
