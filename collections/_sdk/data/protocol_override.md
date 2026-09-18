---
title: "ProtocolOverride"
slug: "data-protocol-override"
excerpt: "Canvas SDK ProtocolOverride"
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

## Convenience methods

The `ProtocolOverride` model manager includes convenience methods for the filters plugins most often apply when working with protocol overrides.

`active` returns the overrides whose `status` is `active`:

```python
from canvas_sdk.v1.data.protocol_override import ProtocolOverride

active_overrides = ProtocolOverride.objects.active()
```

`adjustments` returns the adjustment overrides (`is_adjustment=True`) for a given protocol key, and `snoozes` returns the snooze overrides (`is_snooze=True`) for a given protocol key:

```python
from canvas_sdk.v1.data.protocol_override import ProtocolOverride

adjustments = ProtocolOverride.objects.adjustments("HCC001v1")
snoozes = ProtocolOverride.objects.snoozes("HCC001v1")
```

Each method returns a queryset, so you can chain them with `for_patient`, `committed`, and with one another. For example, to get the active adjustments for a given patient and protocol key:

```python
from canvas_sdk.v1.data.protocol_override import ProtocolOverride

adjustments = (
    ProtocolOverride.objects
    .for_patient("1eed3ea2a8d546a1b681a2a45de1d790")
    .committed()
    .active()
    .adjustments("HCC001v1")
)
```

## Attributes

### ProtocolOverride

| Field Name       | Type                                  |
| ---------------- | ------------------------------------- |
| id               | UUID                                  |
| dbid             | Integer                               |
| created          | DateTime                              |
| modified         | DateTime                              |
| committer        | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)    |
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
| ------ | ------ |
| days   | days   |
| months | months |
| years  | years  |

### Status

| Value    | Label    |
| -------- | -------- |
| active   | active   |
| inactive | inactive |

<br/>
<br/>
<br/>
