---
title: "Task"
slug: "data-task"
excerpt: "Canvas SDK Task"
hidden: false
---

### Fields

| Name           | Type     | Required                               | Description                                                             |
| :------------- | :------- | :------------------------------------- | :---------------------------------------------------------------------- |
| `id`      | _string_ | if updating | The id of the `Task`.  |
| `assignee` | `Staff` | `false` | The `Staff` member assigned to the task. |
| `patient` | `Patient` | `false` | The `Patient` that the task pertains to. |
| `title` | _string_ | `true` | The title of the task. This shows in the task header in the Canvas UI. |
| `due` | _datetime_ | `false` | The date/time that the task is due. |
| `status` | One of _open_, _completed_ or _closed_.  | `true` | The status of the task. Defaults to 'open' if not supplied. |
| `comments` | _list[TaskComment]_  | `false` | Comments that have been left on the task. |
| `label` | _list[string]_  | `false` | Labels that have been added to the task. |

### Methods

#### create

Returns an Effect to create a `Task`. Example:

```
from datetime import datetime, timedelta

from canvas_sdk.data.patient import Patient
from canvas_sdk.data.staff import Staff
from canvas_sdk.data.task import Task

task = Task(
    assignee=Staff(id="3640cd20de8a470aa570a852859ac87e"),
    patient=Patient(id="5350cd20de8a470aa570a852859ac87e"),
    title="Follow Up with patient",
    due=datetime.now() + timedelta(days=30),
)

task.create()
```

#### update

Returns an Effect to update a `Task`. Example:

```
task.labels = ["Urgent"]
task.update()
```

#### add_comment

Returns an Effect to add a comment to a `Task`. Example:

```
task.add_comment("This needs addressing soon.")
```
