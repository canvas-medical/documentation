---
title: "ReasonForVisit"
slug: "data-reason-for-visit"
excerpt: "Canvas SDK ReasonForVisit and its codings"
hidden: false
---

## Introduction

This page covers three models:

- `ReasonForVisit` — a Reason for Visit recorded on a note, and the anchor for the
  [Reason for Visit](/sdk/commands/#reasonforvisit) command.
- `ReasonForVisitCoding` — the codings on a recorded Reason for Visit.
- `ReasonForVisitSettingCoding` — the configured codings an instance offers, used to populate the
  coding field when a Reason for Visit is recorded.

## ReasonForVisit

A `ReasonForVisit` is always associated with a note and a patient. To get one by identifier:

```python?partial=true
from canvas_sdk.v1.data import ReasonForVisit

rfv = ReasonForVisit.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

From a patient or a note, use the `reasons_for_visit` attribute:

```python
from canvas_sdk.v1.data import Note, Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
reasons = patient.reasons_for_visit.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
reasons = note.reasons_for_visit.all()
```

### Reading the narrative

The text is exposed through the `narrative` property, which returns the free-text value when there is
one and otherwise renders the structured `narrative_json`:

```python?partial=true
from canvas_sdk.v1.data import ReasonForVisit

rfv = ReasonForVisit.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
text = rfv.narrative
```

### Committed reasons for visit

The `committed` method returns records that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import ReasonForVisit

committed = ReasonForVisit.objects.committed()
```

### Codings

Each `ReasonForVisit` exposes its codings through `codings`:

```python?partial=true
from canvas_sdk.v1.data import ReasonForVisit

rfv = ReasonForVisit.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
codings = rfv.codings.all()
```

### Attributes

#### ReasonForVisit

| Field Name       | Type                                  | Description                                                            |
| ---------------- | ------------------------------------- | ---------------------------------------------------------------------- |
| id               | UUID                                  | The universally unique identifier for this record.                     |
| dbid             | Integer                               | The database identifier for this record.                               |
| created          | DateTime                              | When the record was created.                                           |
| modified         | DateTime                              | When the record was last modified.                                     |
| originator       | [CanvasUser](/sdk/data-canvasuser)    | The user who originated the command.                                   |
| committer        | [CanvasUser](/sdk/data-canvasuser)    | The user who committed the command, if it has been committed.          |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)    | The user who entered the record in error, if it has been.              |
| patient          | [Patient](/sdk/data-patient/#patient) | The patient the reason for visit was recorded for.                     |
| note             | [Note](/sdk/data-note)                | The note it was recorded on.                                           |
| narrative        | String                                | The reason for visit text.                                             |
| codings          | _list_                                | The `ReasonForVisitCoding` records on this reason for visit.           |

#### ReasonForVisitCoding

| Field Name       | Type                                             | Description                                              |
| ---------------- | ------------------------------------------------ | -------------------------------------------------------- |
| dbid             | Integer                                          | The database identifier for this coding record.          |
| code             | String                                           | The code representing the concept.                       |
| display          | String                                           | The human-readable display name for the concept.         |
| system           | String                                           | The coding system.                                       |
| version          | String                                           | The version of the coding system.                        |
| user_selected    | Boolean                                          | Whether a user chose this coding directly.               |
| reason_for_visit | [ReasonForVisit](#reasonforvisit)                | The reason for visit this coding belongs to.             |

## ReasonForVisitSettingCoding

The `ReasonForVisitSettingCoding` model represents the coding information used to populate the coding field within a
Reason For Visit in Canvas.

### Basic Usage

To retrieve a specific coding record by its identifier, use the model manager's `get` method:

```python
from canvas_sdk.v1.data import ReasonForVisitSettingCoding

rfv_coding = ReasonForVisitSettingCoding.objects.get(id="e2b1e1e3-3f52-4a0a-bb3a-123456789abc")
```

You can also filter records by attributes. For example, to get all codings from a specific coding system:

```python
from canvas_sdk.v1.data import ReasonForVisitSettingCoding

codings = ReasonForVisitSettingCoding.objects.filter(system="http://snomed.info/sct")
```

### Attributes

#### ReasonForVisitSettingCoding

| Field Name | Type              | Description                                                                       |
| ---------- | ----------------- | --------------------------------------------------------------------------------- |
| id         | UUID              | The universally unique identifier for this coding record.                         |
| dbid       | Integer           | The database identifier for this coding record.                                   |
| code       | String            | The code representing the concept.                                                |
| display    | String            | The human-readable display name for the concept.                                  |
| system     | String            | The coding system (e.g., `http://snomed.info/sct`).                               |
| version    | String            | The version of the coding system.                                                 |
| duration   | Array of Duration | An array of durations (as Python `timedelta` objects) associated with the coding. |
| user_selected | Boolean        | The active/inactive flag for this reason-for-visit coding: `True` = active, `False` = inactive. |

<br/>
<br/>
<br/>
