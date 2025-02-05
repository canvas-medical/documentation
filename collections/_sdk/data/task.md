---
title: "Task"
slug: "data-task"
excerpt: "Canvas SDK Task"
hidden: false
---

## Introduction

A `Task` represents a to-do item to be addressed. Tasks can be assigned to individual staff members and can also have associated comments and labels.

## Basic usage

To get a task by it's identifier, use the `get` method on the `Task` model manager:

```python
from canvas_sdk.v1.data.task import Task

task = Task.objects.get(id="7895e1db-f8de-4660-a0a3-9e5b43a475c6")
```

From a `Patient` object, tasks for the patient can be accessed with the `tasks` attribute:

```python
import arrow
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.task import TaskStatus

patient = Patient.objects.get(id="36950971cb3e4174ad8b9d365abfd6d0")

# All tasks for the patient
tasks_for_patient = patient.tasks.all()

# Tasks for the patient that are overdue
tasks_for_patient_overdue = patient.tasks.filter(due__lte=arrow.utcnow().datetime, status=TaskStatus.OPEN)
```

`Task` objects are also able to have associated `TaskLabel` objects.

```python
from canvas_sdk.v1.data.task import Task

task = Task.objects.get(id="7895e1db-f8de-4660-a0a3-9e5b43a475c6")

[(label.name, label.color,) for label in task.labels.all()]

# [('Emergent', 'red')]
```

`Staff` members are able to leave comments on tasks. These are stored as associated `TaskComment` objects. For example:

```python
from canvas_sdk.v1.data.task import Task

task = Task.objects.get(id="7895e1db-f8de-4660-a0a3-9e5b43a475c6")

[(comment.creator, comment.body,) for comment in task.comments.all()]
# [(<Staff: Sam Jones>, "Please call patient.")]
```

## Attributes

### Task

| Field Name | Type                                  |
|------------|---------------------------------------|
| id         | UUID                                  |
| dbid       | Integer                               |
| created    | DateTime                              |
| modified   | DateTime                              |
| creator    | [Staff](/sdk/data-staff/#staff)       |
| assignee   | [Staff](/sdk/data-staff/#staff)       |
| patient    | [Patient](/sdk/data-patient/#patient) |
| task_type  | [TaskType](#tasktype)                 |
| tag        | String                                |
| title      | String                                |
| due        | DateTime                              |
| due_event  | [EventType](#eventtype)               |
| status     | [TaskStatus](#taskstatus)             |
| comments   | [TaskComment](#taskcomment)[]         |
| labels     | [TaskLabel](#tasklabel)[]             |

### TaskComment

| Field Name       | Type                            |
|------------------|---------------------------------|
| id               | UUID                            |
| dbid             | Integer                         |
| created          | DateTime                        |
| modified         | DateTime                        |
| creator          | [Staff](/sdk/data-staff/#staff) |
| task             | [Task](/sdk/data-task/#task)    |
| body             | String                          |

### TaskLabel

| Field Name       | Type                                                |
|------------------|-----------------------------------------------------|
| id               | UUID                                                |
| dbid             | Integer                                             |
| tasks            | M2M                                                 |
| position         | Integer                                             |
| color            | [ColorEnum](/sdk/data-enumeration-types/#colorenum) |
| task_association | [Origin](/sdk/data-enumeration-types/#origin)       |
| name             | String                                              |
| active           | Boolean                                             |
| modules          | [TaskLabelModule](#tasklabelmodule)                 |

## Enumeration types

### TaskType

| Value    | Label     |
|----------|-----------|
| Task     | Task      |
| Reminder | Reminder  |

### EventType

| Value      | Label      |
|------------|------------|
| Chart Open | Chart Open |

### TaskStatus

| Value       | Label       |
|-------------|-------------|
| COMPLETED   | Completed   |
| CLOSED      | Closed      |
| OPEN        | Open        |

### TaskLabelModule

| Value       | Label       |
|-------------|-------------|
| claims      | Claims      |
| tasks       | Tasks       |

<br/>
<br/>
<br/>
