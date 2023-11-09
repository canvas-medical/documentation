---
title: "Permissions"
layout: documentation
---

Security in an EMR is critical. As healthcare organizations grow, it only becomes more important. Canvas's permissions model provides a flexible framework, allowing customers to both restrict actions within the application and limit access to specific groups of patients. 


## Overview
In Canvas, there are two kinds of permissions:

- <b>Object permissions:</b> “Object” in this case means “Patient”. Therefore these permissions control which users can access which patients. If a staff does not have access to a certain patient, they cannot access any data pertaining to that patient, with a few exceptions. Exceptions include: information that can be gathered from the main search bar (name, date of birth) and information in appointments that are scheduled for that patient.

- <b>Model permissions:</b> These essentially assign read/write vs. read only vs. no access for different parts of the app. If a staff has read/write access to the clinical chart, they can write notes, enter commands, mutate patient data, etc. If they have read-only access, they can see all clinical data but make no changes. If they have no access, they will not be able to see the clinical chart, nor any clinical data present in other parts of the app (like Labs, Imaging, etc.)

Both object and model permissions are assigned in Canvas via <b>auth groups <b>

## Model permissions

Auth groups for model permissions are managed by Canvas. They cannot be altered. We provide the following auth groups:

- <b>Schedule write:</b> Allows the user to schedule new appointments and change appointment statuses.
- <b>Profile read:</b> Allows the user to read data on the patient profile, which is the page where demographics, addresses, etc. are placed. Without this group, the user will not be able to access the Patient profile at all, unless they have either the Patient create or Clinical read auth groups, which also give access at the moment.
- <b>Profile write:</b> Description: Allows the user to write data on the patient profile, which is the page where demographics, addresses, etc. are placed. Includes actions like running eligibility checks.
- <b>Clinical read:</b> Allows the user to read clinical data, both in the patient chart and in the panel views like "New labs", "New imaging", etc. Important note: because "Can view patient" is in this group, and that is the gateway permission to enter the Profile page, currently anyone with Clinical read should also get Profile read.
- <b>Clinical write:</b> Allows the user to write clinical data, both in the patient chart (e.g. creating new notes, etc.) and in the panel views like "New labs", "New imaging" (e.g. reviewing results, etc.). Also includes ability to change appointment statuses (because that is related to note state changes).
- <b>Revenue access:</b> Allows the user to access the revenue model and access claims and revenue data on the Patient profile.
- <b>Patient Create:</b> Allows the user to create new patients from the "New patient" button on the schedule page.
- <b>Document Read:</b> Allows the user the see patient's administrative documents
- <b>Document Write:</b> Allows the user to edit or remove patient's administrative documents
- <b>Data integration Access:</b> Allows the user to access data integration and take actions like upload files, link files to a patient, etc. Currently, Clinical write auth group is also required to 
- <b>Printing Access:</b> Allows the user to use fast print actions, which essentially consists of any link that includes "Print" in the title.
- <b>Tasking Access:</b> Can view and modify tasks.


## Object permissions

Follow [these instructions](/documentation/patient-groups){:target="_blank"} to create patient groups. When creating them, there is an option to use them for permissions. Selecting yes will automatically create object-based auth groups. 

Object permissions will impact user experience in the following ways:
- <b>Navigating to the patient chart:</b> If a user does not have access to a patient, they will not be able to navigate to their chart or profile. Links to the patient's chart or profile will be grayed out. If the user navigates to the URL for a patient's chart, they will encounter a generic screen with a message "You do not have permission to view this data".
- <b>Filtered patient search: </b>This search will be filtered so that patients the user does not have access to do not appear in the initial search. However, if the user clicks "See all patients" (at the bottom of the search results), then the user will see patients they do not have access to (alongside inactive or deceased patients that currently appear here). The reason for this is so that the user can verify that a patient is already in the system, and request access to them, rather than creating a new patient.
- <b>Creating a new patient:</b> Object permissions will not have an impact on creating a new patient. Users will continue to get warnings regarding duplicate patients if they try to create a new patient with the same name and DOB as an existing patient, whether or not they have access to the existing patient.
- <b>Filtered data in panel views:</b> Items assigned to staff will not be visible to them if they do not have access to the patient. It is critical to ensure that important clinical data like new lab results are not assigned to staff who do not have access to the patient.
- <b>Filtered list of patients in patients view:</b> The patients view will only include patients that the user has access to. 
	

Every instance has a default auth group called <b>“All Patients”</b>. If a staff member has access to the “All Patients” auth group, they will have access to all patients, even though it is not tied to an underlying patient group. 


## Setting permissions

### Default permissions based on role

When configuring [roles](/documentation/roles){:target="_blank"}, you can set default auth groups. Every time a new staff is created with that role, they will automatically inherit these auth groups.

Updates to roles have the following impact on auth groups assigned to staff:
- If the default auth groups are changed after a staff is created, it will have no impact on their assigned auth groups.
- If a new role is added to a staff profile, they will be assigned any auth groups associated with that role which they do not already have.
- If a role is removed from a staff, no auth groups will be removed. You must update the staff permissions of that staff member. 
 
### Manually adding and removing auth groups 

If you need to update permissions, or override the defaults set based on role, you can change the auth groups for each staff member as well. To do this, navigate to Staff Permissions in your admin menu, select the staff member, and move the group from `available groups` to `chosen groups` or vice versa. 



