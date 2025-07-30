---
title: "Goal"
slug: "data-goal"
excerpt: "Canvas SDK Goal"
hidden: false
---

## Introduction

The `Goal` model represents a patient Goal in Canvas, which is always associated with a Note and a Patient.

## Basic usage

To get a goal by identifier, use the `get` method on the `Goal` model manager:

```python
from canvas_sdk.v1.data import Goal

goal = Goal.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, or note object, the goals for a patient or note can be accessed with the `goals` attribute on a `Patient` or `Note` object:

```python
from canvas_sdk.v1.data import Patient, Note

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
goals = patient.goals.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
goals = note.goals.all()
```

## Filtering

Goals can be filtered by any attribute that exists on the model.

Filtering for goals is done with the `filter` method on the `Goal` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data import Goal, GoalAchievementStatus

goals = Goal.objects.filter(achievement_status=GoalAchievementStatus.IN_PROGRESS)
```

## Attributes

### Goal

| Field Name         | Type                                            |
| ------------------ | ----------------------------------------------- |
| id                 | UUID                                            |
| dbid               | Integer                                         |
| created            | DateTime                                        |
| modified           | DateTime                                        |
| originator         | [CanvasUser](/sdk/data-canvasuser)              |
| committer          | [CanvasUser](/sdk/data-canvasuser)              |
| entered_in_error   | [CanvasUser](/sdk/data-canvasuser)              |
| patient            | [Patient](/sdk/data-patient/#patient)           |
| note               | [Note](/sdk/data-note)                          |
| lifecycle_status   | [GoalLifecycleStatus](#goallifecyclestatus)     |
| achievement_status | [GoalAchievementStatus](#goalachievementstatus) |
| priority           | [GoalPriority](#goalpriority)                   |
| due_date           | Date                                            |
| start_date         | Date                                            |
| progress           | String                                          |
| goal_statement     | String                                          |

## Enumeration types

### GoalLifecycleStatus

| Name      | Value     |
| --------- | --------- |
| PROPOSED  | proposed  |
| PLANNED   | planned   |
| ACCEPTED  | accepted  |
| ACTIVE    | active    |
| ON_HOLD   | on-hold   |
| COMPLETED | completed |
| CANCELLED | cancelled |
| REJECTED  | rejected  |

### GoalAchievementStatus

| Name           | Value          |
| -------------- | -------------- |
| IN_PROGRESS    | in-progress    |
| IMPROVING      | improving      |
| WORSENING      | worsening      |
| NO_CHANGE      | no-change      |
| ACHIEVED       | achieved       |
| SUSTAINING     | sustaining     |
| NOT_ACHIEVED   | not-achieved   |
| NO_PROGRESS    | no-progress    |
| NOT_ATTAINABLE | not-attainable |

### GoalPriority

| Name   | Value           |
| ------ | --------------- |
| HIGH   | high-priority   |
| MEDIUM | medium-priority |
| LOW    | low-priority    |

<br/>
<br/>
<br/>
