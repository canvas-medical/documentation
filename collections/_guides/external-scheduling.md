---
title: "External Scheduling"

---

Maximizing scheduling efficiency is necessary to grow and support high volumes of patients. Allowing your patients to self schedule will support both a better patient experience, while also saving your care team time. In order to be successful, the complexities of patient scheduling needs to be built into the workflow. You may want to build complex logic into your own scheduling experience, or leverage a third party partner when first launching. Either way, Canvas’s FHIR API and Workflow Kit allow for a deep scheduling integration. 
<br> 
<br>
* * *
## What you'll learn
In this guide, you will learn how to do the following:
- Configure scheduling in Canvas
- Manage appointments through the FHIR API
- Sync appointments to third party calendars
- Send appointment confirmation messages 
<br>
<br>

* * *

### Configure scheduling in Canvas
{% tabs CSIC %}
{% tab CSIC Super Users %}
Before partnering with your dev team to build external schedling workflows, you will need to configure Canvas's advanced scheduling capabilities as follows.<br><br>
[Availability:](https://canvas-medical.zendesk.com/knowledge/articles/360058400553/en-us?brand_id=360005403014&return_to=%2Fhc%2Fen-us%2Farticles%2F360058400553) Provider Availability in Canvas is managed through an integration with Google Calendar. This allows you to set availability using recurring events that are easy to update as needed. Updates made in gCal will reflect within Canvas in minutes. You can set availability at the location level or leave the location empty to have it be set for the clinician across locations. <br><br>
[Note Types:](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-) The differentiated care models of our customers often include all types of patient interactions, including in-person visits, telehealth, and asynchronous encounters. You can configure your note types to fit your offering by creating completely custom note types and codes, or, you can use an established system such as [LOINC®](https://loinc.org/LG41826-5) codes.<br><br>
[Appointment Types:](https://canvas-medical.zendesk.com/hc/en-us/articles/15704289792659-Scheduling-Other-Events-#h_01GXV9832Z74GRAQKDD4JA9677) Creating Custom Appointment Types allows your team to schedule Other Events that block time but do not generate Notes within the Timeline. They can be associated with a specific patient (but do not require one) and can be used to account for meetings, travel time, or co-visits during which multiple clinicians need to be included, but only one Note needs to be generated. <br><br>
[Structured Reason for Visit:](https://canvas-medical.zendesk.com/hc/en-us/articles/4417495811859-Structured-Reason-for-Visit) Structured Reason for Visit is a setting that can be enabled in Canvas. In doing so you can define a set of reasons and then associate one or more possible durations with each. This can help ensure your team follows set scheduling guidelines. Alternatively, the unstructured option allows the scheduler to free text the reason and choose the duration from any of the configured options. 

{% endtab %}
{% tab CSIC Developers %}
After your team completes the scheduling set up in Canvas, you will want to take note of the naming conventions and code systems used. You can access them in the associated admin menus. 

{% endtab %}
{% endtabs %}
<br>
* * *
### Manage appointments through the FHIR API
{% tabs MAPP %}
{% tab MAPP Developers %}
The following endpoints support scheduling in Canvas:<br><br>
[FHIR Schedule Search:]({{site.baseurl}}/api/schedule/) The schedule ID returned in the response payload is important when searching for bookable time slots for appointments.The schedule ID allows you to find the staff’s availability at a specific location.<br><br>
[FHIR Slot Search:]({{site.baseurl}}/api/slot/) You can define your own scheduling logic, using the query params to only return availability for clinicians that match based on specialty and/or state licensure.<br><br>
[FHIR Appointment Create:]({{site.baseurl}}/api/appointment/) Our customers have the option to create [Structured Reason for Visits](https://canvas-medical.zendesk.com/hc/en-us/articles/4417495811859-Structured-Reason-for-Visit). If configured, the codings can be utilized in the FHIR request payload in the reasonCode attribute.<br><br>
{% endtab %}
{% tab MAPP Super Users %}
Make sure to update your team when you update your settings in Canvas. Also note that appointments made using the API will show as scheduled by "Canvas Bot".
{% endtab %}
{% endtabs %}
<br>
* * *






