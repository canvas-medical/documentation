---
title: "EligibilityResponse"
slug: "data-eligibility-response"
excerpt: "Canvas SDK EligibilityResponse"
hidden: false
---

## Introduction

The `EligibilityResponse` model represents a coverage eligibility (271) response returned by a payer for a patient's `Coverage`, along with the originating `EligibilityRequest` (270). An `EligibilityResponse` also derives a check `status` (Active, Inactive, or Failed) from the payer's response.

## Basic usage

To get an eligibility response by identifier, use the `get` method on the `EligibilityResponse` model manager:

```python?partial=true
from canvas_sdk.v1.data.eligibility_response import EligibilityResponse

response = EligibilityResponse.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

Eligibility requests and responses are linked to a `Coverage`. From a coverage object, use the `requests` and `eligibility_responses` attributes:

```python
from canvas_sdk.v1.data.coverage import Coverage

coverage = Coverage.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
requests = coverage.requests.all()
responses = coverage.eligibility_responses.all()
```

## Eligibility status

`EligibilityResponse.status` returns an `EligibilityResponseStatus` derived from the payer's response — `FAILED` when the check errored, `INACTIVE` when the payer reports an inactive benefit section, otherwise `ACTIVE`:

```python?partial=true
from canvas_sdk.v1.data.coverage import Coverage
from canvas_sdk.v1.data.eligibility_response import EligibilityResponseStatus

coverage = Coverage.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
response = coverage.eligibility_responses.order_by("created").last()
is_active = response is not None and response.status == EligibilityResponseStatus.ACTIVE
```

A coverage with no eligibility responses (an empty `coverage.eligibility_responses` queryset) has not been verified.

`NOT_APPLICABLE`, like `UNKNOWN`, is a value returned by [`Coverage.eligibility_status`](/sdk/data-coverage/#eligibility-status), never by an individual `EligibilityResponse.status`. A single response only ever resolves to `FAILED`, `INACTIVE`, or `ACTIVE`.

## Attributes

### EligibilityRequest

| Field Name         | Type                           |
| ------------------ | ------------------------------ |
| id                 | UUID                           |
| dbid               | Integer                        |
| created            | DateTime                       |
| modified           | DateTime                       |
| coverage           | [Coverage](/sdk/data-coverage) |
| trading_partner_id | String                         |
| member             | JSON                           |
| provider           | JSON                           |
| payload            | String                         |
| control_number     | String                         |

### EligibilityResponse

| Field Name          | Type                                                                          |
| ------------------- | ---------------------------------------------------------------------------- |
| id                  | UUID                                                                         |
| dbid                | Integer                                                                      |
| created             | DateTime                                                                     |
| modified            | DateTime                                                                     |
| eligibility_request | [EligibilityRequest](#eligibilityrequest)                                    |
| coverage            | [Coverage](/sdk/data-coverage)                                               |
| client_id           | String                                                                       |
| correlation_id      | String                                                                       |
| deductible          | JSON                                                                         |
| out_of_pocket       | JSON                                                                         |
| coverage_info       | JSON                                                                         |
| payer               | JSON                                                                         |
| provider            | JSON                                                                         |
| service_type_codes  | List[String]                                                                 |
| service_types       | List[String]                                                                 |
| subscriber          | JSON                                                                         |
| trading_partner_id  | String                                                                       |
| valid_request       | Boolean                                                                      |
| errors              | List[String]                                                                 |
| eligid              | String                                                                       |
| x12_response        | String                                                                       |
| parsed_x12_response | JSON                                                                         |
| status              | [EligibilityResponseStatus](#eligibilityresponsestatus) (computed)           |
| eligibility_or_benefit_information | List (computed)                                               |

`status` and `eligibility_or_benefit_information` are computed from `errors` and `parsed_x12_response` rather than stored, so neither can be used in `filter()`. To select responses by outcome, filter on the columns they derive from — a failed check is one with a non-empty `errors`:

```python
from canvas_sdk.v1.data.eligibility_response import EligibilityResponse

failed = EligibilityResponse.objects.exclude(errors=None).exclude(errors=[])
```

## Enumeration types

### EligibilityResponseStatus

| Name           | Value         |
| -------------- | ------------- |
| ACTIVE         | Active        |
| INACTIVE       | Inactive      |
| FAILED         | Failed        |
| UNKNOWN        | Unknown       |
| NOT_APPLICABLE | NotApplicable |

<br/>
<br/>
<br/>
