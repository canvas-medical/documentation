---
title: "CancelPrescription"
slug: "data-cancel-prescription"
excerpt: "Canvas SDK CancelPrescription"
hidden: false
---

## Introduction

The `CancelPrescription` model is the anchor for the CancelPrescription command — a request to cancel a patient's prescription, recorded on a Note.

## Basic usage

To get a cancel prescription by identifier, use the `get` method on the `CancelPrescription` model manager:

```python?partial=true
from canvas_sdk.v1.data import CancelPrescription

cancel = CancelPrescription.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the cancel prescriptions for a patient can be accessed with the `cancel_prescriptions` attribute:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
cancels = patient.cancel_prescriptions.all()
```

Or, from a prescription, reach its cancellations with the same `cancel_prescriptions` attribute:

```python
from canvas_sdk.v1.data import Prescription

prescription = Prescription.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
cancels = prescription.cancel_prescriptions.all()
```

## Committed records

The `committed` method returns cancel prescriptions that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import CancelPrescription

committed_cancels = CancelPrescription.objects.committed()
```

## Attributes

### CancelPrescription

| Field Name       | Type                                                  |
| ---------------- | ---------------------------------------------------- |
| id               | UUID                                                 |
| dbid             | Integer                                              |
| created          | DateTime                                             |
| modified         | DateTime                                             |
| originator       | [CanvasUser](/sdk/data-canvasuser)                  |
| committer        | [CanvasUser](/sdk/data-canvasuser)                  |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)                  |
| patient          | [Patient](/sdk/data-patient/#patient)               |
| note             | [Note](/sdk/data-note)                              |
| prescription     | [Prescription](/sdk/data-prescription)              |
| message_id       | String                                              |
| status           | [CancelPrescriptionStatus](#cancelprescriptionstatus) |
| response         | [CancelPrescriptionResponse](/sdk/data-cancel-prescription-response/#cancelprescriptionresponse) |

## Enumeration types

### CancelPrescriptionStatus

| Name                | Value               |
| ------------------- | ------------------- |
| OPEN                | open                |
| PENDING             | pending             |
| ULTIMATELY_ACCEPTED | ultimately-accepted |

<br/>
<br/>
<br/>
