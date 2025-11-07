---
title: "Labs"
slug: "data-labs"
excerpt: "Canvas SDK Labs"
hidden: false
---

## Introduction

The Canvas SDK provides comprehensive models for working with laboratory data throughout the entire lab workflow—from ordering tests to reviewing results. The primary models include:

- **`LabOrder`**: Represents a lab order placed for a patient, including order details, transmission type, and associated tests
- **`LabTest`**: Individual tests within a lab order, tracking status from creation through processing
- **`LabReport`**: Contains the results returned from the lab, including all values and associated metadata
- **`LabValue`**: Individual test results within a lab report, including values, units, and reference ranges
- **`LabReview`**: Tracks the clinical review process for lab results, including provider comments and patient communication

## Basic Usage

To retrieve a `LabReport` model by id, use the `objects.get` method on the model. For example:

```python
from canvas_sdk.v1.data.lab import LabReport

lab_report = LabReport.objects.get(id="bcd287b7-8b04-4540-a1ea-6529eb576565")
```

## Filtering

To retrieve the `LabValue` instances that are associated with the `LabReport`, you can either call the `values` on the `LabReport` instance:

```python
from canvas_sdk.v1.data.lab import LabReport

lab_report = LabReport.objects.get(id="bcd287b7-8b04-4540-a1ea-6529eb576565")
lab_values = lab_report.values.all()
```

Or query the `LabValue` model and pass the `report` argument:

```python
from canvas_sdk.v1.data.lab import LabReport, LabValue

lab_report = LabReport.objects.get(id="bcd287b7-8b04-4540-a1ea-6529eb576565")
lab_values = LabValue.objects.filter(lab_report=lab_report)
```

Additionally, codings for lab values can be attained by querying the `LabValueCoding` model. To retrieve the codings associated with a `LabValue`, you can call `codings` on the `LabValue` instance:

```python
from logger import log
from canvas_sdk.v1.data.lab import LabReport, LabValue

lab_report = LabReport.objects.get(id="bcd287b7-8b04-4540-a1ea-6529eb576565")
lab_values = LabValue.objects.filter(lab_report=lab_report)
for value in lab_values:
    log.info(value.codings.all())
```

Or query the `LabValueCoding` model directly:

```python
from logger import log
from canvas_sdk.v1.data.lab import LabReport, LabValue, LabValueCoding

lab_report = LabReport.objects.get(id="bcd287b7-8b04-4540-a1ea-6529eb576565")
lab_values = LabValue.objects.filter(lab_report=lab_report)
for value in lab_values:
    lab_value_codings = LabValueCoding.objects.filter(value=value)
    log.info(lab_value_codings)
```

To query all lab reports for a particular patient, the `patient` argument can be used:

```python
from logger import log
from canvas_sdk.v1.data.lab import LabReport
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="6cbc40b408294a5f9b41f57ba1b2b487")
lab_report = LabReport.objects.filter(patient=patient)
```

## Example

The following plugin code will run every time a new Lab Report is created and log the patient it is for, along with the values and codings from the report's results:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log

from canvas_sdk.v1.data.lab import LabReport


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.LAB_REPORT_CREATED)

    def compute(self):
        lab_report = LabReport.objects.select_related("patient").get(id=self.target)
        if lab_report.patient:
            log.info(f"{lab_report.patient.first_name} {lab_report.patient.last_name}")
        for value in lab_report.values.all():
            log.info(f"{value.value} {value.units}")
            for coding in value.codings.all():
                log.info(coding.system)
                log.info(coding.name)
                log.info(coding.code)
        return []
```

For complete field documentation on all lab models, see the [Attributes](#attributes) section below.

### Working with Lab Orders and Tests

You can also work with lab orders and their associated tests. Here's an example of querying a lab order and checking the status of its tests:

```python
from canvas_sdk.v1.data.lab import LabOrder, LabTest

# Get a lab order by ID
lab_order = LabOrder.objects.get(id="abc123...")

