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
