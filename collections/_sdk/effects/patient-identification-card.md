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
| `card_id`          | `int`            | The `dbid` of an existing identification card. Cards have no UUID, so they are identified by `dbid`. Must be unset when creating a card. | For `update()` and `delete()` |
| `patient_id`       | `str`            | The `id` of the patient the card belongs to. | For `create()` |
| `image_upload_key` | `str`            | The upload key of the card image. See [Card image](#card-image). | For `create()` |
| `title`            | `str` or `None`  | A label for the card, such as `"Driver license"`. Up to 255 characters. | No |
| `active`           | `bool`           | Whether the card is active. | No |

## Card image

The card image is a PNG or JPEG file that a user uploads to your plugin through a SimpleAPI route declared with `file_uploads="stored"`. Set `image_upload_key` to the `key` of the uploaded `StoredFilePart`. See [Storing uploaded files](/sdk/handlers-simple-api-http/#storing-uploaded-files).

When the effect is applied, Canvas checks that your plugin uploaded the file and that it is a PNG or JPEG image. It copies the file to the card and then deletes the upload, so each key works only once. On `update()`, setting `image_upload_key` replaces the card's image, and a key of `None` keeps the current image.

## Who can write identification cards

A staff member needs the same permissions to add, change, or delete identification cards as in the chart. A patient, for example on a patient portal page, can write only their own cards. An effect with no user behind it runs as Canvas Bot and needs no permission.

## Examples

```python
from canvas_sdk.effects.patient import PatientIdentificationCard
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="d7af3e356368446c85b40a5d6ff7288e")

# Create a card. In a SimpleAPI handler, use the key of the uploaded StoredFilePart.
create = PatientIdentificationCard(
    patient_id=patient.id,
    image_upload_key="acme/plugin-uploads/my_plugin/20261014T120000Z-abc-license.jpg",
    title="Driver license",
).create()

card = patient.identification_cards.filter(active=True).first()

# Deactivate a card
deactivate = PatientIdentificationCard(card_id=card.dbid, active=False).update()

# Delete a card
delete = PatientIdentificationCard(card_id=card.dbid).delete()
```
