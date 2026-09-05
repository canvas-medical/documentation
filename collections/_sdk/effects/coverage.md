---
title: "Coverage"
slug: "effect-coverage"
excerpt: "Create, update, expire, remove, reorder, and remove photos from patient insurance coverages."
hidden: false
---

The `Coverage` effects let a plugin manage a patient's insurance coverages — create new coverages, update existing ones, expire or remove a coverage, reorder the rank of a patient's coverages, and remove a previously uploaded card photo. Card images are attached via S3 keys; Canvas performs a server-side copy into the coverage's image storage, so no file bytes pass through your plugin.

## Common Attributes

These attributes are shared across the create / update effects. Required-ness depends on which effect is being applied; see the per-effect sections below.

| Attribute                              | Type             | Description                                                                                       |
|----------------------------------------|------------------|---------------------------------------------------------------------------------------------------|
| `patient_id`                           | `str`            | The patient the coverage is for.                                                                  |
| `coverage_id`                          | `str` or `UUID`  | The coverage being acted on (update / remove / expire / remove-photo).                            |
| `issuer_id`                            | `str` or `UUID`  | Payer ID.                                                                                         |
| `issuer_address_id`                    | `str` or `UUID`  | Payer address ID.                                                                                 |
| `issuer_phone_id`                      | `str` or `UUID`  | Payer phone ID.                                                                                   |
| `subscriber_id`                        | `str`            | Subscriber patient ID. Set equal to `patient_id` when relationship is `SELF`.                     |
| `patient_relationship_to_subscriber`   | `str`            | Two-character relationship code: `"01"` (Self), `"02"` (Spouse), `"19"` (Child), etc.             |
| `subscriber_identifier`                | `str`            | Subscriber member ID, when different from `id_number`.                                            |
| `coverage_rank`                        | `int`            | 1 = primary, 2 = secondary, 3 = tertiary, 4 = quaternary, 5 = quinary.                            |
| `plan_type`                            | `str`            | `"COMMERCIAL"`, `"WORKERS_COMP"`, `"BCBS"`, `"TRICARE"`, `"MEDICAID"`, `"MEDICARE"`, `"TPA"`, `"MVA"`, `"LIEN"`, `"PIP"`. |
| `coverage_type`                        | `str`            | Free-text coverage sub-type.                                                                       |
| `id_number`                            | `str`            | Member / policy number on the card.                                                                |
| `plan`                                 | `str`            | Plan name.                                                                                         |
| `sub_plan`                             | `str`            | Sub-plan name.                                                                                     |
| `group`                                | `str`            | Group number.                                                                                      |
| `sub_group`                            | `str`            | Sub-group number.                                                                                  |
| `employer`                             | `str`            | Employer name.                                                                                     |
| `coverage_start_date`                  | `date`           | Effective date.                                                                                    |
| `coverage_end_date`                    | `date`           | End date.                                                                                          |
| `comments`                             | `str`            | Free-text notes.                                                                                   |
| `card_image_front_upload_key`          | `str`            | S3 key under your plugin's uploads prefix for the front of the card.                              |
| `card_image_back_upload_key`           | `str`            | S3 key under your plugin's uploads prefix for the back of the card.                               |

## Card image attachment

Card images are attached by passing S3 keys on the effect, not by sending bytes inline. The keys must live under your plugin's uploads prefix (`plugin-uploads/<your-plugin-name>/...`); keys outside that prefix are rejected. Canvas performs a server-side S3 copy into the coverage's image storage when the effect is applied — no file bytes pass through your plugin.

### Example workflow: capture from the browser

One common way to land bytes under that prefix is to use a [SimpleAPI](/sdk/handlers-simple-api-http/) route declared with `upload_files=True`, which uploads multipart file parts to S3 for you and hands the resulting keys back to your plugin:

1. The plugin exposes `@api.post("/cards/upload", upload_files=True)`.
2. The browser POSTs `multipart/form-data` with one or two file parts (`front`, `back`).
3. Canvas uploads each part to S3 and provides your handler with the resulting keys via `request.form_data()`.
4. The handler returns those keys to the browser.
5. On save, the browser sends the keys back as `card_image_front_upload_key` / `card_image_back_upload_key` on the `Coverage` effect.

Other flows that land bytes at a key under your plugin's uploads prefix work the same way; the effect only cares about the final key.

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

Set the `coverage_end_date` on an existing coverage.

**Required:** `coverage_id`, `coverage_end_date`.

**Effect Type:** `EXPIRE_COVERAGE`

```python
import datetime

effect = Coverage(coverage_id="coverage-uuid-here")
return [effect.expire(coverage_end_date=datetime.date(2026, 5, 31))]
```

### `.remove()`

Mark a coverage as removed. The coverage is taken out of the patient's active stack and an audit-log entry is written; the row is not hard-deleted.

**Required:** `coverage_id`.

**Effect Type:** `REMOVE_COVERAGE`

```python
effect = Coverage(coverage_id="coverage-uuid-here")
return [effect.remove()]
```

### `.remove_photo(side)`

Clear the front or back card image on a coverage.

**Required:** `coverage_id`, `side`.

`side` is one of `"FRONT"` or `"BACK"`.

**Effect Type:** `REMOVE_COVERAGE_PHOTO`

```python
effect = Coverage(coverage_id="coverage-uuid-here")
return [effect.remove_photo(side="BACK")]
```

### `CoverageReorder.apply()`

Reorder the ranks of all of a patient's coverages in one effect. Useful when a new primary is added and existing coverages need to slot down.

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
- **Authorization**: the acting staff user must have permission to add / change / delete coverage on the named patient. Your plugin's own session authentication is not, by itself, sufficient — Canvas re-checks staff permissions when the effect is applied.
- **Card image keys**: must be S3 keys under your plugin's uploads prefix (`plugin-uploads/<your-plugin-name>/...`). Keys outside that prefix are rejected.

## Eligibility checks

After a successful create or update, Canvas runs an eligibility check against the configured clearinghouse and stores the result on the coverage. Failures do not roll back the effect.

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

- Reordering is performed across the entire stack at once via `CoverageReorder.apply()`. Updating one coverage's rank in isolation via `.update()` will be rejected if it leaves another coverage at the same rank.
