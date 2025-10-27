---
title: "Appointment Label Automation"
guide_for:
- /sdk/effects/appointment-labels/
- /sdk/events/
- /sdk/examples/appointment_coverage_label/
- /sdk/examples/coverage_metadata_sync/
---

# Appointment Label Automation Guide

This guide demonstrates how to automate appointment labels in Canvas using the Canvas SDK. Appointment labels provide visual indicators and enable automated workflows for appointment categorization, insurance verification, and staff notifications.

## What You'll Learn

- How appointment labels work in Canvas
- Using `AddAppointmentLabel` and `RemoveAppointmentLabel` effects
- Responding to `APPOINTMENT_LABEL_ADDED` and `APPOINTMENT_LABEL_REMOVED` events
- Building complete automation workflows
- Best practices for label management

## Overview: Appointment Labels in Canvas

Appointment labels are visual indicators that help categorize and track appointments beyond their basic scheduling information. Canvas supports up to 3 labels per appointment, and these can be managed both manually through the UI and programmatically through plugins.

### Key Features

- **Visual indicators**: Labels appear as colored badges on appointments
- **Categorization**: Organize appointments by type, priority, or status
- **Automation**: Labels can be added/removed automatically based on business logic
- **Integration**: Labels trigger events that other plugins can respond to
- **Reporting**: Labels can be used for analytics and reporting

For more information on using labels in the Canvas UI, see [Appointment Labels](https://help.canvasmedical.com/articles/9726289513-fs-appointment-labels).

## Core Concepts

### Label Constraints

- **Maximum labels**: 3 labels per appointment (enforced by validation)
- **Label format**: Labels are strings, automatically sorted for consistency
- **Uniqueness**: Labels are stored as a set, preventing duplicates
- **Case sensitivity**: Label names are case-sensitive

### Label Lifecycle

1. **Creation**: Labels are added to appointments using `AddAppointmentLabel`
2. **Modification**: Labels can be removed using `RemoveAppointmentLabel`
3. **Events**: Label changes trigger `APPOINTMENT_LABEL_ADDED` and `APPOINTMENT_LABEL_REMOVED` events
4. **Automation**: Other plugins can respond to these events to create workflows

### Event-Driven Automation

The appointment label system is designed around events:

- **APPOINTMENT_LABEL_ADDED**: Fired when labels are added to an appointment
- **APPOINTMENT_LABEL_REMOVED**: Fired when labels are removed from an appointment

These events enable plugins to create automated workflows that respond to label changes.

## Effects Reference

### AddAppointmentLabel Effect

The `AddAppointmentLabel` effect adds one or more labels to an existing appointment.

#### Basic Usage

```python
from canvas_sdk.effects.note.appointment import AddAppointmentLabel
from canvas_sdk.handlers.base import BaseHandler

class MyProtocol(BaseHandler):
    def compute(self):
        # Add labels to an appointment
        effect = AddAppointmentLabel(
            appointment_id="appointment-uuid",
            labels={"URGENT", "FOLLOW_UP"}
        )
        
        return [effect.apply()]
```

#### Error Handling

```python
def add_labels_safely(self, appointment_id, labels):
    try:
        effect = AddAppointmentLabel(
            appointment_id=appointment_id,
            labels=labels
        )
        return [effect.apply()]
    except ValidationError as e:
        # Handle validation errors (e.g., appointment doesn't exist, too many labels)
        logger.warning(f"Failed to add labels: {e}")
        return []
```

### RemoveAppointmentLabel Effect

The `RemoveAppointmentLabel` effect removes one or more labels from an existing appointment.

#### Basic Usage

```python
from canvas_sdk.effects.note.appointment import RemoveAppointmentLabel
from canvas_sdk.handlers.base import BaseHandler

class MyProtocol(BaseHandler):
    def compute(self):
        # Remove labels from an appointment
        effect = RemoveAppointmentLabel(
            appointment_id="appointment-uuid",
            labels={"CANCELLED", "RESCHEDULED"}
        )
        
        return [effect.apply()]
```

## Events Reference

### APPOINTMENT_LABEL_ADDED Event

This event is fired when one or more labels are added to an appointment.

#### Event Structure

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

#### Responding to the Event

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

class LabelAddedProtocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.APPOINTMENT_LABEL_ADDED)
    
    def compute(self):
        label_name = self.event.context.get("label")
        patient_id = self.event.context.get("patient", {}).get("id")
        
        if label_name == "MISSING_COVERAGE":
            # Update patient metadata when coverage label is added
            return [
                PatientMetadata(
                    patient_id=patient_id,
                    key="coverage_status"
                ).upsert("Missing")
            ]
        
        return []
