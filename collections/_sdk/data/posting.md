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

Payments, adjustments, and transfers each record the claim line item the amount was posted to. To find the charge behind a payment, go through its claim line item:

```python
from canvas_sdk.v1.data import NewLineItemPayment

payment = NewLineItemPayment.objects.select_related("claim_line_item").get(dbid=1234)
claim_line_item = payment.claim_line_item
print(claim_line_item.proc_code)

# None when the claim line item has no billing line item
charge = claim_line_item.billing_line_item
```

On a remit, each coverage posting also records the amount the payer allowed on each claim line item and the remark codes the payer sent with it:

```python
from canvas_sdk.v1.data import CoveragePosting

posting = CoveragePosting.objects.get(dbid=1234)

for allowed in posting.lineitemalloweds.active():
    print(allowed.claim_line_item.proc_code, allowed.amount)

for remark in posting.remark_codes.all():
    print(remark.claim_line_item.proc_code, remark.remark_code)
```

{% include alert.html type="warning" content="<b>Deprecation Notice:</b> The <code>billing_line_item</code> attribute on <code>NewLineItemPayment</code>, <code>NewLineItemAdjustment</code>, and <code>LineItemTransfer</code> is deprecated. It can return an unrelated charge, because the stored ID belongs to a claim line item, not a billing line item. Use <code>claim_line_item.billing_line_item</code> instead. <code>billing_line_item_id</code> holds the same claim line item ID as <code>claim_line_item_id</code>." %}

## Remits

A remit is a payer's payment and explanation for one or more claims. Canvas stores each one as a [BaseRemittanceAdvice](#baseremittanceadvice), which is either an [ElectronicRemittanceAdvice](#electronicremittanceadvice) received from a clearinghouse or a [ManualRemittanceAdvice](#manualremittanceadvice) posted by hand. Query the subtype to get only one kind, along with its own fields:

```python
from canvas_sdk.v1.data import ElectronicRemittanceAdvice

for era in ElectronicRemittanceAdvice.objects.filter(payer_name="Acme Health"):
    print(era.era_id, era.received_time, era.total_paid)
```

