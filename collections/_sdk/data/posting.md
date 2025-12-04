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

| Field Name          | Type                                    |
|---------------------|-----------------------------------------|
| dbid                | Integer                                 |
| corrected\_posting  | BasePosting                             |
| claim               | [Claim](/sdk/data-claim/#claim)         |
| payment\_collection | [PaymentCollection](#paymentcollection) |
| description         | String                                  |
| entered\_in\_error  | [CanvasUser](/sdk/data-canvasuser/)           |
| created             | DateTime                                |
| modified            | DateTime                                |

**Computed Properties**:

* `paid_amount`: Total paid
* `contractual_adjusted_amount`: Adjustments marked as write-offs
* `non_write_off_adjusted_amount`: Non-write-off adjustments
* `transferred_amount`: Total transferred
* `transferred_to_patient_amount`: Portion transferred to patient
* `transferred_to_coverage_amount`: Portion transferred to another coverage
* `adjusted_and_transferred_amount`: Combined adjusted and transferred amount
* `posted_amount`: Total of payments and write-offs

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

| Field Name       | Type                                          |
|------------------|-----------------------------------------------|
| claim\_patient   | [ClaimPatient](/sdk/data-claim/#claimpatient) |
| patient\_payment | [BulkPatientPosting](#bulkpatientposting)     |
| copay            | [BulkPatientPosting](#bulkpatientposting)     |

**Computed Properties**:

* `discounted_amount`: Discount applied
* `charges_amount`: Discount + paid amount

### BulkPatientPosting

 Aggregates bulk patient payments on multiple claims.

| Field Name          | Type                                    |
|---------------------|-----------------------------------------|
| id                  | UUID                                    |
| dbid                | Integer                                 |
| payment\_collection | [PaymentCollection](#paymentcollection) |
| total\_paid         | Decimal                                 |
| created             | DateTime                                |
| modified            | DateTime                                |
| discount            | [Discount](#discount)                   |
| payer               | [Patient](/sdk/data-patient/)           |

**Computed Properties**:

* `total_posted_amount`: Sum of all posted amounts
* `discounted_amount`: Sum of discounted amounts

### BaseRemittanceAdvice

Represents shared data for both electronic and manual remittance advice.

| Field Name          | Type                                          |
|---------------------|-----------------------------------------------|
| id                  | UUID                                          |
| dbid                | Integer                                       |
| payment\_collection | [PaymentCollection](#paymentcollection)       |
| total\_paid         | Decimal                                       |
| created             | DateTime                                      |
| modified            | DateTime                                      |
| transactor          | [Transactor](/sdk/data-coverage/#transactor/) |
| era\_id             | String                                        |

**Computed Properties**:

* `total_posted_amount`: Sum of all posted amounts

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

### NewLineItemPayment

Represents a payment applied to a billing line item within a claim.

| Field Name          | Type                                            |
|---------------------|-------------------------------------------------|
| dbid                | Integer                                         |
| posting             | [BasePosting](#baseposting)                     |
| billing\_line\_item | [BillingLineItem](/sdk/data-billing-line-item/) |
| amount              | Decimal                                         |
| charged             | Decimal                                         |
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


## Enumeration types

### PostingMethods

| Value | Label |
|-------|-------|
| cash  | Cash  |
| check | Check |
| card  | Card  |
| other | Other |
