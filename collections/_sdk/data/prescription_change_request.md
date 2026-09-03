---
title: "PrescriptionChangeRequest"
slug: "data-prescription-change-request"
excerpt: "Canvas SDK PrescriptionChangeRequest"
hidden: false
---

## Introduction

The `PrescriptionChangeRequest` model represents an incoming Surescripts (NCPDP SCRIPT) request to change a prescription — for example, a generic substitution, a prior-authorization requirement, or a script clarification. Each request carries the raw request payload in its `content` attribute, the medication codings that describe the drug in question (`PrescriptionChangeRequestCoding`), and a reference to the original prescription it relates to.

`PrescriptionChangeRequest` is a read-only data model. Because a request originates from the pharmacy, its `patient`, `note`, and `staff` associations are nullable and may be unset. The provider's approve/deny decision is recorded as a [PrescriptionChangeResponse](/sdk/data-prescription-change-response/), which links back to the request and is available through the request's `response` reverse relation.

## Basic usage

To get a prescription change request by identifier, use the `get` method on the `PrescriptionChangeRequest` model manager:

```python?partial=true
from canvas_sdk.v1.data import PrescriptionChangeRequest

change_request = PrescriptionChangeRequest.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

## Related data

A change request's medication codings are available through the `codings` reverse relation, and the responses recorded against it are available through the `response` reverse relation:

```python?partial=true
from canvas_sdk.v1.data import PrescriptionChangeRequest
from logger import log

change_request = PrescriptionChangeRequest.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

for coding in change_request.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")

responses = change_request.response.all()
```

The `PrescriptionChangeRequestCoding` entries represent the coding of the medication in question (for example, FDB or RxNorm), with an unstructured fallback whose `display` carries the drug description text when no structured code is available.

## Message content

The `message_id` and `content` attributes carry the details of the inbound eRx message.

`message_id` is the eRx (NCPDP SCRIPT / Surescripts) message identifier of the inbound change request.

`content` is a JSON field holding the parsed inbound NCPDP SCRIPT change-request payload. It is a free-form, unstructured representation whose exact shape can vary between messages, typically including the pharmacy, the prescriber as reported by the sender, and the dispensed medication details (drug description, NDC, quantity, and similar). `content` defaults to an empty object (`{}`), so it is safe to call `.get()` on, but individual keys may be absent — plugins should access it defensively.

## Change types

The `type_code` attribute identifies the kind of change the pharmacy is requesting:

| Code | Description                          |
|------|--------------------------------------|
| G    | Generic Substitution                 |
| P    | Prior Authorization Required         |
| S    | Therapeutic Interchange/Substitution |
| D    | Drug Use Evaluation                  |
| S    | Script Clarification                 |
| OS   | Pharmacy is out of stock             |
| U    | Prescriber Authorization             |

`S` really does carry two meanings. Canvas maps it to both Therapeutic
Interchange/Substitution and Script Clarification, so the two are indistinguishable from
`type_code` alone.

The `sub_type_code` attribute further qualifies the request. It is nullable and currently supports:

| Code | Description                      |
|------|----------------------------------|
| A    | Confirm Prescriber State License |

## Attributes

### PrescriptionChangeRequest

| Field Name            | Type                                                                   |
|-----------------------|------------------------------------------------------------------------|
| id                    | UUID                                                                   |
| dbid                  | Integer                                                                |
| created               | DateTime                                                               |
| modified              | DateTime                                                               |
| patient               | [Patient](/sdk/data-patient/#patient)                                  |
| note                  | [Note](/sdk/data-note)                                                 |
| staff                 | [Staff](/sdk/data-staff/#staff)                                        |
| message_id            | String                                                                 |
| original_prescription | [Prescription](/sdk/data-prescription/#prescription)                   |
| type_code             | [PrescriptionChangeRequestType](#prescriptionchangerequesttype)        |
| sub_type_code         | [PrescriptionChangeRequestSubType](#prescriptionchangerequestsubtype)  |
| content               | JSON                                                                   |
| codings               | [PrescriptionChangeRequestCoding](#prescriptionchangerequestcoding)[]  |
| response              | [PrescriptionChangeResponse](/sdk/data-prescription-change-response/)[] |

### PrescriptionChangeRequestCoding

| Field Name     | Type                                                    |
|----------------|---------------------------------------------------------|
| dbid           | Integer                                                 |
| change_request | [PrescriptionChangeRequest](#prescriptionchangerequest) |
| system         | String                                                  |
| version        | String                                                  |
| code           | String                                                  |
| display        | String                                                  |
| user_selected  | Boolean                                                 |

<br/>
<br/>
<br/>

## Enumeration types

### PrescriptionChangeRequestType

| Name          | Value | Label                                |
|---------------|-------|--------------------------------------|
| GENERIC       | G     | Generic Substitution                 |
| PRIOR         | P     | Prior Authorization Required         |
| SUBSTITUTION  | S     | Therapeutic Interchange/Substitution |
| DRUG          | D     | Drug Use Evaluation                  |
| OUTOFSTOCK    | OS    | Pharmacy is out of stock             |
| AUTHORIZATION | U     | Prescriber Authorization             |

### PrescriptionChangeRequestSubType

| Name    | Value | Label                            |
|---------|-------|----------------------------------|
| LICENSE | A     | Confirm Prescriber State License |
