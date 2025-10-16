---
title: "Events"
slug: "events"
layout: devpage
hidden: false
---

**Lesson 3: Understanding Events in Canvas Plugins**

## What are Events?

Events are real-time occurrences of actions within Canvas. When something happens in the EHR system (like creating a prescription, updating a patient record, or entering vitals), Canvas emits an event that your plugin can listen to and respond with custom logic.

## Setting Up Event Handlers

To respond to events, create a protocol class that inherits from `BaseProtocol` and specify which events to listen for:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log

class Protocol(BaseProtocol):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_CREATED)]

    def compute(self):
        # Your custom logic here
        log.info(f"New patient created: {self.target}")
        return []
```

## Understanding Event Data

When an event triggers your `compute()` method, you have access to:

- **`self.target`** - The ID of the primary resource (patient, task, condition, etc.)
- **`self.context`** - Additional data specific to the event type
- **`self.event`** - The complete event object
- **`self.secrets`** - Your configured plugin secrets

## Common Event Types and Their Payloads

### 1. Record Lifecycle Events

These fire when records are created, updated, or deleted.

**Patient Created:**
```python
from logger import log
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.events import EventType

class Protocol(BaseProtocol):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_CREATED)]

    def compute(self):
        # Target: patient_id
        # Context: {} (empty)
        patient_id = self.target
        return []
```

**Task Created:**
```python
from logger import log
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.events import EventType

class Protocol(BaseProtocol):
    RESPONDS_TO = [EventType.Name(EventType.TASK_CREATED)]

    def compute(self):
        # Target: task_id
        # Context: {"patient": {"id": "patient_123"}}
        task_id = self.target
        patient_id = self.context["patient"]["id"]
        return []
```

### 2. Command Lifecycle Events

These fire during clinical documentation workflows.

**Generic Command Events:**
- `PRE_COMMAND_COMMIT` - Before any command is saved
- `POST_COMMAND_COMMIT` - After any command is saved
- `PRE_COMMAND_UPDATE` - Before command data changes
- `POST_COMMAND_UPDATE` - After command data changes

**Command Context Structure**:
```python
{
    "note": {"uuid": "note_123"},
    "patient": {"id": "patient_123"},
    "fields": {
        # Command-specific data
    }
}
```

**Prescribe Command Example:**
```python
from logger import log
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.events import EventType

class Protocol(BaseProtocol):
    RESPONDS_TO = [EventType.Name(EventType.PRESCRIBE_COMMAND__PRE_COMMIT)]

    def compute(self):
        # Validate prescription before commit
        fields = self.context["fields"]
        medication = fields.get("prescribe")
        days_supply = fields.get("days_supply")

        if days_supply and days_supply > 90:
            log.warning(f"Long prescription: {days_supply} days")

        return []
```

**Vitals Command Example**:
```python
from logger import log
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.events import EventType

class Protocol(BaseProtocol):
    RESPONDS_TO = [EventType.Name(EventType.VITALS_COMMAND__POST_COMMIT)]

    def compute(self):
        fields = self.context["fields"]
        systolic = fields.get("blood_pressure_systole")

        if systolic and systolic > 140:
            patient_id = self.context["patient"]["id"]
            log.warning(f"High BP for patient {patient_id}: {systolic}")

        return []
```

### 3. Search Events

These fire when users search for items, allowing you to customize results.

**Medication Search Result Structure**:
```json
{
    "text": "acetaminophen 500 mg tablet",
    "value": 206813,
    "extra": {
        "coding": [{
            "code": "198440",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
        }]
    }
}
```

### 4. UI Events

These fire during UI interactions.

**Action Button Click:**
```python
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.events import EventType

class Protocol(BaseProtocol):
    RESPONDS_TO = [EventType.Name(EventType.ACTION_BUTTON_CLICKED)]

    def compute(self):
        # Context includes clicked button key and user info
        button_key = self.context["key"]
        user_id = self.context["user"]["id"]
        patient_id = self.target

        if button_key == "my_custom_action":
            # Handle button click
            pass

        return []
```

## Best Practices

1. **Log First** - Canvas SDK provides a custom logging module that publishes logs to a pub/sub channel. When working with a new event, log the data to understand what's available:

```python
from logger import log

def compute(self):
    log.info(f"Target: {self.target}")
    log.info(f"Context: {self.context}")
    return []
```

2. **Handle Errors Gracefully** - Wrap your logic in try-except blocks:
```python
from logger import log

def compute(self):
    try:
        # Your logic here
        pass
    except Exception as e:
        log.error(f"Error: {str(e)}")
    return []
```

3. **Use Pre/Post Events Wisely**:
   - Use `PRE_*` events for validation or prevention
   - Use `POST_*` events for notifications or downstream actions

## Monitoring Your Plugin

View logs in real-time with the Canvas CLI:
```bash
canvas logs --host your-instance-name
```

## Quick Reference

| Event Category | Common Events | Target | Context |
|---|---|---|---|
| Records | `PATIENT_CREATED`, `TASK_UPDATED` | Record ID | `{"patient": {"id": "..."}}` |
| Commands | `*_COMMAND__PRE_COMMIT` | Command ID | Note, patient, and field data |
| Search | `*__POST_SEARCH` | Command ID | Search term and results |
| UI | `ACTION_BUTTON_CLICKED` | Patient ID | Button key and user info |

For a complete list of events and their payloads, refer to the [Canvas SDK documentation](https://docs.canvasmedical.com/sdk/events/).

## Next Steps

Now that we've explored different event types and their contexts, you're ready for the following:

* Traverse Data objects
* Return various Effect types
* SimpleAPI deep dive
