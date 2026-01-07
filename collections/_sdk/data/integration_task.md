---
title: "IntegrationTask"
slug: "data-integration-task"
excerpt: "Canvas SDK IntegrationTask"
hidden: false
---

## Introduction

The `IntegrationTask` and `IntegrationTaskReview` models represent incoming documents that need processing and their associated review assignments. Integration tasks include faxes, document uploads, lab results, and patient portal submissions.

## Basic Usage

To get an integration task by its identifier, use the `get` method on the `IntegrationTask` model manager:

```python
from canvas_sdk.v1.data.integration_task import IntegrationTask

task = IntegrationTask.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

To get an integration task review:

```python
from canvas_sdk.v1.data.integration_task import IntegrationTaskReview

review = IntegrationTaskReview.objects.get(id="c1a5a35a-4ee2-4a0e-85c0-21739dc8c4a8")
```

From a `Patient` object, integration tasks for the patient can be accessed with the `integration_tasks` attribute:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="36950971cb3e4174ad8b9d365abfd6d0")
tasks_for_patient = patient.integration_tasks.all()
```

## Filtering

Integration tasks and reviews can be filtered by any attribute that exists on the models. The models also provide convenient filter methods for common use cases.

### By Status

```python
from canvas_sdk.v1.data.integration_task import IntegrationTask

unread_tasks = IntegrationTask.objects.unread()
pending_tasks = IntegrationTask.objects.pending_review()
processed_tasks = IntegrationTask.objects.processed()
error_tasks = IntegrationTask.objects.with_errors()
junked_tasks = IntegrationTask.objects.junked()
active_tasks = IntegrationTask.objects.not_junked()
```

### By Channel

```python
from canvas_sdk.v1.data.integration_task import IntegrationTask

faxes = IntegrationTask.objects.faxes()
uploads = IntegrationTask.objects.uploads()
from_engine = IntegrationTask.objects.from_integration_engine()
from_portal = IntegrationTask.objects.from_patient_portal()
```

### By Patient

```python
from canvas_sdk.v1.data.integration_task import IntegrationTask

patient_tasks = IntegrationTask.objects.for_patient("36950971cb3e4174ad8b9d365abfd6d0")
unread_faxes = IntegrationTask.objects.for_patient("36950971cb3e4174ad8b9d365abfd6d0").faxes().unread()
```

### Filtering Reviews

```python
from canvas_sdk.v1.data.integration_task import IntegrationTaskReview

task_reviews = IntegrationTaskReview.objects.for_task("d2194110-5c9a-4842-8733-ef09ea5ead11")
active_reviews = IntegrationTaskReview.objects.active()
junked_reviews = IntegrationTaskReview.objects.junked()
reviewer_reviews = IntegrationTaskReview.objects.by_reviewer("staff-uuid-here")
team_reviews = IntegrationTaskReview.objects.by_team("team-uuid-here")
```

## Attributes

### IntegrationTask

| Field Name       | Type                                                  |
|------------------|-------------------------------------------------------|
| id               | UUID                                                  |
| dbid             | Integer                                               |
| created          | DateTime                                              |
| modified         | DateTime                                              |
| status           | [IntegrationTaskStatus](#integrationtaskstatus)       |
| type             | String                                                |
| title            | String                                                |
| channel          | [IntegrationTaskChannel](#integrationtaskchannel)     |
| patient          | [Patient](/sdk/data-patient/#patient)                 |
| service_provider | [ServiceProvider](/sdk/data-serviceprovider/#service-provider) |
| reviews          | [IntegrationTaskReview](#integrationtaskreview)[]     |

#### Properties

| Property     | Type    | Description                                      |
|--------------|---------|--------------------------------------------------|
| is_fax       | Boolean | Returns True if this is a fax task               |
| is_pending   | Boolean | Returns True if task is pending review           |
| is_processed | Boolean | Returns True if task has been processed          |
| has_error    | Boolean | Returns True if task has an error status         |
| is_junked    | Boolean | Returns True if task is junked                   |

### IntegrationTaskReview

| Field Name    | Type                                              |
|---------------|---------------------------------------------------|
| id            | UUID                                              |
| dbid          | Integer                                           |
| created       | DateTime                                          |
| modified      | DateTime                                          |
| task          | [IntegrationTask](#integrationtask)               |
| template_name | String                                            |
| document_key  | String                                            |
| reviewer      | [Staff](/sdk/data-staff/#staff)                   |
| team_reviewer | [Team](/sdk/data-team/#team)                      |
| junked        | Boolean                                           |

#### Properties

| Property  | Type    | Description                                |
|-----------|---------|--------------------------------------------|
| is_active | Boolean | Returns True if review is not junked       |

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

| Value                   | Label                   |
|-------------------------|-------------------------|
| fax                     | Fax                     |
| document_upload         | Document Upload         |
| from_integration_engine | From Integration Engine |
| from_patient_portal     | From Patient Portal     |

<br/>
<br/>
<br/>
