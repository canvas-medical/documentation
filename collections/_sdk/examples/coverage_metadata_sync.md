---
title: "Coverage Metadata Sync Plugin"
excerpt: "Example plugin that synchronizes patient metadata based on appointment label changes"
hidden: false
---

# Coverage Metadata Sync Plugin

This example plugin demonstrates how to automatically maintain patient metadata based on appointment label changes. It works in tandem with the `appointment_coverage_label` plugin to provide a complete coverage tracking solution.

## Overview

The coverage metadata sync plugin automatically maintains a patient metadata field that reflects their insurance coverage status based on appointment label changes. It provides:

- **Centralized coverage status**: Maintains a single source of truth for patient coverage status in metadata
- **Easy reporting**: Enables queries and reports based on coverage status metadata
- **Automated synchronization**: No manual metadata updates required
- **Integration-friendly**: Other systems can read the metadata field to understand coverage status
- **Audit trail**: Metadata changes are tracked in Canvas, providing coverage status history

## Features

### Metadata Synchronization

The plugin automatically updates patient metadata when appointment labels change:

- **Sets metadata to "Missing"**: When the "MISSING_COVERAGE" label is added to an appointment
- **Sets metadata to "Active"**: When the "MISSING_COVERAGE" label is removed from an appointment
- **Idempotent updates**: Safe to call multiple times with the same result
- **Single metadata field**: Uses `coverage_status` as the metadata key

### Event-Driven Architecture

The plugin responds to appointment label events:

- **APPOINTMENT_LABEL_ADDED**: Triggered when any label is added to an appointment
- **APPOINTMENT_LABEL_REMOVED**: Triggered when any label is removed from an appointment

### Integration with appointment_coverage_label Plugin

This plugin is designed to work seamlessly with the `appointment_coverage_label` plugin to create a complete workflow:

1. **appointment_coverage_label** manages appointment labels based on coverage
2. **coverage_metadata_sync** listens for label changes and updates patient metadata
3. Together they provide automated coverage tracking with both visual indicators (labels) and queryable data (metadata)

## Events

### APPOINTMENT_LABEL_ADDED

**When it fires**: When any label is added to an appointment

**Plugin response**: 
- Checks if the added label is "MISSING_COVERAGE"
- If yes, updates patient metadata: `coverage_status = "Missing"`
- If no, ignores the event

**Example event context**:
```json
{
  "target": {
    "id": "appointment-uuid",
    "type": null
  },
  "context": {
    "patient": {
      "id": "patient-uuid"
    },
    "label": "MISSING_COVERAGE"
  }
}
```

### APPOINTMENT_LABEL_REMOVED

**When it fires**: When any label is removed from an appointment

**Plugin response**:
- Checks if the removed label is "MISSING_COVERAGE"
- If yes, updates patient metadata: `coverage_status = "Active"`
- If no, ignores the event

**Example event context**:
```json
{
  "target": {
    "id": "appointment-uuid",
    "type": null
  },
  "context": {
    "patient": {
      "id": "patient-uuid"
    },
    "label": "MISSING_COVERAGE"
  }
}
```

## Effects

### PatientMetadata.upsert()

Creates or updates the `coverage_status` metadata field for a patient.

**Usage**:
```python
PatientMetadata(
    patient_id="patient-uuid",
    key="coverage_status"
).upsert("Missing")
```

**Behavior**:
- Creates metadata field if it doesn't exist
- Updates existing metadata field with new value
- Idempotent operation (safe to call multiple times)
- Maintains audit trail of changes

## Implementation Details

### Protocol Class Structure

The plugin uses a single protocol class that handles both label events:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.effects.patient_metadata import PatientMetadata

class CoverageStatusSyncProtocol(BaseProtocol):
    RESPONDS_TO = [
        EventType.Name(EventType.APPOINTMENT_LABEL_ADDED),
        EventType.Name(EventType.APPOINTMENT_LABEL_REMOVED)
    ]
    
    MONITORED_LABEL = "MISSING_COVERAGE"
    METADATA_KEY = "coverage_status"
    
    def compute(self):
        label_name = self.event.context.get("label")
        patient_id = self.event.context.get("patient", {}).get("id")
        
        if not patient_id or label_name != self.MONITORED_LABEL:
            return []
        
        if self.event.name == EventType.Name(EventType.APPOINTMENT_LABEL_ADDED):
            return self._handle_label_added(patient_id)
        elif self.event.name == EventType.Name(EventType.APPOINTMENT_LABEL_REMOVED):
            return self._handle_label_removed(patient_id)
        
        return []
