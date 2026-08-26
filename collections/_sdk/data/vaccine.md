---
title: "Vaccine"
slug: "data-vaccine"
excerpt: "Canvas SDK Vaccine"
hidden: false
---

## Introduction

The `Vaccine` model represents an entry in a Canvas instance's vaccine catalog — what a
provider can choose when documenting an [Immunize](/sdk/commands/#immunize) command.
`VaccineLot` represents a physical lot of one of those vaccines, along with how many doses
remain on hand.

## Basic usage

A vaccine carries the CPT and CVX codes that identify it. The CVX code is on the vaccine;
the CPT codes come from its charges, and those charges are what produce the billing line
item when an [Immunize](/sdk/commands/#immunize) command is committed.

```python?partial=true
from canvas_sdk.v1.data import Vaccine

vaccine = Vaccine.objects.filter(active=True, cvx_code="135").first()
print(vaccine.cvx_code, [charge.cpt_code for charge in vaccine.charges.all()])
# 135 ["90662"]
```

Each physical lot of a vaccine tracks how many doses remain, and committing an Immunize
command decrements that count:

```python?partial=true
from canvas_sdk.v1.data import VaccineLot

lot = VaccineLot.objects.filter(lot_number="LOT-135-001").first()
print(lot.vaccine.short_name, lot.on_hand_inventory, lot.expiration_date)
# Fluzone High-Dose 25 2027-06-30
```

`mvx_code` holds a CDC MVX manufacturer code. The codes are declared as the field's
choices, so Django's display helper resolves the manufacturer name:

```python?partial=true
from canvas_sdk.v1.data import VaccineLot

lot = VaccineLot.objects.filter(lot_number="LOT-135-001").first()
print(lot.mvx_code, "->", lot.get_mvx_code_display())
# ASZ -> AstraZeneca
```

Some instances record a single stock figure on the vaccine itself rather than tracking
lots. That value lives in `Vaccine.inventory` as free text and is independent of
`VaccineLot.on_hand_inventory`.

## Filtering

A vaccine is selectable on a note when it is active **and** carries an active CPT charge.
Filtering the same way keeps a plugin in step with what a provider would see:

```python?partial=true
from datetime import date

from django.db.models import Q

from canvas_sdk.v1.data import Vaccine

today = date.today()
selectable = Vaccine.objects.filter(
    Q(active=True),
    Q(charges__effective_date__lte=today),
    Q(charges__end_date__isnull=True) | Q(charges__end_date__gte=today),
).distinct()
print([vaccine.short_name for vaccine in selectable])
# ["Fluzone High-Dose", "Trumenba", "Prevnar 13™"]
```

Lots are administrable while they have doses on hand:

```python?partial=true
from canvas_sdk.v1.data import VaccineLot

in_stock = VaccineLot.objects.filter(vaccine__cvx_code="135", on_hand_inventory__gt=0)
print([(lot.lot_number, lot.on_hand_inventory) for lot in in_stock])
# [("LOT-135-001", 25)]
```

## Attributes

### Vaccine

| Field Name | Type                                                                                              |
|------------|---------------------------------------------------------------------------------------------------|
| id         | UUID                                                                                              |
| dbid       | Integer                                                                                           |
| created    | DateTime                                                                                          |
| modified   | DateTime                                                                                          |
| payer      | [Transactor](/sdk/data-coverage/#transactor)                                                      |
| charges    | QuerySet[[ChargeDescriptionMaster](/sdk/data-charge-description-master/#chargedescriptionmaster)] |
| cvx_code   | String                                                                                            |
| name       | String                                                                                            |
| short_name | String                                                                                            |
| inventory  | String                                                                                            |
| ndc_code   | String                                                                                            |
| mvx_code   | [VaccineManufacturer](#vaccinemanufacturer)                                                       |
| route      | String                                                                                            |
| active     | Boolean                                                                                           |
| units      | Integer                                                                                           |
| lots       | QuerySet[[VaccineLot](#vaccinelot)]                                                               |

A vaccine may appear more than once for the same `cvx_code` — instances commonly carry a
payer-specific entry alongside a general one. Use `payer` to tell them apart.

### VaccineLot

| Field Name              | Type                                        |
|-------------------------|---------------------------------------------|
| id                      | UUID                                        |
| dbid                    | Integer                                     |
| created                 | DateTime                                    |
| modified                | DateTime                                    |
| vaccine                 | [Vaccine](#vaccine)                         |
| lot_number              | String                                      |
| ndc_code                | String                                      |
| mvx_code                | [VaccineManufacturer](#vaccinemanufacturer) |
| expiration_date         | Date                                        |
| diluent_lot_number      | String                                      |
| diluent_expiration_date | Date                                        |
| starting_inventory      | Integer                                     |
| quantity_adjustment     | Integer                                     |
| adjustment_notes        | String                                      |
| on_hand_inventory       | Integer                                     |
| used_inventory          | Integer                                     |

`on_hand_inventory` is derived from `starting_inventory + quantity_adjustment -
used_inventory`.

## Enumeration types

### VaccineManufacturer

CDC MVX manufacturer codes. Prefer `get_mvx_code_display()` over mapping these yourself.

| Value | Label                                                        |
| ----- | ------------------------------------------------------------ |
| ASZ   | AstraZeneca                                                  |
| BBI   | Bharat Biotech International Limited                         |
| BN    | Bavarian Nordic A/S                                          |
| BTP   | Biotest Pharmaceuticals Corporation                          |
| CAN   | CanSino Biologics, Inc                                       |
| DVC   | DynPort Vaccine Company, LLC                                 |
| DVX   | Dynavax, Inc                                                 |
| GEO   | GeoVax Labs, Inc                                             |
| GRF   | Grifols                                                      |
| IDB   | ID Biomedical                                                |
| JNJ   | Johnson and Johnson                                          |
| JSN   | Janssen                                                      |
| KED   | Kedrion Biopharma                                            |
| KGC   | Korea Green Cross Corporation                                |
| MBL   | Massachusetts Biologic Laboratories                          |
| MDO   | Medicago, Inc                                                |
| MED   | MedImmune, Inc. (AstraZeneca)                                |
| MIP   | Emergent BioSolutions                                        |
| MOD   | Moderna US, Inc                                              |
| MSD   | Merck and Co., Inc                                           |
| MSP   | MSP Vaccine Company - (partnership Merck and Sanofi Pasteur) |
| NAB   | NABI                                                         |
| NVX   | Novavax, Inc                                                 |
| OTH   | Other manufacturer                                           |
| PAX   | Emergent Travel Health, Inc (Formerly PaxVax)                |
| PFR   | Pfizer, Inc                                                  |
| PMC   | Sanofi Pasteur                                               |
| PSC   | Protein Sciences                                             |
| SEQ   | Seqirus                                                      |
| SKB   | GlaxoSmithKline                                              |
| SNV   | Sinovac                                                      |
| SPH   | Sinopharm-Biotech                                            |
| TVA   | TEVA Pharmaceuticals USA                                     |
| UNK   | Unknown manufacturer                                         |
| VAL   | Valneva                                                      |
| VBI   | VBI Vaccines, Inc                                            |
| WAL   | Wyeth                                                        |
