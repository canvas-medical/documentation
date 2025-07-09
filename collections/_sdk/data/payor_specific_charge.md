---
title: "Payor Specific Charge"
slug: "data-payor-specific-charge"
excerpt: "Canvas SDK Payor Specific Charge"
hidden: false
---

## Introduction

The `PayorSpecificCharge` model represents charges specific to a [Transactor](/sdk/data-coverage/#transactor) in Canvas.

## Usage

The `PayorSpecificCharge` model can be used to find all of the charges specific to a single `Transactor`:

```python
>>> from canvas_sdk.v1.data import PayorSpecificCharge, Transactor
>>> aetna = Transactor.objects.get(payer_id="60054")
>>> aetna_charges = PayorSpecificCharge.objects.filter(transactor=aetna)
>>> print([charge.charge_amount for charge in aetna_charges])
[150.00, 40.00, 99.99]
```

You can also access a transactor's specific charges from the `Transactor` model:

```python
>>> from canvas_sdk.v1.data import Transactor
>>> aetna = Transactor.objects.get(payer_id="60054")
>>> aetna_charges = aetna.specific_charges.all()
>>> print([charge.charge_amount for charge in aetna_charges])
[150.00, 40.00, 99.99]
```

`

## Attributes

### PayorSpecificCharge

| Field Name            | Type                                                           |
| --------------------- | -------------------------------------------------------------- |
| dbid                  | Integer                                                        |
| transactor            | [Transactor](/sdk/data-coverage/#transactor)                   |
| charge                | [ChargeDescriptionMaster](/sdk/data-charge-description-master) |
| charge_amount         | Decimal                                                        |
| effective_date        | Date                                                           |
| end_date              | Date                                                           |
| part_of_capitated_set | Boolean                                                        |
