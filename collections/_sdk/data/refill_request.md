---
title: "RefillRequest"
slug: "data-refill-request"
excerpt: "Canvas SDK RefillRequest"
hidden: false
---

## Introduction

The `RefillRequest` model represents an incoming request to refill a patient's medication — for example, a renewal request received electronically from a pharmacy. Each request carries the raw request payload in its `content` attribute, the associated patient and staff member, the medication codings that describe the requested drug (`RefillRequestCoding`), and the prescription(s) written in response.

`RefillRequest` is a read-only data model. An incoming request is routed to a [staff](/sdk/data-staff/#staff) member — the provider expected to respond to it, who becomes the `prescriber` of the responding prescription, not the original requester — and can be marked as `ignored` to drop it from the active refill worklist. Once acted on, the request links to the responding prescription(s) through its `response` attribute, and each [Prescription](/sdk/data-prescription/#prescription) points back to the request through its `refill_request` field. Because the request originates from the pharmacy, and a pharmacy may route it to a provider other than the original prescriber, `staff` is not the requester; it is also nullable, so it may be unset.

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

The `ignored` attribute is a boolean dismiss flag (default `False`). Marking a request ignored removes it from the active refill worklist and is used to suppress duplicates — for example, a pharmacy re-sending a request. Requests that have already been responded to are excluded from the worklist separately, through their linked `response`. Because `RefillRequest` is read-only, a plugin can filter on `ignored` but cannot set it through this model. The example above returns the active (non-dismissed) requests.

## Related data

A refill request's medication codings are available through the `codings` reverse relation, and the prescriptions written in response are available through the `response` reverse relation:

```python
from canvas_sdk.v1.data.refill_request import RefillRequest
from logger import log

refill_request = RefillRequest.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

for coding in refill_request.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")

responding_prescriptions = refill_request.response.all()
```

The `RefillRequestCoding` entries represent the coding of the requested drug (for example, FDB or RxNorm), with an unstructured fallback whose `display` carries the drug description text when no structured code is available.

## Message content

The `message_id` and `content` attributes carry the details of the inbound eRx message.

`message_id` is the eRx (NCPDP SCRIPT / Surescripts) message identifier of the inbound refill-renewal request itself.

`content` is a JSON field holding the parsed inbound NCPDP SCRIPT refill-renewal request payload. It is a free-form, unstructured representation whose exact shape can vary between messages. The information typically available includes:

- the pharmacy (name, NCPDP ID, phone, address)
- the prescriber as reported by the sender (name, NPI, SPI, and a sender-supplied identifier)
- the dispensed and prescribed medication details (drug description, NDC, quantity, days supply, directions, number of refills, substitution allowance, written date, and similar)
- reference identifiers such as the Rx reference number and the message ID of the original prescription it renews — distinct from this request's own `message_id`

`content` is always a JSON object — it defaults to an empty object (`{}`) when no data was captured — so it is safe to call `.get()` on, but individual keys may be absent. Because the shape is not guaranteed, plugins should access `content` defensively, checking that a key is present before relying on it.

## Attributes

### RefillRequest

| Field Name | Type                                                     |
|------------|----------------------------------------------------------|
| id         | UUID                                                     |
| dbid       | Integer                                                  |
| created    | DateTime                                                 |
| modified   | DateTime                                                 |
| patient    | [Patient](/sdk/data-patient/#patient)                    |
| staff      | [Staff](/sdk/data-staff/#staff)                          |
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
