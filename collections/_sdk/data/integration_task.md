---
title: "Integration Task"
slug: "data-integration-task"
excerpt: "Canvas SDK Integration Task"
hidden: false
---

## Introduction

The `IntegrationTask` and `IntegrationTaskReview` models represent incoming documents that need processing in Canvas. Integration tasks are created when documents arrive via fax, document upload, integration engine, or the patient portal. Each task can have one or more reviews that track who is responsible for processing the document and its current state.

## Basic Usage

To retrieve an `IntegrationTask` or `IntegrationTaskReview` by identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data.integration_task import IntegrationTask, IntegrationTaskReview

task = IntegrationTask.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
review = IntegrationTaskReview.objects.get(id="c1a5a35a-4ee2-4a0e-85c0-21739dc8c4a8")
```

If you have a patient object, integration tasks can be accessed with the `integration_tasks` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
tasks = patient.integration_tasks.all()
```

## Filtering

Integration tasks and reviews can be filtered by any attribute that exists on the models.

### By status

Filter tasks by their processing status:

```python
from canvas_sdk.v1.data.integration_task import IntegrationTask

# Get all unread tasks
unread = IntegrationTask.objects.unread()

# Get tasks pending review (UNREAD or READ)
pending = IntegrationTask.objects.pending_review()

# Get processed tasks (PROCESSED or REVIEWED)
processed = IntegrationTask.objects.processed()

# Get tasks with errors
errored = IntegrationTask.objects.with_errors()

# Get non-junked tasks
active = IntegrationTask.objects.not_junked()
```

### By channel

Filter tasks by their source channel:

```python
from canvas_sdk.v1.data.integration_task import IntegrationTask

faxes = IntegrationTask.objects.faxes()
uploads = IntegrationTask.objects.uploads()
engine_tasks = IntegrationTask.objects.from_integration_engine()
portal_tasks = IntegrationTask.objects.from_patient_portal()
```

### By patient

```python
from canvas_sdk.v1.data.integration_task import IntegrationTask

tasks = IntegrationTask.objects.for_patient("patient-id")
```

### Filtering reviews

```python
from canvas_sdk.v1.data.integration_task import IntegrationTaskReview

# Get reviews for a specific task
reviews = IntegrationTaskReview.objects.for_task("task-id")

# Get active (non-junked) reviews
active_reviews = IntegrationTaskReview.objects.active()

# Get reviews by a specific reviewer
reviewer_reviews = IntegrationTaskReview.objects.by_reviewer("staff-id")

# Get reviews assigned to a specific team
team_reviews = IntegrationTaskReview.objects.by_team("team-id")
```

## Attributes

### IntegrationTask

| Field Name       | Type                                                           |
|------------------|----------------------------------------------------------------|
| id               | UUID                                                           |
| dbid             | Integer                                                        |
| created          | DateTime                                                       |
| modified         | DateTime                                                       |
| status           | [IntegrationTaskStatus](#integrationtaskstatus)                |
| type             | String                                                         |
| title            | String                                                         |
| channel          | [IntegrationTaskChannel](#integrationtaskchannel)              |
| patient          | [Patient](/sdk/data-patient/#patient)                          |
| service_provider | [ServiceProvider](/sdk/data-serviceprovider/#service-provider) |
| reviews          | [IntegrationTaskReview](#integrationtaskreview)[]              |

#### Properties

| Property     | Type    | Description                              |
|--------------|---------|------------------------------------------|
| is_fax       | Boolean | Whether this is a fax task               |
| is_pending   | Boolean | Whether this task is pending review      |
| is_processed | Boolean | Whether this task has been processed     |
| has_error    | Boolean | Whether this task has an error           |
| is_junked    | Boolean | Whether this task is junked              |

### IntegrationTaskReview

| Field Name    | Type                                          |
|---------------|-----------------------------------------------|
| id            | UUID                                          |
| dbid          | Integer                                       |
| created       | DateTime                                      |
| modified      | DateTime                                      |
| task          | [IntegrationTask](#integrationtask)           |
| template_name | String                                        |
| document_key  | String                                        |
| reviewer      | [Staff](/sdk/data-staff/#staff)               |
| team_reviewer | [Team](/sdk/data-team/#team)                  |
| junked        | Boolean                                       |

#### Properties

| Property  | Type    | Description                               |
|-----------|---------|-------------------------------------------|
| is_active | Boolean | Whether this review is active (not junked) |

## Enumeration types

### IntegrationTaskStatus

| Value | Label        |
|-------|--------------|
| UNR   | Unread       |
| UER   | Unread Error |
| REA   | Read         |
| ERR   | Error        |
| PRO   | Processed    |
| REV   | Reviewed     |
| JUN   | Junk         |

### IntegrationTaskChannel

| Value                    | Label                    |
|--------------------------|--------------------------|
| fax                      | Fax                      |
| document_upload          | Document Upload          |
| from_integration_engine  | From Integration Engine  |
| from_patient_portal      | From Patient Portal      |

<br/>
<br/>
<br/>
