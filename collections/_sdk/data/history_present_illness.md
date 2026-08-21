---
title: "HistoryOfPresentIllness"
slug: "data-history-present-illness"
excerpt: "Canvas SDK HistoryOfPresentIllness"
hidden: false
---

## Introduction

The `HistoryOfPresentIllness` model represents a History of Present Illness (HPI) recorded on a Note, and is always associated with a Note and a Patient. It is the data model behind the `hpi` command.

## Basic usage

To get an HPI by identifier, use the `get` method on the `HistoryOfPresentIllness` model manager:

```python?partial=true
from canvas_sdk.v1.data.history_present_illness import HistoryOfPresentIllness

hpi = HistoryOfPresentIllness.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, or note object, the histories of present illness for a patient or note can be accessed with the `histories_of_present_illness` attribute on a `Patient` or `Note` object:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.note import Note

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
histories = patient.histories_of_present_illness.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
histories = note.histories_of_present_illness.all()
```

## Reading the narrative

The HPI text is exposed through the read-only `narrative` property, so plugin authors only need to read one field:

```python?partial=true
from canvas_sdk.v1.data.history_present_illness import HistoryOfPresentIllness

hpi = HistoryOfPresentIllness.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
text = hpi.narrative
```

## Filtering

Histories of present illness can be filtered by any attribute that exists on the model.

### Committed histories of present illness

The `committed` method returns records that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data.history_present_illness import HistoryOfPresentIllness

committed_histories = HistoryOfPresentIllness.objects.committed()
```

## Attributes

### HistoryOfPresentIllness

| Field Name       | Type                                  |
| ---------------- | ------------------------------------- |
| id               | UUID                                  |
| dbid             | Integer                               |
| created          | DateTime                              |
| modified         | DateTime                              |
| originator       | [CanvasUser](/sdk/data-canvasuser)    |
| committer        | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)    |
| patient          | [Patient](/sdk/data-patient/#patient) |
| note             | [Note](/sdk/data-note)                |
| narrative        | String                                |

<br/>
<br/>
<br/>
