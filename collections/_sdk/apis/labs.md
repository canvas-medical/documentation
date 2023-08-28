---
title: Labs
---

# Labs

The Labs API is responsible for managing lab orders.

## Examples

``` python
from canvas_core import events, logging
from canvas_core.labs.models import LabOrder
logger = logging.get_logger(__name__)

@events.handle_event(events.PreRecordCreate[LabOrder], origin=LabOrder)
def handle_lab_order_status_pre_create(event: events.PreRecordCreate[LabOrder]) -> None:
    logger.info("LabOrder will be created.")

@events.handle_event(events.PostRecordCreate[LabOrder], origin=LabOrder)
def handle_lab_order_post_create(event: events.PostRecordCreate[LabOrder]) -> None:
    logger.info("LabOrder Created.")

@events.handle_event(events.PreRecordUpdate[LabOrder], origin=LabOrder)
def handle_lab_order_pre_change(event: events.PreRecordUpdate[LabOrder]) -> None:
    logger.info("LabOrder will be updated.", diff=event.diff)

@events.handle_event(events.PostRecordUpdate[LabOrder], origin=LabOrder)
def handle_lab_order_post_change(event: events.PostRecordUpdate[LabOrder]) -> None:
    logger.info("LabOrder Updated.", diff=event.diff)
```

## API Reference

::: {.automodule members=""}
canvas_core.labs
:::

::: {.automodule members=""}
canvas_core.labs.models
:::
