---
title: "DetectedIssue"
slug: "data-detected-issue"
excerpt: "Canvas SDK DetectedIssue"
hidden: false
---

## Introduction

The `DetectedIssue` model represents an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient.

## Basic usage

To get a detected issue by identifier, use the `get` method on the `DetectedIssue` model manager:

```python
from canvas_sdk.v1.data.detected_issue import DetectedIssue

detected_issue = DetectedIssue.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the detected issues for a patient can be accessed with the `detected_issues` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
detected_issues = patient.detected_issues.all()
```

## Evidence

The codings for the evidence of a detected issue can be accessed with the `evidence` attribute on a `DetectedIssue` object:

```python
from canvas_sdk.v1.data.detected_issue import DetectedIssue
from logger import log

detected_issue = DetectedIssue.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in detected_issue.evidence.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Mitigations

The actions recorded against a detected issue, such as accepting or refuting it, are available through the `mitigations` attribute on a `DetectedIssue` object. Each mitigation records the action, when it was taken, and the staff member who took it:

```python
from canvas_sdk.v1.data.detected_issue import DetectedIssue
from logger import log

detected_issue = DetectedIssue.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for mitigation in detected_issue.mitigations.select_related("author").order_by("date"):
    log.info(f"{mitigation.date}: {mitigation.action} by {mitigation.author}")
```

To find the mitigations a staff member recorded, use the `detected_issue_mitigations` attribute on a [Staff](/sdk/data-staff/#staff) object.

## Filtering

Detected issues can be filtered by any attribute that exists on the model.

Filtering for detected issues is done with the `filter` method on the `DetectedIssue` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.detected_issue import DetectedIssue

detected_issues = DetectedIssue.objects.filter(status="active")
```

### Committed detected issues

The `committed` method returns detected issues that have been committed and not entered in error:

```python
from canvas_sdk.v1.data.detected_issue import DetectedIssue

committed_detected_issues = DetectedIssue.objects.committed()
```

## Attributes

### DetectedIssue

| Field Name              | Type                                              |
| ----------------------- | ------------------------------------------------- |
| id                      | UUID                                              |
| dbid                    | Integer                                           |
| created                 | DateTime                                          |
| modified                | DateTime                                          |
| identified              | DateTime                                          |
| originator              | [CanvasUser](/sdk/data-canvasuser)                |
| committer               | [CanvasUser](/sdk/data-canvasuser)                |
| entered_in_error        | [CanvasUser](/sdk/data-canvasuser)                |
| patient                 | [Patient](/sdk/data-patient/#patient)             |
| code                    | String                                            |
| status                  | [DetectedIssueStatus](#detectedissuestatus)       |
| severity                | [DetectedIssueSeverity](#detectedissueseverity)   |
| reference               | String                                            |
| issue_identifier        | String                                            |
| issue_identifier_system | String                                            |
| detail                  | String                                            |
| evidence                | [DetectedIssueEvidence](#detectedissueevidence)[] |
| mitigations             | [DetectedIssueMitigation](#detectedissuemitigation)[] |
| assessed_coding_gap_events  | [AssessCodingGapEvent](/sdk/data-coding-gap-event/#assesscodinggapevent)[]     |
| created_coding_gap_events   | [CreateCodingGapEvent](/sdk/data-coding-gap-event/#createcodinggapevent)[]     |
| deferred_coding_gap_events  | [DeferCodingGapEvent](/sdk/data-coding-gap-event/#defercodinggapevent)[]       |
| validated_coding_gap_events | [ValidateCodingGapEvent](/sdk/data-coding-gap-event/#validatecodinggapevent)[] |

### DetectedIssueEvidence

| Field Name     | Type                                                     |
| -------------- | -------------------------------------------------------- |
| id             | UUID                                                     |
| dbid           | Integer                                                  |
| created        | DateTime                                                 |
| modified       | DateTime                                                 |
| system         | String                                                   |
| version        | String                                                   |
| code           | String                                                   |
| display        | String                                                   |
| user_selected  | Boolean                                                  |
| detected_issue | [DetectedIssue](/sdk/data-detected-issue/#detectedissue) |

### DetectedIssueMitigation

| Field Name     | Type                                                         |
| -------------- | ------------------------------------------------------------ |
| id             | UUID                                                         |
| dbid           | Integer                                                      |
| action         | [DetectedIssueMitigationAction](#detectedissuemitigationaction) |
| date           | DateTime                                                     |
| author         | [Staff](/sdk/data-staff/#staff)                              |
| detected_issue | [DetectedIssue](/sdk/data-detected-issue/#detectedissue)     |

### DetectedIssueStatus

Available on the model as `DetectedIssue.Status`, so a comparison reads
`detected_issue.status == DetectedIssue.Status.FINAL`.

| Enum             | Value            | Label            |
| ---------------- | ---------------- | ---------------- |
| REGISTERED       | registered       | Registered       |
| PRELIMINARY      | preliminary      | Preliminary      |
| CANCELLED        | cancelled        | Cancelled        |
| AMENDED          | amended          | Amended          |
| FINAL            | final            | Final            |
| CORRECTED        | corrected        | Corrected        |
| ENTERED_IN_ERROR | entered-in-error | Entered in Error |

### DetectedIssueSeverity

Available on the model as `DetectedIssue.Severity`. A detected issue that carries no
severity holds an empty string rather than `None`.

| Enum     | Value    | Label    |
| -------- | -------- | -------- |
| HIGH     | high     | High     |
| MODERATE | moderate | Moderate |
| LOW      | low      | Low      |

### DetectedIssueMitigationAction

Available on the model as `DetectedIssueMitigation.Action`, so a comparison reads
`mitigation.action == DetectedIssueMitigation.Action.REFUTED`.

| Enum      | Value     | Label     |
| --------- | --------- | --------- |
| ACCEPTED  | accepted  | Accepted  |
| CORRECTED | corrected | Corrected |
| REFUTED   | refuted   | Refuted   |
| DEFERRED  | deferred  | Deferred  |
| VALID     | valid     | Valid     |
| INVALID   | invalid   | Invalid   |

<br/>
<br/>
<br/>
