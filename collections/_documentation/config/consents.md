---
title: "Consents"
layout: documentation
---

Canvas allows users to customize the types of consents that are documented in the Registration view of the patient's chart. You will need to configure Consent Codings and Consent Rejections Codings to leverage this functionality. 
<br>
<br>
## Patient Consent Codings

### Adding a Patient Cosent Coding

To add a new patient consent, click ![role-button](/assets/images/add-patient-consent-coding.png){:width="16%"} in the top right corner and then complete the following form. 

<b>System:</b> You can leverage established systems, like [LOINC](https://www.findacode.com/loinc/LG39005-0--patientanytypeofserviceanykindofnoteanysetting.html) or [SNOMED](https://www.findacode.com/snomed/309370004--consent-status.html), or set this to INTERNAL if you wish to create your own unique codes. 

<b>Version:</b> You may need to update your forms from time to time. Adding an updated version allows you to track which version of the form a patient has on file. 

<b>Code:</b> The combination of code & version needs to be unique. 

{% include alert.html type="danger" content="You cannot update the code for a Consent once added. Make sure to coordinate with your developers to ensure they are set up in a way that supports any external workflows." %}

<b>Display:</b> What will be shown in the UI.

<b>User selected:</b> You can inactivate an older version of a consent, or one that is no longer necesssary, by unchecking this box.

<b>Expiration rule:</b> You can set a default rule for expiration based on your consent policies. The options are in one year (+365 days from the date of the consent), end of year, (the last day of calendar year, i.e. 12/31/20XX), or never. This date can be overwritten during registration.

<b>Is mandatory:</b> Mandatory consents will be present on the patient profile with a red warning. Non mandatory consents will be available in a pick list after a user selects `add consent`.

<b>Is proof required:</b> If proof is required, there will be a warning letting your users know that a documen must be linked to the consent if one is not present.

![consent](/assets/images/consent.png){:width="60%"}
<br>
<br>
### Updating a Patient Cosent Coding
To edit a Patient Consent Coding, click into an existing consent and make changes as needed. You can also take a bulk action to delete Patient Consent Codings by checking the boxes next to each and using delete in the action drop-down. 
<br>
<br>
## Patient Consent Rejection Codings

### Adding a Patient Consent Rejection Coding

End users can document refusal of a consent by marking it as rejected. After doing so, a second dropdown will appear, allowing for the selection of a reason for rejection.

To add a new Patient Consent Rejection Coding, click the ![role-button](/assets/images/add-patient-consent-rejection-coding.png){:width="20%"} in the top right corner and then complete the following form. 

<b>System:</b> You can leverage an established system, like [LOINC](https://loinc.org/71801-5) or set this to INTERNAL if you wish to create your own unique codes. 

<b>Display:</b> Enter text you'd like displayed as a reason for rejection in a dropdown (i.e. Declined)

![Protocol framework](/assets/images/reject-consent.png){:width="60%"}