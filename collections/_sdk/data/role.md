---
title: "Role"
slug: "data-role"
excerpt: "Canvas SDK Role"
hidden: false
---

## Introduction

The `Role` model represents a staff role definition, such as Physician, Nurse, or Front Desk, that can be assigned to [Staff](/sdk/data-staff/). Use it to look up the roles an instance defines, for example to find the provider roles before you build a scheduling or staffing workflow.

## Basic usage

```python
from canvas_sdk.v1.data import Role

physician = Role.objects.get(internal_code="MD")
print(physician.name, physician.role_type)
```

## Filtering

**List the roles in the clinical domain**

```python
from canvas_sdk.v1.data import Role
from canvas_sdk.v1.data.staff import StaffRole

clinical_roles = Role.objects.filter(domain=StaffRole.RoleDomain.CLINICAL)
```

**List the provider roles**

```python
from canvas_sdk.v1.data import Role
from canvas_sdk.v1.data.role import RoleType

provider_roles = Role.objects.filter(role_type=RoleType.PROVIDER)
```

## Attributes

### Role

| Field Name             | Type                                                    |
| ---------------------- | ------------------------------------------------------- |
| dbid                   | Integer                                                 |
| created                | DateTime                                                |
| modified               | DateTime                                                |
| internal_code          | String                                                  |
| public_abbreviation    | String                                                  |
| domain                 | [RoleDomain](/sdk/data-staff/#role-domain)              |
| name                   | String                                                  |
| domain_privilege_level | Integer                                                 |
| role_type              | [RoleType](#roletype)                                   |

## Enumeration types

### RoleType

| Value        | Label        |
| ------------ | ------------ |
| NON-LICENSED | Non-Licensed |
| LICENSED     | Licensed     |
| PROVIDER     | Provider     |
