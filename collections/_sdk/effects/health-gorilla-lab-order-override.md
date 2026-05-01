---
title: "Health Gorilla Lab Order Override"
slug: "effect-health-gorilla-lab-order-override"
excerpt: "Inject FHIR-shaped values into the outbound Health Gorilla lab-order payload from a plugin handler."
hidden: true
---

The `HealthGorillaLabOrderOverride` effect lets a plugin inject FHIR-shaped values
(account numbers, bill-to, performer organization, sub-tenant, location)
into Canvas's outbound Health Gorilla lab-order payload at order-send time.
It is returned from a handler of the
[`LAB_ORDER_COMMAND__PRE_SEND`](/sdk/events/) event, which fires from Canvas
right before the FHIR `RequestGroup` is built and POSTed to Health Gorilla.

This is the supported way to drive lab-order routing from plugin-owned
state (for example, a partner-specific lab account selected in a custom
chart UI) without putting any partner/tenant concept into Canvas core.

## Behavior

Each field on the effect is independently optional. A field set to a
non-`None` value overrides Canvas's default resolution for that field; a
field left as `None` (the default) means **no override** — Canvas falls
through to its existing resolution path for that field.

Multiple plugins may return overrides for the same order. When two effects
set the same field, the later one wins.

## Attributes

| Attribute                       | Type   | Description                                                                                                              |
| ------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------ |
| practitioner_account_number     | str    | Stamped on the contained `Practitioner.identifier` (Account Number).                                                     |
| organizational_account_number   | str    | Stamped on the contained authorizing `Organization.identifier` (Account Number).                                         |
| hg_organization_id              | str    | Health Gorilla facility id (`f-...`) used for the `requestgroup-performer` reference. Skips the lab-name catalog lookup. |
| hg_tenant_id                    | str    | Health Gorilla sub-tenant Organization id. Adds a `requestgroup-authorizedBy` reference to `Organization/t-{tenant_id}`. |
| hg_location_id                  | str    | Optional Location reference for the order.                                                                               |
| bill_to_code                    | [BillToCode](#billtocode) | Explicit `Account.type` coding. Overrides the existing coverage-derived inference.                  |

### BillToCode

`bill_to_code` is constrained to one of four Health-Gorilla–recognized codes.
It is a Pydantic `Literal`, so attempting to construct the effect with any
other value raises a `ValidationError` at construction time.

| Value         | HG `Account.type.coding.code` | Display       |
| ------------- | ----------------------------- | ------------- |
| `self`        | `self`                        | Client        |
| `patient`     | `patient`                     | Patient       |
| `guarantor`   | `guarantor`                   | Guarantor     |
| `thirdParty`  | `thirdParty`                  | Third Party   |

When `bill_to_code` is `patient` or `guarantor`, Canvas attaches the
appropriate `guarantor` reference to the FHIR `Account` automatically.

## Example

```python
from canvas_generated.messages.events_pb2 import EventType
from canvas_sdk.effects.lab_order import HealthGorillaLabOrderOverride
from canvas_sdk.handlers import BaseHandler


class InjectPartnerLabAccount(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.LAB_ORDER_COMMAND__PRE_SEND)

    def compute(self):
        # Resolve the selected lab account from plugin-owned state — for
        # example, a custom-model row keyed off the note's partner_slug
        # stored in note.related_data.
        account = self.resolve_lab_account_for_note(self.event.target)
        if account is None:
            return []

        return [HealthGorillaLabOrderOverride(
            practitioner_account_number=account.practitioner_account_number,
            organizational_account_number=account.organizational_account_number,
            hg_organization_id=account.hg_organization_id,
            hg_tenant_id=account.tenant_id or None,
            hg_location_id=account.location_id or None,
            bill_to_code="self",
        ).apply()]
```

## Related

- [`LAB_ORDER_COMMAND__PRE_SEND`](/sdk/events/) event — fires this effect's host
- [Health Gorilla multi-tenant Organization model](https://developer.healthgorilla.com/docs/organization-2)
- [HG `RequestGroup` profile](https://developer.healthgorilla.com/docs/requestgroup)
