---
title: "Chart Overview"
---

The patient chart represents a comprehensive digital collection of a patient's health information and includes all of the data captured during patient interactions. The Canvas chart was purpose built to help reduce the cognitive burden placed on clinicians. The three panel design allows for relevant data to be surfaced and/or easily accessible at the point of care. In this article, we will review how to navigate the chart and the functionality available within each of the following sections:

1. [Global Navigation](/documentation/chart-overview/#global-navigation)
2. [Patient Card](/documentation/chart-overview/#patient-card)
3. [Patient Summary](/documentation/chart-overview/#patient-summary)
4. Patient Timeline
5. Chart Sidepanels
6. Canvas Chat

![chart-overview](/assets/images/chart-overview.png){:width="99%"}

## Global Navigation
The global navigation stays consistent with other areas of the Canvas application. You can access your {%glossary admin settings%}, click your logo to return to the home page, or search for a patient as needed. 

### Patient Card
The patient card includes the following:
- Patient photo (or a default avatar if a photo hasn't been added)
- First and Last Name
- Preferred Name (if captured)
- Date of Birth
- Patient timezone (if enabled and captured)

<!-- DOCSTODO : Add link to constance config page on timezone-->

![Navigation](/assets/images/patient-card.png){:width="50%"}

## Patient Summary
The patient summary is located on the left hand side of the patient chart.  It provides a quick summary of essential patient details without having to move to search through notes or move to another screen.

Many of the sections are interactive. The action buttons included in each section allow care team members to leverage the existing documentation to add to their encounters. 

{% include alert.html type="warning" content="The presence and order of summary sections is not currently configurable." %}

### Social Determinants
Social determinants of health are the economic and social conditions that influence an individual's health, functioning, and quality-of-life outcomes and risks. 

In Canvas, social determinants are determined by answers to corresponding questionnaires. The `use_in_shx (REQ)` setting can be set at both the questionnaire and question level when creating [custom questionnaires](/documentation/questionnaires). Selecting `True` will display the questionnaire or question name and the date that it was last recorded within the social determinants section.

{% include alert.html type="info" content="You may see that the responses to some questions also appear in this section. We have coded that logic into the system. You cannot accomplish this with custom questionnaires; however, many Canvas provided questionnaires leverage this capability." %}

### Goals
All active goals display in the patient summary by default. From this section, you can easily reference each goal, aong with its current status and due date. 

#### Detailed View
To monitor the progress of a goal over time, you can leverage the detailed view. Click on each goal to bring up the goal modal, which includes the start date, due date, priority level, each assessment date, and their respective status. Clicking on specific assessment dates allows you to view the associated progress or barrier comments. To exit the detailed view, simply click on the `X` or anywhere outside of the modal.

![Goal Status](/assets/images/goal-status.gif){:width="99%"}

#### Sorting and Filters
Hover over the goals section header to activate the filter button. Clicking on the button will result in two dropdowns to appear. The first allows you to filter the goals based on status, choosing from `Active`, `Closed`, or `All`. The second drop-down menu allows you to sort goals either by due date or alphabetically. After adjusting your filters and sorting preferences, click on the filter icon again to hide the options. 

![Goal Filter](/assets/images/goal-filter.gif){:width="99%"}
<!-- DOCSTODO : Add combined gif and remove both above-->

### Conditions
The condition list allows you to see all of the patients medical issues and their associated ICD-10 codes at a glance. The summary section surfaces both active and historical records. The default sort logic is based on when the condition was last assessed.

#### Detailed View
The condition modal allows you to see the progression of a condition over time. Click on any condition (active or resolved) to see more details, including the onset date, the background, any medications where the condition added an an indication, and a timeline view of past actions taken during or in between encounters. From the modal, you can choose to assess or resolve the condition. To exit the detailed view, simply click on the `X` or anywhere outside of the modal.

#### Sorting and Filters
Hover over the condition section header to activate the filter button. Clicking on the button will result in two dropdowns to appear. The first allows you to filter the condition list based on status, choosing from `Active`, `Resolved`, or `All`. The second drop-down menu allows you to sort conditions either by last assessed date or alphabetically. After adjusting your filters and sorting preferences, click on the filter icon again to hide the options. 

#### Take Action
From the condition list, end users can choose to `assess` or `resolve` active conditions, `activate` resolved conditions, or add a new condition using the plus sign. Clicking on each of these buttons will prompt the user to complete additional details relevant to the action. Clicking the button again will add those details to the appropriate note based on command insertion logic noted [here]

{% include alert.html type="danger" content="After adding the necessary details, make sure to click the assess/resolve/diagnose buttons to make sure the data is added to the note. Clicking outside of the form may cause data loss, as the form does not automatically save or warn the user that navigating away will cause the input to be cleared." %}



<!-- DOCSTODO : Add GIF of condition modal-->


### Medications

#### Detailed View
#### Filters
#### Take Action

### Allergies
#### Filters
#### Take Action

### Care Team

### Vitals
#### Flowsheet

### Immunzations
#### Take Action

### Surgical History
#### Take Action

### Family History
#### Take Action

### Note

## Note Filter Button
Canvas's Note Filter function allows you to easily browse the patient's clinical timeline. 

### How to use the Note Filter button.
- Navigate to the desired patient's chart
- Select the button located at the top of the patient note
- Select the check box next to the Note Type name to filter by
- Select the Staff name to filter by 

NOTE: Filter selection should not reset when utilizing the panel filter buttons.

### FAQ

Q: Why can't I see all the provider names in the staff filter?

A: Only providers that have created notes for the patient chart will be available to filter by.

## Printing a Patient Summary
A chart summary captures the patient demographics, contact information, coverages, care team information, allergies and intolerances, immunizations, conditions, and medications.

### How to print a chart summary
- Begin with the desired patient's chart open.
- Click on the triple dot located next to the patient's name on the left hand side.
- Select `Print Chart Summary` from the drop down menu
- A PDF of the patient's chart summary generates. Review this information. 
- Select `Print`

NOTE: Adjust printer settings as desired.

## Printing a Vitals Flowsheet
Viewing and printing a flowsheet of a patient's previous vital signs allows the user to view patient vitals over a period of time in order to assess for trends and aberrations.

### How to print the vitals flowsheet
- Navigate to the left side of the chart, also known as the patient summary. 
- Scroll to `Vitals`.
- Click on the vitals table to open up a full view of the vitals table.
- Customize the desired "from" and "to" dates for printing if appropriate. 
- Select the blue `Print` icon at the bottom right of this modal.
- A print dialog box appears where you can customize the print settings.
- Select `Print`.
- You are then directed back to the vitals table without any further input necessary. 
- Click outside of the table to return to the chart.

## Printing Basic Patient Information
Printing basic patient information includes patient demographics, coverages and contact information.

### How toprint basic information
- Click on the triple dot located next to the patient's name on the left hand side. 
- Select `Print Basic Information` from the drop down menu.
- A PDF of the patient's basic information generates. Review this information. 
- Select `Print`

NOTE: Adjust printer settings as desired.

## Printing current medication and allergy list
The ability to print a patient's current medication and allergy list is often times needed to provide to the patient or other providers.   

### How to print the patient's medications and allergies
- Click on the triple dot located next to the patient's name on the left hand side 
- Select `Print Medications and Allergies` from the drop down menu
- A PDF of the patient's basic information generates
- Select `Print`

NOTE: Adjust printer settings as desired.

## Printing the patients chart
Users have the ability to generate and print the patient's entire chart.
### Patient Chart PDF from the triple dot
- Begin with the desired patient's chart open
- Click on the triple dot menu located next to the patient's name on the left hand side 
- Select `Generate Full Chart PDF` from the drop down menu and a pop up notification appears to confirm that the PDF is being generated and will appear as a task

{% include alert.html type="info" content="As stated on the notification, this process can take up to 10 minutes." %}

- Click on the Task icon located in the top right of the screen within the patient's chart

{% include alert.html type="info" content="The Task icon indicates when a new task has been assigned to the user; this is indicated by a red badge above the task." %}


- Select View on the task labeled "Chart PDF ready for _(patient's name)_" and a PDF will open in a new tab of browser
- Print the chart and if desired, download 
- Select `Done` on the task

### Patient Chart PDF Task via the Task List
- Navigate to the the panel filter badge icons on the top right which is always visible from the Schedule View
- Select Tasks icon to open the Task List
{% include alert.html type="info" content="A red badge with a number above the icon indicates new tasks to be reviewed." %}
- Select `View` on the task labeled "Chart PDF ready for _(patient's name)_" and a PDF will open in a new tab of browser
- Print the chart and if desired, download 
- Select `Done` on the task

### FAQ:
Q: Do I have to wait in the patient chart for the full 10 minutes?

A: No, you can move on with other tasks inside or outside of the patient chart.  You will receive a task notification on the task list when the PDF is ready.

Q: Can I print only a specific time frame?

A: When generating a Full Chart PDF the entire patient chart is included, however you can select specific pages to print when the PDF is completed. 

Q: What is included in the PDF?

A: The PDF includes anything documented in Canvas along with any scanned documents.