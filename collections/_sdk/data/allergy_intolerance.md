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

If you have a patient object, the allergy intolerances for a patient can be accessed with the `allergy_intolerances` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
allergies = patient.allergy_intolerances.all()
```

If you have a patient ID, you can get the allergies for the patient with the `for_patient` method on the `AllergyIntolerance` model:

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
allergies = AllergyIntolerance.objects.for_patient(patient_id)
```

# Codings

The codings for an allergy intolerance can be accessed with the `codings` attribute on an `AllergyIntolerance` object:

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance
from logger import log

allergy = AllergyIntolerance.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in allergy.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

# Filtering

Allergy intolerances can be filtered by any attribute that exists on the model.

Filtering for allergy intolerances is done with the `filter` method on the `AllergyIntolerance` model manager.

## By attribute

Specify an attribute calling `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance

allergies = AllergyIntolerance.objects.filter(status="active")
```

## By ValueSet

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance
from canvas_sdk.value_set.v2022.allergy import EggSubstance

allergies = AllergyIntolerance.objects.find(EggSubstance)
```