A remit lists the claims it covers in `claims`, and a claim lists its remits in `remits`. The file a remit was posted from is a [NewRemittanceDocument](#newremittancedocument), reached through the remit's `document`:

```python
from canvas_sdk.v1.data import BaseRemittanceAdvice, NewRemittanceDocument

remit = BaseRemittanceAdvice.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
claims = remit.claims.all()

try:
    # Presigned S3 URL to the remit file, or None if there is no file
    url = remit.document.document_url
except NewRemittanceDocument.DoesNotExist:
    url = None
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
| lineitemalloweds                   | QuerySet[[LineItemAllowed](#lineitemallowed)] | Allowed amounts per claim line item |
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
| remark\_codes      | QuerySet[[RemarkCode](#remarkcode)]             |

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
| claims                | QuerySet[[Claim](/sdk/data-claim/#claim)]     | Claims the remit covers, including claims whose remit processing was skipped |
| postings              | QuerySet[[CoveragePosting](#coverageposting)] |                           |
| document              | [NewRemittanceDocument](#newremittancedocument) | File the remit was posted from |
| total\_posted\_amount | Decimal (computed)                            | Sum of all posted amounts |

### ElectronicRemittanceAdvice

An electronic remit (ERA) received from a clearinghouse. It has every [BaseRemittanceAdvice](#baseremittanceadvice) field, plus:

| Field Name     | Type     |
|----------------|----------|
| check\_type    | String   |
| payer\_name    | String   |
| provider\_name | String   |
| provider\_npi  | String   |
| download\_date | Date     |
| received\_time | DateTime |

### ManualRemittanceAdvice

A remit posted by hand. It has the [BaseRemittanceAdvice](#baseremittanceadvice) fields and no others.

### BaseRemittanceAdviceClaim

Links a remit to a claim it covers. Read the link through `remit.claims` or `claim.remits` rather than querying this model.

```python
from canvas_sdk.v1.data import Claim

claim = Claim.objects.get(id="9d2e0f58-338b-11ec-8d3d-0242ac130003")
remits = claim.remits.all()
```

| Field Name | Type                                          |
|------------|-----------------------------------------------|
| dbid       | Integer                                       |
| remittance | [BaseRemittanceAdvice](#baseremittanceadvice) |
| claim      | [Claim](/sdk/data-claim/#claim)               |

### NewRemittanceDocument

The file a manual or electronic remit was posted from.

| Field Name         | Type                                          | Description                                          |
|--------------------|-----------------------------------------------|------------------------------------------------------|
| dbid               | Integer                                       |                                                      |
| remittance         | [BaseRemittanceAdvice](#baseremittanceadvice) |                                                      |
| document           | File (S3 key)                                 |                                                      |
| document\_url      | String (computed)                             | Presigned URL for the file, or `None` when unset     |
| originator         | [CanvasUser](/sdk/data-canvasuser/)           |                                                      |
| committer          | [CanvasUser](/sdk/data-canvasuser/)           |                                                      |
| entered\_in\_error | [CanvasUser](/sdk/data-canvasuser/)           |                                                      |
| created            | DateTime                                      |                                                      |
| modified           | DateTime                                      |                                                      |

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

Represents a payment applied to a claim line item.

| Field Name          | Type                                            |
|---------------------|-------------------------------------------------|
| dbid                | Integer                                         |
| posting             | [BasePosting](#baseposting)                     |
| billing\_line\_item | [BillingLineItem](/sdk/data-billing-line-item/) (deprecated) |
| claim\_line\_item   | [ClaimLineItem](/sdk/data-claim/#claimlineitem) |
| amount              | Decimal                                         |
| charged             | Decimal                                         |
| entered\_in\_error  | [CanvasUser](/sdk/data-canvasuser/)             |
| created             | DateTime                                        |
| modified            | DateTime                                        |

### NewLineItemAdjustment

Represents an adjustment applied to a claim line item.

| Field Name                       | Type                                            |
|----------------------------------|-------------------------------------------------|
| dbid                             | Integer                                         |
| posting                          | [BasePosting](#baseposting)                     |
| billing\_line\_item              | [BillingLineItem](/sdk/data-billing-line-item/) (deprecated) |
| claim\_line\_item                | [ClaimLineItem](/sdk/data-claim/#claimlineitem) |
| amount                           | Decimal                                         |
| code                             | String                                          |
| group                            | String                                          |
| deviated\_from\_posting\_ruleset | Boolean                                         |
| write\_off                       | Boolean                                         |
| entered\_in\_error               | [CanvasUser](/sdk/data-canvasuser/)             |
| created                          | DateTime                                        |
| modified                         | DateTime                                        |

### LineItemTransfer

Represents a transfer of a claim line item balance to another coverage or patient.

| Field Name                       | Type                                            |
|----------------------------------|-------------------------------------------------|
| dbid                             | Integer                                         |
| posting                          | [BasePosting](#baseposting)                     |
| billing\_line\_item              | [BillingLineItem](/sdk/data-billing-line-item/) (deprecated) |
| claim\_line\_item                | [ClaimLineItem](/sdk/data-claim/#claimlineitem) |
| amount                           | Decimal                                         |
| code                             | String                                          |
| group                            | String                                          |
| deviated\_from\_posting\_ruleset | Boolean                                         |
| transfer\_to                     | [ClaimCoverage](/sdk/data-claim/#claimcoverage) |
| transfer\_to\_patient            | Boolean                                         |
| entered\_in\_error               | [CanvasUser](/sdk/data-canvasuser/)             |
| created                          | DateTime                                        |
| modified                         | DateTime                                        |

### LineItemAllowed

Represents the amount a payer allowed on a claim line item. Call `active()` to leave out amounts entered in error.

| Field Name          | Type                                            |
|---------------------|-------------------------------------------------|
| dbid                | Integer                                         |
| posting             | [BasePosting](#baseposting)                     |
| billing\_line\_item | [BillingLineItem](/sdk/data-billing-line-item/) (deprecated) |
| claim\_line\_item   | [ClaimLineItem](/sdk/data-claim/#claimlineitem) |
| amount              | Decimal                                         |
| entered\_in\_error  | [CanvasUser](/sdk/data-canvasuser/)             |
| created             | DateTime                                        |
| modified            | DateTime                                        |

### RemarkCode

Represents a remark code a payer sent in an 835 remit for a claim line item on a coverage posting.

`remark_code` holds the code exactly as the payer sent it. Payers send codes from the X12 [Remittance Advice Remark Codes](https://x12.org/codes/remittance-advice-remark-codes) list, such as `N381` or `M15`, which X12 updates several times a year, so look up a code's meaning there rather than hardcoding a list.

| Field Name        | Type                                            |
|-------------------|-------------------------------------------------|
| dbid              | Integer                                         |
| posting           | [CoveragePosting](#coverageposting)             |
| claim\_line\_item | [ClaimLineItem](/sdk/data-claim/#claimlineitem) |
| remark\_code      | String                                          |
| created           | DateTime                                        |
| modified          | DateTime                                        |

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
