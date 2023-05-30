---
title: "Care Modeling: Behavioral Health"
guide_for:
 - /api/patient/
 - /api/coverage/
 - /api/consent/
 - /api/questionnaireresponse/
 - /documentation/configuringquestionnaires/
---

Canvas is purpose built to accommodate every stage and scale for care delivery organizations such as yours. This is absolutely true for behavioral health. Canvas can meet your ever-evolving needs, whether you are building a cash-pay digital mental health clinic, an evidence-based treatment program targeting Medicare/Medicaid, or any meaningful behavioral health care model in between. 

This guide applies our Care Modeling framework to Behavioral Health and provides relevant examples of how to implement various Canvas capabilities for each of the seven elements of Care Modeling. 

### **Canvas for Behavioral Health**
To understand why Canvas can effectively support all specialties and care models, we must start with the basics. The Canvas approach to charting is fundamentally different. Most of today's EMR's work like cash registers, treating patient interactions as transactional. We invented Narrative Charting in order to model the actual work of the clinician instead. We start all of our notes with a blank Canvas and allow you to pull in Commands to document what is relevant for that patient and interaction. This works extremely well for behavioral health, as our application doesn't force your clinicians to navigate through a set workflow or the typical SOAP note, if it's not necessary to do so. 

In addition to our entirely new way of charting, our FHIR API and Workflow Kit make Canvas extremely extensible. You can build both a differentiated patient experience and influence the in-application workflows using the available read and write endpoints, and protocols. 

Canvas is not just an EMR, we are a Care Modeling platform. Choosing Canvas allows you to iterate quickly on what differentiates your offering. The behavioral health applications below are only a starting point to give you some ideas of how you **could** leverage Canvas's capabilities.


### **Patient Sourcing and Intake**
Strategy around how you source and onboard new patients is necessary to successfully attract and connect with individuals in need of mental health services, establish a positive first impression, gather comprehensive patient information, and prioritize the well-being and safety of patients throughout their care journey.

#### Creating your Patient Profiles

Whether you are **sourcing patients** from your direct-to-consumer site, getting patient lists through a payer relationship and/or leveraging a CRM, **our FHIR API will enable you to create and update your patient profiles within Canvas** with all of the necessary demographic information to get started. The endpoints listed below are the most commonly utilized to do so.


