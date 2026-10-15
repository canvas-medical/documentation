---
title: "Tasks"
slug: "effect-tasks"
excerpt: "Effects for creating and updating tasks"
hidden: false
---

The Canvas SDK includes functionality to create, update and add comments to tasks in Canvas.

## Adding a Task

To add a task, build an `AddTask` and return its `apply()` from your handler.

### Methods

#### apply() → Effect

Creates the task.

- `title` is required.
- `id` is optional. Canvas generates one when it is omitted; set it yourself to reference the new task from another effect in the same handler, as in [Creating a task and a comment together](#creating-a-task-and-a-comment-together).

### Attributes

| Attribute          | Type               | Description                                                                          | Required |
|--------------------|--------------------|--------------------------------------------------------------------------------------|----------|
| id                 | string or UUID     | Task unique UUID. If none is supplied, one is generated automatically.               | No       |
| assignee_id        | string             | The id of the [staff](/sdk/data-staff/) the task should be assigned to.              | No       |
| team_id            | string             | The id of the [team](/sdk/data-team/) the task should be assigned to.                | No       |
| patient_id         | string             | The id of the [patient](/sdk/data-patient/) the task is associated with.             | No       |
| title              | string             | The title of the task. This is displayed at the top of a task card in the Canvas UI. | Yes      |
| due                | datetime           | A date/time when the task is due.                                                    | No       |
| status             | TaskStatus         | A status of `OPEN`, `CLOSED` or `COMPLETED`. Defaults to `OPEN` if not supplied.     | No       |
| priority           | TaskPriority       | A priority of `STAT`, `URGENT`, or `ROUTINE`. Defaults to no priority if not supplied. | No       |
| labels             | list[string]       | A list of labels that will be added at the bottom of a task card in the Canvas UI.   | No       |
| author_id          | string or UUID     | Author's id to set task creator, defaults to CanvasBot.                              | No       |
| linked_object_id   | string or UUID     | Linked object id of linked object.                                                   | No       |
| linked_object_type | LinkableObjectType | Type of the [LinkedObject](#linked-object-type)                                      | No       |

### Enumeration Types

#### Linked Object Type

| Value    | Description |
|----------|-------------|
| REFERRAL | REFERRAL    |
| IMAGING  | IMAGING     |

#### TaskPriority

| Value   | Description                                                                            |
|---------|----------------------------------------------------------------------------------------|
| STAT    | The request should be actioned immediately — highest possible priority. E.g. an emergency. |
| URGENT  | The request should be actioned promptly — higher priority than routine.                |
| ROUTINE | The request has normal priority.                                                       |

### Example

An example of adding a task:

```python
import arrow

from canvas_sdk.effects import Effect
from canvas_sdk.effects.task import AddTask, AddTaskComment, UpdateTask, TaskPriority, TaskStatus
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler

from canvas_sdk.v1.data.lab import LabReport
from canvas_sdk.v1.data.staff import Staff
from canvas_sdk.v1.data.team import Team
from canvas_sdk.v1.data.referral import Referral


class MyHandler(BaseHandler):
    RESPONDS_TO = [
        EventType.Name(EventType.LAB_REPORT_CREATED),
    ]

    def compute(self) -> list[Effect]:
        lab_report = LabReport.objects.get(id=self.target)
        staff_assignee = Staff.objects.get(last_name="Weed")
        team = Team.objects.get(name="Labs")

        linked_task_type = AddTask.LinkableObjectType.REFERRAL
        referral = Referral.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

        if lab_report.patient:
            add_task = AddTask(
                assignee_id=staff_assignee.id,
                author_id=staff_assignee.id,
                team_id = team.id,
                patient_id=lab_report.patient.id,
                title="Please call the patient with their test results.",
                due=arrow.utcnow().shift(days=5).datetime,
                status=TaskStatus.OPEN,
                priority=TaskPriority.URGENT,
                labels=["call"],
                linked_object_id=referral.id,
                linked_object_type=linked_task_type,
            )

            return [add_task.apply()]

        return []
```

## Updating a Task

To update an existing task, build an `UpdateTask` and return its `apply()` from your handler.

### Methods

#### apply() → Effect

Updates the task.

- `id` is required, and must be the id of an existing task.
- Only the attributes you set on the effect are changed. Attributes you leave unset keep their current values.

### Attributes

| Attribute   | Type           | Description                                                                          | Required |
|-------------|----------------|--------------------------------------------------------------------------------------|----------|
| id          | string         | The id of the task being updated.                                                    | Yes      |
| assignee_id | string         | The id of the [staff](/sdk/data-staff/) the task should be assigned to.              | No       |
| team_id     | string         | The id of the [team](/sdk/data-team/) the task should be assigned to.                | No       |
| patient_id  | string         | The id of the [patient](/sdk/data-patient/) the task is associated with.             | No       |
| title       | string         | The title of the task. This is displayed at the top of a task card in the Canvas UI. | No       |
| due         | datetime       | A date/time when the task is due.                                                    | No       |
| status      | TaskStatus     | A status of `OPEN`, `CLOSED` or `COMPLETED`.                                          | No       |
| priority    | TaskPriority   | A priority of `STAT`, `URGENT`, or `ROUTINE`. See [TaskPriority](#taskpriority).      | No       |
| labels      | list[string]   | A list of labels that will be added at the bottom of a task card in the Canvas UI.   | No       |

### Example

An example of updating a task to a status of `COMPLETED`:

```python
from canvas_sdk.effects.task import UpdateTask, TaskStatus
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self):
        update_task = UpdateTask(
            id="d06276ba-85c5-471b-87c0-9c9805f4ca6f",
            status=TaskStatus.COMPLETED,
        )

        return [update_task.apply()]
```

## Adding a comment to a task

To add a comment to a task, build an `AddTaskComment` and return its `apply()` from your handler.

### Methods

#### apply() → Effect

Adds the comment to the task.

- `task_id` and `body` are required. To comment on a task created in the same handler, see [Creating a task and a comment together](#creating-a-task-and-a-comment-together).

### Attributes

| Attribute | Type           | Description                                                     | Required |
|-----------|----------------|-----------------------------------------------------------------|----------|
| task_id   | string         | The id of the task the comment is added to.                     | Yes      |
| body      | string         | The comment body.                                               | Yes      |
| author_id | string or UUID | Author's id to set task comment creator, defaults to CanvasBot. | No       |

### Example

```python
from canvas_sdk.effects.task import AddTaskComment
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.staff import Staff

class MyHandler(BaseHandler):
    def compute(self):
        author = Staff.objects.get(last_name="Weed")
        add_task_comment = AddTaskComment(
            task_id="d06276ba-85c5-471b-87c0-9c9805f4ca6f",
            body="I tried to call the patient but did not get an answer.",
            author_id=author.id
        )

        return [add_task_comment.apply()]
```

## Creating a task and a comment together

`AddTaskComment` requires the `task_id` of an existing task. To create a brand new
task **and** add a comment to it in a single `compute()` return, supply your own
`id` to `AddTask` and reuse that same value as the `task_id` on `AddTaskComment`.
Because the `id` on `AddTask` is optional and is generated for you when omitted,
the trick is simply to generate it yourself so you can reference it on the comment.

There is no need to create the task first and listen for a follow-up event — just
return both effects from the same handler, with the `AddTask` effect before the
`AddTaskComment` effect.

```python
import uuid

import arrow

from canvas_sdk.effects import Effect
from canvas_sdk.effects.task import AddTask, AddTaskComment, TaskStatus
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = [
        EventType.Name(EventType.LAB_REPORT_CREATED),
    ]

    def compute(self) -> list[Effect]:
        # Generate the task id up front so the comment can reference it.
        task_id = str(uuid.uuid4())

        add_task = AddTask(
            id=task_id,
            title="Please call the patient with their test results.",
            due=arrow.utcnow().shift(days=1).datetime,
            status=TaskStatus.OPEN,
        )

        add_task_comment = AddTaskComment(
            task_id=task_id,
            body="Results flagged abnormal — follow up today.",
        )

        # Order matters: the task must be created before the comment.
        return [add_task.apply(), add_task_comment.apply()]
```

> **Note:** The effects are applied in the order they are returned, so the `AddTask`
> effect must come before the `AddTaskComment` effect that references it. Both
> effects must be returned from the same handler — don't split them across separate
> handlers or plugins, and don't defer either effect, since that breaks the ordering
> the comment relies on.

<br/>
<br/>
<br/>