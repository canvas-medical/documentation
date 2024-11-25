---
title: "Protocol Override"
slug: "data-protocol-override"
excerpt: "Canvas SDK Protocol Override"
hidden: false
---

## Introduction

The `ProtocolOverride` model represents an instance of a protocol being snoozed for a patient.

## Basic usage

To get a protocol override by identifier, use the `get` method on the `ProtocolOverride` model manager:

```python
from canvas_sdk.v1.data.protocol_override import ProtocolOverride

protocol_override = ProtocolOverride.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the protocol overrides for a patient can be accessed with the `protocol_overrides` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
overrides = patient.protocol_overrides.all()
```

If you have a patient ID, you can get the protocol overrides for the patient with the `for_patient` method on the `ProtocolOverride` model manager:

```python
from canvas_sdk.v1.data.protocol_override import ProtocolOverride

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
override = ProtocolOverride.objects.for_patient(patient_id)
```

## Filtering

Protocol overrides can be filtered by any attribute that exists on the model.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.protocol_override import ProtocolOverride

overrides = ProtocolOverride.objects.filter(status="active")
```

## Attributes

### ProtocolOverride
| Field Name       | Type                                  |
|------------------|---------------------------------------|
| id               | UUID                                  |
| dbid             | Integer                               |
| created          | DateTime                              |
| modified         | DateTime                              |
| deleted          | Boolean                               |
| committer        | CanvasUser                            |
| entered_in_error | CanvasUser                            |
| patient          | [Patient](/sdk/data-patient/#patient) |
| protocol_key     | String                                |
| is_adjustment    | Boolean                               |
| reference_date   | DateTime                              |
| cycle_in_days    | Integer                               |
| is_snooze        | Boolean                               |
| snooze_date      | Date                                  |
| snoozed_days     | Integer                               |
| snooze_comment   | String                                |
| narrative        | String                                |
| cycle_quantity   | Integer                               |
| cycle_unit       | [IntervalUnit](#intervalunit)         |
| status           | [Status](#status)                     |

## Enumeration types

### IntervalUnit
| Value  | Label  |
|--------|--------|
| days   | days   |
| months | months |
| years  | years  |

### Status
| Value    | Label    |
|----------|----------|
| active   | active   |
| inactive | inactive |
