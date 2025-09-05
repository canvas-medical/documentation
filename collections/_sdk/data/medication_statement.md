---
title: "Medication Statement"
slug: "data-medication-statement"
excerpt: "Canvas SDK Medication Statement"
hidden: false
---

## Introduction

The `MedicationStatement` model represents a record of a medication statement by a patient from the past.

## Basic usage

To get a medication statement by identifier, use the `get` method on the `MedicationStatement` model manager:

```python
from canvas_sdk.v1.data import MedicationStatement

medication_statement = MedicationStatement.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
```

If you have a patient object, the medication statements for a patient can be accessed with the `medication_statements` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
medication_statements = patient.medication_statements.all()
```

You can also access the referenced medication with the `medication` attribute:

```python
from canvas_sdk.v1.data import MedicationStatement

medication_statement = MedicationStatement.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
medication = medication_statement.medication
```

Or for a given medication, you can access all medication statements:

```python
from canvas_sdk.v1.data import Medication

medication = Medication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
medication_statements = medication.medication_statements.all()
```

## Attributes

### MedicationStatement

| Field Name                | Type                                  |
| ------------------------- | ------------------------------------- |
| id                        | UUID                                  |
| dbid                      | Integer                               |
| patient                   | [Patient](/sdk/data-patient/#patient) |
| note                      | [Note](/sdk/data-note)                |
| medication                | [Medication](/sdk/data-medication)    |
| indications               | [Assessment](/sdk/data-assessment)[]  |
| entered_in_error          | [CanvasUser](/sdk/data-canvasuser)    |
| committer                 | [CanvasUser](/sdk/data-canvasuser)    |
| originator                | [CanvasUser](/sdk/data-canvasuser)    |
| created                   | DateTime                              |
| modified                  | DateTime                              |
| start_date_original_input | String                                |
| start_date                | Date                                  |
| end_date_original_input   | String                                |
| end_date                  | Date                                  |
| dose_quantity             | Number                                |
| dose_form                 | String                                |
| dose_route                | String                                |
| dose_frequency            | Number                                |
| dose_frequency_interval   | String                                |
| sig_original_input        | String                                |

<br/>
<br/>
<br/>
