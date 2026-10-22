---
title: "Patient Identification Card Effect"
slug: "effect-patient-identification-card"
excerpt: "Create, update, or delete a patient's identification card images."
hidden: false
---

The `PatientIdentificationCard` effect adds, changes, or deletes an image of a patient's identification card, such as a driver's license, from a plugin. Use it to collect ID images during intake or registration. To read existing cards, see [PatientIdentificationCard](/sdk/data-patient/#patientidentificationcard) on the patient data model.

Build a `PatientIdentificationCard` with the [attributes](#attributes) you want to set, then return one of its methods from your handler: `create()`, `update()`, or `delete()`.

## Methods

### create() → Effect

Creates an identification card for a patient.

- `patient_id` and `image_upload_key` are required.
- `card_id` must not be set.

### update() → Effect

Changes an existing identification card.

- `card_id` is required, and must be the `dbid` of an existing card.
- Only the attributes you set on the effect are changed.
- `patient_id` cannot be changed, and `active` cannot be set to `None`.

### delete() → Effect

Deletes an existing identification card. `card_id` is required.

## Attributes

| Attribute          | Type             | Description | Required |
|--------------------|------------------|-------------|----------|
| `card_id`          | `int`            | The `dbid` of an existing [PatientIdentificationCard](/sdk/data-patient/#patientidentificationcard). Cards have no UUID, so they are identified by `dbid`. Must be unset when creating a card. | For `update()` and `delete()` |
| `patient_id`       | `str`            | The `id` of the [Patient](/sdk/data-patient/#patient) the card belongs to. | For `create()` |
| `image_upload_key` | `str`            | The upload key of the card image. See [Card image](#card-image). | For `create()` |
| `title`            | `str` or `None`  | A label for the card, such as `"Driver license"`. Up to 255 characters. | No |
| `active`           | `bool`           | Whether the card is active. | No |

## Card image

The card image is a PNG or JPEG file that a user uploads to your plugin through a SimpleAPI route declared with `file_uploads="stored"`. Set `image_upload_key` to the `key` of the uploaded `StoredFilePart`. See [Storing uploaded files](/sdk/handlers-simple-api-http/#storing-uploaded-files).

The key must come from a file your plugin uploaded, and the file must be a PNG or JPEG image. When the effect is applied, Canvas copies the file to the card and then deletes the upload, so each key works only once. On `update()`, setting `image_upload_key` replaces the card's image, and a key of `None` keeps the current image.

For working code, see [Upload an ID card from a form](#upload-an-id-card-from-a-form).

## Examples

### Upload an ID card from a form

This SimpleAPI route creates an identification card from a `multipart/form-data` request that carries the patient's id, a title, and a photo of the card. The route uses the [API key mixin](/sdk/handlers-simple-api-http/#api-key-1), so declare the `simpleapi-api-key` secret in your manifest and set it on your instance:

```python
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient import PatientIdentificationCard
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPI, api


class IdentificationCardAPI(APIKeyAuthMixin, SimpleAPI):
    @api.post("/identification-card", file_uploads="stored")
    def identification_card(self) -> list[Response | Effect]:
        form = self.request.form_data()
        image = form["card_image"]
        if image.error:
            return [JSONResponse({"error": "upload failed"}, status_code=HTTPStatus.BAD_GATEWAY)]

        card = PatientIdentificationCard(
            patient_id=form["patient_id"].value,
            image_upload_key=image.key,
            title=form["title"].value,
        )
        return [card.create(), JSONResponse({}, status_code=HTTPStatus.ACCEPTED)]
```

Call the route with a `multipart/form-data` POST. Each form field name matches a key the handler reads, the card photo is sent as a file, and the API key goes in the `Authorization` header:

```shell
curl --request POST \
     --url 'https://<instance-name>.canvasmedical.com/plugin-io/api/<plugin-name>/identification-card' \
     --header 'Authorization: <api-key>' \
     --form 'patient_id=b80b1cdc2e6a4aca90ccebc02e683f35' \
     --form 'title=Driver license' \
     --form 'card_image=@license.jpg;type=image/jpeg'
```

The same request from a Python script, uploading a photo saved on disk, using the [`requests`](https://requests.readthedocs.io/) library:

```python
from pathlib import Path

import requests

url = "https://<instance-name>.canvasmedical.com/plugin-io/api/<plugin-name>/identification-card"
image_path = Path("license.jpg")

with image_path.open("rb") as image:
    response = requests.post(
        url,
        headers={"Authorization": "<api-key>"},
        data={
            "patient_id": "b80b1cdc2e6a4aca90ccebc02e683f35",
            "title": "Driver license",
        },
        files={"card_image": (image_path.name, image, "image/jpeg")},
        timeout=30,
    )

print(response.status_code)
```

The route answers:

- `202 Accepted` when the photo was stored and the effect was returned.
- `502 Bad Gateway` when the photo failed to store.
- `400 Bad Request` when the request isn't `multipart/form-data`.
- `401 Unauthorized` when the API key is missing or wrong.

### Deactivate or delete a card

```python
from canvas_sdk.effects.patient import PatientIdentificationCard
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="d7af3e356368446c85b40a5d6ff7288e")
card = patient.identification_cards.filter(active=True).first()

# Deactivate a card
deactivate = PatientIdentificationCard(card_id=card.dbid, active=False).update()

# Delete a card
delete = PatientIdentificationCard(card_id=card.dbid).delete()
```
