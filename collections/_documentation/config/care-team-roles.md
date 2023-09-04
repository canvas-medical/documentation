---
title: "Care Team Roles"
layout: documentation
---

Care teams in Canvas allow you to easily assign care staff members to one patient allowing you to build a team with multidisciplinary skills. You can configure your Care Team Roles to support your care model. 

{% include alert.html type="warning" content="The care team switch needs to be enabled to leverage care teams and set care team roles. Please contact Canvas Support for assistance enabling this switch." %}

Navigate to Care Team Roles in your admin settings. New instances are created with the following roles, using SNOMED codes. They can be updated and made inactive if they are not needed. 

![default-care-team-roles](/assets/images/default-care-team-roles.png){:width="60%"}

## Adding Care Team Roles

To add a new role, click ![care-team-role-button](/assets/images/add-care-team-role.png){:width="10%"} in the top right and then complete the following form:

<b>System:</b> This refers to the system that the code below belongs to. Canvas supports using the following existing systems, ICD10, CPT, SNOMED, and LOINC, or you can leverage a custom code by specifying INTERNAL as the system.

<b>Version</b> This is not required

<b>Code</b> This should be a unique code used to represent the Care Team Role.

<b>Display:</b> This is what your end user will select when assigning care team membership in the patient's profile and what is visible in clinical workflows (in the chart and when assigning tasks, document, etc).

<b>Active:</b> This determines whether the role is available for use <br><br>

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/care-team-roles.gif){:width="100%"}
{: refdef}

## Updating Care Team Roles

To edit a care team role, click into an existing care team role and make changes as needed. You can also take bulk actions to activate or deactive care team roles by checking the boxes next to each and using the action drop-down. 