```

### Event Filtering

The plugin only processes events for the "MISSING_COVERAGE" label:

```python
def compute(self):
    label_name = self.event.context.get("label")
    
    # Only process MISSING_COVERAGE label events
    if label_name != self.MONITORED_LABEL:
        logger.info(f"Ignoring event for label '{label_name}' because it is not the monitored label ('{self.MONITORED_LABEL}').")
        return []
    
    # ... rest of implementation
```

### Metadata Key/Value Structure

The plugin uses a standardized metadata structure:

**Key**: `coverage_status`

**Values**:
- `"Missing"` - Patient lacks insurance coverage (MISSING_COVERAGE label present)
- `"Active"` - Patient has insurance coverage (MISSING_COVERAGE label removed)

### Label Added Handler

```python
def _handle_label_added(self, patient_id):
    """Set metadata to 'Missing' when MISSING_COVERAGE label is added."""
    logger.info(f"Reacting to 'APPOINTMENT_LABEL_ADDED'. Updating patient {patient_id} metadata '{self.METADATA_KEY}' to 'Missing'.")
    
    return [
        PatientMetadata(
            patient_id=patient_id,
            key=self.METADATA_KEY
        ).upsert("Missing")
    ]
```

### Label Removed Handler

```python
def _handle_label_removed(self, patient_id):
    """Set metadata to 'Active' when MISSING_COVERAGE label is removed."""
    logger.info(f"Reacting to 'APPOINTMENT_LABEL_REMOVED'. Updating patient {patient_id} metadata '{self.METADATA_KEY}' to 'Active'.")
    
    return [
        PatientMetadata(
            patient_id=patient_id,
            key=self.METADATA_KEY
        ).upsert("Active")
    ]
```

## Code Walkthrough

### Key Components

1. **Event Registration**: The protocol responds to both APPOINTMENT_LABEL_ADDED and APPOINTMENT_LABEL_REMOVED events
2. **Event Filtering**: Only processes events for the "MISSING_COVERAGE" label
3. **Metadata Management**: Updates patient metadata based on label changes
4. **Error Handling**: Gracefully handles missing data and validation errors
5. **Logging**: Provides detailed logging for troubleshooting

### Error Handling

The plugin includes comprehensive error handling:

```python
def compute(self):
    try:
        label_name = self.event.context.get("label")
        patient_id = self.event.context.get("patient", {}).get("id")
        
        if not patient_id:
            logger.warning("No patient ID found in label event")
            return []
        
        if not label_name:
            logger.warning("No label name found in label event")
            return []
        
        # ... rest of implementation
        
    except Exception as e:
        logger.error(f"Error processing label event: {e}", exc_info=True)
        return []
```

### Performance Considerations

- **Event filtering**: Filters events early to ignore non-relevant labels
- **Single metadata operation**: One metadata update per event
- **Idempotent updates**: Safe to call multiple times
- **Minimal database queries**: Only updates metadata when necessary
- **Fast execution path**: Quick return for ignored events

## Integration Pattern

This plugin demonstrates a powerful integration pattern with the `appointment_coverage_label` plugin:

### Complete Workflow Example

**Step 1: Appointment Created (No Coverage)**
- `appointment_coverage_label` detects new appointment for patient without insurance
- Adds "MISSING_COVERAGE" label to appointment

**Step 2: Label Added (This Plugin)**
- `coverage_metadata_sync` detects "MISSING_COVERAGE" label addition
- Updates patient metadata: `coverage_status = "Missing"`

**Step 3: Coverage Added Later**
- Patient's insurance information is entered into Canvas
- COVERAGE_CREATED event is fired

**Step 4: Label Removed**
- `appointment_coverage_label` removes "MISSING_COVERAGE" label from appointment
- `coverage_metadata_sync` detects label removal
- Updates patient metadata: `coverage_status = "Active"`

### Result

- Appointments are labeled appropriately
- Patient metadata accurately reflects current coverage status
- Both data points stay in sync automatically

## Usage

### Installation

1. Install the plugin using Canvas CLI:
   ```bash
   canvas install /path/to/coverage_metadata_sync
   ```

2. Enable the plugin in your Canvas instance

3. Optionally install `appointment_coverage_label` plugin for complete automation

4. The plugin will automatically monitor appointment label events

### Configuration

No configuration is required - the plugin works automatically once installed. The plugin monitors the "MISSING_COVERAGE" label and uses the "coverage_status" metadata key.

### Metadata Access

Once the plugin is running, you can access the coverage status metadata:

#### Via Django ORM

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.patient_metadata import PatientMetadata

# Get patient
patient = Patient.objects.get(id="patient-id")

# Get coverage status metadata
metadata = PatientMetadata.objects.filter(
    patient=patient,
    key="coverage_status"
).first()

if metadata:
    print(f"Coverage status: {metadata.value}")
    # Output: "Coverage status: Missing" or "Coverage status: Active"
```

