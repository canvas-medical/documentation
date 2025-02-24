---
title: "Billing Line Item"
slug: "data-billing-line-item"
excerpt: "Canvas SDK Billing Line Item"
hidden: false
---

## Introduction

The `BillingLineItem` model represents billing line items linked to [Notes](/sdk/data-note) that can be found in the note footer. BillingLineItems are also linked to [Patient](/sdk/data-patient/#patient) instances.

## Usage

The `BillingLineItem` model can be used to find all of the billable codes linked to a patient note. For example, to find all of the current billing line items for a note, the `Note.billing_line_items` method can be used:

```python
>>> from canvas_sdk.v1.data.note import Note
>>> from canvas_sdk.v1.data.billing import BillingLineItemStatus
>>> note_1 = Note.objects.get(id="a74592ae8a6c4d0ebe0799d3fb3713d1")
>>> note_1_billing_line_items = note_1.billing_line_items.filter(status=BillingLineItemStatus.ACTIVE)
>>> print([item.cpt for item in note_1_billing_line_items])
['99213', '90703']
```

Alternatively, you could find all the `BillingLineItem` instances for a single `Patient`:

```python
>>> from canvas_sdk.v1.data.patient import Patient
>>> patient_1 = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> patient_billing_line_items = patient_1.billing_line_items.all()
>>> print([item.cpt for item in patient_billing_line_items])
['99213', '90703', '76942', '67505']
```

You can also access all `BillingLineItemModifier`s associated with a `BillingLineItem`:

```python
>>> from canvas_sdk.v1.data.billing import BillingLineItem, BillingLineItemModifier
>>> line_item = BillingLineItem.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")
>>> line_item_modifiers = line_item.modifiers.all()
>>> print([mod.code for mod in line_item_modifiers])
['25', '59']
```

## Filtering

The `filter` method can be used to filter by desired attributes. The following examples show commonly used operations to filter billing line item data:

**Show a Patient's active BillingLineItems that start with '99-' in order of descending charge amount**

```python
>>> from canvas_sdk.v1.data.patient import Patient
>>> from canvas_sdk.v1.data.billing import BillingLineItemStatus
>>> patient_1 = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> office_visit_charges = patient_1.billing_line_items.filter(status=BillingLineItemStatus.ACTIVE, cpt__startswith='99').order_by("charge")
>>> print([(item.cpt, item.charge,) for item in office_visit_charges])
[('99215', 200.00), ('99215', 190.00), ('99214', 100.00), ('99213', 80.00)]
```

**Find All Removed BillingLineItems from a Note**

```python
>>> import arrow
>>> from canvas_sdk.v1.data.note import Note
>>> from canvas_sdk.v1.data.billing import BillingLineItemStatus
>>> note_1 = Note.objects.get(id="a74592ae8a6c4d0ebe0799d3fb3713d1")
>>> note_1_removed_items = note_1.billing_line_items.filter(status=BillingLineItemStatus.REMOVED)
>>> print([item.cpt for item in note_1_removed_items])
['11901', '00950']
```

For examples of how to use the BillingLineItem data class with the BillingLineItem effects, check out [this page](sdk/effect-billing-line-items)

## Attributes

### BillingLineItem

| Field Name   | Type                                             |
| ------------ | ------------------------------------------------ |
| id           | UUID                                             |
| dbid         | Integer                                          |
| created      | DateTime                                         |
| modified     | DateTime                                         |
| note         | [Note](/sdk/data-note)                           |
| patient      | [Patient](/sdk/data-patient/#patient)            |
| cpt          | String                                           |
| charge       | Decimal                                          |
| description  | String                                           |
| units        | Integer                                          |
| command_type | String                                           |
| command_id   | Integer                                          |
| status       | [BillingLineItemStatus ](#billinglineitemstatus) |

### BillingLineItemModifier

| Field Name    | Type                                |
| ------------- | ----------------------------------- |
| dbid          | Integer                             |
| line_item     | [BillingLineItem](#billinglineitem) |
| system        | String                              |
| version       | String                              |
| code          | String                              |
| display       | String                              |
| user_selected | Boolean                             |

## Enumeration types

### BillingLineItemStatus

| Value   | Label   |
| ------- | ------- |
| ACTIVE  | Active  |
| REMOVED | Removed |
