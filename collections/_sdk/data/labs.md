---
title: "Labs"
slug: "data-labs"
excerpt: "Canvas SDK Labs"
hidden: false
---

# Introduction

The `LabReport`, `LabValue` and `LabReview` models represent diagnostic clinical laboratory results.

# Basic Usage

To retrieve a `LabReport` model by id, use the `objects.get` method on the model. For example:

```python
from canvas_sdk.v1.data.lab import LabReport

lab_report = LabReport.objects.get(id="bcd287b7-8b04-4540-a1ea-6529eb576565")
```

# Filtering

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

# Example

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
