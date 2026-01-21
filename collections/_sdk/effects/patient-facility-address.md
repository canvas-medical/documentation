---
title: "Patient Facility Address"
slug: "effect-patient-facility-address"
excerpt: "Create, update, or delete patient facility address associations"
hidden: false
---

The `PatientFacilityAddress` effect enables the creation, updating, and deletion of patient facility address records within Canvas. Patient facility addresses link patients to healthcare facilities, with optional room number information. The address details are automatically populated from the linked facility.

You can either reference an existing facility by ID, or create a new facility inline by providing the facility details.

## Attributes

| Attribute               | Type                   | Description                                            | Required                       |
|-------------------------|------------------------|--------------------------------------------------------|--------------------------------|
| `id`                    | `str` or `UUID`        | ID of the patient facility address (for update/delete) | Yes (update/delete)            |
| `patient_id`            | `str` or `UUID`        | ID of the patient                                      | Yes (create)                   |
| `facility_id`           | `str` or `UUID`        | ID of an existing facility to link                     | Yes (if not creating new)      |
| `facility_name`         | `str`                  | Name of new facility to create                         | Yes (if creating new facility) |
| `facility_npi_number`   | `str`                  | NPI number for new facility                            | No                             |
| `facility_phone_number` | `str`                  | Phone number for new facility                          | No                             |
| `facility_fax_number`   | `str`                  | Fax number for new facility                            | No                             |
| `facility_active`       | `bool`                 | Whether the new facility is active                     | No                             |
| `facility_line1`        | `str`                  | Street address line 1 for new facility                 | No                             |
| `facility_line2`        | `str`                  | Street address line 2 for new facility                 | No                             |
| `facility_city`         | `str`                  | City for new facility                                  | Yes (if creating new facility) |
| `facility_district`     | `str`                  | District for new facility                              | No                             |
| `facility_state_code`   | `str`                  | State code for new facility (e.g., "CA", "NY")         | Yes (if creating new facility) |
| `facility_postal_code`  | `str`                  | Postal code for new facility                           | Yes (if creating new facility) |
| `room_number`           | `str`                  | Room number at the facility                            | No                             |
| `address_type`          | `AddressType` or `str` | Type of address: "physical" or "both"                  | No (defaults to "physical")    |

## Facility Reference Options

When creating a patient facility address, you must either:

1. **Reference an existing facility** by providing `facility_id`
2. **Create a new facility inline** by providing facility creation fields (`facility_name`, `facility_city`, `facility_state_code`, `facility_postal_code`)

{% include alert.html type="warning" content="You cannot specify both <code>facility_id</code> and facility creation fields. Use one approach or the other." %}

### Required Fields for Inline Facility Creation

When creating a new facility inline, the following fields are required:
- `facility_name`
- `facility_city`
- `facility_state_code`
- `facility_postal_code`

## Address Type

The `address_type` field accepts the following values:

| Value      | Description                       |
|------------|-----------------------------------|
| `physical` | Physical/street address (default) |
| `both`     | Both physical and mailing address |

## Effect Methods

### `.create()`

Creates a new patient facility address. Requires `patient_id` and either `facility_id` or facility creation fields.

**Effect Type:** `CREATE_PATIENT_FACILITY_ADDRESS`

### `.update()`

Updates an existing patient facility address. Requires `id` of the address to update.

**Effect Type:** `UPDATE_PATIENT_FACILITY_ADDRESS`

### `.delete()`

Deletes an existing patient facility address. Requires `id` of the address to delete.

**Effect Type:** `DELETE_PATIENT_FACILITY_ADDRESS`

## Validation

The effect validates:
- **Create**: `patient_id` is required and must reference an existing patient
- **Create**: Either `facility_id` or facility creation fields must be provided (not both)
- **Create**: If `facility_id` is provided, it must reference an existing facility
- **Create**: If creating a new facility, all required facility fields must be provided
- **Update/Delete**: `id` is required and must reference an existing patient facility address
- **Update**: If updating facility, same rules apply as create (facility_id OR creation fields)
- `address_type` must be "physical" or "both" if provided

## Example Usage

### Creating with Existing Facility

```python
from canvas_sdk.effects.patient_facility_address import PatientFacilityAddress, AddressType
from canvas_sdk.handlers.base import BaseHandler


class MyProtocol(BaseHandler):
    def compute(self):
        effect = PatientFacilityAddress(
            patient_id="patient-uuid-here",
            facility_id="facility-uuid-here",
            room_number="101A",
            address_type=AddressType.PHYSICAL,
        )
        return [effect.create()]
```

### Creating with New Facility

```python
from canvas_sdk.effects.patient_facility_address import PatientFacilityAddress, AddressType
from canvas_sdk.handlers.base import BaseHandler


class MyProtocol(BaseHandler):
    def compute(self):
        effect = PatientFacilityAddress(
            patient_id="patient-uuid-here",
            facility_name="Downtown Medical Center",
            facility_line1="123 Main Street",
            facility_line2="Suite 400",
            facility_city="Boston",
            facility_state_code="MA",
            facility_postal_code="02101",
            facility_phone_number="617-555-1234",
            facility_npi_number="1234567890",
            room_number="Room 205",
            address_type=AddressType.PHYSICAL,
        )
        return [effect.create()]
```

### Updating an Existing Address

```python
from canvas_sdk.effects.patient_facility_address import PatientFacilityAddress
from canvas_sdk.handlers.base import BaseHandler


class MyProtocol(BaseHandler):
    def compute(self):
        # Update to use a different existing facility
        effect = PatientFacilityAddress(
            id="existing-address-uuid",
            facility_id="new-facility-uuid",
            room_number="202B",
        )
        return [effect.update()]
```

### Deleting an Address

```python
from canvas_sdk.effects.patient_facility_address import PatientFacilityAddress
from canvas_sdk.handlers.base import BaseHandler


class MyProtocol(BaseHandler):
    def compute(self):
        effect = PatientFacilityAddress(
            id="existing-address-uuid",
        )
        return [effect.delete()]
```

## Notes

- The address details (line1, line2, city, state, country, postal_code) displayed for a patient facility address are automatically populated from the linked facility's address information.
- When creating a new facility inline, the facility is created first, then linked to the patient facility address.
- Room number is optional and can be used to specify the patient's specific room within the facility.
