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

To access diagnosis codes for a claim:

```python
from canvas_sdk.v1.data.claim import Claim

claim = Claim.objects.get(id="9d2e0f58-338b-11ec-8d3d-0242ac130003")
diagnosis_codes = claim.diagnosis_codes.all().order_by("rank")

for diagnosis in diagnosis_codes:
    print(f"Rank {diagnosis.rank}: {diagnosis.code} - {diagnosis.display}")
```

## Filtering

```python
from canvas_sdk.v1.data.claim import Claim

# Active claims only
active_claims = Claim.objects.active()
```

## Attributes

### Claim

Represents a complete healthcare claim.

| Field Name                 | Type                                        |
| -------------------------- | ------------------------------------------- |
| id                         | UUID                                        |
| dbid                       | Integer                                     |
| note                       | [Note](/sdk/data-note/)                     |
| installment_plan           | [InstallmentPlan](#installmentplan)         |
| current_queue              | [ClaimQueue](#claimqueue)                   |
| current_coverage           | [ClaimCoverage](#claimcoverage)             |
| accept_assign              | Boolean                                     |
| auto_accident              | Boolean                                     |
| auto_accident_state        | String                                      |
| employment_related         | Boolean                                     |
| other_accident             | Boolean                                     |
| accident_code              | String                                      |
| illness_date               | Date                                        |
| remote_batch_id            | String                                      |
| remote_file_id             | String                                      |
| prior_auth                 | String                                      |
| narrative                  | String                                      |
| account_number             | String                                      |
| snoozed_until              | Date                                        |
| patient_balance            | Decimal                                     |
| aggregate_coverage_balance | Decimal                                     |
| created                    | DateTime                                    |
| modified                   | DateTime                                    |
| diagnosis_codes            | [ClaimDiagnosisCode](#claimdiagnosiscode)[] |
| comments                   | [ClaimComment](#claimcomment)[]             |

**Computed Properties**:

- `total_charges`: Total charges for active line items
- `total_paid`: Sum of paid amounts from postings
- `total_adjusted`: Sum of adjustments and transfers
- `balance`: Remaining balance (coverage + patient)
- `total_patient_paid`: Paid amount by the patient
- `total_payer_paid`: Paid amount by coverages

### ClaimLineItem

Represents individual billed procedures or services tied to a claim.

| Field Name        | Type                                                       |
| ----------------- | ---------------------------------------------------------- |
| dbid              | Integer                                                    |
| billing_line_item | [BillingLineItem](/sdk/data-billing-line-item/)            |
| claim             | [Claim](#claim)                                            |
| status            | [ClaimLineItemStatus](#claimlineitemstatus)                |
| charge            | Decimal                                                    |
| from_date         | String                                                     |
| thru_date         | String                                                     |
| narrative         | String                                                     |
| ndc_code          | String                                                     |
| ndc_dosage        | String                                                     |
| ndc_measure       | String                                                     |
| place_of_service  | [PracticeLocationPOS](/sdk/data-note/#practicelocationpos) |
| proc_code         | String                                                     |
| display           | String                                                     |
| remote_chg_id     | String                                                     |
| units             | Integer                                                    |
| epsdt             | String                                                     |
| family_planning   | [FamilyPlanningOptions](#familyplanningoptions)            |
| created           | DateTime                                                   |
| modified          | DateTime                                                   |

### ClaimCoverage

Links a claim to a specific insurance coverage.

| Field Name                         | Type                                                                     |
| ---------------------------------- | ------------------------------------------------------------------------ |
| dbid                               | Integer                                                                  |
| claim                              | [Claim](#claim)                                                          |
| coverage                           | [Coverage](/sdk/data-coverage/)                                          |
| active                             | Boolean                                                                  |
| payer_name                         | String                                                                   |
| payer_id                           | String                                                                   |
| payer_typecode                     | String                                                                   |
| payer_order                        | [ClaimPayerOrder](#claimpayerorder)                                      |
| payer_addr1                        | String                                                                   |
| payer_addr2                        | String                                                                   |
| payer_city                         | String                                                                   |
| payer_state                        | String                                                                   |
| payer_zip                          | String                                                                   |
| payer_plan_type                    | [ClaimTypeCode](#claimtypecode)                                          |
| coverage_type                      | [CoverageType](/data-coverage/#coveragetype)                             |
| subscriber_employer                | String                                                                   |
| subscriber_group                   | String                                                                   |
| subscriber_number                  | String                                                                   |
| subscriber_plan                    | String                                                                   |
| subscriber_dob                     | String                                                                   |
| subscriber_first_name              | String                                                                   |
| subscriber_last_name               | String                                                                   |
| subscriber_middle_name             | String                                                                   |
| subscriber_phone                   | String                                                                   |
| subscriber_sex                     | [PersonSex](/sdk/data-patient/#sexatbirth)                               |
| subscriber_addr1                   | String                                                                   |
| subscriber_addr2                   | String                                                                   |
| subscriber_city                    | String                                                                   |
| subscriber_state                   | String                                                                   |
| subscriber_zip                     | String                                                                   |
| subscriber_country                 | String                                                                   |
| patient_relationship_to_subscriber | [CoverageRelationshipCode](/sdk/data-coverage/#coveragerelationshipcode) |
| pay_to_addr1                       | String                                                                   |
| pay_to_addr2                       | String                                                                   |
| pay_to_city                        | String                                                                   |
| pay_to_state                       | String                                                                   |
| pay_to_zip                         | String                                                                   |
| resubmission_code                  | String                                                                   |
| payer_icn                          | String                                                                   |
| created                            | DateTime                                                                 |
| modified                           | DateTime                                                                 |

### ClaimComment

Represents a free-text comment made on a Claim.

| Field Name       | Type                               |
| ---------------- | ---------------------------------- |
| id               | UUID                               |
| dbid             | Integer                            |
| claim            | [Claim](#claim)                    |
| created          | DateTime                           |
| modified         | DateTime                           |
| deleted          | Boolean                            |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser) |
| committer        | [CanvasUser](/sdk/data-canvasuser) |
| comment          | String                             |

### ClaimDiagnosisCode

Represents diagnosis codes associated with a claim, ordered by rank.

| Field Name | Type            |
| ---------- | --------------- |
| id         | UUID            |
| dbid       | Integer         |
| claim      | [Claim](#claim) |
| rank       | Integer         |
| code       | String          |
| display    | String          |
| created    | DateTime        |
| modified   | DateTime        |

### ClaimQueue

Defines the metadata for claim queues used in revenue workflows.

| Field Name          | Type                                            |
| ------------------- | ----------------------------------------------- |
| dbid                | Integer                                         |
| queue_sort_ordering | Integer                                         |
| name                | String                                          |
| display_name        | String                                          |
| description         | String                                          |
| show_in_revenue     | Boolean                                         |
| visible_columns     | Array\[[ClaimQueueColumns](#claimqueuecolumns)] |
| created             | DateTime                                        |
| modified            | DateTime                                        |

### ClaimPatient

Captures patient-level data related to a specific claim.

| Field Name  | Type                                       |
| ----------- | ------------------------------------------ |
| dbid        | Integer                                    |
| claim       | [Claim](#claim)                            |
| photo       | String                                     |
| dob         | String                                     |
| first_name  | String                                     |
| last_name   | String                                     |
| middle_name | String                                     |
| phone       | String                                     |
| sex         | [PersonSex](/sdk/data-patient/#sexatbirth) |
| ssn         | String                                     |
| addr1       | String                                     |
| addr2       | String                                     |
| city        | String                                     |
| state       | String                                     |
| zip         | String                                     |
| country     | String                                     |
| created     | DateTime                                   |
| modified    | DateTime                                   |

### InstallmentPlan

Represents a payment plan between a patient and provider.

| Field Name           | Type                                            |
| -------------------- | ----------------------------------------------- |
| creator              | [CanvasUser](/sdk/data-user/)                   |
| patient              | [Patient](/sdk/data-patient/)                   |
| total_amount         | Decimal                                         |
| status               | [InstallmentPlanStatus](#installmentplanstatus) |
| expected_payoff_date | Date                                            |
| created_at           | DateTime                                        |
| updated_at           | DateTime                                        |

## Enumeration types

### ClaimLineItemStatus

| Value   | Label   |
| ------- | ------- |
| active  | Active  |
| removed | Removed |

### LineItemCodes

| Value    |
| -------- |
| COPAY    |
| UNLINKED |

### FamilyPlanningOptions

| Value | Label |
| ----- | ----- |
| Y     | Yes   |
| N     | No    |

### ClaimLineItemStatus

| Value   | Label   |
| ------- | ------- |
| active  | Active  |
| removed | Removed |

### LineItemCodes

| Value    |
| -------- |
| COPAY    |
| UNLINKED |

### FamilyPlanningOptions

| Value | Label |
| ----- | ----- |
| Y     | Yes   |
| N     | No    |

### ClaimPayerOrder

| Value      | Label      |
| ---------- | ---------- |
| Primary    | Primary    |
| Secondary  | Secondary  |
| Tertiary   | Tertiary   |
| Quaternary | Quaternary |
| Quinary    | Quinary    |

### ClaimTypeCode

| Code | Description                          |
| ---- | ------------------------------------ |
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
| ---------------- | ----------------- |
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
| ----- | ---------------------- |
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
| --------- | --------- |
| active    | Active    |
| completed | Completed |
| cancelled | Cancelled |
