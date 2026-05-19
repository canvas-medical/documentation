---
title: "Coverage"
slug: "effect-coverage"
excerpt: "Create, update, expire, remove, reorder, and remove photos from patient insurance coverages."
hidden: false
---

The `Coverage` effects let a plugin manage a patient's insurance coverages — create new coverages, update existing ones, expire or remove a coverage, reorder the rank of a patient's coverages, and remove a previously uploaded card photo. Card images are attached via S3 keys returned from a SimpleAPI endpoint declared with `upload_files=True`; the platform performs a server-side copy into the coverage's canonical image location, so no file bytes pass through your plugin.

Coverage write effects mirror the existing GraphQL `CreateCoverage` / `UpdateCoverage` / `OrderCoverage` / `ExpireCoverage` / `RemoveCoverage` / `RemoveCoveragePhoto` mutations one-for-one. They are the recommended write path for coverage from a plugin — prefer them over Canvas's FHIR `Coverage` endpoints when you have the choice, as the FHIR endpoints don't support card-image attachment.

## Common Attributes

These attributes are shared across the create / update effects. Required-ness depends on which effect is being applied; see the per-effect sections below.

| Attribute                              | Type             | Description                                                                                       |
|----------------------------------------|------------------|---------------------------------------------------------------------------------------------------|
| `patient_id`                           | `str` or `UUID`  | The patient the coverage is for.                                                                  |
| `coverage_id`                          | `str` or `UUID`  | The coverage being acted on (update / remove / expire / remove-photo).                            |
| `issuer_id`                            | `str` or `UUID`  | `Transactor` (payer) ID.                                                                          |
| `issuer_address_id`                    | `str` or `UUID`  | Payer address ID.                                                                                 |
| `issuer_phone_id`                      | `str` or `UUID`  | Payer phone ID.                                                                                   |
| `subscriber_id`                        | `str` or `UUID`  | Subscriber `Patient` ID. Set equal to `patient_id` when relationship is `SELF`.                   |
| `patient_relationship_to_subscriber`   | `str`            | A `CoverageRelationshipCode` value: `"01"` (Self), `"02"` (Spouse), `"19"` (Child), etc.          |
| `subscriber_identifier`                | `str`            | Subscriber member ID, when different from `id_number`.                                            |
| `coverage_rank`                        | `int`            | 1 = primary, 2 = secondary, 3 = tertiary, 4 = quaternary, 5 = quinary.                            |
| `plan_type`                            | `str`            | `"COMMERCIAL"`, `"WORKERS_COMP"`, `"BCBS"`, `"TRICARE"`, `"MEDICAID"`, `"MEDICARE"`, `"TPA"`, `"MVA"`, `"LIEN"`, `"PIP"`. |
| `coverage_type`                        | `str`            | Free-text coverage sub-type (matches existing `Coverage.coverage_type`).                           |
| `id_number`                            | `str`            | Member / policy number on the card.                                                                |
| `plan`                                 | `str`            | Plan name.                                                                                         |
| `sub_plan`                             | `str`            | Sub-plan name.                                                                                     |
| `group`                                | `str`            | Group number.                                                                                      |
| `sub_group`                            | `str`            | Sub-group number.                                                                                  |
| `employer`                             | `str`            | Employer name.                                                                                     |
| `coverage_start_date`                  | `date`           | Effective date.                                                                                    |
| `coverage_end_date`                    | `date`           | End date.                                                                                          |
| `comments`                             | `str`            | Free-text notes.                                                                                   |
| `card_image_front_upload_key`          | `str`            | S3 key returned from an `upload_files=True` SimpleAPI endpoint, for the front of the card.        |
| `card_image_back_upload_key`           | `str`            | S3 key returned from an `upload_files=True` SimpleAPI endpoint, for the back of the card.         |

## Card image attachment

Card images are not passed as base64 blobs or raw bytes. Instead:

