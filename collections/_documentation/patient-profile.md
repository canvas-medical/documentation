---
title: "Patient Profile"
---

## Introduction
The patient’s profile can be used to register your patients and store important demographic and billing information. 

## Patient Banner
After creating a new profile, key patient identifiers are displayed in the top left corner of the patient’s profile and chart. The banner pulls first and last name, with preferred name in parentheses, DOB, patient’s preferred timezone, age, sex at birth, and phone number from the patient demographics. Edits can be made by following the instructions below. The patient’s photo can be added using the [Canvas Remote]({{site.baseurl}}/documentation/canvas-remote/) iOS app, which can be downloaded from the app store. 

Use the Administrative Caption to communicate reminders/notes within the office related to insurance, copay, payments, and forms. It is visible within the profile, the detailed view of the appointment card on the schedule, the patient search when creating new appointments, and on the print view of the schedule. 
{% include alert.html type="warning" content="The administrative caption is not visible within the Chart. Switch over to the Chart and leverage the Clinical Caption if you need to communicate with your clinicians." %}

The Canvas generated MRN is available in the top navigation menu, with a button to quickly copy it. The banner will also display badges that indicate a patient's status of inactive or deceased, or both. 


## Patient Demographics
### Demographics
The patient demographics section allows you to capture additonal fields beyond the basics needs to create a new profile. You must click `Edit` to update the fields and `Submit` to save. If you do not want to save your changes you can click `Cancel` instead. All fields marked with a red asterisk are required in order to save. 
### Active Status
The patient's status (Active vs Inactive) can be managed using the checkbox at the top. After submitting an updated form with an unchecked box, you will see an `Inactive` badge added to the patient's banner.  
### Deceased Workflow
Clicking the deceased checkbox in the top right will initiate an automated workflow that cancels future appointments, removes follow up appointment requests, and marks contact information as unverifed in order to block outgoing messages. After checking the box, a modal will ask you to enter date of death, cause of death, and comments, all of which are option. After clicking `Mark as Deceased`, those additional fields will be viewable and editable within the demographics section.
{% include alert.html type="info" content="If a mistake was made, you can uncheck the deceased box. Doing so will prompt the user to confirm that the patient should be marked as alive. This action <b>will not</b> reverse the automated actions taken when marking the patient as deceased." %}


## Preferences
You can add the patient's primary care provider, referring provider, and time zone under the patient's preferences. 

The primary care provider is a freetext field used to capture the information; however, it is not leveraged in any workflows. The referring provider is also freetext. It may be pulled into the claim depending on your settings.

Preferred Scheduling Time Zone is useful to support national offerings that span multiple time zones. If added, the patient's timezone will be visible when scheduling appointments and available slots will be presented in the patient's preferred time. [Time Zones]({{site.baseurl}}/documentation/constance-config/#registration) must be enabled in your settings. 

## Preferred Pharmacies
Adding a preferred pharmacy in the profile will drive prescribing workflows. The pharmacy added will default in new prescriptions. We use a directory of pharmacies provided by Surescripts. You can search by name, address, store number, or phone number. The type of pharmacy is shown in the search results and added as a badge once added.

If the patient uses multiple pharmacies (let's say brick & mortar and mail-order), you can add multiple preferred pharmacies to their profile. You must set a default to drive the behavior noted above. The additional pharmacies will be available as quickpicks within the pharmacy dropdown in the Prescribe Commands. 

## Patient Consents
After Patient Consents have been configured, they can be added either through the Profile or in Data Integration. After being added, the Profile should be used to track and manage existing consents. 

Consents marked as mandatory will always present on the profile, whether or not they have been collected. A red badge is used to indicate outstanding consents that need to be collected and/or updated with the necessary documentation. 

### Adding a Consent
On the profile page, click the edit button, and complete the form to capture the state, effective date, and expiration date of the consent. The default expiration date will populate based on how the consent was configured. The options are one year, the end of the calendar year, or never. You can also override the default by selecting `custom date` from the dropdown and then adding a specific date. Rejecting the consent which then surface an additional field to capture the reason. Click `Done` to save.

If documentation of the consent is required (a signature on file is necessary verse only needing verbal consent), a red warning, "Document required", will display . You must process the document and link it through Data Integration. Once linked, you can click on the link, `View Document`, to see the attached PDF. If an updated document is linked to the same consent with a later effective date, the profile will link to the newest version. Documents with earlier effective dates will still be available under the Admin Documents in the chart. 

{% include alert.html type="info" content="Consents added directly in Data Integration will be added to the profile. It may make more sense to add consents requiring documents directly in Data Integration to save a step." %}

### Removing a Consent
You can remove a consent by clicking the edit button on the consent and choosing `Clear`. Doing so will permanently remove the consent record. If a document was associated with the consent, it will not be deleted. It will still be accessible in the Admin Documents section of the chart.  



## Contacts
## Collecting Payments
## Adding Coverages
## Patient Claims
