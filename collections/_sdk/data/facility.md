---
title: "Facility"
slug: "data-facility"
excerpt: "Canvas SDK Facility"
hidden: false
---

## Introduction

The `Facility` object represents a healthcare facility associated with patients within Canvas. Facilities can include hospitals, clinics, or other healthcare institutions where patients receive care. This object contains essential information about the facility, such as its address, contact details, and operational status.

## Basic Usage

To get a facility by identifier, use the `get` method on the `Facility` model manager:

```python
from canvas_sdk.v1.data.facility import Facility

facility = Facility.objects.get(id="34b50dfa-1b3e-4dc2-a11d-41b3115c29f3")
```

## Filtering

Facilities can be filtered by any attribute that exists on the model.

Filtering for facilities is done with the `filter` method on the `Facility` model manager.

## Attributes

Specify attributes with `filter` to filter by those attributes:

```python
from canvas_sdk.v1.data.facility import Facility

facilities = Facility.objects.filter(name="General Hospital", city="Metropolis")
```

### Facility

| Field Name   | Type     |
| ------------ | -------- |
| id           | UUID     |
| dbid         | Integer  |
| created      | DateTime |
| modified     | DateTime |
| line1        | String   |
| line2        | String   |
| city         | String   |
| district     | String   |
| state_code   | String   |
| postal_code  | String   |
| name         | String   |
| npi_number   | String   |
| phone_number | String   |
| active       | Boolean  |
