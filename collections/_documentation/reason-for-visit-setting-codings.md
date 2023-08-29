---
title: "Reason for Visit Setting Codings"
layout: documentation
---
The Reason for Visit command frames the motivation for an encounter. In Canvas, you have the option to have a structured on unstructured reason for visit. If enabling structured reason for visits, you can configure them in your admin settings. 

{% include alert.html type="warning" content="You must set STRUCTURED_REASON_FOR_VISIT_ENABLED to true in your constance config settings to leverage this functionality." %}

Navigate to Reason For Visit Setting Codings under the Practice section of your admin settings. 

## Adding Structured Reason for Visits

To add a new structured reason for visit, click ![rfv-button](/assets/images/structured-rfv-button.png){:width="18%"} in the top right corner and then complete the following form. 

<b>System:</b> This refers to the system that the code below belongs to. Canvas supports using the following existing systems, ICD10, CPT, SNOMED, and LOINC, or you can leverage a custom code by specifying INTERNAL as the system.

<b>Code</b> This should be a unique code used to represent the reason for visit. 

<b>Display:</b> This is what your end user will select when choosing a reason for visit when scheduling appointments, or using the Reason for Visit or Follow Up Commands. 

<b>Possible durations:</b> When scheduling, end users will only be able to choose from the associated durations. This allows you to define how much time should be alotted to certain types of visits. The available options are controlled by configuring [Schedule Durations] under your admin settings.  

## Updating Structured Reason for Visits 

To edit a reason for visit setting coding, click into an existing reason for visit setting and make changes as needed.