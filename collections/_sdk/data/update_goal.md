---
title: "UpdateGoal"
slug: "data-update-goal"
excerpt: "Canvas SDK UpdateGoal"
hidden: false
---

## Introduction

The `UpdateGoal` model is the read-only record behind the [UpdateGoal](/sdk/commands/#updategoal) and [CloseGoal](/sdk/commands/#closegoal) commands, capturing a goal update or closure recorded against a [Goal](/sdk/data-goal/#goal). Like the other models in the data module, it cannot be written to directly; a goal update or closure is recorded by committing an `UpdateGoal` or `CloseGoal` command.

## Basic usage

To get an update goal by identifier, use the `get` method on the `UpdateGoal` model manager:

```python
from canvas_sdk.v1.data import UpdateGoal

update_goal = UpdateGoal.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
```

The primary way to retrieve a goal's update and closure history is the `updates` reverse accessor on a `Goal` object:

```python
from canvas_sdk.v1.data.goal import Goal

goal = Goal.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
updates = goal.updates.all()
```

You can also access the parent goal from an update with the `goal` attribute:

```python
from canvas_sdk.v1.data import UpdateGoal

update_goal = UpdateGoal.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
goal = update_goal.goal
```

## Filtering

`UpdateGoal` records can be filtered by any attribute that exists on the model.

Filtering is done with the `filter` method on the `UpdateGoal` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.goal import UpdateGoal, GoalAchievementStatus

updates = UpdateGoal.objects.filter(achievement_status=GoalAchievementStatus.ACHIEVED)
```

### Committed records

The `committed` method returns update goals that have been committed and not entered in error:

```python
from canvas_sdk.v1.data import UpdateGoal

committed_update_goals = UpdateGoal.objects.committed()
```

## Attributes

### UpdateGoal

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
| goal               | [Goal](/sdk/data-goal/#goal)                    |
| lifecycle_status   | [GoalLifecycleStatus](#goallifecyclestatus)     |
| achievement_status | [GoalAchievementStatus](#goalachievementstatus) |
| priority           | [GoalPriority](#goalpriority)                   |
| due_date           | Date                                            |
| progress           | String                                          |

Note: `patient` keys are UUIDs without dashes (for example, `1eed3ea2a8d546a1b681a2a45de1d790`), unlike the dashed `Goal` and `UpdateGoal` record IDs shown in the examples above.

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