[**`Patient:`**](https://main.d298pum72820gn.amplifyapp.com/api/patient/) The create and update endpoints allow you to sync the patient's demographic data, including addresses, contact methods, patient preferences, patient contacts, and more. 

[**`Coverage:`**](https://main.d298pum72820gn.amplifyapp.com/api/coverage/)  Whether you are billing to commercial insurance plans, or need to add custom employer-based coverages, the Coverage endpoint can be leveraged to add a Patient's coverage information. We populate the [initial list of available insurers](https://www.claim.md/payer_list.html) through our integration with ClaimMD. Additional coverage options such as employee programs can be added and updated following [these steps](https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers). The ID associated with each insurer is needed to create the coverage through the API. 

[**`Consent:`**](https://main.d298pum72820gn.amplifyapp.com/api/consent/) Consents also have to be [configured](https://canvas-medical.zendesk.com/hc/en-us/articles/5524511564947-Patient-Consents) before they can be added through the API. The `ConsentCoding` cannot be changed once created, so make sure to configure your consents with that in mind. In addition to recording the consent, you can attach a PDF version using the `sourceAttachment` attribute. This attachment will be available in the admin documents within the chart, and linked to the consent recorded in the patient's profile. 

#### Surfacing custom data points using Banner Protocols
The `identifier` attribute on the `patient` resource is a great place to store unique identifiers and additional data for that patient that does not fit elsewhere. With a cardinality of zero to many, you can use the `identifier` attribute to store multiple values. Although `identifiers` added through the API do not display in the Canvas UI by default, this Banner Alert Protocol can be used to surface the information to your end users. You can update both [`alertplacement` and `alertintent`](https://docs.canvasmedical.com/docs/banner-alerts-for-contacts#alertplacement) in the code below as needed. 

[//]: # (TODO Reba Check the code below) 

```python 
from canvas_workflow_kit.protocol import (
    ClinicalQualityMeasure,
    ProtocolResult,
    STATUS_DUE,
    STATUS_SATISFIED
)
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.recommendation import Recommendation
from canvas_workflow_kit.intervention import BannerAlertIntervention
class ExternalIdentifierBanner(ClinicalQualityMeasure):
    class Meta:
        title = 'External identifier banner'
        description = 'Display any external identifiers in a banner'
        version = '2022-05-10v8'
        information = 'https://docs.canvasmedical.com'
        identifiers = ['external_identifier']
        types = ['CQM']
        compute_on_change_types = [
            CHANGE_TYPE.PATIENT
        ]
        references = [
            'NA'
        ]
    def in_denominator(self):
        """
        Patients with at least one external identifier.
        """
        external_identifiers = self.patient.patient["externalIdentifiers"]
        if len(external_identifiers) > 0:
            return True
        else:
            return False
    def in_numerator(self):
        """
        Patients that have already been notified.
        """
        return False
    def compute_results(self):
        result = ProtocolResult()
        if self.in_denominator():
            if self.in_numerator():
                result.status = STATUS_SATISFIED
                result.add_narrative(
                    'Placeholder text'
                )
            else:
                result.status = STATUS_DUE
                result.due_in = -1
                result.add_narrative(
                    f'{self.patient.first_name} has external identifer(s)'
                )
                external_identifiers = self.patient.patient["externalIdentifiers"]
                for external_identifier in external_identifiers:
                    result.recommendations.append(
                        BannerAlertIntervention(
                            narrative=(f"{external_identifier['system']}: {external_identifier['value']}"),
                            placement=['profile'],
                            intent='info')
                        )
        return result     
```

#### Incorporating patient collected data with Questionnaires

Leading up to a scheduled appointment, you can streamline **patient intake** by writing patient data that has been collected in your patient application to Canvas through our FHIR API.

**`QuestionnaireResponse Create:`** The `QuestionnaireResponse` endpoint can be used to capture structured data through the use of custom forms. Questionnaires must first be [configured](https://main.d298pum72820gn.amplifyapp.com/documentation/ConfiguringQuestionnaires/) in your Canvas instance. Your team can utilize our no-code google sheet template to build, update, and load questionnaires into Canvas. 

<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTIe3s2zh0FAZMaIxaxg2EQ5x7ot4U4iSX95tLNClkNvQ4LQAr_qZm6b9nmdG68xDf4NdeNqEIvKlpo/pubhtml?gid=2051129171&amp;single=true&amp;widget=true&amp;headers=false" width=800px height=600px ></iframe>

They are designed to be code-backed to ensure that you can interact with them programmatically. Make sure to coordinate across your Clinical Operations, Engineering and Product teams to set them up with unique codes, using our supported code systems. We do offer some pre-built questionnaires, including many common behavioral health assessments such as the PHQ-9 shown above.<Br>

```
💡Evaluating Canvas? To load this PHQ-9 questionnaire into your sandbox, navigate to Settings>Practice>Questionnaire
Loader or to: https://{sandboxname}-preview.canvasmedical.com/admin/api/questionnaireloader/ and paste in the following:
```

**Google Sheet ID:** 1RIYAvyp62EOlQ6DPRV4tRPyca8xgEbg4z2vGo_EEhT4<br>
**Google Sheet tab name:** ques-PHQ9-all<br>

You may want your patients to complete these assessments, or your custom built workflows, prior to their visit. **Canvas Notes are meant to be collaborative and authored by multiple people, including the patient**. When adding patient-collected data you can set the `author` attribute to `patient/{patientkey}`. Doing so will then be visible within the Command history tool-tip in the Note.

#### Supercharging your patient onboarding with Canvas + Zus 🔱 

If you find that your care team is spending countless hours hunting down your patient's historical records and converting them to structured data, the **Canvas + Zus integration** may be a game changer.  Clinicians can leverage the Zus Aggregated Profile (ZAP) to insert relevant patient data (historical medications, conditions, labs, and encounters sourced from various HIEs and proprietary data networks) directly into Canvas profiles in actionable ways. Learn more about our Partner ship with Zus [here](https://www.prnewswire.com/news-releases/canvas-medical-and-zus-announce-strategic-product-partnership-redefining-the-speed-and-effectiveness-of-collaborative-development-in-healthtech-301736901.html) . 

### **Ongoing Interaction Modes and Utilization Policies**

Understanding and effectively managing interaction modes in your behavioral healthcare model is crucial to providing a seamless and efficient patient experience. Implementing interconnected synchronous and asynchronous communication channels, guided by well-structured Utilization Policies, can streamline your operations, enhance patient engagement, and ultimately improve care outcomes. 

#### Configuring Canvas to support your scheduling needs

Maximizing scheduling efficiency is necessary to grow and support high volumes of patients. Our advanced scheduling capabilities can be configured to support your needs as follows:

[**Availability in Canvas**](https://canvas-medical.zendesk.com/knowledge/articles/360058400553/en-us?brand_id=360005403014&return_to=%2Fhc%2Fen-us%2Farticles%2F360058400553) is managed through and integration with Google Calendar. This allows you to set availability using recurring events that are easy to update as needed. 

**Note Types:** Releasing [**configurable Note Types**](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-) was tightly aligned with our strategy shift away from focusing solely on primary care. The differentiated care models of our customers often include all types of patient interactions, including in-person visits, telehealth, and asynchronous encounters. You can configure your note types to fit your behavioral health offering by creating completely custom note types and codes, or, you can use an established system such as the [LOINC®](https://loinc.org/LG41826-5) codes listed below. <br><br>
18776-5	Plan of care note <br>
28628-6	Psychiatry Note<br>
34792-2	Psychology Note<br>
28653-4	Social worker Note<br>
34786-4	Mental health Note<br>
34748-4 Telephone encounter Note<br>
34790-6	Psychiatry Group counseling note<br>
34793-0	Psychology Group counseling note<br>
34787-2	Mental health Group counseling note<br>

**Appointment Types:** [Creating Custom Appointment Types](https://canvas-medical.zendesk.com/hc/en-us/articles/15704289792659-Scheduling-Other-Events-#h_01GXV9832Z74GRAQKDD4JA9677) allows your team to schedule other events that block time but do not generate Notes within the Timeline. They can be associated with a specific patient (but do not require one) and can be used to account for meetings, travel time, or co-visits during which multiple providers need to be included, but only one Note needs to be generated. 

#### Scheduling with the Canvas API
Once your availability has been set, you can use the following endpoints to build out your own patient-facing scheduling platform or integrate with an existing offering. <br>

[//]: # (TODO Kristen to expand on importance callouts for each resource)
[**`schedule:`**](https://main.d298pum72820gn.amplifyapp.com/api/schedule/#schedule-search)The schedule id here is important when searching for bookable time slots for appointments.<br> 
[**`slot:`**](https://main.d298pum72820gn.amplifyapp.com/api/slot/) You can define your own scheduling logic, using the query params to only return availability for providers that match based on specialty and/or state licensure. <br>
[**`appointment:`**](https://main.d298pum72820gn.amplifyapp.com/api/appointment/) Our customers have the option to create [structured Reasons for Visits](https://canvas-medical.zendesk.com/hc/en-us/articles/4417495811859-Structured-Reason-for-Visit). If configured, the associated IDs are necessary to write appointments to Canvas. 

#### Syncing clinical and administrative calendars
Your providers may be part time or juggling both clinical hours and internal meetings. Syncing clinical and administrative calendars is often a must. You can use the [notification protocol](https://docs.canvasmedical.com/docs/notification-protocol) below to know when an appointment has been created or updated in Canvas and use it to write that appointment to your administrative calendars in Google or Outlook. With this, you can control what info is shared, whether you have a BAA with Google and can write PHI, or just need to block time. You can also block time in Canvas through the API by writing Other Events through the appointment endpoint. 
```
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
#### Communicating with your patients in between visits
Staying in touch with your patients in between visits is often essential. Checking in with them needs to be frictionless for your providers. The messaging workflow in Canvas allows clinicians to generate an outbound message using free text or templates. Use the notification protocol below to know when a message has been created. The protocol below uses a FHIR call to then read all of the attributes of the message created in Canvas so that you can deliver to your patient's and/or authorized their contacts, as needed.  

 💡 Canvas uses Twilio and Sendgrid for our built-in messaging capabilities. You will need to disable these in order to takeover the patient messaging experience. 

 [//]: # (TODO: Notification protocols are also a great way to kick off automated follow up communications. You can trigger them based on many events within the Chart, including signing a Note. After the visit is over, the notification protocol can be used to pass information from the patient encounter to your patient application. The example below shows how you can use a notification protocol to pull Healthwise content using our documentreference read endpoint. Add notification protocol - signing the note - pulling instruct command and fhir documentreference healthwise content)

Patient responses can be written to Canvas using the `communication` create endpoint. They can be assigned to a user through the  `recipient` attribute, which ingests either a patient or practitioner reference. All users in Canvas have a practitioner ID, not just clinicians. The `practitioner` search includes a query param to include non-schedulable providers. 

### **Diagnostic Range and Inputs**
What is your target population? Does your care model support a broad range of mental health concerns for all genders and ages (everything in the DSM), or are you hyper focused on adolescents suffering from eating disorders. Recognizing your Diagnostic Range is vital, as it informs the complexity of your healthcare practice and determines the technological aids necessary for effective patient care. 

#### Using Plugins to limit the Condition Search
When diagnosing a patient, our default is to surface all 71,920+ current ICD-10 codes. These may be necessary for a full scope Primary Care/Urgent Care practice but you likely only need a fraction of those available to account for the mental health issues you have chosen to focus on and their comorbidities. Recognizing that too many options can often be overwhelming, our plugins allow you to remove the unnecessary noise. The plugin below 

`Condition Search Annotation and Limiting`

#### Leveraging Behavioral Health assessments

Well established assessment tools remain a cornerstone of care models centering around the human mind. Mental health professionals depend on these tools to make decisions about the best course of treatment for their patient. Canvas offers many pre-built assessments ready to load in your instance, including:

<ul>
<li>PHQ-2</li>
<li>PHQ-9</li>
<li>GAD-2</li>
<li>GAD-7</li>
<li>ADHD self-report scale</li>
</ul>

💡 We provide publicly available screening questionnaires and assessments to get you started. If you have the appropriate permissions/licensing to reuse copyrighted content, you are able to build and load those using our Questionnaire Google Sheet template as needed. 

You may also want to use a much simpler questionnaire to capture data points such as mood, anxiety level, or side effects on a more frequent basis. If you capture this data through your patient facing application, a questionnaires would allow you to write it to Canvas in a structured way that can be leveraged in reporting or used in Protocols. 

### **Scope of Interventions and Safety Framework**
An essential part of defining your care model is determining what services and treatments you plan to offer. As your Scope of Interventions broadens - and your care model gets more complex - you will need to apply more rigor in your safety framework

#### Narrative Charting for Behavioral Health
We have built over [40 Commands](https://canvas-medical.zendesk.com/hc/en-us/sections/360011167953-Charting-Commands-Library) to support both diagnostic interventions like labs, imaging, and consults as well as therapeutic interventions like medications, instructions, exercises, referrals, and enrollments. The Commands you use most will be dictated by the scope of the interventions you offer. 

#### Securing your team's use of Canvas with Permissions
Privacy is critical when dealing with mental health and designating user privileges is a critical aspect of medical record security. Knowing that each of our customers has unique needs, we developed a flexible framework for [permissions](https://canvas-medical.zendesk.com/hc/en-us/articles/13143167734291-User-permissions). Our customers can define permissions along two dimensions, allowing administrators to ensure that users only have the necessary access needed to fulfill their roles and responsibilities. <br>

**Object permissions:** “Object” in this case means “Patient”. These permissions control which users can access which patients. Defining groups of patients can be accomplished manually, or using a protocol to define a group based on a certain attribute, such as the patient's home state, care team composition, or another data point (maybe even using the identifier attribute noted above). The protocol below defines a group based on their home state. <br>

```
Patient Group Example
```

**Model permission:s**. These essentially assign read and write access for different parts of the app. If a staff has read/write access to the clinical chart, they can write notes, enter commands, mutate patient data, etc. If they have read-only access, they can see all clinical data but make no changes. If they have no access, they will not be able to see the clinical chart, nor any clinical data present in other parts of the app (like Labs, Imaging, etc.). 


#### Using Protocols to and promote patient safety
Healthcare has come a long way since the US Institute of Medicine published its landmark To Err is Human report in 1999. While patients are safer, practicing evidence-based medicine is often still too hard. Our Workflow Kit allows you to program complex clinical logic into the the point of care. Recommendations, presented as either protocol cards and banners, allow you to surface care gaps or safety risk within the clinicians workflow. The example below surfaces a recommendation to switch a patient's schizophrenia medication from Olanzipine to Ziprasidone if diabetes is added to the condition list. 

```python
from canvas_workflow_kit import events
from canvas_workflow_kit.protocol import (ClinicalQualityMeasure,
                                          ProtocolResult, STATUS_DUE,
                                          STATUS_SATISFIED)
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.recommendation import PrescribeRecommendation
from canvas_workflow_kit.value_set.value_set import ValueSet

from canvas_workflow_kit.value_set.v2021 import Diabetes

class ValueSetWithNDC(ValueSet):
    value_systems = [*ValueSet.value_systems, 'NDC']

class ZiprasidoneMed(ValueSet):
    VALUE_SET_NAME = 'ziprasidone'
    RXNORM = {'314286'}    

class ZiprasidoneNewRx(ValueSetWithNDC):
    VALUE_SET_NAME = 'ziprasidone 20 mg capsule'
    NDC = {'00049005260'}
    RXNORM = {'314286'}
    FDB = {222887}

class Olanzapine(ValueSet):
    VALUE_SET_NAME = 'Olanzapine'
    RXNORM = {'314154','312078','331548'}

class ZiprasidoneRx(ClinicalQualityMeasure):
    """
    A protocol with a prescribe button recommendation that inserts a 
    completed prescribe command
    """

    class Meta:

        title = 'Ziprasidone recommendation'
        version = 'v1.0.19'
        description = 'If a patient on olanzapine has diabetes, recommend ziprasidone'
        information = 'https://canvasmedical.com/'
        identifiers = ['Prescribe']
        types = ['Orders']
        responds_to_event_types = [
            events.HEALTH_MAINTENANCE,
        ]

        compute_on_change_types = [
            CHANGE_TYPE.MEDICATION, CHANGE_TYPE.CONDITION
        ]
        authors = ['Canvas Medical']
        references = ['Canvas Medical']
        funding_source = ''

    diabetes = None

    def in_denominator(self):
        """
        Patients with diabetes on olanzapine.
        """
        diabetes_conditions = self.patient.conditions.find(Diabetes).filter(
            clinicalStatus='active')

        if not diabetes_conditions:
            return False

        if len(self.patient.medications.find(Olanzapine).filter(status='active')) == 0:
            return False

        self.diabetes = diabetes_conditions[0]
        return True

    def in_numerator(self):
        """
        Patients that are already on ziprasidone
        """
        return len(
            self.patient.medications.find(ZiprasidoneMed).filter(status='active')) > 0

    def compute_results(self):
        result = ProtocolResult()
        if self.in_denominator():
            if self.in_numerator():
                result.status = STATUS_SATISFIED
            else:
                result.due_in = -1
                result.status = STATUS_DUE
                result.add_narrative(
                    'Ziprasidone may be preferred to Olanzapine in patients with diabetes.')
                title = 'Ziprasidone 20 mg tablet'
                prescribe_recommendation = PrescribeRecommendation(
                    key='RECOMMEND_ZIPRASIDONE',
                    rank=1,
                    button='Prescribe',
                    patient=self.patient,
                    prescription=ZiprasidoneNewRx,
                    title=title,
                    narrative=result.narrative)
                conditions = [
                    coding for coding in self.diabetes['coding']
                    if coding['system'] == 'ICD-10'
                ]
                prescribe_recommendation.context = {
                    'conditions': [conditions],
                    'dosage_form': 'capsule',
                    'sig_original_input': '1 tab by mouth twice per day',
                    'duration_in_days': 30,
                    'dispense_quantity': 60,
                    'dosage_form': 'tablet',
                    'count_of_refills_allowed': 2,
                    'generic_substitutions_allowed': True,
                    'note_to_pharmacist': ''
                }
                result.add_recommendation(prescribe_recommendation)

        return result
```


### **Care Team Composition and Sourcing**
Understanding and properly structuring your care team is critical to meet the unique and diverse needs of your patients. This requires a careful balance between productivity and experience levels to ensure optimal care without compromising safety. The team structure influences how effectively you can manage your Diagnostic Range and Scope of Interventions, ultimately impacting the quality of mental health services you deliver.

#### Setting up your Care Teams in Canvas<br>
Canvas was built to support team-based delivery. During implementation, you will set up Roles, Teams, and Care Teams to ensure your team can collaborate effectively.  


[**Roles:**](https://canvas-medical.zendesk.com/hc/en-us/articles/12851926883859-Creating-and-modifying-roles) are configurable in Canvas and can drive a default permissions set though Auth Groups. 

[**Teams**](https://canvas-medical.zendesk.com/hc/en-us/articles/360057499933-Admin-Teams) are used to group work. By assigning responsibilities to teams, you can drive how automated tasks in Canvas are assigned. For instance, you may want all all delegated referrals to go to a care coordination team. You can read and search Team participation using the [`group`](https://docs.canvasmedical.com/reference/group-search) endpoint. 

[**Care Teams:**](https://canvas-medical.zendesk.com/hc/en-us/articles/4409741845011-Care-Teams) Care teams are used to define the role an individual plays in a patient's care. Once created you can assign staff to patients with a Care Team role. Designating a team lead will drive default assignment for items coming into Canvas needing clinical review (if not directed to a specific staff member). Members of the care team are also prioritized in the drop down when assigning items in Canvas. 

#### Routing Automated Tasks to Teams using Protocols
Our Teams setup allow you assign the Canvas automated tasks to a team; however, the way we've grouped responsibilities may not be granular enough for you. If you have multiple teams that should be coordinating referrals or communicating diagnostic results, you can leverage protocols to update team assignment based on the details of the task once created. The example below looks for the task name `referral_task_title = "Refer patient to Psychiatry (TBD)"`,  updates the team assignment to a different team, and adds a label. 

`Route Referrals to correct Team Protocol` 

```python
import requests
from canvas_workflow_kit import events
from canvas_workflow_kit.protocol import ClinicalQualityMeasure, ProtocolResult
from canvas_workflow_kit.constants import CHANGE_TYPE


class BehvaioralReferralTaskUpdate(ClinicalQualityMeasure):
    """
    This protocol updates the label and team for a task created from a behavioral health referral.
    """

    class Meta:
        title = "Behavioral Referral Task Update"
        version = "2023-v01"
        description = "This protocol updates the label and team for a task created from a behavioral health referral. "
        information = "https://link_to_protocol_information"
        identifiers = ["BehvaioralReferralTaskUpdate"]
        types = ["CQM"]
        responds_to_event_types = [
            events.HEALTH_MAINTENANCE,
        ]
        compute_on_change_types = [CHANGE_TYPE.TASK]
        authors = ["Canvas Example Medical Association (CEMA)"]
        notification_only = True

    token = None
    task_id = None

    behavioral_group_fhir_id = "Group/895037a1-98ea-432b-a42b-5727a40ba2ca"
    behavioral_group_name = "Behavioral Health Coordinators"
    internal_referral_label = "Internal Referral"
    referral_task_title = "Refer patient to Psychiatry (TBD)"

    def get_fhir_api_token(self):
        """Given the Client ID and Client Secret for authentication to FHIR,
        return a bearer token"""

        grant_type = "client_credentials"
        client_id = self.settings.CLIENT_ID
        client_secret = self.settings.CLIENT_SECRET

        token_response = requests.request(
            "POST",
            f"https://{self.settings.INSTANCE_NAME}.canvasmedical.com/auth/token/",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}",
        )

        return token_response.json().get("access_token")

    def get_fhir_task(self):
        """Given a Task ID, request a FHIR Task Resource"""
        if not self.token or not self.task_id:
            return None

        bundle = requests.get(
            (
                f"https://fhir-{self.settings.INSTANCE_NAME}.canvasmedical.com/"
                f"Task?identifier={self.task_id}"
            ),
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        ).json()

        resources = bundle.get("entry", [])
        if len(resources) == 0:
            return None

        return resources[0].get("resource")

    def update_fhir_task(self, task):
        """Given a Task ID and Task Resource perform a FHIR Task Update"""
        if not self.token or not self.task_id:
            return None

        return requests.put(
            (
                f"https://fhir-{self.settings.INSTANCE_NAME}.canvasmedical.com/"
                f"Task/{self.task_id}"
            ),
            json=task,
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )

    def edit_task(self, task):
        # update behavioral team to owner
        new_extension = {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
            "valueReference": {
                "reference": self.behavioral_group_fhir_id,
                "display": self.behavioral_group_name,
            },
        }
        extension = [*task.get("extension", []), new_extension]

        # add label
        new_input = {
            "type": {"text": "label"},
            "valueString": self.internal_referral_label,
        }
        input = [*task.get("input", []), new_input]

        new_task = task | {"extension": extension, "input": input}
        return {k: v for k, v in new_task.items() if k != "note"}

    def is_a_referral_task(self, task_id):
        """Returns true if the task has the title given to Behavioral Referral tasks"""
        return (
            len(
                self.patient.tasks.filter(
                    externallyExposableId=task_id, title=self.referral_task_title
                )
            )
            == 1
        )

    def compute_results(self):
        if not (token := self.get_fhir_api_token()):
            return result
        self.token = token

        result = ProtocolResult()

        field_changes = self.field_changes or {}
        task_id = str(field_changes.get("external_id", ""))
        created = field_changes.get("created") == True
        if not created or not task_id or not self.is_a_referral_task(task_id):
            return result

        self.task_id = task_id
        if not (task := self.get_fhir_task()):
            return result

        self.update_fhir_task(self.edit_task(task))

        return result
```

### **Content and Automation**
In the context of care modeling, content falls into two buckets: patient-facing content which includes questionnaires, instructions, and educational materials; and care team-facing content including diagnostic guidelines, micro-templates, clinical quality measures (CQMs), and treatment standards of care. Since we've already touched how we make content available through commands, questionnaires, educational material, and protocols, we are going to focus on how we can automate it's use. 

#### Speed up documentation using Automations

[Automations](https://canvas-medical.zendesk.com/hc/en-us/articles/360059338953-Automations) are a key feature in Canvas that allow you to sequence many Commands together. Think of these as Macros in Excel / Google Sheets, but supercharged for clinical context. Below, you'll find an example of a “Major Depressive Disorder” automation you could create. Once building the Automation, every time you diagnose MDD, you can enter the Automation to surface the Commands in sequence, adjusting where relevant to fit the needs of your patient. 

Questionnaire - PHQ-9 <br>
Perform - CPT Code 90801: Psychiatric diagnostic interview examination<br>
Diagnose - Major Depressive Disorder<br>
Prescribe - Fluoxetine 40, take once per day with or without food <br>
Instruct - Depression Education <br>
new

![MDD Automation](https://github.com/canvas-medical/documentation/assets/91080969/5cc17b2b-6a82-4609-9bb7-3e33e29e917b)

💡When building Automations, it may be useful to add a few most commonly used options. For instance, you may typically prescribe one of two antidepressants when beginning treatment. If you add both to your Automation, it is easy to X out the one you don't need. 


#### Enforce Standards of Care with Protocols. 
This is an area where we really shine 🌟. We used our own SDK to build dozens of Protocols that call out gaps in care, present actions to take at the point of care, and capture and manage quality data at the patient and population levels. You can leverage those that are relevant for behavioral health and deactivate those that are not. You can also build out Protocols your own based on your Care Model. The example below shows one application (recommending a follow up appointment and creating a task when a patient has an elevated PHQ-9) but the possibilities are truly endless. You get to decide where and when you think it is necessary to insert guidance and then can measure outcomes to determine the efficacy of your interventions. Care Modeling requires iteration. Our workflow kit allows you to implement, evaluate, and update interventions at a rapid pace so that you can quickly differentiate from your competitors. 

```python
import arrow
import requests
import json

from canvas_workflow_kit import events
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.protocol import (
    STATUS_DUE,
    STATUS_SATISFIED,
    ClinicalQualityMeasure,
    ProtocolResult,
)
from canvas_workflow_kit.recommendation import FollowUpRecommendation, ReferRecommendation
from canvas_workflow_kit.value_set.value_set import ValueSet


class QuestionnairePhq9(ValueSet):
    VALUE_SET_NAME = "PHQ-9 Questionnaire"
    LOINC = {"44249-1"}


TELEHEALTH_NOTE_TYPE_CODE = '448337001'

APPOINTMENT_CANCELLED_STATUSES = [
    "cancelled",
    "noshowed",
    "entered-in-error",
    "noshow"
]

class FollowUpElevatedPHQ9(ClinicalQualityMeasure):
    """
    This protocol recommends a follow-up behavioral appointment for patients with a PHQ9 score >= 10
    It also creates a Task for someone to schedule the follow up
    """

    class Meta:
        title = "Follow Up: Elevated PHQ-9"

        version = "2023-v01"

        description = "This protocol recommends a follow-up appointment for patients with a PHQ9 score >= 10"

        information = "https://link_to_protocol_information"

        identifiers = ["FollowUpElevatedPHQ9"]

        types = ["CQM"]

        responds_to_event_types = [
            events.HEALTH_MAINTENANCE,
        ]

        compute_on_change_types = [CHANGE_TYPE.INTERVIEW, CHANGE_TYPE.APPOINTMENT]

        authors = ["Canvas Example Medical Association (CEMA)"]

        score = None
        interview_time = None

        notification_only = True # If True the protocol will no recompute on upload


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

    def get_care_coordination_group(self):
        return "4dfcb0f8-3594-4195-8870-32464756ae47"

        # Below is the request to make if you want to programatically fetch the group
        # but most of the time these values are stable per instance and we want to reduce calls

        # response = requests.request(
        #     "GET",
        #     f"https://fhir-{self.instance_name}.canvasmedical.com/Group",
        #     headers={
        #         'Authorization': f'Bearer {self.token}',
        #         'accept': 'application/json'
        #     },
        # )

        # if response.status_code != 200:
        #     raise Exception("Unable to search FHIR Group")

        # for entry in response.json()['entry']:
        #     resource = entry['resource']
        #     if resource['name'] == 'Care Coordination':
        #         return resource['id']

    def get_canvas_bot(self):
        return "5eede137ecfe4124b8b773040e33be14"

        # Below is the request to make if you want to programatically fetch the group
        # but most of the time these values are stable per instance and we want to reduce calls

        # response = requests.request(
        #     "GET",
        #     (f"https://fhir-{self.instance_name}.canvasmedical.com/"
        #     "Practitioner?include-non-scheduleable-practitioners=true"),
        #     headers={
        #         'Authorization': f'Bearer {self.token}',
        #         'accept': 'application/json'
        #     },
        # )

        # if response.status_code != 200:
        #     raise Exception("Unable to search FHIR Practitioner")

        # for entry in response.json()['entry']:
        #     resource = entry['resource']
        #     if resource['name'][0]['text'] == 'Canvas Bot':
        #         return resource['id']

    def get_care_team_lead(self):
        key = None
        care_teams = self.patient.patient.get('careTeamMemberships', [])
        for care_team in self.patient.patient.get('careTeamMemberships', []):
            if care_team.get('lead'):
                key = care_team.get('staff', {}).get('key')

        return {
            "owner": {
                "reference": f"Practitioner/{key}"
            }
        } if key else {}

    def create_fhir_task(self):
        """ Create a Task to schedule Follow UP"""
        payload = json.dumps({
            "resourceType": "Task",
            "extension": [
                {
                  "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
                  "valueReference": {
                    "reference": f"Group/{self.get_care_coordination_group()}"
                  }
                }
            ],
            "status": "requested",
            "description": "Schedule PHQ-9 follow up for patient",
            "for": {
                "reference": f"Patient/{self.patient.patient_key}"
            },
            "requester": {
                "reference": f"Practitioner/{self.get_canvas_bot()}"
            },
            **self.get_care_team_lead(),
            "input": [
                {
                  "type": {
                    "text": "label"
                  },
                  "valueString": "Urgent"
                }
            ],
            "restriction": {
                "period": {
                  "end": f'{arrow.now().shift(days=1).format("YYYY-MM-DD")}T00:00:00+00:00'
                }
            }
        })
        response = requests.request(
            "POST",
            f"https://fhir-{self.instance_name}.canvasmedical.com/Task",
            headers={
                'Authorization': f'Bearer {self.token}',
                'accept': 'application/json'
            },
            data=payload
        )

        if response.status_code != 201:
            raise Exception(f"Failed to create FHIR Task status {response.status_code} and payload {payload}")

    def get_fhir_task(self, task_id):
        """ Given a Task ID we can perform a FHIR Task Search Request"""
        response = requests.get(
            f"https://fhir-{self.instance_name}.canvasmedical.com/Task?_id={task_id}",
            headers={
                'Authorization': f'Bearer {self.token}',
                'accept': 'application/json'
            }
        )

        if response.status_code != 200:
            raise Exception('Failed to get FHIR Task')

        resources = response.json().get("entry", [])
        if len(resources) == 0:
            return None

        return resources[0].get("resource")

    def update_fhir_task(self, task_id, payload):
        """ Given a Task ID and payload, we will want to mark as complete
        and send it to the FHIR Task Update Endpoint """

        payload['status'] = 'completed'
        if 'note' in payload:
            del payload['note']

        response = requests.request(
            "PUT",
            f'https://fhir-{self.instance_name}.canvasmedical.com/Task/{task_id}',
            headers={
                'Authorization': f'Bearer {self.token}',
                'accept': 'application/json'
            },
            data=json.dumps(payload)
        )

        if response.status_code != 200:
            raise Exception(f"Failed to mark Task as completed with {response.status_code} and payload {payload}")


    def get_follow_up_task(self):
        return self.patient.tasks.filter(
            status='OPEN', title="Schedule PHQ-9 follow up for patient")

    def close_task(self):
        open_tasks = self.get_follow_up_task()
        for task in open_tasks:
            task_id = task['externallyExposableId']
            task_payload = self.get_fhir_task(task_id)
            if task_payload:
                self.update_fhir_task(task_id, task_payload)

    def get_fhir_appointments(self):
        """ Given a Task ID we can perform a FHIR Task Search Request"""
        response = requests.get(
            (f"https://fhir-{self.instance_name}.canvasmedical.com/"
             f"Appointment?date=ge{self.interview_time[:10]}&patient=Patient/{self.patient.patient_key}"),
            headers={
                'Authorization': f'Bearer {self.get_fhir_api_token()}',
                'accept': 'application/json'
            }
        )

        if response.status_code != 200:
            raise Exception("Failed to search Appointments")

        return response.json()

    def in_denominator(self):
        """
        Patients with most recent PHQ9 score >= 10

        """
        phq9_ques = self.patient.interviews.find(QuestionnairePhq9).last()
        if not phq9_ques:
            return False

        score = next(
            (
                result.get("score")
                for result in phq9_ques.get("results", [])
                if result.get("score") and result.get("score") >= 10
            ),
            None,
        )
        self.score = score
        self.interview_time = phq9_ques['noteTimestamp']
        return bool(score)

    def in_numerator(self):
        # Patients that have a follow-up appointment scheduled in the future
        telehealth_appts = self.patient.upcoming_appointments.filter(
            startTime__gt=self.interview_time, noteType__code=TELEHEALTH_NOTE_TYPE_CODE
        )

        if any(
            appt
            for appt in telehealth_appts
            if appt.get("status") not in APPOINTMENT_CANCELLED_STATUSES
        ):
            return True

        # if there are no upcoming appointments, we need to make sure they dont have a completed
        # appointment after the PHQ-9 was filled out
        appointments = self.get_fhir_appointments()

        for apt in appointments.get('entry', []):
            apt_code = apt['resource']['appointmentType']['coding'][0]['code']
            start_time = arrow.get(apt['resource']['start'])
            status = apt['resource']['status']
            if (apt_code == TELEHEALTH_NOTE_TYPE_CODE and
                start_time > arrow.get(self.interview_time) and
                status not in APPOINTMENT_CANCELLED_STATUSES):
                return True


    def compute_results(self):
        """ """
        result = ProtocolResult()

        self.instance_name = self.settings.INSTANCE_NAME
        self.token = self.get_fhir_api_token()

        # Check if a paitent has an elevated PHQ-9
        if self.in_denominator():

            if (self.field_changes.get('model_name') == 'appointment' and
                not self.field_changes.get('created')):
                return result

            if self.in_numerator():
                result.status = STATUS_SATISFIED

                # Let's make sure we mark the Task as Done as well
                self.close_task()
            else:
                result.due_in = -1
                result.status = STATUS_DUE

                narrative = f"{self.patient.first_name} has completed a PHQ-9 with an elevated score"
                result.add_narrative(narrative)

                follow_up_recommendation = FollowUpRecommendation(
                    key="RECOMMEND_FOLLOW_UP",
                    rank=1,
                    button="Follow up",
                    patient=self.patient,
                    title=f"Schedule a One Week Follow Up",
                    narrative=narrative,
                    context={
                        "requested_date": arrow.now().shift(days=7).format("YYYY-MM-DD"),
                        "internal_comment": "Reassess PHQ-9",
                        "requested_note_type": TELEHEALTH_NOTE_TYPE_CODE,
                        "reason_for_visit": "Follow Up Visit"
                    },
                )
                result.add_recommendation(follow_up_recommendation)

                if not self.get_follow_up_task():
                    self.create_fhir_task()


        return result
```
### **Healthcare Pricing and Payments**
Your Care Model will undoubtedly be influenced by your payment model, and your payment model could potentially evolve and change over time. We built our fully integrated Revenue module to support any combination of the following options:

D2C: direct-to-consumer
SIE: self-insured employers
FFS: fee-for-service reimbursement with commercial or government payers
VBC: value-based contracting with commercial or government payers

#### Capturing what services were provided

Your documentation in Canvas feeds into your billing workflows. We make it easy by populating the [Billing Footer](https://canvas-medical.zendesk.com/hc/en-us/articles/4416815562387-Billing-Footer) using the relevant commands (Diagnose, Assess Perform, etc).[**Structured Assessments**](https://canvas-medical.zendesk.com/hc/en-us/articles/4415631833875-Structured-Assessment) are a great way to create custom templates as they use our Questionnaire model but also map answers to ICD-10 and CPT codes.

Below, you will see a custom-built Structured Assessment for behavioral health therapeutic interventions in action. Upon performing a Structured Assessment for Therapy, note that CPT code 90853 is automatically logged, removing duplicate workflow.

#### Managing Claims and Payments through the API
After adding a patient's `coverage` as part of your intake process, you can leverage the following endpoints to automate charges and payments. <br><br>
[**`CoverageEligibilityRequest`**](https://main.d298pum72820gn.amplifyapp.com/api/coverageeligibilityrequest/) & [**`CoverageEligibilityResponse:`**](https://main.d298pum72820gn.amplifyapp.com/api/coverageeligibilityresponse/) You may need to ensure that a patient's Coverage is active. We will automatically run eligibility leading up to scheduled appointments, but you may also want or need to run them using the API prior to providing asynchronous care.  <br>
[**`Claim:`**](https://main.d298pum72820gn.amplifyapp.com/api/claim/) Creating a claim through the API will populate the patient's record with a Data Import note. <br> 
[**`PaymentNotice:`**](https://main.d298pum72820gn.amplifyapp.com/api/paymentnotice/)  HOW DO WE KNOW BALANCE?<br>


#### Conclusion
...

