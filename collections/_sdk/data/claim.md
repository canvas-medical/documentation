---
title: "Claim"
slug: "data-claim"
excerpt: "Canvas SDK Claim and related models"
hidden: false
---

## Introduction

This module defines the data models used to manage healthcare claim workflows.

## Basic usage

To retrieve a claim by its identifier:

```python
from canvas_sdk.v1.data.claim import Claim

claim = Claim.objects.get(id="9d2e0f58-338b-11ec-8d3d-0242ac130003")
```

## Filtering

```python
# Active claims only
active_claims = Claim.objects.active()
```

## Attributes

### Claim

Represents a complete healthcare claim.

| Field Name                   | Type                                |
|------------------------------|-------------------------------------|
| id                           | UUID                                |
| dbid                         | Integer                             |
| note                         | [Note](/sdk/data-note/)             |
| installment\_plan            | [InstallmentPlan](#installmentplan) |
| current\_queue               | [ClaimQueue](#claimqueue)           |
| current\_coverage            | [ClaimCoverage](#claimcoverage)     |
| accept\_assign               | Boolean                             |
| auto\_accident               | Boolean                             |
| auto\_accident\_state        | String                              |
| employment\_related          | Boolean                             |
| other\_accident              | Boolean                             |
| accident\_code               | String                              |
| illness\_date                | Date                                |
| remote\_batch\_id            | String                              |
| remote\_file\_id             | String                              |
| prior\_auth                  | String                              |
| narrative                    | String                              |
| account\_number              | String                              |
| snoozed\_until               | Date                                |
| patient\_balance             | Decimal                             |
| aggregate\_coverage\_balance | Decimal                             |
| created                      | DateTime                            |
| modified                     | DateTime                            |

**Computed Properties**:

* `total_charges`: Total charges for active line items
* `total_paid`: Sum of paid amounts from postings
* `total_adjusted`: Sum of adjustments and transfers
* `balance`: Remaining balance (coverage + patient)
* `total_patient_paid`: Paid amount by the patient
* `total_payer_paid`: Paid amount by coverages

### ClaimLineItem

Represents individual billed procedures or services tied to a claim.

| Field Name          | Type                                                       |
|---------------------|------------------------------------------------------------|
| dbid                | Integer                                                    |
| billing\_line\_item | [BillingLineItem](/sdk/data-billing-line-item/)            |
| claim               | [Claim](#claim)                                            |
| status              | [ClaimLineItemStatus](#claimlineitemstatus)                |
| charge              | Decimal                                                    |
| from\_date          | String                                                     |
| thru\_date          | String                                                     |
| narrative           | String                                                     |
| ndc\_code           | String                                                     |
| ndc\_dosage         | String                                                     |
| ndc\_measure        | String                                                     |
| place\_of\_service  | [PracticeLocationPOS](/sdk/data-note/#practicelocationpos) |
| proc\_code          | String                                                     |
| display             | String                                                     |
| remote\_chg\_id     | String                                                     |
| units               | Integer                                                    |
| epsdt               | String                                                     |
| family\_planning    | [FamilyPlanningOptions](#familyplanningoptions)            |
| created             | DateTime                                                   |
| modified            | DateTime                                                   |

### ClaimCoverage

Links a claim to a specific insurance coverage.

| Field Name                            | Type                                                                     |
|---------------------------------------|--------------------------------------------------------------------------|
| dbid                                  | Integer                                                                  |
| claim                                 | [Claim](#claim)                                                          |
| coverage                              | [Coverage](/sdk/data-coverage/)                                          |
| active                                | Boolean                                                                  |
| payer\_name                           | String                                                                   |
| payer\_id                             | String                                                                   |
| payer\_typecode                       | String                                                                   |
| payer\_order                          | [ClaimPayerOrder](#claimpayerorder)                                      |
| payer\_addr1                          | String                                                                   |
| payer\_addr2                          | String                                                                   |
| payer\_city                           | String                                                                   |
| payer\_state                          | String                                                                   |
| payer\_zip                            | String                                                                   |
| payer\_plan\_type                     | [ClaimTypeCode](#claimtypecode)                                          |
| coverage\_type                        | [CoverageType](/data-coverage/#coveragetype)                             |
| subscriber\_employer                  | String                                                                   |
| subscriber\_group                     | String                                                                   |
| subscriber\_number                    | String                                                                   |
| subscriber\_plan                      | String                                                                   |
| subscriber\_dob                       | String                                                                   |
| subscriber\_first\_name               | String                                                                   |
| subscriber\_last\_name                | String                                                                   |
| subscriber\_middle\_name              | String                                                                   |
| subscriber\_phone                     | String                                                                   |
| subscriber\_sex                       | [PersonSex](/sdk/data-patient/#sexatbirth)                               |
| subscriber\_addr1                     | String                                                                   |
| subscriber\_addr2                     | String                                                                   |
| subscriber\_city                      | String                                                                   |
| subscriber\_state                     | String                                                                   |
| subscriber\_zip                       | String                                                                   |
| subscriber\_country                   | String                                                                   |
| patient\_relationship\_to\_subscriber | [CoverageRelationshipCode](/sdk/data-coverage/#coveragerelationshipcode) |
| pay\_to\_addr1                        | String                                                                   |
| pay\_to\_addr2                        | String                                                                   |
| pay\_to\_city                         | String                                                                   |
| pay\_to\_state                        | String                                                                   |
| pay\_to\_zip                          | String                                                                   |
| resubmission\_code                    | String                                                                   |
| payer\_icn                            | String                                                                   |
| created                               | DateTime                                                                 |
| modified                              | DateTime                                                                 |

### ClaimQueue

Defines the metadata for claim queues used in revenue workflows.

| Field Name            | Type                                            |
|-----------------------|-------------------------------------------------|
| dbid                  | Integer                                         |
| queue\_sort\_ordering | Integer                                         |
| name                  | String                                          |
| display\_name         | String                                          |
| description           | String                                          |
| show\_in\_revenue     | Boolean                                         |
| visible\_columns      | Array\[[ClaimQueueColumns](#claimqueuecolumns)] |
| created               | DateTime                                        |
| modified              | DateTime                                        |

### ClaimPatient

Captures patient-level data related to a specific claim.

| Field Name   | Type                                       |
|--------------|--------------------------------------------|
| dbid         | Integer                                    |
| claim        | [Claim](#claim)                            |
| photo        | String                                     |
| dob          | String                                     |
| first\_name  | String                                     |
| last\_name   | String                                     |
| middle\_name | String                                     |
| phone        | String                                     |
| sex          | [PersonSex](/sdk/data-patient/#sexatbirth) |
| ssn          | String                                     |
| addr1        | String                                     |
| addr2        | String                                     |
| city         | String                                     |
| state        | String                                     |
| zip          | String                                     |
| country      | String                                     |
| created      | DateTime                                   |
| modified     | DateTime                                   |

### InstallmentPlan

Represents a payment plan between a patient and provider.

| Field Name             | Type                                            |
|------------------------|-------------------------------------------------|
| creator                | [CanvasUser](/sdk/data-user/)                   |
| patient                | [Patient](/sdk/data-patient/)                   |
| total\_amount          | Decimal                                         |
| status                 | [InstallmentPlanStatus](#installmentplanstatus) |
| expected\_payoff\_date | Date                                            |
| created\_at            | DateTime                                        |
| updated\_at            | DateTime                                        |

## Enumeration types

### ClaimLineItemStatus

| Value   | Label   |
|---------|---------|
| active  | Active  |
| removed | Removed |

### LineItemCodes

| Value    |
|----------|
| COPAY    |
| UNLINKED |

### FamilyPlanningOptions

| Value | Label |
|-------|-------|
| Y     | Yes   |
| N     | No    |

### ClaimLineItemStatus

| Value   | Label   |
|---------|---------|
| active  | Active  |
| removed | Removed |

### LineItemCodes

| Value    |
|----------|
| COPAY    |
| UNLINKED |

### FamilyPlanningOptions

| Value | Label |
|-------|-------|
| Y     | Yes   |
| N     | No    |

### ClaimPayerOrder

| Value      | Label      |
|------------|------------|
| Primary    | Primary    |
| Secondary  | Secondary  |
| Tertiary   | Tertiary   |
| Quaternary | Quaternary |
| Quinary    | Quinary    |

### ClaimTypeCode

| Code | Description                          |
|------|--------------------------------------|
| 12   | Working Aged (Age 65 or older)       |
| 13   | End-Stage Renal Disease              |
| 14   | No-fault                             |
| 15   | Workers Compensation                 |
| 41   | Black Lung                           |
| 42   | Veterans Administration              |
| 43   | Disabled (Under Age 65)              |
| 47   | Other Liability Insurance is primary |
| ""   | No Typecode necessary                |

### ClaimQueueColumns

| Value            | Label             |
|------------------|-------------------|
| NoteType         | Note type         |
| ClaimID          | Claim ID          |
| DateOfService    | Date of service   |
| Patient          | Patient           |
| ActiveInsurance  | Active insurance  |
| InsuranceBalance | Insurance balance |
| PatientBalance   | Patient balance   |
| DaysInQueue      | Days in queue     |
| Provider         | Provider          |
| Guarantor        | Guarantor         |
| LatestRemit      | Latest remit      |
| LastInvoiced     | Last invoiced     |
| SnoozedUntil     | Snoozed until     |
| Labels           | Labels            |

### ClaimQueues

| Value | Label                  |
|-------|------------------------|
| 1     | Appointment            |
| 2     | NeedsClinicianReview   |
| 3     | NeedsCodingReview      |
| 4     | QueuedForSubmission    |
| 5     | FiledAwaitingResponse  |
| 6     | RejectedNeedsReview    |
| 7     | AdjudicatedOpenBalance |
| 8     | PatientBalance         |
| 9     | ZeroBalance            |
| 10    | Trash                  |

### InstallmentPlanStatus

| Value     | Label     |
|-----------|-----------|
| active    | Active    |
| completed | Completed |
| cancelled | Cancelled |
