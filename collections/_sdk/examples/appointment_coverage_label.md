---
title: "Appointment Coverage Label Plugin"
excerpt: "Example plugin that automatically manages appointment labels based on patient insurance coverage"
hidden: false
---

# Appointment Coverage Label Plugin

This example plugin demonstrates how to automatically manage appointment labels based on patient insurance coverage status. It automatically adds "MISSING_COVERAGE" labels to appointments for patients without insurance and removes them when coverage is added.

## Overview

The appointment coverage label plugin provides automated insurance verification workflows by:

- **Monitoring appointment creation**: Adds "MISSING_COVERAGE" labels when appointments are created for patients without insurance
- **Tracking coverage changes**: Removes "MISSING_COVERAGE" labels when insurance coverage is added to a patient
- **Handling multiple appointments**: Updates all appointments for a patient when their coverage status changes
- **Providing visual indicators**: Staff can immediately see which appointments need insurance verification

## Features

### Automatic Label Management

The plugin automatically manages "MISSING_COVERAGE" labels based on patient coverage status:

- **Adds labels**: When appointments are created for patients without insurance
- **Removes labels**: When insurance coverage is added for a patient
- **Handles multiple appointments**: Updates all appointments for a patient consistently
- **Bidirectional sync**: Responds to both appointment creation and coverage changes

### Event-Driven Architecture

The plugin responds to two key Canvas events:

- **APPOINTMENT_CREATED**: Triggered when new appointments are scheduled
- **COVERAGE_CREATED**: Triggered when insurance coverage is added for a patient

### Integration Ready

This plugin is designed to work seamlessly with other plugins, particularly the `coverage_metadata_sync` plugin, to provide a complete coverage tracking solution.

## Events

### APPOINTMENT_CREATED

**When it fires**: When a new appointment is scheduled for a patient

**Plugin response**: 
- Checks if the patient has insurance coverage
- If no coverage exists, adds "MISSING_COVERAGE" label to all of the patient's appointments
- If coverage exists, no action is taken

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
    }
  }
}
```

### COVERAGE_CREATED

**When it fires**: When insurance coverage is added for a patient

**Plugin response**:
- Finds all appointments for the patient that have "MISSING_COVERAGE" labels
- Removes the "MISSING_COVERAGE" label from all matching appointments

**Example event context**:
```json
{
  "target": {
    "id": "coverage-uuid",
    "type": null
  },
  "context": {
    "patient": {
      "id": "patient-uuid"
    }
  }
}
```

## Effects

### AddAppointmentLabel

Adds "MISSING_COVERAGE" labels to appointments for patients without insurance.

**Usage**:
```python
AddAppointmentLabel(
    appointment_id="appointment-uuid",
    labels={"MISSING_COVERAGE"}
).apply()
```

**Validation**:
- Ensures appointment exists
- Respects the 3-label limit per appointment
- Automatically sorts labels for consistency

### RemoveAppointmentLabel

Removes "MISSING_COVERAGE" labels from appointments when coverage is added.

**Usage**:
```python
RemoveAppointmentLabel(
    appointment_id="appointment-uuid",
    labels={"MISSING_COVERAGE"}
).apply()
```

**Behavior**:
- Removes specified labels from appointment
- Ignores non-existent labels (no error thrown)
- Maintains label sorting consistency

## Implementation Details

### Protocol Class Structure

The plugin uses a single protocol class that handles both events:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.effects.note.appointment import AddAppointmentLabel, RemoveAppointmentLabel
from canvas_sdk.v1.data.coverage import Coverage
from canvas_sdk.v1.data.appointment import Appointment

class AppointmentLabelsProtocol(BaseProtocol):
    RESPONDS_TO = [
        EventType.Name(EventType.APPOINTMENT_CREATED),
        EventType.Name(EventType.COVERAGE_CREATED)
    ]
    
    def compute(self):
        if self.event.name == EventType.Name(EventType.APPOINTMENT_CREATED):
            return self._handle_appointment_created()
        elif self.event.name == EventType.Name(EventType.COVERAGE_CREATED):
            return self._handle_coverage_created()
        return []
```

### Event Handling Logic

#### Appointment Created Handler

```python
def _handle_appointment_created(self):
    """Add MISSING_COVERAGE label if patient has no coverage."""
    patient_id = self.event.context.get("patient", {}).get("id")
    
    if not patient_id:
        return []
    
    # Check if patient has coverage
    has_coverage = Coverage.objects.filter(patient__id=patient_id).exists()
    
    if not has_coverage:
        # Add label to all appointments for this patient
        appointments = Appointment.objects.filter(patient__id=patient_id)
        effects = []
        
        for appointment in appointments:
            # Only add label if it doesn't already exist
            if "MISSING_COVERAGE" not in appointment.labels:
                effects.append(
                    AddAppointmentLabel(
                        appointment_id=str(appointment.id),
                        labels={"MISSING_COVERAGE"}
                    ).apply()
                )
        
        return effects
    
    return []
```

#### Coverage Created Handler

```python
def _handle_coverage_created(self):
    """Remove MISSING_COVERAGE labels when coverage is added."""
    patient_id = self.event.context.get("patient", {}).get("id")
    
    if not patient_id:
        return []
    
    # Find all appointments with MISSING_COVERAGE label
    appointments = Appointment.objects.filter(
        patient__id=patient_id,
        labels__contains=["MISSING_COVERAGE"]
    )
    
    effects = []
    for appointment in appointments:
        effects.append(
            RemoveAppointmentLabel(
                appointment_id=str(appointment.id),
                labels={"MISSING_COVERAGE"}
            ).apply()
        )
    
    return effects
```

