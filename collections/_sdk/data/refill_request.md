---
title: "RefillRequest"
slug: "data-refill-request"
excerpt: "Canvas SDK RefillRequest"
hidden: false
---

## Introduction

The `RefillRequest` model represents an inbound electronic prescription (eRx) refill or renewal request received for a patient. It is a read-only data model.

## Basic usage

To get a refill request by identifier, use the `get` method on the `RefillRequest` model manager:

```python
from canvas_sdk.v1.data.refill_request import RefillRequest

refill_request = RefillRequest.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
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

## Codings

The codings for a refill request can be accessed with the `codings` attribute on a `RefillRequest` object:

```python
from canvas_sdk.v1.data.refill_request import RefillRequest
from logger import log

refill_request = RefillRequest.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in refill_request.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Filtering

Refill requests can be filtered by any attribute that exists on the model.

Filtering for refill requests is done with the `filter` method on the `RefillRequest` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.refill_request import RefillRequest

refill_requests = RefillRequest.objects.filter(ignored=False)
```

## Attributes

### RefillRequest

| Field Name | Type                                            |
| ---------- | ----------------------------------------------- |
| id         | UUID                                            |
| dbid       | Integer                                         |
| patient    | [Patient](/sdk/data-patient/)                   |
| staff      | [Staff](/sdk/data-staff/)                       |
| message_id | String                                          |
| ignored    | Boolean                                         |
| content    | JSON                                            |
| codings    | [RefillRequestCoding](#refillrequestcoding)[]   |
| response   | [Prescription](/sdk/data-prescription/)[]       |
| created    | DateTime                                        |
| modified   | DateTime                                        |

### RefillRequestCoding

| Field Name     | Type                                |
| -------------- | ----------------------------------- |
| dbid           | Integer                             |
| system         | String                              |
| version        | String                              |
| code           | String                              |
| display        | String                              |
| user_selected  | Boolean                             |
| refill_request | [RefillRequest](#refillrequest)     |

<br/>
<br/>
<br/>
