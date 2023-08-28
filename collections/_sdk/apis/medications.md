---
title: Medications
---

# Medications

The Medications API is responsible for managing medications and
prescriptions.

## Examples

``` python
from canvas_core import events, logging
from canvas_core.medications.models import Prescription
logger = logging.get_logger(__name__)

@events.handle_event(events.PreRecordCreate[Prescription], origin=Prescription)
def handle_prescription_status_pre_create(event: events.PreRecordCreate[Prescription]) -> None:
    logger.info("Prescription will be created.")

@events.handle_event(events.PostRecordCreate[Prescription], origin=Prescription)
def handle_prescription_post_create(event: events.PostRecordCreate[Prescription]) -> None:
    logger.info("Prescription Created.")

@events.handle_event(events.PreRecordUpdate[Prescription], origin=Prescription)
def handle_prescription_pre_change(event: events.PreRecordUpdate[Prescription]) -> None:
    logger.info("Prescription will be updated.", diff=event.diff)

@events.handle_event(events.PostRecordUpdate[Prescription], origin=Prescription)
def handle_prescription_post_change(event: events.PostRecordUpdate[Prescription]) -> None:
    logger.info("Prescription Updated.", diff=event.diff)
```

## API Reference

::: {.automodule members=""}
canvas_core.medications
:::

::: {.automodule members="Prescription, Medication"}
canvas_core.medications.models
:::
