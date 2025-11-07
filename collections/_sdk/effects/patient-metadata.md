---
title: "PatientMetadata Effect"
slug: "effect-patient-metadata"
excerpt: "Effects for patient metadata management"
hidden: false
---

The `PatientMetadata` effect provides a flexible key-value storage system for patient-specific data within the Canvas
system.
This effect enables the creation and updating of custom metadata entries associated with patient records, allowing for
extensible patient information storage beyond standard demographic fields.

## Overview

Patient metadata serves as a powerful extension mechanism for storing custom patient-related information that doesn't
fit within the standard patient data model.

## Attributes

| Attribute    | Type  | Description                                                         | Required |
|--------------|-------|---------------------------------------------------------------------|----------|
| `patient_id` | `str` | Id of the patient record to associate metadata with                 | Yes      |
| `key`        | `str` | Unique identifier for the metadata entry within the patient context | Yes      |

## Methods

### upsert(value: str) → Effect

Creates or updates a metadata entry for the specified patient and key combination.

#### Parameters

| Parameter | Type  | Description                 | Required |
|-----------|-------|-----------------------------|----------|
| `value`   | `str` | The metadata value to store | Yes      |

#### Returns

An `Effect` object configured for upserting patient metadata.

#### Behavior

- If a metadata entry with the specified key already exists for the patient, it will be updated with the new value
- If no entry exists, a new metadata entry will be created
- The operation is idempotent - repeated calls with the same key and value will not create duplicate entries

## Implementation Details

### Validation

The effect performs comprehensive validation before execution:

1. **Patient Existence Validation**: Verifies that the referenced patient exists in the system

- Queries the patient database to confirm the `patient_id` corresponds to an existing patient record
- Returns a descriptive error if the patient is not found

2. **Field Validation**: Ensures all required fields are provided and properly formatted

- Both `patient_id` and `key` must be non-empty strings
- The `value` parameter in the `upsert` method must be provided

### Data Structure

The effect payload is structured as JSON with the following schema:

```json
{
  "data": {
    "patient_id": "patient-id",
    "key": "metadata-key",
    "value": "metadata-value"
  }
}
```

## Example Usage

### Basic Usage

```python
from canvas_sdk.effects.patient_metadata import PatientMetadata

# Create a metadata entry for patient preferences
metadata = PatientMetadata(
    patient_id="550e8400e29b41d4a716446655440000",
    key="preferred_contact_time"
)

# Upsert the metadata value
effect = metadata.upsert("morning")
```

### Metadata Parsing Example

```python
import json
import re
from canvas_sdk.effects.patient_metadata import PatientMetadata
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.events import EventType


class NarrativeMetadataExtractor(BaseHandler):
  """
  Extracts structured metadata from clinical narratives.
  """

  RESPONDS_TO = EventType.Name(EventType.PLAN_COMMAND__POST_UPDATE)

  def compute(self):
    patient_id = self.context["patient"]["id"]
    narrative = self.context.get("fields", {}).get("narrative", "")

    # Extract key-value pairs from narrative text
    # Pattern: key=somekey*value=somevalue
    key_match = re.search(r'key=([^*#_\s]+)', narrative)
    value_match = re.search(r'value=([^*#_\s]+)', narrative)

    if not (key_match and value_match):
      return []

    key = key_match.group(1)
    value = value_match.group(1)

    # Create metadata effect
    metadata = PatientMetadata(
      patient_id=patient_id,
      key=key
    )

    return [metadata.upsert(value)]
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
   # Storing JSON data
   import json
   from canvas_sdk.effects.patient_metadata import PatientMetadata

   metadata = PatientMetadata(
       patient_id="550e8400e29b41d4a716446655440000",
       key="result"
   )
   complex_data = {"scores": [85, 92, 78], "average": 85.0}
   metadata.upsert(json.dumps(complex_data))
   ```

2. **Boolean Values**: Store as "true" or "false" strings for consistency
   ```python
   from canvas_sdk.effects.patient_metadata import PatientMetadata

   patient_consented = False
   metadata = PatientMetadata(
       patient_id="550e8400e29b41d4a716446655440000",
       key="boolean_value"
   )
   metadata.upsert("true" if patient_consented else "false")
   ```

## Notes

- Metadata entries are patient-specific and isolated - the same key can have different values for different patients
- There is no built-in versioning; updating a key overwrites the previous value
- The system does not enforce any schema on metadata values - validation is the responsibility of the implementing code
