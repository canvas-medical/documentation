---
title: "Organization"
slug: "data-organization"
excerpt: "Canvas SDK Organization"
hidden: false
---

## Introduction

The `Organization` model represents the overall Organization in a Canvas EMR instance. An `Organization` can have multiple related [Practice Locations](/sdk/data-practicelocation).

## Basic usage

Canvas instances can contain only a single `Organization` entry. To retrieve the `Organization` entry, you can either query by the organization's name:

```python
from canvas_sdk.v1.data.organization import Organization

organization = Organization.objects.get(full_name="Medical Organization")
```

Or since there will only be one `Organization` in an instance, it can also be fetched by using the `first` method:

```python
from canvas_sdk.v1.data.organization import Organization

organization = Organization.objects.first()
```

## Attributes

### Organization

| Field Name            | Type                                                |
| --------------------- | --------------------------------------------------- |
| dbid                  | Integer                                             |
| created               | DateTime                                            |
| modified              | DateTime                                            |
| full_name             | String                                              |
| short_name            | String                                              |
| subdomain             | String                                              |
| logo_url              | String                                              |
| background_image_url  | String                                              |
| background_gradient   | String                                              |
| active                | Boolean                                             |
| tax_id                | String                                              |
| tax_id_type           | [TaxIDType](/sdk/data-enumeration-types/#taxidtype) |
| group_npi_number      | String                                              |
| group_taxonomy_number | String                                              |
| include_zz_qualifier  | Boolean                                             |
| main_location         | [PracticeLocation](/sdk/data-practicelocation/#practicelocation)            |
| practice_locations    | QuerySet[[PracticeLocation](/sdk/data-practicelocation/#practicelocation)]  |
| addresses             | QuerySet[[OrganizationAddress](#organizationaddress)]                       |
| telecom               | QuerySet[[OrganizationContactPoint](#organizationcontactpoint)]             |
| business_lines        | QuerySet[[BusinessLine](/sdk/data-business-line/#businessline)]             |
| settings              | QuerySet[[OrganizationSetting](#organizationsetting)]                       |

## OrganizationAddress

The `OrganizationAddress` model represents a physical or mailing address associated with an Organization. Multiple addresses can be linked to a single Organization, each with its own type and details.

### Attributes

| Field Name           | Type                                                                        |
| -------------------- | --------------------------------------------------------------------------- |
| id                   | UUID                                                                        |
| dbid                 | Integer                                                                     |
| created              | DateTime                                                                    |
| modified             | DateTime                                                                    |
| organization         | [Organization](#organization)                                               |
| use                  | [AddressUseWithBilling](/sdk/data-enumeration-types/#addressusewithbilling) |
| type                 | [AddressType](/sdk/data-enumeration-types/#addresstype)                     |
| longitude            | Float                                                                       |
| latitude             | Float                                                                       |
| start                | Date                                                                        |
| end                  | Date                                                                        |
| country              | String                                                                      |
| state                | [AddressState](/sdk/data-enumeration-types/#addressstate)                   |
| address_search_index | String                                                                      |
| line1                | String                                                                      |
| line2                | String                                                                      |
| city                 | String                                                                      |
| district             | String                                                                      |
| state_code           | String                                                                      |
| postal_code          | String                                                                      |

## OrganizationContactPoint

The `OrganizationContactPoint` model represents a contact method (such as phone, email, or fax) for an Organization. Multiple contact points can be associated with a single Organization, each with its own type, use, and status.

### Attributes

| Field Name   | Type                                                                  |
| ------------ | --------------------------------------------------------------------- |
| id           | UUID                                                                  |
| dbid         | Integer                                                               |
| created      | DateTime                                                              |
| modified     | DateTime                                                              |
| organization | [Organization](#organization)                                         |
| system       | [ContactPointSystem](/sdk/data-enumeration-types/#contactpointsystem) |
| value        | String                                                                |
| use          | [ContactPointUse](/sdk/data-enumeration-types/#contactpointuse)       |
| use_notes    | String                                                                |
| rank         | Integer                                                               |
| state        | [ContactPointState](/sdk/data-enumeration-types/#contactpointstate)   |

## OrganizationSetting

The `OrganizationSetting` model holds the organization's appointment reminder configuration and the staff roles Canvas treats as schedulable or as prescribers. Each setting has a `name` and a JSON `value`:

| Name                               | Value                                                                                                                                              |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `appointmentReminders`             | The reminder schedule, as `{"daysAhead": int, "hourOfDay": int}`. Canvas sends reminders for appointments from tomorrow through `daysAhead` days ahead, starting at `hourOfDay` in the instance's time zone. |
| `appointmentReminderCustomization` | The text Canvas adds to reminder messages. It can contain `{{...}}` template variables, which Canvas fills in when it sends the reminder.          |
| `SCHEDULABLE_STAFF_ROLES`          | The role codes that make a staff member schedulable, as a list such as `["MD", "DO", "NP", "PA"]`. A staff member is schedulable when any of their [roles](/sdk/data-staff/#staffrole) has an `internal_code` in the list. |
| `PRESCRIBER_STAFF_ROLES`           | The role codes Canvas treats as prescriber roles, as a list such as `["MD", "DO", "NP", "PA"]`. See [Finding staff who can e-prescribe](/sdk/data-staff/#finding-staff-who-can-e-prescribe). |

When an instance has no `SCHEDULABLE_STAFF_ROLES` or `PRESCRIBER_STAFF_ROLES` setting, Canvas uses `MD`, `DO`, `NP`, and `PA`.

The reminder schedule always comes from the organization. A [business line](/sdk/data-business-line/#businesslinesetting) can replace the organization's `appointmentReminderCustomization` for its own patients.

```python
from canvas_sdk.v1.data.organization import Organization

organization = Organization.objects.first()
schedule = organization.settings.filter(name="appointmentReminders").first()

if schedule:
    days_ahead = schedule.value.get("daysAhead")
    hour_of_day = schedule.value.get("hourOfDay")
```

### Attributes

| Field Name   | Type                          |
| ------------ | ----------------------------- |
| dbid         | Integer                       |
| created      | DateTime                      |
| modified     | DateTime                      |
| organization | [Organization](#organization) |
| name         | String                        |
| value        | JSON                          |

<br/>
<br/>
<br/>
