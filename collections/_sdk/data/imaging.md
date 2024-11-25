---
title: "Imaging"
slug: "data-imaging"
excerpt: "Canvas SDK Imaging"
hidden: false
---

## Introduction

The `ImagingOrder`, `ImagingReview` and `ImagingReport` models represent imaging results.

## Basic Usage

To retrieve an `ImagingOrder`, `ImagingReview`, or `ImagingReport` by identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data.imaging import ImagingOrder, ImagingReview, ImagingReport

imaging_order = ImagingOrder.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
imaging_review = ImagingReview.objects.get(id="c02c6b02-2581-46bf-819c-b5aacad2134c")
imaging_report = ImagingReport.objects.get(id="c1a5a35a-4ee2-4a0e-85c0-21739dc8c4a8")
```

If you have a patient object, the orders, reviews, and reports can be accessed with the `imaging_orders`, `imaging_reviews`, and `imaging_results` attributes, respectively on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
orders = patient.imaging_orders.all()
reviews = patient.imaging_reviews.all()
reports = patient.imaging_results.all()
```

## Filtering

Imaging orders, reviews, and reports can be filtered by any attribute that exists on the models.

Filtering is done with the `filter` method on the `ImagingOrder`, `ImagingReview`, and `ImagingReport` model managers.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.imaging import ImagingOrder, ImagingReview, ImagingReport

orders = ImagingOrder.objects.filter(status="completed")
reviews = ImagingReview.objects.filter(is_released_to_patient=False)
reports = ImagingReport.objects.filter(requires_signature=True)
```

## Attributes

### ImagingOrder
| Field Name          | Type                                  |
|---------------------|---------------------------------------|
| id                  | UUID                                  |
| dbid                | Integer                               |
| created             | DateTime                              |
| modified            | DateTime                              |
| originator          | CanvasUser                            |
| deleted             | Boolean                               |
| committer           | CanvasUser                            |
| entered_in_error    | CanvasUser                            |
| patient             | [Patient](/sdk/data-patient/#patient) |
| imaging             | String                                |
| note_to_radiologist | String                                |
| internal_comment    | String                                |
| status              | [OrderStatus](#orderstatus)           |
| date_time_ordered   | DateTime                              |
| priority            | String                                |
| delegated           | Boolean                               |

### ImagingReview
| Field Name                   | Type                                                                  |
|------------------------------|-----------------------------------------------------------------------|
| id                           | UUID                                                                  |
| dbid                         | Integer                                                               |
| created                      | DateTime                                                              |
| modified                     | DateTime                                                              |
| originator                   | CanvasUser                                                            |
| deleted                      | Boolean                                                               |
| committer                    | CanvasUser                                                            |
| patient_communication_method | [ReviewPatientCommunicationMethod](#reviewpatientcommunicationmethod) |
| internal_comment             | String                                                                |
| message_to_patient           | String                                                                |
| is_released_to_patient       | Boolean                                                               |
| status                       | [ReviewStatus](#reviewstatus)                                         |
| patient                      | [Patient](/sdk/data-patient/#patient)                                 |

### ImagingReport
| Field Name         | Type                                        |
|--------------------|---------------------------------------------|
| id                 | UUID                                        |
| dbid               | Integer                                     |
| created            | DateTime                                    |
| modified           | DateTime                                    |
| review_mode        | [DocumentReviewMode](#documentreviewmode)   |
| junked             | Boolean                                     |
| requires_signature | Boolean                                     |
| assigned_date      | DateTime                                    |
| patient            | [Patient](/sdk/data-patient/#patient)       |
| order              | [ImagingOrder](#imagingorder)               |
| source             | [ImagingReportSource](#imagingreportsource) |
| name               | String                                      |
| result_date        | Date                                        |
| original_date      | Date                                        |
| review             | [ImagingReview](#imagingreview)             |

## Enumeration types

### OrderStatus
| Value       | Description      |
|-------------|------------------|
| proposed    | Proposed         |
| draft       | Draft            |
| planned     | Planned          |
| requested   | Requested        |
| received    | Received         |
| accepted    | Accepted         |
| in-progress | In-progress      |
| review      | Review           |
| completed   | Completed        |
| cancelled   | Cancelled        |
| suspended   | Suspended        |
| rejected    | Rejected         |
| failed      | Failed           |
| EIE         | Entered in Error |

### ReviewPatientCommunicationMethod
| Value | Description                           |
|-------|---------------------------------------|
| DM    | delegate call, can leave message      |
| DA    | delegate call, need patient to answer |
| DL    | delegate letter                       |
| DC    | do not communicate                    |
| AM    | already left message                  |
| AR    | already reviewed with patient         |

### ReviewStatus
| Value     | Label     |
|-----------|-----------|
| reviewing | reviewing |
| reviewed  | reviewed  |

### DocumentReviewMode
| Value | Label                    |
|-------|--------------------------|
| RR    | Review required          |
| AR    | Already reviewed offline |
| RN    | Review not required      |

### ImagingReportSource
| Value              | Label                         |
|--------------------|-------------------------------|
| RADIOLOGY_PATIENT  | Radiology Report From Patient |
| VERBAL_PATIENT     | Verbal Report From Patient    |
| DIRECTLY_RADIOLOGY | Directly Radiology Report     |
```
