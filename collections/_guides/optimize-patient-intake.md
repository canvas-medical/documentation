---
title: "Optimize Patient Intake"
guide_for: (https://canvas-medical.zendesk.com/hc/en-us/articles/5804335726483-Patient-Metadata)
---

Patient intake is how care delivery organizations ensure they have everything they need from a patient before an encounter. Historically, this typically consists of manual processes to gather and verify important information including demographics, billing and insurance, medical histories, and consents; however, it can and <b>should</b> be so much more than that. Current data continues to support the idea that traditional patient intake is a consumer pain point. Canvas's extensibility enables you to differentiate your care model by using external data to create operational efficiencies, resulting in an enhanced patient experience.
<br>
<br>
* * *
## What you'll learn
In this guide, you will learn how to do the following:
- Write your patient profiles to Canvas
- Surface custom data points in the Canvas UI
- Incorporate patient collected data with Questionnaires
- Supercharge your patient onboarding with Canvas + Zus 
<br>
<br>

* * *

### Write your patient profiles to Canvas
{% tabs WPP %}
{% tab WPP Developers %}
After mapping your patient data and determining when and where in your workflow you will create and update patient profiles with your super users, you'll likely leverage the following endpoints to do so:

[FHIR Patient:]({{site.baseurl}}/api/patient/) The identifier attribute on the patient resource is a great place to store unique identifiers and additional data for that patient that does not fit elsewhere (like an internal MRN or program membership levels). You can use the identifier attribute to store multiple values. You can also surface these values in the record using the Protocol below.<br><br>
[FHIR Coverage:]({{site.baseurl}}/api/coverage/) The ID associated with each insurer is needed to create the coverage through the API.<br><br>
[FHIR CoverageEligibilityRequest:]({{site.baseurl}}/api/coverageeligibilityrequest/)<br><br>
[FHIR CoverageEligibilityResponse:]({{site.baseurl}}/api/coverageeligibilityresponset/)<br><br>
[FHIR Consent:]({{site.baseurl}}/api/consent/)  Work with your super users to configure consents in Canvas. The ConsentCoding cannot be changed once created. In addition to recording the consent, you can attach a PDF version using the sourceAttachment attribute.<br>


{% endtab %}
{% tab WPP Super Users %}
Whether you are sourcing patients from your direct-to-consumer site, getting patient lists through a payer relationship, and/or leveraging a CRM, our FHIR API will enable you to create and update your patient profiles within Canvas with all of the necessary demographic information to get started. The endpoints listed below are the most commonly utilized to do so. Work with your developers to map out how you can leverage the FHIR API to create efficiencies in your onboarding flow.<br><br>
[FHIR Patient:]({{site.baseurl}}/api/patient/) The create and update endpoints allow you to sync patients' demographic data, including addresses, contact methods, patient preferences, patient contacts, and more. The identifier attribute on the patient resource is a great place to store unique identifiers and additional data for that patient that does not fit elsewhere (like an internal MRN or program membership levels). You can use the identifier attribute to store multiple values. You can surface these values in the record using the Protocol below.<br><br>
[FHIR Coverage:]({{site.baseurl}}/api/coverage/) Whether you are billing to commercial insurance plans, or need to add custom employer-based coverages, the Coverage endpoint can be leveraged to add a patient’s coverage information. We populate the initial list of available insurers through our integration with ClaimMD. Additional coverage options such as employee programs can be added and updated following these steps. Your developers will need the IDs to write coverages. <br><br>
[FHIR CoverageEligibilityRequest:]({{site.baseurl}}/api/coverageeligibilityrequest/)<br><br>
[FHIR CoverageEligibilityResponse:]({{site.baseurl}}/api/coverageeligibilityresponset/)<br><br>
[FHIR Consent:]({{site.baseurl}}/api/consent/) Consents also have to be configured before they can be added through the API. The ConsentCoding cannot be changed once created, so make sure to configure your consents with that in mind. Once you create them, share the consent codings with your team to leverage them through the FHIR API. 


{% endtab %}
{% endtabs %}
<br>
* * *
### Surface custom data points
{% tabs SCDP %}
{% tab SCDP Developers %}
Although identifiers added through the API do not display in the Canvas UI by default, you can insert a Banner Alert protocol, like the one below, to surface the information to your end users. You can update both alertplacement and alertintent in the code below as needed, see here for more information on possible configurations for the banner alerts.

``` python
from canvas_workflow_kit.protocol import (
    ClinicalQualityMeasure,
    ProtocolResult,
    STATUS_DUE,
)
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.intervention import BannerAlertIntervention

class ExternalIdentifierBanner(ClinicalQualityMeasure):
    class Meta:
        title = 'External Identifier Banner'
        description = 'Display any external identifiers in a banner'
        version = '2022-05-10v8'
        types = ['Banner']
        compute_on_change_types = [CHANGE_TYPE.PATIENT]

    def compute_results(self):
        result = ProtocolResult()

        external_identifiers = self.patient.patient["externalIdentifiers"]
        if len(external_identifiers):
            result.status = STATUS_DUE
            result.due_in = -1
            for external_identifier in external_identifiers:
                result.recommendations.append(
                    BannerAlertIntervention(
                        narrative=(f"{external_identifier['system']}: {external_identifier['value']}"),
                        placement=['profile'],
                        intent='info')
                    )
        return result

```

{% endtab %}
{% tab SCDP  Super Users %}

The identifier attribute on the patient profile can be used to store data points that are not currently represented in Canvas's data model. You can add multiple values, including internal identifiers, program information, or status within a measurement group. We do not currently surface these values in the UI, but you can partner with your developers to create protocols if needed. 

You can also add [metadata](https://canvas-medical.zendesk.com/hc/en-us/articles/5804335726483-Patient-Metadata) to patient's profile through our admin settings. 

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/metadata.gif){:width="100%"}
{: refdef}


{% endtab %}
{% endtabs %}
<br>
* * *
###  Incorporate patient collected data with Questionnaires
{% tabs PCDQ %}
{% tab PCDQ Developers %}
Your super users may want patients to complete intake forms ahead of their visit.  The FHIR QuestionnaireResponse Create endpoint can be used to capture structured data through the use of Questionnaires.  

Questionnaires can be added to an existing note by adding an encounter reference. The [FHIR Encounter Search]({{site.baseurl}}/api/encounter/) endpoint can be used to obtain the encounter_id. 

```
"encounter": {
        "reference": "Encounter/(encounter_id)"
    }
```
<br>
{% include alert.html type="info" content="Historically, Canvas only created encounters at check-in. To support these pre-visit workflows, we have updated our logic as of 08/0X/23 to create the encounter when an appointment is made, in a status of planned." %}

Canvas Notes are meant to be collaborative and authored by multiple people, including the patient. When adding patient-collected data you can set the author reference  to Patient/{patient_id}. Doing so will then be visible within the Command history tool-tip in the Note.


{% endtab %}
{% tab PCDQ  Super Users %}
[Questionnaires](https://canvas-medical.zendesk.com/hc/en-us/articles/4403561447827-Creating-a-New-Questionnaire) in Canvas represent a structured set of questions intended to guide the collection of answers from end-users and promote consistent data collection. They support many workflows, from evidence-based assessments to completely custom forms and templates. Your team can utilize our no-code google sheet template to build, update, and load questionnaires into Canvas.  Make sure to coordinate with your developers to set Questionnaire up with unique codes, using our supported code systems, so that they can be leveraged in the FHIR API and with Protocols. 

{% endtab %}
{% endtabs %}
<br>
* * *
###  Supercharge your patient onboarding with Canvas + Zus 
If you still find that your care team is spending countless hours hunting down your patient’s historical records and converting them to structured data, the Canvas + Zus integration may be a game changer. Clinicians can leverage the Zus Aggregated Profile (ZAP) to insert relevant patient data (historical medications, conditions, labs, and encounters sourced from various HIEs and proprietary data networks) directly into Canvas profiles in actionable ways. Learn more about our Partnership with Zus here .




