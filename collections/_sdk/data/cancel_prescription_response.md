---
title: "CancelPrescriptionResponse"
slug: "data-cancel-prescription-response"
excerpt: "Canvas SDK CancelPrescriptionResponse"
hidden: false
---

## Introduction

The `CancelPrescriptionResponse` model captures the response to a [CancelPrescription](/sdk/data-cancel-prescription) request. Each response is linked one-to-one to the request that produced it.

## Basic usage

To get a cancel prescription response by identifier, use the `get` method on the `CancelPrescriptionResponse` model manager:

```python?partial=true
from canvas_sdk.v1.data import CancelPrescriptionResponse

response = CancelPrescriptionResponse.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the cancel prescription responses for a patient can be accessed with the `cancel_prescription_responses` attribute:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
responses = patient.cancel_prescription_responses.all()
```

Or, from a cancel prescription, reach its response with the `response` attribute:

```python?partial=true
from canvas_sdk.v1.data import CancelPrescription

cancel = CancelPrescription.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
response = cancel.response
```

## Attributes

### CancelPrescriptionResponse

| Field Name  | Type                                              |
| ----------- | ------------------------------------------------- |
| id          | UUID                                              |
| dbid        | Integer                                           |
| created     | DateTime                                          |
| modified    | DateTime                                          |
| patient     | [Patient](/sdk/data-patient/#patient)             |
| request     | [CancelPrescription](/sdk/data-cancel-prescription) |
| message_id  | String                                            |
| note        | String                                            |
| reason_code | String                                            |
| response    | String                                            |

<br/>
<br/>
<br/>
