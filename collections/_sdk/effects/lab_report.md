---
title: "Lab Report Effect"
slug: "effect-lab-report"
excerpt: "Create, update, or enter-in-error a lab report, and attach results to it after the fact."
hidden: false
---

The `LabReport` effect creates and manages a [lab report](/sdk/data-labs/#labreport) directly from a plugin, independent of any lab order, results, or PDF. It's built for the asynchronous OCR pattern: create the report now with a plugin-supplied handle, then attach the extracted results later with [`LabReportAttachResults`](#labreportattachresults) once they're available.

A report is identified by one of two handles:

- `external_id` — a stable handle that your plugin supplies and controls. Use it throughout the asynchronous lifecycle, while the Canvas id is not yet known.
- `report_id` — the report's Canvas externally-exposable id. It becomes available once the report is created, and can be recovered from the `LAB_REPORT_CREATED` event or a [`LabReport`](/sdk/data-labs/#labreport) data query.

Reports created through this effect are routed to staff for review before they appear on the patient's chart.

## Attributes

| Name             | Type                        | Description                                                                                                                            |
|------------------|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `report_id`      | `str` or `UUID` or `None`   | The report's Canvas externally-exposable id. Must be unset when creating; used as the handle for `update()` and `enter_in_error()` once known. |
| `external_id`    | `str` or `None`             | A stable, plugin-supplied handle for the report. Required when creating, and usable as the handle for later updates and attachments.   |
| `patient_id`     | `str` or `None`             | ID of the patient the report belongs to. Required when creating.                                                                      |
| `report_name`    | `str` or `None`             | A name for the report. Maps to the report's custom document name.                                                                     |
| `date_performed` | `datetime` or `None`        | When the report was performed.                                                                                                        |

## Methods

The examples below share this setup:

```python
import datetime

from canvas_sdk.effects.lab_report import LabReport
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.first()
```

### create() → Effect

Create a new lab report. The report stands on its own, decoupled from any lab order, results, or PDF; attach results separately with [`LabReportAttachResults`](#labreportattachresults).

- **Effect Type:** `CREATE_LAB_REPORT`

#### Validation

- `report_id` must **not** be set (creation assigns it).
- `patient_id` is **required**.
- `external_id` is **required**. It is the stable handle your plugin uses to attach results to this report later.

#### Example

```python?partial=True
report = LabReport(
    patient_id=patient.id,
    external_id="myplugin:ocr-2026-06-17-44",
    report_name="CBC scanned 2026-06-17",
    date_performed=datetime.datetime(2026, 6, 17, 8, 15, 0),
)

effect_create = report.create()
```

### update() → Effect

Update a report's metadata, such as renaming it through `report_name`.

- **Effect Type:** `UPDATE_LAB_REPORT`
- Only modified fields are included in the update.

#### Validation

- A handle is **required**: supply either `report_id` or `external_id`, and it must reference an existing report.
- At least one of `report_name` or `date_performed` must be set.

#### Example

```python?partial=True
renamed = LabReport(
    external_id="myplugin:ocr-2026-06-17-44",
    report_name="Complete Blood Count",
)

effect_update = renamed.update()
```

### enter_in_error() → Effect

Mark a report as entered in error. Use this when a report was created incorrectly and should be voided rather than deleted. Entering a report in error also cascades to the linked FHIR `DiagnosticReport` and `DocumentReference`.

- **Effect Type:** `ENTER_IN_ERROR_LAB_REPORT`
- Only a handle is honored; setting any other field raises a validation error.

#### Validation

- A handle is **required**: supply either `report_id` or `external_id`, and it must reference an existing report.
- No other fields may be set (only a handle is allowed).

#### Example

```python?partial=True
voided = LabReport(external_id="myplugin:ocr-2026-06-17-44")

effect_error = voided.enter_in_error()
```

## LabReportAttachResults

The `LabReportAttachResults` effect attaches lab tests and their values to an existing report. This is the second half of the asynchronous OCR pattern — the report is created first with [`create()`](#create--effect), and the extracted results are attached once they're available.

Attachment is **additive**: each call appends the supplied values to the report without removing any existing values.

### Attributes

| Name          | Type              | Description                                                                                       |
|---------------|-------------------|---------------------------------------------------------------------------------------------------|
| `report_id`   | `str`             | The report's Canvas externally-exposable id. Defaults to an empty string.                         |
| `external_id` | `str`             | The plugin-supplied handle for the report. Defaults to an empty string.                           |
| `lab_values`  | `list[LabValue]`  | The lab values to attach. See [`LabValue`](#labvalue).                                            |

#### Validation

- Exactly one of `report_id` or `external_id` is **required** to identify the report.
- At least one `LabValue` is **required**.

### LabValue

A single lab value, and its implied test, to attach to a report.

| Name                 | Type   | Description                                                          |
|----------------------|--------|----------------------------------------------------------------------|
| `ontology_test_code` | `str`  | The code identifying the test. **Required.**                         |
| `value`              | `str`  | The result value. **Required.**                                      |
| `ontology_test_name` | `str`  | Human-readable name of the test. Defaults to an empty string.        |
| `units`              | `str`  | Unit of measure for the value. Defaults to an empty string.          |
| `reference_range`    | `str`  | Reference range for the value. Defaults to an empty string.          |
| `abnormal_flag`      | `str`  | Flag indicating an abnormal result. Defaults to an empty string.     |
| `observation_status` | `str`  | Status of the observation. Defaults to `"final"`.                    |
| `comment`            | `str`  | A free-text comment on the value. Defaults to an empty string.       |

### Example

```python?partial=True
from canvas_sdk.effects.lab_report import LabReportAttachResults, LabValue

attach = LabReportAttachResults(
    external_id="myplugin:ocr-2026-06-17-44",
    lab_values=[
        LabValue(
            ontology_test_code="718-7",
            ontology_test_name="Hemoglobin",
            value="14.2",
            units="g/dL",
            reference_range="13.5-17.5",
        ),
    ],
)

effect_attach = attach.apply()
```

<br/>
<br/>
<br/>
