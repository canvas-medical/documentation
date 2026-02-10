---
title: "Command Validation"
slug: "effect-command-validation"
excerpt: "Validate commands and return structured error messages to users."
hidden: false
---

The Canvas SDK allows you to validate commands and return structured error messages that will be displayed to users in the Canvas UI.

## Command Validation Effect

To add validation errors to a command, import the `CommandValidationErrorEffect` class and create an instance of it. This effect is typically used in conjunction with the `PLAN_COMMAND__POST_VALIDATION` event (or similar validation events for other command types).

### Parameters

The `CommandValidationErrorEffect` class accepts an optional list of `ValidationError` objects during initialization:

| Attribute | Type                     | Required | Description                                            |
| --------- | ------------------------ | -------- | ------------------------------------------------------ |
| `errors`  | list[ValidationError]    | optional | List of validation errors to be displayed to the user. |

### ValidationError

Each `ValidationError` object represents a single validation error message:

| Attribute | Type   | Required | Description                         |
| --------- | ------ | -------- | ----------------------------------- |
| `message` | String | required | The validation error message to display. Must not be empty. |

### Adding Validation Errors

There are several ways to add validation errors to the effect:

#### Method 1: Using `add_error()` method

The `add_error()` method allows you to incrementally build validation errors and supports method chaining:

```python
from canvas_sdk.commands import PlanCommand
from canvas_sdk.commands.validation import CommandValidationErrorEffect
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PLAN_COMMAND__POST_VALIDATION)

    def compute(self) -> list[Effect]:
        narrative = self.context["fields"]["narrative"]

        # Create the validation effect
        effect = CommandValidationErrorEffect()

        # Add validation errors using the add_error method
        if not narrative or len(narrative.strip()) < 10:
            effect.add_error("Narrative must be at least 10 characters long")

        if "TODO" in narrative.upper():
            effect.add_error("Narrative cannot contain TODO items")

        # Return the effect using the apply() method
        return [effect.apply()]
```

#### Method 2: Method chaining

The `add_error()` method returns `self`, allowing for clean method chaining:

```python
from canvas_sdk.commands.validation import CommandValidationErrorEffect
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PLAN_COMMAND__POST_VALIDATION)

    def compute(self) -> list[Effect]:
        narrative = self.context["fields"]["narrative"]

        effect = CommandValidationErrorEffect()

        if not narrative:
            effect.add_error("Narrative is required").add_error("Please provide details about the plan")

        return [effect.apply()]
```

#### Method 3: Initialize with errors

You can also initialize the effect with a list of `ValidationError` objects:

```python
from canvas_sdk.commands.validation import CommandValidationErrorEffect, ValidationError
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PLAN_COMMAND__POST_VALIDATION)

    def compute(self) -> list[Effect]:
        narrative = self.context["fields"]["narrative"]

        errors = []

        if not narrative:
            errors.append(ValidationError("Narrative is required"))

        if narrative and len(narrative.strip()) < 10:
            errors.append(ValidationError("Narrative must be at least 10 characters long"))

        effect = CommandValidationErrorEffect(errors=errors)
        return [effect.apply()]
```

## Example Use Case

Here's a complete example that validates a Plan command to ensure it meets specific requirements:

```python
from canvas_sdk.commands import PlanCommand
from canvas_sdk.commands.validation import CommandValidationErrorEffect
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log

class Protocol(BaseProtocol):
    """
    Example protocol demonstrating command validation.

    This protocol validates Plan commands to ensure they meet
    organizational requirements before being committed.
    """

    RESPONDS_TO = EventType.Name(EventType.PLAN_COMMAND__POST_VALIDATION)

    def compute(self) -> list[Effect]:
        log.info("Running command validation protocol.")

        # Extract command fields from context
        narrative = self.context["fields"]["narrative"]

        # Create the validation effect
        effect = CommandValidationErrorEffect()

        # Perform validation checks
        if not narrative or not narrative.strip():
            effect.add_error("Narrative is required and cannot be empty")
        elif len(narrative.strip()) < 10:
            effect.add_error("Narrative must be at least 10 characters long")

        # Check for prohibited content
        prohibited_terms = ["TODO", "TBD", "FIXME"]
        if any(term in narrative.upper() for term in prohibited_terms):
            effect.add_error("Narrative cannot contain placeholder text (TODO, TBD, FIXME)")

        # Check for required keywords (example: follow-up plans must mention timeline)
        if "follow" in narrative.lower() and not any(word in narrative.lower() for word in ["week", "month", "day"]):
            effect.add_error("Follow-up plans must include a specific timeline")

        # Return the effect
        return [effect.apply()]
```

## Behavior

- When validation errors are returned, they will be displayed to the user in the Canvas UI
- The command will not be committed if validation errors are present
- Multiple validation errors can be returned at once, and all will be displayed to the user

## Related Events

The command validation effect can be used with command validation events. All command types support `__POST_VALIDATION` events following the naming pattern:

`{COMMAND_KEY}_COMMAND__POST_VALIDATION`

For example:
- `PLAN_COMMAND__POST_VALIDATION`
- `PRESCRIBE_COMMAND__POST_VALIDATION`
- `DIAGNOSE_COMMAND__POST_VALIDATION`

For more information about command events and their context objects, see the [Events documentation](/sdk/events/).

<br/>
<br/>
<br/>
