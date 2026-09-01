---
title: "FollowUp"
slug: "data-follow-up"
excerpt: "Canvas SDK FollowUp"
hidden: false
---

## Introduction

The `FollowUp` model is the anchor for the [Follow Up](/sdk/commands/#followup) command — a requested follow-up (recall) recorded on a Note for a Patient.

## Basic usage

To get a follow up by identifier, use the `get` method on the `FollowUp` model manager:

```python?partial=true
from canvas_sdk.v1.data.follow_up import FollowUp

follow_up = FollowUp.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient or note object, the follow ups can be accessed with the `follow_ups` attribute:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.note import Note

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
follow_ups = patient.follow_ups.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
follow_ups = note.follow_ups.all()
```

## Committed follow ups

The `committed` method returns follow ups that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data.follow_up import FollowUp

committed_follow_ups = FollowUp.objects.committed()
```

## Attributes

### FollowUp

| Field Name                                | Type                                  |
| ----------------------------------------- | ------------------------------------- |
| id                                        | UUID                                  |
| dbid                                      | Integer                               |
| created                                   | DateTime                              |
| modified                                  | DateTime                              |
| originator                                | [CanvasUser](/sdk/data-canvasuser)    |
| committer                                 | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error                          | [CanvasUser](/sdk/data-canvasuser)    |
| patient                                   | [Patient](/sdk/data-patient/#patient) |
| note                                      | [Note](/sdk/data-note)                |
| appointment_note                          | [Note](/sdk/data-note)                |
| requested_appointment_date                | Date                                  |
| requested_appointment_date_original_input | String                                |
| reason_for_visit                          | String                                |
| reason_for_visit_coding                   | String                                |
| note_to_patient                           | String                                |
| internal_comment                          | String                                |
| requested_appointment_type                | [EncounterMedium](#encountermedium)   |
| requested_note_type                       | [NoteType](/sdk/data-note)            |

## Enumeration types

### EncounterMedium

| Name    | Value   |
| ------- | ------- |
| VOICE   | voice   |
| VIDEO   | video   |
| OFFICE  | office  |
| HOME    | home    |
| OFFSITE | offsite |
| LAB     | lab     |

<br/>
<br/>
<br/>
