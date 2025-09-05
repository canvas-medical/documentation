---
title: "Stop Medication Event"
slug: "data-stop-medication-event"
excerpt: "Canvas SDK Stop Medication Event"
hidden: false
---

## Introduction

The `StopMedicationEvent` model represents a record of a Stop Medication Event, when a medication is removed from a patient's medication list.

## Basic usage

To get a stop medication event by identifier, use the `get` method on the `StopMedicationEvent` model manager:

```python
from canvas_sdk.v1.data import StopMedicationEvent

stopped_medication = StopMedicationEvent.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
```

If you have a patient object, the stop medication events for a patient can be accessed with the `stopped_medications` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
stopped_medications = patient.stopped_medications.all()
```

You can also access the referenced medication with the `medication` attribute:

```python
from canvas_sdk.v1.data import StopMedicationEvent

stopped_medication = StopMedicationEvent.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
medication = stopped_medication.medication
```

Or for a given medication, you can access all stop events:

```python
from canvas_sdk.v1.data import Medication

medication = Medication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
stopped_medication_events = medication.stopmedicationevent_set.all()
```

## Attributes

### StopMedicationEvent

| Field Name       | Type                                  |
| ---------------- | ------------------------------------- |
| id               | UUID                                  |
| dbid             | Integer                               |
| patient          | [Patient](/sdk/data-patient/#patient) |
| note             | [Note](/sdk/data-note)                |
| medication       | [Medication](/sdk/data-medication)    |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)    |
| committer        | [CanvasUser](/sdk/data-canvasuser)    |
| originator       | [CanvasUser](/sdk/data-canvasuser)    |
| created          | DateTime                              |
| modified         | DateTime                              |
| rationale        | String                                |

<br/>
<br/>
<br/>
