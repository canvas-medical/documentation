---
title: Patients
---

# Patients

The Patients API is responsible for providing a simple interface for
accessing patient information.

## Basic Usage

The Patients API currently supports retrieval of a patient by its unique
key.

``` python
from canvas_core import patients

>>> patient_key = "08a4804ed2a40630d65e684904b2b9fc"
>>> patients.get_patient(patient_key)
<Patient: Patient object (1)>
```

## Events

You can use
`Record Lifecycle Events <record-lifecycle-events>`{.interpreted-text
role="ref"} to customize behaviour based on database events.

Here\'s an example of using the `PostRecordCreate` event to log a
message when a new patient is created.

``` python
from canvas_core import events, logging, patients

logger = logging.get_logger(__name__)

Patient = patients.get_patient_model()

@events.handle_event(events.PostRecordCreate, origin=Patient)
def handle_patient_create(event: events.PostRecordCreate[Patient]) -> None:
    """Log a message when a new patient is created."""
    patient = event.record

    # Log a message with the patient name.
    logger.info("A new patient was created.", patient_key=patient.key)
```

## API Reference

::: {.automodule members=""}
canvas_core.patients
:::
