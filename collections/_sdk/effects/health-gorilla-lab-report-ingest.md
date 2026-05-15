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

The home-app interpreter is equivalent to what
`LabEngineInboundService.process_and_store_report` does for HG-pull
ingest, minus the HG fetch — the partner provides the PDF and Canvas
stores it through the existing S3 + `ElectronicLabIntegrationTask` path.

## Dedup

Reports are deduped server-side on `(external_id, version)`:

| State                                              | Result                                                  |
| -------------------------------------------------- | ------------------------------------------------------- |
| New `external_id`                                  | Create new `LabReport`.                                 |
| Same `external_id`, higher `version`               | Replace values, bump version on existing record, re-store PDF. |
| Same `external_id`, same or lower `version`        | No-op; existing record kept, no PDF fetch.              |

This matches the version-bump contract in
`LabEngineInboundService.process_and_store_report`, so partners can
safely replay events.

## PDF handling

Exactly one of `pdf_url` or `pdf_base64` must be set. The home-app
interpreter fetches the PDF (or decodes the inline base64) **outside**
the `LabReport` transaction so a slow partner bucket cannot hold row
locks. Limits:

- `pdf_base64` capped at 1 MB encoded (~750 KB binary). Use `pdf_url`
  for larger PDFs.
- `pdf_url` fetch capped at 10 MB.

## Attributes

| Attribute        | Type           | Required | Description                                                                                                                     |
| ---------------- | -------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------- |
| lab_order_id     | str            | yes      | Canvas LabOrder `externally_exposable_id` (uuid) the report belongs to.                                                          |
| patient_id       | str            | yes      | Canvas Patient `key` (uuid).                                                                                                     |
| external_id      | str            | yes      | Partner-side report id. Used for dedup.                                                                                          |
| version          | int            | yes      | Report version, monotonically increasing per `external_id`. Must be `>= 1`.                                                      |
| status           | str            | no       | Report status; defaults to `"final"`.                                                                                            |
| date_performed   | datetime       | yes      | When the report was generated on the partner side.                                                                               |
| lab_values       | list[dict]     | yes      | Per-test results. Each entry: `ontology_test_code`, `ontology_test_name`, `value`, `units`, `reference_range`, `abnormal_flag`, `observation_status`, `comment`. |
| pdf_url          | str            | one of   | URL the home-app interpreter can GET the PDF from (typically a partner's presigned URL).                                          |
| pdf_base64       | str            | one of   | PDF bytes inline as base64. Use only for small PDFs.                                                                              |

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
