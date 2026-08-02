---
title: "Lab Report Effect"
slug: "effect-lab-report"
excerpt: "Create lab reports decoupled from their results, attach results later, rename, and enter-in-error."
hidden: false
---

The `LabReport` effect lets plugins manage a lab report's full lifecycle, independently of any
lab order. It is designed for workflows where a report exists before its structured results do —
for example, a scanned report that arrives by fax or upload and is OCR'd asynchronously, so the
lab tests and values aren't ready until hours or days after the report is created.

With these effects a plugin can:

- **Create** a report up front, with no order, no PDF, and no results.
- **Attach results** (lab tests and values) to that report later, as they become available.
- **Update** report metadata, such as its name.
- **Enter-in-error** a report so a user can self-correct a mistake.

A created report is linked to the patient you supply. It starts **empty** — until you attach results it
holds no tests or values, so it's a placeholder on the chart. Attaching results fills the report in and
creates the observations behind its values, at which point it reads like any other lab report. It is
**not** a Data Integration document, so it never appears in the Data Integration queue, and Canvas
creates the report's diagnostic report and renders a document from its data automatically.

## Identifying a report

Every effect references a report by one of two handles:

| Handle        | What it is                                                        | When to use it                                          |
| ------------- |-------------------------------------------------------------------|---------------------------------------------------------|
| `reference_id` | A stable identifier your plugin assigns when it creates a report. | The report your plugin created. Required on `create()`. |
| `report_id`   | The [LabReport](/sdk/data-labs/)'s `id`.                          | Any report — including ones your plugin didn't create.  |

Effects are fire-and-forget, so `create()` does not return the new report's `report_id`. Use the
`reference_id` you assigned as your handle for the later `attach`/`update`/`enter_in_error` calls.
If you need the `report_id` (for example to act on a report your plugin did not create), read it
from the `LAB_REPORT_CREATED` event or query the [LabReport](/sdk/data-labs/) data model by
`reference_id` (the handle you assigned is stored there; the data model's own `external_id` is
reserved for electronic/Health-Gorilla feed ids).

Namespace your `reference_id` values (e.g. `"my-plugin:batch-2026-06-17:img-44"`) so they don't
collide with report ids from other inbound-lab sources.

## Attributes

