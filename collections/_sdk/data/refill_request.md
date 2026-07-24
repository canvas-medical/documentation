---
title: "RefillRequest"
slug: "data-refill-request"
excerpt: "Canvas SDK RefillRequest"
hidden: false
---

## Introduction

The `RefillRequest` model represents an incoming request to refill a patient's medication — for example, a renewal request received electronically from a pharmacy. Each request carries the raw request payload in its `content` attribute, the associated patient and staff member, the medication codings that describe the requested drug (`RefillRequestCoding`), and the prescription(s) written in response.

## Basic usage

To get a refill request by identifier, use the `get` method on the `RefillRequest` model manager:

```python
from canvas_sdk.v1.data.refill_request import RefillRequest

refill_request = RefillRequest.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

If you have a patient object, the refill requests for a patient can be accessed with the `refill_requests` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
refill_requests = patient.refill_requests.all()
```

If you have a patient ID, you can get the refill requests for the patient with the `for_patient` method on the `RefillRequest` model manager:

```python
from canvas_sdk.v1.data.refill_request import RefillRequest

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
refill_requests = RefillRequest.objects.for_patient(patient_id)
```

## Filtering

Refill requests can be filtered by any attribute that exists on the model.

Filtering is done with the `filter` method on the `RefillRequest` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.refill_request import RefillRequest

outstanding_requests = RefillRequest.objects.filter(ignored=False)
```

## Related data

A refill request's medication codings are available through the `codings` reverse relation, and the prescriptions written in response are available through the `response` reverse relation:

```python
from canvas_sdk.v1.data.refill_request import RefillRequest

refill_request = RefillRequest.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
codings = refill_request.codings.all()
responding_prescriptions = refill_request.response.all()
```

## Attributes

### RefillRequest

| Field Name | Type                                                     |
|------------|----------------------------------------------------------|
| id         | UUID                                                     |
| dbid       | Integer                                                  |
| created    | DateTime                                                 |
| modified   | DateTime                                                 |
| patient    | [Patient](/sdk/data-patient/)                            |
| staff      | [Staff](/sdk/data-staff/)                                |
| message_id | String                                                   |
| ignored    | Boolean                                                  |
| content    | JSON                                                     |
| codings    | [RefillRequestCoding](#refillrequestcoding)[]            |
| response   | [Prescription](/sdk/data-prescription/#prescription)[]   |

### RefillRequestCoding

| Field Name     | Type                              |
|----------------|-----------------------------------|
| dbid           | Integer                           |
| refill_request | [RefillRequest](#refillrequest)   |
| system         | String                            |
| version        | String                            |
| code           | String                            |
| display        | String                            |
| user_selected  | Boolean                           |

<br/>
<br/>
<br/>