#### For Reporting

```python
# Find all patients with missing coverage
missing_coverage = PatientMetadata.objects.filter(
    key="coverage_status",
    value="Missing"
).values_list("patient_id", flat=True)

# Find all patients with active coverage
active_coverage = PatientMetadata.objects.filter(
    key="coverage_status",
    value="Active"
).values_list("patient_id", flat=True)
```

## Example Scenarios

### Scenario 1: New Patient Without Insurance

**Initial State**:
- Patient John Doe, no insurance
- Appointment created for 2025-11-15

**Event Flow**:
1. Appointment created → `appointment_coverage_label` adds "MISSING_COVERAGE" label
2. Label added → `coverage_metadata_sync` sets metadata `coverage_status = "Missing"`

**Final State**:
- Appointment has "MISSING_COVERAGE" label
- Patient metadata shows `coverage_status: "Missing"`
- Reports can now identify patients needing coverage

### Scenario 2: Insurance Added

**Initial State**:
- Patient Jane Smith
- Metadata: `coverage_status = "Missing"`
- 3 appointments with "MISSING_COVERAGE" labels

**Event Flow**:
1. Insurance coverage added → COVERAGE_CREATED event fires
2. `appointment_coverage_label` removes labels from all 3 appointments
3. First label removed → `coverage_metadata_sync` sets `coverage_status = "Active"`
4. Subsequent label removals → `coverage_metadata_sync` updates same field (idempotent)

**Final State**:
- All appointments have labels removed
- Patient metadata shows `coverage_status: "Active"`
- Patient record is clean and up-to-date

### Scenario 3: Multiple Patients

**Scenario**:
- 100 patients without insurance
- Each has 1-3 appointments

**Plugin Behavior**:
- Each appointment creation triggers label addition
- Each label addition triggers metadata update
- All 100 patients have `coverage_status = "Missing"` in metadata
- Business intelligence reports can easily identify these patients
- Targeted outreach campaigns can be run based on metadata

## Troubleshooting

### Metadata Not Being Updated

**Possible Causes**:
- Plugin not enabled in Canvas instance
- Label change events not firing
- Different label being used (not "MISSING_COVERAGE")

**Check**:
- Verify plugin is installed and enabled
- Confirm label events are being generated in Canvas
- Review plugin logs for event processing messages
- Ensure label name exactly matches "MISSING_COVERAGE"

### Metadata Shows Wrong Value

**Possible Causes**:
- Label was added/removed outside of normal workflow
- Multiple conflicting label events
- Race condition with multiple appointments

**Check**:
- Review event logs for sequence of label changes
- Verify most recent label event for patient
- Check if patient has multiple appointments with different label states

### Integration Issues

**Problem**: Plugin works but labels aren't being added/removed

**Solution**: This plugin only RESPONDS to label changes. Install the `appointment_coverage_label` plugin to automatically manage labels.

## Source Code

The complete source code for this plugin is available in the Canvas Plugins repository:

- **Location**: `canvas-plugins/example-plugins/coverage_metadata_sync/`
- **Main file**: `protocols/metadata_sync.py`
- **Manifest**: `CANVAS_MANIFEST.json`
- **Documentation**: `README.md`

## Related Documentation

- [Patient Metadata Effects](/sdk/effect-patient-metadata/) - Effect documentation
- [Appointment Label Events](/sdk/events/#appointments) - Event documentation
- [Appointment Label Automation Guide](/guides/appointment-label-automation/) - Complete workflow guide
- [Appointment Coverage Label Example](/sdk/examples/appointment_coverage_label/) - Complementary plugin