| Name             | Type                 | Description                                                                                                     |
| ---------------- | -------------------- |-----------------------------------------------------------------------------------------------------------------|
| `reference_id`    | `str` or `None`      | The plugin-assigned handle (maximum 40 characters). **Required** when creating; usable as the handle for other operations.              |
| `report_id`      | `UUID` or `None`     | The [LabReport](/sdk/data-labs/)'s `id` (a valid uuid string is also accepted). Must be **unset** when creating; an alternative handle otherwise. |
| `patient_id`     | `str` or `None`      | The [Patient](/sdk/data-patient/)'s `id`. **Required** when creating.                                           |
| `report_name`    | `str` or `None`      | Human-readable report name (maps to the report's document name).                                                |
| `date_performed` | `datetime` or `None` | The report's effective/displayed date. If omitted on `create`, it defaults to the creation time — correct it later via `update`. |

## Methods

### create()

Create a lab report decoupled from its results — no order, no PDF, and no values required.

#### Validation

- `reference_id` is **required** (it is your handle for attaching results later).
- `patient_id` is **required**.
- `report_id` must **not** be set (creation assigns the id).
- The `reference_id` must not already be in use by an existing report.

#### Example

```python?partial=True
import datetime

from canvas_sdk.effects.lab_report import LabReport
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.first()

report = LabReport(
    reference_id="my-plugin:batch-2026-06-17:img-44",
    patient_id=patient.id,
    report_name="CBC (scanned 2026-06-17)",
    date_performed=datetime.datetime.now(),
)

effect = report.create()
```

### update()

Update report metadata, such as renaming it via `report_name`. Only the fields you set are sent. Only `report_name` and `date_performed` can be changed — `update()` **cannot move the report to a different patient**; the patient is fixed when the report is created. If a report was attached to the wrong patient, enter it in error and recreate it on the correct patient.

#### Validation

- Exactly one handle (`reference_id` or `report_id`) is **required**.
- At least one mutable field (`report_name` or `date_performed`) must be provided.
- The report must not already be entered-in-error or reviewed by a provider.

#### Example

```python?partial=True
from canvas_sdk.effects.lab_report import LabReport

renamed = LabReport(
    reference_id="my-plugin:batch-2026-06-17:img-44",
    report_name="Complete Blood Count",
)

effect = renamed.update()
```

### enter_in_error()

Flag a report as entered-in-error — use it when a report was filed incorrectly. It junks the report (removing it from active views) and records who entered it in error. A `post_save` signal cascade then also marks the report's observations and the linked FHIR DiagnosticReport and DocumentReference records as entered-in-error. Once a report is entered-in-error (or junked) it can no longer be modified — `update()` and `attach_results()` on it raise a validation error.

#### Validation

- A handle (`reference_id` or `report_id`) is **required**.
- Any other field is ignored (not rejected).
- The report must not already be entered-in-error or reviewed by a provider.

#### Example

```python?partial=True
from canvas_sdk.effects.lab_report import LabReport

voided = LabReport(reference_id="my-plugin:batch-2026-06-17:img-44")

effect = voided.enter_in_error()
```

## Attaching results

Once results are available, attach them with the `attach_results` method on `LabReport`. The report
handle comes from the `LabReport` instance (`report_id` or `reference_id`); the method takes a list of
`LabTest`s, each grouping the `LabValue`s measured for it — so the values for one test are bundled
under that test in the chart. Attaching is **additive**: it appends tests and values without removing
any already on the report, and Canvas creates an observation for each value automatically.

Attaching results saves the report, which re-runs the FHIR cascade — so the linked DiagnosticReport and the rendered DocumentReference (the report's document) are regenerated to reflect the newly attached values. The first `attach_results()` call also commits the report (a never-populated report stays an uncommitted draft). A committed report enters the lab-review workflow **review-required** and **requiring a signature**, but with **no reviewer assigned** — a clinician still has to pick it up, review, and sign it. Once a provider has reviewed it, the report is locked to further SDK edits.

### Arguments

| Name        | Type            | Description                                                                                            |
| ----------- | --------------- |--------------------------------------------------------------------------------------------------------|
| `lab_tests` | `list[LabTest]` | The tests to attach. At least one is required. The report handle comes from the `LabReport` instance.  |

### `LabTest`

A `LabTest` is a test that was performed — an ordered panel or a single analyte — and it groups its
result values (a result test can carry many values). `ontology_test_code`/`ontology_test_name` are
the lab's **order/compendium** code and name — *not* LOINC. LOINC is supplied separately via `codings`
(see [`CodingData`](#codingdata) below).

| Name                 | Type                         | Description                                                                                        |
| -------------------- | ---------------------------- |----------------------------------------------------------------------------------------------------|
| `ontology_test_code` | `str`                        | The lab's order/compendium code for the test. Defaults to empty string.                            |
| `ontology_test_name` | `str`                        | Human-readable test name. Defaults to empty string.                                                |
| `codings`            | `list[CodingData]` or `None` | The test's LOINC coding(s); only LOINC-system codings are stored.                                  |
| `values`             | `list[LabValue]`             | The result values for this test. **At least one is required.**                                     |

### `LabValue`

Each `LabValue` is one measured result on its test.

| Name                 | Type                         | Description                                                        |
| -------------------- | ---------------------------- | ------------------------------------------------------------------ |
| `value`              | `str`                        | The result value. Required.                                        |
| `units`              | `str`                        | Unit of measure (e.g. `"g/dL"`). Defaults to empty string.         |
| `reference_range`    | `str`                        | Reference range as free text. Defaults to empty string.            |
| `abnormal_flag`      | `AbnormalFlag` or `None`     | Flags the value against its reference range — see [`AbnormalFlag`](#abnormalflag) for all values. Any non-empty flag marks the result abnormal in the lab report. Defaults to `None`. |
| `observation_status` | `ObservationStatus`          | Status enum: `final` (default), `preliminary`, `amended`, `corrected`, `cancelled`, `registered`, `unknown`, `entered-in-error`. |
| `comment`            | `str`                        | Free-text comment. Defaults to empty string.                       |
| `codings`            | `list[CodingData]` or `None` | The value's LOINC coding(s); only LOINC-system codings are stored. |

### `CodingData`

A coding attached to a test or a value, reused from the [`Observation`](/sdk/effect-observation/)
effect. Only codings whose `system` is `http://loinc.org` are persisted, and the `display` becomes
the stored coding name.

| Name            | Type   | Description                                            |
| --------------- | ------ | ------------------------------------------------------ |
| `code`          | `str`  | The LOINC code (e.g. `"718-7"`). Required.             |
| `display`       | `str`  | Human-readable display; stored as the coding's name.   |
| `system`        | `str`  | Coding system URI. Use `"http://loinc.org"`.           |
| `version`       | `str`  | Optional coding-system version. Defaults to empty.     |
| `user_selected` | `bool` | Whether a user selected this coding. Defaults to `False`. |

### `AbnormalFlag`

A `StrEnum` of abnormal-result flags (HL7 v2 table 0078) for a `LabValue`. Setting any of these marks the result abnormal on the lab report.

| Member                | Value |
| --------------------- | ----- |
| `HIGH`                | `H`   |
| `LOW`                 | `L`   |
| `CRITICAL_HIGH`       | `HH`  |
| `CRITICAL_LOW`        | `LL`  |
| `BELOW_ABSOLUTE_LOW`  | `<`   |
| `ABOVE_ABSOLUTE_HIGH` | `>`   |
| `ABNORMAL`            | `A`   |
| `CRITICAL_ABNORMAL`   | `AA`  |
| `SUSCEPTIBLE`         | `S`   |
| `RESISTANT`           | `R`   |
| `INTERMEDIATE`        | `I`   |
| `NEGATIVE`            | `NEG` |
| `POSITIVE`            | `POS` |

#### Validation

- Exactly one of `reference_id` or `report_id` is **required**.
- At least one `LabTest` is **required**, and each `LabTest` requires at least one `LabValue`.
- The report must exist and must not be entered-in-error or reviewed by a provider.

#### Example

A SimpleAPI route an OCR service calls once it has abstracted the values:

```python
from canvas_sdk.effects.lab_report import LabReport, LabTest, LabValue
from canvas_sdk.effects.observation import CodingData
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPIRoute

LOINC = "http://loinc.org"


class LabResultsAPI(APIKeyAuthMixin, SimpleAPIRoute):
    PATH = "/lab-results"

    def post(self) -> list[Response]:
        body = self.request.json()
        return [
            LabReport(reference_id=body["reference_id"]).attach_results(
                [
                    LabTest(
                        ontology_test_code=test.get("order_code", ""),
                        ontology_test_name=test.get("name", ""),
                        codings=(
                            [CodingData(code=test["loinc"], display=test.get("name", ""), system=LOINC)]
                            if test.get("loinc")
                            else None
                        ),
                        values=[
                            LabValue(
                                value=value["value"],
                                units=value.get("units", ""),
                                reference_range=value.get("reference_range", ""),
                                codings=(
                                    [CodingData(code=value["loinc"], display=value.get("name", ""), system=LOINC)]
                                    if value.get("loinc")
                                    else None
                                ),
                            )
                            for value in test["values"]
                        ],
                    )
                    for test in body["tests"]
                ]
            ),
            JSONResponse({"reference_id": body["reference_id"]}, status_code=202),
        ]
```

## Example Workflow

The four effects compose into the asynchronous OCR workflow:

1. A scanned report arrives. The plugin calls `LabReport(reference_id=..., patient_id=..., ...).create()`,
   keying off an `reference_id` it controls.
2. Days later, the OCR service finishes. The plugin calls
   `LabReport(reference_id=...).attach_results([LabTest(..., values=[LabValue(...)])])` to attach the
   abstracted tests and values — the report's observations populate from there.
3. To fix the report name, the plugin calls `LabReport(reference_id=..., report_name=...).update()`.
4. If the report was filed in error, the plugin calls `LabReport(reference_id=...).enter_in_error()`.

## Related

- [`Observation`](/sdk/effect-observation/) — create or update individual clinical observations.

<br/>
<br/>
<br/>
