---
title: "Immunization"
slug: "data-immunization"
excerpt: "Canvas SDK Immunization"
hidden: false
---

## Introduction

The `Immunization` model represents a record of immunization events and immunization statements for a patient. Immunizations can be actively administered medications or historical records of immunizations received elsewhere. The `ImmunizationStatement` model represents historical immunization records and vaccination history. The [`ConsolidatedImmunization`](#consolidated-immunizations) model combines both into one record per vaccine.

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

See [Value Sets](/sdk/data-value-sets/) for the library of built-in value sets and how to create your own.

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.immunization import Immunization
from canvas_sdk.value_set.v2022.immunization import InfluenzaVaccine

immunizations = Immunization.objects.find(InfluenzaVaccine)
```

`find` also works on the `ImmunizationStatement` model manager, matching against the statement's own coding records, which it exposes through the singular `coding` accessor (unlike `Immunization.codings`):

```python
from canvas_sdk.v1.data.immunization import ImmunizationStatement
from canvas_sdk.value_set.v2022.immunization import InfluenzaVaccine

immunization_statements = ImmunizationStatement.objects.find(InfluenzaVaccine)
```

### Committed and active records

The `committed` method returns immunizations that have been committed and not entered in error. The `active` method is an alias for `committed` and returns the same records:

```python
from canvas_sdk.v1.data.immunization import Immunization

committed_immunizations = Immunization.objects.committed()
active_immunizations = Immunization.objects.active()
```

The same methods are available on the `ImmunizationStatement` model manager:

```python
from canvas_sdk.v1.data.immunization import ImmunizationStatement

committed_statements = ImmunizationStatement.objects.committed()
active_statements = ImmunizationStatement.objects.active()
```

## Immunization Statements

To work with immunization statements (historical records), use the `ImmunizationStatement` model:

```python
from canvas_sdk.v1.data.immunization import ImmunizationStatement

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
immunization_statements = ImmunizationStatement.objects.for_patient(patient_id)
```

## Consolidated immunizations

The `ConsolidatedImmunization` model holds a patient's immunizations and immunization statements as one list, in the form the [FHIR Immunization API](/api/immunization/) returns them. Read it when a plugin needs every vaccine on record for a patient, whether it was administered in Canvas or recorded from history.

Each record links back to the `Immunization` or `ImmunizationStatement` it was built from. The `source` property returns that record, or `None` when the source can't be resolved:

```python
from canvas_sdk.v1.data.patient import Patient
from logger import log

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")

for record in patient.consolidated_immunizations.committed():
    codes = ", ".join(coding.code for coding in record.coding.all())
    kind = type(record.source).__name__ if record.source else "unknown"
    log.info(f"{record.date or record.date_ordered}: {codes} ({kind})")
```

The `ConsolidatedImmunization` model manager provides the same `for_patient`, `find`, `committed`, and `active` methods as `ImmunizationStatement`. Like `ImmunizationStatement`, it exposes its codings through the singular `coding` accessor:

```python
from canvas_sdk.v1.data.immunization import ConsolidatedImmunization
from canvas_sdk.value_set.v2022.immunization import InfluenzaVaccine

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
flu_vaccines = ConsolidatedImmunization.objects.for_patient(patient_id).find(InfluenzaVaccine)
```

## Attributes

### Immunization

| Field Name                    | Type                                            |
|-------------------------------|-------------------------------------------------|
| id                            | UUID                                            |
| dbid                          | Integer                                         |
| patient                       | [Patient](/sdk/data-patient/#patient)          |
| note                          | [Note](/sdk/data-note/#note)                   |
| assessment                    | [Assessment](/sdk/data-assessment/#assessment) |
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
| committer                     | [CanvasUser](/sdk/data-canvasuser)             |
| entered_in_error              | [CanvasUser](/sdk/data-canvasuser)             |
| originator                    | [CanvasUser](/sdk/data-canvasuser)             |
| created                       | DateTime                                        |
| modified                      | DateTime                                        |
| codings                       | [ImmunizationCoding](#immunizationcoding)[]    |

### ImmunizationCoding

| Field Name    | Type                              |
|---------------|-----------------------------------|
| dbid          | Integer                           |
| created       | DateTime                          |
| modified      | DateTime                          |
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
| committer        | [CanvasUser](/sdk/data-canvasuser)                              |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)                              |
| originator       | [CanvasUser](/sdk/data-canvasuser)                              |
| created          | DateTime                                                          |
| modified         | DateTime                                                          |
| coding           | [ImmunizationStatementCoding](#immunizationstatementcoding)[]    |

### ImmunizationStatementCoding

| Field Name             | Type                                              |
|------------------------|---------------------------------------------------|
| dbid                   | Integer                                           |
| created                | DateTime                                          |
| modified               | DateTime                                          |
| system                 | String                                            |
| version                | String                                            |
| code                   | String                                            |
| display                | String                                            |
| user_selected          | Boolean                                           |
| immunization_statement | [ImmunizationStatement](#immunizationstatement)  |

### ConsolidatedImmunization

| Field Name                   | Type                                                         | Description |
|------------------------------|--------------------------------------------------------------|-------------|
| id                           | UUID                                                         |             |
| dbid                         | Integer                                                      |             |
| created                      | DateTime                                                     |             |
| modified                     | DateTime                                                     |             |
| originator                   | [CanvasUser](/sdk/data-canvasuser)                           |             |
| committer                    | [CanvasUser](/sdk/data-canvasuser)                           |             |
| entered_in_error             | [CanvasUser](/sdk/data-canvasuser)                           |             |
| patient                      | [Patient](/sdk/data-patient/#patient)                        |             |
| note                         | [Note](/sdk/data-note/#note)                                 |             |
| content_type                 | [ContentType](/sdk/data-content-type/)                       | The content type of the source record: `immunization` or `immunizationstatement` |
| object_id                    | Integer                                                      | The `dbid` of the source record |
| primary_source               | Boolean                                                      |             |
| status                       | [ImmunizationStatus](#immunizationstatus)                    |             |
| lot_number                   | String                                                       |             |
| manufacturer                 | String                                                       |             |
| exp_date_original            | String                                                       |             |
| exp_date                     | Date                                                         |             |
| sig_original                 | String                                                       |             |
| date_ordered                 | Date                                                         |             |
| given_by                     | [Staff](/sdk/data-staff/#staff)                              |             |
| consent_given                | Boolean                                                      |             |
| take_quantity                | Float                                                        |             |
| dose_form                    | String                                                       |             |
| route                        | String                                                       |             |
| frequency_normalized_per_day | Float                                                        |             |
| evidence                     | String                                                       |             |
| comment                      | String                                                       |             |
| reason_not_given             | [ImmunizationReasonsNotGiven](#immunizationreasonsnotgiven)  |             |
| date_original                | String                                                       |             |
| date                         | Date                                                         |             |
| coding                       | [ConsolidatedImmunizationCoding](#consolidatedimmunizationcoding)[] |      |
| source                       | [Immunization](#immunization) or [ImmunizationStatement](#immunizationstatement) (computed) | The record this one was built from, or `None` |

### ConsolidatedImmunizationCoding

| Field Name                | Type                                                  | Description |
|---------------------------|-------------------------------------------------------|-------------|
| dbid                      | Integer                                               |             |
| created                   | DateTime                                              |             |
| modified                  | DateTime                                              |             |
| system                    | String                                                |             |
| version                   | String                                                |             |
| code                      | String                                                |             |
| display                   | String                                                |             |
| user_selected             | Boolean                                               |             |
| content_type              | [ContentType](/sdk/data-content-type/)                | The content type of the coding it was copied from |
| object_id                 | Integer                                               | The `dbid` of the coding it was copied from |
| consolidated_immunization | [ConsolidatedImmunization](#consolidatedimmunization) |             |

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
