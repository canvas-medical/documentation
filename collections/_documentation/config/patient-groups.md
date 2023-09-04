---
title: "Patient Groups"
layout: documentation
---

Canvas supports the ability to define patient groups. These groups can be used for a variety of purposes,<b> most importantly permissions</b>. In the context of permissions, users can be given access to a patient group, which gives them access to all patients in that patient group. This article describes how to manage patient groups.
<br>
<br>
## Adding patient groups
If you do not have access to patient groups in your settings, you may need your administrator or Canvas to provide access. Of note, access to this part of admin is granted with the "Staff permissions" auth group

To add a new patient group, click ![add-patient-group](/assets/images/add-patient-group-button.png){:width="9%"}. Enter a name for the group
If you want to use the patient group for permissions, check the checkbox which reads "Use for permissions"
What this checkbox does is to automatically create an auth group that represents access to the patient group. If that auth group is provided to a user, they will have access to all patients in the patient group.
Select save
<br>
<br>
## Updating patient groups
To edit a patient group, click into an existing patient and make changes as needed. From here you can update the name and change whether the group is used for permissions. 
<br>
<br>
###  Adding patients (manually)
You can manually add and remove patients from a patient group through the patient group membership admin page by clicking `members`. Click ![add-patient-group-member](/assets/images/add-patient-group-member-button.png){:width="12%"} and then search for the patient group and patient. Start and end dates are optional and can be leveraged to define a limited timeframe that a patient should belong to a certain group. Click locked if you want to prevent automated membership rules (see below) to be ignored, keeping the patient in the group despite not falling in the logic used to create it. 
<br>
<br>
### Removing patients (manually) 
You can remove patients from a group by changing the expiration date to today/now. 
<br>
<br>
## Using logic to manage patient group membership
As patient groups get larger, managing them manually may not be feasible. In these cases, we recommend using the Canvas Workflow Kit. See [here]({{site.baseurl}}/sdk/create-update-patient-resources/) for our technical documentation. 

You can build a protocol that defines rules that determine whether someone is a part of a group. You can leverage any data points that are available to the workflow kit, such as patient demographics (i.e what state they live in), whether a consent is on file, or care team members (patient's PCP is Dr. Smith)

Although the logic may account for the majority of cases, you may still need to override membership. You can do so in the following ways.
1. <b>Adding members to protocol managed groups:</b> If a patient is not included in the group based on your logic, but you want to add them to it manually, you can add the patient group member, making sure to select locked. This will prevent the protocol from removing that patient from the group.
 
2. <b>Excluding members from protocol managed groups:</b> Navigate to Patient group member exclusions in your admin settings and click ![add-patient-group-member-exclusion +](/assets/images/add-patient-group-member-exclusion-button.png){:width="16%"}. Search for the patient you want to exclude and provide a reason. Doing so will lock the patient out of the patient group. If they have an active patient group membership, it will automatically be expired. The workflow kit will not be able to reactivate the membership. You can delete this exclusion at any time by using the action dropdown on the admin page. 