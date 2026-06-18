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

### Note Tasks and Initial Comments

A `NoteTask` represents the link between a Task command and the `Task` it generates. When a task is created via a Task command, a `NoteTask` record is created that stores the original values entered in the command. Of importance is the **initial comment** that is provided during task creation in the `internal_comment` field.

This is important because `task.comments.all()` only returns manual comments added after the task is created through the interface—it does not include the original comment entered during task creation. To access that initial comment, you need to use the `NoteTask` model.

To get a note task by its identifier:

```python
from canvas_sdk.v1.data.task import NoteTask

note_task = NoteTask.objects.get(id="a1b2c3d4-e5f6-7890-abcd-ef1234567890")
print(f"Initial comment: {note_task.internal_comment}")
```

From a `Task` object, you can access the associated `NoteTask` to retrieve the initial comment:

```python
from canvas_sdk.v1.data.task import Task

task = Task.objects.get(id="7895e1db-f8de-4660-a0a3-9e5b43a475c6")

# Access the NoteTask to get the initial comment
note_task = task.note_tasks.first()
if note_task:
    print(f"Initial comment: {note_task.internal_comment}")
    print(f"Original title: {note_task.original_title}")
    print(f"Original assignee: {note_task.original_assignee}")
```

Common workflow pattern: handling a TASK_CREATED event and accessing the initial comment:

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.task import Task

class TaskCreatedHandler(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.TASK_CREATED)]

    def compute(self):
        task_id = self.target
        task = Task.objects.get(id=task_id)

        # Get the initial comment from the NoteTask
        note_task = task.note_tasks.first()
        if note_task:
            initial_comment = note_task.internal_comment
            # Use the initial comment for your logic
            self.log(f"Task created with initial comment: {initial_comment}")
```

From a `Note` object, note tasks can be accessed with the `note_tasks` attribute:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
note_tasks = note.note_tasks.all()

for note_task in note_tasks:
    print(f"Task: {note_task.original_title}")
    print(f"Initial comment: {note_task.internal_comment}")
```

## Attributes

### Task

| Field Name | Type                                  |
| ---------- | ------------------------------------- |
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
| metadata   | [TaskMetadata](#taskmetadata)[]       |
| note_tasks | [NoteTask](#notetask)[]               |

### NoteTask

| Field Name        | Type                                    |
| ----------------- | --------------------------------------- |
| id                | UUID                                    |
| dbid              | Integer                                 |
| created           | DateTime                                |
| modified          | DateTime                                |
| originator        | [CanvasUser](/sdk/data-canvas-user/)    |
| committer         | [CanvasUser](/sdk/data-canvas-user/)    |
| entered_in_error  | [CanvasUser](/sdk/data-canvas-user/)    |
| deleted           | Boolean                                 |
| note              | [Note](/sdk/data-note/#note)            |
| task              | [Task](#task)                           |
| patient           | [Patient](/sdk/data-patient/#patient)   |
| original_title    | String                                  |
| original_assignee | [Staff](/sdk/data-staff/#staff)         |
| original_team     | [Team](/sdk/data-team/)                 |
| original_role     | [CareTeamRole](/sdk/data-care-team/#careteamrole) |
| original_due      | DateTime                                |
| internal_comment  | String                                  |
| labels            | [TaskLabel](#tasklabel)[]               |

### TaskComment

| Field Name | Type                            |
| ---------- | ------------------------------- |
| id         | UUID                            |
| dbid       | Integer                         |
| created    | DateTime                        |
| modified   | DateTime                        |
| creator    | [Staff](/sdk/data-staff/#staff) |
| task       | [Task](/sdk/data-task/#task)    |
| body       | String                          |

### TaskLabel

| Field Name       | Type                                                |
| ---------------- | --------------------------------------------------- |
| id               | UUID                                                |
| dbid             | Integer                                             |
| tasks            | M2M                                                 |
| position         | Integer                                             |
| color            | [ColorEnum](/sdk/data-enumeration-types/#colorenum) |
| task_association | [Origin](/sdk/data-enumeration-types/#origin)       |
| name             | String                                              |
| active           | Boolean                                             |
| modules          | [TaskLabelModule](#tasklabelmodule)                 |
| claims           | [Claim](/sdk/data-claim)[]                          |

### TaskMetadata

| Field Name | Type              |
|------------|-------------------|
| id         | UUID              |
| dbid       | Integer           |
| created    | DateTime          |
| modified   | DateTime          |
| task       | [Task](#task)     |
| key        | String            |
| value      | String            |

```python
from canvas_sdk.v1.data.task import Task
from logger import log

task_id = "7895e1db-f8de-4660-a0a3-9e5b43a475c6"
task = Task.objects.get(id=task_id)
task_metadata = task.metadata.all()

for metadata in task_metadata:
   log.info(f"Task metadata: {metadata.key}, {metadata.value}") # external_system_id - EXT-12345
```

## Enumeration types

### TaskType

| Value    | Label    |
| -------- | -------- |
| Task     | Task     |
| Reminder | Reminder |

### EventType

| Value      | Label      |
| ---------- | ---------- |
| Chart Open | Chart Open |

### TaskStatus

| Value     | Label     |
| --------- | --------- |
| COMPLETED | Completed |
| CLOSED    | Closed    |
| OPEN      | Open      |

### TaskLabelModule

| Value  | Label  |
| ------ | ------ |
| claims | Claims |
| tasks  | Tasks  |

<br/>
<br/>
<br/>
