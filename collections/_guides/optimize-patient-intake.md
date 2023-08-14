---
title: "Optimize Patient Intake"
---

Patient intake is how care delivery organizations ensure they have everything they need from a patient before an encounter. Historically, this typically consists of manual processes to gather and verify important information including demographics, billing and insurance, medical histories, and consents; however, it can and should be so much more than that. Recent studies have reinforced the notion that conventional patient intake remains a concern for consumers.Canvas's extensibility enables you to differentiate your care model by using external data to create operational efficiencies, resulting in an enhanced patient experience.
<br>
<br>
* * *
## What you'll learn
In this guide, you will learn how to do the following:
- Write your patient profiles to Canvas
- Surface custom data points in the Canvas UI
- Incorporate patient collected data with Questionnares
- Supercharge your patient onboarding with Canvas + Zus 
<br>
<br>

* * *

## Write your patient profiles to Canvas
{% tabs WPP %}
{% tab WPP Developers %}
Whether you are sourcing patients from your direct-to-consumer site, getting patient lists through a payer relationship, and/or leveraging a CRM, our FHIR API will enable you to create and update your patient profiles within Canvas with all of the necessary demographic information to get started. The endpoints listed below are the most commonly utilized to do so.<br><br>
[FHIR Patient:]({{site.baseurl}}/api/patient/) The create and update endpoints allow you to sync the patient’s demographic data, including addresses, contact methods, patient preferences, patient contacts, and more. The identifier attribute on the patient resource is a great place to store unique identifiers and additional data for that patient that does not fit elsewhere (like an internal MRN or program membership levels). You can use the identifier attribute to store multiple values. You can surface these values in the record using the Protocol below.<br><br>
[FHIR Coverage:]({{site.baseurl}}/api/coverage/) Whether you are billing to commercial insurance plans, or need to add custom employer-based coverages, the Coverage endpoint can be leveraged to add a Patient’s coverage information. We populate the initial list of available insurers through our integration with ClaimMD. Additional coverage options such as employee programs can be added and updated following these steps. The ID associated with each insurer is needed to create the coverage through the API.<br><br>
[FHIR CoverageEligibilityRequest:]({{site.baseurl}}/api/coverageeligibilityrequest/)<br><br>
[FHIR CoverageEligibilityResponse:]({{site.baseurl}}/api/coverageeligibilityresponset/)<br><br>
[FHIR Consent:]({{site.baseurl}}/api/consent/) Consent: Consents also have to be configured before they can be added through the API. The ConsentCoding cannot be changed once created, so make sure to configure your consents with that in mind. In addition to recording the consent, you can attach a PDF version using the sourceAttachment attribute. 

{% endtab %}
{% tab WPP  Super Users %}

After determining how you will source your patients and what data you will have at your disposal, you can work with your developers to automate creating patient profiles in Canvas. They will need to know when within your workflow you will need to create or update patients within Canvas. 


{% endtab %}
{% endtabs %}