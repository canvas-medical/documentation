---
title: "External Scheduling"
guide_for: 
- /api/appointment/
- /api/schedule
- /api/slot/
- /documentation/reason-for-visit-setting-codings/
- /documentation/provider-availability/
- /documentation/appointment-and-note-types/
---

Maximizing scheduling efficiency is necessary to grow and support high volumes of patients. Allowing patients to self schedule offers the potential of creating a better experience, while also saving your care team time. However, it is not as easy as it seems. Patients cannot just have free reign on your calendars. To make it work, the complexities of scheduling needs to be built into the workflow. You may want to build the logic into your own scheduling experience, or leverage a third party partner when first launching. Either way, Canvas’s FHIR API and Workflow Kit enable external systems to completely takeover or supplement scheduling in Canvas. 
<br> 
<br>
* * *
## What you'll learn
In this guide, you will learn how to do the following:
1. Configure scheduling in Canvas
2. Manage appointments through the FHIR API
3. Sync appointments to third party calendars
<br>
<br>

* * *

### 1. Configure scheduling in Canvas

Before you can build external scheduling workflows, you will need to configure Canvas's advanced scheduling capabilities as follows.<br><br>
[Availability:](/documentation/provider-availability/) Provider Availability in Canvas is managed through an integration with Google Calendar. This allows you to set availability using recurring events that are easy to update as needed. Updates made in gCal will reflect within Canvas in minutes. You can set availability at the location level or leave the location empty to have it be set for the clinician across all locations. <br><br>
[Note Types:](/documentation/appointment-and-note-types/) The differentiated care models of our customers often include all types of patient interactions, including in-person visits, telehealth, and asynchronous encounters. You can configure your note types to fit your offering by creating completely custom note types and codes, or leveraging [SNOMED](https://www.snomed.org/).<br><br>
[Appointment Types:](/documentation/appointment-and-note-types/) Creating custom appointment types allows your team to schedule Other Events that block time but do not generate Notes within the Timeline. They can be associated with a specific patient (but do not require one) and can be used to account for meetings, travel time, or co-visits during which multiple clinicians need to be included, but only one note needs to be generated. <br><br>
[Structured Reason for Visit:](/documentation/reason-for-visit-setting-codings/) Structured reason for visit is a setting that can be enabled in Canvas. In doing so you can define a set of reasons and then associate one or more possible durations with each. This can help ensure your team follows set scheduling guidelines. Alternatively, the unstructured option allows the scheduler to free text the reason and choose the duration from any of the configured options. 

<br>
* * *

### 2. Manage appointments through the FHIR API

If you are managing provider provider availability in Canvas you will need to leverage the following two endpoints to surface available time slots:

[FHIR Schedule Search:]({{site.baseurl}}/api/schedule/) The schedule ID returned in the response payload is important when searching for bookable time slots for appointments. The schedule ID allows you to find the staff member's availability at a specific location.<br><br>
[FHIR Slot Search:]({{site.baseurl}}/api/slot/) You'll need to define the logic using your front end or a scheduling partner to determine which schedules to search, using the query params to return availability for clinicians that match based on specialty and/or state licensure. <br>

Then, after determining the, provider, location, date, and time, you can book the appointment: <br>

[FHIR Appointment Create:]({{site.baseurl}}/api/appointment/) You can write both patient appointments or events to Canvas. For appointments, you have the option to create [Structured Reason for Visits]({{site.baseurl}}/documentation/reason-for-visit-setting-codings/). If configured, the codings can be utilized in the FHIR request payload in the `reasonCode` attribute.

<br>

* * *

### 3. Sync appointments and events with third party calendars

<b> Sync appointments made in Canvas to your admin calendar</b><br>
The notification protocol below allows you to watch for changes to appointments. It pushes the changes to a receiving URL, or "Webhook" callback receiver so that you can then write the appointment to your administrative calendars in Google or Outlook. With this, you can control what info is shared, whether you have a BAA with Google and can write PHI, or just need to block time. 

{% include alert.html type="info" content="If you do have a BAA, it might be beneficial to include the patient's address in the calendar event so that field teams can click a link to initiate navigation to the patient. " %}


 ``` python
 import json
import requests

from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.protocol import (STATUS_NOT_APPLICABLE,
                                          ClinicalQualityMeasure,
                                          ProtocolResult)
from canvas_workflow_kit.utils import send_notification
from canvas_workflow_kit.fhir import FumageHelper


class AppointmentNotification(ClinicalQualityMeasure):
    class Meta:

        title = 'Appointment Notification'
        version = 'v1.0.8'
        description = 'Listens for appointment create / update and sends a notification.'
        types = ['Notification']
        compute_on_change_types = [CHANGE_TYPE.APPOINTMENT]
        notification_only = True

    def get_fhir_appointment(self, appointment_id):
        """ Given a Task ID we can perform a FHIR Task Search Request"""
        response = self.fhir.read("Appointment", appointment_id)

        if response.status_code != 200:
            raise Exception("Failed to search Appointments")

        return response.json()

    def get_rescheduled_appointment_id(
            self, appointment):
        for info in appointment.get('supportingInformation', {}):
            if info.get("display") == 'Previously Rescheduled Appointment':
                return info.get("reference").split("/")[1]

        return False

    def get_new_field_value(self, field_name):
        change_context_fields = self.field_changes.get('fields', {})
        if field_name not in change_context_fields:
            return None
        return change_context_fields[field_name][1]

    def get_appointment_by_note_state_event(self, _id):
        for apt in self.patient.appointments:
            state_id = apt.get('state', {}).get('id')
            if state_id == _id:
                return json.loads(json.dumps(apt, default=str))
        return {}

    def compute_results(self):
        result = ProtocolResult()
        result.status = STATUS_NOT_APPLICABLE

        payload = {
            'canvas_patient_key': self.patient.patient['key'],
        }
        changed_model = self.field_changes.get('model_name', '')

        if changed_model == 'notestatechangeevent':
            state = self.get_new_field_value('state')

            state_map = {
                'CLD': 'cancelled',
                'NSW': 'no_show',
                'RVT': 'reverted',
                'CVD': 'checked_in'
            }

            # we only care about cancelled, no-show, reverted, or check-in state changes
            if state not in state_map:
                return result

            appointment = self.get_appointment_by_note_state_event(self.field_changes['canvas_id'])
            payload = {
                **payload,
                'appointment_external_id': appointment.get('externallyExposableId'),
                state_map[state]: True
            }

        elif changed_model == 'appointment':
            self.fhir = FumageHelper(self.settings)
            self.fhir.get_fhir_api_token()

            appointment_id = self.field_changes.get('external_id')
            appointment = self.get_fhir_appointment(appointment_id)

            rescheduled = self.get_rescheduled_appointment_id(appointment)
            created = self.field_changes.get('created')

            payload = {
                **payload,
                'appointment_external_id': self.field_changes.get('external_id'),
                'start_time': appointment.get("start"),
                'end_time': appointment.get("end")
            }

            if created and not rescheduled:
                payload['created'] = True
            elif created and rescheduled:
                payload['rescheduled'] = True
            else:
                return result
        else:
            return result

        # REPLACE this url with your server url which should receive these notifications
        send_notification(
            'https://webhook.site/0a8f7cb1-fcc5-421c-8a99-9c87533cf678',
            json.dumps(payload),
            headers={'Content-Type': 'application/json'})

        return result
```
<br>
<b> Sync meetings scheduled in your admin calendars to Canvas</b>

Most calendar system support similar functionality [(here is Google's)](https://developers.google.com/calendar/api/guides/push), alerting you to changes to events. You can leverage these to then write non-patient events using the [FHIR Appointment Create](/api/appointment/) endpoint.


<br>






