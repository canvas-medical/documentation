---
title: "OrganizationalEntity"
slug: "data-organizational-entity"
excerpt: "Canvas SDK OrganizationalEntity"
hidden: false
---

## Introduction

The `OrganizationalEntity` model represents an external entity that Canvas references through a generic relation — for example, the [ServiceProvider](/sdk/data-serviceprovider/#service-provider) backing a patient's external care team member. Its `type` indicates which kind of entity it points at, and the `content_type` and `object_id` fields identify the specific record.

The most common use is reaching the external members of a patient's care team. A [CareTeamMembership](/sdk/data-care-team/#careteammembership) with no `staff` is an external member, and its `organizational_entity` links to the `OrganizationalEntity` describing the external provider.

## Basic usage

When an `OrganizationalEntity` has a `type` of `Service Provider`, its `service_provider` property resolves to the linked [ServiceProvider](/sdk/data-serviceprovider/#service-provider), giving you access to the provider's contact details — such as `business_fax` — without leaving the plugin:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="a74592ae8a6c4d0ebe0799d3fb3713d1")
external_member = patient.care_team_memberships.filter(staff__isnull=True).first()

entity = external_member.organizational_entity
if entity and entity.service_provider:
    print(entity.service_provider.business_fax)
```

For entities of any other `type`, the `service_provider` property returns `None`.

## Attributes

### OrganizationalEntity

| Field Name   | Type                                                                  |
| ------------ | --------------------------------------------------------------------- |
| id           | UUID                                                                  |
| dbid         | Integer                                                               |
| content_type | [ContentType](/sdk/data-content-type/#contenttype)                    |
| object_id    | Integer                                                               |
| name         | String                                                                |
| active       | Boolean                                                               |
| type         | [OrganizationalEntityType](#organizationalentitytype)                 |

## Properties

| Name             | Type                                                                       | Description                                                                                       |
| ---------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| service_provider | [ServiceProvider](/sdk/data-serviceprovider/#service-provider) \| `None`   | The linked `ServiceProvider` when `type` is `Service Provider`; otherwise `None`.                 |

## Enumeration types

### OrganizationalEntityType

| Value            | Label            |
| ---------------- | ---------------- |
| Transactor       | Transactor       |
| Business Entity  | Business Entity  |
| Vendor           | Vendor           |
| Service Provider | Service Provider |
