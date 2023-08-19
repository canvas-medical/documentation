---
title: "Asynchronous Care"
guide_for: 
---

Async care can happen in various ways, and while it’s not a new model of care delivery, it has become increasingly popular in recent years, especially since the start of the Covid-19 pandemic. The guide below outlines how you can surface patient completed questionnaires for review by your care team. It also offers suggestions on how you can leverage the structured data collected to surface recommendations based on your care model.
<br> 

* * *
## What you'll learn
In this guide, you will learn how to do the following:
- Add Questionnaires to an existing Encounter
- Write tasks to create a worklist in Canvas
- Surface recommendations based on Questionnaire responses
<br>
<br>

* * *

### Add Questionnaires to an existing Encounter
{% tabs QEA %}
{% tab QEA Developers %}
{% include alert.html type="warning" content="Some of the functionality below is only available in our updated API. If you have not yet migrated and need access, please reach out to support. " %}

Questionnaires can be added to an existing Note by adding an Encounter reference. The [FHIR Encounter Search]({{site.baseurl}}/api/encounter/) endpoint can be used to obtain the encounter_id.

```
"encounter": {
        "reference": "Encounter/(encounter_id)"
    }
```

In order for this to work, you need an Ecounter to write to. Since Canvas does not yet support a FHIR Encounter Create endpoint, you can leverage the [FHIR Appointment Create endpoint]({{site.baseurl}}/api/appointment/) . Appointments written to Canvas will automatically create an Encounter in a planned state. Note that this workflow may affect your appointment reporting. You will likely want to leverage a unique Note Type for this type of visit. Work with your Super Users to determine how the appointments should be booked.

{% include alert.html type="info" content="If your clinicians are also seeing scheduled patients, we recommend booking these asynchronous visits during off hours, either late at night or in the early morning, to prevent clutter in their calendars. You can use the same time across all incoming questionnaires." %}
<br>
{% endtab %}
{% tab QEA Super Users %}
Without specifying an Encounter, Questionnaires written to Canvas are added to a Data Import Note in the timeline. These Notes are automatically locked and cannot be updated in the application. 

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/data-import.png){:width="100%"}
{: refdef}

Writing to an open Note, using the Encounter reference, allows your clinicians to add additional documentation, including their associated diagnoses, orders, and plan, to that same Note. 

Today, this is only possible by scheduling appointments as well. Let your developers know what times of day they should be scheduled for, to avoid disruption. It may also be helpful to leverage a specific [Note Type](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-) for asynchronous care.  

{% endtab %}
{% endtabs %}

* * *


### Write tasks to create a worklist in Canvas
{% tabs TWL %}
{% tab TWL Developers %}
After a patient completes your online questionnaire, you can leverage a task to alert your team it is ready for review. 

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/work-queue.png){:width="95%"}
{: refdef}

The [FHIR Task Create and Update]({{site.baseurl}}/api/task/) endpoints allow you to assign tasks to a both individuals and or teams in Canvas. If assigning to an individual, add a practitiioner reference in the owner attribute. 

You can also assign the task to a team using the task group extension. In Canvas teams are mapped to the FHIR Group resource. Use the [FHIR Group Search]({{site.baseurl}}/api/group/) to find the necessary group ID. Teams must be configured in your admin settings. Work with your super users to set them up. 

Task labels can be added as well for quick filtering. Labels do not have to exist in your admin setting in order to be added through the API, however, the custom colors will only show if they have been assigned in admin. 


{% endtab %} 
{% tab TWL Super Users %}
The task panel is a great tool to organize work to be done. Writing tasks through the API allows you to standardize the incoming requests for your care team. 

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/work-queue.png){:width="95%"}
{: refdef}

Tasks can be assigned to individuals and/or teams in Canvas. Teams need to be configured following [these steps](https://canvas-medical.zendesk.com/hc/en-us/articles/360057499933-Admin-Teams). If you are leveraging a pool of resources that monitor incoming requests assigned to a team, they can assign themselves as part of the workflow to take ownership. Doing so will remove it from view from the other team members.

{% include alert.html type="info" content="<B>Bookmarks:</B> The task panel allow users to filter based on assignee and label. If you want to save a filtered view, you can bookmark the page. The filters are preserved in the saved url." %}

{% endtab %}
{% endtabs %}
<br>
* * *

### Surface recommendations based on Questionnaire responses
{% tabs RQR %}
{% tab RQR Developers %}
developer text
{% endtab %}
{% tab RQR Super Users %}
super user text
{% endtab %}
{% endtabs %}




