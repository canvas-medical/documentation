---
title: "ServiceRequest"
slug: "data-service-request"
excerpt: "Canvas SDK ServiceRequest"
hidden: false
---

## Introduction

The `ServiceRequest` model is the FHIR ServiceRequest that Canvas keeps over an imaging order, lab order, referral, or procedure. Use it to read a patient's orders of all four kinds through one model, with their status, requester, category and service codings, and the conditions given as reasons. The order itself is available through `requested_service`.

The same records are available over the FHIR API as [ServiceRequest](/api/servicerequest/).

## Basic usage

To get a service request by identifier, use the `get` method on the `ServiceRequest` model manager:

```python?partial=true
from canvas_sdk.v1.data.service_request import ServiceRequest

service_request = ServiceRequest.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient or staff object, their service requests can be accessed with the `service_requests` attribute. For staff, these are the service requests they requested:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.staff import Staff

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
service_requests = patient.service_requests.all()

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")
requested = staff.service_requests.all()
```

If you have a patient ID, you can get the service requests for the patient with the `for_patient` method on the `ServiceRequest` model manager:

```python?partial=true
from canvas_sdk.v1.data.service_request import ServiceRequest

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
service_requests = ServiceRequest.objects.for_patient(patient_id)
```

## The requested order

The `requested_service` property returns the order a service request wraps: an [ImagingOrder](/sdk/data-imaging/#imagingorder), [LabOrder](/sdk/data-labs/#laborder), [Referral](/sdk/data-referral/#referral), or [Procedure](/sdk/data-procedure/#procedure). It returns `None` when the service request has no linked order, when the order is of another type, or when the order has been deleted.

`requested_service_type` and `requested_service_object_id` form the link to the order. `requested_service_type` is the order's [ContentType](/sdk/data-content-type/), and `requested_service_object_id` is the order's `dbid`.

Each read of `requested_service` queries the content type and then the order. When you loop over service requests, add `select_related("requested_service_type")` to skip the content type query:

```python
from canvas_sdk.v1.data.imaging import ImagingOrder
from canvas_sdk.v1.data.lab import LabOrder
from canvas_sdk.v1.data.service_request import ServiceRequest
from logger import log

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
service_requests = ServiceRequest.objects.for_patient(patient_id).select_related(
    "requested_service_type"
)

for service_request in service_requests:
    order = service_request.requested_service
    if isinstance(order, LabOrder):
        log.info(f"Lab order {order.id}")
    elif isinstance(order, ImagingOrder):
        log.info(f"Imaging order {order.id}")
```

To read only one kind of order, filter on the content type's stable `app_label` and `model`. The values are `api` and one of `imagingorder`, `laborder`, `referral`, or `procedure`:

```python?partial=true
from canvas_sdk.v1.data.service_request import ServiceRequest

lab_service_requests = ServiceRequest.objects.filter(
    requested_service_type__app_label="api",
    requested_service_type__model="laborder",
)
```

## Codings

A service request has two sets of codings. `category_codings` holds the category of the request, such as imaging or laboratory procedure. `codings` holds the service being requested:

```python?partial=true
from canvas_sdk.v1.data.service_request import ServiceRequest
from logger import log

service_request = ServiceRequest.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in service_request.category_codings.all():
    log.info(f"category: {coding.system} {coding.code} {coding.display}")

for coding in service_request.codings.all():
    log.info(f"service:  {coding.system} {coding.code} {coding.display}")
```

## Reason conditions

The conditions given as the reason for a service request are available with the `conditions` attribute. Going the other way, `service_requests` on a [Condition](/sdk/data-condition/#condition) returns the service requests that give it as a reason:

```python?partial=true
from canvas_sdk.v1.data.condition import Condition
from canvas_sdk.v1.data.service_request import ServiceRequest

service_request = ServiceRequest.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
conditions = service_request.conditions.all()

condition = Condition.objects.get(id="c3a5e1f2-7b4d-4e8a-9f6c-2d1b0a9e8f7c")
service_requests = condition.service_requests.all()
```

Each link is a [ServiceRequestReasonCondition](#servicerequestreasoncondition) row, available with `reason_conditions` on the service request and `service_request_reasons` on the condition.

## Filtering

Service requests can be filtered by any attribute that exists on the model.

Filtering for service requests is done with the `filter` method on the `ServiceRequest` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python?partial=true
from canvas_sdk.v1.data.service_request import ServiceRequest, ServiceRequestStatus

active_service_requests = ServiceRequest.objects.filter(status=ServiceRequestStatus.ACTIVE)
```

## Attributes

### ServiceRequest

| Field Name                  | Type                                                              |
|-----------------------------|-------------------------------------------------------------------|
| id                          | UUID                                                              |
| dbid                        | Integer                                                           |
| created                     | DateTime                                                          |
| modified                    | DateTime                                                          |
| status                      | [ServiceRequestStatus](#servicerequeststatus)                     |
| patient                     | [Patient](/sdk/data-patient/#patient)                             |
| requester                   | [Staff](/sdk/data-staff/#staff) (or `None`)                       |
| authored_on                 | DateTime                                                          |
| occurrence_period_start     | DateTime                                                          |
| occurrence_period_end       | DateTime                                                          |
| requested_service_type      | [ContentType](/sdk/data-content-type/) (the order's type)         |
| requested_service_object_id | Integer (the order's `dbid`)                                      |
| requested_service           | [ImagingOrder](/sdk/data-imaging/#imagingorder), [LabOrder](/sdk/data-labs/#laborder), [Referral](/sdk/data-referral/#referral), or [Procedure](/sdk/data-procedure/#procedure) (computed; the wrapped order, or `None`) |
| category_codings            | [ServiceRequestCategoryCoding](#servicerequestcategorycoding)[]   |
| codings                     | [ServiceRequestCoding](#servicerequestcoding)[]                   |
| reason_conditions           | [ServiceRequestReasonCondition](#servicerequestreasoncondition)[] |
| conditions                  | [Condition](/sdk/data-condition/#condition)[]                     |

### ServiceRequestCategoryCoding

| Field Name      | Type                                |
|-----------------|-------------------------------------|
| dbid            | Integer                             |
| created         | DateTime                            |
| modified        | DateTime                            |
| system          | String                              |
| version         | String                              |
| code            | String                              |
| display         | String                              |
| user_selected   | Boolean                             |
| service_request | [ServiceRequest](#servicerequest) |

### ServiceRequestCoding

| Field Name      | Type                                |
|-----------------|-------------------------------------|
| dbid            | Integer                             |
| created         | DateTime                            |
| modified        | DateTime                            |
| system          | String                              |
| version         | String                              |
| code            | String                              |
| display         | String                              |
| user_selected   | Boolean                             |
| service_request | [ServiceRequest](#servicerequest) |

### ServiceRequestReasonCondition

| Field Name      | Type                                        |
|-----------------|---------------------------------------------|
| dbid            | Integer                                     |
| service_request | [ServiceRequest](#servicerequest)           |
| condition       | [Condition](/sdk/data-condition/#condition) |

## Enumeration types

### ServiceRequestStatus

| Name             | Value              | Label            |
|------------------|--------------------|------------------|
| DRAFT            | `draft`            | Draft            |
| ACTIVE           | `active`           | Active           |
| COMPLETED        | `completed`        | Completed        |
| ENTERED_IN_ERROR | `entered-in-error` | Entered in Error |

<br/>
<br/>
<br/>
