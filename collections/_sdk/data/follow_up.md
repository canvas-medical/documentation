---
title: "FollowUp"
slug: "data-follow-up"
excerpt: "Canvas SDK FollowUp"
hidden: false
---

## Introduction

The `FollowUp` model represents a follow-up request recorded on a note. It is the read-side counterpart to the write-side [`follow_up` command](/sdk/commands/#followup) that creates these records.

## Basic usage

To get a follow-up by identifier, use the `get` method on the `FollowUp` model manager:

```python
from canvas_sdk.v1.data.follow_up import FollowUp

follow_up = FollowUp.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the follow-ups for a patient can be accessed with the `follow_ups` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
follow_ups = patient.follow_ups.all()
```

If you have a note object, the follow-ups for that note can be accessed with the `follow_ups` attribute on a `Note` object:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
follow_ups = note.follow_ups.all()
```

## Filtering

Follow-ups can be filtered by any attribute that exists on the model.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.follow_up import FollowUp

follow_ups = FollowUp.objects.filter(reason_for_visit="Annual physical")
```

### By patient

```python
from canvas_sdk.v1.data.follow_up import FollowUp
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
follow_ups = FollowUp.objects.filter(patient=patient)
```

### Committed follow-ups

The `committed` method returns follow-ups that have been committed and not entered in error:

```python
from canvas_sdk.v1.data.follow_up import FollowUp

committed_follow_ups = FollowUp.objects.committed()
```

## Attributes

### FollowUp

| Field Name | Type |
|------------|------|
| id | UUID |
| dbid | Integer |
| created | DateTime |
| modified | DateTime |
| patient | [Patient](/sdk/data-patient/#patient) |
| note | [Note](/sdk/data-note/) |
| appointment_note | [Note](/sdk/data-note/) (OneToOne, may be null) |
| requested_appointment_date | Date (may be null) |
| requested_appointment_date_original_input | String |
| reason_for_visit | String |
| reason_for_visit_coding | String |
| note_to_patient | String |
| internal_comment | String |
| requested_appointment_type | [EncounterMedium](/sdk/data-encounter/#encountermedium) (defaults to `office`, may be null) |
| requested_note_type | [NoteType](/sdk/data-note/#notetype) |
| originator | [CanvasUser](/sdk/data-canvasuser) |
| committer | [CanvasUser](/sdk/data-canvasuser) |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser) |
