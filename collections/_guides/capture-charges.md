---
title: "Capture Charges"
guide_for:
---
Canvas makes it easy to charge for the services you provide by integrating your fees directly into the documentation.  Use this guide to learn how to set your charges and capture them through commands. 
<br>
<br>
* * *
## What you'll learn
In this guide, you will learn how to do the following:
1. Configure your fee schedule and discounts
2. Use your documentation to add charges
<br>
<br>

* * *

### 1. Configure your fee schedule and discounts

You can set charges by configuring your [fee schedule](/documentation/fee-schedule) in admin. Determining what to charge is ultimately up to you but here are a few methods that might be helpful.
* set charges based on costs of services
* set charges based on your contracted rates
* set charges based on a set percentage of medicare. 


{% include alert.html type="info" content="You will want to make sure your charges are higher than your allowables to ensure you are receiving full payment from payers. You can create a report using our read-only replica that flags payments equaling 100% of charges to indicate where your fee schedule may be too low." %}

You can then apply [discounts](/documentation/discounts) for cash pay patients. 
<br>
<br>
* * *
### 2. Use your documentation to add charges

The perform command pulls from your fee schedule. You can control what shows here by adding new codes or removing procedures that are not relevant to your care model.  We recommend creating [automations](/documentation/automations) to tie specific procedure codes to your documentation. 

You can also use a structured assessment. A structured assessment is a type of [questionnaire](documentation/questionnaires) that allows you to link ICD-10 and CPT codes to the responses. You can use these to build templates that document and charge for the services provided. 

{% include alert.html type="warning" content="Using a structured assessment to add a diagnosis may add duplicate conditions to the condition list if already present without a warning. We recommend continuing to use the assess command for already diagnosed conditions."  %}

![structured assessment](/assets/images/sa.gif){:width="100%"}

