---
title: "Condition"
slug: "data-condition"
excerpt: "Canvas SDK Condition"
hidden: false
---

## Introduction

The `Condition` model represents a clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.

## Basic usage

To get a condition by identifier, use the `get` method on the `Condition` model manager:

```python
from canvas_sdk.v1.data.condition import Condition

condition = Condition.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the conditions for a patient can be accessed with the `conditions` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
conditions = patient.conditions.all()
```

If you have a patient ID, you can get the conditions for the patient with the `for_patient` method on the `Condition` model manager:

```python
from canvas_sdk.v1.data.condition import Condition

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
condition = Condition.objects.for_patient(patient_id)
```

## Codings

The codings for a condition can be accessed with the `codings` attribute on an `Condition` object:

```python
from canvas_sdk.v1.data.condition import Condition
from logger import log

condition = Condition.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in condition.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Filtering

Conditions can be filtered by any attribute that exists on the model.

Filtering for conditions is done with the `filter` method on the `Condition` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.condition import Condition

conditions = Condition.objects.filter(onset_date__gte="2024-10-15")
```

### By ValueSet

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.condition import Condition
from canvas_sdk.value_set.v022.condition import Diabetes

conditions = Condition.objects.find(Diabetes)
```

## Attributes

### Condition
| Field Name       | Type                                  |
|------------------|---------------------------------------|
| id               | UUID                                  |
| dbid             | Integer                               |
| deleted          | Boolean                               |
| entered_in_error | CanvasUser                            |
| committer        | CanvasUser                            |
| patient          | [Patient](/sdk/data-patient/#patient) |
| onset_date       | Date                                  |
| resolution_date  | Date                                  |
| clinical_status  | [ClinicalStatus](#clinicalstatus)     |

### ConditionCoding
| Field Name    | Type                                        |
|---------------|---------------------------------------------|
| dbid          | Integer                                     |
| system        | String                                      |
| version       | String                                      |
| code          | String                                      |
| display       | String                                      |
| user_selected | Boolean                                     |
| condition     | [Condition](/sdk/data-condition/#condition) |

## Enumeration types

### ClinicalStatus
| Value         | Label         |
|---------------|---------------|
| active        | active        |
| relapse       | relapse       |
| remission     | remission     |
| resolved      | resolved      |
| investigative | investigative |
