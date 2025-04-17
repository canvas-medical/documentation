---
permalink: /product-updates/patient-portal/
title: "Beta | Patient Portal Updates"
layout: betas
date: 2024-01-22
---


## Overview

We've recently invested in expanding the Canvas patient experience, creating a fully-featured patient portal. We've designed the experience in a way that is suitable for many, but can be customized to support your care model using plugins. 

<div style="background-color: #c9dfe3; color: black; padding: 10px;">
Opportunities for customization via plugins are highlighted in blue. 
</div>

## Expected Benefits
- A broader set of core functionality:
	- Reliable access via username and password
	- Patient self scheduling
	- Access to health data
	- Ability to upload documents
	- Consent capture
- Opportunities to personalize:
	- Landing page content and branding
	- Custom forms that can be associated with upcoming appointments or interval based
	- Scheduling rules based on business logic



## Username & Password Login

Enabled through: `ENABLE_PATIENT_PORTAL` in Constance config.

Customers that use the Canvas patient portal have a new section in the profile to manage portal users. 

Phone and email capture (including verification flows) within registration has remain unchanged; however, there is now an additional step to register and invite patients to the portal. 

To invite a patient to the portal, you must link a unique email or phone to their portal user in their profile. The email and/or phone number do not necessarily have to match what have been added as contact points - but they will be **leveraged for password resets**. Once added, you can send an invite. After the patient successfully activates their account, staff can continue to trigger password reset emails if necessary.


{:refdef: style="text-align: center;"}
![description](/assets/images/patient-reg.gif){:width="98%"}
{: refdef}

{% include alert.html type="info" content="We included phone or email since some current users may only have one or the other. If you would like to link portal users via email only, you can update your settings within constance config in admin." %}

<div style="background-color: #c9dfe3; color: black; padding: 10px;">
If you do not want this to be a manual process, a plugin can be used to automatically update the portal user based on changes to the patient contacts and trigger an invite. Reach out to support for help enabling this workflow.
</div>

All communication will continue to be sent to the verified contact points (not the portal user email or phone). We have plans in the future to manage outbound communication via plugins, which will allow for further configuration.

## Login Page Banner

Enabeled through: `PATIENT_APP_BANNER`  in Constance config.

You can add a banner to your login page using this new config. Leverage HTML to add style to the text. 

## Landing Page 

<div style="background-color: #c9dfe3; color: black; padding: 10px;">
We've implemented a landing page that is powered by plugins. The Canvas managed default includes panels for upcoming appointments and messages. Customers can customize as desired. See this <a href="/guides/custom-landing-page/">guide</a> for instructions.  
</div>

{:refdef: style="text-align: center;"}
![landing page](/assets/images/landing-page.png){:width="98%"}
{: refdef}

## My Health

Enabeled through: `PATIENT_APP_MY_HEALTH` in Constance config.

### Chart Summary
The My Health section includes a new chart summary and the current Health Records section (if enabled). Each section will mimic the filters used in the default view of the chart (if you see it in Canvas - the patient will see it on their portal)

The chart summary shows the following:

- **Conditions:** All conditions where show_in_summary = true. This includes active conditions and past medical history. Patients will see the last assessed date and the name of the provider who last committed the associated assessment. 
- **Medications:** Active medications. Patients will see the name of the medication, start date, instructions (sig), and the last prescriber.
- **Allergies:** Active allergies. Patients will see all available fields (allergy, severity, reaction, and onset date).

### Upload Documents
Patients will also be able to upload documents. Documents added within the portal will populate a new channel in Data Integration. 

{% include alert.html type="warning" content="This is permission based and needs to be configured for testing. Reach out to support if you would like to enable this feature for testing. " %}

{:refdef: style="text-align: center;"}
![landing page](/assets/images/patient-upload.png){:width="98%"}
{: refdef}

## Consents

Enabled though: `PATIENT_APP_CONSENTS` in Constance config

You can now ask patients to complete their consents via the portal. When configuring consents, there are three new settings: 
- **Document:** PDF of the consent. Patient will see a link to review this document. 
- **Description:** Used as a title / summary for the consent. The patient sees this in their list of consents to review. 
- **Show in Patient Portal:** Only consents with this checked will appear in the portal. 

When a patient logs in, the portal will assess whether the necessary portal consents have been acknowledged by the patient and then prompt the patient to complete any outstanding consents. Mandatory consents must be agreed to in order to continue. Non-mandatory consents can be skipped.

{:refdef: style="text-align: center;"}
![consents](/assets/images/portal-consents.png){:width="50%"}
{: refdef}

The responses will then be recorded in the patient profile. Accepted consents will show `accepted via patient portal` and skipped consents will appear as `rejected via patient portal.` A copy of the consent is not saved. 

{:refdef: style="text-align: center;"}
![consents in profile](/assets/images/portal-consents-profile.png){:width="70%"}
{: refdef}

## Forms

<div style="background-color: #c9dfe3; color: black; padding: 10px;">
  <b>Plugins</b> can be leveraged to present forms to the patient within the portal. 
  This <a href="/guides/patient-portal-forms" style="color: black; text-decoration: underline;">guide</a> walks through how to implement intake forms based on upcoming appointments.
</div>

{:refdef: style="text-align: center;"}
![patient forms](/assets/images/patient-forms.png){:width="98%"}
{: refdef}


## Appointments

Enabeled through: `PATIENT_APP_APPOINTMENTS` in Constance config.

### Viewing Appointments
Patients can now manage their appointments through the portal

Enabling the appointments section within constance allows all patients to: 
- See their upcoming appointments
- See their past appointments
- Join telehealth appointments
- Cancel upcoming appointments 

<div style="background-color: #c9dfe3; color: black; padding: 10px;">
Available actions can be restricted based on your business logic. See <a href="https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/portal_disable_cancel_appts%20">here</a> for an example plugin that hides the cancellation button.
</div>

### Patient Self-Scheduling
You can also now allow patients to self schedule. Note types have two new settings, `Is scheduleable via patient portal` and `Online duration:`. If any note types have these set, patients will have the option to schedule an appointment from the appointment section or home page. 

{:refdef: style="text-align: center;"}
![scheduling settings](/assets/images/portal-scheduling-settings.png){:width="98%"}
{: refdef}

If configured, patients can: 
- See their upcoming appointments
- See their past appointments
- **Make new appointments**
- Join telehealth appointments
- Cancel upcoming appointments
- **Reschedule upcoming appointments**  


When scheduling, the appointment search allows the patient to select the appointment type (note type), location, a provider (optional), and date (optional). They are then presented within open slots across one or many providers to choose from.

The scheduling form includes a note which will translate to the comment within the reason for visit Command.

The audit trail in the note footer will show that the appointment was created by the patient user.

{:refdef: style="text-align: center;"}
![description](/assets/images/patient-scheduling.gif){:width="98%"}
{: refdef}


<div style="background-color: #c9dfe3; color: black; padding: 10px;">
You can leverage the <a href="/sdk/events/#patient-portal-lifecycle-events">patient portal appointment lifecycle events</a> if you need more advanced scheduling logic. These will allow you to limit the dropdown options within the scheduling form (i.e. only show patients certain appointment types or providers based on their profile).
</div>








