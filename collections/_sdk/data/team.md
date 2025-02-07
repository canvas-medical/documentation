---
title: "Team"
slug: "data-team"
excerpt: "Canvas SDK Team"
hidden: false
---

## Introduction

The `Team` model represents a team of staff members in a Canvas instance.

## Basic usage

To get an team by identifier, use the `get` method on the `Team` model manager:

```python
from canvas_sdk.v1.data.team import Team

team = Team.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a staff object, the teams that a staff is a member of can be accessed with the `teams` attribute on a `Staff` object:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
teams = staff.teams.all()
```

## Team Members

The members of a team can be access with the `members` attribute on a `Team` object:

```python
from canvas_sdk.v1.data.team import Team
from logger import log

team = Team.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for member in team.members.all():
    log.info(f"first_name: {member.first_name}")
    log.info(f"last_name: {member.last_name}")
```

## Filtering

Teams can be filtered by any attribute that exists on the model.

Filtering for teams is done with the `filter` method on the `Team` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.team import Team

teams = Team.objects.filter(created__gt="2025-01-01")
```

## Attributes

### Team

| Field Name       | Type                                             |
|------------------|--------------------------------------------------|
| id               | UUID                                             |
| dbid             | Integer                                          |
| created          | DateTime                                         |
| modified         | DateTime                                         |
| name             | String                                           |
| responsibilities | Array[[TeamResponsibility](#teamresponsibility)] |
| members          | [Staff](/sdk/data-staff/#staff)[]                |

### TeamContactPoint

| Field Name | Type                                                                  |
|------------|-----------------------------------------------------------------------|
| id         | UUID                                                                  |
| dbid       | Integer                                                               |
| system     | [ContactPointSystem](/sdk/data-enumeration-types/#contactpointsystem) |
| value      | String                                                                |
| use        | [ContactPointUse](/sdk/data-enumeration-types/#contactpointuse)       |
| use_notes  | String                                                                |
| rank       | Integer                                                               |
| state      | [ContactPointState](/sdk/data-enumeration-types/#contactpointstate)   |
| team       | [Team](#team)                                                         |

## Enumeration types

### TeamResponsibility

| Field Name                                | Type                                            |
|-------------------------------------------|-------------------------------------------------|
| COLLECT_SPECIMENS_FROM_PATIENT            | Collect specimens from a patient                |
| COMMUNICATE_DIAGNOSTIC_RESULTS_TO_PATIENT | Communicate diagnostic results to patient       |
| COORDINATE_REFERRALS_FOR_PATIENT          | Coordinate referrals for a patient              |
| PROCESS_REFILL_REQUESTS                   | Process refill requests from a pharmacy         |
| PROCESS_CHANGE_REQUESTS                   | Process change requests from a pharmacy         |
| SCHEDULE_LAB_VISITS_FOR_PATIENT           | Schedule lab visits for a patient               |
| POPULATION_HEALTH_CAMPAIGN_OUTREACH       | Population health campaign outreach             |
| COLLECT_PATIENT_PAYMENTS                  | Collect patient payments                        |
| COMPLETE_OPEN_LAB_ORDERS                  | Complete open lab orders                        |
| REVIEW_ERA_POSTING_EXCEPTIONS             | Review electronic remittance posting exceptions |
| REVIEW_COVERAGES                          | Review incomplete patient coverages             |

<br/>
<br/>
<br/>
