---
title: "Group"
slug: "data-group"
excerpt: "Canvas SDK Group"
hidden: false
---

## Introduction

The `Group` model gives you the stable external identifier Canvas uses to expose a [Team](/sdk/data-team/#team) or a [PatientGroup](/sdk/data-patient-group/#patientgroup) as a single FHIR resource, so you can move between an SDK record and its FHIR representation without tracking a separate identifier yourself.

A `Group` is a stable external identifier that Canvas attaches through a generic relation — the [`content_type`](/sdk/data-content-type/#contenttype) and `object_id` fields, the same pattern [OrganizationalEntity](/sdk/data-organizational-entity/#organizationalentity) uses — to either a `Team` or a `PatientGroup`, the record this reference calls the Group's content object. This identifier is exactly what the FHIR [Group endpoint](/api/group/) exposes as its `id`. A `Team` surfaces as a FHIR Group of type `practitioner`, and a `PatientGroup` surfaces as a FHIR Group of type `person`.

Reach for `Group` when you hold a FHIR Group `id` — the stable external identifier — and need to resolve which SDK record it names, a `Team` or a `PatientGroup`. When you already have a `Team` in hand, its [`group_id`](/sdk/data-team/#reconciling-with-fhir) is the shorter path, because it exposes the FHIR Group id directly.

`Group` exposes the linked record through typed property accessors, and the `Group` record itself is read-only; create or update the underlying FHIR Group through the [FHIR API](/api/group/) rather than an SDK effect.

## Basic usage

To follow a `Group` to the record it points at, retrieve the `Group` by `id` and read whichever typed property is set:

```python
from canvas_sdk.v1.data import Group

group = Group.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

if group.team is not None:
    linked = group.team
elif group.patient_group is not None:
    linked = group.patient_group
else:
    linked = None
```

For a `Group` whose content object is a `Team`, `team` returns the linked [Team](/sdk/data-team/#team) and `patient_group` is `None`. For a `Group` whose content object is a `PatientGroup`, `patient_group` returns the linked [PatientGroup](/sdk/data-patient-group/#patientgroup) and `team` is `None`. When a `Group` is not backed by either type, both properties return `None`, so read whichever property is set rather than assuming one always resolves.

## Attributes

### Group

| Field Name   | Type                                               |
| ------------ | -------------------------------------------------- |
| id           | UUID                                               |
| dbid         | Integer                                            |
| created      | DateTime                                           |
| modified     | DateTime                                           |
| content_type | [ContentType](/sdk/data-content-type/#contenttype) |
| object_id    | Integer                                            |

The `object_id` field holds the target record's `dbid` — its internal integer identifier — rather than its `id` UUID.

## Properties

| Name          | Type                                                            | Description                                                                                          |
| ------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| team          | [Team](/sdk/data-team/#team) \| `None`                          | The `Team` this group points at, or `None` when its content object is not a `Team`.                 |
| patient_group | [PatientGroup](/sdk/data-patient-group/#patientgroup) \| `None` | The `PatientGroup` this group points at, or `None` when its content object is not a `PatientGroup`. |