```

### APPOINTMENT_LABEL_REMOVED Event

This event is fired when one or more labels are removed from an appointment.

#### Event Structure

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

#### Responding to the Event

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

class LabelRemovedProtocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.APPOINTMENT_LABEL_REMOVED)
    
    def compute(self):
        label_name = self.event.context.get("label")
        patient_id = self.event.context.get("patient", {}).get("id")
        
        if label_name == "MISSING_COVERAGE":
            # Update patient metadata when coverage label is removed
            return [
                PatientMetadata(
                    patient_id=patient_id,
                    key="coverage_status"
                ).upsert("Active")
            ]
        
        return []
```

## Complete Example Workflow

Let's walk through a complete example using the two provided example plugins that work together to create an automated insurance coverage tracking system.

### Workflow Overview

1. **appointment_coverage_label**: Monitors patient coverage and manages appointment labels
2. **coverage_metadata_sync**: Listens to label changes and updates patient metadata
3. Together they provide automated coverage tracking with both visual indicators (labels) and queryable data (metadata)

### Step 1: Appointment Coverage Label Plugin

This plugin automatically manages "MISSING_COVERAGE" labels based on patient insurance status.

#### Key Features

- **Automatic label management**: Adds/removes labels based on coverage
- **Handles multiple appointments**: Updates all appointments for a patient
- **Bidirectional sync**: Responds to both appointment creation and coverage changes

#### Implementation Highlights

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.effects.note.appointment import AddAppointmentLabel, RemoveAppointmentLabel
from canvas_sdk.v1.data.coverage import Coverage

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

### Step 2: Coverage Metadata Sync Plugin

This plugin synchronizes patient metadata based on appointment label changes.

#### Key Features

- **Metadata synchronization**: Updates patient metadata when labels change
- **Integration**: Works seamlessly with appointment_coverage_label
- **Idempotent updates**: Safe to call multiple times

#### Implementation Highlights

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
            # Set metadata to "Missing" when label is added
            return [
                PatientMetadata(
                    patient_id=patient_id,
                    key=self.METADATA_KEY
                ).upsert("Missing")
            ]
        
        elif self.event.name == EventType.Name(EventType.APPOINTMENT_LABEL_REMOVED):
            # Set metadata to "Active" when label is removed
            return [
                PatientMetadata(
                    patient_id=patient_id,
                    key=self.METADATA_KEY
                ).upsert("Active")
            ]
        
        return []
```

### Step 3: Integration Pattern

The two plugins work together to create a complete automation workflow:

1. **Appointment Created (No Coverage)**:
   - `appointment_coverage_label` detects new appointment for patient without insurance
   - Adds "MISSING_COVERAGE" label to appointment
   - `coverage_metadata_sync` detects label addition
   - Updates patient metadata: `coverage_status = "Missing"`

2. **Coverage Added Later**:
   - Patient's insurance information is entered into Canvas
   - COVERAGE_CREATED event is fired
   - `appointment_coverage_label` removes "MISSING_COVERAGE" label from appointment
   - `coverage_metadata_sync` detects label removal
   - Updates patient metadata: `coverage_status = "Active"`

## Code Examples

### Insurance Verification Workflow

```python
from canvas_sdk.effects.note.appointment import AddAppointmentLabel
from canvas_sdk.handlers.base import BaseHandler

class InsuranceVerificationProtocol(BaseHandler):
    def compute(self):
        patient_id = self.event.context.get("patient", {}).get("id")
        
        if not self._patient_has_coverage(patient_id):
            return [
                AddAppointmentLabel(
                    appointment_id=self.event.context["appointment"]["id"],
                    labels={"MISSING_COVERAGE"}
                ).apply()
            ]
        return []
    
    def _patient_has_coverage(self, patient_id):
        from canvas_sdk.v1.data.coverage import Coverage
        return Coverage.objects.filter(patient__id=patient_id).exists()
```

### Appointment Status Tracking

```python
from canvas_sdk.effects.note.appointment import AddAppointmentLabel, RemoveAppointmentLabel
from canvas_sdk.handlers.base import BaseHandler

