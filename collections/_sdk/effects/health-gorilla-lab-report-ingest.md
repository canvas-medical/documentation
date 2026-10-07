---
title: "Health Gorilla Lab Report Ingest"
slug: "effect-health-gorilla-lab-report-ingest"
excerpt: "Push a lab report received outside Canvas (e.g. on a partner's HG tenant) into Canvas with PDF attachment and dedup."
hidden: true
---

The `HealthGorillaLabReportIngest` effect creates a Canvas `LabReport`
plus its `LabValue` rows and attaches a PDF for a result that was
received outside Canvas — for example, by a partner on its own Health
Gorilla tenant or any upstream lab interface. It is the inbound
counterpart to [`HealthGorillaLabOrderIngest`](/sdk/effects/).

Canvas's ingest path is equivalent to a standard Health Gorilla pull, minus the HG fetch — the partner provides the PDF and Canvas stores it through the existing inbound-lab pipeline.

Build a `HealthGorillaLabReportIngest` with the [attributes](#attributes) you want to set, then return its `apply()` from your handler.

## Methods

### apply() → Effect

Creates or updates the lab report, as described under [Dedup](#dedup) and [PDF handling](#pdf-handling).

- `lab_order_id`, `patient_id`, `external_id`, `version`, `date_performed`, and `lab_values` are required, and `version` must be at least 1.
- The patient and lab order must exist.
- Set at most one of `pdf_url` or `pdf_base64`.

## Dedup

Reports are deduped server-side on `(external_id, version)`:

| State                                              | Result                                                  |
| -------------------------------------------------- | ------------------------------------------------------- |
| New `external_id`                                  | Create new `LabReport`.                                 |
| Same `external_id`, higher `version`               | Replace values, bump version on existing record, re-store PDF. |
| Same `external_id`, same or lower `version`        | No-op; existing record kept, no PDF fetch.              |

This matches Canvas's standard inbound-lab version-bump contract, so partners can safely replay events.

## PDF handling

Set at most one of `pdf_url` or `pdf_base64`; setting both is an error. Canvas fetches the PDF (or decodes the inline base64) **outside** the `LabReport` transaction so a slow partner bucket cannot hold row locks. Limits:

- `pdf_base64` capped at 1 MB encoded (~750 KB binary). Use `pdf_url`
  for larger PDFs.
- `pdf_url` fetch capped at 10 MB.

## Attributes

| Attribute        | Type         | Description                                                                                                                     | Required |
| ---------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `lab_order_id`   | `str`        | The id of the [lab order](/sdk/data-labs/) the report belongs to.                                                               | Yes      |
| `patient_id`     | `str`        | The id of the [patient](/sdk/data-patient/).                                                                                    | Yes      |
| `external_id`    | `str`        | Partner-side report id. Used for dedup.                                                                                         | Yes      |
| `version`        | `int`        | Report version, monotonically increasing per `external_id`. Must be `>= 1`.                                                     | Yes      |
| `status`         | `str`        | Report status; defaults to `"final"`.                                                                                           | No       |
| `date_performed` | `datetime`   | When the report was generated on the partner side.                                                                              | Yes      |
| `lab_values`     | `list[dict]` | Per-test results. Each entry: `ontology_test_code`, `ontology_test_name`, `value`, `units`, `reference_range`, `abnormal_flag`, `observation_status`, `comment`. | Yes      |
| `pdf_url`        | `str`        | URL Canvas will GET the PDF from (typically a partner's presigned URL).                                                         | No       |
| `pdf_base64`     | `str`        | PDF bytes inline as base64. Use only for small PDFs.                                                                            | No       |
## Example

```python
from datetime import datetime, UTC

from canvas_sdk.effects.lab_order import HealthGorillaLabReportIngest
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class ExternalLabReportsAPI(SimpleAPIRoute):
    PATH = "/external-lab-reports"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        return credentials.key == self.secrets["ingest-api-key"]

    def post(self) -> list[Response]:
        body = self.request.json()
        return [
            HealthGorillaLabReportIngest(
                lab_order_id=body["lab_order_id"],
                patient_id=body["patient_id"],
                external_id=body["external_id"],
                version=body.get("version", 1),
                date_performed=datetime.fromisoformat(body["date_performed"]),
                lab_values=body["lab_values"],
                pdf_url=body["pdf_url"],
            ).apply(),
            JSONResponse(
                {"external_id": body["external_id"], "version": body.get("version", 1)},
                status_code=202,
            ),
        ]
```

## Related

- [`HealthGorillaLabOrderIngest`](/sdk/effects/) — the matching effect for inbound lab orders