### Coverage Checking

The plugin uses efficient database queries to check patient coverage:

```python
# Check if patient has any active coverage
has_coverage = Coverage.objects.filter(patient__id=patient_id).exists()

# More specific check for active coverage
has_active_coverage = Coverage.objects.filter(
    patient__id=patient_id,
    status="active"
).exists()
```

### Label Management

The plugin includes logic to prevent duplicate labels and handle edge cases:

```python
# Only add label if it doesn't already exist
if "MISSING_COVERAGE" not in appointment.labels:
    effects.append(
        AddAppointmentLabel(
            appointment_id=str(appointment.id),
            labels={"MISSING_COVERAGE"}
        ).apply()
    )
```

## Code Walkthrough

### Key Components

1. **Event Registration**: The protocol responds to both APPOINTMENT_CREATED and COVERAGE_CREATED events
2. **Event Routing**: The `compute()` method routes events to appropriate handlers
3. **Coverage Validation**: Checks patient coverage status using database queries
4. **Label Management**: Adds/removes labels based on coverage status
5. **Error Handling**: Gracefully handles missing data and validation errors

### Error Handling

The plugin includes comprehensive error handling:

```python
def _handle_appointment_created(self):
    try:
        patient_id = self.event.context.get("patient", {}).get("id")
        
        if not patient_id:
            logger.warning("No patient ID found in appointment created event")
            return []
        
        # ... rest of implementation
        
    except Exception as e:
        logger.error(f"Error handling appointment created: {e}", exc_info=True)
        return []
```

### Performance Considerations

- **Efficient queries**: Uses `exists()` for coverage checks
- **Batch processing**: Processes multiple appointments in a single operation
- **Label filtering**: Only processes appointments that need label changes
- **Database optimization**: Uses proper indexing for patient and appointment queries

## Usage

### Installation

1. Install the plugin using Canvas CLI:
   ```bash
   canvas install /path/to/appointment_coverage_label
   ```

2. Enable the plugin in your Canvas instance

3. The plugin will automatically start monitoring appointment and coverage events

### Configuration

No configuration is required - the plugin works automatically once installed. The plugin uses the standard "MISSING_COVERAGE" label name.

### Integration with Other Plugins

This plugin works best when paired with the `coverage_metadata_sync` plugin:

1. **appointment_coverage_label** manages appointment labels
2. **coverage_metadata_sync** listens for label changes and updates patient metadata
3. Together they provide a complete coverage tracking solution

## Example Scenarios

### Scenario 1: New Patient Without Insurance

**Initial State**:
- Patient John Doe has no insurance coverage
- Appointment scheduled for 2025-11-15

**Plugin Action**:
- Detects appointment creation
- Checks coverage → None found
- Adds "MISSING_COVERAGE" label to appointment

**Result**:
- Appointment now flagged for insurance verification
- Staff can proactively contact patient before appointment

### Scenario 2: Insurance Added Later

**Initial State**:
- Patient Jane Smith has 3 appointments with "MISSING_COVERAGE" labels
- Coverage was just added to her account

**Plugin Action**:
- Detects coverage creation
- Queries all Jane's appointments with "MISSING_COVERAGE" label
- Removes label from all 3 appointments

**Result**:
- Appointments no longer flagged
- Clean patient record reflects current coverage status

### Scenario 3: Multiple Appointments

**Initial State**:
- Patient has no coverage
- First appointment created on 2025-11-01

**Plugin Action (First Appointment)**:
- Adds "MISSING_COVERAGE" label to first appointment

**Later**:
- Second appointment created on 2025-11-10 for same patient

**Plugin Action (Second Appointment)**:
- Detects no coverage still
- Adds "MISSING_COVERAGE" label to BOTH appointments

**Result**:
- All appointments consistently flagged until coverage is added

## Troubleshooting

### Labels Not Being Added

**Possible Causes**:
- Plugin not enabled in Canvas instance
- Patient already has coverage
- Appointment already has "MISSING_COVERAGE" label

**Check**:
- Verify plugin is installed and enabled
- Confirm patient has no Coverage records
- Review plugin logs for error messages

### Labels Not Being Removed

**Possible Causes**:
- Coverage not properly saved to database
- Coverage record doesn't match patient
- Plugin event handler not triggered

**Check**:
- Verify `Coverage.objects.filter(patient=patient).exists()` returns True
- Check that coverage is associated with correct patient
- Review Canvas event logs for COVERAGE_CREATED events

## Source Code

The complete source code for this plugin is available in the Canvas Plugins repository:

- **Location**: `canvas-plugins/example-plugins/appointment_coverage_label/`
- **Main file**: `protocols/appointment_labels.py`
- **Manifest**: `CANVAS_MANIFEST.json`
- **Documentation**: `README.md`

## Related Documentation

- [Appointment Label Effects](/sdk/effect-appointment-labels/) - Effect documentation
- [Appointment Events](/sdk/events/#appointments) - Event documentation
- [Appointment Label Automation Guide](/guides/appointment-label-automation/) - Complete workflow guide
- [Coverage Metadata Sync Example](/sdk/examples/coverage_metadata_sync/) - Complementary plugin
