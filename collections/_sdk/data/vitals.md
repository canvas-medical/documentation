---
title: "Vitals"
slug: "data-vitals"
excerpt: "Canvas SDK Vitals"
hidden: false
---

## Introduction

A `VitalSignReading` is the anchor for a set of vital-sign measurements recorded on a note for a patient — the record produced by a [Vitals command](/sdk/commands/#vitals). A `VitalSign` is a single measurement, such as blood pressure or body temperature, that belongs to a reading.

Both models are read-only, like the rest of the [data module](/sdk/data/): to record or change vital signs, use an effect or the FHIR API rather than writing through these models. `VitalSignReading` and `VitalSign` represent the readings recorded on a note through the Vitals command, whereas [Observation](/sdk/data-observation/) is the broader model for measurements and assertions, including vital signs.

## Basic usage

To get a reading by identifier, use the `get` method on the `VitalSignReading` model manager:

```python
from canvas_sdk.v1.data.vitals import VitalSignReading

reading = VitalSignReading.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

Patient keys on this page are UUIDs without dashes, while the other IDs used here — the reading id and the note id — use the standard dashed UUID format.

If you have a patient object, the readings for a patient can be accessed with the `vital_sign_readings` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
readings = patient.vital_sign_readings.all()
```

If you have a `Note` object, the vital sign readings recorded on it can be accessed with the `vital_sign_readings` reverse relation:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="c3f1a2b4-6d7e-4f80-9a1b-2c3d4e5f6a7b")
readings = note.vital_sign_readings.all()
```

If you have a patient key, you can get the readings for the patient with the `for_patient` method on the `VitalSignReading` model manager:

```python
from canvas_sdk.v1.data.vitals import VitalSignReading

patient_key = "1eed3ea2a8d546a1b681a2a45de1d790"
readings = VitalSignReading.objects.for_patient(patient_key)
```

To limit the results to readings that have been committed, chain `committed`. The `committed` method returns readings that have been committed and not entered in error:

```python
from canvas_sdk.v1.data.vitals import VitalSignReading

readings = VitalSignReading.objects.for_patient("1eed3ea2a8d546a1b681a2a45de1d790").committed()
```

## Signs

The individual measurements for a reading can be accessed with the `signs` attribute on a `VitalSignReading` object:

```python
from canvas_sdk.v1.data.vitals import VitalSignReading
from logger import log

reading = VitalSignReading.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

for sign in reading.signs.all():
    log.info(f"sign:  {sign.sign}")
    log.info(f"value: {sign.value}")
    log.info(f"units: {sign.units}")
```

A `VitalSign` may be linked to a parent measurement through `parent`, and its child measurements are available through the `children` reverse relation. Given a `sign` and the `log`, you can traverse its children:

```python?partial=true
for child in sign.children.all():
    log.info(f"{child.sign}: {child.value}")
```

## Filtering

`VitalSign` objects can be filtered by any attribute that exists on the model.

### By attribute

A `VitalSign` is reached through its reading, so it has no `for_patient` method of its own. To get the individual measurements for a patient, filter on the reading's patient with the `reading__patient` lookup:

```python
from canvas_sdk.v1.data.vitals import VitalSign

signs = VitalSign.objects.filter(reading__patient__id="1eed3ea2a8d546a1b681a2a45de1d790")
```

## Attributes

### VitalSignReading

| Field Name       | Type                                  |
|------------------|---------------------------------------|
| id               | UUID                                  |
| dbid             | Integer                               |
| created          | DateTime                              |
| modified         | DateTime                              |
| originator       | [CanvasUser](/sdk/data-canvasuser)    |
| committer        | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)    |
| patient          | [Patient](/sdk/data-patient/#patient) |
| note             | [Note](/sdk/data-note/#note)          |
| date_recorded    | DateTime                              |
| signs            | [VitalSign](#vitalsign)[]             |

### VitalSign

| Field Name       | Type                                        |
|------------------|---------------------------------------------|
| id               | UUID                                        |
| dbid             | Integer                                     |
| created          | DateTime                                    |
| modified         | DateTime                                    |
| reading          | [VitalSignReading](#vitalsignreading)       |
| date_recorded    | DateTime                                    |
| loinc_num        | String                                      |
| sign             | [Sign](#sign)                               |
| sign_description | String                                      |
| value            | String                                      |
| units            | String                                      |
| source           | String                                      |
| parent           | [VitalSign](#vitalsign)                     |
| children         | [VitalSign](#vitalsign)[]                   |

## Enumeration types

### Sign

These are the string values that `VitalSign.sign` can hold. Filter on the value itself, not on a choices class:

| Value                            | Label                                            |
|----------------------------------|--------------------------------------------------|
| head_circumference_tape_measure  | Head Circumference by Tape Measure               |
| head_circumference               | Head Circumference                               |
| last_menstrual_period            | Last Menstrual Period                            |
| pain_severity                    | Pain Severity                                    |
| waist_circumference              | Waist Circumference                              |
| blood_pressure                   | Blood Pressure                                   |
| systole                          | Systole                                          |
| diastole                         | Diastole                                         |
| weight                           | Weight                                           |
| height                           | Height                                           |
| length                           | Length                                           |
| body_temperature                 | Body Temperature                                 |
| pulse                            | Pulse                                            |
| pulse_rhythm                     | Pulse Rhythm                                     |
| oxygen_saturation_arterial       | Oxygen Saturation Arterial                       |
| oxygen_saturation                | Oxygen Saturation                                |
| inhale_oxygen_concentration      | Inhaled Oxygen Concentration                     |
| inhaled_oxygen_concentration     | Inhaled Oxygen Contentration                     |
| inhaled_oxygen_flow_rate         | Inhaled Oxygen Flow Rate                         |
| respiration_rate                 | Respiration Rate                                 |
| bmi                              | Body Mass Index                                  |
| bmi_percentile                   | BMI for Age Percentile                           |
| note                             | Note                                             |
| head_circumference_percentile    | Head Occipital-frontal circumference Percentile  |
| weight_for_length_percentile     | Weight-for-Length Percentile                     |
| supplemental_oxygen              | Supplemental Oxygen                              |

<br/>
<br/>
<br/>
