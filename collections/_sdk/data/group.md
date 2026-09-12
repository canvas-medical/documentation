---
title: "Group"
slug: "data-group"
excerpt: "Canvas SDK Group"
hidden: false
---

## Introduction

The `Group` model is a stable external identifier that Canvas attaches — through a generic relation (`content_type` + `object_id`) — to either a [Team](/sdk/data-team/) or a [PatientGroup](/sdk/data-patient-group/#patientgroup). It is the model the FHIR Group resource surfaces.

## Basic usage

Use the `team` and `patient_group` properties to resolve the record a group points at. Each returns its target only when the group's `content_type` matches, and `None` otherwise:

```python?partial=true
from canvas_sdk.v1.data import Group

group = Group.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

if group.patient_group:
    print(group.patient_group.name)
elif group.team:
    print(group.team.name)
```

## Attributes

### Group

| Field Name   | Type                                               | Description                                          |
| ------------ | -------------------------------------------------- | ---------------------------------------------------- |
| id           | UUID                                               | The universally unique identifier for this record.   |
| dbid         | Integer                                            | The database identifier for this record.             |
| created      | DateTime                                           | When the record was created.                         |
| modified     | DateTime                                           | When the record was last modified.                  |
| content_type | [ContentType](/sdk/data-content-type/#contenttype) | The type of record this group points at.             |
| object_id    | Integer                                            | The database id of the record this group points at.  |

## Properties

| Name          | Type                                                            | Description                                                                          |
| ------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| team          | [Team](/sdk/data-team/) \| `None`                               | The linked `Team` when `content_type` is a team; otherwise `None`.                  |
| patient_group | [PatientGroup](/sdk/data-patient-group/#patientgroup) \| `None` | The linked `PatientGroup` when `content_type` is a patient group; otherwise `None`. |

<br/>
<br/>
<br/>