class StatusTrackingProtocol(BaseHandler):
    def compute(self):
        appointment_id = self.event.context["appointment"]["id"]
        effects = []
        
        # Add urgent label for high-priority appointments
        if self._is_urgent_appointment():
            effects.append(
                AddAppointmentLabel(
                    appointment_id=appointment_id,
                    labels={"URGENT"}
                ).apply()
            )
        
        # Remove cancelled label if appointment is rescheduled
        if self._is_rescheduled():
            effects.append(
                RemoveAppointmentLabel(
                    appointment_id=appointment_id,
                    labels={"CANCELLED"}
                ).apply()
            )
            effects.append(
                AddAppointmentLabel(
                    appointment_id=appointment_id,
                    labels={"RESCHEDULED"}
                ).apply()
            )
        
        return effects
```

### Multi-Label Management

```python
def replace_all_labels(self, appointment_id, new_labels):
    """Replace all existing labels with new ones."""
    # First remove all common labels
    remove_effect = RemoveAppointmentLabel(
        appointment_id=appointment_id,
        labels={"URGENT", "FOLLOW_UP", "CANCELLED", "RESCHEDULED", "MISSING_COVERAGE"}
    )
    
    # Then add new labels
    add_effect = AddAppointmentLabel(
        appointment_id=appointment_id,
        labels=new_labels
    )
    
    return [remove_effect.apply(), add_effect.apply()]
```

## Best Practices

### Error Handling

Always handle validation errors gracefully:

```python
def add_labels_safely(self, appointment_id, labels):
    try:
        effect = AddAppointmentLabel(
            appointment_id=appointment_id,
            labels=labels
        )
        return [effect.apply()]
    except ValidationError as e:
        logger.warning(f"Failed to add labels to appointment {appointment_id}: {e}")
        return []
```

### Label Naming Conventions

Use consistent, descriptive label names:

```python
# Good: Clear, descriptive labels
LABELS = {
    "MISSING_COVERAGE": "Patient lacks insurance coverage",
    "URGENT": "High priority appointment",
    "FOLLOW_UP": "Follow-up appointment required",
    "CANCELLED": "Appointment was cancelled",
    "RESCHEDULED": "Appointment was rescheduled"
}

# Avoid: Vague or inconsistent labels
BAD_LABELS = {"X", "123", "temp", "urgent"}  # Case inconsistency
```

### Performance Considerations

- **Batch operations**: When possible, add/remove multiple labels in a single effect
- **Check limits**: Always be aware of the 3-label limit
- **Efficient queries**: Use proper database queries to check existing labels

```python
def efficient_label_check(self, appointment_id):
    """Efficiently check existing labels without loading full appointment."""
    from canvas_sdk.v1.data.appointment import Appointment
    
    appointment = Appointment.objects.filter(id=appointment_id).only('labels').first()
    if not appointment:
        return set()
    
    return set(appointment.labels)
```

### Testing

Test your label automation thoroughly:

```python
def test_label_automation(self):
    """Test that labels are added/removed correctly."""
    # Test adding labels
    effect = AddAppointmentLabel(
        appointment_id="test-appointment-id",
        labels={"TEST_LABEL"}
    )
    
    result = effect.apply()
    assert result is not None
    
    # Test removing labels
    effect = RemoveAppointmentLabel(
        appointment_id="test-appointment-id",
        labels={"TEST_LABEL"}
    )
    
    result = effect.apply()
    assert result is not None
```

## Common Use Cases

### 1. Insurance Verification Workflow

Automatically label appointments for patients without insurance coverage to ensure staff can proactively address coverage issues.

### 2. Appointment Categorization

Categorize appointments by type (urgent, follow-up, routine) to help staff prioritize their work.

### 3. Staff Notifications

Use labels to trigger notifications or alerts for specific appointment types.

### 4. Reporting and Analytics

Use labels to generate reports on appointment types, coverage status, or other business metrics.

### 5. Workflow Automation

Create automated workflows that respond to label changes, such as updating patient metadata or sending notifications.

## Related Documentation

- [Appointment Label Effects](/sdk/effect-appointment-labels/) - Detailed effect documentation
- [Appointment Events](/sdk/events/#appointments) - Event documentation
- [Appointment Coverage Label Example](/sdk/examples/appointment_coverage_label/) - Complete example plugin
- [Coverage Metadata Sync Example](/sdk/examples/coverage_metadata_sync/) - Metadata synchronization example
- [Canvas Help: Appointment Labels](https://help.canvasmedical.com/articles/9726289513-fs-appointment-labels) - UI documentation
