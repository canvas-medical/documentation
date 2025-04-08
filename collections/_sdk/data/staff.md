---
title: "Staff"
slug: "data-staff"
excerpt: "Canvas SDK Staff"
hidden: false
---

## Introduction

The `Staff` model represents a staff member in a Canvas instance.

To get a `Staff` object by it's identifier, use the `get` method:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")
```

`Staff` objects are commonly used in related models, for example the `Task` model.
To see all of a staff member's assigned or created tasks, the following code can be used:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")

staff.assignee_tasks.all()
# <QuerySet [<Task: Task object (3)>]>

staff.creator_tasks.all()
# <QuerySet [<Task: Task object (7)>]>
```

To show a Staff member's contact points (email, phone, etc.), the `telecom` attribute can be used. For example:

```python
>>> from canvas_sdk.v1.data.staff import Staff

>>> staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")

>>> [(t.system, t.value,) for t in staff.telecom.all()]
[('phone', '8005551416'), ('email', 'support@canvasmedical.com')]
```

## Attributes

### Staff

| Field Name                 | Type                                                            |
|----------------------------|-----------------------------------------------------------------|
| id                         | UUID                                                            |
| dbid                       | Integer                                                         |
| created                    | DateTime                                                        |
| modified                   | DateTime                                                        |
| created                    | DateTime                                                        |
| modified                   | DateTime                                                        |
| prefix                     | String                                                          |
| suffix                     | String                                                          |
| first_name                 | String                                                          |
| middle_name                | String                                                          |
| last_name                  | String                                                          |
| maiden_name                | String                                                          |
| nickname                   | String                                                          |
| previous_names             | JSON                                                            |
| birth_date                 | Date                                                            |
| sex_at_birth               | [PersonSex](/sdk/data-enumeration-types/#personsex)             |
| sexual_orientation_term    | String                                                          |
| sexual_orientation_code    | String                                                          |
| gender_identity_term       | String                                                          |
| gender_identity_code       | String                                                          |
| preferred_pronouns         | String                                                          |
| biological_race_codes      | Array[String]                                                   |
| biological_race_terms      | Array[String]                                                   |
| cultural_ethnicity_codes   | Array[String]                                                   |
| cultural_ethnicity_terms   | Array[String]                                                   |
| last_known_timezone        | TimeZone                                                        |
| active                     | Boolean                                                         |
| primary_practice_location  | [PracticeLocation](/sdk/data-practicelocation/)                 |
| npi_number                 | String                                                          |
| nadean_number              | String                                                          |
| group_npi_number           | String                                                          |
| bill_through_organization  | Boolean                                                         |
| tax_id                     | String                                                          |
| tax_id_type                | [TaxIDType](/sdk/data-enumeration-types/#taxidtype)             |
| spi_number                 | String                                                          |
| personal_meeting_room_link | URL                                                             |
| state                      | JSON                                                            |
| user                       | [CanvasUser](/sdk/data-canvasuser)                              |
| supervising_team           | [Staff](#staff)[]                                               |
| notes                      | Note[]                                                          |
| creator_tasks              | [Task](/sdk/data-task/#task)[]                                  |
| assignee_tasks             | [Task](/sdk/data-task/#task)[]                                  |
| comments                   | [TaskComment](/sdk/data-task/#taskcomment)[]                    |
| care_team_memberships      | [CareTeamMembership](/sdk/data-care-team/#careteammembership)[] |
| teams                      | [Team](/sdk/data-team/#team)[]                                  |
| telecom                    | [StaffContactPoint](#staffcontactpoint)[]                       |

### StaffContactPoint

| Field Name         | Type                                                                  |
|--------------------|-----------------------------------------------------------------------|
| id                 | UUID                                                                  |
| dbid               | Integer                                                               |
| system             | [ContactPointSystem](/sdk/data-enumeration-types/#contactpointsystem) |
| value              | String                                                                |
| use                | String                                                                |
| use_notes          | String                                                                |
| rank               | Integer                                                               |
| state              | [ContactPointState](/sdk/data-enumeration-types/#contactpointstate)   |
| staff              | [Staff](#staff)                                                       |

<br/>
<br/>
<br/>
