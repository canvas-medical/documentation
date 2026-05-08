---
title: "Health Gorilla Lab Order Ingest"
slug: "effect-health-gorilla-lab-order-ingest"
excerpt: "Push a lab order originated outside Canvas (e.g. on a partner's HG tenant) into Canvas without re-sending to Health Gorilla."
hidden: true
---

The `HealthGorillaLabOrderIngest` effect creates a Canvas `LabOrder` plus
its `LabTest` rows for an order that was placed outside Canvas — for
example, by a partner on its own Health Gorilla tenant. Canvas records
the order so it shows up in the chart, but the order's `hg_request_result`
field is set to a partner-supplied skip-send marker so Canvas's
send-to-Health-Gorilla worker treats the order as already-sent and never
forwards it.

Typical use is from a SimpleAPI route the partner POSTs to when they place
a standing or recurring order on their side.

## Behavior

The effect targets the home-app `HealthGorillaLabOrderIngest` interpreter,
which in a single transaction:

1. Resolves `Patient` (by `key`), `Staff` (by NPI), and `Note` (by external id).
2. Creates a `LabOrder` with `hg_request_result` set non-empty so the
   send-to-HG worker leaves it alone.
3. Creates one `LabTest` row per HG order code in `test_codes`. Test names
   are filled from the HG ontology when available.

Each `LabTest` is created with status `RECEIVED`, since externally-originated
orders are past the Canvas send pipeline.

## Attributes

| Attribute                | Type        | Required | Description                                                                                          |
| ------------------------ | ----------- | -------- | ---------------------------------------------------------------------------------------------------- |
| patient_id               | str         | yes      | Canvas Patient `key` (uuid).                                                                         |
| ordering_provider_npi    | str         | yes      | NPI used to look up the Staff record.                                                                |
| note_id                  | str         | yes      | Canvas Note `externally_exposable_id` (uuid). LabOrders require a Note FK in home-app.               |
| ontology_lab_partner     | str         | yes      | Ontology lab partner name (e.g. `"Quest Diagnostics"`, `"LabCorp"`).                                 |
| date_ordered             | datetime    | yes      | When the order was authored on the partner side.                                                     |
| hg_request_result        | str         | yes      | Skip-send marker. Convention is the partner's HG `RequestGroup` URL or id so Canvas can correlate later. Any non-empty value works. |
| test_codes               | list[str]   | yes      | One or more HG order codes. One `LabTest` row is created per entry.                                  |
| external_id              | str         | no       | Stored on `LabOrder.healthgorilla_id`; useful for partner-side dedup.                                |
| comment                  | str         | no       | Stored on `LabOrder.comment`.                                                                        |

## Example

```python
from datetime import datetime, UTC

from canvas_sdk.effects.lab_order import HealthGorillaLabOrderIngest
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class StandingLabOrdersAPI(SimpleAPIRoute):
    PATH = "/standing-lab-orders"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        return credentials.key == self.secrets["ingest-api-key"]

    def post(self) -> list[Response]:
        body = self.request.json()
        return [
            HealthGorillaLabOrderIngest(
                patient_id=body["patient_id"],
                ordering_provider_npi=body["ordering_provider_npi"],
                note_id=body["note_id"],
                ontology_lab_partner=body["ontology_lab_partner"],
                date_ordered=datetime.fromisoformat(body["date_ordered"]),
                hg_request_result=body["hg_request_result"],
                test_codes=body["test_codes"],
                external_id=body.get("external_id", ""),
            ).apply(),
            JSONResponse({"external_id": body["external_id"]}, status_code=201),
        ]
```

## Related

- [`HealthGorillaLabReportIngest`](/sdk/effects/) — the matching effect for inbound lab reports
- [`HealthGorillaLabOrderOverride`](/sdk/effects/) — for orders Canvas itself sends to HG
