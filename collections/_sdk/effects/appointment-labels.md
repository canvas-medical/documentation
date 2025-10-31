---
title: "Appointment Labels"
slug: "effect-appointment-labels"
excerpt: "Effects for managing appointment labels"
hidden: false
---

# Appointment Label Effects

The appointment label effects provide programmatic management of labels in Canvas. Labels serve as visual indicators and categorization tools, enabling automated workflows and improved organization for appointments.

## Overview

Labels are a powerful way to categorize and track appointments. Canvas supports up to 3 labels per appointment, and these effects allow plugins to automatically manage labels based on business logic.

## AddAppointmentLabel Effect

The `AddAppointmentLabel` effect adds one or more labels to an existing appointment.

### Attributes

| Attribute        | Type      | Description                                                             | Required |
|------------------|-----------|-------------------------------------------------------------------------|----------|
| `appointment_id` | `str`     | ID of the appointment to add labels to                                  | Yes      |
| `labels`         | `set[str]`| Set of label names to add (1-3 labels total per appointment)            | Yes      |

### apply() → Effect

Adds the specified labels to the appointment.

#### Returns

An `Effect` object configured for adding appointment labels.

#### Behavior

- Labels are added to the appointment if the total count doesn't exceed 3
- Labels are automatically sorted for consistency
- Duplicate labels are ignored (labels are stored as a set)
- Validates the appointment exists before adding labels
- Validates label names are non-empty strings
- Returns an error if adding labels would exceed the 3-label limit

#### Example Usage

```python?partial=true
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

```python?partial=true
from canvas_sdk.effects.note.appointment import AddAppointmentLabel
from canvas_sdk.exceptions import ValidationError

def handle_validation_errors():
    # Example of handling validation errors
    try:
        effect = AddAppointmentLabel(
            appointment_id="invalid-id",
            labels={"LABEL1", "LABEL2", "LABEL3", "LABEL4"}  # Would exceed limit
        )
        return [effect.apply()]
    except ValidationError as e:
        # Handle validation errors
        return []
```

---

## RemoveAppointmentLabel Effect

The `RemoveAppointmentLabel` effect removes one or more labels from an existing appointment.

### Attributes

| Attribute        | Type      | Description                                                             | Required |
|------------------|-----------|-------------------------------------------------------------------------|----------|
| `appointment_id` | `str`     | ID of the appointment to remove labels from                             | Yes      |
| `labels`         | `set[str]`| Set of label names to remove                                            | Yes      |

### apply() → Effect

Removes the specified labels from the appointment.

#### Returns

An `Effect` object configured for removing appointment labels.

#### Behavior

- Removes the specified labels from the appointment
- Non-existent labels are ignored (no error thrown)
- Validates the appointment exists before removing labels

#### Example Usage

```python?partial=true
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

---

## Implementation Details

### Label Constraints

- **Maximum labels**: 3 labels per appointment (enforced by validation)
- **Label format**: Labels are strings, automatically sorted for consistency
- **Uniqueness**: Labels are stored as a set, preventing duplicates
- **Case sensitivity**: Label names are case-sensitive

### Validation Messages

The effects provide clear error messages for common issues:

- `"Appointment {appointment_id} does not exist"` - When appointment ID is invalid
- `"Limit reached: Only 3 appointment labels allowed. Attempted to add {count} label(s) to appointment with {existing} existing label(s)."` - When label limit would be exceeded

## Common Use Cases

### Insurance Verification Workflow

```python?partial=true
from canvas_sdk.effects.note.appointment import AddAppointmentLabel

# Automatically label appointments for patients without coverage
def handle_appointment_created(self):
    if not self._patient_has_coverage():
        return [
            AddAppointmentLabel(
                appointment_id=self.event.context["appointment"]["id"],
                labels={"MISSING_COVERAGE"}
            ).apply()
        ]
    return []
```

### Appointment Status Tracking

```python?partial=true
from canvas_sdk.effects.note.appointment import AddAppointmentLabel, RemoveAppointmentLabel

# Update labels based on appointment status changes
def handle_status_change(self):
    effects = []
    
    if self._is_urgent():
        effects.append(
            AddAppointmentLabel(
                appointment_id=self.appointment_id,
                labels={"URGENT"}
            ).apply()
        )
    
    if self._is_cancelled():
        effects.append(
            RemoveAppointmentLabel(
                appointment_id=self.appointment_id,
                labels={"SCHEDULED"}
            ).apply()
        )
        effects.append(
            AddAppointmentLabel(
                appointment_id=self.appointment_id,
                labels={"CANCELLED"}
            ).apply()
        )
    
    return effects
```

### Multi-Label Management

```python?partial=true
from canvas_sdk.effects.note.appointment import AddAppointmentLabel, RemoveAppointmentLabel

# Replace all labels with new ones
def replace_labels(self, appointment_id, new_labels):
    # First remove existing labels
    remove_effect = RemoveAppointmentLabel(
        appointment_id=appointment_id,
        labels={"URGENT", "CANCELLED", "FOLLOW_UP"}  # Remove common labels
    )

    # Then add new labels
    add_effect = AddAppointmentLabel(
        appointment_id=appointment_id,
        labels=new_labels
    )

    return [remove_effect.apply(), add_effect.apply()]
```

## Best Practices

1. **Handle validation errors**: The effects automatically validate appointment existence and label limits, so catch `ValidationError` exceptions to handle edge cases gracefully
2. **Use meaningful labels**: Choose descriptive label names that clearly indicate their purpose
3. **Batch operations**: When possible, add/remove multiple labels in a single effect
4. **Consistent naming**: Use consistent label naming conventions across your organization (e.g., all caps, underscores for spaces)

## Integration with Events

These effects work seamlessly with appointment label events:

- `APPOINTMENT_LABEL_ADDED` - Fired when labels are added
- `APPOINTMENT_LABEL_REMOVED` - Fired when labels are removed

For more information on these events, see [Appointment Events](/sdk/events/#appointments).

## Related Documentation

- [Appointment Events](/sdk/events/#appointments) - Event documentation
- [Appointment Coverage Label Example](/sdk/examples/appointment_coverage_label/) - Real-world example plugin
