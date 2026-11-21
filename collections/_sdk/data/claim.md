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

The flag lives on [NoteType](/sdk/data-note/#notetype), reached through the note's `note_type_version` attribute. To read the claim itself, call the note's `get_claim()` method, which returns the note's most recent claim, or `None` when it has none:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")

expects_claim = note.note_type_version.is_billable
claim = note.get_claim()
```

## How diagnosis codes are ranked

A claim lists its diagnosis codes in `rank` order, and rank 1 is the primary diagnosis. Each time Canvas syncs a claim with its note, such as when the note is locked or its charges are pushed, the sync adds each ICD-10 code on the note that the claim doesn't have yet. It adds each code once, even when two of the note's conditions share it.

A note in the revamped format, on an instance in the [revamped note beta program](/product-updates/note-revamp/), also sets the order of the claim's codes. The sync ranks the note's codes first, in the order their commands appear in the note body. Codes that were added only on the claim follow, in their current order. A condition takes the position of the topmost command that records or assesses it, such as Diagnose, Assess, or Update Diagnosis. Conditions with no command of their own, such as an order's indication, come after those, in the order they were added. When a provider moves commands in the note, the next sync re-ranks the claim to match, including a claim that has already been filed, and adds a comment to the claim listing the new order.

For other notes, the sync adds new codes after the existing ones and leaves the existing ranks unchanged.

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

## Claim history

Canvas records an event each time a claim changes queue, has a coverage changed, is assigned, or is snoozed. Read these events to build an audit trail or to report on how claims move through your revenue workflow. Each event has a `created` timestamp, and each kind has its own relation on the claim:

| Relation on the claim | Model | What it records |
| --- | --- | --- |
| `claim_state_change_events` | [ClaimStateChangeEvent](#claimstatechangeevent) | The queue the claim left and the queue it entered |
| `claim_coverage_events` | [ClaimCoverageEvent](#claimcoverageevent) | A coverage activated, deactivated, made current, reordered, or edited |
| `assignee_events` | [ClaimAssigneeEvent](#claimassigneeevent) | The staff member or team the claim was assigned to, or that it was unassigned |
| `snooze_events` | [ClaimSnoozeEvent](#claimsnoozeevent) | A snooze set, cleared, or expired |

To list a claim's queue moves in order:

```python
from canvas_sdk.v1.data import Claim

claim = Claim.objects.get(id="9d2e0f58-338b-11ec-8d3d-0242ac130003")

for event in claim.claim_state_change_events.select_related("queue_exited", "queue_entered").order_by("created"):
    exited = event.queue_exited.display_name if event.queue_exited else None
    entered = event.queue_entered.display_name if event.queue_entered else None
    print(f"{event.created}: {exited} -> {entered}")
```

A [ClaimQueue](#claimqueue) lists the moves into it as `enter_events` and the moves out of it as `exit_events`, and a [ClaimCoverage](#claimcoverage) lists its own changes as `events`.

## Claim responses

When a clearinghouse or payer answers a submitted claim, Canvas stores the answer as a [ClaimResponse](#claimresponse) on the claim's `claim_responses`. Each message in the answer, such as a rejection reason, is a [ClaimResponseDetail](#claimresponsedetail) on the response's `responses`.

`status` holds the code the clearinghouse sent. [ClaimResponseStatus](#claimresponsestatus) names the two codes Canvas acts on: `A` (accepted) and `R` (rejected). To read why a claim was rejected:

```python
from canvas_sdk.v1.data import Claim, ClaimResponseStatus

claim = Claim.objects.get(id="9d2e0f58-338b-11ec-8d3d-0242ac130003")

rejections = claim.claim_responses.committed().filter(status=ClaimResponseStatus.REJECTED)
for claim_response in rejections:
    for detail in claim_response.responses.all():
        print(claim_response.response_time, detail.response_code, detail.response)
```

`committed()` keeps responses that were committed and not entered in error.

To find the remits that paid a claim, read `claim.remits`. Each one is a [BaseRemittanceAdvice](/sdk/data-posting/#baseremittanceadvice).

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
| assignee                   | [Staff](/sdk/data-staff/#staff)                       | Staff member the claim is assigned to     |
| team                       | [Team](/sdk/data-team/#team)                          | Team the claim is assigned to             |
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
| remits                     | [BaseRemittanceAdvice](/sdk/data-posting/#baseremittanceadvice)[] | Remits that cover the claim   |
| full_invoices              | [Invoice](/sdk/data-invoice/#invoice)[]               | Statements the claim appeared on          |
| claim_responses            | [ClaimResponse](#claimresponse)[]                     |                                           |
| claim_state_change_events  | [ClaimStateChangeEvent](#claimstatechangeevent)[]     |                                           |
| claim_coverage_events      | [ClaimCoverageEvent](#claimcoverageevent)[]           |                                           |
| assignee_events            | [ClaimAssigneeEvent](#claimassigneeevent)[]           |                                           |
| snooze_events              | [ClaimSnoozeEvent](#claimsnoozeevent)[]               |                                           |
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
| newlineitempayments    | QuerySet[[NewLineItemPayment](/sdk/data-posting/#newlineitempayment)]       |
| newlineitemadjustments | QuerySet[[NewLineItemAdjustment](/sdk/data-posting/#newlineitemadjustment)] |
| lineitemtransfers      | QuerySet[[LineItemTransfer](/sdk/data-posting/#lineitemtransfer)]           |
| lineitemalloweds       | QuerySet[[LineItemAllowed](/sdk/data-posting/#lineitemallowed)]             |
| remark_codes           | QuerySet[[RemarkCode](/sdk/data-posting/#remarkcode)]                       |

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
| payer_typecode                     | [ClaimTypeCode](#claimtypecode)                                          |
| payer_order                        | [ClaimPayerOrder](#claimpayerorder)                                      |
| payer_addr1                        | String                                                                   |
| payer_addr2                        | String                                                                   |
| payer_city                         | String                                                                   |
| payer_state                        | String                                                                   |
| payer_zip                          | String                                                                   |
| payer_plan_type                    | [CoverageType](/sdk/data-coverage/#coveragetype)                         |
| coverage_type                      | [TransactorCoverageType](/sdk/data-coverage/#transactorcoveragetype)     |
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
| events                             | QuerySet[[ClaimCoverageEvent](#claimcoverageevent)]                      |

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

Represents diagnosis codes associated with a claim, ordered by rank. See [How diagnosis codes are ranked](#how-diagnosis-codes-are-ranked).

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
| enter_events        | QuerySet[[ClaimStateChangeEvent](#claimstatechangeevent)] |
| exit_events         | QuerySet[[ClaimStateChangeEvent](#claimstatechangeevent)] |

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

### ClaimStateChangeEvent

Records a claim leaving one queue and entering another.

| Field Name    | Type                                | Description                         |
|---------------|-------------------------------------|-------------------------------------|
| dbid          | Integer                             |                                     |
| claim         | [Claim](#claim)                     |                                     |
| queue_exited  | [ClaimQueue](#claimqueue)           | Queue the claim left                |
| queue_entered | [ClaimQueue](#claimqueue)           | Queue the claim entered             |
| originator    | [CanvasUser](/sdk/data-canvasuser/) | User who moved the claim            |
| created       | DateTime                            |                                     |
| modified      | DateTime                            |                                     |

### ClaimCoverageEvent

Records a change to one of a claim's coverages.

| Field Name     | Type                                                | Description                    |
|----------------|-----------------------------------------------------|--------------------------------|
| dbid           | Integer                                             |                                |
| claim          | [Claim](#claim)                                     |                                |
| claim_coverage | [ClaimCoverage](#claimcoverage)                     | Coverage that changed          |
| event_type     | [ClaimCoverageEventType](#claimcoverageeventtype)   | What changed                   |
| originator     | [CanvasUser](/sdk/data-canvasuser/)                 | User who made the change       |
| created        | DateTime                                            |                                |
| modified       | DateTime                                            |                                |

### ClaimAssigneeEvent

Records a change to who owns a claim: a staff member, a team, or nobody.

| Field Name    | Type                                | Description                                                       |
|---------------|-------------------------------------|-------------------------------------------------------------------|
| dbid          | Integer                             |                                                                   |
| claim         | [Claim](#claim)                     |                                                                   |
| assignee      | [Staff](/sdk/data-staff/#staff)     | Staff member the claim was assigned to                            |
| team          | [Team](/sdk/data-team/#team)        | Team the claim was assigned to                                    |
| assignee_name | String                              | Staff member's name at the time of the change                     |
| team_name     | String                              | Team's name at the time of the change                             |
| originator    | [CanvasUser](/sdk/data-canvasuser/) | User who made the change, or `None` when a plugin made it         |
| created       | DateTime                            |                                                                   |
| modified      | DateTime                            |                                                                   |

- When both `assignee` and `team` are `None`, the claim was unassigned.
- `assignee_name` and `team_name` keep the owner's name after the staff member or team is deleted and `assignee` or `team` becomes `None`.

### ClaimSnoozeEvent

Records a claim's snooze being set, cleared, or expiring.

| Field Name | Type                                  | Description                                        |
|------------|---------------------------------------|----------------------------------------------------|
| dbid       | Integer                               |                                                    |
| claim      | [Claim](#claim)                       |                                                    |
| state      | [ClaimSnoozeState](#claimsnoozestate) |                                                    |
| date       | Date                                  | Date the claim is snoozed until, empty on a clear  |
| originator | [CanvasUser](/sdk/data-canvasuser/)   | User who made the change                           |
| created    | DateTime                              |                                                    |
| modified   | DateTime                              |                                                    |

### ClaimResponse

A clearinghouse or payer response to a submitted claim.

| Field Name              | Type                                | Description                                                  |
|-------------------------|-------------------------------------|--------------------------------------------------------------|
| dbid                    | Integer                             |                                                              |
| claim                   | [Claim](#claim)                     |                                                              |
| status                  | String                              | Code the clearinghouse sent; see [ClaimResponseStatus](#claimresponsestatus) |
| response_time           | DateTime                            |                                                              |
| clearinghouse_claim_id  | String                              |                                                              |
| remote_claim_id         | String                              |                                                              |
| batch_id                | String                              |                                                              |
| file_id                 | String                              |                                                              |
| file_name               | String                              |                                                              |
| from_date               | Date                                |                                                              |
| payer_id                | String                              |                                                              |
| subscriber_number       | String                              |                                                              |
| billing_provider_npi    | String                              |                                                              |
| billing_provider_tax_id | String                              |                                                              |
| sender_icn              | String                              |                                                              |
| sender_name             | String                              |                                                              |
| sender_id               | String                              |                                                              |
| total_charge            | Decimal                             |                                                              |
| originator              | [CanvasUser](/sdk/data-canvasuser/) |                                                              |
| committer               | [CanvasUser](/sdk/data-canvasuser/) |                                                              |
| entered_in_error        | [CanvasUser](/sdk/data-canvasuser/) |                                                              |
| created                 | DateTime                            |                                                              |
| modified                | DateTime                            |                                                              |
| responses               | QuerySet[[ClaimResponseDetail](#claimresponsedetail)] | Messages in the response                   |

### ClaimResponseDetail

One message within a claim response.

| Field Name                | Type                            |
|---------------------------|---------------------------------|
| dbid                      | Integer                         |
| claim_response            | [ClaimResponse](#claimresponse) |
| clearinghouse_response_id | String                          |
| response_code             | String                          |
| response                  | String                          |
| fields                    | String                          |
| status                    | String                          |
| created                   | DateTime                        |
| modified                  | DateTime                        |

## Enumeration types

### ClaimCoverageEventType

| Value       | Label      |
|-------------|------------|
| activate    | Activate   |
| deactivated | Deactivate |
| current     | Current    |
| reorder     | Reordered  |
| edit        | Edited     |

### ClaimSnoozeState

| Value  | Label  |
|--------|--------|
| set    | set    |
| clear  | clear  |
| expire | expire |

### ClaimResponseStatus

| Value | Label    |
|-------|----------|
| A     | Accepted |
| R     | Rejected |

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
