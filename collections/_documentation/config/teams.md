---
title: "Teams"
layout: documentation
---

Teams in Canvas are used to group work. Teams allow you to create a group staff so that they can be assigned specific tasks or be alerted of announcements that only correspond to that specific team. 
<br>
<br>
## Adding Teams

To add a new role, click ![role-button](/assets/images/add-team.png){:width="9%"} in the top right corner and then complete the following form. 

<b>Name: (REQ)</b> Name your team (i.e. Patient Care Coordinators)

<b>Responsibilities </b> Canvas creates automated tasks to support various workflows. You can assign these tasks to teams using the responsibilities. 

List of Responsibilities and Actions triggered:
* Collect Specimens from a patient: No action triggered
* Communicate diagnostic results to a patient: Will receive task with communication when delegate option is selected after diagnostic result gets review 
* Coordinate referrals for a patient: Will receive task when referral is delegated 
* Process refill requests from pharmacy: Will see notifications on refill request icon.
* Process change request from a pharmacy: No current logic behind this. (In Progress)
* Schedule lab visits for a patient: No action triggered
* Population health campaign outreach: Will receive task when campaign is created 
* Collect patient payments: Phone number assigned as contact point for team will be printed on patient statements
* Complete open lab orders: Will receive task when an open lab needs to be modified (e.g. patient address missing)
* Review electronic remittance posting exceptions: No current logic behind this. (In Progress)
* Review incomplete patient coverages: Will receive a task to finish documenting coverage

{% include alert.html type="info" content="If more than one responsibility is required, click on the line while holding down the Ctrl (Windows) or Command (Mac) key. To unselect, hold down the same key. Responsibilities amy not be shared by more than one team." %}


### Team-Staff Relationships

Assign staff memmbers to the team by clicking the plus sign and then choosing the staff object from the drop down. 
<br>
<br>
## Updating and Deleting Teams

To edit a team, click into an existing team and make changes as needed.

If you have the permissions to do so, you can delete a team by check the box and then selecting "delete selected teams" from the action dropd down and click "Go". 

{% include alert.html type="danger" content="Deleting a team that is used within task within an automation will break the automation and cause an error in the note. Please make sure to update your automations before deleting a team." %}

