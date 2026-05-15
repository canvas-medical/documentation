---
title: "Immunization"
slug: "data-immunization"
excerpt: "Canvas SDK Immunization"
hidden: false
---

## Introduction

The `Immunization` model represents a record of immunization events and immunization statements for a patient. Immunizations can be actively administered medications or historical records of immunizations received elsewhere. The `ImmunizationStatement` model represents historical immunization records and vaccination history.

## Basic usage

To get an immunization by identifier, use the `get` method on the `Immunization` model manager:

```python
from canvas_sdk.v1.data.immunization import Immunization

immunization = Immunization.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the immunizations for a patient can be accessed with the `immunizations` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
immunizations = patient.immunizations.all()
```

If you have a patient ID, you can get the immunizations for the patient with the `for_patient` method on the `Immunization` model manager:

```python
from canvas_sdk.v1.data.immunization import Immunization

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
immunizations = Immunization.objects.for_patient(patient_id)
```

## Codings

The codings for an immunization can be accessed with the `codings` attribute on an `Immunization` object:

```python
from canvas_sdk.v1.data.immunization import Immunization
from logger import log

immunization = Immunization.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in immunization.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Filtering

Immunizations can be filtered by any attribute that exists on the model.

Filtering for immunizations is done with the `filter` method on the `Immunization` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.immunization import Immunization

immunizations = Immunization.objects.filter(status="completed")
```

### By ValueSet

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.immunization import Immunization
from canvas_sdk.value_set.v2022.immunization import InfluenzaVaccine

immunizations = Immunization.objects.find(InfluenzaVaccine)
```

## Immunization Statements

To work with immunization statements (historical records), use the `ImmunizationStatement` model:

```python
from canvas_sdk.v1.data.immunization import ImmunizationStatement

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
immunization_statements = ImmunizationStatement.objects.for_patient(patient_id)
```

## Attributes

### Immunization

| Field Name                    | Type                                            |
|-------------------------------|-------------------------------------------------|
| id                            | UUID                                            |
| dbid                          | Integer                                         |
| patient                       | [Patient](/sdk/data-patient/#patient)          |
| note                          | [Note](/sdk/data-note/#note)                   |
| status                        | [ImmunizationStatus](#immunizationstatus)      |
| lot_number                    | String                                          |
| manufacturer                  | String                                          |
| exp_date_original             | String                                          |
| exp_date                      | Date                                            |
| sig_original                  | String                                          |
| date_ordered                  | Date                                            |
| given_by                      | [Staff](/sdk/data-staff/#staff)                |
| consent_given                 | Boolean                                         |
| take_quantity                 | Float                                           |
| dose_form                     | String                                          |
| route                         | String                                          |
| frequency_normalized_per_day  | Float                                           |
| deleted                       | Boolean                                         |
| codings                       | [ImmunizationCoding](#immunizationcoding)[]    |

### ImmunizationCoding

| Field Name    | Type                              |
|---------------|-----------------------------------|
| dbid          | Integer                           |
| system        | String                            |
| version       | String                            |
| code          | String                            |
| display       | String                            |
| user_selected | Boolean                           |
| immunization  | [Immunization](#immunization)     |

### ImmunizationStatement

| Field Name       | Type                                                              |
|------------------|-------------------------------------------------------------------|
| id               | UUID                                                              |
| dbid             | Integer                                                           |
| patient          | [Patient](/sdk/data-patient/#patient)                            |
| note             | [Note](/sdk/data-note/#note)                                     |
| date_original    | String                                                            |
| date             | Date                                                              |
| evidence         | String                                                            |
| comment          | String                                                            |
| reason_not_given | [ImmunizationReasonsNotGiven](#immunizationreasonsnotgiven)      |
| deleted          | Boolean                                                           |
| coding           | [ImmunizationStatementCoding](#immunizationstatementcoding)[]    |

### ImmunizationStatementCoding

| Field Name             | Type                                              |
|------------------------|---------------------------------------------------|
| dbid                   | Integer                                           |
| system                 | String                                            |
| version                | String                                            |
| code                   | String                                            |
| display                | String                                            |
| user_selected          | Boolean                                           |
| immunization_statement | [ImmunizationStatement](#immunizationstatement)  |

## Enumeration types

### ImmunizationStatus

| Value       | Label       |
|-------------|-------------|
| in-progress | In Progress |
| on-hold     | on-hold     |
| completed   | completed   |
| stopped     | stopped     |

### ImmunizationReasonsNotGiven

| Value     | Label               |
|-----------|---------------------|
| NA        | not applicable      |
| IMMUNE    | immunity            |
| MEDPREC   | medical precaution  |
| OSTOCK    | product out of stock|
| PATOBJ    | patient objection   |

<br/>
<br/>
<br/>
