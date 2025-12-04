---
title: "ChargeDescriptionMaster"
slug: "data-charge-description-master"
excerpt: "Canvas SDK ChargeDescriptionMaster"
hidden: false
---

## Introduction

The `ChargeDescriptionMaster` model represents a billing charge in Canvas that can be added to the note footer.

## Usage

The `ChargeDescriptionMaster` model can be filtered by any of its attributes, including `cpt_code`, `name`, and `short_name`:

```python
>>> from canvas_sdk.v1.data import ChargeDescriptionMaster
>>> office_visit_charges = ChargeDescriptionMaster.objects.filter(cpt_code__startswith="99")
>>> print([charge.short_name for charge in office_visit_charges])
["Office outpatient visit 40 minutes", "Office outpatient visit 25 minutes", "Office outpatient visit 10 minutes"]
```

You can also access `PayorSpecificCharge`s from the `ChargeDescriptionMaster` model:

```python
>>> from canvas_sdk.v1.data import ChargeDescriptionMaster
>>> office_visit_40min = ChargeDescriptionMaster.objects.filter(cpt_code="99215").first()
>>> payor_specific_charges = office_visit_40min.transactor_charges.all()
>>> print([charge.transactor.name for charge in payor_specific_charges])
["Aetna", "Medicare", "Blue Shield of CA"]
```

`

## Attributes

### ChargeDescriptionMaster

| Field Name     | Type                            |
| -------------- | ------------------------------- |
| dbid           | Integer                         |
| cpt_code       | String                          |
| name           | String                          |
| short_name     | String                          |
| charge_amount  | Decimal                         |
| effective_date | Date                            |
| end_date       | Date                            |
| code_system    | [CDMCodeSystem](#cdmcodesystem) |
| ndc_code       | String                          |

## Enumeration types

### CDMCodeSystem

| Value    | Label    |
| -------- | -------- |
| INTERNAL | Internal |
| CPT      | CPT      |
