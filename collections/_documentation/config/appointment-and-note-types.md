---
title: "Appointment and Note Types"
layout: documentation
---

The differentiated care models of our customers often include all types of patient interactions, including in-person visits, telehealth, and asynchronous encounters. Configuring appointment and note types allow you to tailor your scheduling and visit settings to your care model. To configure your interaction modes and scheduling needs, navigate to `Appointment and Note Types` under your Pracice settings. 

**Note types** generate notes in the timeline. They can be associated with appointments or added through the new note dropdown in the Chart. Patients are required. These should be used to schedule and document your patient interactions.<br>
![visit-types](/assets/images/visit-types.png){:width="31%"}
![add-note](/assets/images/add-note.png){:width="17%"}

**Appointment types** are used to configure `other events.` They do not generate notes in the timeline and do not require a patient. These are great for blocking time. <br>
![event-types](/assets/images/event-types.png){:width="31%"}
<br>
<br>

## Adding Note Types
The following note types are automatically added to your instance upon creation: 
- Home visit
- Telehealth
- Office visit
- Lab visit
- Inpatient visit
- Phone call
- Chart review - used when commands are added through the chart without having your cursor in an existing note. 
- Letter
- Message
- Data Import - used for data added through the API without an `encounter` reference

To add a new note type click ![create note type](/assets/images/create-note-type.png){:width="10%"} and complete the following form

**Name:** The name of the note type.  

**Icon:** Image to be used on the appointment card and notes header. 

**System:** System/code must be a unique pair for active note types. These will be used as an identifier to create appointments with the FHIR API.

**Code:** System/code must be a unique pair for active note types. These will be used as an identifier to create appointments with the FHIR API.

**Display:** This is a description of the code, which would only be seen when reading appointments by the API. (Users often input the same value for Name and Display)

**Rank:** Determines the order in which notes are listed within the scheduling modal drop down and add note drop down in the chart.

**Is Scheduleable:** When checked this note type will be available as an appointment type, whether scheduling from the Schedule page, from the patient chart via New Note > Appointment, or via the API.

**Is default appointment type:** When checked this type will be the default selection for a new appointment whether scheduling from the UI, or via the API. Only one note type can be the default.

**Is billable:** When checked notes of this type will generate claims

**Is telehealth:** When checked notes of this type will have a telehealth button on the header

**Defer place of service to practice location:**When checked notes of this type will defer their place of service code to the value selected in the respective practice location. This place of service will be applied to the claim for the note.

**Available places of service:**  This is only relevant if “Defer place of service to practice location” (above) is unchecked and is billable is checked. 

**Default place of service:** If a type has multiple possible places of service use this field to select the one that is going to be selected by default on the note footer

**Is active checkbox:** If you uncheck this box, notes of this type will no longer be options in the “New Note” dropdown in the patient chart or when scheduling.
<br>
<br>
## Adding Appointment Types

To add a new appointment type click ![create appointment type](/assets/images/create-appointment-type.png){:width="14%"} and complete the following form

**Name:** The name of the appointment type.  

**Icon:** Image to be used on the appointment card.

**System:** System/code must be a unique pair for active appointment types. These will be used as an identifier to create appointments with the FHIR API.

**Code:** System/code must be a unique pair for active appointment types. These will be used as an identifier to create appointments with the FHIR API.

**Display:** This is a description of the code, which would only be seen when reading appointments by the API. (Users often input the same value for Name and Display)

**Rank:** Where each unique appointment type ranks with all other appointments and note types and impacts the order in which appointments are listed within the scheduling modal dropdown. 

**Possible Durations:** Users will have the ability to select the possible durations to be associated with each appointment type. Additional durations can be added within the “Schedule durations” settings page. 

**Is patient required checkbox:** By checking this box, the associated appointment type will require a patient to be added to the appointment. By default this checkbox is unchecked so that “other event” appointments can be scheduled without a new for a patient. Even when the checkbox is unchecked, a patient can be included if a user would prefer.

**Allow custom title checkbox:** Checking this box allows users to enter a custom title for appointments of this type within the schedule modal. This custom title within the scheduling workflow will be the title of the event in the scheduling view block and tile. It provides users with the flexibility of having a generic appointment type that can be customized by each user on the frontend.  

**Is active checkbox:** When this box is unchecked, this appointment type will not appear as an option when scheduling “other events”
<br>
<br>
## Updating and Inactivating Appointment and Note Types
To edit an appointment or note type, click into an existing appointment or note type and make changes as needed. You can also take a bulk action to deactivate appointment and note types by checking the boxes next to each and selecting deactivate in the action drop-down. 

{% include alert.html type="info" content="Changes made to appointment and note types will only impact appointment and notes created after the change. Changes are not retroactive." %}


Deactivating appointment and note types does not prevent them from being added programmatically. For example, sometimes “Date import” type notes are created to import Data into Canvas. This could continue to happen even if “Data import” type note is marked inactive.




