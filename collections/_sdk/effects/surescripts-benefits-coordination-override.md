---
title: "Surescripts Benefits Coordination Override"
slug: "effect-surescripts-benefits-coordination-override"
excerpt: "Override the BenefitsCoordination fields on an outbound Surescripts NewRx from a plugin handler."
hidden: true
---

The `SurescriptsBenefitsCoordinationOverride` effect lets a plugin override the
BenefitsCoordination fields — BIN, PCN, Group ID, and Member ID — on Canvas's
outbound Surescripts `NewRx` message. It is returned from a handler of the
[`PRESCRIBE_COMMAND__PRE_SEND`](/sdk/events/) event, which fires from Canvas
right before the `NewRx` is sent to the pharmacy.

This is the e-prescribing analog of the
[`HealthGorillaLabOrderOverride`](/sdk/effect-health-gorilla-lab-order-override/)
effect. Use it to drive prescription benefits routing from plugin-owned state
without putting any payer-specific concept into Canvas core.

## Behavior

Each field on the effect is independently optional. A field set to a
non-`None` value overrides the value Canvas derives from the Surescripts
eligibility response for that field; a field left as `None` (the default) means
**no override** — Canvas falls through to the eligibility-derived value for that
field. A plugin can override a single value without disturbing the others.

When an override is present, it takes precedence over the eligibility-derived
value, and the BenefitsCoordination segment is included even when no eligibility
lookup was performed.

## Attributes

| Attribute                         | Type | Description                                                                 |
| --------------------------------- | ---- | --------------------------------------------------------------------------- |
| iin_number                        | str  | PayerIdentification IINumber on the NewRx — the BIN.                         |
| processor_identification_number   | str  | PayerIdentification ProcessorIdentificationNumber — the PCN.                 |
| group_id                          | str  | BenefitsCoordination GroupID — the Group ID.                                |
| pbm_member_id                     | str  | BenefitsCoordination PBMMemberID — the Member ID.                           |

## Example

```python
from canvas_generated.messages.events_pb2 import EventType
from canvas_sdk.effects.surescripts import SurescriptsBenefitsCoordinationOverride
from canvas_sdk.handlers import BaseHandler


class OverrideBenefitsCoordination(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PRESCRIBE_COMMAND__PRE_SEND)

    def compute(self):
        # Resolve the patient's pharmacy benefit from plugin-owned state.
        benefit = self.resolve_pharmacy_benefit(self.event.target)
        if benefit is None:
            return []

        return [SurescriptsBenefitsCoordinationOverride(
            iin_number=benefit.bin,
            processor_identification_number=benefit.pcn,
            group_id=benefit.group_id,
            pbm_member_id=benefit.member_id,
        ).apply()]
```

## Related

- [`PRESCRIBE_COMMAND__PRE_SEND`](/sdk/events/) event — fires this effect's host
- [`HealthGorillaLabOrderOverride`](/sdk/effect-health-gorilla-lab-order-override/) — the lab-order analog
