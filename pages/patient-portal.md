---
permalink: /product-updates/patient-portal/
title: "Beta | Patient Portal Updates"
layout: betas
date: 2024-01-22
---

## Username & Password Login
**Access to the Canvas patient portal will soon require a username and password.**

Customers that leverage the Canvas patient portal will have new section in the profile to manage portal users. 

Phone and email capture (including verification flows) within registration will remain unchanged. However, there is now an additional step to register and invite patients to the portal. 

To invite a patient to the portal, you must link a unique email or phone to their portal user in their profile. The email and/or phone number does not necessarily have to match what have been added as contact points - but they will be **leveraged for password resets**. Once added, you can send an invite. After the patient successfully activates their account, staff can continue to trigger password reset emails if necessary.

{:refdef: style="text-align: center;"}
![description](/assets/images/patient-reg.gif){:width="98%"}
{: refdef}

{% include alert.html type="info" content="We included phone or email since some current users may only have one or the other. If you would like to link portal users via email only you can update your settings within the Constance settings in admin." %}

If you do not want this to be a manual process, a plugin can be used to automatically update the portal user based on changes to the patient contacts and trigger an invite. [Click here] for an example plugin or reach out to support to enable this workflow.

All communication will continue to be sent to the verified contact points (not the portal user email/phone). We have plans in the future to manage outbound communication via plugins, which will allow for further configuration.


### Transition
If you are a current app user, Canvas will create a plugin that identifies all patients with verified phone numbers and emails using a protocol. That protocol can be used to send your patients a customizable message via a campaign prior to the transition. You can opt to send this communication via your own CRM if preferred. We will provide a link to a [video](youtube) with instruction. This video will also be posted as a banner on the login page when we launch.

When the update is released, we will migrate preferred, verified phone numbers and emails to the user profile and trigger the invite to all users, prompting them to set a username and password. 

{:refdef: style="text-align: center;"}
![description](/assets/images/portal-invite.gif){:width="98%"}
{: refdef}

## Self Registration
`PATIENT_APP_REGISTER`

## Appointments

`PATIENT_APP_APPOINTMENTS`

### Viewing Appointments
Patients can now manage their appointments through the portal

Enabling the appointments section within constance allows all patient to: 
- See their upcoming appointments
- See their past appointments
- Join telehealth appointments
- Cancel upcoming appointments (need window of time)

### Patient Self-Scheduling
You can also now allow patients to self schedule. Note types have a two new settings, `Is scheduleable via patient portal` and `Online duration:`. If any note types have these set, patients will have the option to schedule an appointment from the appointment section or home page. 

{:refdef: style="text-align: center;"}
![description](/assets/images/portal-scheduling-settings.png){:width="98%"}
{: refdef}


The appointment search allows the patient to select the appointment type (note type), location, and optionally a provider, and date. 

The scheduling form includes a note which will translate to the comment within the Reason for Visit Command

The audit trail in the note footer will show that the appointment was created by the patient user.

{:refdef: style="text-align: center;"}
![description](/assets/images/patient-scheduling.gif){:width="98%"}
{: refdef}

If you need more advanced scheduling logic (i.e. only show patients certain appointment types or providers based on their profile) you can leverage plugins. 


## My Health

`PATIENT_APP_MY_HEALTH`

The My Health section will include a new chart summary and the current Health Records section, if enabled. Each section will mimic the filters used in the default view of the chart (if you see it in Canvas - the patient will see it on their portal)

The chart summary will show the following:

- Conditions: All conditions where show_in_summary = true. This includes active conditions and past medical history. . Patients will see the last assessed date and the name of the provider who last committed the associated assessment. 
- Medications: Active medications. 
- Allergies: Active allergies. 


## Consents
`PATIENT_APP_CONSENTS`

## Forms