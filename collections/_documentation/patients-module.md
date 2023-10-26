---
title: "Patients Module"
layout: documentation
---

## Introduction {#h_01HDP9051Q4K1J3D0DFSGN2RQX}

Historically, EMRs treat the schedule as the home page. However, for high-touch care models with a lot of asynchronous care, a more intuitive home page is a list of all patients under a provider’s care. The Patient Module serves this role. It displays a filterable list of all patients in a table.

![mceclip0.png](/assets/images/patients-module/screenshot.png){:width="100%"}

## Navigating to the patients module

To navigate to the patients module, click the main hamburger menu and select **Patients**.

![navigating](/assets/images/patients-module/navigating.png){:width="250"}

## Sorting and filtering the list of patients

The list of patients can be sorted according to patient name, facility (note that facilities are managed on the Patient profile page <link>), or date the patient was last seen (this is defined as the last encounter-type note in the patient’s chart).

The list of patients can also be filtered by patient name, care team, and facility name. Filtering by care team members is the most commonly used functionality. The way this works is the list of patients will be filtered down to any patient who has any of the selected staff members on their care team.

![staff-list](/assets/images/patients-module/staff-list.png){:width="250"}

A user’s sorting and filtering selections are remembered. Therefore if a user filters the Patients list to patients under their care, this filter will remain next time the user accesses the Patients view.

## Viewing protocol status

A column of particular interest in the Patients Module is the protocol column. This column allows the user to view the status of multiple protocols for each patient. In order to adjust which protocols are displayed, click the pen icon next to the column header name.

![header](/assets/images/patients-module/header.png){:width="250"}

This displays a modal in which the protocols to be displayed can be selected.

![modal](/assets/images/patients-module/modal.png){:width="500"}

After clicking “Done”, the status of each protocol is represented by a dot. Red means “Due”, Green means “Satisfied”, White means “Not applicable”. Hovering over each dot displays the name of the protocol.

![dots](/assets/images/patients-module/dots.png){:width="250"}

## Built-in protocols

Canvas offers tremendous flexibility to customize the user interface, automate workflows, surface specially tailored recommendations at the site of care. To learn more about this, check out our [SDK documentation](/sdk).

However, for ease of use, Canvas ships with several built-in protocols that require zero developer work to use. These represent standard quality measures that many practices may want to use. They can be turned on and off easily<!-- TODO: link to protocol settings -->. These built-in protocols are described below.
