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
from canvas_sdk.v1.data.goal import Goal

goal = Goal.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, or note object, the goals for a patient or note can be accessed with the `goals` attribute on a `Patient` or `Note` object:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.note import Note

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
from canvas_sdk.v1.data.goal import Goal, GoalAchievementStatus

goals = Goal.objects.filter(achievement_status=GoalAchievementStatus.IN_PROGRESS)
```

### Committed goals

The `committed` method returns goals that have been committed and not entered in error:

```python
from canvas_sdk.v1.data.goal import Goal

committed_goals = Goal.objects.committed()
```

## Goal updates and closures

Each change to a goal — via the `update_goal` or `close_goal` command — is recorded as an `UpdateGoal`. Update actions revise the goal while leaving it active; close actions also move it to a closed `lifecycle_status` (e.g. `completed`, `cancelled`, `rejected`). A goal's updates are reachable through its `updates` accessor:

```python
from canvas_sdk.v1.data.goal import Goal

goal = Goal.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

# Every update or close recorded against this goal.
updates = goal.updates.all()

# The most recent committed update — the goal's current state — or None.
latest = goal.updates.committed().order_by("dbid").last()
```

`UpdateGoal` carries the same status, priority, and progress fields as `Goal` (without `goal_statement` / `start_date`), plus a `goal` foreign key back to the goal it updates. Like `Goal`, its manager supports `committed()` to filter to committed, non-entered-in-error records.

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
| updates            | QuerySet[[UpdateGoal](#updategoal)]             |

### UpdateGoal

An update or close action recorded against a [Goal](#goal), reachable from a goal via `goal.updates`. Written by the `update_goal` and `close_goal` commands.

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
| goal               | [Goal](#goal)                                   |
| lifecycle_status   | [GoalLifecycleStatus](#goallifecyclestatus)     |
| achievement_status | [GoalAchievementStatus](#goalachievementstatus) |
| priority           | [GoalPriority](#goalpriority)                   |
| due_date           | Date                                            |
| progress           | String                                          |

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