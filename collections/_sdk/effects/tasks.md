---
title: "Tasks"
slug: "effect-tasks"
excerpt: "Effects for creating and updating tasks"
hidden: false
---

The Canvas SDK includes functionality to create, update and add comments to tasks in Canvas.

## Adding a Task

To add a task, import the `AddTask` class and create an instance of it.

| Attribute          |          | Type               | Description                                                                          |
|--------------------|----------|--------------------|--------------------------------------------------------------------------------------|
| id                 | optional | string or UUID     | Task unique UUID. If none one will be generated automatically.                       |
| assignee_id        | optional | string             | The id of the [staff](/sdk/data-staff/) the task should be assigned to.              |
| team_id            | optional | string             | The id of the [team](/sdk/data-team/) the task should be assigned to.                |
| patient_id         | optional | string             | The id of the [patient](/sdk/data-patient/) the task is associated with.             |
| title              | required | string             | The title of the task. This is displayed at the top of a task card in the Canvas UI. |
| due                | optional | datetime           | A date/time when the task is due.                                                    |
| status             | optional | TaskStatus         | A status of OPEN, CLOSED or COMPLETED. Defaults to OPEN if not supplied.             |
| priority           | optional | TaskPriority       | A priority of `STAT`, `URGENT`, or `ROUTINE`. Defaults to no priority if not supplied. |
| labels             | optional | list[string]       | A list of labels that will be added at the bottom of a task card in the Canvas UI.   |
| author_id          | optional | string or UUID     | Author's id to set task creator, defaults to CanvasBot.                              |
| linked_object_id   | optional | string or UUID     | Linked object id of linked object. (Legacy - use add_linked_item instead)            |
| linked_object_type | optional | LinkableObjectType | Type of the [LinkedObject](#linked-object-type). (Legacy - use add_linked_item instead) |


### Methods

#### add_linked_item

The `add_linked_item` method allows you to link multiple items to a task. This is the recommended way to add linked items to tasks.

```python
add_linked_item(item_type: LinkedItemType, item_id: str) -> Self
```

**Parameters:**
- `item_type`: The type of item to link (see [LinkedItemType](#linked-item-type) enum)
- `item_id`: The URN (Uniform Resource Name) of the item to link

**Returns:** Self (for method chaining)

### Enumeration Types

#### Linked Item Type

The `LinkedItemType` enum defines all supported types of items that can be linked to a task:

| Value                            | Description                         |
|----------------------------------|-------------------------------------|
| COMMAND                          | Command objects                     |
| NOTE                             | Clinical notes                      |
| TASK                             | Other tasks                         |
| CLAIM                            | Claim objects                       |
| PATIENT_ADMINISTRATIVE_DOCUMENT  | Patient administrative documents    |
| UNCATEGORIZED_CLINICAL_DOCUMENT  | Uncategorized clinical documents    |
| IMAGING_REPORT                   | Imaging reports                     |
| REFERRAL_REPORT                  | Referral reports                    |
| LAB_REPORT                       | Lab reports                         |

#### Linked Object Type (Legacy)

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


An example of adding a task:

```python
import arrow

from canvas_sdk.effects import Effect
from canvas_sdk.effects.task import (
    AddTask,
    AddTaskComment,
    LinkedItemType,
    TaskPriority,
    TaskStatus,
    UpdateTask,
)
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

### Linking Multiple Items to a Task

You can use the `add_linked_item()` method to link multiple items to a task. This method supports linking notes, commands, claims, and various document types.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.task import AddTask, LinkedItemType, TaskStatus
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data.lab import LabReport
from canvas_sdk.v1.data.note import Note
from canvas_sdk.v1.data.staff import Staff
from canvas_sdk.v1.data.team import Team
from permalinks.urn import get_urn_v1


class Protocol(BaseProtocol):
    RESPONDS_TO = [
        EventType.Name(EventType.LAB_REPORT_CREATED),
    ]

    def compute(self) -> list[Effect]:
        lab_report = LabReport.objects.get(id=self.target)
        staff_assignee = Staff.objects.get(last_name="Weed")
        team = Team.objects.get(name="Labs")

        if lab_report.patient:
            # Create a task with multiple linked items
            add_task = AddTask(
                assignee_id=staff_assignee.id,
                author_id=staff_assignee.id,
                team_id=team.id,
                patient_id=lab_report.patient.id,
                title="Review lab results and follow up with patient",
                status=TaskStatus.OPEN,
                labels=["lab-review", "follow-up"],
            )

            # Link the lab report
            lab_report_urn = get_urn_v1(lab_report)
            add_task.add_linked_item(LinkedItemType.LAB_REPORT, lab_report_urn)

            # Link a related note if it exists
            related_note = Note.objects.filter(
                patient=lab_report.patient,
                is_committed=True
            ).first()
            if related_note:
                note_urn = get_urn_v1(related_note)
                add_task.add_linked_item(LinkedItemType.NOTE, note_urn)

            return [add_task.apply()]

        return []
```

## Updating a Task

To update an existing task, import the `UpdateTask` class and create an instance of it.

| Attribute   |          | Type           | Description                                                                          |
|-------------|----------|----------------|--------------------------------------------------------------------------------------|
| id          | required | string         | The id of the task being updated.                                                    |
| assignee_id | optional | string         | The id of the [staff](/sdk/data-staff/) the task should be assigned to.              |
| team_id     | optional | string         | The id of the [team](/sdk/data-team/) the task should be assigned to.                |
| patient_id  | optional | string         | The id of the [patient](/sdk/data-patient/) the task is associated with.             |
| title       | optional | string         | The title of the task. This is displayed at the top of a task card in the Canvas UI. |
| due         | optional | datetime       | A date/time when the task is due.                                                    |
| status      | optional | TaskStatus     | A status of `OPEN`, `CLOSED` or `COMPLETED`. Defaults to `OPEN` if not supplied.     |
| priority    | optional | TaskPriority   | A priority of `STAT`, `URGENT`, or `ROUTINE`. See [TaskPriority](#taskpriority).      |
| labels      | optional | list[string]   | A list of labels that will be added at the bottom of a task card in the Canvas UI.   |

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

### Updating a Task with Linked Items

You can also use `add_linked_item()` with `UpdateTask` to add linked items to an existing task:

```python
from canvas_sdk.effects.task import UpdateTask, LinkedItemType, TaskStatus
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.claim import Claim
from permalinks.urn import get_urn_v1


class Protocol(BaseHandler):
    def compute(self):
        # Get a claim to link to the task
        claim = Claim.objects.filter(
            patient__key="patient-123"
        ).first()

        # Update the task and add a linked claim
        update_task = UpdateTask(
            id="d06276ba-85c5-471b-87c0-9c9805f4ca6f",
            status=TaskStatus.OPEN,
        )

        if claim:
            claim_urn = get_urn_v1(claim)
            update_task.add_linked_item(LinkedItemType.CLAIM, claim_urn)

        return [update_task.apply()]
```

## Adding a comment to a task

To add a comment to a task, import the `AddTaskComment` class and create an instance of it.

| Attribute |          | Type           | Description                                                     |
|-----------|----------|----------------|-----------------------------------------------------------------|
| task_id   | required | string         | The id of the task being updated.                               |
| body      | required | string         | The comment body.                                               |
| author_id | optional | string or UUID | Author's id to set task comment creator, defaults to CanvasBot. |


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

<br/>
<br/>
<br/>