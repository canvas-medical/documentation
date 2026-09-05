---
title: "Medication"
slug: "data-medication"
excerpt: "Canvas SDK Medication"
hidden: false
---

## Introduction

The `Medication` model represents a record of a medication that is being consumed by a patient, either now, in the past, or in the future. `Medication` records can represent both prescriptions and medication statements for a patient.

## Basic usage

To get a medication by identifier, use the `get` method on the `Medication` model manager:

```python
from canvas_sdk.v1.data.medication import Medication

medication = Medication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the medications for a patient can be accessed with the `medications` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
medications = patient.medications.all()
```

If you have a patient ID, you can get the medications for the patient with the `for_patient` method on the `Medication` model manager:

```python
from canvas_sdk.v1.data.medication import Medication

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
medication = Medication.objects.for_patient(patient_id)
```

# Codings

The codings for a medication can be accessed with the `codings` attribute on an `Medication` object:

```python
from canvas_sdk.v1.data.medication import Medication
from logger import log

medication = Medication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in medication.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Filtering

Medications can be filtered by any attribute that exists on the model.

Filtering for medications is done with the `filter` method on the `Medication` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.medication import Medication

medications = Medication.objects.filter(status="active")
```

### By ValueSet

See [Value Sets](/sdk/data-value-sets/) for the library of built-in value sets and how to create your own.

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.medication import Medication
from canvas_sdk.value_set.v2022.medication import AdhdMedications

medications = Medication.objects.find(AdhdMedications)
```

<!-- source: discussion #1613 -->
<!-- REVIEW: clinical-accuracy sign-off required -->
## Filtering to match the patient chart

Filtering on `status == "active"` alone does not reproduce the chart's medication list. Per Canvas, the chart applies two exclusion layers before considering status:

1. Exclude uncommitted and entered-in-error records — a medication must have a non-null `committer` (it was finalized) and a null `entered_in_error` (no one flagged it as erroneous).
2. Filter by `status` — the chart defaults to `status == "active"`; users can toggle to inactive or all.

To replicate the chart's "active medications" view:

```python
from canvas_sdk.v1.data.medication import Medication

active_meds = Medication.objects.filter(
    patient__id=patient_id,
    committer_id__isnull=False,
    entered_in_error_id__isnull=True,
    status="active",
)
```

For all visible medications (the chart's "All" filter — active plus inactive), omit the status filter:

```python
all_visible_meds = Medication.objects.filter(
    patient__id=patient_id,
    committer_id__isnull=False,
    entered_in_error_id__isnull=True,
)
```

Per Canvas, the precedence of the relevant fields is: `entered_in_error` (highest — excludes from all chart views) → `committer` (must be set for the record to count as finalized) → `status` (only distinguishes active vs. inactive after the first two pass). `start_date` and `end_date` are informational only and are not used for filtering, so you should not derive your own normalized status from them. The `deleted` field is inherited from a base class but is effectively never `True` on `Medication` records and can be ignored.

### How status is computed

Per Canvas, `status` is set automatically from the medication's command history, not set directly by users. A medication is `inactive` if it has a committed, non-entered-in-error stop medication event; a committed, non-entered-in-error prescription cancellation; only refill denials; or no committed commands linked to it. Otherwise it is `active`. Canvas recomputes `status`, `start_date`, and `end_date` whenever a related command is committed, entered in error, or created (for example a medication statement, a prescription/refill/adjust, a stop event, a prescription cancellation, an eRx refill response, or a note date-of-service change).

Per Canvas, one exception is the FHIR API: creating a `MedicationStatement` via FHIR writes `effectivePeriod.start`/`effectivePeriod.end` and the FHIR-derived status directly to the `Medication` record and bypasses this synchronization, so those values are preserved until a later action triggers recomputation from the command chain.

## Attributes

### Medication

| Field Name                     | Type                                                     |
| ------------------------------ | -------------------------------------------------------- |
| id                             | UUID                                                     |
| dbid                           | Integer                                                  |
| patient                        | [Patient](/sdk/data-patient/#patient)                    |
| entered_in_error               | [CanvasUser](/sdk/data-canvasuser)                       |
| committer                      | [CanvasUser](/sdk/data-canvasuser)                       |
| status                         | String                                                   |
| start_date                     | Date                                                     |
| end_date                       | Date                                                     |
| quantity_qualifier_description | String                                                   |
| clinical_quantity_description  | String                                                   |
| potency_unit_code              | String                                                   |
| national_drug_code             | String                                                   |
| erx_quantity                   | String                                                   |
| codings                        | [MedicationCoding](#medicationcoding)[]                  |
| medication_statements          | [MedicationStatement](/sdk/data-medication-statement)[]  |
| change_medications             | [ChangeMedication](/sdk/data-change-medication)[]        |
| stopmedicationevent_set        | [StopMedicationEvent](/sdk/data-stop-medication-event)[] |
| prescriptions                  | [Prescription](/sdk/data-prescription)[]                 |
| previous_medications           | [Prescription](/sdk/data-prescription)[]                 |
| prescription_change_responses  | [PrescriptionChangeResponse](/sdk/data-prescription-change-response/#prescriptionchangeresponse)[] |

### MedicationCoding

| Field Name    | Type                      |
| ------------- | ------------------------- |
| dbid          | Integer                   |
| system        | String                    |
| version       | String                    |
| code          | String                    |
| display       | String                    |
| user_selected | Boolean                   |
| medication    | [Medication](#medication) |

<br/>
<br/>
<br/>
