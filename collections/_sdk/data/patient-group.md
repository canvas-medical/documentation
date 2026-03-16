---
title: "Patient Group"
slug: "data-patient-group"
excerpt: "Canvas SDK Patient Group"
hidden: false
---

## Introduction

The `PatientGroup` model represents a named collection of patients. Patients are associated with a group through the `PatientGroupMember` model, which tracks membership along with start/end dates and active status.

## Basic usage

To get a patient group by identifier, use the `get` method on the `PatientGroup` model manager:

```python
from canvas_sdk.v1.data.patient_group import PatientGroup

group = PatientGroup.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

To get the members of a group:

```python
from canvas_sdk.v1.data.patient_group import PatientGroup

group = PatientGroup.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for patient in group.members.all():
    log.info(f"Patient: {patient.id}")
```

If you have a patient object, the groups that a patient belongs to can be accessed with the `patient_groups` attribute on a [Patient](/sdk/data-patient/#patient) object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="a74592ae8a6c4d0ebe0799d3fb3713d1")
groups = patient.patient_groups.all()
```

## Membership

The `PatientGroupMember` model represents a patient's membership in a group. To access the membership records for a group:

```python
from canvas_sdk.v1.data.patient_group import PatientGroup, PatientGroupMember

group = PatientGroup.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

# Get active members
active_members = PatientGroupMember.objects.filter(patient_group=group, active=True)

for membership in active_members:
    log.info(f"Patient: {membership.member.id}, Start: {membership.start_date}")
```

## Filtering

Patient groups and memberships can be filtered by any attribute that exists on the model.

### By name

```python
from canvas_sdk.v1.data.patient_group import PatientGroup

groups = PatientGroup.objects.filter(name="Diabetes Management")
```

### By active membership

```python
from canvas_sdk.v1.data.patient_group import PatientGroupMember

active_memberships = PatientGroupMember.objects.filter(active=True, patient_group__name="Diabetes Management")
```

## Attributes

### PatientGroup

| Field Name | Type                            |
| ---------- |---------------------------------|
| id         | UUID                            |
| name       | String                          |
| members    | [Patient](/sdk/data-patient/)[] |

### PatientGroupMember

| Field Name    | Type                          |
| ------------- |-------------------------------|
| created       | DateTime                      |
| modified      | DateTime                      |
| patient_group | [PatientGroup](#patientgroup) |
| member        | [Patient](/sdk/data-patient/) |
| start_date    | DateTime                      |
| end_date      | DateTime (nullable)           |
| locked        | Boolean                       |
| active        | Boolean                       |

<br/>
<br/>
<br/>
