---
title: "PrescriptionChangeResponse"
slug: "data-prescription-change-response"
excerpt: "Canvas SDK PrescriptionChangeResponse"
hidden: false
---

## Introduction

The `PrescriptionChangeResponse` model is the anchor for the ApproveChange and DenyChange commands — a response to a Surescripts prescription change request, recorded on a Note.

## Basic usage

To get a prescription change response by identifier, use the `get` method on the `PrescriptionChangeResponse` model manager:

```python?partial=true
from canvas_sdk.v1.data import PrescriptionChangeResponse

response = PrescriptionChangeResponse.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the prescription change responses for a patient can be accessed with the `prescription_change_responses` attribute:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
responses = patient.prescription_change_responses.all()
```

The same attribute is available on a medication:

```python
from canvas_sdk.v1.data import Medication

medication = Medication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
responses = medication.prescription_change_responses.all()
```

## Committed records

The `committed` method returns responses that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import PrescriptionChangeResponse

committed_responses = PrescriptionChangeResponse.objects.committed()
```

## Attributes

### PrescriptionChangeResponse

| Field Name                 | Type                                                              |
| -------------------------- | --------------------------------------------------------------- |
| id                         | UUID                                                            |
| dbid                       | Integer                                                         |
| created                    | DateTime                                                        |
| modified                   | DateTime                                                        |
| originator                 | [CanvasUser](/sdk/data-canvasuser)                             |
| committer                  | [CanvasUser](/sdk/data-canvasuser)                             |
| entered_in_error           | [CanvasUser](/sdk/data-canvasuser)                             |
| patient                    | [Patient](/sdk/data-patient/#patient)                         |
| note                       | [Note](/sdk/data-note)                                        |
| medication                 | [Medication](/sdk/data-medication)                            |
| response_type              | [PrescriptionChangeResponseType](#prescriptionchangeresponsetype) |
| status                     | [PrescriptionChangeResponseStatus](#prescriptionchangeresponsestatus) |
| denied_medication          | String                                                         |
| refills                    | Integer                                                        |
| note_to_pharmacist         | String                                                         |
| approved_drug_index        | Integer                                                        |
| reason_code                | String                                                         |
| message_id                 | String                                                         |
| prior_authorization_number | String                                                         |
| request                    | [PrescriptionChangeRequest](/sdk/data-prescription-change-request/) |

## Enumeration types

### PrescriptionChangeResponseType

| Name     | Value |
| -------- | ----- |
| APPROVED | A     |
| DENIED   | D     |

### PrescriptionChangeResponseStatus

| Name                | Value               |
| ------------------- | ------------------- |
| OPEN                | open                |
| PENDING             | pending             |
| ULTIMATELY_ACCEPTED | ultimately-accepted |
| ERROR               | error               |

<br/>
<br/>
<br/>
