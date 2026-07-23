---
title: "RefillRequest"
slug: "data-refill-request"
excerpt: "Canvas SDK RefillRequest"
hidden: false
---

## Introduction

The `RefillRequest` model represents an inbound electronic prescription (eRx) refill or renewal request received for a patient. It is a read-only data model.

An incoming request is routed to a staff member — the provider expected to respond to it — and can be marked as ignored to drop it from the active refill worklist. Once acted on, the request links to the responding prescription(s): the `response` attribute gives the resulting `Prescription`(s), and each `Prescription` points back to this request through its `refill_request` field.

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

The `RefillRequestCoding` entries represent the medication coding of the requested drug (for example, FDB or RxNorm), with an unstructured fallback whose `display` carries the drug description text when no structured code is available.

## Responding staff

When the request is acted on, the [staff](/sdk/data-staff/) member it was routed to becomes the `prescriber` of the responding prescription(s).

Note that `staff` is not the requester. The request originates from the pharmacy, and a pharmacy may route it to a provider other than the original prescriber. This attribute is nullable, so it may be unset.

One or more responding prescriptions are available through the `response` attribute; from a [Prescription](/sdk/data-prescription/), the `refill_request` field links back to this request.

## Message content

The `message_id` and `content` attributes carry the details of the inbound eRx message.

The `message_id` attribute is the eRx (NCPDP SCRIPT / Surescripts) message identifier of the inbound Refill Renewal Request message itself. It is a plain string — not a foreign key, and not a link to the [Message](/sdk/data-message/) model.

The `content` attribute is a JSON field holding the parsed inbound NCPDP SCRIPT Refill Renewal Request (RxRenewalRequest) payload. It is a free-form, unstructured representation of the request, and its exact shape can vary between messages. The kind of information typically available includes:

- the pharmacy (name, NCPDP ID, phone, address)
- the patient (name, gender, date of birth, phone)
- the prescriber as reported by the sender (name, NPI, SPI, and a sender-supplied identifier)
- the dispensed and prescribed medication details (drug description, NDC, quantity, days supply, directions, number of refills, substitution allowance, written date, and similar)
- reference identifiers such as the Rx reference number and the message ID of the original New Rx prescription it renews — distinct from this request's own `message_id` attribute

The `content` value is always a JSON object — it defaults to an empty object (`{}`) when no data was captured — so it is safe to call `.get()` on, but individual keys may be absent. Because this shape is not guaranteed, plugins should access `content` defensively — check that a key is present before relying on it.

## Filtering

Refill requests can be filtered by any attribute that exists on the model.

Filtering for refill requests is done with the `filter` method on the `RefillRequest` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute.

The `ignored` attribute is a boolean dismiss flag that defaults to `False`. Marking a request ignored removes it from the active refill worklist; it is used to suppress duplicate requests (for example, a pharmacy re-sending a request). Requests that have already been responded to are separately excluded from the worklist through their linked `response`. Because `RefillRequest` is read-only, `ignored` reflects state set within Canvas and is not written through this SDK model — a plugin can filter on it but not set it here. The example below filters on `ignored` to return the active (non-dismissed) requests:

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
