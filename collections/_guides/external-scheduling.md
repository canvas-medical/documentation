---
title: "External Scheduling"

---

Maximizing scheduling efficiency is necessary to grow and support high volumes of patients. Allowing patients to self schedule offers the potential of creating a better experience, while also saving your care team time. However, it is not as easy as it seems. Patients cannot just have free reign on your calendars. To make it work, the complexities of scheduling needs to be built into the workflow. You may want to build the logic into your own scheduling experience, or leverage a third party partner when first launching. Either way, Canvas’s FHIR API and Workflow Kit enable external systems to completely takeover or supplement scheduling in Canvas. 
<br> 
<br>
* * *
## What you'll learn
In this guide, you will learn how to do the following:
- Configure scheduling in Canvas
- Manage appointments through the FHIR API
- Sync appointments to third party calendars
- Send appointment confirmation messages 
<br>
<br>

* * *

### Configure scheduling in Canvas
{% tabs CSIC %}
{% tab CSIC Super Users %}
Before partnering with your dev team to build external schedling workflows, you will need to configure Canvas's advanced scheduling capabilities as follows.<br><br>
[Availability:](https://canvas-medical.zendesk.com/knowledge/articles/360058400553/en-us?brand_id=360005403014&return_to=%2Fhc%2Fen-us%2Farticles%2F360058400553) Provider Availability in Canvas is managed through an integration with Google Calendar. This allows you to set availability using recurring events that are easy to update as needed. Updates made in gCal will reflect within Canvas in minutes. You can set availability at the location level or leave the location empty to have it be set for the clinician across all locations. <br><br>
[Note Types:](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-) The differentiated care models of our customers often include all types of patient interactions, including in-person visits, telehealth, and asynchronous encounters. You can configure your note types to fit your offering by creating completely custom note types and codes, or, you can use an established system such as [LOINC®](https://loinc.org/LG41826-5) codes.<br><br>
[Appointment Types:](https://canvas-medical.zendesk.com/hc/en-us/articles/15704289792659-Scheduling-Other-Events-#h_01GXV9832Z74GRAQKDD4JA9677) Creating Custom Appointment Types allows your team to schedule Other Events that block time but do not generate Notes within the Timeline. They can be associated with a specific patient (but do not require one) and can be used to account for meetings, travel time, or co-visits during which multiple clinicians need to be included, but only one Note needs to be generated. <br><br>
[Structured Reason for Visit:](https://canvas-medical.zendesk.com/hc/en-us/articles/4417495811859-Structured-Reason-for-Visit) Structured Reason for Visit is a setting that can be enabled in Canvas. In doing so you can define a set of reasons and then associate one or more possible durations with each. This can help ensure your team follows set scheduling guidelines. Alternatively, the unstructured option allows the scheduler to free text the reason and choose the duration from any of the configured options. 

{% endtab %}
{% tab CSIC Developers %}
After your team completes the scheduling set up in Canvas, you will want to take note of the naming conventions and code systems used. You can access them in the associated admin menus. 

{% endtab %}
{% endtabs %}
<br>
* * *
### Manage appointments through the FHIR API
{% tabs MAPP %}
{% tab MAPP Developers %}
If you are managing provider provider availability in Canvas you will need to leverage the following two endpoints to surface available timeslots:

[FHIR Schedule Search:]({{site.baseurl}}/api/schedule/) The schedule ID returned in the response payload is important when searching for bookable time slots for appointments. The schedule ID allows you to find the staff’s availability at a specific location.<br><br>
[FHIR Slot Search:]({{site.baseurl}}/api/slot/) You'll need to define the logic using your front end or a scheduling partner to determine which schedules to search, using the query params to return availability for clinicians that match based on, specialty and/or state licensure. <br>

Then, after determining the date and time, you can book the appointment: <br>

[FHIR Appointment Create:]({{site.baseurl}}/api/appointment/) You can write both patient appointments or events to Canvas. Events do not require a patient and are great for blocking time. For appointments, you have the option to create [Structured Reason for Visits](https://canvas-medical.zendesk.com/hc/en-us/articles/4417495811859-Structured-Reason-for-Visit). If configured, the codings can be utilized in the FHIR request payload in the reasonCode attribute.

{% endtab %}
{% tab MAPP Super Users %}
Make sure to update your team when you update your note and appointment types in Canvas. Also note that appointments made using the API will show as scheduled by "Canvas Bot".
{% endtab %}
{% endtabs %}
<br>
* * *

### Sync appointments and events with third party calendars
{% tabs SATP %}
{% tab SATP Developers %}
<b> Sync appointments made in Canvas to your admin calendar</b><br>
The notification protocol below allows you to watch for changes to appointments. It pushes the changes to a receving URL, or "Webhook" callback receiver so that you can then write the appointment to your administrative calendars in Google or Outlook. With this, you can control what info is shared, whether you have a BAA with Google and can write PHI, or just need to block time. 

{% include alert.html type="info" content="If you do have a BAA, it might be beneficial to include the patient's address in the calendar event so that field teams can click a link to initiate navigation to the patient. " %}


 ``` python
 import json
import requests

from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.protocol import (STATUS_NOT_APPLICABLE,
                                          ClinicalQualityMeasure,
                                          ProtocolResult)
from canvas_workflow_kit.utils import send_notification


class AppointmentNotification(ClinicalQualityMeasure):
    class Meta:

        title = 'Appointment Notification'
        version = 'v1.0.8'
        description = 'Listens for appointment create / update and sends a notification.'
        types = ['Notification']
        compute_on_change_types = [CHANGE_TYPE.APPOINTMENT]
        notification_only = True

    def get_fhir_api_token(self):
        """ Given the Client ID and Client Secret for authentication to FHIR,
        return a bearer token """

        grant_type = "client_credentials"
        client_id = self.settings.CLIENT_ID
        client_secret = self.settings.CLIENT_SECRET

        token_response = requests.request(
            "POST",
            f'https://{self.instance_name}.canvasmedical.com/auth/token/',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
        )

        if token_response.status_code != 200:
            raise Exception('Unable to get a valid FHIR bearer token')

        return token_response.json().get('access_token')

    def get_fhir_appointment(self, appointment_id):
        """ Given a Task ID we can perform a FHIR Task Search Request"""
        response = requests.get(
            (f"https://fhir-{self.instance_name}.canvasmedical.com/"
             f"Appointment/{appointment_id}"),
            headers={
                'Authorization': f'Bearer {self.get_fhir_api_token()}',
                'accept': 'application/json'
            }
        )

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
            self.instance_name = self.settings.INSTANCE_NAME
            self.token = self.get_fhir_api_token()

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

Most calendar system support similar functionality [(here is Google's)](https://developers.google.com/calendar/api/guides/push), alerting you to changes to events. You can leverage these to then write non-patient events to Canvas to block time. 

{% endtab %}
{% tab SATP Super Users %}
Your clinicians may be part time or juggling both clinical hours and internal meetings. Make sure to set up your appointment and note types to support these syncing workflows. It may be helpful to map out with your developers what changes should intitiate an update in each system. 
{% endtab %}
{% endtabs %}
<br>
* * *






