---
title: "Change Medication"
slug: "data-change-medication"
excerpt: "Canvas SDK Change Medication"
hidden: false
---

## Introduction

The `ChangeMedication` model represents a record of a change to a medication's sig or dose instructions on a patient's medication list, created when a `ChangeMedicationCommand` is committed.

## Basic usage

To get a change medication by identifier, use the `get` method on the `ChangeMedication` model manager:

```python
from canvas_sdk.v1.data import ChangeMedication

change_medication = ChangeMedication.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
```

If you have a patient object, the change medications for a patient can be accessed with the `change_medications` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
change_medications = patient.change_medications.all()
```

You can also access the referenced medication with the `medication` attribute:

```python
from canvas_sdk.v1.data import ChangeMedication

change_medication = ChangeMedication.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
medication = change_medication.medication
```

Or for a given medication, you can access all change medications:

```python
from canvas_sdk.v1.data import Medication

medication = Medication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
change_medications = medication.change_medications.all()
```

## Committed records

The `committed` method returns change medications that have been committed and not entered in error:

```python
from canvas_sdk.v1.data import ChangeMedication

committed_change_medications = ChangeMedication.objects.committed()
```

## Attributes

### ChangeMedication

| Field Name         | Type                                  |
| ------------------ | ------------------------------------- |
| id                 | UUID                                  |
| dbid               | Integer                               |
| patient            | [Patient](/sdk/data-patient/#patient) |
| note               | [Note](/sdk/data-note)                |
| medication         | [Medication](/sdk/data-medication)    |
| entered_in_error   | [CanvasUser](/sdk/data-canvasuser)    |
| committer          | [CanvasUser](/sdk/data-canvasuser)    |
| originator         | [CanvasUser](/sdk/data-canvasuser)    |
| created            | DateTime                              |
| modified           | DateTime                              |
| sig_original_input | String                                |

<br/>
<br/>
<br/>
