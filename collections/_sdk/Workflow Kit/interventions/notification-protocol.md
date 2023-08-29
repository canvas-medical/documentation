---
title: "Notification Protocol"
---
If you're looking to implement some webhook-style functionality in your Canvas instance that responds to database events, look no further than Notification Protocols! These protocols are similar to regular ones, with two major differences:
* there need not be a UI card presented in the UI (there optionally can be)
* they only compute in response to database events defined in `compute_on_change_types` - they never compute on upload

## Overview

To make your protocol behave as a Notification Protocol, all you need to do to is add `notification_only = True` to the Meta attributes of the protocol class. You'll also want to make sure you have at least one change_type defined in `compute_on_change_types` - otherwise the protocol will never compute at all! 

As a convenience, we offer a utility function called `send_notification` that many of our users find helpful to use in their Notification Protocols. You just need to pass in the url you want to send data to, a payload, and some headers and it will send a POST request for you. 

The code below which just highlights the necessary pieces you'll need to get the notification party started.

``` python
from canvas_workflow_kit.utils import send_notification

class MyNotificationProtocol(ClinicalQualityMeasure):

    class Meta:
        ...
        compute_on_change_types = [CHANGE_TYPE.APPOINTMENT]
        notification_only = True

    def compute_results(self):
        result = ProtocolResult()
        result.status = STATUS_NOT_APPLICABLE
        ...
        send_notification('https://my-url.com', my_payload, my_headers)

        return result
```
<br>

## Appointment Notification Example

You can find the code here: [**Appointment Notification code** ](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/appointment_notifications.py)

This is a protocol that computes whenever there is a change to an Appointment in the Canvas database, and sends a notification to an external server with relevant information about the Appointment. There is no corresponding UI for this protocol, it works purely in the background similar to a webhook. 

In this protocol, we want to send notifications to an external server when an Appointment is:

- created,
- rescheduled
- cancelled
- no showed
- restored/reverted after being cancelled
- checked in

When an appointment is **created**, you should expect a payload like below to be sent to your endpoint:

```json
{
    "canvas_patient_key": "06669a76329f4577bea114bc50072da6",
    "appointment_external_id": "e999b5c7-d12f-498c-816a-f3c66946a911",
    "start_time": "2021-12-24T21:30:00+00:00",
    "end_time": "2021-12-24T22:00:00+00:00",
    "created": true
}
```

When an appointment is **rescheduled**, you can expect a payload like below. Note that this will catch any reschedules that happen in the Canvas UI, as well as via the FHIR API.

```json
{
    "canvas_patient_key": "06669a76329f4577bea114bc50072da6",
    "appointment_external_id": "317d8c8d-6bfc-4d09-bf33-037718cd942a",
    "start_time": "2021-12-24T21:30:00+00:00",
    "end_time": "2021-12-24T22:00:00+00:00",
    "rescheduled": true
}
```

When an appointment is **cancelled**, you can expect a payload like below. 

```json
{
    "canvas_patient_key": "06669a76329f4577bea114bc50072da6",
    "cancelled": true,
    "appointment_external_id": "317d8c8d-6bfc-4d09-bf33-037718cd942a"
}
```

When an appointment that was cancelled is then **restored**, you can expect a payload like below:

```json
{
    "canvas_patient_key": "06669a76329f4577bea114bc50072da6",
    "reverted": true,
    "appointment_external_id": "317d8c8d-6bfc-4d09-bf33-037718cd942a"
}
```

When an appointment is deemed a **no show**, you can expect a payload like below:

```json
{
    "canvas_patient_key": "06669a76329f4577bea114bc50072da6",
    "no_show": true,
    "appointment_external_id": "317d8c8d-6bfc-4d09-bf33-037718cd942a"
}
```

When an appointment is **checked in**, you can expect a payload like below:

```json
{
    "canvas_patient_key": "06669a76329f4577bea114bc50072da6",
    "checked_in": true,
    "appointment_external_id": "317d8c8d-6bfc-4d09-bf33-037718cd942a"
}
```

### Understanding the code

This protocol is specifically triggered by the `CHANGE_TYPE.APPOINTMENT`. There are two models in Canvas that are tied to appointments.  We can see what model was specifically changed by using the `self.field_changes['model_name']` attribute. 

If the model name that changed is the Note State Change Event, we can figure out if the event state is canceled, no showed, reverted, or checked in. Then we further have to fetch the appointment's ID in this scenario. This can be done by looking at the `self.patient.appointments` to find the appointment with the state that ID matches the `self.field_changes['canvas_id']` attribute 

If the model name that changed is the Appointment model itself, we can figure out if the appointment was created for the first time or rescheduled to a different time.