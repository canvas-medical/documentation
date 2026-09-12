---
title: "Patient Identification Card"
slug: "effect-patient-identification-card"
excerpt: "Create, update, or delete a patient's identification card record with an attached image."
hidden: false
---

The `PatientIdentificationCard` effect lets a plugin attach, update, or delete a patient's identification-card image (driver license, passport, etc.). The image is attached by passing an S3 key on `image_upload_key`; Canvas performs a server-side copy into the card's storage when the effect is applied — no file bytes pass through your plugin.

## Attributes

| Attribute           | Type    | Description                                                          |
|---------------------|---------|----------------------------------------------------------------------|
| `card_id`           | `int`   | The card being acted on (update / delete).                           |
| `patient_id`        | `str`   | The patient the card belongs to (create only).                       |
| `image_upload_key`  | `str`   | S3 key under your plugin's uploads prefix for the card image.        |
| `title`             | `str`   | Label for the card (e.g. "Driver license").                          |
| `active`            | `bool`  | Whether the card is currently in use.                                |

## File attachment

`image_upload_key` must live under your plugin's uploads prefix (`plugin-uploads/<your-plugin-name>/...`) — keys outside that prefix are rejected. The platform performs a server-side S3 copy into the canonical `identification-cards/` storage when the effect is applied. See the [SimpleAPI HTTP documentation](/sdk/handlers-simple-api-http/) for the `upload_files=True` flag that produces these keys.

## Effect Methods

### `.create()`

Create a new identification card for a patient.

**Required:** `patient_id`, `image_upload_key`.

**Effect Type:** `CREATE_PATIENT_IDENTIFICATION_CARD`

```python
from canvas_sdk.effects.patient_identification_card import PatientIdentificationCard
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self):
        effect = PatientIdentificationCard(
            patient_id="patient-key-here",
            image_upload_key="plugin-uploads/my_plugin/abc-license.jpg",
            title="Driver license",
        )
        return [effect.create()]
```

### `.update()`

Update an existing card. Only fields you set are changed. Provide a new `image_upload_key` to replace the image.

**Required:** `card_id`.

**Effect Type:** `UPDATE_PATIENT_IDENTIFICATION_CARD`

### `.delete()`

Delete an existing card.

**Required:** `card_id`.

**Effect Type:** `DELETE_PATIENT_IDENTIFICATION_CARD`

## Validation

- **Create**: `patient_id` must reference an existing patient; `image_upload_key` is required; `card_id` must *not* be set.
- **Update**: `card_id` is required and must reference an existing card.
- **Delete**: `card_id` is required.
- **Authorization**: the acting staff user must have permission to add / change / delete identification cards on the named patient. Your plugin's own session authentication is not sufficient — Canvas re-checks staff permissions when the effect is applied.
- **Card image keys**: must be S3 keys under your plugin's uploads prefix.
