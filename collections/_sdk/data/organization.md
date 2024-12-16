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
organization = Organization.objects.first()
```

## Attributes

### Organization

| Field Name            | Type                    |
|---------------------- |------------------------ |
| dbid                  | Integer                 |
| created               | DateTime                |
| modified              | DateTime                |
| full_name             | String                  |
| short_name            | String                  |
| subdomain             | String                  |
| logo_url              | String                  |
| background_image_url  | String                  |
| background_gradient   | String                  |
| active                | Boolean                 |
| tax_id                | String                  |
| tax_id_type           | [TaxIDType](#taxidtype) |
| group_npi_number      | String                  |
| group_taxonomy_number | String                  |
| include_zz_qualifier  | Boolean                 |

## Enumeration types

### TaxIDType

| Value | Label      |
|-------|------------|
| E     | EIN text   |
| S     | SSN        |

<br/>
<br/>
<br/>
