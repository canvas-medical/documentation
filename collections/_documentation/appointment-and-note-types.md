---
title: "Appointment and Note Types"
---

The differentiated care models of our customers often include all types of patient interactions, including in-person visits, telehealth, and asynchronous encounters. Configuring appointment and note types allow you to tailor your scheduling and visit settings to your care model. 

To configure your interaction modes and scheduling needs, navigate to `Appointment and Note Types` under your Pracice settings. 

## Note Types


## Appointment Types

Click ![create appointment type](/assets/images/create-appointment-type.png){:width="10%"} to configure `Other Events`. `Other Events` do not need to be associated with a patient and do not generate notes, allowing for greater flexibility. 

Required information to input:

Name: Which should be the name of the appointment type.  
Icon: Image to be used on notes header. You may pick an icon name from this page.
System: System/code must be a unique pair for active appointment types. These will be used as an identifier to create appointments with the FHIR API.
Code: System/code must be a unique pair for active appointment types. These will be used as an identifier to create appointments with the FHIR API.
Display: This is a description of the code, which would only be seen when reading appointments by the API. (Users often input the same value for Name and Display)
Possible Durations: Users will have the ability to select the possible durations to be associated with each appointment type. Additional durations can be added within the “Schedule durations” settings page. 
Optional information to input:

Rank: Where each unique appointment type ranks with all other appointments and note types and impacts the order in which appointments are listed within the scheduling modal dropdown. 
Is patient required checkbox: By checking this box, the associated appointment type will require a patient to be added to the appointment. By default this checkbox is unchecked so that “other event” appointments can be scheduled without a new for a patient. Even when the checkbox is unchecked, a patient can be included if a user would prefer.  
Allow custom title checkbox: Checking this box allows users to enter a custom title for appointments of this type within the schedule modal. This custom title within the scheduling workflow will be the title of the event in the scheduling view block and tile. It provides users with the flexibility of having a generic appointment type that can be customized by each user on the frontend.  
Is active checkbox: When this box is unchecked, this appointment type will not appear as an option when scheduling “other events”
Once new appointments have been saved, they will appear within the “Event Type” dropdown of the “Other Events” tab in the scheduling modal. 
## Note Types

Key Objectives
You will learn how to enable configurable note types.
You will learn how to configure note types.
You will learn how place of service (POS) is determined.
Video 
Review a recording of our live Webinar reviewing configuration of note types



FAQ
Q: What are base note types? 

A: Canvas ships out with a preset list of base notes. Base note types include the following:

Home visit
Telehealth
Office visit
Lab visit
Inpatient visit
Phone call
Chart review
Letter
Message
Data
Tips & Tricks
 Settings > Note types will show a list of all note types available in your Canvas environment along with details for that note type.
mceclip1.png

Navigating to Settings > Note types also allows you to filter by active, scheduleable, billable, and telehealth note types. 
mceclip0.png

Step By Step
Configure note types
Begin in the schedule view
Locate and select the triple line menumceclip4.png
Locate and select Settings
Locate and select Note Types
Selectmceclip0.png
Fill in the following fields:
*Name: Name must be unique
*Icon: Name of icon to be used on notes header (Icon names come from this page)
*System: System/Code must be a unique pair for active note types.
System will be used as an identifier to create appointments via the FHIR API.
*Code: System/Code must be a unique pair for active note types.
Code will be used as an identifier to create appointments via the FHIR API.
*Display: Description of the code used when reading appointments/note types via the API. This will not be seen in the Canvas UI. Only “Name” will be seen in the UI.
*Rank: Place on drop down list (defaults to 99)
Check or uncheck the following settings to enable / disable them 
Is Scheduleable: When checked this note type will be available as an appointment type, whether scheduling from the Schedule page, from the patient chart via New Note > Appointment, or via the API.
Is default appointment type:When checked this type will be the default selection for a new appointment whether scheduling from the UI, or via the API. Only one note type can be the default.
Is billable: When checked notes of this type will generate claims
Is telehealth: When checked notes of this type will have a telehealth button on the header
Defer place of service to practice location:When checked notes of this type will defer their place of service code to the value selected in the respective practice location. This place of service will be applied to the claim for the note.
Select one or more Available places of service, if appropriate. This is only relevant if “Defer place of service to practice location” (above) is unchecked.
Ensure you use the mceclip2.png buttons to move permissions to the "Chosen" column
Select a Default place of service: If a type has multiple possible places of service use this field to select the one that is going to be selected by default on the note footer
Check or uncheck the Is active checkbox to enable or disable the note type as an option in the UI for new appointments / notes. If you uncheck this box, notes of this type will no longer be options in the “New Note” dropdown in the patient chart. However, notes of this type could still be created programmatically, or via the API. For example, sometimes “Date import” type notes are created to import Data into Canvas. This could continue to happen even if “Data import” type note is marked inactive.
Select mceclip3.png
Ensure you see a message stating the changes were saved successfully at the top of the page mceclip5.png
NOTE: * text above signals a required fields when setting up note types. Changes made to existing or new note types will apply to all end users across your organization's environment.

NoteTypes.gif

Place of Service (POS)
As background, Place of service is a billing concept that is included in every claim created in Canvas. The options for place of service are determined by CMS.

As shown above, Configurable note types allows you to configure the place of service for each note type. The algorithm to determine which place of service ultimately goes on the claim is as follows:

