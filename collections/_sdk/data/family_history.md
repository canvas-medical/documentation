---
title: "FamilyHistory"
slug: "data-family-history"
excerpt: "Canvas SDK FamilyHistory"
hidden: false
---

## Introduction

The `FamilyHistory` model represents a patient's family medical history — the condition(s) recorded for one of the patient's relatives, captured by the `family_history` command. The relative is identified by a SNOMED code and term, and the condition(s) are stored as `FamilyHistoryCoding` records reachable through the `codings` accessor.

## Basic usage

To get a family history record by identifier, use the `get` method on the `FamilyHistory` model manager:

```python
from canvas_sdk.v1.data.family_history import FamilyHistory

family_history = FamilyHistory.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, a patient's family history can be accessed with the `family_histories` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
family_histories = patient.family_histories.all()
```

If you have a patient ID, you can get the family history for the patient with the `for_patient` method on the `FamilyHistory` model manager:

```python
from canvas_sdk.v1.data.family_history import FamilyHistory

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
family_histories = FamilyHistory.objects.for_patient(patient_id)
```

## Codings

The relative's condition codings can be accessed with the `codings` attribute on a `FamilyHistory` object:

```python
from canvas_sdk.v1.data.family_history import FamilyHistory
from logger import log

family_history = FamilyHistory.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in family_history.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Filtering

Family history records can be filtered by any attribute that exists on the model.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.family_history import FamilyHistory

family_histories = FamilyHistory.objects.filter(relation_snomed_term="Mother")
```

### By ValueSet

See [Value Sets](/sdk/data-value-sets/) for the library of built-in value sets and how to create your own. The `find` method filters by the relative's condition codings:

```python
from canvas_sdk.v1.data.family_history import FamilyHistory
from canvas_sdk.value_set.v2022.condition import Diabetes

family_histories = FamilyHistory.objects.find(Diabetes)
```

## Attributes

### FamilyHistory

| Field Name           | Type                                          |
|----------------------|-----------------------------------------------|
| id                   | UUID                                          |
| dbid                 | Integer                                       |
| created              | DateTime                                      |
| modified             | DateTime                                      |
| deleted              | Boolean                                       |
| committer            | [CanvasUser](/sdk/data-canvasuser)            |
| entered_in_error     | [CanvasUser](/sdk/data-canvasuser)            |
| patient              | [Patient](/sdk/data-patient/#patient)         |
| note                 | [Note](/sdk/data-note)                        |
| relation_snomed_code | Integer                                       |
| relation_snomed_term | String                                        |
| narrative            | String                                        |
| codings              | [FamilyHistoryCoding](#familyhistorycoding)[] |

### FamilyHistoryCoding

| Field Name     | Type                            |
|----------------|---------------------------------|
| dbid           | Integer                         |
| system         | String                          |
| version        | String                          |
| code           | String                          |
| display        | String                          |
| user_selected  | Boolean                         |
| family_history | [FamilyHistory](#familyhistory) |

<br/>
<br/>
<br/>
