---
title: "Coding Gap Events"
slug: "data-coding-gap-event"
excerpt: "Canvas SDK Coding Gap Events"
hidden: false
---

## Introduction

The `CreateCodingGapEvent`, `ValidateCodingGapEvent`, `AssessCodingGapEvent`, and `DeferCodingGapEvent` models are read-only records of the actions taken on a coding gap — create, validate, assess, and defer. Each model is the anchor for the corresponding coding gap command.

A coding gap itself is represented by a [DetectedIssue](/sdk/data-detected-issue/) together with its `DetectedIssueEvidence`. These four models record only the actions taken on the coding gap. A coding gap event's `detected_issue` foreign key is nullable, so expect events without an associated `DetectedIssue`.

These are audit records of create, validate, assess, and defer actions — useful for reporting, deduplication logic, and risk adjustment and HCC (Hierarchical Condition Category) coding gap analytics. A plugin does not perform these actions through these models. Each is performed instead through its own command — the Create Coding Gap, Validate Coding Gap, Assess Coding Gap, and Defer Coding Gap commands respectively.

## Basic usage

To get a coding gap event by identifier, use the `get` method on the model manager. Each of the four models is imported from `canvas_sdk.v1.data`:

```python?partial=true
from canvas_sdk.v1.data import CreateCodingGapEvent

create_event = CreateCodingGapEvent.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
```

All four models expose the same manager, so `get`, `filter`, and `committed` are available on each. The models are read-only — there is no create or save.

## Accessing events from a patient or note

The coding gap events for a patient or note are reachable through reverse accessors. For each model, the accessor name is the same on `Patient` and on `Note`:

| Model | Patient & Note reverse accessor | DetectedIssue reverse accessor |
| --- | --- | --- |
| CreateCodingGapEvent | `created_detected_issues` | `created_coding_gap_events` |
| ValidateCodingGapEvent | `assessed_detected_issues` | `validated_coding_gap_events` |
| AssessCodingGapEvent | `assessed_coding_gaps` | `assessed_coding_gap_events` |
| DeferCodingGapEvent | `deferred_detected_issues` | `deferred_coding_gap_events` |

For a patient, use the accessor on the `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
create_events = patient.created_detected_issues.all()
```

The same records are reachable from the note they were recorded on, with the matching accessor on the `Note` object:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
defer_events = note.deferred_detected_issues.all()
```

## Accessing events from a detected issue

For a given coding gap, each model's events are reachable from the [DetectedIssue](/sdk/data-detected-issue/) through its own reverse accessor:

| Model | DetectedIssue reverse accessor |
| --- | --- |
| CreateCodingGapEvent | `created_coding_gap_events` |
| ValidateCodingGapEvent | `validated_coding_gap_events` |
| AssessCodingGapEvent | `assessed_coding_gap_events` |
| DeferCodingGapEvent | `deferred_coding_gap_events` |

```python
from canvas_sdk.v1.data.detected_issue import DetectedIssue

detected_issue = DetectedIssue.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
create_events = detected_issue.created_coding_gap_events.all()
```

## Assessed coding gaps on a condition

`AssessCodingGapEvent` records the conditions a coding gap was assessed against through its `conditions` many-to-many relationship:

```python?partial=true
from canvas_sdk.v1.data import AssessCodingGapEvent

assess_event = AssessCodingGapEvent.objects.get(id="0b2f2f8c-3c2c-4d9e-9a1a-2b6a4c7d8e90")
conditions = assess_event.conditions.all()
```

For a given condition, the assess events it was included in are reachable with the `assessed_coding_gaps` accessor on a `Condition` object:

```python
from canvas_sdk.v1.data import Condition

condition = Condition.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
assess_events = condition.assessed_coding_gaps.all()
```

## Committed records

The `committed` method returns records that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import CreateCodingGapEvent

committed_create_events = CreateCodingGapEvent.objects.committed()
```

The `committed` method is available on all four managers.

## Attributes

### CreateCodingGapEvent

| Field Name       | Type                                                     |
| ---------------- | -------------------------------------------------------- |
| id               | UUID                                                     |
| dbid             | Integer                                                  |
| created          | DateTime                                                 |
| modified         | DateTime                                                 |
| originator       | [CanvasUser](/sdk/data-canvasuser)                       |
| committer        | [CanvasUser](/sdk/data-canvasuser)                       |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)                       |
| patient          | [Patient](/sdk/data-patient/#patient)                    |
| note             | [Note](/sdk/data-note)                                   |
| detected_issue   | [DetectedIssue](/sdk/data-detected-issue/#detectedissue) |

### ValidateCodingGapEvent

| Field Name       | Type                                                     |
| ---------------- | -------------------------------------------------------- |
| id               | UUID                                                     |
| dbid             | Integer                                                  |
| created          | DateTime                                                 |
| modified         | DateTime                                                 |
| originator       | [CanvasUser](/sdk/data-canvasuser)                       |
| committer        | [CanvasUser](/sdk/data-canvasuser)                       |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)                       |
| patient          | [Patient](/sdk/data-patient/#patient)                    |
| note             | [Note](/sdk/data-note)                                   |
| detected_issue   | [DetectedIssue](/sdk/data-detected-issue/#detectedissue) |

### AssessCodingGapEvent

| Field Name       | Type                                                     |
| ---------------- | -------------------------------------------------------- |
| id               | UUID                                                     |
| dbid             | Integer                                                  |
| created          | DateTime                                                 |
| modified         | DateTime                                                 |
| originator       | [CanvasUser](/sdk/data-canvasuser)                       |
| committer        | [CanvasUser](/sdk/data-canvasuser)                       |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)                       |
| patient          | [Patient](/sdk/data-patient/#patient)                    |
| note             | [Note](/sdk/data-note)                                   |
| detected_issue   | [DetectedIssue](/sdk/data-detected-issue/#detectedissue) |
| conditions       | [Condition](/sdk/data-condition)[]                       |

### DeferCodingGapEvent

| Field Name       | Type                                                     |
| ---------------- | -------------------------------------------------------- |
| id               | UUID                                                     |
| dbid             | Integer                                                  |
| created          | DateTime                                                 |
| modified         | DateTime                                                 |
| originator       | [CanvasUser](/sdk/data-canvasuser)                       |
| committer        | [CanvasUser](/sdk/data-canvasuser)                       |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)                       |
| patient          | [Patient](/sdk/data-patient/#patient)                    |
| note             | [Note](/sdk/data-note)                                   |
| detected_issue   | [DetectedIssue](/sdk/data-detected-issue/#detectedissue) |

<br/>
<br/>
<br/>