# Access all tests in the order
for test in lab_order.tests.all():
    print(f"Test: {test.ontology_test_name}")
    print(f"Status: {test.status}")
    print(f"Code: {test.ontology_test_code}")

    # Check if results have been received
    if test.report:
        print(f"Report available with {test.report.values.count()} values")
```

### Navigating Between Lab Orders and Reports

Lab orders and lab reports are connected through the `LabTest` model. Here's how to navigate between them:

#### Getting the LabOrder from a LabReport

```python
from canvas_sdk.v1.data.lab import LabReport

# Get a lab report
lab_report = LabReport.objects.get(id="report-id")

# Access the lab order through the tests
# Each report can have multiple tests, and each test references its order
for test in lab_report.tests.all():
    lab_order = test.order
    print(f"Order ID: {lab_order.id}")
    print(f"Ordered by: {lab_order.ordering_provider.full_name if lab_order.ordering_provider else 'N/A'}")
    print(f"Date ordered: {lab_order.date_ordered}")
    break  # Usually all tests in a report share the same order
```

#### Getting LabReports from a LabOrder

```python
from canvas_sdk.v1.data.lab import LabOrder

# Get a lab order
lab_order = LabOrder.objects.get(id="order-id")

# Access reports through the tests
for test in lab_order.tests.all():
    if test.report:
        print(f"Report ID: {test.report.id}")
        print(f"Date performed: {test.report.date_performed}")
        print(f"Number of values: {test.report.values.count()}")
```

### Working with Lab Reviews

Lab reviews track the clinical review process for lab results, including provider comments and patient communication. Here's how to work with the LabReport and LabReview relationship:

#### Accessing the Review from a LabReport

```python
from canvas_sdk.v1.data.lab import LabReport

# Get a lab report
lab_report = LabReport.objects.get(id="report-id")

# Check if the report has been reviewed
if lab_report.review:
    lab_review = lab_report.review
    print(f"Review status: {lab_review.status}")
    print(f"Internal comment: {lab_review.internal_comment}")
    print(f"Message to patient: {lab_review.message_to_patient}")

    # Access the provider who reviewed it
    if lab_review.originator:
        print(f"Reviewed by: {lab_review.originator.full_name}")
else:
    print("Report has not been reviewed yet")
```

#### Accessing Reports from a LabReview

```python
from canvas_sdk.v1.data.lab import LabReview

# Get a lab review
lab_review = LabReview.objects.get(id="review-id")

# Access all reports in this review batch
for report in lab_review.reports.all():
    print(f"Report ID: {report.id}")
    print(f"Date performed: {report.date_performed}")
    print(f"Number of values: {report.values.count()}")

    # Check if this report requires signature
    if report.requires_signature:
        print("  ⚠️  Requires provider signature")
```

#### Finding Unreviewed Lab Reports

```python
from canvas_sdk.v1.data.lab import LabReport
from canvas_sdk.v1.data.patient import Patient

# Get all unreviewed lab reports for a patient
patient = Patient.objects.get(id="patient-id")
unreviewed_reports = LabReport.objects.filter(
    patient=patient,
    review__isnull=True,
    deleted=False
)

print(f"Found {unreviewed_reports.count()} unreviewed reports")
for report in unreviewed_reports:
    print(f"Report from {report.date_performed} - {report.values.count()} values")
```

### Filtering Lab Results by Abnormal Values

A common use case is to identify abnormal lab values that may require clinical attention:

```python
from canvas_sdk.v1.data.lab import LabReport, LabValue
from canvas_sdk.v1.data.patient import Patient

# Get all lab reports for a patient
patient = Patient.objects.get(id="patient-id")
lab_reports = LabReport.objects.filter(patient=patient)

