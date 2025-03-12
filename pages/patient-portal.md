---
permalink: /product-updates/patient-portal/
title: "Beta | Patient Portal Updates"
layout: betas
date: 2024-01-22
---

## Username & Password Login
**Access to the Canvas patient portal will soon require a username and password.**

Customers that use the Canvas patient portal will have new section in the profile to manage portal users. 

Phone and email capture (including verification flows) within registration will remain unchanged; however, there is now an additional step to register and invite patients to the portal. 

To invite a patient to the portal, you must link a unique email or phone to their portal user in their profile. The email and/or phone number do not necessarily have to match what have been added as contact points - but they will be **leveraged for password resets**. Once added, you can send an invite. After the patient successfully activates their account, staff can continue to trigger password reset emails if necessary.

{:refdef: style="text-align: center;"}
![description](/assets/images/patient-reg.gif){:width="98%"}
{: refdef}

{% include alert.html type="info" content="We included phone or email since some current users may only have one or the other. If you would like to link portal users via email only, you can update your settings within constance config in admin." %}

If you do not want this to be a manual process, a plugin can be used to automatically update the portal user based on changes to the patient contacts and trigger an invite. [Click here] for an example plugin or reach out to support to enable this workflow.

All communication will continue to be sent to the verified contact points (not the portal user email or phone). We have plans in the future to manage outbound communication via plugins, which will allow for further configuration.


### Transition
If you are a current app user, Canvas will create a plugin that identifies all patients with verified phone numbers and emails using a protocol. That protocol can be used to send your patients a customizable message via a campaign prior to the transition. You can opt to send this communication via your own CRM if preferred. We will provide a link to a [video](youtube) with instructions. This video will also be posted as a banner on the login page when we launch.

When the update is released, we will migrate preferred, verified phone numbers and emails to the user profile and trigger the invite to all users, prompting them to set a username and password. 

{:refdef: style="text-align: center;"}
![description](/assets/images/portal-invite.gif){:width="98%"}
{: refdef}

## Appointments

Enabeled through: `PATIENT_APP_APPOINTMENTS` in Constance config.

### Viewing Appointments
Patients can now manage their appointments through the portal

Enabling the appointments section within constance allows all patients to: 
- See their upcoming appointments
- See their past appointments
- Join telehealth appointments
- Cancel upcoming appointments (need window of time)

### Patient Self-Scheduling
You can also now allow patients to self schedule. Note types have two new settings, `Is scheduleable via patient portal` and `Online duration:`. If any note types have these set, patients will have the option to schedule an appointment from the appointment section or home page. 

{:refdef: style="text-align: center;"}
![description](/assets/images/portal-scheduling-settings.png){:width="98%"}
{: refdef}


The appointment search allows the patient to select the appointment type (note type), location, and optionally a provider, and date. 

The scheduling form includes a note which will translate to the comment within the reason for visit Command.

The audit trail in the note footer will show that the appointment was created by the patient user.

{:refdef: style="text-align: center;"}
![description](/assets/images/patient-scheduling.gif){:width="98%"}
{: refdef}

You can leverage plugins if you need more advanced scheduling logic (i.e. only show patients certain appointment types or providers based on their profile).  


## My Health

Enabeled through: `PATIENT_APP_MY_HEALTH` in Constance config.

The My Health section will include a new chart summary and the current Health Records section, if enabled. Each section will mimic the filters used in the default view of the chart (if you see it in Canvas - the patient will see it on their portal)

The chart summary will show the following:

- **Conditions:** All conditions where show_in_summary = true. This includes active conditions and past medical history. Patients will see the last assessed date and the name of the provider who last committed the associated assessment. 
- **Medications:** Active medications. Patients will see the name of the medication, start date, instructions (sig), and the last prescriber.
- **Allergies:** Active allergies. Patients will see all available fields (allergy, severity, reaction, and onset date).


## Consents

Enabled though: `PATIENT_APP_CONSENTS` in Constance config

You can now ask patients to complete their consents via the portal. When configuring consents, there are three new settings: 
- **Document:** PDF of the consent. Patient will see a link to review this document. 
- **Description:** Used as a title / summary for the consent. The patient sees this in their list of consents to review. 
- **Show in Patient Portal:** Only consents with this checked will appear in the portal. 

When a patient logs in, the portal will assess whether the necessary portal consents have been acknowledged by the patient and then prompt the patient to complete any outstanding consents. Mandatory consents must be agreed to in order to continue. Non-mandatory consents can be skipped.

{:refdef: style="text-align: center;"}
![description](/assets/images/portal-consents.png){:width="50%"}
{: refdef}

The responses will then be recorded in the patient profile. Accepted consents will show `accepted via patient portal` and skipped consents will appear as `rejected via patient portal.` A copy of the consent is not saved. 

{:refdef: style="text-align: center;"}
![description](/assets/images/portal-consents-profile.png){:width="70%"}
{: refdef}
