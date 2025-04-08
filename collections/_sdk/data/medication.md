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

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.medication import Medication
from canvas_sdk.value_set.v022.medication import AdhdMedications

medications = Medication.objects.find(AdhdMedications)
```

## Attributes

### Medication

| Field Name                     | Type                                    |
|--------------------------------|-----------------------------------------|
| id                             | UUID                                    |
| dbid                           | Integer                                 |
| patient                        | [Patient](/sdk/data-patient/#patient)   |
| deleted                        | Boolean                                 |
| entered_in_error               | [CanvasUser](/sdk/data-canvasuser)      |
| committer                      | [CanvasUser](/sdk/data-canvasuser)      |
| status                         | String                                  |
| start_date                     | Date                                    |
| end_date                       | Date                                    |
| quantity_qualifier_description | String                                  |
| clinical_quantity_description  | String                                  |
| potency_unit_code              | String                                  |
| national_drug_code             | String                                  |
| erx_quantity                   | String                                  |
| codings                        | [MedicationCoding](#medicationcoding)[] |

### MedicationCoding

| Field Name    | Type                      |
|---------------|---------------------------|
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
