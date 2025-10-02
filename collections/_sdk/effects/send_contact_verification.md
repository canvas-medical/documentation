---
title: "SendContactVerification"
slug: "effect-send-contact-verification"
excerpt: "Effect to send a verification message to a patient contact."
hidden: false
---

# SendContactVerification Effect

The `SendContactVerification` effect instructs Canvas to send a verification (for example, an email or SMS code) to a specific Patient Contact Point. Typical uses are verifying a patient's email address or phone number before enabling patient-portal features that require a verified contact channel.

## Attributes

| Name               | Type            | Description                                    |
| ------------------ | --------------- | ---------------------------------------------- |
| `contact_point_id` | `str` or `UUID` | The id of the `PatientContactPoint` to verify. |

## Validation & Errors

When an effect is prepared, the model validates inputs and returns structured error details if something is invalid.

- **Contact Point Exists** — The effect verifies the provided `contact_point_id` maps to an existing `PatientContactPoint` record. If no matching record exists the effect will include an error detail with message: `Patient Contact Point does not exist`.

## Caveats

- Emitting this effect will trigger a save to the associated `PatientContactPoint`. If your plugin sends `SendContactVerification` in direct response to a `PATIENT_CONTACT_POINT_UPDATED` event, the save triggered by the effect can cause the same event to fire again, producing an infinite event loop. To avoid this, debounce or detect origin (for example, ignore updates originating from the plugin runner or set a transient flag on the model) before emitting the effect in response to contact point update events.

## Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.send_contact_verification import SendContactVerificationEffect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CONTACT_POINT_CREATED)

    def compute(self) -> list[Effect]:
        contact_point_id = self.event.target
        verification_effect = SendContactVerificationEffec(contact_point_id=contact_point_id)
        return [verification_effect.apply()]
```

## Notes

- This effect only triggers a verification send for the contact point. It does not mark the contact as verified — verification completion is handled by the platform when the patient completes the challenge.
- The effect relies on `PatientContactPoint` existing in the database. If your integration creates contact points in the same operation, ensure they are persisted before emitting this effect.
