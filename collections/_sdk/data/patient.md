---
title: "Patient"
slug: "data-patient"
excerpt: "Canvas SDK Patient"
hidden: false
---

# Introduction

The `Patient` model represents an individual receiving care or other health-related services.

# Basic usage

To get a patient by identifier, use the `get` method on the `Patient` model manager:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")
```

# Filtering

Patients can be filtered by any attribute that exists on the model.

Filtering for patients is done with the `filter` method on the `Patient` model manager.

## By attribute

Specify attributes with `filter` to filter by those attributes:

```python
from canvas_sdk.v1.data.patient import Patient

patients = Patient.objects.filter(first_name="Bob", last_name="Loblaw", birth_date="1960-09-22")
```
