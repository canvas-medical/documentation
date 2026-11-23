---
title: "SuspectHCC"
slug: "data-suspect-hcc"
excerpt: "Canvas SDK SuspectHCC"
hidden: false
---

## Introduction

The `SuspectHCC` model is a Hierarchical Condition Category (HCC) suspected on a patient. Use it in risk adjustment reporting, or to find the suspected HCCs that are still open on a patient.

Each suspected HCC has a `kind` that says why Canvas suspects it:

- `implied_by_clinical_data`: the patient's clinical data implies the HCC. `hcc_code` and `hcc_description` name the HCC, and `reasons` lists the clinical data behind it, such as `Condition: End-stage liver disease`.
- `previous_condition`: the patient had a diagnosis that maps to an HCC. `previous_condition` holds that diagnosis and its code, such as `Bitten by orca, sequela (W56.21XS)`, and `hcc_description` holds its description. `hcc_code` is empty and `reasons` is an empty list.

## Basic usage

A suspected HCC has no `id` attribute. To get one by its database identifier, use the `get` method on the `SuspectHCC` model manager:

```python
from canvas_sdk.v1.data import SuspectHCC

suspect_hcc = SuspectHCC.objects.get(dbid=1234)
```

If you have a patient object, the patient's suspected HCCs can be accessed with the `suspect_hccs` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
suspect_hccs = patient.suspect_hccs.all()
```

## Filtering

Filter on `status` to get the suspected HCCs that are still open, and on `kind` to get the ones suspected for a given reason. The `SuspectHCCStatus` and `SuspectHCCKind` enumerations hold the values:

```python
from canvas_sdk.v1.data import Patient, SuspectHCCKind, SuspectHCCStatus

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")

active_suspect_hccs = patient.suspect_hccs.filter(status=SuspectHCCStatus.ACTIVE)

from_previous_conditions = patient.suspect_hccs.filter(
    status=SuspectHCCStatus.ACTIVE,
    kind=SuspectHCCKind.PREVIOUS_CONDITION,
)

for suspect_hcc in from_previous_conditions:
    print(suspect_hcc.hcc_description, suspect_hcc.previous_condition)
```

## Attributes

### SuspectHCC

| Field Name         | Type                                    | Description |
| ------------------ | --------------------------------------- | ----------- |
| dbid               | Integer                                 | |
| created            | DateTime                                | |
| modified           | DateTime                                | |
| patient            | [Patient](/sdk/data-patient/#patient)   | |
| status             | [SuspectHCCStatus](#suspecthccstatus)   | Whether the suspected HCC is still open on the patient. |
| hcc_code           | String                                  | The HCC code, such as `27`. Empty when `kind` is `previous_condition`. |
| hcc_description    | String                                  | The HCC's description, such as `End-stage liver disease`. When `kind` is `previous_condition`, the description of the earlier diagnosis. |
| kind               | [SuspectHCCKind](#suspecthcckind)       | Why the HCC is suspected. |
| reasons            | String[]                                | The clinical data that implies the HCC, each entry prefixed with its type, such as `Condition: End-stage liver disease`. Empty when `kind` is `previous_condition`. |
| previous_condition | String                                  | The earlier diagnosis the HCC is suspected from, when `kind` is `previous_condition`. Empty otherwise. |

## Enumeration types

### SuspectHCCStatus

| Value      | Label    |
| ---------- | -------- |
| `active`   | Active   |
| `inactive` | Inactive |

### SuspectHCCKind

| Value                      | Label                    |
| -------------------------- | ------------------------ |
| `implied_by_clinical_data` | Implied by Clinical Data |
| `previous_condition`       | Previous Condition       |
| `unknown`                  | Unknown                  |

<br/>
<br/>
<br/>
