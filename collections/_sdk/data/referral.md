---
title: "Referral"
slug: "data-referral"
excerpt: "Canvas SDK Referral"
hidden: false
---

## Introduction

The `Referral`, `ReferralReport`, and `ReferralReview` models represent referral results and their reviews.

## Basic Usage

To retrieve a `Referral`, `ReferralReport`, or `ReferralReview` by identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data.referral import Referral, ReferralReport, ReferralReview

referral = Referral.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
referral_report = ReferralReport.objects.get(id="c1a5a35a-4ee2-4a0e-85c0-21739dc8c4a8")
referral_review = ReferralReview.objects.get(id="b3e6f74c-2a1b-4c8d-9f2e-31842ae7d3b9")
```

If you have a patient object, the referrals, reports, and reviews can be accessed with the `referral_set`, `referral_reports`, and `referral_reviews` attributes, respectively on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
referrals = patient.referral_set.all()
reports = patient.referral_reports.all()
reviews = patient.referral_reviews.all()
```

## Filtering

Referrals, reports, and reviews can be filtered by any attribute that exists on the models.

Filtering is done with the `filter` method on the `Referral`, `ReferralReport`, and `ReferralReview` model managers.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.referral import Referral, ReferralReport, ReferralReview

referrals = Referral.objects.filter(priority="urgent")
reports = ReferralReport.objects.filter(requires_signature=True)
reviews = ReferralReview.objects.filter(status="completed")
```

## Related Tasks
To retrieve an Referral's related tasks, use the `get_task_objects` method on the Referral object.

```python
from canvas_sdk.v1.data.referral import Referral

referral = Referral.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
tasks = referral.get_task_objects().all()
```

## Attributes

### Referral

| Field Name            | Type                                                           |
|-----------------------|----------------------------------------------------------------|
| id                    | UUID                                                           |
| dbid                  | Integer                                                        |
| created               | DateTime                                                       |
| modified              | DateTime                                                       |
| originator            | [CanvasUser](/sdk/data-canvasuser)                             |
| deleted               | Boolean                                                        |
| committer             | [CanvasUser](/sdk/data-canvasuser)                             |
| entered_in_error      | [CanvasUser](/sdk/data-canvasuser)                             |
| patient               | [Patient](/sdk/data-patient/#patient)                          |
| note                  | [Note](/sdk/data-note/#note)                                   |
| assessments           | [Assessment](/sdk/data-assessment/#assessment)                 |
| service_provider      | [ServiceProvider](/sdk/data-serviceprovider/#service-provider) |
| clinical_question     | String                                                         |
| priority              | String                                                         |
| include_visit_note    | Boolean                                                        |
| notes                 | String                                                         |
| date_referred         | DateTime                                                       |
| internal_comment      | String                                                         |
| forwarded             | Boolean                                                        |
| internal_task_comment | [TaskComment](/sdk/data-task/#taskcomment)                     |
| task_ids              | String                                                         |

### ReferralReport

| Field Name         | Type                                                                  |
|--------------------|-----------------------------------------------------------------------|
| id                 | UUID                                                                  |
| dbid               | Integer                                                               |
| created            | DateTime                                                              |
| modified           | DateTime                                                              |             
| originator         | [CanvasUser](/sdk/data-canvasuser)                                    |
| assigned_by        | [CanvasUser](/sdk/data-canvasuser)                                    | 
| review_mode        | [DocumentReviewMode](/sdk/data-enumeration-types/#documentreviewmode) |
| junked             | Boolean                                                               |
| requires_signature | Boolean                                                               |
| assigned_date      | DateTime                                                              |
| team_assigned_date | DateTime                                                              |
| team               | [Team](/sdk/data-team/#team)                                          |
| patient            | [Patient](/sdk/data-patient/#patient)                                 |
| referral           | [Referral](#referral)                                                 |
| specialty          | String                                                                |
| comment            | String                                                                |
| priority           | Boolean                                                               |
| original_date      | Date                                                                  |
| review             | [ReferralReview](#referralreview)                                     |

### ReferralReview

| Field Name                    | Type                                   |
|-------------------------------|----------------------------------------|
| id                            | UUID                                   |
| dbid                          | Integer                                |
| created                       | DateTime                               |
| modified                      | DateTime                               |
| originator                    | [CanvasUser](/sdk/data-canvasuser)     |
| deleted                       | Boolean                                |
| committer                     | [CanvasUser](/sdk/data-canvasuser)     |
| entered_in_error              | [CanvasUser](/sdk/data-canvasuser)     |
| internal_comment              | String                                 |
| message_to_patient            | String                                 |
| status                        | String                                 |
| note                          | [Note](/sdk/data-note/)                |
| patient                       | [Patient](/sdk/data-patient/#patient)  |
| patient_communication_method  | String                                 |
