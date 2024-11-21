---
title: "Device"
slug: "data-device"
excerpt: "Canvas SDK Device"
hidden: false
---

## Introduction

The `Device` model represents a type of a manufactured item that is used in the provision of healthcare without being substantially changed through that activity. The device may be a medical or non-medical device.

## Basic usage

To get a device by identifier, use the `get` method on the `Device` model manager:

```python
from canvas_sdk.v1.data.device import Device

device = Device.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the devices for a patient can be accessed with the `devices` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
devices = patient.devices.all()
```

## Filtering

Devices can be filtered by any attribute that exists on the model.

Filtering for devices is done with the `filter` method on the `Device` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.device import Device

devices = Devices.objects.filter(manufacturer="ACME Biomedical", lot_number="M320")
```

## Attributes

### Device
| Field Name                  | Type                          |
|-----------------------------|-------------------------------|
| id                          | UUID                          |
| dbid                        | Integer                       |
| created                     | DateTime                      |
| modified                    | DateTime                      |
| originator                  | CanvasUser                    |
| committer                   | CanvasUser                    |
| entered_in_error            | CanvasUser                    |
| patient                     | [Patient](/sdk/data-patient/) |
| note_id                     | Integer                       |
| deleted                     | Boolean                       |
| labeled_contains_NRL        | Boolean                       |
| assigning_authority         | String                        |
| scoping_entity              | String                        |
| udi                         | String                        |
| di                          | String                        |
| issuing_agency              | String                        |
| lot_number                  | String                        |
| brand_name                  | String                        |
| mri_safety_status           | String                        |
| version_model_number        | String                        |
| company_name                | String                        |
| gmdnPTName                  | Text                          |
| status                      | String                        |
| expiration_date             | Date                          |
| expiration_date_original    | String                        |
| serial_number               | String                        |
| manufacturing_date_original | String                        |
| manufacturing_date          | Date                          |
| manufacturer                | String                        |
| procedure_id                | Integer                       |
