---
title: "FamilyHistory"
slug: "data-family-history"
excerpt: "Canvas SDK FamilyHistory"
hidden: false
---

## Introduction

The `FamilyHistory` model represents a patient's family medical history — the condition(s) recorded for one of the patient's relatives, captured by the `family_history` command. The relative is identified by a SNOMED code and term, and the condition(s) are stored as `FamilyHistoryCoding` records reachable through the `coding` accessor.

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

The relative's condition codings can be accessed with the `coding` attribute on a `FamilyHistory` object:

```python
from canvas_sdk.v1.data.family_history import FamilyHistory
from logger import log

family_history = FamilyHistory.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in family_history.coding.all():
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

### By coding

Filter across the relation to match the relative's condition codings:

```python
from canvas_sdk.v1.data.family_history import FamilyHistory

family_histories = FamilyHistory.objects.filter(
    coding__code__in=["44054006", "46635009"],
).distinct()
```

{% include alert.html type="warning" content="<code>FamilyHistory.objects.find()</code> is inherited from the shared queryset but does not work on this model: it builds its filter against a <code>codings</code> relation, while <code>FamilyHistoryCoding</code> links back as <code>coding</code>, so the call raises a <code>FieldError</code>. Filter on <code>coding</code> directly, as above, until value set lookup is supported here." %}

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
| coding               | [FamilyHistoryCoding](#familyhistorycoding)[] |

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
