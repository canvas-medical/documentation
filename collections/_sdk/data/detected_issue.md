---
title: "Detected Issue"
slug: "data-detected-issue"
excerpt: "Canvas SDK Detected Issue"
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

## Filtering

Detected issues can be filtered by any attribute that exists on the model.

Filtering for detected issues is done with the `filter` method on the `DetectedIssue` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.detected_issues import DetectedIssue

detected_issues = DetectedIssue.objects.filter(status="active")
```

## Attributes

### DetectedIssue

| Field Name              | Type                                  |
|-------------------------|---------------------------------------|
| id                      | UUID                                  |
| dbid                    | Integer                               |
| created                 | DateTime                              |
| modified                | DateTime                              |
| identified              | DateTime                              |
| deleted                 | Boolean                               |
| originator              | CanvasUser                            |
| committer               | CanvasUser                            |
| entered_in_error        | CanvasUser                            |
| patient                 | [Patient](/sdk/data-patient/#patient) |
| code                    | String                                |
| status                  | String                                |
| severity                | String                                |
| reference               | String                                |
| issue_identifier        | String                                |
| issue_identifier_system | String                                |
| detail                  | String                                |

### DetectedIssueEvidence

| Field Name     | Type                                                    |
|----------------|---------------------------------------------------------|
| dbid           | Integer                                                 |
| system         | String                                                  |
| version        | String                                                  |
| code           | String                                                  |
| display        | String                                                  |
| user_selected  | Boolean                                                 |
| detected_issue | [DetectedIssue](sdk/data-detected-issue/#detectedissue) |

<br/>
<br/>
<br/>
