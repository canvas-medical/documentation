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

To access banner alerts for a claim:

```python
from canvas_sdk.v1.data.claim import Claim

claim = Claim.objects.get(id="9d2e0f58-338b-11ec-8d3d-0242ac130003")
active_alerts = claim.banner_alerts.filter(status="active")

for alert in active_alerts:
    print(f"[{alert.intent}] {alert.narrative}")
```

## Filtering

```python
from canvas_sdk.v1.data.claim import Claim

# Active claims only
active_claims = Claim.objects.active()
```

## Attributes

### Claim

Represents a complete healthcare claim. Claim belongs to a Note and has a one-to-one relationship with a ClaimPatient.

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
| line_items                 | [ClaimLineItem](#claimlineitem)[]           |
| labels                     | [TaskLabel](/sdk/data-task/#tasklabel)[]    |
| metadata                   | [ClaimMetadata](#claimmetadata)[]           |
| banner_alerts              | [ClaimBannerAlert](#claimbanneralert)[]     |
| provider                   | [ClaimProvider](#claimprovider)             |

**Computed Properties**:

- `total_charges`: Total charges for active line items
- `total_paid`: Sum of paid amounts from postings
- `total_adjusted`: Sum of adjustments and transfers
- `balance`: Remaining balance (coverage + patient)
- `total_patient_paid`: Paid amount by the patient
- `total_payer_paid`: Paid amount by coverages

**Helpful Methods**:

- `get_coverage_by_payer_id(payer_id: str, subscriber_number: str | None = None)`: Finds the active coverage associated with a payer_id. Optionally checks if the subscriber_number matches, which will choose the correct coverage in the case where a patient has two coverages with the same payer_id.

### ClaimLineItem

Represents individual billed procedures or services tied to a claim.

| Field Name        | Type                                                        |
| ----------------- | ----------------------------------------------------------- |
| id                | UUID                                                        |
| dbid              | Integer                                                     |
| billing_line_item | [BillingLineItem](/sdk/data-billing-line-item/)             |
| diagnosis_codes   | [ClaimLineItemDiagnosisCode](#claimlineitemdiagnosiscode)[] |
| claim             | [Claim](#claim)                                             |
| status            | [ClaimLineItemStatus](#claimlineitemstatus)                 |
| charge            | Decimal                                                     |
| from_date         | String                                                      |
| thru_date         | String                                                      |
| narrative         | String                                                      |
| ndc_code          | String                                                      |
| ndc_dosage        | String                                                      |
| ndc_measure       | String                                                      |
| place_of_service  | [PracticeLocationPOS](/sdk/data-note/#practicelocationpos)  |
| proc_code         | String                                                      |
| display           | String                                                      |
| remote_chg_id     | String                                                      |
| units             | Integer                                                     |
| epsdt             | String                                                      |
| family_planning   | [FamilyPlanningOptions](#familyplanningoptions)             |
| created           | DateTime                                                    |
| modified          | DateTime                                                    |

### ClaimLineItemDiagnosisCode

Represents a diagnosis code for a given ClaimLineItem. There exists one ClaimLineItemDiagnosisCode for each ClaimDiagnosisCode, and the "linked" attribute indicates whether or not the diagnosis code is linked to the line item.

| Field Name           | Type                                      |
| -------------------- | ----------------------------------------- |
| id                   | UUID                                      |
| dbid                 | Integer                                   |
| line_item            | [ClaimLineItem](#claimlineitem)           |
| claim_diagnosis_code | [ClaimDiagnosisCode](#claimdiagnosiscode) |
| code                 | String                                    |
| poa                  | String                                    |
| linked               | Boolean                                   |
| created              | DateTime                                  |
| modified             | DateTime                                  |

### ClaimCoverage

Links a claim to a specific insurance coverage.

| Field Name                         | Type                                                                     |
| ---------------------------------- | ------------------------------------------------------------------------ |
| id                                 | UUID                                                                     |
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

### ClaimBannerAlert

Represents banner alerts associated with a claim. Banner alerts are displayed in the UI to surface important information about a claim. To create or remove `ClaimBannerAlert` records, see [Claim Effects](/sdk/effect-claims/#add-banner).

| Field Name  | Type                                                           |
| ----------- | -------------------------------------------------------------- |
| dbid        | Integer                                                        |
| claim       | [Claim](#claim)                                                |
| plugin_name | String                                                         |
| key         | String                                                         |
| narrative   | String                                                         |
| intent      | [BannerAlertIntent](/sdk/data-banner-alert/#banneralertintent) |
| href        | String                                                         |
| status      | [BannerAlertStatus](/sdk/data-banner-alert/#banneralertstatus) |
| created     | DateTime                                                       |
| modified    | DateTime                                                       |

### ClaimDiagnosisCode

Represents diagnosis codes associated with a claim, ordered by rank.

| Field Name                | Type                                                        |
| ------------------------- | ----------------------------------------------------------- |
| id                        | UUID                                                        |
| dbid                      | Integer                                                     |
| claim                     | [Claim](#claim)                                             |
| line_item_diagnosis_codes | [ClaimLineItemDiagnosisCode](#claimlineitemdiagnosiscode)[] |
| rank                      | Integer                                                     |
| code                      | String                                                      |
| display                   | String                                                      |
| created                   | DateTime                                                    |
| modified                  | DateTime                                                    |

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

### ClaimLabel

Represents labels assigned to the claim.

| Field Name | Type                                   |
| ---------- | -------------------------------------- |
| id         | UUID                                   |
| dbid       | Integer                                |
| claim      | [Claim](#claim)                        |
| label      | [TaskLabel](/sdk/data-task/#tasklabel) |

### ClaimMetadata

Represents key-value metadata associated with a claim. Each claim-key pair is unique.

| Field Name | Type                  |
| ---------- | --------------------- |
| id         | UUID                  |
| dbid       | Integer               |
| claim      | [Claim](#claim)       |
| key        | String                |
| value      | String                |
| created    | DateTime              |
| modified   | DateTime              |

### ClaimProvider

Captures provider-level data related to a specific claim.

| Field Name                         | Type            |
| ---------------------------------- | --------------- |
| id                                 | UUID            |
| dbid                               | Integer         |
| claim                              | [Claim](#claim) |
| clia_number                        | String          |
| billing_provider_name              | String          |
| billing_provider_phone             | String          |
| billing_provider_addr1             | String          |
| billing_provider_addr2             | String          |
| billing_provider_city              | String          |
| billing_provider_state             | String          |
| billing_provider_zip               | String          |
| billing_provider_id                | String          |
| billing_provider_npi               | String          |
| billing_provider_tax_id            | String          |
| billing_provider_tax_id_type       | String          |
| billing_provider_taxonomy          | String          |
| provider_id                        | String          |
| provider_first_name                | String          |
| provider_last_name                 | String          |
| provider_middle_name               | String          |
| provider_npi                       | String          |
| provider_tax_id                    | String          |
| provider_tax_id_type               | String          |
| provider_taxonomy                  | String          |
| provider_ptan_identifier           | String          |
| referring_provider_id              | String          |
| referring_provider_first_name      | String          |
| referring_provider_last_name       | String          |
| referring_provider_middle_name     | String          |
| referring_provider_npi             | String          |
| referring_provider_ptan_identifier | String          |
| ordering_provider_first_name       | String          |
| ordering_provider_last_name        | String          |
| ordering_provider_middle_name      | String          |
| ordering_provider_npi              | String          |
| facility_id                        | String          |
| facility_name                      | String          |
| facility_npi                       | String          |
| facility_addr1                     | String          |
| facility_addr2                     | String          |
| facility_city                      | String          |
| facility_state                     | String          |
| facility_zip                       | String          |
| hosp_from_date                     | String          |
| hosp_to_date                       | String          |
| created                            | DateTime        |
| modified                           | DateTime        |

### ClaimSubmission

Captures clearinghouse submission details about a claim.

| Field Name             | Type                            |
| ---------------------- | ------------------------------- |
| id                     | UUID                            |
| dbid                   | Integer                         |
| claim                  | [Claim](#claim)                 |
| coverage               | [ClaimCoverage](#claimcoverage) |
| clearinghouse_claim_id | String                          |
| claim_index            | Integer                         |

### InstallmentPlan

Represents a payment plan between a patient and provider.

| Field Name           | Type                                            |
| -------------------- | ----------------------------------------------- |
| creator              | [CanvasUser](/sdk/data-canvasuser/)             |
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
