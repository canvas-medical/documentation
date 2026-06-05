---
title: "Prescription"
slug: "data-prescription"
excerpt: "Canvas SDK Prescription"
hidden: false
---

## Introduction

The `Prescription` model represents a prescription for a medication that has been written for a patient. Prescriptions track the full lifecycle of a medication order, including dosage details, pharmacy information, and electronic prescribing status.

## Basic usage

To get a prescription by identifier, use the `get` method on the `Prescription` model manager:

```python
from canvas_sdk.v1.data.prescription import Prescription

prescription = Prescription.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the prescriptions for a patient can be accessed with the `prescriptions` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
prescriptions = patient.prescriptions.all()
```

If you have a patient ID, you can get the prescriptions for the patient with the `for_patient` method on the `Prescription` model manager:

```python
from canvas_sdk.v1.data.prescription import Prescription

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
prescriptions = Prescription.objects.for_patient(patient_id)
```

## Filtering

Prescriptions can be filtered by any attribute that exists on the model.

Filtering for prescriptions is done with the `filter` method on the `Prescription` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.prescription import Prescription, PrescriptionStatus

prescriptions = Prescription.objects.filter(status=PrescriptionStatus.OPEN)
```

```python
from canvas_sdk.v1.data.prescription import Prescription, PrescriptionResponse

approved_prescriptions = Prescription.objects.filter(response_type=PrescriptionResponse.APPROVED)
```

### Active prescriptions

The `active` method returns committed prescriptions that have not been denied:

```python
from canvas_sdk.v1.data.prescription import Prescription

active_prescriptions = Prescription.objects.active()
```

### Committed prescriptions

The `committed` method returns prescriptions that have been committed and not entered in error:

```python
from canvas_sdk.v1.data.prescription import Prescription

committed_prescriptions = Prescription.objects.committed()
```

## Attributes

### Prescription

| Field Name                    | Type                                                 |
| ----------------------------- | ---------------------------------------------------- |
| id                            | UUID                                                 |
| dbid                          | Integer                                              |
| patient                       | [Patient](/sdk/data-patient/)                        |
| note                          | [Note](/sdk/data-note/)                              |
| prescriber                    | [Staff](/sdk/data-staff/)                            |
| supervising_provider          | [Staff](/sdk/data-staff/)                            |
| medication                    | [Medication](/sdk/data-medication/)                  |
| compound_medication           | [CompoundMedication](/sdk/data-compound-medication/) |
| previous_medication           | [Medication](/sdk/data-medication/)                  |
| indications                   | [Assessment](/sdk/data-assessment/)[]                |
| related_refill                | [Prescription](#prescription)                        |
| status                        | [PrescriptionStatus](#prescriptionstatus)            |
| response_type                 | [PrescriptionResponse](#prescriptionresponse)        |
| is_refill                     | Boolean                                              |
| is_adjustment                 | Boolean                                              |
| is_epcs                       | Boolean                                              |
| generic_substitutions_allowed | Boolean                                              |
| written_date                  | DateTime                                             |
| dispensed_date                | DateTime                                             |
| end_date                      | Date                                                 |
| end_date_original_input       | String                                               |
| sig_original_input            | String                                               |
| dose_form                     | String                                               |
| dose_route                    | String                                               |
| dose_quantity                 | Float                                                |
| dose_frequency                | Float                                                |
| dose_frequency_interval       | String                                               |
| maximum_daily_dose            | String                                               |
| potency_quantity              | Float                                                |
| dispense_quantity             | Float                                                |
| duration_in_days              | Integer                                              |
| count_of_refills_allowed      | Integer                                              |
| note_to_pharmacist            | String                                               |
| pharmacy_name                 | String                                               |
| pharmacy_ncpdp_id             | String                                               |
| pharmacy_address              | String                                               |
| pharmacy_phone_number         | String                                               |
| pharmacy_fax_number           | String                                               |
| pharmacy_is_read_only         | Boolean                                              |
| message_id                    | String                                               |
| prescription_order_number     | String                                               |
| reason_code                   | String                                               |
| error_message                 | String                                               |
| deleted                       | Boolean                                              |
| entered_in_error              | [CanvasUser](/sdk/data-canvasuser)                   |
| committer                     | [CanvasUser](/sdk/data-canvasuser)                   |
| created                       | DateTime                                             |
| modified                      | DateTime                                             |

## Enumeration types

### PrescriptionStatus

| Enum             | Value               | Label               |
| ---------------- | ------------------- | ------------------- |
| OPEN             | open                | Open                |
| PENDING          | pending             | Pending             |
| ACCEPTED         | ultimately-accepted | Ultimately Accepted |
| ERROR            | error               | Error               |
| CANCEL_REQUESTED | cancel-requested    | Cancel Requested    |
| CANCELED         | canceled            | Canceled            |
| CANCEL_DENIED    | cancel-denied       | Cancel Denied       |
| RECEIVED         | received            | Received by DrFirst |
| SIGNED           | signed              | Signed              |
| INQUEUE          | inqueue             | In Queue            |
| TRANSMITTED      | transmitted         | Transmitted         |
| DELIVERED        | delivered           | Delivered           |

### PrescriptionResponse

| Enum                          | Value | Label                              |
| ----------------------------- | ----- | ---------------------------------- |
| APPROVED                      | A     | Approved                           |
| APPROVED_WITH_CHANGES         | C     | Approved with changes              |
| DENIED                        | D     | Denied                             |
| DENIED_PRESCRIPTION_TO_FOLLOW | N     | Denied, new prescription to follow |

<br/>
<br/>
<br/>