1. The plugin exposes a SimpleAPI route declared with `@api.post("/cards/upload", upload_files=True)`.
2. The browser POSTs `multipart/form-data` with one or two file parts (`front`, `back`).
3. The platform uploads each part to S3 under `plugin-uploads/<plugin_name>/<timestamp>-<uuid>-<filename>` and rewrites the request body to a JSON envelope containing the resulting S3 keys.
4. The plugin returns those keys to the browser.
5. On save, the browser sends the keys back as `card_image_front_upload_key` / `card_image_back_upload_key` on the `Coverage` effect.
6. When the effect is applied, the platform performs a **server-side S3 `CopyObject`** from `plugin-uploads/...` to the canonical coverage-image location, then deletes the source key. No file bytes pass through the plugin or the home-app.

This pattern is the canonical way to attach files to records from a plugin and will be reused by future write effects.

See the [SimpleAPI HTTP documentation](/sdk/handlers-simple-api-http/) for the `upload_files=True` flag and the `UploadedFilePart` request shape.

## Effect Methods

### `.create()`

Create a new `Coverage` for a patient.

**Required:** `patient_id`, `issuer_id`, `coverage_rank`, `plan_type`, `id_number`, `patient_relationship_to_subscriber`.

**Effect Type:** `CREATE_COVERAGE`

```python
from canvas_sdk.effects.coverage import Coverage
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self):
        effect = Coverage(
            patient_id="patient-uuid-here",
            issuer_id="transactor-uuid-here",
            coverage_rank=1,
            plan_type="COMMERCIAL",
            id_number="ABC123456789",
            patient_relationship_to_subscriber="01",   # SELF
            subscriber_id="patient-uuid-here",
            plan="Gold PPO",
            group="GRP-000001",
            employer="Acme Corp",
            card_image_front_upload_key="plugin-uploads/patient_coverage_companion/20260519T184500Z-abc123-front.jpg",
            card_image_back_upload_key="plugin-uploads/patient_coverage_companion/20260519T184500Z-def456-back.jpg",
        )
        return [effect.create()]
```

### `.update()`

Update an existing `Coverage`. Only the fields you set are changed; unset fields are left alone. Image upload keys are processed only when set.

**Required:** `coverage_id`.

**Effect Type:** `UPDATE_COVERAGE`

```python
effect = Coverage(
    coverage_id="coverage-uuid-here",
    card_image_back_upload_key="plugin-uploads/patient_coverage_companion/20260519T184800Z-xyz789-back.jpg",
)
return [effect.update()]
```

### `.expire(coverage_end_date)`

Set the `coverage_end_date`. Mirrors GraphQL `ExpireCoverage`.

**Required:** `coverage_id`, `coverage_end_date`.

**Effect Type:** `EXPIRE_COVERAGE`

```python
import datetime

effect = Coverage(coverage_id="coverage-uuid-here")
return [effect.expire(coverage_end_date=datetime.date(2026, 5, 31))]
```

### `.remove()`

Mark a coverage as removed. The row stays in the database; its `stack` is set to `REMOVED` and an audit-log entry is written. Mirrors GraphQL `RemoveCoverage`.

**Required:** `coverage_id`.

**Effect Type:** `REMOVE_COVERAGE`

```python
effect = Coverage(coverage_id="coverage-uuid-here")
return [effect.remove()]
```

### `.remove_photo(side)`

Clear the front or back card image on a coverage. Mirrors GraphQL `RemoveCoveragePhoto`.

**Required:** `coverage_id`, `side`.

`side` is one of `"FRONT"` or `"BACK"`.

**Effect Type:** `REMOVE_COVERAGE_PHOTO`

```python
effect = Coverage(coverage_id="coverage-uuid-here")
return [effect.remove_photo(side="BACK")]
```

### `CoverageReorder.apply()`

Reorder the ranks of all of a patient's coverages in one effect. Useful when a new primary is added and existing coverages need to slot down. Mirrors GraphQL `OrderCoverage`.

**Effect Type:** `REORDER_COVERAGE`

```python
from canvas_sdk.effects.coverage import CoverageReorder

effect = CoverageReorder(
    patient_id="patient-uuid-here",
    ordering=[
        {"coverage_id": "new-primary-uuid", "coverage_rank": 1, "stack": "IN_USE"},
        {"coverage_id": "old-primary-uuid", "coverage_rank": 2, "stack": "IN_USE"},
        {"coverage_id": "old-secondary-uuid", "coverage_rank": 3, "stack": "IN_USE"},
    ],
)
return [effect.apply()]
```

