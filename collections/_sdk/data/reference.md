---
title: "Reference"
slug: "data-reference"
excerpt: "Canvas SDK Reference data model"
hidden: false
---

## Introduction

The `Reference` model is the read-only record of a diagnostic view embedded in a note, created when the [Reference](/sdk/commands/#reference) command is originated — for example, when a clinician adds a diagnostic view to a note through diagnostic theater, or a plugin originates a `ReferenceCommand`. It captures a snapshot of the referenced diagnostic view's rendered table. The command creates the reference record when it is originated, and commits it when the command is committed.

## Basic usage

To get a reference by identifier, use the `get` method on the `Reference` model manager:

```python?partial=true
from canvas_sdk.v1.data import Reference

reference = Reference.objects.get(id="a1b2c3d4-e5f6-7890-abcd-ef1234567890")
```

If you have a patient object, the references for a patient can be accessed with the `references` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
references = patient.references.all()
```

If you have a note object, the references on that note can be accessed with the `references` attribute on a `Note` object:

```python
from canvas_sdk.v1.data import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
references = note.references.all()
```

## Committed references

A reference stays staged until its command is committed, so it can exist in an uncommitted state while the command is staged. The basic-usage queries above return staged and committed references together. Use the `committed` method to get only references that have been committed and not entered in error:

```python
from canvas_sdk.v1.data import Reference

committed = Reference.objects.committed()
```

## Attributes

### Reference

| Field Name       | Type                                                     | Description                                                                            |
| ---------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| id               | UUID                                                     | The universally unique identifier for this record.                                     |
| dbid             | Integer                                                  | The database identifier for this record.                                               |
| created          | DateTime                                                 | When the record was created.                                                           |
| modified         | DateTime                                                 | When the record was last modified.                                                     |
| originator       | [CanvasUser](/sdk/data-canvasuser)                       | The user who originated the command.                                                   |
| committer        | [CanvasUser](/sdk/data-canvasuser)                       | The user who committed the command, if it has been committed.                          |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)                       | The user who entered the record in error, if it has been.                              |
| patient          | [Patient](/sdk/data-patient/#patient)                    | The patient the reference was recorded for.                                            |
| note             | [Note](/sdk/data-note/#note)                             | The note it was recorded on.                                                           |
| diagnostic_view  | [DiagnosticView](/sdk/data-diagnostic-view/#diagnosticview) | The diagnostic view that was referenced. May be null if no view was set when the command was originated, or if the supplied view id did not match a diagnostic view on the instance and was discarded. |
| name             | String (up to 100 characters)                            | The label shown on the note, captured at origination. May be an empty string. Derived from the diagnostic view when the command is originated and not recalculated if the command is later pointed at a different diagnostic view with `edit()`. |
| content          | JSON                                                     | A snapshot of the referenced diagnostic view's rendered table, captured when the reference was created and not updated if the command is later pointed at a different diagnostic view with `edit()`. |
