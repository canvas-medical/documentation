---
title: "Observation"
slug: "data-observation"
excerpt: "Canvas SDK Observation"
hidden: false
---

## Introduction

The `Observation` model represents measurements or assertions made about a patient, such as vital signs, lab results, or other clinical findings.

## Basic usage

To get an observation by identifier, use the `get` method on the `Observation` model manager:

```python
from canvas_sdk.v1.data.observation import Observation

observation = Observation.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the observations for a patient can be accessed with the `observations` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
observations = patient.observations.all()
```

If you have a patient ID, you can get the observations for the patient with the `for_patient` method on the `Observation` model manager:

```python
from canvas_sdk.v1.data.observation import Observation

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
observations = Observation.objects.for_patient(patient_id)
```

## Codings

The codings for an observation can be accessed with the `codings` attribute on an `Observation` object:

```python
from canvas_sdk.v1.data.observation import Observation
from logger import log

observation = Observation.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in observation.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Components

The components for an observation can be accessed with the `components` attribute on an `Observation` object:

```python
from canvas_sdk.v1.data.observation import Observation
from logger import log

observation = Observation.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for component in observation.components.all():
    log.info(f"name: {component.name}")
    log.info(f"value: {component.value_quantity}")
    log.info(f"unit: {component.value_quantity_unit}")
```

### Component codings

Component codings can be accessed similarly to codings on the observation, by using the `codings` attribute on an `ObservationComponent` object.

## Filtering

Observations can be filtered by any attribute that exists on the model.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.observation import Observation

observations = Observation.objects.filter(effective_datetime__gte="2024-11-20")
```

### By ValueSet

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.observation import Observation
from canvas_sdk.value_set.v2022.physical_exam import Weight

observations = Observation.objects.find(Weight)
```

## Attributes

### Observation

| Field Name         | Type                                  |
|--------------------|---------------------------------------|
| id                 | UUID                                  |
| dbid               | Integer                               |
| created            | DateTime                              |
| modified           | DateTime                              |
| originator         | CanvasUser                            |
| committer          | CanvasUser                            |
| entered_in_error   | CanvasUser                            |
| deleted            | Boolean                               |
| patient            | [Patient](/sdk/data-patient/#patient) |
| is_member_of       | [Observation](#observation)           |
| category           | String                                |
| units              | String                                |
| value              | String                                |
| note_id            | Integer                               |
| name               | String                                |
| effective_datetime | DateTime                              |

### ObservationCoding

| Field Name    | Type                       |
|---------------|----------------------------|
| dbid          | Integer                    |
| system        | String                     |
| version       | String                     |
| code          | String                     |
| display       | String                     |
| user_selected | Boolean                    |
| observation   | [Observation](#observation) |

### ObservationComponent

| Field Name          | Type                        |
|---------------------|-----------------------------|
| dbid                | Integer                     |
| created             | DateTime                    |
| modified            | DateTime                    |
| observation         | [Observation](#observation) |
| value_quantity      | String                      |
| value_quantity_unit | String                      |
| name                | String                      |

### ObservationComponentCoding

| Field Name            | Type                                |
|-----------------------|-------------------------------------|
| dbid                  | Integer                             |
| system                | String                              |
| version               | String                              |
| code                  | String                              |
| display               | String                              |
| user_selected         | Boolean                             |
| observation_component | [ObservationComponent](#observation) |

### ObservationValueCoding

| Field Name    | Type                       |
|---------------|----------------------------|
| dbid          | Integer                    |
| system        | String                     |
| version       | String                     |
| code          | String                     |
| display       | String                     |
| user_selected | Boolean                    |
| observation   | [Observation](#observation) |

<br/>
<br/>
<br/>
