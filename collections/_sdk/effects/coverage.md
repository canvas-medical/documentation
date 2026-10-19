---
title: "Coverage Effect"
slug: "effect-coverage"
excerpt: "Create, update, expire, remove, and reorder a patient's insurance coverages, with insurance card images."
hidden: false
---

The `Coverage` effect writes a patient's insurance coverage from a plugin, including the front and back images of the insurance card. Use it to capture insurance during intake, such as from a patient portal form where the patient photographs their card. You can also use it to keep coverages in step with an external system. The `CoverageReorder` effect changes the rank and stack of several coverages at once.

Canvas applies the same rules to these effects as it does to the coverage form in the patient's chart. The effects also check most of those rules in your plugin before the effect is sent. An invalid coverage raises a validation error in your handler.

To read coverages, see the [Coverage data model](/sdk/data-coverage/).

## Methods

Build a `Coverage` with the [attributes](#attributes) you want to set, then return one of its methods from your handler.

### create() → Effect

Creates a coverage for a patient.

- `patient_id`, `issuer_id`, `coverage_rank`, `id_number`, and `patient_relationship_to_subscriber` are required.
- `coverage_id` must not be set.
- The patient must not already have a coverage with the same `coverage_rank` in the same stack. A coverage that ends today or earlier, in the instance's time zone, frees its rank. To replace a primary coverage, expire the old one with today's date, then create the new one the same day.
- `stack` defaults to `IN_USE`, and `coverage_start_date` defaults to today in the instance's time zone.
- Canvas requests an eligibility check after the coverage is saved.

### update() → Effect

Changes an existing coverage.

- `coverage_id` is required, and must be the id of an existing coverage.
- Only the attributes you set on the effect are changed. Setting an optional attribute to `None` clears it.
- The required attributes, `stack`, `subscriber_id`, and `coverage_start_date` cannot be set to `None` or an empty string.
- `patient_id` cannot be changed.
- If you change `issuer_id`, Canvas clears the coverage's `issuer_address_id`, `issuer_phone_id`, and `coverage_type`, unless you set new values in the same update.
- If another coverage in the same stack already holds the new rank, the coverage you updated takes it. The other coverage moves down one rank.
- Canvas requests a new eligibility check when the update changes `issuer_id`, `issuer_address_id`, `id_number`, `subscriber_id`, or `patient_relationship_to_subscriber`.

### expire(coverage_end_date) → Effect

Ends an existing coverage on `coverage_end_date`, a `datetime.date`. `coverage_id` is required. The end date must be on or after the coverage's start date; a coverage can end on the day it starts. Canvas records an audit event, as it does when a coverage is expired from the chart.

### remove() → Effect

Moves an existing coverage to the `REMOVED` stack. `coverage_id` is required. Canvas records an audit event.

`create()`, `update()`, and `CoverageReorder` do not accept the `REMOVED` stack. Use `remove()` instead.

### remove_photo(side) → Effect

Removes the front or back card image from an existing coverage. `coverage_id` is required. Set `side` to `PhotoSide.FRONT` or `PhotoSide.BACK`.

## Attributes

| Attribute                            | Type                                                                        | Description | Required |
|--------------------------------------|-----------------------------------------------------------------------------|-------------|----------|
| `coverage_id`                        | `UUID` or `str`                                                             | The `id` of an existing [Coverage](/sdk/data-coverage/#coverage). Must be unset when creating a coverage. | For every method except `create()` |
| `patient_id`                         | `str`                                                                       | The `id` of the patient the coverage belongs to. | For `create()` |
| `issuer_id`                          | `UUID` or `str`                                                             | The `id` of the payer, a [Transactor](/sdk/data-coverage/#transactor). The coverage's plan type comes from the payer. | For `create()` |
| `issuer_address_id`                  | `UUID` or `str` or `None`                                                   | The `id` of a [TransactorAddress](/sdk/data-coverage/#transactoraddress) that belongs to the payer. | No |
| `issuer_phone_id`                    | `UUID` or `str` or `None`                                                   | The `id` of a [TransactorPhone](/sdk/data-coverage/#transactorphone) that belongs to the payer. | No |
| `patient_relationship_to_subscriber` | [`CoverageRelationshipCode`](/sdk/data-coverage/#coveragerelationshipcode) | The patient's relationship to the subscriber. See [Subscribers](#subscribers). | For `create()` |
| `subscriber_id`                      | `str`                                                                       | The `id` of the patient who holds the policy. See [Subscribers](#subscribers). | When the patient is not the subscriber |
| `subscriber_identifier`              | `str` or `None`                                                             | The subscriber's identifier on the policy. Up to 100 characters. | No |
| `coverage_rank`                      | `CoverageRank`                                                              | The coverage's order within its stack: `PRIMARY` (1), `SECONDARY` (2), `TERTIARY` (3), `QUATERNARY` (4), or `QUINARY` (5). | For `create()` |
| `stack`                              | [`CoverageStack`](/sdk/data-coverage/#coveragestack)                        | `IN_USE` or `OTHER`. Defaults to `IN_USE` on create. | No |
| `coverage_type`                      | [`TransactorCoverageType`](/sdk/data-coverage/#transactorcoveragetype) or `None` | The type of coverage. | No |
| `id_number`                          | `str`                                                                       | The member ID on the insurance card. Up to 100 characters. | For `create()` |
| `plan`                               | `str` or `None`                                                             | Plan name. Up to 255 characters. | No |
| `sub_plan`                           | `str` or `None`                                                             | Sub-plan name. Up to 255 characters. | No |
| `group`                              | `str` or `None`                                                             | Group number. Up to 255 characters. | No |
| `sub_group`                          | `str` or `None`                                                             | Sub-group number. Up to 255 characters. | No |
| `employer`                           | `str` or `None`                                                             | The subscriber's employer. Up to 255 characters. | No |
| `coverage_start_date`                | `datetime.date`                                                             | The date the coverage starts. Must be on or before `coverage_end_date`. Defaults to today on create. | No |
| `coverage_end_date`                  | `datetime.date` or `None`                                                   | The date the coverage ends. | No |
| `comments`                           | `str` or `None`                                                             | Free-text comments. | No |
| `card_image_front_upload_key`        | `str` or `None`                                                             | The upload key of the front image of the insurance card. See [Card images](#card-images). | No |
| `card_image_back_upload_key`         | `str` or `None`                                                             | The upload key of the back image of the insurance card. See [Card images](#card-images). | No |

`CoverageRank`, `CoverageRelationshipCode`, `CoverageStack`, `TransactorCoverageType`, and `Transactor` are imported from `canvas_sdk.v1.data.coverage`. `PhotoSide` is imported from `canvas_sdk.effects.coverage`.

### Subscribers

When `patient_relationship_to_subscriber` is `CoverageRelationshipCode.SELF`, the patient is the subscriber. Leave `subscriber_id` unset, or set it to the patient's `id`.

For any other relationship, set `subscriber_id` to the `id` of a different patient, the person who holds the policy.

## Card images

Card images are PNG or JPEG files that a user uploads to your plugin through a SimpleAPI route declared with `file_uploads="stored"`. Set `card_image_front_upload_key` and `card_image_back_upload_key` to the `key` of each uploaded `StoredFilePart`. See [Storing uploaded files](/sdk/handlers-simple-api-http/#storing-uploaded-files).

When the effect is applied, Canvas checks that your plugin uploaded each file and that each file is a PNG or JPEG image. It copies the file to the coverage and then deletes the upload, so each key works only once. If any part of the effect fails, Canvas saves none of it, including the card images.

On `update()`, setting one image key replaces that side of the card and leaves the other side unchanged. To remove an image, use `remove_photo()`.

## Reordering coverages

`CoverageReorder` sets the rank and stack of several of a patient's coverages in one effect. Build it with the patient's `id` and an `ordering` list of `CoverageReorderEntry` objects, then return `apply()`.

| Attribute    | Type                             | Description |
|--------------|----------------------------------|-------------|
| `patient_id` | `str`                            | The `id` of the patient. |
| `ordering`   | `list[CoverageReorderEntry]`     | The new position of each coverage. Must contain at least one entry. |

Each `CoverageReorderEntry` has these attributes, all required:

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `coverage_id`   | `UUID` or `str` | The `id` of one of the patient's coverages. |
| `coverage_rank` | `CoverageRank`  | The coverage's new rank. |
| `stack`         | `CoverageStack` | The coverage's new stack: `IN_USE` or `OTHER`. |

The ordering must follow these rules:

- Each coverage appears once and belongs to the patient.
- Within each stack, ranks are unique and consecutive, starting at 1.
- For each stack the ordering places a coverage in, the ordering lists every active coverage in that stack.

## Who can write coverages

Canvas applies the permissions of the user behind the effect:

- A staff member needs the same permissions as in the chart: permission to change coverages, and access to the patient. This applies to every coverage change, including `expire()`, `remove()`, `remove_photo()`, and `CoverageReorder`.
- A patient, for example on a patient portal page, can write only their own coverages.
- An effect with no user behind it, such as one from a scheduled task, runs as Canvas Bot and needs no permission.

## Examples

### Capture an insurance card from a form

This SimpleAPI route creates a primary coverage from a `multipart/form-data` request. The request carries the patient's id, the payer's id, the member ID, and photos of both sides of the card:

```python
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.coverage import Coverage
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import SessionCredentials, SimpleAPI, api
from canvas_sdk.v1.data.coverage import CoverageRank, CoverageRelationshipCode


class InsuranceCardAPI(SimpleAPI):
    def authenticate(self, credentials: SessionCredentials) -> bool:
        return credentials.logged_in_user["type"] == "Staff"

    @api.post("/insurance-card", file_uploads="stored")
    def insurance_card(self) -> list[Response | Effect]:
        form = self.request.form_data()
        front = form["card_front"]
        back = form["card_back"]
        if front.error or back.error:
            return [JSONResponse({"error": "upload failed"}, status_code=HTTPStatus.BAD_GATEWAY)]

        coverage = Coverage(
            patient_id=form["patient_id"].value,
            issuer_id=form["payer_id"].value,
            id_number=form["member_id"].value,
            coverage_rank=CoverageRank.PRIMARY,
            patient_relationship_to_subscriber=CoverageRelationshipCode.SELF,
            card_image_front_upload_key=front.key,
            card_image_back_upload_key=back.key,
        )
        return [coverage.create(), JSONResponse({}, status_code=HTTPStatus.ACCEPTED)]
```

To find a payer's `id`, query the [Transactor](/sdk/data-coverage/#transactor) model:

```python
from canvas_sdk.v1.data.coverage import Transactor

payer = Transactor.objects.filter(name__icontains="aetna", active=True).first()
```

### Update a coverage

```python
from canvas_sdk.effects.coverage import Coverage
from canvas_sdk.v1.data.coverage import Coverage as CoverageModel

coverage = CoverageModel.objects.get(id="b3b5e4f6-1c2d-4e8a-9f0b-7a6c5d4e3f21")

# Change the group number and clear the comments
effect = Coverage(coverage_id=coverage.id, group="GRP-2027", comments=None).update()
```

### Expire, remove, or remove a card image

```python
from datetime import date

from canvas_sdk.effects.coverage import Coverage, PhotoSide

coverage_id = "b3b5e4f6-1c2d-4e8a-9f0b-7a6c5d4e3f21"

expire = Coverage(coverage_id=coverage_id).expire(coverage_end_date=date(2026, 12, 31))
remove = Coverage(coverage_id=coverage_id).remove()
remove_back = Coverage(coverage_id=coverage_id).remove_photo(side=PhotoSide.BACK)
```

### Swap primary and secondary coverages

```python
from canvas_sdk.effects.coverage import CoverageReorder, CoverageReorderEntry
from canvas_sdk.v1.data.coverage import CoverageRank, CoverageStack

effect = CoverageReorder(
    patient_id="d7af3e356368446c85b40a5d6ff7288e",
    ordering=[
        CoverageReorderEntry(
            coverage_id="b3b5e4f6-1c2d-4e8a-9f0b-7a6c5d4e3f21",
            coverage_rank=CoverageRank.PRIMARY,
            stack=CoverageStack.IN_USE,
        ),
        CoverageReorderEntry(
            coverage_id="4a9e2c71-8d3b-4f5e-a6c0-1b2d3e4f5a6b",
            coverage_rank=CoverageRank.SECONDARY,
            stack=CoverageStack.IN_USE,
        ),
    ],
).apply()
```
