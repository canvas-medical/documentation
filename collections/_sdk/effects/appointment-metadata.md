---
title: "AppointmentMetadata"
slug: "effect-appointment-metadata"
excerpt: "Effects for appointment metadata management"
hidden: false
---

# AppointmentMetadata Effect

The `AppointmentMetadata` effect provides a flexible key-value storage system for appointment-specific data within the Canvas
system.
This effect enables the creation and updating of custom metadata entries associated with appointment records. This allows for
extensible appointment information storage beyond standard scheduling fields.

## Overview

Appointment metadata serves as a powerful extension mechanism for storing custom appointment-related information that doesn't
fit within the standard appointment data model.

## Attributes

| Attribute        | Type  | Description                                                             | Required |
|------------------|-------|-------------------------------------------------------------------------|----------|
| `appointment_id` | `str` | Id of the appointment record to associate metadata with                 | Yes      |
| `key`            | `str` | Unique identifier for the metadata entry within the appointment context | Yes      |

## Methods

### upsert(value: str) → Effect

Creates or updates a metadata entry for the specified appointment and key combination.

#### Parameters

| Parameter | Type  | Description                 | Required |
|-----------|-------|-----------------------------|----------|
| `value`   | `str` | The metadata value to store | Yes      |

#### Returns

An `Effect` object configured for upserting appointment metadata.

#### Behavior

- If a metadata entry with the specified key already exists for the appointment, it will be updated with the new value
- If no entry exists, a new metadata entry will be created
- The operation is idempotent - repeated calls with the same key and value will not create duplicate entries

## Implementation Details

### Validation

The effect performs comprehensive validation before execution:

1. **Appointment Existence Validation**: Verifies that the referenced appointment exists in the system

- Queries the appointment database to confirm the `appointment_id` corresponds to an existing appointment record
- Returns a descriptive error if the appointment is not found

2. **Field Validation**: Ensures all required fields are provided and properly formatted

- Both `appointment_id` and `key` must be non-empty strings
- The `value` parameter in the `upsert` method must be provided

### Data Structure

The effect payload is structured as JSON with the following schema:

```json
{
  "data": {
    "appointment_id": "appointment-id",
    "key": "metadata-key",
    "value": "metadata-value"
  }
}
```

## Example Usage

### Basic Usage

```python
from canvas_sdk.effects.appointments_metadata.base import AppointmentsMetadata

# Create a metadata entry for appointment state
metadata = AppointmentsMetadata(
    appointment_id="550e8400e29b41d4a716446655440001",
    key="state"
)

# Upsert the metadata value
effect = metadata.upsert("CA")
```

## Best Practices

### Key Naming Conventions

1. **Use Descriptive Names**: Choose keys that clearly indicate the purpose of the metadata

- Good: `external_mrn`, `preferred_pharmacy_id`, `risk_score_diabetes`
- Avoid: `data1`, `temp`, `misc`

2. **Namespace Your Keys**: When building integrations or modules, prefix keys to avoid collisions

- Example: `integration_patient_id`, `module_diabetes_last_a1c_date`

### Value Storage

1. **String Serialization**: All values are stored as strings. For complex data types:

   ```python
   import json
   from canvas_sdk.effects.appointments_metadata.base import AppointmentsMetadata
   
   metadata = AppointmentsMetadata(
       appointment_id="550e8400e29b41d4a716446655440001",
       key="result"
   )
   complex_data = {"scores": [85, 92, 78], "average": 85.0}
   metadata.upsert(json.dumps(complex_data))
   ```

2. **Boolean Values**: Store as "true" or "false" strings for consistency

   ```python
   from canvas_sdk.effects.appointments_metadata.base import AppointmentsMetadata

   consented = True

   metadata = AppointmentsMetadata(
       appointment_id="550e8400e29b41d4a716446655440001",
       key="boolean_value"
   )
   metadata.upsert("true" if consented else "false")
   ```

## Notes

- Metadata entries are appointment-specific and isolated - the same key can have different values for different appointments
- There is no built-in versioning; updating a key overwrites the previous value
- The system does not enforce any schema on metadata values - validation is the responsibility of the implementing code
