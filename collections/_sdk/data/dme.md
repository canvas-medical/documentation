---
title: "DME"
slug: "data-dme"
excerpt: "Canvas SDK DmeProduct and DmeOrder"
hidden: false
---

## Introduction

The DME data models let a plugin read the durable medical equipment (DME) that providers order with the [OrderDme](/sdk/commands/#orderdme) command:

- `DmeProduct` is an item on your instance's DME formulary. Its `id` is the value `OrderDmeCommand` takes as `dme_product_id`, so a plugin can find a product by its code or name instead of hard-coding the ID.
- `DmeOrder` is the record a signed Order DME command creates. It keeps the ordered item, indications, quantity, supplier, and ordering provider, along with the patient's height and weight when the order was signed.

Both models are read-only. Admins manage the formulary in the Django Admin UI under **DME Products**.

## Basic usage

### Find a formulary product

Filter `DmeProduct` by code, and include `active=True`, because the Order DME command only accepts active products:

```python
from canvas_sdk.v1.data import DmeProduct

wheelchair = DmeProduct.objects.filter(code="K0001", active=True).first()
```

A product can have no code, and two products can share one, so check that the lookup found a product before you use it. To match on the product name instead, use `name__icontains`.

### Order a formulary product

Pass the product's `id` as `dme_product_id`:

```python
from canvas_sdk.commands import OrderDmeCommand
from canvas_sdk.v1.data import DmeProduct

wheelchair = DmeProduct.objects.filter(code="K0001", active=True).first()

if wheelchair:
    order = OrderDmeCommand(
        note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
        dme_product_id=str(wheelchair.id),
        diagnosis_codes=["R262"],
        quantity=1,
        ordering_provider_key="b8a7c6d5-4e3f-4a2b-9c1d-0e8f7a6b5c4d",
    )
```

### Read signed orders

To get an order by identifier, use the `get` method on the `DmeOrder` model manager:

```python
from canvas_sdk.v1.data import DmeOrder

order = DmeOrder.objects.get(id="3c9e2f4a-6b1d-4e8a-9f7c-5d2b0a1e8c63")
```

If you have a patient object, the patient's orders are available from the `dme_orders` attribute:

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
orders = patient.dme_orders.all()
```

A `DmeOrder` is the [anchor object](/sdk/data-command/#the-anchor-object) of its `orderDme` command, so you can also reach it from the command:

```python
from canvas_sdk.v1.data import Command

command = Command.objects.get(id="c1b5a4d2-7e3f-4a8b-9c6d-2f1e0a9b8c7d")
order = command.anchor_object
```

## Filtering

DME products and orders can be filtered by any attribute that exists on the model.

### Products by code system

`code_system` is a `DmeProductCodeSystem` value: `HCPCS` for Healthcare Common Procedure Coding System (HCPCS) codes, or `INTERNAL` for codes your organization assigns:

```python
from canvas_sdk.v1.data import DmeProduct, DmeProductCodeSystem

hcpcs_products = DmeProduct.objects.filter(code_system=DmeProductCodeSystem.HCPCS, active=True)
```

### Committed orders

The `committed` method returns orders that have been committed and not entered in error:

```python
from canvas_sdk.v1.data import DmeOrder

committed_orders = DmeOrder.objects.committed()
```

## What a signed order records

Canvas copies the item into the order when the command is signed, so later formulary changes don't change an existing order:

- For a formulary product, `product` links to the `DmeProduct`, and `item_name`, `item_code`, and `item_code_system` hold the product's values at signing.
- For an off-formulary item, `product` is `None`, `item_name` holds the `free_text_item` text, and `item_code` and `item_code_system` are empty strings.

`indications` is a list of the diagnoses the order was placed for, each a dictionary with `code` and `display` keys.

`patient_height` and `patient_weight` hold the patient's latest committed height and weight as display text with units, such as `"70 in"` and `"10 lbs, 8 oz"`. Each is an empty string when the patient had no reading at signing.

## Attributes

### DmeProduct

| Field Name  | Type                                            |
|-------------|-------------------------------------------------|
| id          | UUID                                            |
| dbid        | Integer                                         |
| name        | String                                          |
| code        | String                                          |
| code_system | [DmeProductCodeSystem](#dmeproductcodesystem)   |
| active      | Boolean                                         |
| orders      | [DmeOrder](#dmeorder)[]                         |

### DmeOrder

| Field Name        | Type                                                  |
|-------------------|-------------------------------------------------------|
| id                | UUID                                                  |
| dbid              | Integer                                               |
| created           | DateTime                                              |
| modified          | DateTime                                              |
| originator        | [CanvasUser](/sdk/data-canvasuser)                    |
| committer         | [CanvasUser](/sdk/data-canvasuser)                    |
| entered_in_error  | [CanvasUser](/sdk/data-canvasuser)                    |
| deleted           | Boolean                                               |
| patient           | [Patient](/sdk/data-patient/#patient)                 |
| note              | [Note](/sdk/data-note/#note)                          |
| product           | [DmeProduct](#dmeproduct)                             |
| item_name         | String                                                |
| item_code         | String                                                |
| item_code_system  | String                                                |
| indications       | JSON                                                  |
| quantity          | Integer                                               |
| length_of_need    | String                                                |
| supplier          | [ServiceProvider](/sdk/data-serviceprovider/)         |
| ordering_provider | [Staff](/sdk/data-staff/#staff)                       |
| patient_height    | String                                                |
| patient_weight    | String                                                |

### DmeProductCodeSystem

| Value    | Label    |
|----------|----------|
| HCPCS    | HCPCS    |
| INTERNAL | Internal |

<br/>
<br/>
<br/>
