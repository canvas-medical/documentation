---
title: "Procedure"
slug: "data-procedure"
excerpt: "Canvas SDK Procedure"
hidden: false
---

## Introduction

The `Procedure` model represents a procedure performed on or ordered for a patient. It is the data model behind the Perform command, is always associated with a Note and a Patient, and has an optional performing provider. Its CPT (or other) codings are available via `codings`.

## Basic usage

To get a procedure by identifier, use the `get` method on the `Procedure` model manager:

```python?partial=true
from canvas_sdk.v1.data.procedure import Procedure

procedure = Procedure.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient or note object, the procedures for a patient or note can be accessed with the `procedures` attribute:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.note import Note

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
procedures = patient.procedures.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
procedures = note.procedures.all()
```

If you have a patient ID, you can get the procedures for the patient with the `for_patient` method on the `Procedure` model manager:

```python?partial=true
from canvas_sdk.v1.data.procedure import Procedure

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
procedures = Procedure.objects.for_patient(patient_id)
```

## Codings

The codings for a procedure can be accessed with the `codings` attribute on a `Procedure` object:

```python?partial=true
from canvas_sdk.v1.data.procedure import Procedure
from logger import log

procedure = Procedure.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in procedure.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Filtering

Procedures can be filtered by any attribute that exists on the model.

Filtering for procedures is done with the `filter` method on the `Procedure` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python?partial=true
from canvas_sdk.v1.data.procedure import Procedure, ProcedureStatus

procedures = Procedure.objects.filter(status=ProcedureStatus.COMPLETED)
```

### Committed procedures

The `committed` method returns procedures that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data.procedure import Procedure

committed_procedures = Procedure.objects.committed()
```

### By ValueSet

See [Value Sets](/sdk/data-value-sets/) for the library of built-in value sets and how to create your own.

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python?partial=true
from canvas_sdk.v1.data.procedure import Procedure
from canvas_sdk.value_set.v2022.procedure import Colonoscopy

procedures = Procedure.objects.find(Colonoscopy)
```

## Attributes

### Procedure

| Field Name       | Type                                  |
| ---------------- | ------------------------------------- |
| id               | UUID                                  |
| dbid             | Integer                               |
| created          | DateTime                              |
| modified         | DateTime                              |
| originator       | [CanvasUser](/sdk/data-canvasuser)    |
| committer        | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)    |
| patient          | [Patient](/sdk/data-patient/#patient) |
| note             | [Note](/sdk/data-note)                |
| provider         | [Staff](/sdk/data-staff/)             |
| status           | [ProcedureStatus](#procedurestatus)   |
| notes            | String                                |
| codings          | [ProcedureCoding](#procedurecoding)[] |

### ProcedureCoding

| Field Name    | Type                    |
| ------------- | ----------------------- |
| dbid          | Integer                 |
| system        | String                  |
| version       | String                  |
| code          | String                  |
| display       | String                  |
| user_selected | Boolean                 |
| procedure     | [Procedure](#procedure) |

## Enumeration types

### ProcedureStatus

| Name        | Value | Label       |
| ----------- | ----- | ----------- |
| IN_PROGRESS | 1     | in-progress |
| ABORTED     | 2     | aborted     |
| COMPLETED   | 3     | completed   |

<br/>
<br/>
<br/>
