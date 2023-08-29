---
title: "Roles"
layout: documentation
---
Roles in Canvas are meant to define how a care team member is intended to participate in the care of your patients. They are used to drive default permissions and whether staff are relevant in certain clinical worfklows. When creating a new staff profile, you must assign one or more roles. Common roles include clinical roles such as MD, NP or RN, or adminstrative roles such as Administrator, Product Lead, or Developer. 

## Adding Roles

To add a new role, click ![role-button](/assets/images/role-button.png){:width="10%"} in the top right corner and then complete the following form. 

<b> Internal code: (REQ)</b> this is the unique code to identify that role; best practice is to use a meaningful abbreviation like "MD", "DO", "LCSW", "RN", etc.

<b>Public abbreviation:</b>  This can be used to add a suffix to the display names of your clinicians. It does not need to be unique. 

<b>Domain: (REQ)</b> this a choice between "Clinical", "Administrative" and "Hybrid". If a staff member’s domain is “administrative” they will not appear as an option when making additions to a patient care team. 

<b>Name: (REQ)</b> this is the human readable name that will be displayed on the Roles page (see above).

<b>Domain privilege level: (REQ)</b> if a staff has multiple roles, then the role with the highest domain privilege level determines which public abbreviation is displayed in places where the credentials are displayed. For example, if a staff has role MD and NP, and the privilege level of NP is higher, then their name may be displayed "John Smith, NP". Additionally, if the user has multiple clinical roles, then the domain privilege level may help determine whether they can prescribe and order labs (see below in "Role type").

<b>Permissions:</b> This should not be used by customers. Instead customers should determine initial permissions with "Default auth groups" (below).

<b>Role type:</b> This determines whether the role can prescribe meds and order labs. If "Provider" is selected, this role can prescribe and therefore can be selected as "Prescriber" or "Ordering provider" in the "Prescribe" and "Lab order" commands. If the staff member has more than one role in the clinical domain, then the "role type" from their role with highest domain privilege level is the one used to determine whether they can prescribe / order labs.

<b>Default auth groups for this role: </b> this determines which auth groups will be assigned to staff that are assigned this role. See more on auth groups [here]({{site.baseurl}}/documentation/permissions). Adding new roles to existing staff will add the associated auth groups. 

![role-button](/assets/images/default-auth-groups.png){:width="100%"} 

## Updating Roles

To edit a role, click into an existing role and make changes as needed. You can also take a bulk action to delete roles by checking the boxes next to each and using the action drop-down. 

Changing the default auth groups for a role only affects new staff created with that role moving forward. The autho groups assigned to existing staff would need to be updated individually. 




