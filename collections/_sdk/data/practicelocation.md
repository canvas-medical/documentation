---
title: "Practice Location"
slug: "data-practicelocation"
excerpt: "Canvas SDK Practice Location"
hidden: false
---

## Introduction

The `PracticeLocation` model lists all the clinical practice locations that fall under an [Organization](/sdk/data-organization).

## Basic usage

To query a `PracticeLocation` by name, the `filter` method can be used like so:

```python
from canvas_sdk.v1.data.practicelocation import PracticeLocation

practice_location = PracticeLocation.objects.filter(full_name__icontains="downtown")
```

To retrieve a list of all practice locations:

```python
practice_locations = PracticeLocation.objects.all()
```

Each `PracticeLocation` has location-specific settings that control certain behavior within the EMR application. To retrieve the available settings for a `PracticeLocation` instance, the `settings` attribute can be used to retrieve a list of names:

```python
practice_location = PracticeLocation.objects.first()

available_settings = practice_location.settings.values_list('name', flat=True)
```

Additionally, a setting's value can be found by accessing the `value` attribute on the `PracticeLocationSetting`:

```python
practice_location = PracticeLocation.objects.first()

preferred_lab_partner_text = practice_location.settings.get(name="preferredLabPartner").value
```

Please note that the content of each `value` field can contain any value that is JSON-serializable, which includes string values. This means that `value` could be any of the Python types `string`, `list` or `dict`.

## Attributes

### PracticeLocation

| Field Name                | Type                                                 |
|-------------------------- |----------------------------------------------------- |
| id                        | UUID                                                 |
| dbid                      | Integer                                              |
| created                   | DateTime                                             |
| modified                  | DateTime                                             |
| organization              | [Organization](/sdk/data-organization/#organization) |
| place_of_service_code     | String                                               |
| full_name                 | String                                               |
| short_name                | String                                               |
| background_image_url      | String                                               |
| background_gradient       | String                                               |
| active                    | Boolean                                              |
| npi_number                | String                                               |
| bill_through_organization | Boolean                                              |
| tax_id                    | String                                               |
| tax_id_type               | [TaxIDType](/sdk/data-enumeration-types/#taxidtype)  |
| billing_location_name     | String                                               |
| group_npi_number          | String                                               |
| taxonomy_number           | String                                               |
| include_zz_qualifier      | Boolean                                              |


### PracticeLocationSetting

| Field Name                | Type                                                 |
|-------------------------- |----------------------------------------------------- |
| dbid                      | Integer                                              |
| practice_location         | [PracticeLocation](#practicelocation)                |
| name                      | String                                               |
| value                     | JSON                                                 |
