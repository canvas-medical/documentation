---
title: "Behavioral Health"
guide_for:
	--api/patient
zendesk articles: 
https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers
https://canvas-medical.zendesk.com/hc/en-us/articles/5524511564947-Patient-Consents
---
## **Care Modeling: Behavioral Health**

**Canvas is purpose built to accommodate every stage and scale for a care delivery organization. This is absolutely true for behavioral health. Canvas can meet your ever-evolving needs, whether you’re building a cash-pay digital mental health clinic, an evidence-based treatment program targeting Medicare/Medicaid, or any meaningful behavioral health care model in between,  Let’s learn about how you can launch your behavioral health program in as little as 8 weeks.**

### **Patient Sourcing and Intake**

#### Patient Sourcing

Whether you are **sourcing patients** from your direct-to-consumer site, getting patient lists through a payer relationship and/or leverage a CRM, **our FHIR API will enable you to create and update your patient profiles within Canvas** with all of the necessary demographic information to get started. The endpoints listed below are the most commonly needed to do so.

***
##### Patient Create/Update
[https://fhir-example.canvasmedical.com/Patient](https://fhir-example.canvasmedical.com/Patient) <br><br>
The create and update endpoints allow you to sync the patient's demographic data, including addresses, contact methods, notes about the patient, and patient preferences. The `identifier` attribute is a great place to store unique identifiers and additional data for that patient that does not fit elsewhere. Although it does not display in the Canvas UI by default, this Banner Alert Protocol can be used to display the values in various spots throughout the record if necessary. 

***
##### Coverage Create/Update
[https://fhir-example.canvasmedical.com/Coverage](
https://fhir-example.canvasmedical.com/Coverage)<br><br>
Whether you are billing to commercial insurance plans, or need to add custom employer-based coverages, the Coverage endpoint can be leveraged to add a Patient's coverage information. We populate the [initial list of availble insurers](https://www.claim.md/payer_list.html) through our integration with ClaimMD. Additional coverage options such as employee programs can be added and updated following [these steps](https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers). The ID associated with each insurer is needed to create the coverage throught the API. 

***
##### Consent Create
[https://fhir-example.canvasmedical.com/Consent](
https://fhir-example.canvasmedical.com/Consent)<br><br>
Consents also have to be [configured](https://canvas-medical.zendesk.com/hc/en-us/articles/5524511564947-Patient-Consents) before they can be added through the API. The `ConsentCoding` cannot be changed once created, so make sure to configure your consents with that in mind. In addition to recording the consent, you can attach a PDF version using the sourceAttachment attribute. 

***

#### Intake

**Completing intake** for your patients can be made more efficient by writing patient-collected data to Canvas through our API. 

***
##### QuestionnareResponse Create
[https://fhir-example.canvasmedical.com/Questionnaire](
https://fhir-example.canvasmedical.com/Questionnaire)<br><br>
The `QuestionnaireResponse` endpoint can be used to capture structured data. Questionnaires must be [configured](https://main.d298pum72820gn.amplifyapp.com/documentation/ConfiguringQuestionnaires/) in your Canvas instance. They are designed to be code-backed to ensure you can interact with them programatically. Make sure to coordinate across your clinical ops and development teams to set them up with the appropriate codes and code systems. We do offer some pre-built questionnaires, including these common behavioral health assessments:<Br>
<ul>
<li>PHQ-2</li>
<li>PHQ-9</li>
<li>GAD-2</li>
<li>GAD-7</li>
<li>ADHD self-report scale</li>
</ul>

You may want your patients to complete these assesmsments or your cusotom built workflows prior to their visit. Canvas Notes are meant to be collaborative and authored by multiple people, including the patient. When adding patient-collected data you can set the `author` attribute to patient/patientkey. Doing so will then be visible within the Command history tooltip in the Note.<br>

The `QuestionnaireResponse` endpoint allows you to specify the encounter you would like to enter it into. An encounter is only generated once an appointment is checked in. If you would like to wait to add your questionnaire to the Encounter being used by your clinicans, you can use a notification protocol to act as a webhook. The Encounter `change_type` allows you to respond to the act of checking in an appointment and send a payload that includes the encounter ID needed for the Questionnaire Create api call. 



***
##### Condition Create
Coming Soon

***
##### Allergy Create
Coming Soon

***
##### MedicatonStatement Create
Coming Soon

***
##### Immunization Create
Coming Soon

***


##### Canvas + Zus 🔱 

If you find that your care team is spending countless hours hunting down your patient's historical records and converting them to structured data, the [**Canvas + Zus integration**](https://www.prnewswire.com/news-releases/canvas-medical-and-zus-announce-strategic-product-partnership-redefining-the-speed-and-effectiveness-of-collaborative-development-in-healthtech-301736901.html), integration may be a game changer.  Clinicians can leverage the Zus Aggregated Profile (ZAP) to insert relevant patient data (historical medications, conditions, labs, and encounters sourced from various HIEs and proprietary data networks. ) directly into Canvas profiles in actionable ways, creating efficiencies that serve to elevate patient outcomes and unlock business value. 


### **Ongoing Interaction Modes and Utilization Policies**
### **Diagnostic Range and Inputs**
### **Scope of Interventions and Safety Framework**
### **Care Team Composition and Sourcing**
### **Content and Automation**
### **Healthcare Pricing and Payments**
