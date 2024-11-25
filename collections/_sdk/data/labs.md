---
title: "Labs"
slug: "data-labs"
excerpt: "Canvas SDK Labs"
hidden: false
---

## Introduction

The `LabReport`, `LabValue` and `LabReview` models represent diagnostic clinical laboratory results.

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

A common plugin use case may be for a plugin to run every time a new Lab Report is created in Canvas. The following plugin code will run every time a new Lab Report is created and log the patient it is for, along with the values and codings from the report's results:

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

Each value and coding are instances of `LabValue` and `LabValueCoding`, respectively. To view the fields available for each of these models, they are available in the [Canvas SDK open source repository](https://github.com/canvas-medical/canvas-plugins/blob/main/canvas_sdk/v1/data/lab.py).

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
| originator           | CanvasUser                            |
| committer            | CanvasUser                            |
| entered_in_error     | CanvasUser                            |
| deleted              | Boolean                               |

### LabReview
| Field Name                   | Type                                  |
|------------------------------|---------------------------------------|
| id                           | UUID                                  |
| dbid                         | Integer                               |
| created                      | DateTime                              |
| modified                     | DateTime                              |
| originator                   | CanvasUser                            |
| deleted                      | Boolean                               |
| committer                    | CanvasUser                            |
| entered_in_error             | CanvasUser                            |
| internal_comment             | String                                |
| message_to_patient           | String                                |
| status                       | String                                |
| patient                      | [Patient](/sdk/data-patient/#patient) |
| patient_communication_method | String                                |

### LabValue
| Field Name         | Type                    |
|--------------------|-------------------------|
| id                 | UUID                    |
| dbid               | Integer                 |
| created            | DateTime                |
| modified           | DateTime                |
| report             | [LabReport](#labreport) |
| value              | String                  |
| units              | String                  |
| abnormal_flag      | String                  |
| reference_range    | String                  |
| low_threshold      | String                  |
| high_threshold     | String                  |
| comment            | String                  |
| observation_status | String                  |

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
| originator                | CanvasUser                                        |
| deleted                   | Boolean                                           |
| committer                 | CanvasUser                                        |
| entered_in_error          | CanvasUser                                        |
| patient                   | [Patient](/sdk/data-patient/#patient)             |
| ontology_lab_partner      | String                                            |
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

### LabOrderReason
| Field Name       | Type                            |
|------------------|---------------------------------|
| dbid             | Integer                         |
| created          | DateTime                        |
| modified         | DateTime                        |
| originator       | CanvasUser                      |
| deleted          | Boolean                         |
| committer        | CanvasUser                      |
| entered_in_error | CanvasUser                      |
| order            | [LabOrder](#laborder)           |
| mode             | [LabReasonMode](#labreasonmode) |

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
