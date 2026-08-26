---
title: "VitalSignReading"
slug: "data-vital-sign-reading"
excerpt: "Canvas SDK VitalSignReading"
hidden: false
---

## Introduction

The `VitalSignReading` model is the anchor for the `vitals` command — a set of vital-sign readings recorded on a Note for a Patient. The individual measurements (blood pressure, heart rate, temperature, weight, etc.) are stored as related `VitalSign` records, reachable via the `signs` attribute.

## Basic usage

To get a vital sign reading by identifier, use the `get` method on the `VitalSignReading` model manager:

```python?partial=true
from canvas_sdk.v1.data.vitals import VitalSignReading

reading = VitalSignReading.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient or note object, the readings can be accessed with the `vital_sign_readings` attribute:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.note import Note

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
readings = patient.vital_sign_readings.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
readings = note.vital_sign_readings.all()
```

If you have a patient ID, you can get the readings for the patient with the `for_patient` method:

```python?partial=true
from canvas_sdk.v1.data.vitals import VitalSignReading

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
readings = VitalSignReading.objects.for_patient(patient_id)
```

## Reading the individual measurements

Each `VitalSignReading` has one or more `VitalSign` measurements, accessed with the `signs` attribute. Each `VitalSign` carries the measurement's LOINC code, name, value, and units:

```python?partial=true
from canvas_sdk.v1.data.vitals import VitalSignReading
from logger import log

reading = VitalSignReading.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for sign in reading.signs.all():
    log.info(f"{sign.sign}: {sign.value} {sign.units} (LOINC {sign.loinc_num})")
```

## Filtering

Vital sign readings can be filtered by any attribute that exists on the model.

### Committed readings

The `committed` method returns readings that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data.vitals import VitalSignReading

committed_readings = VitalSignReading.objects.committed()
```

## Attributes

### VitalSignReading

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
| date_recorded    | DateTime                              |
| signs            | [VitalSign](#vitalsign)[]             |

### VitalSign

| Field Name       | Type                                  |
| ---------------- | ------------------------------------- |
| id               | UUID                                  |
| dbid             | Integer                               |
| created          | DateTime                              |
| modified         | DateTime                              |
| reading          | [VitalSignReading](#vitalsignreading) |
| date_recorded    | DateTime                              |
| loinc_num        | String                                |
| sign             | String                                |
| sign_description | String                                |
| value            | String                                |
| units            | String                                |
| source           | String                                |
| parent           | [VitalSign](#vitalsign)               |

<br/>
<br/>
<br/>
