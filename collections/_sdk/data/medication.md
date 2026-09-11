---
title: "Medication"
slug: "data-medication"
excerpt: "Canvas SDK Medication"
hidden: false
---

## Introduction

The `Medication` model represents a record of a medication that is being consumed by a patient, either now, in the past, or in the future. `Medication` records can represent both prescriptions and medication statements for a patient.

## Basic usage

To get a medication by identifier, use the `get` method on the `Medication` model manager:

```python
from canvas_sdk.v1.data.medication import Medication

medication = Medication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the medications for a patient can be accessed with the `medications` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
medications = patient.medications.all()
```

If you have a patient ID, you can get the medications for the patient with the `for_patient` method on the `Medication` model manager:

```python
from canvas_sdk.v1.data.medication import Medication

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
medication = Medication.objects.for_patient(patient_id)
```

# Codings

The codings for a medication can be accessed with the `codings` attribute on an `Medication` object:

```python
from canvas_sdk.v1.data.medication import Medication
from logger import log

medication = Medication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in medication.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Filtering

Medications can be filtered by any attribute that exists on the model.

Filtering for medications is done with the `filter` method on the `Medication` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.medication import Medication

medications = Medication.objects.filter(status="active")
```

### By ValueSet

See [Value Sets](/sdk/data-value-sets/) for the library of built-in value sets and how to create your own.

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.medication import Medication
from canvas_sdk.value_set.v2022.medication import AdhdMedications

medications = Medication.objects.find(AdhdMedications)
```

## Latest sig

The `latest_sig` property returns a medication's most recent sig — its directions for use — as a string. It draws on three sources: the medication's active prescriptions, its [change medications](/sdk/data-change-medication/) that are not entered in error, and its [medication statements](/sdk/data-medication-statement/). It returns the sig from whichever of those is most recent. Because `latest_sig` is a property computed in Python, it is read from each `Medication` object and is not available to a queryset `.filter()` or `.order_by()`.

When both an active prescription and a change medication exist, the source whose [note](/sdk/data-note/) has the later date of service wins. Otherwise the sig comes from the first source that has one, in this order:

1. The latest prescription.
2. The latest change medication.
3. The latest medication statement.

The latest source is the one with the highest `dbid`. A prescription contributes its `combined_sig` (its sig text, plus a maximum daily dose when one is set); a change medication or medication statement contributes its sig text. When no source has a sig, `latest_sig` returns an empty string.

```python
from canvas_sdk.v1.data.medication import Medication

medication = Medication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
sig = medication.latest_sig  # "" when no source has a sig
```

### Sig across many medications

Reading `latest_sig` on each medication in a queryset issues a separate query per medication for the prescriptions, change medications, and medication statements `latest_sig` inspects. The `with_latest_sig` method prefetches those sources, so `latest_sig` resolves without a per-medication query:

```python
from canvas_sdk.v1.data.medication import Medication

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
medications = Medication.objects.for_patient(patient_id).with_latest_sig()

for medication in medications:
    sig = medication.latest_sig
```

## Attributes

### Medication

| Field Name                     | Type                                                     |
| ------------------------------ | -------------------------------------------------------- |
| id                             | UUID                                                     |
| dbid                           | Integer                                                  |
| patient                        | [Patient](/sdk/data-patient/#patient)                    |
| entered_in_error               | [CanvasUser](/sdk/data-canvasuser)                       |
| committer                      | [CanvasUser](/sdk/data-canvasuser)                       |
| status                         | String                                                   |
| start_date                     | Date                                                     |
| end_date                       | Date                                                     |
| quantity_qualifier_description | String                                                   |
| clinical_quantity_description  | String                                                   |
| potency_unit_code              | String                                                   |
| national_drug_code             | String                                                   |
| erx_quantity                   | String                                                   |
| codings                        | [MedicationCoding](#medicationcoding)[]                  |
| medication_statements          | [MedicationStatement](/sdk/data-medication-statement)[]  |
| change_medications             | [ChangeMedication](/sdk/data-change-medication)[]        |
| stopmedicationevent_set        | [StopMedicationEvent](/sdk/data-stop-medication-event)[] |
| prescriptions                  | [Prescription](/sdk/data-prescription)[]                 |
| previous_medications           | [Prescription](/sdk/data-prescription)[]                 |
| prescription_change_responses  | [PrescriptionChangeResponse](/sdk/data-prescription-change-response/#prescriptionchangeresponse)[] |
| latest_sig                     | String (property) — see [Latest sig](#latest-sig)        |

### MedicationCoding

| Field Name    | Type                      |
| ------------- | ------------------------- |
| dbid          | Integer                   |
| system        | String                    |
| version       | String                    |
| code          | String                    |
| display       | String                    |
| user_selected | Boolean                   |
| medication    | [Medication](#medication) |

<br/>
<br/>
<br/>