# Find all abnormal values
for report in lab_reports:
    abnormal_values = report.values.filter(abnormal_flag__isnull=False).exclude(abnormal_flag="")

    if abnormal_values.exists():
        print(f"Report from {report.date_performed}:")
        for value in abnormal_values:
            for coding in value.codings.all():
                print(f"  {coding.name}: {value.value} {value.units} (Flag: {value.abnormal_flag})")
```

## Attributes

### LabReport

| Field Name           | Type                                  |
|----------------------|---------------------------------------|
| id                   | UUID                                  |
| dbid                 | Integer                               |
| created              | DateTime                              |
| modified             | DateTime                              |
| review_mode          | String                                |
| junked               | Boolean                               |
| requires_signature   | Boolean                               |
| assigned_date        | DateTime                              |
| patient              | [Patient](/sdk/data-patient/#patient) |
| transmission_type    | [TransmissionType](#transmissiontype) |
| for_test_only        | Boolean                               |
| external_id          | String                                |
| version              | Integer                               |
| requisition_number   | String                                |
| review               | [LabReview](#labreview)               |
| original_date        | DateTime                              |
| date_performed       | DateTime                              |
| custom_document_name | String                                |
| originator           | [CanvasUser](/sdk/data-canvasuser)    |
| committer            | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error     | [CanvasUser](/sdk/data-canvasuser)    |
| deleted              | Boolean                               |
| values               | [LabValue](#labvalue)[]               |

### LabReview

| Field Name                   | Type                                  |
|------------------------------|---------------------------------------|
| id                           | UUID                                  |
| dbid                         | Integer                               |
| created                      | DateTime                              |
| modified                     | DateTime                              |
| originator                   | [CanvasUser](/sdk/data-canvasuser)    |
| deleted                      | Boolean                               |
| committer                    | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error             | [CanvasUser](/sdk/data-canvasuser)    |
| internal_comment             | String                                |
| message_to_patient           | String                                |
| status                       | String                                |
| patient                      | [Patient](/sdk/data-patient/#patient) |
| patient_communication_method | String                                |
| reports                      | [LabReport](#labreport)[]             |
| tests                        | [LabTest](#labtest)[]                 |

### LabValue

| Field Name         | Type                                |
|--------------------|-------------------------------------|
| id                 | UUID                                |
| dbid               | Integer                             |
| created            | DateTime                            |
| modified           | DateTime                            |
| report             | [LabReport](#labreport)             |
| value              | String                              |
| units              | String                              |
| abnormal_flag      | String                              |
| reference_range    | String                              |
| low_threshold      | String                              |
| high_threshold     | String                              |
| comment            | String                              |
| observation_status | String                              |
| codings            | [LabValueCoding](#labvaluecoding)[] |

### LabValueCoding

| Field Name | Type                  |
|------------|-----------------------|
| dbid       | Integer               |
| created    | DateTime              |
| modified   | DateTime              |
| value      | [LabValue](#labvalue) |
| code       | String                |
| name       | String                |
| system     | String                |

### LabOrder

| Field Name                | Type                                              |
|---------------------------|---------------------------------------------------|
| id                        | UUID                                              |
| dbid                      | Integer                                           |
| created                   | DateTime                                          |
| modified                  | DateTime                                          |
| originator                | [CanvasUser](/sdk/data-canvasuser)                |
| deleted                   | Boolean                                           |
| committer                 | [CanvasUser](/sdk/data-canvasuser)                |
| entered_in_error          | [CanvasUser](/sdk/data-canvasuser)                |
| patient                   | [Patient](/sdk/data-patient/#patient)             |
| note                      | [Note](/sdk/data-note/#note)                      |
| ontology_lab_partner      | String                                            |
| ordering_provider         | [Staff](/sdk/data-staff/#staff)                   |
| comment                   | String                                            |
| requisition_number        | String                                            |
| is_patient_bill           | Boolean                                           |
| date_ordered              | DateTime                                          |
| fasting_status            | Boolean                                           |
| specimen_collection_type  | [SpecimenCollectionType](#specimencollectiontype) |
| transmission_type         | [TransmissionType](#transmissiontype)             |
| courtesy_copy_type        | [CourtesyCopyType](#courtesycopytype)             |
| courtesy_copy_number      | String                                            |
| courtesy_copy_text        | String                                            |
| parent_order              | [LabOrder](#laborder)                             |
| healthgorilla_id          | String                                            |
| manual_processing_status  | [ManualProcessingStatus](#manualprocessingstatus) |
| manual_processing_comment | String                                            |
| labcorp_abn_url           | URL                                               |
| reasons                   | [LabOrderReason](#laborderreason)[]               |
| tests                     | [LabTest](#labtest)[]                             |

### LabOrderReason

| Field Name        | Type                                                  |
|-------------------|-------------------------------------------------------|
| dbid              | Integer                                               |
| created           | DateTime                                              |
| modified          | DateTime                                              |
| originator        | [CanvasUser](/sdk/data-canvasuser)                    |
| deleted           | Boolean                                               |
| committer         | [CanvasUser](/sdk/data-canvasuser)                    |
| entered_in_error  | [CanvasUser](/sdk/data-canvasuser)                    |
| order             | [LabOrder](#laborder)                                 |
| mode              | [LabReasonMode](#labreasonmode)                       |
| reason_conditions | [LabOrderReasonCondition](#laborderreasoncondition)[] |

### LabOrderReasonCondition

| Field Name         | Type                                  |
|--------------------|---------------------------------------|
| dbid               | Integer                               |
| created            | DateTime                              |
| modified           | DateTime                              |
| originator         | [CanvasUser](/sdk/data-canvasuser)    |
| deleted            | Boolean                               |
| committer          | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error   | [CanvasUser](/sdk/data-canvasuser)    |
| reason             | [LabOrderReason](#laborderreason)     |
| condition          | [Condition](/sdk/data-condition)      |

### LabTest

Represents an individual test within a lab order. Each `LabTest` tracks the lifecycle of a specific test from order creation through processing and result receipt.

| Field Name                  | Type                                      |
|-----------------------------|-------------------------------------------|
| id                          | UUID                                      |
| dbid                        | Integer                                   |
| created                     | DateTime                                  |
| modified                    | DateTime                                  |
| ontology_test_name          | String                                    |
| ontology_test_code          | String                                    |
| status                      | [LabTestOrderStatus](#labtestorderstatus) |
| report                      | [LabReport](#labreport)                   |
| specimen_type               | String                                    |
| specimen_source_code        | String                                    |
| specimen_source_description | String                                    |
| specimen_source_coding_system | String                                  |
| order                       | [LabOrder](#laborder)                     |
| aoe_code                    | String                                    |
| procedure_class             | String                                    |

## Enumeration types

### TransmissionType

| Value | Label  |
|-------|--------|
| F     | fax    |
| H     | hl7    |
| M     | manual |

### SpecimenCollectionType

| Value | Label                  |
|-------|------------------------|
| L     | on location            |
| P     | patient service center |
| O     | other                  |

### CourtesyCopyType

| Value | Label  |
|-------|--------|
| A     | account|
| F     | fax    |
| P     | patient|

### ManualProcessingStatus

| Value        | Label        |
|--------------|--------------|
| NEEDS_REVIEW | Needs Review |
| IN_PROGRESS  | In Progress  |
| PROCESSED    | Processed    |
| FLAGGED      | Flagged      |

### LabReasonMode

| Value | Label       |
|-------|-------------|
| MO    | monitor     |
| IN    | investigate |
| SF    | screen for  |
| UNK   | unknown     |

### LabTestOrderStatus

| Value | Label                  |
|-------|------------------------|
| NE    | new                    |
| SR    | staged for requisition |
| SE    | sending                |
| SF    | sending failed         |
| PR    | processing             |
| PF    | processing failed      |
| RE    | received               |
| RV    | reviewed               |
| IN    | inactive               |

<br/>
<br/>
<br/>
