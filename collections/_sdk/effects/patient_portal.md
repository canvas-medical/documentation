---
title: "Patient Portal"
slug: "patient-portal"
excerpt: "Patient portal configuration"
hidden: false
---

The Canvas SDK allows you to configure the patient portal.

## Configuring the Patient Portal

To configure the patient portal, you can use the `PatientPortalApplicationConfiguration` effect

| Attribute                 | Type | Description                                                  |
|---------------------------|------|--------------------------------------------------------------|
| can_schedule_appointments | bool | If the patient is allowed to book or reschedule appointments |



```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_portal.application_configuration import PatientPortalApplicationConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol



class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__GET_APPLICATION_CONFIGURATION)


    def compute(self) -> list[Effect]:
        return [
          PatientPortalApplicationConfiguration(
            can_schedule_appointments=True
          ).apply()
        ]

```

## Customize Landing Page

To customize the landing page you can leverage the `Portal Widgets` effect. See <a href="{% link _guides/custom-landing-page.md %}" target="_blank">Tailoring Portal Landing Page</a> for examples.


## Customize Appointment Cards

Customize your patient appointment cards so patients can easily join their telehealth appointments, cancel or reschedule appointments.
Each appointment can be customized individually, allowing each one to have its own unique settings.

### Hide 'Cancel' button


```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__APPOINTMENT_CAN_BE_CANCELED)


    def compute(self) -> list[Effect]:
        return [
          Effect(
            type=EffectType.PATIENT_PORTAL__APPOINTMENT_IS_CANCELABLE,
            payload=json.dumps({"result": False}))
        ]

```

### Hide 'Reschedule' button


```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__APPOINTMENT_CAN_BE_RESCHEDULED)


    def compute(self) -> list[Effect]:
        return [
          Effect(
            type=EffectType.PATIENT_PORTAL__APPOINTMENT_IS_RESCHEDULABLE,
            payload=json.dumps({"result": False}))
        ]

```

### Hide 'Join' button

This button shows on telehealth appointments


```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__APPOINTMENT_CAN_SHOW_MEETING_LINK)


    def compute(self) -> list[Effect]:
        return [
          Effect(
            type=EffectType.PATIENT_PORTAL__APPOINTMENT_SHOW_MEETING_LINK,
            payload=json.dumps({"result": True}))
        ]
```


<br/>
<br/>
<br/>


## Update User

This effect is intended for updating a user’s phone number or email. In the future, we may expand its capabilities to support additional attributes, but for now, only these two are supported.


| Attribute          | Type   | Description                                                  |
|--------------------|--------|--------------------------------------------------------------|
| `user_dbid`        | `str   | UUID`                                                        | The unique ID of the User. |
| `phone_number`     | `str`                                                                 | Specifies the phone number to be stored. |
| `email`            | `str`                                                                 | Specifies the email to be stored. |


```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.update_user import UpdateUserEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import PatientContactPoint


class ContactPoint(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_CONTACT_POINT_UPDATED)]

    def compute(self) -> list[Effect]:
        contact_point = PatientContactPoint.objects.get(id=self.target)
        patient = contact_point.patient

        return [
            UpdateUserEffect(user_dbid=patient.user.dbid, email="test@email.com", phone_number="1234567890").apply(),
        ]
```

<br/>
<br/>
<br/>


## Send Invite

This effect triggers a portal invitation that allows the patient to register or activate their account on the patient portal.


| Attribute          | Type   | Description                                                  |
|--------------------|--------|--------------------------------------------------------------|
| `user_dbid`        | `str   | UUID`                                                        | The unique ID of the User. |


```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.send_invite import SendInviteEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import PatientContactPoint

class ContactPoint(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_CONTACT_POINT_UPDATED)]

    def compute(self) -> list[Effect]:
        contact_point = PatientContactPoint.objects.get(id=self.target)
        patient = contact_point.patient

        return [
            SendInviteEffect(user_dbid=patient.user.dbid).apply(),
        ]
```

<br/>
<br/>
<br/>


## Send Contact Verification

The `SendContactVerification` effect instructs Canvas to send a verification (for example, an email or SMS code) to a specific Patient Contact Point. Typical uses are verifying a patient's email address or phone number before enabling patient-portal features that require a verified contact channel.

| Attribute          | Type            | Description                                    |
|--------------------|-----------------|------------------------------------------------|
| `contact_point_id` | `str` or `UUID` | The id of the [`PatientContactPoint`](/sdk/effect-patient/#patientcontactpoint) to verify. |

### Validation & Errors

When an effect is prepared, the model validates inputs and returns structured error details if something is invalid.

- **Contact Point Exists** — The effect verifies the provided `contact_point_id` maps to an existing `PatientContactPoint` record. If no matching record exists the effect will include an error detail with message: `Patient Contact Point does not exist`.

### Caveats

- Emitting this effect will trigger a save to the associated `PatientContactPoint`. If your plugin sends `SendContactVerification` in direct response to a `PATIENT_CONTACT_POINT_UPDATED` event, the save triggered by the effect can cause the same event to fire again, producing an infinite event loop. To avoid this, debounce or detect origin (for example, ignore updates originating from the plugin runner or set a transient flag on the model) before emitting the effect in response to contact point update events.

### Example Usage

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.send_contact_verification import SendContactVerificationEffect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CONTACT_POINT_CREATED)

    def compute(self) -> list[Effect]:
        contact_point_id = self.event.target
        verification_effect = SendContactVerificationEffect(contact_point_id=contact_point_id)
        return [verification_effect.apply()]
```

### Notes

- This effect only triggers a verification send for the contact point. It does not mark the contact as verified — verification completion is handled by the platform when the patient completes the challenge.
- The effect relies on `PatientContactPoint` existing in the database. If your integration creates contact points in the same operation, ensure they are persisted before emitting this effect.
