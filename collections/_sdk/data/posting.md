---
title: "Posting"
slug: "data-posting"
excerpt: "Canvas SDK Posting and related models"
hidden: false
---

## Introduction

This module defines models related to payments and postings associated with healthcare claims.

## Basic usage

To retrieve a posting by ID:

```python
from canvas_sdk.v1.data.posting import BasePosting

posting = BasePosting.objects.get(dbid=1234)
```

To retrieve all active postings for a given claim:

```python
from canvas_sdk.v1.data.claim import Claim

claim = Claim.objects.get(id="<uuid>")
claim_postings = claim.postings.active()
```

## Attributes

### BasePosting

Base model for aggregating multiple line item-level transactions (payments, adjustments, transfers) associated with a claim.

| Field Name                         | Type                                    | Description                              |
|------------------------------------|-----------------------------------------|------------------------------------------|
| dbid                               | Integer                                 |                                          |
| corrected\_posting                 | BasePosting                             |                                          |
| claim                              | [Claim](/sdk/data-claim/#claim)         |                                          |
| payment\_collection                | [PaymentCollection](#paymentcollection) |                                          |
| description                        | String                                  |                                          |
| entered\_in\_error                 | [CanvasUser](/sdk/data-canvasuser/)     |                                          |
| created                            | DateTime                                |                                          |
| modified                           | DateTime                                |                                          |
| correction\_postings               | QuerySet[[BasePosting](#baseposting)]   |                                          |
| paid\_amount                       | Decimal (computed)                      | Total paid                               |
| contractual\_adjusted\_amount      | Decimal (computed)                      | Adjustments marked as write-offs         |
| non\_write\_off\_adjusted\_amount  | Decimal (computed)                      | Non-write-off adjustments                |
| transferred\_amount                | Decimal (computed)                      | Total transferred                        |
| transferred\_to\_patient\_amount   | Decimal (computed)                      | Portion transferred to the patient       |
| transferred\_to\_coverage\_amount  | Decimal (computed)                      | Portion transferred to another coverage  |
| adjusted\_and\_transferred\_amount | Decimal (computed)                      | Combined adjusted and transferred amount |
| posted\_amount                     | Decimal (computed)                      | Total of payments and write-offs         |

### CoveragePosting

Represents an insurance payment or adjustment associated with a claim's coverage.

| Field Name         | Type                                            |
|--------------------|-------------------------------------------------|
| remittance         | [BaseRemittanceAdvice](#baseremittanceadvice)   |
| claim\_coverage    | [ClaimCoverage](/sdk/data-claim/#claimcoverage) |
| crossover\_carrier | String                                          |
| crossover\_id      | String                                          |
| payer\_icn         | String                                          |
| position\_in\_era  | Integer                                         |

### PatientPosting

Represents patient-side payments or adjustments, including links to copays or patient-level discounts.

| Field Name         | Type                                          | Description               |
|--------------------|-----------------------------------------------|---------------------------|
| claim\_patient     | [ClaimPatient](/sdk/data-claim/#claimpatient) |                           |
| patient\_payment   | [BulkPatientPosting](#bulkpatientposting)     |                           |
| copay              | [BulkPatientPosting](#bulkpatientposting)     |                           |
| discounted\_amount | Decimal (computed)                            | Discount applied          |
| charges\_amount    | Decimal (computed)                            | Discount plus paid amount |

### BulkPatientPosting

 Aggregates bulk patient payments on multiple claims.

| Field Name            | Type                                        | Description               |
|-----------------------|---------------------------------------------|---------------------------|
| id                    | UUID                                        |                           |
| dbid                  | Integer                                     |                           |
| payment\_collection   | [PaymentCollection](#paymentcollection)     |                           |
| total\_paid           | Decimal                                     |                           |
| created               | DateTime                                    |                           |
| modified              | DateTime                                    |                           |
| discount              | [Discount](#discount)                       |                           |
| payer                 | [Patient](/sdk/data-patient/)               |                           |
| postings              | QuerySet[[PatientPosting](#patientposting)] |                           |
| copays                | QuerySet[[PatientPosting](#patientposting)] |                           |
| total\_posted\_amount | Decimal (computed)                          | Sum of all posted amounts |
| discounted\_amount    | Decimal (computed)                          | Sum of discounted amounts |

### BaseRemittanceAdvice

Represents shared data for both electronic and manual remittance advice.

| Field Name            | Type                                          | Description               |
|-----------------------|-----------------------------------------------|---------------------------|
| id                    | UUID                                          |                           |
| dbid                  | Integer                                       |                           |
| payment\_collection   | [PaymentCollection](#paymentcollection)       |                           |
| total\_paid           | Decimal                                       |                           |
| created               | DateTime                                      |                           |
| modified              | DateTime                                      |                           |
| transactor            | [Transactor](/sdk/data-coverage/#transactor)  |                           |
| era\_id               | String                                        |                           |
| postings              | QuerySet[[CoveragePosting](#coverageposting)] |                           |
| total\_posted\_amount | Decimal (computed)                            | Sum of all posted amounts |

### PaymentCollection

Captures metadata about the method and details of a collected payment.

| Field Name       | Type                              |
|------------------|-----------------------------------|
| id               | UUID                              |
| dbid             | Integer                           |
| total\_collected | Decimal                           |
| method           | [PostingMethods](#postingmethods) |
| check\_number    | String                            |
| check\_date      | Date                              |
| deposit\_date    | Date                              |
| description      | String                            |
| created          | DateTime                          |
| modified         | DateTime                          |
| postings         | QuerySet[[BasePosting](#baseposting)] |
| receipt          | [Receipt](/sdk/data-receipt/#receipt) |

### NewLineItemPayment

Represents a payment applied to a billing line item within a claim.

| Field Name          | Type                                            |
|---------------------|-------------------------------------------------|
| dbid                | Integer                                         |
| posting             | [BasePosting](#baseposting)                     |
| billing\_line\_item | [BillingLineItem](/sdk/data-billing-line-item/) |
| amount              | Decimal                                         |
| charged             | Decimal                                         |
| entered\_in\_error  | [CanvasUser](/sdk/data-canvasuser/)             |
| created             | DateTime                                        |
| modified            | DateTime                                        |

### NewLineItemAdjustment

Represents an adjustment applied to a billing line item.

| Field Name                       | Type                                            |
|----------------------------------|-------------------------------------------------|
| dbid                             | Integer                                         |
| posting                          | [BasePosting](#baseposting)                     |
| billing\_line\_item              | [BillingLineItem](/sdk/data-billing-line-item/) |
| amount                           | Decimal                                         |
| code                             | String                                          |
| group                            | String                                          |
| deviated\_from\_posting\_ruleset | Boolean                                         |
| write\_off                       | Boolean                                         |
| entered\_in\_error               | [CanvasUser](/sdk/data-canvasuser/)             |
| created                          | DateTime                                        |
| modified                         | DateTime                                        |

### LineItemTransfer

Represents a transfer of a line item balance to another coverage or patient.

| Field Name                       | Type                                            |
|----------------------------------|-------------------------------------------------|
| dbid                             | Integer                                         |
| posting                          | [BasePosting](#baseposting)                     |
| billing\_line\_item              | [BillingLineItem](/sdk/data-billing-line-item/) |
| amount                           | Decimal                                         |
| code                             | String                                          |
| group                            | String                                          |
| deviated\_from\_posting\_ruleset | Boolean                                         |
| transfer\_to                     | [ClaimCoverage](/sdk/data-claim/#claimcoverage) |
| transfer\_to\_patient            | Boolean                                         |
| entered\_in\_error               | [CanvasUser](/sdk/data-canvasuser/)             |
| created                          | DateTime                                        |
| modified                         | DateTime                                        |

### Discount

Represents a discount applied to a claim or patient posting, linked by adjustment group and code.

| Field Name       | Type      |
|------------------|-----------|
| dbid             | Integer   |
| name             | String    |
| adjustment_group | String    |
| adjustment_code  | String    |
| discount         | Decimal   |
| created          | DateTime  |
| modified         | DateTime  |
| patient_postings | QuerySet[[BulkPatientPosting](#bulkpatientposting)] |

## Enumeration types

### PostingMethods

| Value | Label |
|-------|-------|
| cash  | Cash  |
| check | Check |
| card  | Card  |
| other | Other |