## Validation

The effects validate:

- **Create**: `patient_id`, `issuer_id`, `coverage_rank`, `plan_type`, `id_number`, and `patient_relationship_to_subscriber` are required and must reference existing records where applicable.
- **Create**: No other coverage may exist with the same `(patient_id, coverage_rank, stack=IN_USE)` combination.
- **Create**: When `patient_relationship_to_subscriber` is `"01"` (SELF), the platform sets `subscriber_id = patient_id` automatically; if you pass a different value, the create is rejected.
- **Update**: `coverage_id` is required and must reference an existing coverage.
- **Expire**: `coverage_id` and `coverage_end_date` are required.
- **Remove**: `coverage_id` is required.
- **Remove Photo**: `coverage_id` is required; `side` must be `"FRONT"` or `"BACK"`.
- **Reorder**: every `coverage_id` in `ordering` must belong to the named `patient_id`, ranks within a stack must be unique, and ranks must be consecutive starting at 1.
- **Authorization**: the platform enforces `ModelPermissions` (`add` / `change` / `delete` as appropriate) plus `ParentPatientObjectPermissions` for the patient. A plugin's `StaffSessionAuthMixin` is not, by itself, sufficient.
- **Card image keys**: must be S3 keys returned from the same plugin's `upload_files=True` route. Keys from other plugins or arbitrary keys are rejected.

## Eligibility checks

After a successful create or update, the platform calls `Coverage.verify_eligibility()` against the configured clearinghouse, exactly matching the existing GraphQL behavior. Failures are suppressed and do not roll back the effect; the `EligibilitySummary` is upserted on success.

## Example: full create with card upload

This snippet shows the two-step flow from a SimpleAPI handler — first the browser POSTs the card images, then it POSTs the coverage form fields with the returned keys.

```python
from http import HTTPStatus

from canvas_sdk.effects.coverage import Coverage
from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.handlers.simple_api import SimpleAPI, StaffSessionAuthMixin, api


class CoverageAPI(StaffSessionAuthMixin, SimpleAPI):
    PREFIX = "/app"

    @api.post("/cards/upload", upload_files=True)
    def upload(self):
        # request.form_data() yields UploadedFilePart instances with .key set
        parts = {p.name: p.key for p in self.request.form_data()}
        return [JSONResponse(
            {"front_key": parts.get("front"), "back_key": parts.get("back")},
            status_code=HTTPStatus.OK,
        )]

    @api.post("/coverage")
    def create_coverage(self):
        body = self.request.json() or {}
        effect = Coverage(
            patient_id=body["patient_id"],
            issuer_id=body["issuer_id"],
            coverage_rank=int(body["coverage_rank"]),
            plan_type=body["plan_type"],
            id_number=body["id_number"],
            patient_relationship_to_subscriber=body["relationship"],
            subscriber_id=body.get("subscriber_id") or body["patient_id"],
            plan=body.get("plan"),
            group=body.get("group"),
            coverage_start_date=body.get("coverage_start_date"),
            card_image_front_upload_key=body.get("front_key"),
            card_image_back_upload_key=body.get("back_key"),
        )
        return [
            effect.create(),
            JSONResponse({"status": "submitted"}, status_code=HTTPStatus.ACCEPTED),
        ]
```

As with other create effects, the coverage is materialized after the handler returns — see [Async effects from SimpleAPI handlers](/sdk/companion/#async-effects-from-simpleapi-handlers) for the lookup-after-create pattern when you need the new coverage ID.

## Notes

- Coverage image attachment is the first effect to consume the `upload_files=True` SimpleAPI surface; the same pattern will be used by future file-attaching effects.
- The platform does not generate or send a fax / printout of the coverage; that's an existing chart workflow and not modeled here.
- `OrderCoverage` style reordering is performed across the entire stack at once via `CoverageReorder.apply()`. Updating one coverage's rank in isolation via `.update()` will be rejected if it leaves another coverage at the same rank.
- The legacy `Coverage.card_image_front` / `card_image_back` FileFields are not written by these effects; images flow exclusively through `Snapshot` / `SnapshotImage` to match the canonical read path used by the chart UI, claims, and FHIR export.
