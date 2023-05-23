---
title: "Care Modeling: Behavioral Health"
guide_for:
 - /api/patient/
 - /api/coverage/
 - /api/consent/
 - /api/questionnaireresponse/
 - /documentation/configuringquestionnaires/
---

Canvas is purpose built to accommodate every stage and scale for care delivery organization such as yours. This is absolutely true for behavioral health. Canvas can meet your ever-evolving needs, whether you’re building a cash-pay digital mental health clinic, an evidence-based treatment program targeting Medicare/Medicaid, or any meaningful behavioral health care model in between. This guide applies our Care Modeling framework to Behavioral Health and provides relevant examples of how to implement various Canvas capabilities for each of the seven elements of Care Modeling.   

### **Patient Sourcing and Intake**

#### Creating your Patient Profiles

Whether you are **sourcing patients** from your direct-to-consumer site, getting patient lists through a payer relationship and/or leveraging a CRM, **our FHIR API will enable you to create and update your patient profiles within Canvas** with all of the necessary demographic information to get started. The endpoints listed below are the most commonly utilized to do so.


[**`Patient:`**](https://main.d298pum72820gn.amplifyapp.com/api/patient/) The create and update endpoints allow you to sync the patient's demographic data, including addresses, contact methods, patient preferences, patient contacts, and more. 

[**`Coverage:`**](https://main.d298pum72820gn.amplifyapp.com/api/coverage/)  Whether you are billing to commercial insurance plans, or need to add custom employer-based coverages, the Coverage endpoint can be leveraged to add a Patient's coverage information. We populate the [initial list of availble insurers](https://www.claim.md/payer_list.html) through our integration with ClaimMD. Additional coverage options such as employee programs can be added and updated following [these steps](https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers). The ID associated with each insurer is needed to create the coverage throught the API. 

[**`Consent:`**](https://main.d298pum72820gn.amplifyapp.com/api/consent/) Consents also have to be [configured](https://canvas-medical.zendesk.com/hc/en-us/articles/5524511564947-Patient-Consents) before they can be added through the API. The `ConsentCoding` cannot be changed once created, so make sure to configure your consents with that in mind. In addition to recording the consent, you can attach a PDF version using the `sourceAttachment` attribute. 


#### Surfacing custom data points using Banner Protocols
The `identifier` attribute on the `patient` resource is a great place to store unique identifiers and additional data for that patient that does not fit elsewhere. With a cardinality of zero to many, you can use the `identifier` attribute to store multiple values. Although `identifiers` added through the API do not display in the Canvas UI by default, this Banner Alert Protocol can be used to surface the information to your end users. You can update both [`alertplacement` and `alertintent`](https://docs.canvasmedical.com/docs/banner-alerts-for-contacts#alertplacement) in the code below as needed. 

``` 
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
                            narrative=(f"{external_identifier['system']}: 
                            {external_identifier['value']}"),
                            placement=['profile'],
                            intent='info')
                        )
        return result     
```

#### Incorporating patient collected data with Questionnaires

Leading up to a scheduled appointment, you can streamline **patient intake** by writing patient data that has been collected through your patient application to Canvas with our FHIR API. 


**`QuestionnaireResponse Create:`** The `QuestionnaireResponse` endpoint can be used to capture structured data through the use of custom forms. Questionnaires must first be [configured](https://main.d298pum72820gn.amplifyapp.com/documentation/ConfiguringQuestionnaires/) in your Canvas instance. Your team can utilize our no-code google sheet template to build, update, and load questionnaires into your Canvas instance.

<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTIe3s2zh0FAZMaIxaxg2EQ5x7ot4U4iSX95tLNClkNvQ4LQAr_qZm6b9nmdG68xDf4NdeNqEIvKlpo/pubhtml?gid=2051129171&amp;single=true&amp;widget=true&amp;headers=false" width=800px height=600px ></iframe>

They are designed to be code-backed to ensure that you can interact with them programatically. Make sure to coordinate across your Clinical Operations, Engineering and Product teams to set them up with unique codes, using our supported code systems. We do offer some pre-built questionnaires, including many common behavioral health assessments such as the PHQ-9 shown above.<Br>

```
💡Evaluating Canvas? To load this PHQ-9 questionniare into your sandbox, navigate to Settings>Practice>Questionnaire
Loader or to: https://{sandboxname}-preview.canvasmedical.com/admin/api/questionnaireloader/ and paste in the following:
```


**Google Sheet ID:** 1RIYAvyp62EOlQ6DPRV4tRPyca8xgEbg4z2vGo_EEhT4<br>
**Google Sheet tab name:** ques-PHQ9-all<br>


You may want your patients to complete these assessments, or your custom built workflows, prior to their visit. **Canvas Notes are meant to be collaborative and authored by multiple people, including the patient**. When adding patient-collected data you can set the `author` attribute to `patient/{patientkey}`. Doing so will then be visible within the Command history tooltip in the Note.


#### Canvas + Zus 🔱 

If you find that your care team is spending countless hours hunting down your patient's historical records and converting them to structured data, the **Canvas + Zus integration** may be a game changer.  Clinicians can leverage the Zus Aggregated Profile (ZAP) to insert relevant patient data (historical medications, conditions, labs, and encounters sourced from various HIEs and proprietary data networks) directly into Canvas profiles in actionable ways. Learn more about our Partner ship with Zus [here](https://www.prnewswire.com/news-releases/canvas-medical-and-zus-announce-strategic-product-partnership-redefining-the-speed-and-effectiveness-of-collaborative-development-in-healthtech-301736901.html) . 

### **Ongoing Interaction Modes and Utilization Policies**

#### Configure Canvas to support your scheduling needs

**Note Types:** Releasing [**configurable Note Types**](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-) was tightly aligned with our strategy shift away from focusing on primary care. The differentiated care models of our customers often include all types of patient interactions, including in-person visits, telehealth, and asynchronous encounters. You can configure your note types to fit your behavioral health offering by creating custom note types and codes. Or, you can use an established system such as the [LOINC®](https://loinc.org/LG41826-5) codes listed below. <br><br>
18776-5	Plan of care note <br>
28628-6	Psychiatry Note<br>
34792-2	Psychology Note<br>
28653-4	Social worker Note<br>
34786-4	Mental health Note<br>
34748-4 Telephone encounter Note<br>
34790-6	Psychiatry Group counseling note<br>
34793-0	Psychology Group counseling note<br>
34787-2	Mental health Group counseling note<br>



**Appointment Types** [Creating Custom Appointment Types](https://canvas-medical.zendesk.com/hc/en-us/articles/15704289792659-Scheduling-Other-Events-#h_01GXV9832Z74GRAQKDD4JA9677) allows your team to schedule other events that block time but do no generate Notes within the Timeline. They can be associated with a specific patient (but do not require one) and can be used to account for meetings, travel time, or co-visits during which multiple providers need to be included, but only one Note needs to be generated. 

[**Availabilty in Canvas**](https://canvas-medical.zendesk.com/knowledge/articles/360058400553/en-us?brand_id=360005403014&return_to=%2Fhc%2Fen-us%2Farticles%2F360058400553) is managed through and integration with Google Calendar. This allows you to set availability using recurring events that are easy to update as needed. 

#### Manage your schedules with the Canvas API
Once your availabilty has been set, you can use the `schedule` and `slot` search endpoints to find provider availability and then schedule appointments using the `appointment` endpoint.<


#### Syncing clinical and administrative calendars
Your providers may be part time or juggling both clinical hours and internal meetings. Syncing clinical and administrative calendars is often a must. You can use the notification protocol to know when and appointment has been created or updated in Canvas and use it to write that appointment to your administrative calendars in Google or Outlook. With this, you can control what info is shared, whether you have a BAA with Google and can write PHI, or just need to block time. You can also block time in Canvas through the API by writing other events through the appointment endpoint. 


#### Communicate with your patients in between visits
Staying in touch with your patients in between visits is often essential. Checking in with them needs to be frictionless for your providers. The messaging workflow in Canvas allows clinicians to generate an outbound message using free text or templates. Use the notification protocol below to know when a message has been created. You then have the ability to send the contents of the message as a payload to your outbound messaging system, or you can use the `communication` endpoint to read the message. 

```
message notification protocol with contents in payload
```

Notification protocols are also a great way to kickoff automated follow up communications. You can trigger them based on many events within the Chart, including signing a Note. After the visit is complete, the notification protocol can be used to pass certain information from the note to your patient application, including our customizable patient instructions. It can also leverage an API call to search for available documents, including any healthwise materials that were added to the visit. 

The example below shows how you can use a notification protocol to pull both the contents of the instruct command as well as the selected Healthwise content to the 

```
notification protocol instruct command
```

Patient responses can be written to Canvas using the `communication` create endpoint. They can be assigned to a user through the  `recipient` attribute, which ingests either a patient or practitioner reference. All users in Canvas have a practictioner ID, not just clinicians. The `practictioner` search includes a query param to include non-schedulable providers. 


### **Diagnostic Range and Inputs**
What is your target population? Does your care mdoel support a broad range of mental health concerns for all genders and ages, or are you hyper focused on adolescents suffering from eating disorders. Either way, you can configure Canvas to support your specific diagnostic range. 

Our diagnose command defaults 

Alternatively, you can leverage the questionnaireresponse endpoint to capture responses in a more structured format. You may want to poll your patients daily through your patient facing application to capture and track their mood. A simple questionnaire will ensure you can report and analyze those responses using our read-only replica database. 

<ul>
<li>PHQ-2</li>
<li>PHQ-9</li>
<li>GAD-2</li>
<li>GAD-7</li>
<li>ADHD self-report scale</li>
</ul>

Condition Search Annotation and Limiting

### **Scope of Interventions and Safety Framework**

Narrative Charting for BH
Commands
<ul>
<li>HPI</li>
<li>MANAGE CONDITIONS</li>
<li>GOALS</li>
<li>PLAN</li>
<li>INTSTRUCT/EDUCATION MATERIAL</li>
</ul>
Commands SDK (FUTURE)


### **Care Team Composition and Sourcing**
Care Team set up for BH<br>
Object Permissions through protocols and groups<br>
Route Referrals to correct Team Protocol <br>


### **Content and Automation**
As your Care Team meets with your patient, Canvas drives top-of-license care by enabling efficiency and custom workflow at every step.

[Automations](https://canvas-medical.zendesk.com/hc/en-us/articles/360059338953-Automations) are a key feature in Canvas that allow you to sequence many Commands together. Think of these as Macros in Excel / Google Sheets, but supercharged for clinical context.

Below, you'll find an example of a “Major Depressive Disorder” automation you could create:

Questionnaire - PHQ-9 <br>
Perform - CPT Code 90801: Psychiatric diagnostic interview examination<br>
Diagnose - Major Depressive Disorder<br>
Prescribe - Fluoxetine 40, take once per day with or witout food <br>
Instruct - Depression Education <br>

Once building the Automation, every time you diagnose MDD, you can enter the Automation to surface the Commands in sequence, adjusting where relevant to fit the needs of your patient. 

![MDD Automation](https://github.com/canvas-medical/documentation/assets/91080969/5cc17b2b-6a82-4609-9bb7-3e33e29e917b)


Automated Follow Up Protocol <br>
Prescribe recommendation <br>


### **Healthcare Pricing and Payments**
Structured Assessment (embed excel?) <br>
Claim API <br>
Payment API <br>
