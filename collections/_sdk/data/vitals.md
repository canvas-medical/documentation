---
title: "VitalSignReading"
slug: "data-vital-sign-reading"
excerpt: "Canvas SDK VitalSignReading"
hidden: false
---

## Introduction

The `VitalSignReading` model is the anchor for the [Vitals](/sdk/commands/#vitals) command — a set of vital-sign readings recorded on a Note for a Patient. The individual measurements (blood pressure, heart rate, temperature, weight, etc.) are stored as related `VitalSign` records, reachable via the `signs` attribute.

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

`signs` includes the parts of a composite measurement as well as the measurement itself, so
a blood pressure appears three times in the loop above. See
[Composite measurements](#composite-measurements) to walk only the top-level readings.

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
| sign             | String — one of the [sign values](#sign-values) |
| sign_description | String                                |
| value            | String                                |
| units            | String                                |
| source           | String                                |
| parent           | [VitalSign](#vitalsign) — the composite measurement this one is a part of, if any |
| children         | [VitalSign](#vitalsign)[] — the parts of this measurement, if it is a composite |

## Composite measurements

Some measurements are recorded as a whole *and* as their parts. The whole is stored as one
`VitalSign` and each part as another, linked to it by `parent`; the reverse accessor is
`children`. A measurement that stands on its own has `parent` set to `None` and no
`children`.

The [Vitals](/sdk/commands/#vitals) command produces two of these:

- `blood_pressure` — the combined reading, parent of the `systole` and `diastole` signs
  taken from it.
- `oxygen_saturation` — parent of `inhaled_oxygen_concentration` and
  `inhaled_oxygen_flow_rate`.

Because the parts sit alongside the whole in `reading.signs`, iterating a reading naively
counts a blood pressure three times. Filter on `parent` to walk only the top-level
measurements:

```python?partial=true
from canvas_sdk.v1.data.vitals import VitalSignReading
from logger import log

reading = VitalSignReading.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for sign in reading.signs.filter(parent__isnull=True):
    parts = ", ".join(f"{part.sign}={part.value}" for part in sign.children.all())
    log.info(f"{sign.sign}: {sign.value} {sign.units}" + (f" ({parts})" if parts else ""))
```

## Sign values

`VitalSign.sign` holds one of a fixed set of values — the ones below are those a Canvas
workflow records. Canvas declares them as a `VitalSignChoices` enumeration internally, but
that enumeration is **not** exported to plugins, so compare against the string value
directly:

```python?partial=true
from canvas_sdk.v1.data.vitals import VitalSignReading

reading = VitalSignReading.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
weights = [sign for sign in reading.signs.all() if sign.sign == "weight"]
```

`sign_description` carries a human-readable label for the same measurement, so prefer it
for display and reserve `sign` for matching.

### Where each value comes from

Not every value is produced by every workflow, so which ones you see depends on how the
vitals were recorded:

- **The [Vitals](/sdk/commands/#vitals) command** writes `height`, `weight`,
  `waist_circumference`, `body_temperature`, `blood_pressure`, `systole`, `diastole`,
  `pulse`, `pulse_rhythm`, `respiration_rate`, `oxygen_saturation`,
  `inhaled_oxygen_concentration`, `inhaled_oxygen_flow_rate`, `supplemental_oxygen` and
  `note`. Blood pressure is stored three times over — once as the combined
  `blood_pressure` reading and once each as `systole` and `diastole`.
- **A committed pediatric physical exam questionnaire** records `length` and
  `head_circumference_tape_measure`, taken from the answers carrying those LOINC codes.

Derived measurements are **not** `VitalSign` records. When a height, weight or length is
recorded, Canvas calculates BMI from the height and weight and stores the results — the
BMI-for-age, head-circumference and weight-for-height percentiles — as
[Observation](/sdk/data-observation/) records attached to the reading, because each is
computed from more than one measurement. Read them there rather than looking for a `sign`.

| Value                            | Label                                          |
| -------------------------------- | ---------------------------------------------- |
| blood_pressure                   | Blood Pressure                                 |
| systole                          | Systole                                        |
| diastole                         | Diastole                                       |
| pulse                            | Pulse                                          |
| pulse_rhythm                     | Pulse Rhythm                                   |
| respiration_rate                 | Respiration Rate                               |
| body_temperature                 | Body Temperature                               |
| oxygen_saturation                | Oxygen Saturation                              |
| supplemental_oxygen              | Supplemental Oxygen                            |
| inhaled_oxygen_concentration     | Inhaled Oxygen Concentration                   |
| inhaled_oxygen_flow_rate         | Inhaled Oxygen Flow Rate                       |
| weight                           | Weight                                         |
| height                           | Height                                         |
| length                           | Length                                         |
| head_circumference_tape_measure  | Head Circumference by Tape Measure             |
| waist_circumference              | Waist Circumference                            |
| note                             | Note                                           |

<br/>
<br/>
<br/>
