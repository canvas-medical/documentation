---
title: "Allergy Intolerance"
slug: "data-allergy-intolerance"
excerpt: "Canvas SDK Allergy Intolerance"
hidden: false
---

# Introduction

The `AllergyIntolerance` model represents a known risk, specific to a patient, of a harmful or undesirable physiological response associated with exposure to a substance.

# Basic usage

To get an allergy intolerance by identifier, use the `get` method on the `AllergyIntolerance` model manager:

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance

allergy = AllergyIntolerance.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

# Filtering

Allergy intolerances can be filtered by any attribute that exists on the model.

Filtering for allergy intolerances is done with the `filter` method on the `AllergyIntolerance` model manager.

## By patient

Specify the `patient` or `patient_id` attribute when calling `filter` to filter by patient.

To filter by patient:

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance

patient = Patient.objects.get(id="f1b1ace27b0645ae98c988019c328223")
allergies = AllergyIntolerance.objects.filter(patient=patient)
```

To filter by patient ID:

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance

allergies = AllergyIntolerance.objects.filter(patient__id="f1b1ace27b0645ae98c988019c328223")
```

## By attribute

Specify an attribute calling `filter` to filter by that attribute.

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance

allergies = AllergyIntolerance.objects.filter(status="active")
```

## By ValueSet

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering.

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance
from canvas_sdk.value_set.v2022.allergy import EggSubstance

allergies = AllergyIntolerance.objects.find(EggSubstance)
```
