---
title: "Care Team"
slug: "data-care-team"
excerpt: "Canvas SDK Care Team"
hidden: false
---

## Introduction

The `CareTeam` model represents a collection of [Staff](/sdk/data-staff/#staff) that are responsible for the care of a [Patient](/sdk/data-patient/#patient).

## Usage

There are 2 data models associated with Care Teams - `CareTeamMembership` and `CareTeamRole`. The `CareTeamRole` model stores all of the available roles that are available to be filled by staff members (i.e. _Physician_, _Nurse Practitioner_, etc.). For example, the following code will show the names of active roles that are available in a Canvas instance:

```python
>>> from canvas_sdk.v1.data.care_team import CareTeamRole
>>> active_care_team_roles = CareTeamRole.objects.filter(active=True)
>>> role_names = [role.display for role in active_care_team_roles]
>>> print(role_names)
['Primary care physician', 'Physician', 'Physician assistant', 'Nurse practitioner', 'Health coach', 'Care coordinator']
```

The `CareTeamMembership` model connects patients, staff members and their associated roles to make up the assembly of a patient's Care Team. To retrieve staff members and their respective roles on a patient's care team, the `care_team_memberships` attribute available on a [Patient](/sdk/data-patient/#patient) instance can be used:

```python
>>> from canvas_sdk.v1.data.patient import Patient
>>> patient_1 = Patient.objects.get(id="a74592ae8a6c4d0ebe0799d3fb3713d1")
>>> patient_1_care_team = patient_1.care_team_memberships.all()
>>> print([(ctm.role.display, ctm.staff,) for ctm in patient_1_care_team])
[('Primary care physician', <Staff: Steven Magee>), ('Nurse practitioner', <Staff: Annalies Hines>), ('Physician assistant', <Staff: Erik McDonald>)]
```

## Filtering

The `filter` method can be used to filter by desired attributes. The following examples show commonly used operations to filter care team data:

__Find a patient's care team lead__

```python
>>> from canvas_sdk.v1.data.patient import Patient
>>> from canvas_sdk.v1.data.care_team import CareTeamMembershipStatus
>>> patient_1 = Patient.objects.get(id="a74592ae8a6c4d0ebe0799d3fb3713d1")
>>> patient_1_care_team_lead = patient_1.care_team_memberships.filter(lead=True, status=CareTeamMembershipStatus.ACTIVE).first()
>>> assert patient_1_care_team_lead is not None
>>> print((patient_1_care_team_lead.staff, patient_1_care_team_lead.role,))
(<Staff: Steven Magee>, <CareTeamRole: Primary care physician>)
```

__Find all Patients that have a Certain Staff Member on their Care Team__

```python
>>> from canvas_sdk.v1.data.staff import Staff
>>> from canvas_sdk.v1.data.care_team import CareTeamMembershipStatus
>>> staff_member = Staff.objects.get(id="3640cd20de8a470aa570a852859ac87e")
>>> staff_care_teams = staff_member.care_team_memberships.filter(status=CareTeamMembershipStatus.ACTIVE)
>>> print([(ctm.patient, ctm.lead,) for ctm in staff_care_teams])
[(<Patient: Danny Boy>, True), (<Patient: Sally Mae>, False)]
```

## Attributes

### CareTeamRole

### CareTeamMembership


## Enumeration types