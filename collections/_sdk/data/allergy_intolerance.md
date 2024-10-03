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
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance
from logger import log


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.ALLERGY_INTOLERANCE_CREATED)

    NARRATIVE_STRING = "Narrative string"

    def compute(self):
        allergy = AllergyIntolerance.objects.get(id=self.target)

        log.info(f"Allergy intolerance {allergy.id} created for Patient {allergy.patient.id}")

        return []
```

# Filtering

Allergy intolerances can be filtered by any attribute that exists on the model.

Filtering for allergy intolerances is done with the `filter` method on the `AllergyIntolerance` model manager.

## By patient

Specify the `patient` or `patient_id` attribute when calling `filter` to filter by patient.

To filter by patient:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance
from canvas_sdk.v1.data.medication import Medication
from logger import log


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PRESCRIPTION_CREATED)

    NARRATIVE_STRING = "Narrative string"

    def compute(self):
        medication = Medication.objects.get(id=self.target)
        patient = medication.patient

		 # Fetch the allergies for the patient
        allergies = AllergyIntolerance.objects.filter(patient=patient)

        log.info(f"Allergy intolerances for patient {patient.id}: {allergies}")

        return []
```

To filter by patient ID:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance
from canvas_sdk.v1.data.medication import Medication
from logger import log


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PRESCRIPTION_CREATED)

    NARRATIVE_STRING = "Narrative string"

    def compute(self):
        medication = Medication.objects.get(id=self.target)
        patient_id = medication.patient.id

		 # Fetch the allergies for the patient by ID
        allergies = AllergyIntolerance.objects.filter(patient_id=patient_id)

        log.info(f"Allergy intolerances for patient {patient_id}: {allergies}")

        return []
```

## By attribute

Specify an attribute calling `filter` to filter by that attribute.

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance
from canvas_sdk.v1.data.medication import Medication
from logger import log


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PRESCRIPTION_CREATED)

    NARRATIVE_STRING = "Narrative string"

    def compute(self):
        medication = Medication.objects.get(id=self.target)

        # Fetch the allergies for the patient
        allergies = AllergyIntolerance.objects.filter(patient=medication.patient)

        # Filter out inactive allergies
        allergies = allergies.filter(status="active")

        log.info(f"Active allergy intolerances for patient {patient.id}: {allergies}")

        return []
```


## By ValueSet

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering.

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data.allergy_intolerance import AllergyIntolerance
from canvas_sdk.v1.data.medication import Medication
from canvas_sdk.value_set.v2022.allergy import EggSubstance
from logger import log

class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.IMMUNIZATION_CREATED)

    NARRATIVE_STRING = "Narrative string"

    def compute(self):
        # NOTE: The Immunization model is not yet available
        immunization = Immunization.objects.get(id=self.target)
        patient = immunization.patient

        # Fetch the allergies for the patient
        allergies = AllergyIntolerance.objects.filter(patient=patient).find(EggSubstance)

        # Filter down further to just allergies associated with egg substance
        allergies = allergies.find(EggSubstance)
        if allergies.exists():
            log.info(f"Patient {patient.id} has a known egg allergy.")
        else:
            log.info(f"Patient {patient.id} is not known to have an egg allergy.")

        return []
```
