---
title: "CompoundMedication"
slug: "data-compound-medication"
excerpt: "Canvas SDK CompoundMedication"
hidden: false
---

## Introduction

The `CompoundMedication` model represents a compound medication formulation that can be prescribed to patients.
Compound medications are customized medications mixed or prepared by a compounding pharmacy according to a prescription.

## Basic usage

To get a compound medication by identifier, use the `get` method on the `CompoundMedication` model manager:

```python
from canvas_sdk.v1.data.compound_medication import CompoundMedication

compound_medication = CompoundMedication.objects.get(id="123")
```

## Filtering

Compound medications can be filtered by any attribute that exists on the model.

Filtering for compound medications is done with the `filter` method on the `CompoundMedication` model manager.

### By attribute

Specify attributes with `filter` to filter by those attributes:

```python
from canvas_sdk.v1.data.compound_medication import CompoundMedication

# Get all active compound medications
active_medications = CompoundMedication.objects.filter(active=True)

# Get compound medications by formulation
compound_medications = CompoundMedication.objects.filter(formulation="Testosterone 200mg/mL in Grapeseed Oil")

# Get all Schedule II controlled substances
schedule_ii_medications = CompoundMedication.objects.filter(controlled_substance="II")

# Get compound medications by potency unit
tablet_medications = CompoundMedication.objects.filter(potency_unit_code="C48542")
```

### Multiple filters

You can combine multiple filters:

```python
from canvas_sdk.v1.data.compound_medication import CompoundMedication

# Get active compound medications that are controlled substances
controlled_active = CompoundMedication.objects.filter(
  active=True,
  controlled_substance__in=["II", "III", "IV", "V"]
)
```

## Attributes

### CompoundMedication

| Field Name               | Type                                                        |
| ------------------------ | ----------------------------------------------------------- |
| dbid                     | Integer                                                     |
| active                   | Boolean                                                     |
| formulation              | String                                                      |
| potency_unit_code        | [PotencyUnit](#potencyunit)                                 |
| controlled_substance     | [ControlledSubstanceSchedule](#controlledsubstanceschedule) |
| controlled_substance_ndc | String                                                      |

## Enumeration types

### PotencyUnit

| Value   | Label       |
| ------- | ----------- |
| C62412  | Applicator  |
| C54564  | Blister     |
| C64696  | Caplet      |
| C48480  | Capsule     |
| C64933  | Each        |
| C53499  | Film        |
| C48155  | Gram        |
| C69124  | Gum         |
| C48499  | Implant     |
| C62276  | Insert      |
| C48504  | Kit         |
| C120263 | Lancet      |
| C48506  | Lozenge     |
| C28254  | Milliliter  |
| C48521  | Packet      |
| C65032  | Pad         |
| C48524  | Patch       |
| C120216 | Pen Needle  |
| C62609  | Ring        |
| C53502  | Sponge      |
| C53503  | Stick       |
| C48538  | Strip       |
| C48539  | Suppository |
| C53504  | Swab        |
| C48542  | Tablet      |
| C48548  | Troche      |
| C38046  | Unspecified |
| C48552  | Wafer       |

### ControlledSubstanceSchedule

| Key                    | Value | Label        |
| ---------------------- | ----- | ------------ |
| SCHEDULE_NOT_SCHEDULED | N     | None         |
| SCHEDULE_II            | II    | Schedule II  |
| SCHEDULE_III           | III   | Schedule III |
| SCHEDULE_IV            | IV    | Schedule IV  |
| SCHEDULE_V             | V     | Schedule V   |

## Notes

- The `formulation` field has a maximum length of 105 characters (as defined by Surescripts).

<br/>
<br/>
<br/>
