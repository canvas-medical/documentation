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

<!-- source: discussion #720 -->
## Accessing questionnaire scores

The `QuestionnaireResult` model, and the `score` on it, is not exposed in the SDK data module. When Canvas scores a questionnaire, it records the score on an `Observation` created alongside the result, so you read scores through the patient's observations. Each scored questionnaire produces one observation:

| Attribute | Value |
| --- | --- |
| `name` | The questionnaire's name, such as `PHQ-9` |
| `value` | The score, as a string |
| `category` | `survey` |
| `note_id` | The `dbid` of the note the questionnaire was completed in |
| [`codings`](#codings) | The questionnaire's scoring code, such as LOINC `44261-6` for the PHQ-9 total score. A questionnaire that could not be scored, such as one left incomplete, has no coding. |

To find a patient's scores for one questionnaire, filter on its coding. `effective_datetime` is not set on these observations, so order by `created`:

```python
from canvas_sdk.v1.data.observation import Observation

phq9_scores = (
    Observation.objects.for_patient("b80b1cdc2e6a4aca90ccebc02e683f35")
    .committed()
    .filter(category="survey", codings__system="http://loinc.org", codings__code="44261-6")
    .order_by("-created")
)

for observation in phq9_scores:
    print(observation.name, observation.value, observation.created)
```

To get the scores recorded in a specific note, filter on `note_id` with the note's `dbid` instead of the coding.

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

See [Value Sets](/sdk/data-value-sets/) for the library of built-in value sets and how to create your own.

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.observation import Observation
from canvas_sdk.value_set.v2022.physical_exam import Weight

observations = Observation.objects.find(Weight)
```

## Attributes

### Observation

| Field Name         | Type                                                |
|--------------------|-----------------------------------------------------|
| id                 | UUID                                                |
| dbid               | Integer                                             |
| created            | DateTime                                            |
| modified           | DateTime                                            |
| originator         | [CanvasUser](/sdk/data-canvasuser)                  |
| committer          | [CanvasUser](/sdk/data-canvasuser)                  |
| entered_in_error   | [CanvasUser](/sdk/data-canvasuser)                  |
| patient            | [Patient](/sdk/data-patient/#patient)               |
| is_member_of       | [Observation]( #observation)                        |
| category           | String (comma-separated list of categories |
| units              | String                                              |
| value              | String                                              |
| note_id            | Integer                                             |
| name               | String                                              |
| effective_datetime | DateTime                                            |
| codings            | [ObservationCoding](#observationcoding)[]           |
| members            | [Observation](#observation)[]                       |
| components         | [ObservationComponent](#observationcomponent)[]     |
| value_codings      | [ObservationValueCoding](#observationvaluecoding)[] |

### ObservationCoding

| Field Name    | Type                       |
|---------------|----------------------------|
| dbid          | Integer                    |
| created       | DateTime                   |
| modified      | DateTime                   |
| system        | String                     |
| version       | String                     |
| code          | String                     |
| display       | String                     |
| user_selected | Boolean                    |
| observation   | [Observation](#observation) |

### ObservationComponent

| Field Name          | Type                                                        |
|---------------------|-------------------------------------------------------------|
| dbid                | Integer                                                     |
| created             | DateTime                                                    |
| modified            | DateTime                                                    |
| observation         | [Observation](#observation)                                 |
| value_quantity      | String                                                      |
| value_quantity_unit | String                                                      |
| name                | String                                                      |
| codings             | [ObservationComponentCoding](#observationcomponentcoding)[] |

### ObservationComponentCoding

| Field Name            | Type                                |
|-----------------------|-------------------------------------|
| dbid                  | Integer                             |
| created               | DateTime                            |
| modified              | DateTime                            |
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
| created       | DateTime                   |
| modified      | DateTime                   |
| system        | String                     |
| version       | String                     |
| code          | String                     |
| display       | String                     |
| user_selected | Boolean                    |
| observation   | [Observation](#observation) |

<br/>
<br/>
<br/>
