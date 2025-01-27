---
title: "Tasks"
slug: "effect-tasks"
excerpt: "Effects for creating and updating tasks"
hidden: false
---

The Canvas SDK includes functionality to create, update and add comments to tasks in Canvas.

## Adding a Task

To add a task, import the `AddTask` class and create an instance of it.

| Attribute   |          | Type         | Description                                                                          |
|-------------|----------|--------------|--------------------------------------------------------------------------------------|
| assignee_id | optional | string       | The id of the [staff](/sdk/data-staff/) the task should be assigned to.              |
| team_id     | optional | string       | The id of the [team](/sdk/data-team/) the task should be assigned to.                |
| patient_id  | optional | string       | The id of the [patient](/sdk/data-patient/) the task is associated with.             |
| title       | required | string       | The title of the task. This is displayed at the top of a task card in the Canvas UI. |
| due         | optional | datetime     | A date/time when the task is due.                                                    |
| status      | optional | TaskStatus   | A status of OPEN, CLOSED or COMPLETED. Defaults to OPEN if not supplied.             |
| labels      | optional | list[string] | A list of labels that will be added at the bottom of a task card in the Canvas UI.   |

An example of adding a task:

```python
import arrow

from canvas_sdk.effects import Effect
from canvas_sdk.effects.task import AddTask, AddTaskComment, UpdateTask, TaskStatus
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

from canvas_sdk.v1.data.lab import LabReport
from canvas_sdk.v1.data.staff import Staff
from canvas_sdk.v1.data.team import Team


class Protocol(BaseProtocol):
    RESPONDS_TO = [
        EventType.Name(EventType.LAB_REPORT_CREATED),
    ]

    def compute(self) -> list[Effect]:
        lab_report = LabReport.objects.get(id=self.target)
        staff_assignee = Staff.objects.get(last_name="Weed")
        team = Team.objecst.get(name="Labs")

        if lab_report.patient:
            add_task = AddTask(
                assignee_id=staff_assignee.id,
                team_id = team.id,
                patient_id=lab_report.patient.id,
                title="Please call the patient with their test results.",
                due=arrow.utcnow().shift(days=5).datetime,
                status=TaskStatus.OPEN,
                labels=["call"],
            )

            return [add_task.apply()]

        return []
```

## Updating a Task

To update an existing task, import the `UpdateTask` class and create an instance of it.

| Attribute   |          | Type         | Description                                                                          |
|-------------|----------|--------------|--------------------------------------------------------------------------------------|
| id          | required | string       | The id of the task being updated.                                                    |
| assignee_id | optional | string       | The id of the [staff](/sdk/data-staff/) the task should be assigned to.              |
| team_id     | optional | string       | The id of the [team](/sdk/data-team/) the task should be assigned to.                |
| patient_id  | optional | string       | The id of the [patient](/sdk/data-patient/) the task is associated with.             |
| title       | optional | string       | The title of the task. This is displayed at the top of a task card in the Canvas UI. |
| due         | optional | satetime     | A date/time when the task is due.                                                    |
| status      | optional | TaskStatus   | A status of `OPEN`, `CLOSED` or `COMPLETED`. Defaults to `OPEN` if not supplied.     |
| labels      | optional | list[string] | A list of labels that will be added at the bottom of a task card in the Canvas UI.   |

An example of updating a task to a status of `COMPLETED`:

```python
from canvas_sdk.effects.task import UpdateTask, TaskStatus

update_task = UpdateTask(
    id="d06276ba-85c5-471b-87c0-9c9805f4ca6f",
    status=TaskStatus.COMPLETED,
)
return [update_task.apply()]
```

## Adding a comment to a task

To add a comment to a task, import the `AddTaskComment` class and create an instance of it.

| Attribute       |          | Type   | Description                       |
| ---------       | ------   | ----   | --------------------------------  |
| task_id         | required | string | The id of the task being updated. |
| body | required | string | The comment body.                 |

```python
from canvas_sdk.effects.task import AddTaskComment

add_task_comment = AddTaskComment(
    task_id="d06276ba-85c5-471b-87c0-9c9805f4ca6f",
    body="I tried to call the patient but did not get an answer.",
)
return [add_task_comment.apply()]
```
