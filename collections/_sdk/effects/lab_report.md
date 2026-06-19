---
title: "Lab Report Effect"
slug: "effect-lab-report"
excerpt: "Create lab reports decoupled from their results, attach results later, rename, and enter-in-error."
hidden: true
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

## Identifying a report

Every effect references a report by one of two handles:

| Handle        | What it is                                      | When to use it                                          |
| ------------- |-------------------------------------------------|---------------------------------------------------------|
| `external_id` | A stable identifier when a report is created.   | The report your plugin created. Required on `create()`. |
| `report_id`   | The report's Canvas `externally_exposable_id`.  | Any report — including ones your plugin didn't create.  |

Effects are fire-and-forget, so `create()` does not return the new report's `report_id`. Use the
`external_id` you assigned as your handle for the later `attach`/`update`/`enter_in_error` calls.
If you need the Canvas `report_id` (for example to act on a report your plugin did not create),
read it from the `LAB_REPORT_CREATED` event or query the `LabReport` data model by `external_id`.

Namespace your `external_id` values (e.g. `"my-plugin:batch-2026-06-17:img-44"`) so they don't
collide with report ids from other inbound-lab sources.

## Attributes

| Name             | Type                          | Description                                                                                                      |
| ---------------- | ----------------------------- |------------------------------------------------------------------------------------------------------------------|
| `external_id`    | `str` or `None`               | The plugin-assigned handle. **Required** when creating; usable as the handle for other operations.               |
| `report_id`      | `UUID` or `None`              | The report's Canvas `externally_exposable_id` (a valid uuid string is also accepted). Must be **unset** when creating; an alternative handle otherwise. |
| `patient_id`     | `str` or `None`               | The patient's `key`. **Required** when creating.                                                                 |
| `report_name`    | `str` or `None`               | Human-readable report name (maps to the report's document name).                                                 |
| `date_performed` | `datetime` or `None`          | The report's effective/displayed date (also sets `original_date` server-side).                                   |

## Methods

The examples below share this setup:

```python
import datetime

from canvas_sdk.effects.lab_report import LabReport, LabValue
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.first()
```

### create() → Effect

Create a lab report decoupled from its results — no order, no PDF, and no values required.

- **Effect Type:** `CREATE_LAB_REPORT`
- **Payload:** `{ "data": { external_id, patient_id, report_name, date_performed } }`

#### Validation

- `external_id` is **required** (it is your handle for attaching results later).
- `patient_id` is **required**.
- `report_id` must **not** be set (creation assigns the Canvas id).
- The `external_id` must not already be in use by an existing report.

#### Example

```python?partial=True
report = LabReport(
    external_id="my-plugin:batch-2026-06-17:img-44",
    patient_id=patient.id,
    report_name="CBC (scanned 2026-06-17)",
    date_performed=datetime.datetime.now(),
)

effect_create = report.create()
```

### update() → Effect

Update report metadata, such as renaming it via `report_name`. Only the fields you set are sent.

- **Effect Type:** `UPDATE_LAB_REPORT`
- **Payload:** `{ "data": { <handle>, <dirty_fields> } }`

#### Validation

- Exactly one handle (`external_id` or `report_id`) is **required**.
- At least one mutable field (`report_name` or `date_performed`) must be provided.
- The report must not be entered-in-error.

#### Example

```python?partial=True
renamed = LabReport(
    external_id="my-plugin:batch-2026-06-17:img-44",
    report_name="Complete Blood Count",
)

effect_update = renamed.update()
```

### enter_in_error() → Effect

Mark a report as entered-in-error. Use this when a report was filed incorrectly and should be
flagged rather than left in place.

- **Effect Type:** `ENTER_IN_ERROR_LAB_REPORT`
- **Payload:** `{ "data": { <handle> } }`
- Only the handle is sent; any other field on the instance is ignored.

#### Validation

- A handle (`external_id` or `report_id`) is **required**.
- Any other field is ignored (not rejected).
- The report must not already be entered-in-error.

#### Example

```python?partial=True
voided = LabReport(external_id="my-plugin:batch-2026-06-17:img-44")

effect_error = voided.enter_in_error()
```

## Attaching results

Once results are available, attach them with the `attach_results` method on `LabReport`. The report
handle comes from the `LabReport` instance (`report_id` or `external_id`); the method takes the list
of `LabValue`s. Attaching is **additive** — it appends tests and values without removing any already
on the report.

- **Effect Type:** `ATTACH_LAB_REPORT_RESULTS`
- **Payload:** `{ "data": { report_id, external_id, lab_values } }`

### Arguments

| Name         | Type             | Description                                                                                           |
| ------------ | ---------------- |-------------------------------------------------------------------------------------------------------|
| `lab_values` | `list[LabValue]` | The results to attach. At least one is required. The report handle comes from the `LabReport` instance. |

### `LabValue`

Each `LabValue` describes one result. Canvas records it as a lab test plus its value on the report.

| Name                 | Type  | Description                                                        |
| -------------------- | ----- | ------------------------------------------------------------------ |
| `ontology_test_code` | `str` | The test's ontology code (e.g. a LOINC code). Required.            |
| `ontology_test_name` | `str` | Human-readable test name. Defaults to empty string.                |
| `value`              | `str` | The result value. Required.                                        |
| `units`              | `str` | Unit of measure (e.g. `"g/dL"`). Defaults to empty string.         |
| `reference_range`    | `str` | Reference range as free text. Defaults to empty string.            |
| `abnormal_flag`      | `str` | Abnormal flag (e.g. `"H"`, `"L"`). Defaults to empty string.       |
| `observation_status` | `ObservationStatus` | FHIR status enum: `final` (default), `preliminary`, `amended`, `corrected`, `cancelled`, `registered`, `unknown`, `entered-in-error`. |
| `comment`            | `str` | Free-text comment. Defaults to empty string.                       |

#### Validation

- Exactly one of `external_id` or `report_id` is **required**.
- At least one `LabValue` is **required**.
- The report must exist and must not be junked or entered-in-error.

#### Example

A SimpleAPI route an OCR service calls once it has abstracted the values:

```python
from canvas_sdk.effects.lab_report import LabReport, LabValue
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class LabResultsAPI(SimpleAPIRoute):
    PATH = "/lab-results"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        return credentials.key == self.secrets["ingest-api-key"]

    def post(self) -> list[Response]:
        body = self.request.json()
        return [
            LabReport(external_id=body["external_id"]).attach_results(
                [
                    LabValue(
                        ontology_test_code=value["code"],
                        ontology_test_name=value.get("name", ""),
                        value=value["value"],
                        units=value.get("units", ""),
                        reference_range=value.get("reference_range", ""),
                    )
                    for value in body["values"]
                ]
            ),
            JSONResponse({"external_id": body["external_id"]}, status_code=202),
        ]
```

## Workflow

The four effects compose into the asynchronous OCR workflow:

1. A scanned report arrives. The plugin calls `LabReport(external_id=..., patient_id=..., ...).create()`,
   keying off an `external_id` it controls.
2. Days later, the OCR service finishes. The plugin calls `LabReport(external_id=...).attach_results([...])`
   to attach the abstracted results — the report's observations and FHIR resources populate from there.
3. To fix the report name, the plugin calls `LabReport(external_id=..., report_name=...).update()`.
4. If the report was filed in error, the plugin calls `LabReport(external_id=...).enter_in_error()`.

## Related

- [`Observation`](/sdk/effect-observation/) — create or update individual clinical observations.

<br/>
<br/>
<br/>
