---
title: "Health Gorilla Lab Order Prepared"
slug: "event-health-gorilla-lab-order-prepared"
excerpt: "Read-only event fired right after Canvas builds the outbound Health Gorilla RequestGroup and before it is POSTed to HG."
hidden: true
---

`HEALTH_GORILLA_LAB_ORDER_PREPARED` fires from Canvas right after the
outbound Health Gorilla FHIR `RequestGroup` dict is constructed and
right before it is POSTed to Health Gorilla. Plugin handlers receive
the prepared dict via the event context and can store it, forward it
to a partner backend, or surface it in the chart.

The event is **read-only**: it has no associated effect type, and any
effects a handler returns are discarded. It does not affect the send
path.

This complements
[`LAB_ORDER_COMMAND__PRE_SEND`](/sdk/events/), which fires *before* the
build and lets a plugin inject overrides via
[`HealthGorillaLabOrderOverride`](/sdk/effects/health-gorilla-lab-order-override).
The pair gives a plugin both an inject hook and a verify hook on every
outbound HG order.

## Event context

The plugin handler receives `self.event.context` as a JSON-serialized
dict with the following keys:

| Key             | Type     | Description                                                                                                       |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| lab_order       | dict     | `{"id": "<uuid>", "uuid": "<uuid>"}` — the LabOrder external id.                                                  |
| lab_partner     | str      | Ontology lab partner name (`order.ontology_lab_partner`).                                                         |
| patient         | dict     | `{"id": "<key>"}` if the order has a patient, else `{}`.                                                          |
| note            | dict     | `{"id": "<uuid>", "uuid": "<uuid>"}` — only present when the order has a Note FK.                                 |
| request_group   | dict     | The full FHIR `RequestGroup` as it will be POSTed to HG, including all overrides applied by `LAB_ORDER_COMMAND__PRE_SEND` handlers. |

## Example

```python
import json

from canvas_generated.messages.events_pb2 import EventType
from canvas_sdk.handlers.base import BaseHandler


class LogHGPayload(BaseHandler):
    """Capture every outbound HG RequestGroup for partner verification."""

    RESPONDS_TO = EventType.Name(EventType.HEALTH_GORILLA_LAB_ORDER_PREPARED)

    def compute(self):
        context = json.loads(self.event.context)
        request_group = context["request_group"]
        lab_order_id = context["lab_order"]["id"]
        # store / forward / display the dict however you need
        return []  # no effect type associated with this event
```

## Related

- [`LAB_ORDER_COMMAND__PRE_SEND`](/sdk/events/) — fires *before* the build, accepts override effects
- [`HealthGorillaLabOrderOverride`](/sdk/effects/health-gorilla-lab-order-override) — the override effect returned from PRE_SEND
- [HG `RequestGroup` profile](https://developer.healthgorilla.com/docs/requestgroup)
