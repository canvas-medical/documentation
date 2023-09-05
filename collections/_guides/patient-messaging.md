---
title: "Patient Messaging"
guide_for:
- /api/communication/
- /api/practitioner/
- /api/questionnaireresponse
- /documentation/contact-categories
---

Staying in touch with your patients in between visits is often essential. Checking in with them needs to be frictionless for your clinicians.

{% include alert.html type="danger" content="Canvas uses Twilio and Sendgrid for our built-in messaging capabilities. If you plan on owning the patient messaging, please reach out to support to disable these integrations." %}

* * *
## What you'll learn
In this guide, you will learn how to do the following:
- Send messages to patients
- Write patient messages to Canvas
- Use Questionnaires to check in
<br>
<br>

* * *

### Send messages to patients



The messaging workflow in Canvas allows clinicians to generate an outbound message using free text or templates. Use the notification protocol below to know when a message has been created. The protocol below uses a FHIR call to read all of the attributes of the message created in Canvas so that you can deliver it to your patients and/or their [authorized contacts](documentation/contact-categoried).
``` python
import json
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.protocol import (STATUS_NOT_APPLICABLE,
                                          ClinicalQualityMeasure,
                                          ProtocolResult)
from canvas_workflow_kit.utils import send_notification
import requests


class MessageNotification(ClinicalQualityMeasure):
    class Meta:
        title = 'Message Notification'
        version = 'v0.0.1'
        description = 'Listens for message submission and sends a notification.'
        types = ['Notification']
        compute_on_change_types = [CHANGE_TYPE.MESSAGE]
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

    def get_fhir_communication(self, message_id):
        """ Given a Communication ID we can perform a FHIR Communication Search Request"""
        request = (f"https://fhir-{self.instance_name}.canvasmedical.com/"
             f"Communication?_id={message_id}")
        response = requests.get(
            request,
            headers={
                'Authorization': f'Bearer {self.get_fhir_api_token()}',
                'accept': 'application/json'
            })

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve FHIR Communicaton with {request}")

        return response.json()['entry'][0]['resource']

    def compute_results(self):
        result = ProtocolResult()
        result.status = STATUS_NOT_APPLICABLE

        if self.field_changes['model_name'] == 'messagetransmission':
            self.instance_name = self.settings.INSTANCE_NAME
            self.token = self.get_fhir_api_token()

            canvas_id = self.field_changes.get('fields', {}).get('message_id', None)
            if canvas_id:
                message = self.patient.messages.filter(id=canvas_id[1]).records
                if message:
                    message_id = message[-1]['externallyExposableId']
                    fhir_record = self.get_fhir_communication(message_id)
                    if fhir_record['sender']['reference'].startswith("Practitioner"):
# REPLACE this url with your server url which should receive these notifications

                        send_notification(
                            'https://webhook.site/0a8f7cb1-fcc5-421c-8a99-9c87533cf678',
                            json.dumps(self.get_fhir_communication(message_id)),
                            headers={'Content-Type': 'application/json'})

        return result
```
<br>

* * *

### Write patient messages to Canvas

Patient responses can be written to Canvas using the [FHIR Communication create endpoint](api/communication/#create). They can be assigned to a user through the `recipient` attribute using a practitioner ID. They will appear in the messages inbox in Canvas. 
<br><br> All users in Canvas have a practitioner ID, not just clinicians. By default the [FHIR Practitioner Search](api/practitioner/#search) endpoint will return clinician's that can be scheduled, however, you can include the `includes non-schedulable practitioners` query param to return all staff members.
<br><br>
* * *

### Use questionnaires to check in
You may also want to use a simpler questionnaire to capture data points such as mood, anxiety level, or side effects on a more frequent basis. If you collect this data through your patient-facing application, the [FHIR QuestionnaireResponse create](api/questionnaireresponse/#create) endpoint would allow you to write it to Canvas in a structured way that can be leveraged in reporting or used in protocols.
{:refdef: style="text-align: center;"}
![symptom-tracker](/assets/images/symptom-tracker.png){:width="40%"}
{: refdef}
