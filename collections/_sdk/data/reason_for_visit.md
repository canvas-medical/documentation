---
title: "ReasonForVisit"
slug: "data-reason-for-visit"
excerpt: "Canvas SDK ReasonForVisit and its codings"
hidden: false
---

## Introduction

The `ReasonForVisit` model is the anchor for the `reason_for_visit` command — a reason for visit recorded on a Note for a Patient. The `ReasonForVisitSettingCoding` model is separate: it represents the practice-settings catalog of selectable reason-for-visit codings (and their durations) used to populate the coding field when documenting a reason for visit.

## ReasonForVisit

To get a reason for visit by identifier, use the `get` method on the `ReasonForVisit` model manager:

```python?partial=true
from canvas_sdk.v1.data import ReasonForVisit

reason_for_visit = ReasonForVisit.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient or note object, the reasons for visit can be accessed with the `reasons_for_visit` attribute:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.note import Note

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
reasons = patient.reasons_for_visit.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
reasons = note.reasons_for_visit.all()
```

The reason-for-visit text is exposed through the read-only `narrative` property:

```python?partial=true
from canvas_sdk.v1.data import ReasonForVisit

reason_for_visit = ReasonForVisit.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
text = reason_for_visit.narrative
```

The `committed` method returns records that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import ReasonForVisit

committed_reasons = ReasonForVisit.objects.committed()
```

## ReasonForVisitSettingCoding

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

## Attributes

### ReasonForVisit

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
| narrative        | String (read-only property)           |

### ReasonForVisitSettingCoding

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
