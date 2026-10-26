---
title: "Instance Configuration Effects"
slug: "effect-instance-configuration"
excerpt: "Create, update, and delete practice locations, teams, note types, insurers, billing and vaccine catalogs, and other instance settings from a plugin"
hidden: false
---

The instance configuration effects let a plugin set up and maintain the configuration of a Canvas instance: practice locations and their settings, teams, care team roles, note types, consent and reason-for-visit codings, insurers, the billing catalog, and the vaccine catalog. Use them to load a new instance's configuration from code, or to keep an instance in sync with a system of record.

Each effect class is a model of one kind of configuration record. Build it with the [attributes](#attributes-by-record-type) you want to set, then return one of its methods from your handler.

## How the effects work

Most classes have three methods:

| Method | What it does | Required attributes |
|---|---|---|
| `create()` | Creates a record. | The attributes the record's table marks as required for `create()`. Don't set `id`. |
| `update()` | Changes the record with the given `id`. Only the attributes you set on the effect are changed, so an update never clears a field you didn't mention. | `id` |
| `delete()` | Deletes the record with the given `id`. Some record types handle delete differently; see each section. | `id` |

`TeamMember` uses `assign()` and `remove()`, and `PracticeLocationSetting` uses `upsert()`.

`id` is the record's `id` in the SDK data model where it has one, and its `dbid` otherwise. Each section below says which.

Effects run independently. If one effect in the list your handler returns fails, the others still apply. A failed effect isn't reported back to your handler: Canvas logs the error for your plugin, so check your plugin's logs when a change doesn't appear.

```python
from canvas_sdk.effects.practice_location import PracticeLocation
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class LocationLoader(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PLUGIN_CREATED)]

    def compute(self):
        return [
            PracticeLocation(
                full_name="Main Street Clinic",
                short_name="Main",
                place_of_service_code="11",
                npi_number="1234567890",
            ).create(),
        ]
```

Every create, update, and delete also emits a lifecycle event, whether a plugin or a person in Canvas made the change. See [Instance configuration events](#instance-configuration-events).

## Practice locations

### PracticeLocation

Import from `canvas_sdk.effects.practice_location`. `id` is the practice location's `id` in the [PracticeLocation](/sdk/data-practicelocation/#practicelocation) data model.

- `create()` adds the location to the instance's organization and gives it the default per-location settings.
- `delete()` deletes the location with its addresses and settings. A location that notes, appointments, or staff refer to can't be deleted. To stop using a location, update it with `active=False` instead.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `full_name` | `str` | Full name of the location | For `create()` |
| `short_name` | `str` | Short name shown where space is limited | For `create()` |
| `place_of_service_code` | `str` | Two-digit place of service code, such as `"11"` (office) | No |
| `active` | `bool` | Whether the location is in use | No |
| `npi_number` | `str` | Location NPI, up to 10 characters | No |
| `bill_through_organization` | `bool` | Bill under the organization rather than the location | No |
| `tax_id` | `str` | Tax ID | No |
| `tax_id_type` | `TaxIdType` | `TaxIdType.EIN` or `TaxIdType.SSN` | No |
| `billing_location_name` | `str` | Name to use on claims | No |
| `group_npi_number` | `str` | Group NPI, up to 10 characters | No |
| `taxonomy_number` | `str` | Taxonomy code | No |
| `include_zz_qualifier` | `bool` | Include the ZZ qualifier with the taxonomy code on claims | No |
| `background_image_url` | `str` | Background image URL | No |
| `background_gradient` | `str` | Background gradient | No |
| `header_color` | `str` | Header color as a hex code, such as `"#1A73E8"` | No |

### PracticeLocationAddress

Import from `canvas_sdk.effects.practice_location`. `id` is the address's `id`, and `practice_location_id` is the practice location's `id`.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `practice_location_id` | `str` or `UUID` | The location the address belongs to | For `create()` |
| `line1` | `str` | First address line | For `create()` |
| `line2` | `str` | Second address line | No |
| `city` | `str` | City | For `create()` |
| `district` | `str` | District or county | No |
| `state_code` | `str` | Two-letter state code | For `create()` |
| `postal_code` | `str` | Postal code | For `create()` |
| `country` | `str` | Country | For `create()` |
| `use` | `PracticeLocationAddressUse` | `HOME`, `WORK`, `TEMP`, `OLD`, or `BILLING`. Defaults to `HOME`, so set `WORK` for a clinic's street address | No |
| `type` | `PracticeLocationAddressType` | `POSTAL`, `PHYSICAL`, or `BOTH` (the default) | No |

### PracticeLocationSetting

Import from `canvas_sdk.effects.practice_location`. `upsert()` sets one setting on a practice location, creating it if the location doesn't have it yet.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `practice_location_id` | `str` or `UUID` | The practice location's `id` | Yes |
| `name` | `PracticeLocationSettingName` | The setting to set | Yes |
| `value` | any JSON value | The new value | No |

Canvas stores `value` as you send it, so send the format each setting expects:

| `name` | `value` |
|---|---|
| `PREFERRED_LAB_PARTNER` | Name of the lab partner that lab orders default to, such as `"Generic Lab"` |
| `PRINTED_PRESCRIPTION_FORMAT` | Printed prescription layout, such as `"quarter_sheet_portrait_top_center"`. An empty string uses the standard layout |
| `SCANNER_INTEGRATION` | `"enabled"` to turn on document scanning. Any other value leaves it off |
| `SERVICE_AREA_ZIP_CODES` | List of ZIP codes, such as `["94612", "94607"]`, used in the referral, imaging order, and DME provider searches |

```python
from canvas_sdk.effects.practice_location import (
    PracticeLocationSetting,
    PracticeLocationSettingName,
)

effect = PracticeLocationSetting(
    practice_location_id="9f2c6f6e-8a39-4a61-8d5e-3f1d8a0d2b10",
    name=PracticeLocationSettingName.SERVICE_AREA_ZIP_CODES,
    value=["94612", "94607"],
).upsert()
```

## Teams and care team roles

### Team

Import from `canvas_sdk.effects.team`. `id` is the team's `id` in the [Team](/sdk/data-team/#team) data model.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `name` | `str` | Team name, up to 200 characters. Must be unique | For `create()` |
| `responsibilities` | `list[TeamResponsibility]` | Work the team handles, such as `TeamResponsibility.PROCESS_REFILL_REQUESTS`. See [TeamResponsibility](/sdk/data-team/#teamresponsibility) | No |

### TeamMember

Import from `canvas_sdk.effects.team`. `assign()` adds a staff member to a team, and `remove()` takes them off it. Both are safe to repeat.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `team_id` | `str` or `UUID` | The team's `id` | Yes |
| `staff_id` | `str` | The staff member's `id` in the [Staff](/sdk/data-staff/#staff) data model | Yes |

```python
from canvas_sdk.effects.team import Team, TeamMember, TeamResponsibility

create_team = Team(
    name="Refills",
    responsibilities=[TeamResponsibility.PROCESS_REFILL_REQUESTS],
).create()

add_member = TeamMember(
    team_id="0c3e5a1e-6d0b-4d55-9a37-0a8f2e3b7c41",
    staff_id="4150cd20de8a470aa570a852859ac87e",
).assign()
```

### CareTeamRole

Import from `canvas_sdk.effects.team`. `id` is the role's `dbid` in the [CareTeamRole](/sdk/data-care-team/#careteamrole) data model.

- `delete()` deletes the role and every patient care team membership that uses it. To stop offering a role and keep the memberships, update it with `active=False` instead.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `system` | `str` | Code system, such as `"http://snomed.info/sct"` | For `create()` |
| `display` | `str` | Name shown for the role | For `create()` |
| `code` | `str` | Code within the system | No |
| `version` | `str` | Code system version | No |
| `user_selected` | `bool` | Whether the code was chosen by a user | No |
| `active` | `bool` | Whether the role is offered. Defaults to `False`, so set `active=True` on create | No |

## Note types

Import `NoteType` and `NoteTypeCategory` from `canvas_sdk.effects.note_type`. `id` is the note type's `unique_identifier` in the [NoteType](/sdk/data-note/#notetype) data model.

You can create and change note types in the encounter and schedule event categories.

- `update()` changes the note type in place.
- `delete()` deprecates the note type rather than removing it, so existing notes keep their type. A deprecated note type can't be updated or deleted again. To hide a note type you might use again, update it with `is_active=False` instead.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `name` | `str` | Note type name. Must be unique among active note types | For `create()` |
| `display` | `str` | Name shown in Canvas | For `create()` |
| `code` | `str` | Code. The `code` and `system` pair must be unique among active note types | For `create()` |
| `system` | `str` | Code system | For `create()` |
| `category` | `NoteTypeCategory` | `ENCOUNTER` or `SCHEDULE_EVENT` | For `create()` |
| `icon` | `str` | Icon name | For `create()` |
| `version` | `str` | Code system version | No |
| `rank` | `int` | Sort order | No |
| `is_active` | `bool` | Whether the note type can be used | No |
| `is_visible` | `bool` | Whether the note type is shown | No |
| `is_scheduleable` | `bool` | Whether appointments can use the note type | No |
| `is_default_appointment_type` | `bool` | Use as the default appointment type | No |
| `is_scheduleable_via_patient_portal` | `bool` | Whether patients can book it in the portal | No |
| `online_duration` | `int` | Appointment length in minutes when booked online | No |
| `is_telehealth` | `bool` | Whether visits are telehealth | No |
| `is_billable` | `bool` | Whether visits are billable. Defaults to `True` | No |
| `is_sig_required` | `bool` | Whether the note needs a signature | No |
| `is_patient_required` | `bool` | Whether the note needs a patient | No |
| `allow_custom_title` | `bool` | Whether users can retitle the note | No |
| `defer_place_of_service_to_practice_location` | `bool` | Use the practice location's place of service | No |
| `default_place_of_service` | `str` | Default place of service code | No |
| `available_places_of_service` | `list[str]` | Place of service codes the note can use | No |

A billable note type needs a place of service: set `available_places_of_service` or `defer_place_of_service_to_practice_location=True`, or set `is_billable=False`.

```python
from canvas_sdk.effects.note_type import NoteType, NoteTypeCategory

effect = NoteType(
    name="Nutrition visit",
    display="Nutrition visit",
    code="NUTR",
    system="INTERNAL",
    category=NoteTypeCategory.ENCOUNTER,
    icon="apple",
    is_scheduleable=True,
    available_places_of_service=["11"],
).create()
```

## Consent and reason-for-visit codings

Import from `canvas_sdk.effects.codings`. These classes share the coding attributes:

| Attribute | Type | Description | Required |
|---|---|---|---|
| `system` | `str` | Code system | For `create()` |
| `display` | `str` | Name shown in Canvas | For `create()` |
| `code` | `str` | Code within the system | No |
| `version` | `str` | Code system version | No |
| `user_selected` | `bool` | Whether the code is offered for selection | No |

### PatientConsentCoding

A type of consent patients can give. `id` is the coding's `dbid` in the [PatientConsentCoding](/sdk/data-patient-consent/#patientconsentcoding) data model. A consent type that patients' consents use can't be deleted.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `expiration_rule` | `ConsentExpirationRule` | `NEVER`, `IN_ONE_YEAR`, or `END_OF_YEAR` | For `create()` |
| `is_mandatory` | `bool` | Whether every patient must have this consent | No |
| `is_proof_required` | `bool` | Whether a signed document is required | No |
| `show_in_patient_portal` | `bool` | Whether patients see it in the portal | No |
| `summary` | `str` | Summary shown with the consent | No |

### PatientConsentRejectionCoding

A reason a patient declines a consent. `id` is the coding's `dbid` in the [PatientConsentRejectionCoding](/sdk/data-patient-consent/#patientconsentrejectioncoding) data model. A reason that patients' consents use can't be deleted. It has only the shared coding attributes.

### ReasonForVisitSettingCoding

A structured reason-for-visit option. `id` is the coding's `id`. It has only the shared coding attributes. Set `user_selected=True` for the option to appear in the Reason for Visit and Follow Up commands.

## Insurers

Import `Insurer` and `InsurerType` from `canvas_sdk.effects.insurer`. `id` is the insurer's `id` in the [Transactor](/sdk/data-coverage/#transactor) data model.

- `delete()` deletes the insurer along with the patient coverages it issued and the lab orders and eligibility requests that use those coverages. An insurer that claims or posting rules refer to can't be deleted. To stop using an insurer and keep its patients' coverages, update it with `active=False` instead.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `name` | `str` | Insurer name | For `create()` |
| `payer_id` | `str` | Clearinghouse payer ID. Must be unique; required when `clearinghouse_payer` is `True` | No |
| `transactor_type` | `InsurerType` | Kind of payer, such as `InsurerType.COMMERCIAL` or `InsurerType.MEDICARE` | No |
| `type` | `str` | Payer type | No |
| `description` | `str` | Description | No |
| `state` | `str` | State | No |
| `active` | `bool` | Whether the insurer can be used | No |
| `clearinghouse_payer` | `bool` | Whether claims go through the clearinghouse | No |
| `institutional`, `professional`, `era`, `eligibility` | `bool` | Which transactions the payer supports | No |
| `institutional_enrollment_req`, `professional_enrollment_req`, `era_enrollment_req`, `eligibility_enrollment_req` | `bool` | Whether each transaction needs enrollment | No |
| `workers_comp` | `bool` | Workers' compensation payer | No |
| `secondary_support` | `bool` | Supports secondary claims | No |
| `claim_fee`, `remit_fee` | `bool` | Whether the clearinghouse charges claim or remittance fees | No |
| `use_provider_for_eligibility` | `bool` | Send the provider on eligibility requests | No |
| `coverage_types` | `list[str]` | Coverage types the insurer offers, as [TransactorCoverageType](/sdk/data-coverage/#transactorcoveragetype) values | No |

```python
from canvas_sdk.effects.insurer import Insurer, InsurerType

effect = Insurer(
    name="Acme Health Plan",
    payer_id="ACME1",
    transactor_type=InsurerType.COMMERCIAL,
    clearinghouse_payer=True,
    professional=True,
    eligibility=True,
    active=True,
).create()
```

## Billing catalog

Import from `canvas_sdk.effects.billing_catalog`. Send amounts as strings, such as `"150.00"`, to keep their decimal precision.

### FeeSchedule

A billable code and its default charge. `id` is the entry's `dbid` in the [ChargeDescriptionMaster](/sdk/data-charge-description-master/) data model.

- `delete()` deletes the entry and its payor charges, and removes the entry from billing line items that use it. To retire a code and keep that history, update it with an `end_date` instead.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `cpt_code` | `str` | Code, up to 10 characters | For `create()` |
| `name` | `str` | Name | For `create()` |
| `short_name` | `str` | Short name | For `create()` |
| `charge_amount` | `str` | Default charge | No |
| `eff_date` | `date` | First day the entry applies. Defaults to today | No |
| `end_date` | `date` | Last day the entry applies | No |
| `code_system` | `FeeScheduleCodeSystem` | `CPT` (the default) or `INTERNAL` | No |
| `ndc_code` | `str` | NDC code | No |
| `ndc_dosage` | `str` | NDC dosage | No |
| `ndc_measure` | `str` | NDC unit of measure | No |

### PayorCharge

An insurer-specific charge for a fee schedule entry. `id` is the charge's `dbid` in the [PayorSpecificCharge](/sdk/data-payor-specific-charge/) data model.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `insurer_id` | `str` or `UUID` | The insurer's `id` | For `create()` |
| `fee_schedule_id` | `int` | The fee schedule entry's `dbid` | For `create()` |
| `charge_amount` | `str` | Charge for this insurer | For `create()` |
| `eff_date` | `date` | First day the charge applies | No |
| `end_date` | `date` | Last day the charge applies | No |
| `part_of_capitated_set` | `bool` | Whether the charge is part of a capitated set | No |

### Discount

A percentage adjustment with its adjustment codes. `id` is the discount's `dbid`.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `name` | `str` | Name | For `create()` |
| `adjustment_group` | `str` | Claim adjustment group code: `CO`, `OA`, `PI`, `PR`, `WO`, `CW`, `CR`, or `TR` | For `create()` |
| `adjustment_code` | `str` | Claim adjustment reason code | For `create()` |
| `discount` | `str` | Percentage, such as `"10.00"` | No |

### PostingRule

An ERA posting rule. `id` is the rule's `dbid` in the [PostingRule](/sdk/data-posting-rule/) data model.

- A blank `adjustment_code` matches every code in the group, and an empty `insurer_id` applies the rule to every insurer.
- `delete()` deletes rules your instance added. Canvas's preset rules, marked `is_preset` in the data model, stay in place.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `description` | `str` | Description | For `create()` |
| `adjustment_group` | `str` | Claim adjustment group code, such as `CO` | For `create()` |
| `behavior` | `PostingRuleBehavior` | `WRITE_OFF`, `NON_WRITE_OFF`, or `TRANSFER` (to the next payer) | For `create()` |
| `adjustment_code` | `str` | Claim adjustment reason code | No |
| `payer_order` | `PostingRulePayerOrder` | `PRIMARY` or `SUPPLEMENTARY` | No |
| `insurer_id` | `str` or `UUID` | The insurer's `id` | No |
| `automated_action_review` | `bool` | Whether automated actions need review | No |

```python
from canvas_sdk.effects.billing_catalog import (
    FeeSchedule,
    PostingRule,
    PostingRuleBehavior,
)

fee = FeeSchedule(
    cpt_code="99213",
    name="Office visit, established patient, low complexity",
    short_name="Est. low",
    charge_amount="150.00",
).create()

rule = PostingRule(
    description="Write off contractual obligation",
    adjustment_group="CO",
    adjustment_code="45",
    behavior=PostingRuleBehavior.WRITE_OFF,
).create()
```

## Vaccine catalog

Import from `canvas_sdk.effects.vaccine_catalog`.

### Vaccine

`id` is the vaccine's `id` in the [Vaccine](/sdk/data-vaccine/#vaccine) data model. Deleting a vaccine keeps its lots.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `cvx_code` | `str` | CVX code | For `create()` |
| `name` | `str` | Name | For `create()` |
| `short_name` | `str` | Short name | For `create()` |
| `inventory` | `str` | Inventory description | No |
| `ndc_code` | `str` | NDC code | No |
| `mvx_code` | `str` | Manufacturer MVX code | No |
| `route` | `str` | Route of administration | No |
| `units` | `int` | Units per dose. Defaults to 1 | No |
| `active` | `bool` | Whether the vaccine can be used | No |
| `insurer_id` | `str` or `UUID` | The `id` of the insurer billed for the vaccine | No |

### VaccineLot

`id` is the lot's `id` in the [VaccineLot](/sdk/data-vaccine/#vaccinelot) data model. Canvas computes on-hand inventory as `starting_inventory` plus `quantity_adjustment` minus the doses given.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `vaccine_id` | `str` or `UUID` | The vaccine's `id` | For `create()` |
| `lot_number` | `str` | Lot number. Must be unique | For `create()` |
| `expiration_date` | `date` | Lot expiration date | For `create()` |
| `starting_inventory` | `int` | Doses received, zero or more | For `create()` |
| `ndc_code` | `str` | NDC code | No |
| `mvx_code` | `str` | Manufacturer MVX code | No |
| `diluent_lot_number` | `str` | Diluent lot number | No |
| `diluent_expiration_date` | `date` | Diluent expiration date | No |
| `quantity_adjustment` | `int` | Doses added or removed by hand | No |
| `adjustment_notes` | `str` | Reason for the adjustment | No |

## Instance configuration events

Canvas emits a `_CREATED`, `_UPDATED`, and `_DELETED` event for each record type on this page, such as `INSURER_CREATED`, whenever the record changes, whether a plugin or a person made the change. Practice location settings emit `PRACTICE_LOCATION_SETTING_UPDATED`. Practice location addresses and team membership changes emit no events. See [Instance configuration](/sdk/events/#instance-configuration) on the Events page for the full list and what each event's target holds.

## Related data models

Read instance configuration with these data models:

- [PracticeLocation](/sdk/data-practicelocation/), [Team](/sdk/data-team/), [CareTeamRole](/sdk/data-care-team/#careteamrole), and [NoteType](/sdk/data-note/#notetype)
- [PatientConsentCoding](/sdk/data-patient-consent/#patientconsentcoding) and [Transactor](/sdk/data-coverage/#transactor)
- [ChargeDescriptionMaster](/sdk/data-charge-description-master/), [PayorSpecificCharge](/sdk/data-payor-specific-charge/), and [PostingRule](/sdk/data-posting-rule/)
- [Vaccine and VaccineLot](/sdk/data-vaccine/)
- [Role](/sdk/data-role/), [ScheduleDuration](/sdk/data-schedule-duration/), and [LetterTemplate](/sdk/data-letter-template/)
