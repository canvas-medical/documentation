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

<!-- source: discussion #1274 -->
## When a claim is created

A claim is created for an appointment or note only when the note's type is billable. A note type with `is_billable` set to `False`, such as the built-in Chart review type, produces a note and no claim, so check the flag rather than assuming every appointment produces a claim.

The flag lives on [NoteType](/sdk/data-note/#notetype), reached through the note's `note_type_version` attribute. To read the claim itself, use the note's `claims` reverse relation; a note has at most one claim, so take it with `first()`:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")

expects_claim = note.note_type_version.is_billable
claim = note.claims.first()
```

<!-- source: discussion #1642 -->
<!-- REVIEW: clinical-accuracy sign-off required -->
## Claim balances and totals

The money on a claim comes from two stored balance fields plus a set of computed properties layered over the claim's line items and postings.

`patient_balance` and `aggregate_coverage_balance` are stored on the claim and kept in sync by signals as coverage postings transfer money to the patient, as coverage is added or removed, and as the patient makes payments. Reading them needs no aggregation on your part, and they stay correct when coverage is added after a note is signed.

The rest are computed on access, each over a different slice of the claim:

| Property | What it adds up |
| --- | --- |
| `total_charges` | `charge` across the claim's active line items, with copay and unlinked items excluded |
| `total_paid` | `paid_amount` across every active posting on the claim, coverage and patient alike |
| `total_payer_paid` | `paid_amount` across the active postings of the claim's active coverages |
| `total_patient_paid` | `paid_amount` across the active postings on the claim's patient record |
| `total_adjusted` | `contractual_adjusted_amount` plus `transferred_amount` across every active posting |
| `balance` | `aggregate_coverage_balance` plus `patient_balance`, the coverage side and the patient side together |

A posting counts as active when it has not been entered in error. Because `total_paid` spans both sides of the claim, `total_payer_paid` and `total_patient_paid` are that figure split by who paid it.

### Computing patient-allocated charges

To find how much has been allocated to the patient on a claim, add what the patient still owes to what they have already paid:

```python
from canvas_sdk.v1.data.claim import Claim

claim = Claim.objects.get(id="9d2e0f58-338b-11ec-8d3d-0242ac130003")

patient_allocated = claim.patient_balance + claim.total_patient_paid
```

This holds for self-pay and insured claims alike, including a self-pay claim carrying no postings at all.

<!-- source: discussion #1407 -->
## Detecting claim changes in the read replica

The `quality_and_revenue_claim.last_modified` column does not update when a claim only moves between queues (the `current_queue_id` changes). Queue movements are sometimes recorded as rows in the `quality_and_revenue_claimstatechangeevent` table instead of updating the claim's modified timestamp. To find claims that changed for any reason in the read replica, take the most recent of the two timestamps with `GREATEST(claim.modified, claimstatechangeevent.modified)`:

```sql
SELECT
    c.id AS claim_id,
    GREATEST(c.modified, csc.modified) AS claim_modified,
    c.created AS claim_created,
    q.name AS current_queue
FROM quality_and_revenue_claim c
    -- Latest claim state change event per claim
    LEFT JOIN LATERAL (
        SELECT id, modified, queue_entered_id
        FROM quality_and_revenue_claimstatechangeevent
        WHERE claim_id = c.id
        ORDER BY modified DESC, id DESC
        LIMIT 1
    ) csc ON TRUE
    LEFT JOIN quality_and_revenue_queue q
        ON c.current_queue_id = q.id
WHERE
    c.modified >= NOW() - INTERVAL '1 day'
    OR csc.modified >= NOW() - INTERVAL '1 day'
ORDER BY 2;
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

| Field Name                 | Type                                                  | Description                               |
|----------------------------|-------------------------------------------------------|-------------------------------------------|
| id                         | UUID                                                  |                                           |
| dbid                       | Integer                                               |                                           |
| note                       | [Note](/sdk/data-note/)                               |                                           |
| installment_plan           | [InstallmentPlan](#installmentplan)                   |                                           |
| current_queue              | [ClaimQueue](#claimqueue)                             |                                           |
| current_coverage           | [ClaimCoverage](#claimcoverage)                       |                                           |
| accept_assign              | Boolean                                               |                                           |
| auto_accident              | Boolean                                               |                                           |
| auto_accident_state        | String                                                |                                           |
| employment_related         | Boolean                                               |                                           |
| other_accident             | Boolean                                               |                                           |
| accident_code              | String                                                |                                           |
| illness_date               | Date                                                  |                                           |
| remote_batch_id            | String                                                |                                           |
| remote_file_id             | String                                                |                                           |
| prior_auth                 | String                                                |                                           |
| narrative                  | String                                                |                                           |
| account_number             | String                                                |                                           |
| snoozed_until              | Date                                                  |                                           |
| patient_balance            | Decimal                                               |                                           |
| aggregate_coverage_balance | Decimal                                               |                                           |
| created                    | DateTime                                              |                                           |
| modified                   | DateTime                                              |                                           |
| diagnosis_codes            | [ClaimDiagnosisCode](#claimdiagnosiscode)[]           |                                           |
| comments                   | [ClaimComment](#claimcomment)[]                       |                                           |
| line_items                 | [ClaimLineItem](#claimlineitem)[]                     |                                           |
| labels                     | [TaskLabel](/sdk/data-task/#tasklabel)[]              |                                           |
| metadata                   | [ClaimMetadata](#claimmetadata)[]                     |                                           |
| banner_alerts              | [ClaimBannerAlert](#claimbanneralert)[]               |                                           |
| provider                   | [ClaimProvider](#claimprovider)                       |                                           |
| incident_to                | Boolean                                               |                                           |
| supervising_provider       | [ClaimSupervisingProvider](#claimsupervisingprovider) |                                           |
| latest_invoice             | [Invoice](/sdk/data-invoice/#invoice)                 |                                           |
| patient                    | [ClaimPatient](#claimpatient)                         |                                           |
| coverages                  | [ClaimCoverage](#claimcoverage)[]                     |                                           |
| submissions                | [ClaimSubmission](#claimsubmission)[]                 |                                           |
| postings                   | [BasePosting](/sdk/data-posting/#baseposting)[]       |                                           |
| total_charges              | Decimal (computed)                                    | Total charges for active line items       |
| total_paid                 | Decimal (computed)                                    | Sum of paid amounts from postings         |
| total_adjusted             | Decimal (computed)                                    | Sum of adjustments and transfers          |
| balance                    | Decimal (computed)                                    | Remaining balance (coverage plus patient) |
| total_patient_paid         | Decimal (computed)                                    | Amount paid by the patient                |
| total_payer_paid           | Decimal (computed)                                    | Amount paid by coverages                  |

**Helpful Methods**:

- `get_coverage_by_payer_id(payer_id: str, subscriber_number: str | None = None)`: Finds the active coverage associated with a payer_id. Optionally checks if the subscriber_number matches, which will choose the correct coverage in the case where a patient has two coverages with the same payer_id.

### ClaimSupervisingProvider

An immutable snapshot of a claim's supervising provider (837P loop 2310D), captured at claim creation from the note's supervising provider and frozen thereafter, so later edits to the note or the underlying Staff record do not retroactively change a submitted claim.

| Field Name  | Type                                                |
| ----------- | --------------------------------------------------- |
| id          | UUID                                                |
| dbid        | Integer                                             |
| claim       | [Claim](#claim)                                     |
| staff       | [Staff](/sdk/data-staff/#staff)                     |
| first_name  | String                                              |
| last_name   | String                                              |
| middle_name | String                                              |
| npi         | String                                              |
| taxonomy    | String                                              |
| tax_id      | String                                              |
| tax_id_type | [TaxIDType](/sdk/data-enumeration-types/#taxidtype) |
| created     | DateTime                                            |
| modified    | DateTime                                            |

### ClaimLineItem

Represents individual billed procedures or services tied to a claim.

| Field Name        | Type                                                        |
| ----------------- | ----------------------------------------------------------- |
| id                | UUID                                                        |
| dbid              | Integer                                                     |
| billing_line_item | [BillingLineItem](/sdk/data-billing-line-item/)             |
| diagnosis_codes   | [ClaimLineItemDiagnosisCode](#claimlineitemdiagnosiscode)[] |
| modifiers         | [ClaimLineItemModifier](#claimlineitemmodifier)[]           |
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

### ClaimLineItemModifier

Represents a modifier code for a given ClaimLineItem.

| Field Name           | Type                                      |
| -------------------- | ----------------------------------------- |
| id                   | UUID                                      |
| dbid                 | Integer                                   |
| line_item            | [ClaimLineItem](#claimlineitem)           |
| modifier             | String                                    |
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
| coverage_type                      | [CoverageType](/sdk/data-coverage/#coveragetype)                             |
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
| originator       | [CanvasUser](/sdk/data-canvasuser) |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser) |
| committer        | [CanvasUser](/sdk/data-canvasuser) |
| comment          | String                             |

### ClaimBannerAlert

Represents banner alerts associated with a claim. Banner alerts are displayed in the UI to surface important information about a claim. To create or remove `ClaimBannerAlert` records, see [Claim Effects](/sdk/effect-claims/#add-banner).

| Field Name  | Type                                                           |
| ----------- | -------------------------------------------------------------- |
| id          | UUID                                                           |
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
| id                  | UUID                                            |
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
| provider_addr1                     | String          |
| provider_addr2                     | String          |
| provider_city                      | String          |
| provider_state                     | String          |
| provider_zip                       | String          |
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
| created                | DateTime                        |
| modified               | DateTime                        |
| claim                  | [Claim](#claim)                 |
| coverage               | [ClaimCoverage](#claimcoverage) |
| clearinghouse_claim_id | String                          |
| claim_index            | Integer                         |

### InstallmentPlan

Represents a payment plan between a patient and provider.

| Field Name           | Type                                            |
| -------------------- | ----------------------------------------------- |
| dbid                 | Integer                                         |
| creator              | [CanvasUser](/sdk/data-canvasuser/)             |
| patient              | [Patient](/sdk/data-patient/)                   |
| total_amount         | Decimal                                         |
| status               | [InstallmentPlanStatus](#installmentplanstatus) |
| expected_payoff_date | Date                                            |
| created              | DateTime                                        |
| modified             | DateTime                                        |
| claims               | [Claim](#claim)[]                               |

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
