---
title: "CarePlan"
slug: "data-care-plan"
excerpt: "Read a patient's care plans and their categories from a plugin."
hidden: false
---

## Introduction

The `CarePlan` model represents a patient's care plan: who started it, its status, its intent, and its category. Read it when your plugin needs to know whether a patient has a plan of care. The FHIR API serves the same records as the [CarePlan](/api/careplan/) resource.

Canvas creates a patient's care plan when the first goal is recorded for that patient, for example with the [Goal](/sdk/commands/#goal) command. A patient has at most one care plan, and later goals belong to the same plan. The care plan's `originator` is the originator of the note the first goal was recorded in.

Every care plan has the same values:

- `status` is `active`.
- `intent` is `plan`.
- `category` is the SNOMED CT code `734163000` (Care plan), stored as a `CarePlanCoding`.

The care plan doesn't link to goals. Read the patient's goals with the [Goal](/sdk/data-goal/) model.

## Basic usage

To get a care plan by identifier, use the `get` method on the `CarePlan` model manager:

```python
from canvas_sdk.v1.data import CarePlan

care_plan = CarePlan.objects.get(id="9c71f9cc-169b-42ad-aa4d-b652cdb13fd8")
```

If you have a patient object, read the patient's care plans with the `care_plans` attribute:

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
care_plans = patient.care_plans.all()
```

If you have a patient ID, use the `for_patient` method on the `CarePlan` model manager:

```python
from canvas_sdk.v1.data import CarePlan

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
care_plans = CarePlan.objects.for_patient(patient_id)
```

## Categories

A care plan's `category` attribute holds its `CarePlanCoding`, or `None` when the plan has no category. Read the coding's `system`, `code`, and `display`:

```python
from canvas_sdk.v1.data import CarePlan

care_plan = CarePlan.objects.select_related("category").get(id="9c71f9cc-169b-42ad-aa4d-b652cdb13fd8")
if care_plan.category is not None:
    category_label = f"{care_plan.category.display} ({care_plan.category.system}|{care_plan.category.code})"
```

From a coding, the `care_plans` attribute returns every care plan in that category.

## Filtering

Filter care plans by any attribute on the model. Compare `status` and `intent` with the [CarePlanStatus](#careplanstatus) and [CarePlanIntent](#careplanintent) values rather than raw strings.

**Find a patient's active care plans**

```python
from canvas_sdk.v1.data import CarePlan, CarePlanStatus

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
active_plans = CarePlan.objects.for_patient(patient_id).filter(status=CarePlanStatus.ACTIVE)
```

**Find care plans by category code**

```python
from canvas_sdk.v1.data import CarePlan

plans = CarePlan.objects.filter(category__system="http://snomed.info/sct", category__code="734163000")
```

**Find care plans a staff member started**

`originator` links to a [CanvasUser](/sdk/data-canvasuser/), which has a `dbid` but no `id`. Filter on the staff member's `user` instead:

```python
from canvas_sdk.v1.data import CarePlan, Staff

staff = Staff.objects.get(id="3640cd20de8a470aa570a852859ac87e")
plans = CarePlan.objects.filter(originator=staff.user)
```

## Attributes

### CarePlan

| Field Name | Type                                         |
| ---------- | -------------------------------------------- |
| id         | UUID                                         |
| dbid       | Integer                                      |
| created    | DateTime                                     |
| modified   | DateTime                                     |
| patient    | [Patient](/sdk/data-patient/#patient)        |
| originator | [CanvasUser](/sdk/data-canvasuser/)          |
| status     | [CarePlanStatus](#careplanstatus)            |
| intent     | [CarePlanIntent](#careplanintent)            |
| category   | [CarePlanCoding](#careplancoding) \| `None`  |

### CarePlanCoding

| Field Name    | Type                      |
| ------------- | ------------------------- |
| dbid          | Integer                   |
| created       | DateTime                  |
| modified      | DateTime                  |
| system        | String                    |
| version       | String                    |
| code          | String                    |
| display       | String                    |
| user_selected | Boolean                   |
| care_plans    | [CarePlan](#careplan)[]   |

## Enumeration types

### CarePlanStatus

| Value            | Label            |
| ---------------- | ---------------- |
| draft            | Draft            |
| active           | Active           |
| on-hold          | On Hold          |
| revoked          | Revoked          |
| completed        | Completed        |
| entered-in-error | Entered in Error |
| unknown          | Unknown          |

### CarePlanIntent

| Value    | Label    |
| -------- | -------- |
| proposal | Proposal |
| plan     | Plan     |
| order    | Order    |
| option   | Option   |
