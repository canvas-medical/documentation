---
title: "Staff"
slug: "data-staff"
excerpt: "Canvas SDK Staff"
hidden: false
---

## Introduction

The `Staff` model represents a staff member in a Canvas instance.

To get a `Staff` object by it's identifier, use the `get` method:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")
```

`Staff` objects are commonly used in related models, for example the `Task` model.
To see all of a staff member's assigned or created tasks, the following code can be used:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")

staff.assignee_tasks.all()
# <QuerySet [<Task: Task object (3)>]>

staff.creator_tasks.all()
# <QuerySet [<Task: Task object (7)>]>
```
