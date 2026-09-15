---
title: "Reference"
slug: "data-reference"
excerpt: "Canvas SDK Reference"
hidden: false
---

## Introduction

The `Reference` model is the anchor for the Reference command — a saved reference embedded on a note, optionally backed by a [DiagnosticView](/sdk/data-diagnostic-view/) (a saved set of lab tests and questionnaire codes whose timeseries is rendered inline).

## Basic usage

To get a reference by identifier, use the `get` method on the `Reference` model manager:

```python?partial=true
from canvas_sdk.v1.data import Reference

reference = Reference.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

From a patient or a note, use the `references` attribute:

```python
from canvas_sdk.v1.data import Note, Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
references = patient.references.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
references = note.references.all()
```

### Committed references

The `committed` method returns records that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import Reference

committed = Reference.objects.committed()
```

## Attributes

### Reference

| Field Name       | Type                                             | Description                                                          |
| ---------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| id               | UUID                                             | The universally unique identifier for this record.                   |
| dbid             | Integer                                          | The database identifier for this record.                             |
| created          | DateTime                                         | When the record was created.                                        |
| modified         | DateTime                                         | When the record was last modified.                                  |
| originator       | [CanvasUser](/sdk/data-canvasuser)               | The user who originated the command.                                 |
| committer        | [CanvasUser](/sdk/data-canvasuser)               | The user who committed the command, if it has been committed.        |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)               | The user who entered the record in error, if it has been.            |
| patient          | [Patient](/sdk/data-patient/#patient)            | The patient the reference was recorded for.                          |
| note             | [Note](/sdk/data-note)                           | The note it was recorded on.                                         |
| diagnostic_view  | [DiagnosticView](/sdk/data-diagnostic-view/)     | The saved diagnostic view this reference renders, if any.            |
| name             | String                                           | The reference's display name.                                        |
| content          | JSON                                             | The reference's stored content.                                      |

<br/>
<br/>
<br/>
