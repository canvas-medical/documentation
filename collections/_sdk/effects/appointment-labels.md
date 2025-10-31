---
title: "Appointment and Task Labels"
slug: "effect-appointment-labels"
excerpt: "Effects for managing appointment and task labels"
hidden: false
---

# Appointment and Task Label Effects

The appointment and task label effects provide programmatic management of labels in Canvas. Labels serve as visual indicators and categorization tools, enabling automated workflows and improved organization across appointments and tasks.

## Overview

Labels are a powerful way to categorize and track items beyond their basic information. Canvas supports up to 3 labels per appointment, and these effects allow plugins to automatically manage labels based on business logic.

### Unified Label System

Canvas provides a unified label system that supports context scoping. Labels can be:

- **Appointment-specific**, **task-specific**, or **claim-specific**
- **Shared across multiple contexts** (e.g., appointments and tasks)
- **Global** (available everywhere)

Labels are automatically filtered to show only where they are applicable, enabling organizations to create labels that are either shared across the system or specific to particular workflows.

## AddAppointmentLabel Effect

The `AddAppointmentLabel` effect adds one or more labels to an existing appointment.

### Attributes

| Attribute        | Type      | Description                                                             | Required |
|------------------|-----------|-------------------------------------------------------------------------|----------|
| `appointment_id` | `str`     | ID of the appointment to add labels to                                  | Yes      |
| `labels`         | `set[str]`| Set of label names to add (1-3 labels total per appointment)            | Yes      |

### Methods

### apply() → Effect

Adds the specified labels to the appointment.

#### Returns

An `Effect` object configured for adding appointment labels.

#### Behavior

- Labels are added to the appointment if the total count doesn't exceed 3
- Labels are automatically sorted for consistency
- Duplicate labels are ignored (labels are stored as a set)
- If the appointment doesn't exist, an error is returned
- If adding labels would exceed the 3-label limit, an error is returned

#### Validation

The effect performs comprehensive validation:

- **Appointment existence**: Verifies the appointment exists
- **Label limit**: Ensures the total number of labels doesn't exceed 3
- **Label format**: Validates label names are non-empty strings

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

### Methods

### apply() → Effect

Removes the specified labels from the appointment.

#### Returns

An `Effect` object configured for removing appointment labels.

#### Behavior

- Labels are removed from the appointment
- Non-existent labels are ignored (no error thrown)
- Labels are automatically sorted for consistency
- If the appointment doesn't exist, an error is returned

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
- **Context filtering**: Labels are automatically filtered based on the current context (appointments, tasks, claims)

### Validation Messages

The effects provide clear error messages for common issues:

- `"Appointment {appointment_id} does not exist"` - When appointment ID is invalid
- `"Limit reached: Only 3 appointment labels allowed. Attempted to add {count} label(s) to appointment with {existing} existing label(s)."` - When label limit would be exceeded

### Performance Considerations

- Effects validate appointment existence before processing
- Label operations are atomic
- Sorting is performed efficiently using Python's built-in sort
- Database queries are optimized with proper indexing

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
    # First remove all existing labels
    remove_effect = RemoveAppointmentLabel(
        appointment_id=appointment_id,
        labels={"LABEL1", "LABEL2", "LABEL3"}  # Remove common labels
    )
    
    # Then add new labels
    add_effect = AddAppointmentLabel(
        appointment_id=appointment_id,
        labels=new_labels
    )
    
    return [remove_effect.apply(), add_effect.apply()]
```

## Label Availability by Context

### How Availability Works

Labels are automatically filtered based on the current context:

- **In appointment contexts**: Labels configured for appointments and global labels are available
- **In task contexts**: Labels configured for tasks and global labels are available
- **In claims contexts**: Labels configured for claims and global labels are available

### Defining Label Scope

When labels are created programmatically, you can define where they should be available (appointments, tasks, claims, multiple, or global).

## Best Practices

1. **Check appointment existence**: Always verify the appointment exists before adding labels
2. **Handle label limits**: Be aware of the 3-label limit and handle validation errors gracefully
3. **Use meaningful labels**: Choose descriptive label names that clearly indicate their purpose
4. **Batch operations**: When possible, add/remove multiple labels in a single effect
5. **Error handling**: Always handle validation errors to prevent workflow interruption
6. **Consistent naming**: Use consistent label naming conventions across your organization
7. **Choose appropriate scope**: Decide whether labels should be module-specific or global based on your workflow needs
8. **Consider cross-module usage**: Use global labels or multi-module labels when the same categorization applies across different contexts

## Integration with Events

These effects work seamlessly with appointment label events:

- `APPOINTMENT_LABEL_ADDED` - Fired when labels are added
- `APPOINTMENT_LABEL_REMOVED` - Fired when labels are removed

For more information on these events, see [Appointment Events](/sdk/events/#appointments).

## Related Documentation

- [Appointment and Task Label Automation Guide](/guides/appointment-label-automation/) - Complete workflow examples
- [Appointment Events](/sdk/events/#appointments) - Event documentation
- [Appointment Coverage Label Example](/sdk/examples/appointment_coverage_label/) - Real-world example plugin
- [Task Data Model](/sdk/data/task/) - Task label field documentation
