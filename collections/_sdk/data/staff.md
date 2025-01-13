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

## Attributes

### Staff

| Field Name                 | Type                                         |
|----------------------------|----------------------------------------------|
| id                         | UUID                                         |
| dbid                       | Integer                                      |
| created                    | DateTime                                     |
| modified                   | DateTime                                     |
| created                    | DateTime                                     |
| modified                   | DateTime                                     |
| prefix                     | String                                       |
| suffix                     | String                                       |
| first_name                 | String                                       |
| middle_name                | String                                       |
| last_name                  | String                                       |
| maiden_name                | String                                       |
| nickname                   | String                                       |
| previous_names             | JSON                                         |
| birth_date                 | Date                                         |
| sex_at_birth               | [PersonSex](#personsex)                      |
| sexual_orientation_term    | String                                       |
| sexual_orientation_code    | String                                       |
| gender_identity_term       | String                                       |
| gender_identity_code       | String                                       |
| preferred_pronouns         | String                                       |
| biological_race_codes      | Array[String]                                |
| biological_race_terms      | Array[String]                                |
| cultural_ethnicity_codes   | Array[String]                                |
| cultural_ethnicity_terms   | Array[String]                                |
| last_known_timezone        | TimeZone                                     |
| active                     | Boolean                                      |
| npi_number                 | String                                       |
| nadean_number              | String                                       |
| group_npi_number           | String                                       |
| bill_through_organization  | Boolean                                      |
| tax_id                     | String                                       |
| tax_id_type                | [TaxIDType](#taxidtype)                      |
| spi_number                 | String                                       |
| personal_meeting_room_link | URL                                          |
| state                      | JSON                                         |
| user                       | CanvasUser                                   |
| supervising_team           | [Staff](#staff)[]                            |
| notes                      | Note[]                                       |
| creator_tasks              | [Task](/sdk/data-task/#task)[]               |
| assignee_tasks             | [Task](/sdk/data-task/#task)[]               |
| comments                   | [TaskComment](/sdk/data-task/#taskcomment)[] |

## Enumeration types

### PersonSex

| Value | Label     |
|-------|-----------|
| "F"   | "female   |
| "M"   | "male"    |
| "O"   | "other"   |
| "UNK" | "unknown" |

### TaxIDType

| Value | Label      |
|-------|------------|
| "E"   | "EIN text" |
| "S"   | "SSN"      |

<br/>
<br/>
<br/>
