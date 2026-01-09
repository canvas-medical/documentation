---
title: "Organization"
slug: "data-organization"
excerpt: "Canvas SDK Organization"
hidden: false
---

## Introduction

The `Organization` model represents the overall Organization in a Canvas EMR instance. An `Organization` can have multiple related [Practice Locations](/sdk/data-practicelocation).

## Basic usage

Canvas instances can contain only a single `Organization` entry. To retrieve the `Organization` entry, you can either query by the organization's name:

```python
from canvas_sdk.v1.data.organization import Organization

organization = Organization.objects.get(full_name="Medical Organization")
```

Or since there will only be one `Organization` in an instance, it can also be fetched by using the `first` method:

```python
from canvas_sdk.v1.data.organization import Organization

organization = Organization.objects.first()
```

## Attributes

### Organization

| Field Name            | Type                                                |
| --------------------- | --------------------------------------------------- |
| dbid                  | Integer                                             |
| created               | DateTime                                            |
| modified              | DateTime                                            |
| full_name             | String                                              |
| short_name            | String                                              |
| subdomain             | String                                              |
| logo_url              | String                                              |
| background_image_url  | String                                              |
| background_gradient   | String                                              |
| active                | Boolean                                             |
| tax_id                | String                                              |
| tax_id_type           | [TaxIDType](/sdk/data-enumeration-types/#taxidtype) |
| group_npi_number      | String                                              |
| group_taxonomy_number | String                                              |
| include_zz_qualifier  | Boolean                                             |

## OrganizationAddress

The `OrganizationAddress` model represents a physical or mailing address associated with an Organization. Multiple addresses can be linked to a single Organization, each with its own type and details.

### Attributes

| Field Name           | Type                                                                        |
| -------------------- | --------------------------------------------------------------------------- |
| id                   | UUID                                                                        |
| dbid                 | Integer                                                                     |
| organization         | [Organization](#organization)                                               |
| use                  | [AddressUseWithBilling](/sdk/data-enumeration-types/#addressusewithbilling) |
| type                 | [AddressType](/sdk/data-enumeration-types/#addresstype)                     |
| longitude            | Float                                                                       |
| latitude             | Float                                                                       |
| start                | Date                                                                        |
| end                  | Date                                                                        |
| country              | String                                                                      |
| state                | [AddressState](/sdk/data-enumeration-types/#addressstate)                   |
| address_search_index | String                                                                      |
| line1                | String                                                                      |
| line2                | String                                                                      |
| city                 | String                                                                      |
| district             | String                                                                      |
| state_code           | String                                                                      |
| postal_code          | String                                                                      |

## OrganizationContactPoint

The `OrganizationContactPoint` model represents a contact method (such as phone, email, or fax) for an Organization. Multiple contact points can be associated with a single Organization, each with its own type, use, and status.

### Attributes

| Field Name   | Type                                                                  |
| ------------ | --------------------------------------------------------------------- |
| id           | UUID                                                                  |
| dbid         | Integer                                                               |
| organization | [Organization](#organization)                                         |
| system       | [ContactPointSystem](/sdk/data-enumeration-types/#contactpointsystem) |
| value        | String                                                                |
| use          | [ContactPointUse](/sdk/data-enumeration-types/#contactpointuse)       |
| use_notes    | String                                                                |
| rank         | Integer                                                               |
| state        | [ContactPointState](/sdk/data-enumeration-types/#contactpointstate)   |

<br/>
<br/>
<br/>
