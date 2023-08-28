# Tasks

The Tasks API is responsible for managing tasks (i.e., work to be done
by staff members). The API provides methods for creating, updating,
(re)assigning, labeling, commenting on, completing, and closing tasks.

## Basic Usage

The Tasks interface is designed to be straightforward and offers a
collection of functions that can be utilized to manage the lifecycle of
tasks in the system.

``` python
from datetime import date
from canvas_core import tasks
from canvas_core.tasks.models import Task

>>> from canvas_core import staffing, tasks

# Create a task.
>>> review_refills_task = tasks.create_task(
...     title="Review all refill requests",
...     creator=staffing.get_service_user_staff(),
...     labels=["urgent"],
... )

# Retrieve a task by its ID.
>>> review_refills_task = tasks.get_task(task_id=review_refills_task.id)

# Assign the task to the appropriate team (or staff member).
>>> Team = staffing.get_team_model()
>>> refills_team = next(staffing.list_teams(responsibility=Team.Responsibility.PROCESS_REFILL_REQUESTS))
>>> tasks.assign_task(review_refills_task, assignee=refills_team)
# Or:
>>> tasks.assign(assignee=refills_team)

# Update a task (e.g., set its due date).
>>> tasks.update_task(review_refills_task, due=date.today())

# Add a label to a task.
>>> tasks.add_task_labels(review_refills_task, label_names=("important",))
# Or:
>>> review_refills_task.add_label(label="important")

# Remove a label from a task.
>>> tasks.remove_task_label(review_refills_task, label_name="urgent")
# Or:
>>> review_refills_task.remove_label(label="urgent")

# Comment on a task.
>>> tasks.add_task_comment(review_refills_task, comment="We'll need to get this done quickly!")
# Or:
>>> review_refills_task.add_comment(comment="We'll need to get this done quickly!")

# Close a task (i.e., as incomplete)
>>> tasks.close_task(review_refills_task)
# Or:
>>> review_refills_task.close()

# Reopen a (closed) task.
>>> tasks.reopen_task(review_refills_task)
# Or:
>>> review_refills_task.reopen()

# Mark a task as complete.
>>> tasks.complete_task(review_refills_task)
# Or:
>>> review_refills_task.complete()

# List tasks and filter by their status, assignee, or creator.
>>> refill_reviews = tasks.list_tasks(status=Task.Status.OPEN, assignee=refills_team)
```

## Models

The Tasks interface provides the following models:

1.  `canvas_core.tasks.models.Task`{.interpreted-text role="py:class"},
    the Task itself.
2.  `canvas_core.tasks.models.Comment`{.interpreted-text
    role="py:class"}, a comment on a Task.
3.  `canvas_core.tasks.models.Label`{.interpreted-text role="py:class"},
    a label on a Task.

## API Reference

::: {.automodule members=""}
canvas_core.tasks
:::

::: {.automodule members="Task, Comment, Label"}
canvas_core.tasks.models
:::
