---
title: "Assessment"
slug: "data-assessment"
excerpt: "Canvas SDK Assessment"
hidden: false
---

## Introduction

The `Assessment` model represents a clinical assessment or evaluation of a patient's medical `Condition`.

## Basic usage

To get an assessment by identifier, use the `get` method on the `Assessment` model manager:

```python
from canvas_sdk.v1.data.assessment import Assessment

assessment = Assessment.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the assessments for a patient can be accessed with the `assessments` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
assessments = patient.assessments.all()
```

## Filtering

Assessments can be filtered by any attribute that exists on the model.

Filtering for assessments is done with the `filter` method on the `Assessment` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.assessment import Assessment, AssessmentStatus

assessments = Assessment.objects.filter(patient__id="1eed3ea2a8d546a1b681a2a45de1d790", status=AssessmentStatus.STATUS_IMPROVING)
```

### Committed assessments

The `committed` method returns assessments that have been committed and not entered in error:

```python
from canvas_sdk.v1.data.assessment import Assessment

committed_assessments = Assessment.objects.committed()
```

## Attributes

### Assessment

| Field Name          | Type                                                    |
| ------------------- | ------------------------------------------------------- | --- |
| id                  | UUID                                                    |
| dbid                | Integer                                                 |
| created             | DateTime                                                |
| modified            | DateTime                                                |
| originator          | [CanvasUser](/sdk/data-canvasuser)                      |     |
| entered_in_error    | [CanvasUser](/sdk/data-canvasuser)                      |
| committer           | [CanvasUser](/sdk/data-canvasuser)                      |
| patient             | [Patient](/sdk/data-patient/#patient)                   |
| note                | [Note](/sdk/data-note/#note)                            |
| condition           | [Condition](/sdk/data-condition/#condition)             |
| interview           | [Interview](/sdk/data-questionnaire/#interview)         |
| status              | [AssessmentStatus](#assessment-status)                  |
| narrative           | String                                                  |
| background          | String                                                  |
| care_team           | String                                                  |
| treatments_stated   | [MedicationStatement](/sdk/data-medication-statement)[] |
| billinglineitem_set | [BillingLineItem](/sdk/data-billing-line-item)[]        |
| referrals           | [Referral](/sdk/data-referral)[]                        |

### Commands linked to an assessment

A Plan- or Procedures-section command written in the same note can be linked to an assessment, which each of these accessors reads back from the assessment's side. The command holds the other half of the link on its own `assessment` field.

| Field Name          | Type                                                                          |
| ------------------- | ----------------------------------------------------------------------------- |
| follow_ups          | [FollowUp](/sdk/data-follow-up/#followup)[]                                   |
| goals               | [Goal](/sdk/data-goal/#goal)[]                                                |
| immunizations       | [Immunization](/sdk/data-immunization/#immunization)[]                        |
| instructions        | [Instruction](/sdk/data-instruction/#instruction)[]                           |
| note_tasks          | [NoteTask](/sdk/data-task/#notetask)[]                                        |
| plans               | [Plan](/sdk/data-plan/#plan)[]                                                |
| procedures          | [Procedure](/sdk/data-procedure/#procedure)[]                                 |
| stopped_medications | [StopMedicationEvent](/sdk/data-stop-medication-event/#stopmedicationevent)[] |
| updategoals         | [UpdateGoal](/sdk/data-goal/#updategoal)[]                                    |

## Enumeration types

### Assessment Status

| Value                | Label        |
| -------------------- | ------------ |
| STATUS_IMPROVING     | Improved     |
| STATUS_STABLE        | Unchanged    |
| STATUS_DETERIORATING | Deteriorated |

<br/>
<br/>
<br/>
