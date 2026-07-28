---
title: "Lab Report Effect"
slug: "effect-lab-report"
excerpt: "Create, update, or enter-in-error a lab report, and attach results to it after the fact."
hidden: false
---

The `LabReport` effect creates and manages a [lab report](/sdk/data-labs/#labreport) directly from a plugin, independent of any lab order, results, or PDF. It's built for the asynchronous OCR pattern: create the report now with a plugin-supplied handle, then attach the extracted results later with [`attach_results()`](#attachresults--effect) once they're available.

`create()` produces an uncommitted draft report; the first `attach_results()` call commits it, so creating a report does not itself file or finalize it. Once committed, the report enters Canvas's normal inbound lab-review workflow. It is created with review required and a signature needed, so a clinician still reviews and signs it after commit.

A report is identified by one of two handles:

- `reference_id` — a stable, plugin-supplied handle your plugin controls (maximum 40 characters). Use it to identify the report at any point in its lifecycle — before the Canvas `report_id` exists, and afterward if you prefer it over `report_id`.
- `report_id` — the report's Canvas externally-exposable id. Becomes available once the report is created, and can be recovered from the `LAB_REPORT_CREATED` event or a [`LabReport`](/sdk/data-labs/#labreport) data query.

## Attributes

| Name             | Type                        | Description                                                                                                                            |
|------------------|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `report_id`      | `UUID` or `None`            | The report's Canvas externally-exposable id (a UUID string is also accepted). Must be unset when creating; used as the handle for `update()`, `enter_in_error()`, and `attach_results()` once known. |
| `reference_id`   | `str` or `None`             | A stable, plugin-supplied handle for the report (maximum 40 characters). Required when creating; usable as the handle for later updates, entering in error, and attaching results. |
| `patient_id`     | `str` or `None`             | ID of the patient the report belongs to. Required when creating.                                                                      |
| `report_name`    | `str` or `None`             | A name for the report. Maps to the report's custom document name.                                                                     |
| `date_performed` | `datetime` or `None`        | When the report was performed.                                                                                                        |

## Helper Classes

### `LabTest`

Groups one or more lab values under an order/compendium-coded test.

| Name                 | Type                          | Description                                                                                       |
|----------------------|-------------------------------|---------------------------------------------------------------------------------------------------|
| `ontology_test_code` | `str`                         | The order/compendium test code (not a LOINC code). Defaults to an empty string.                   |
| `ontology_test_name` | `str`                         | Human-readable test name. Defaults to an empty string.                                            |
| `codings`            | `list[CodingData]` or `None`  | Standardized codings for the test; put LOINC codings here. Defaults to `None`.                    |
| `values`             | `list[LabValue]`              | The values for this test. At least one is required. See [`LabValue`](#labvalue).                  |

### `LabValue`

A single result value within a test.

| Name                 | Type                          | Description                                                                                       |
|----------------------|-------------------------------|---------------------------------------------------------------------------------------------------|
| `value`              | `str`                         | The result value. Required.                                                                       |
| `units`              | `str`                         | Unit of measure. Defaults to an empty string.                                                     |
| `reference_range`    | `str`                         | Reference range. Defaults to an empty string.                                                     |
| `abnormal_flag`      | `AbnormalFlag` or `None`      | Abnormal-result flag. Defaults to `None`. See [`AbnormalFlag`](#abnormalflag).                    |
| `observation_status` | `ObservationStatus`           | Status of the observation. Defaults to `ObservationStatus.FINAL`. See [`ObservationStatus`](#observationstatus). |
| `comment`            | `str`                         | Free-text comment. Defaults to an empty string.                                                   |
| `codings`            | `list[CodingData]` or `None`  | Standardized codings for this value; put LOINC codings here. Defaults to `None`.                  |

### `AbnormalFlag`

A `StrEnum` of abnormal-result flags (HL7 v2 table 0078).

| Member                | Value    |
|-----------------------|----------|
| `HIGH`                | `H`      |
| `LOW`                 | `L`      |
| `CRITICAL_HIGH`       | `HH`     |
| `CRITICAL_LOW`        | `LL`     |
| `BELOW_ABSOLUTE_LOW`  | `<`      |
| `ABOVE_ABSOLUTE_HIGH` | `>`      |
| `ABNORMAL`            | `A`      |
| `CRITICAL_ABNORMAL`   | `AA`     |
| `SUSCEPTIBLE`         | `S`      |
| `RESISTANT`           | `R`      |
| `INTERMEDIATE`        | `I`      |
| `NEGATIVE`            | `NEG`    |
| `POSITIVE`            | `POS`    |

### `ObservationStatus`

A `StrEnum` of FHIR observation statuses.

| Member              | Value              |
|---------------------|--------------------|
| `AMENDED`           | `amended`          |
| `CANCELLED`         | `cancelled`        |
| `CORRECTED`         | `corrected`        |
| `ENTERED_IN_ERROR`  | `entered-in-error` |
| `FINAL`             | `final`            |
| `PRELIMINARY`       | `preliminary`      |
| `REGISTERED`        | `registered`       |
| `UNKNOWN`           | `unknown`          |

### `CodingData`

Imported from `canvas_sdk.effects.observation.base` and reused from the Observation effect — see [`CodingData`](/sdk/effect-observation/#codingdata) for the canonical reference.

| Name | Type | Description |
|---|---|---|
| `code` | `str` | The code value from the terminology system. |
| `display` | `str` | Human-readable display text for the code. |
| `system` | `str` | URI identifying the terminology system (e.g. `http://loinc.org`). |
| `version` | `str` | Version of the terminology system. Defaults to an empty string. |
| `user_selected` | `bool` | Whether this code was explicitly selected by the user. Defaults to `False`. |

Only codings whose `system` is LOINC are persisted server-side (into `OntologyLabTestLoincCode` for a test and `OntologyLabTestValueLoincCode` for a value).

## Methods

The examples below share this setup:

```python
import datetime

from canvas_sdk.effects.lab_report import LabReport, LabTest, LabValue, AbnormalFlag, ObservationStatus
from canvas_sdk.effects.observation.base import CodingData
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.first()
```

### create() → Effect

Create a new lab report. The report stands on its own, decoupled from any lab order, results, or PDF; attach results separately with [`attach_results()`](#attachresults--effect).

- **Effect Type:** `CREATE_LAB_REPORT`
- **Payload:** `{ "data": { patient_id, reference_id, report_name, date_performed } }`

#### Validation

- `report_id` must **not** be set (creation assigns it).
- `patient_id` is **required**.
- `reference_id` is **required**. It is the stable handle your plugin uses to attach results to this report later.
- `reference_id` must be **unique**. The platform rejects a `create()` whose `reference_id` already matches an existing report.

#### Example

```python?partial=True
report = LabReport(
    patient_id=patient.id,
    reference_id="myplugin:ocr-2026-06-17-44",
    report_name="CBC scanned 2026-06-17",
    date_performed=datetime.datetime(2026, 6, 17, 8, 15, 0),
)

effect_create = report.create()
```

### update() → Effect

Update a report's metadata, such as renaming it through `report_name`.

- **Effect Type:** `UPDATE_LAB_REPORT`
- **Payload:** `{ "data": { <handle>, <modified fields> } }`
- Only modified fields are included in the update.

#### Validation

- A handle is **required**: supply either `report_id` or `reference_id`.
- At least one of `report_name` or `date_performed` must be set.
- The platform rejects `update()` once the report is locked (under provider review, entered in error, or junked).

`update()` does not verify the report exists, so you can chain `create()` then `update()` in the same batch of returned effects.

#### Example

```python?partial=True
renamed = LabReport(
    reference_id="myplugin:ocr-2026-06-17-44",
    report_name="Complete Blood Count",
)

effect_update = renamed.update()
```

### enter_in_error() → Effect

Mark a report as entered in error. Use this when a report was created incorrectly and should be voided rather than deleted.

- **Effect Type:** `ENTER_IN_ERROR_LAB_REPORT`
- **Payload:** `{ "data": { <handle> } }`
- Only the handle is sent; any other field set on the instance is ignored (not an error).

#### Validation

- A handle is **required**: supply either `report_id` or `reference_id`.
- The platform rejects `enter_in_error()` once the report is locked (under provider review, entered in error, or junked).

#### Example

```python?partial=True
voided = LabReport(report_id="d2194110-5c9a-4842-8733-ef09ea5ead11")

effect_error = voided.enter_in_error()
```

### attach_results() → Effect

Attach lab tests and their values to an existing report: `attach_results(lab_tests: list[LabTest]) → Effect`. This is the second half of the asynchronous OCR pattern — the report is created first with [`create()`](#create--effect), and the extracted results are attached once they're available.

Attachment is **additive**: each call appends the supplied tests and values without removing any existing ones.

The platform rejects `update()`, `enter_in_error()`, and `attach_results()` once the report is locked — that is, once it is under provider review, entered in error, or junked. Being committed alone is not a lock: a committed report that is not yet under provider review can still be updated and have more results attached.

- **Effect Type:** `ATTACH_LAB_REPORT_RESULTS`
- **Payload:** `{ "data": { <handle>, "lab_tests": [ ... ] } }`

#### Validation

- Exactly one of `report_id` or `reference_id` is **required** to identify the report (setting both is rejected as ambiguous).
- At least one `LabTest` is **required**.
- Each `LabTest` requires at least one `LabValue`.
- The platform rejects the call once the report is locked (under provider review, entered in error, or junked).

#### Example

```python?partial=True
report = LabReport(reference_id="myplugin:ocr-2026-06-17-44")

effect_attach = report.attach_results([
    LabTest(
        ontology_test_code="CBC",
        ontology_test_name="Complete Blood Count",
        codings=[CodingData(code="58410-2", display="CBC panel - Blood by Automated count", system="http://loinc.org")],
        values=[
            LabValue(
                value="14.2",
                units="g/dL",
                reference_range="13.5-17.5",
                abnormal_flag=AbnormalFlag.HIGH,
                observation_status=ObservationStatus.FINAL,
                codings=[
                    CodingData(code="718-7", display="Hemoglobin", system="http://loinc.org"),
                ],
            ),
        ],
    ),
])
```

<br/>
<br/>
<br/>
