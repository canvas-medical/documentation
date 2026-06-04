---
title: "Command Validation"
slug: "effect-command-validation"
excerpt: "Validate commands and return structured error messages to users."
hidden: false
---

The `CommandValidationErrorEffect` returns structured error messages that are displayed to users in the Canvas UI. It serves two purposes:

- **Validate a command** as it is being entered, surfacing problems before the command is committed (`__POST_VALIDATION` events).
- **Block a deletion** by returning the effect from a command's `__PRE_DELETE` handler.

In both cases you build a `CommandValidationErrorEffect`, attach one or more error messages, and return it from your handler.

These validations run as part of the **SDK command lifecycle** — not in the browser — so they apply both to commands entered or acted on in the Canvas UI and to commands driven through the SDK [commands module](/sdk/commands/) (command effects). When a check fails, the operation is stopped and the error is surfaced to whoever initiated it.

## The effect

### CommandValidationErrorEffect

The `CommandValidationErrorEffect` class accepts an optional list of `ValidationError` objects during initialization:

| Attribute | Type                     | Required | Description                                            |
| --------- | ------------------------ | -------- | ------------------------------------------------------ |
| `errors`  | list[ValidationError]    | optional | List of validation errors to be displayed to the user. |

### ValidationError

Each `ValidationError` object represents a single validation error message:

| Attribute | Type   | Required | Description                         |
| --------- | ------ | -------- | ----------------------------------- |
| `message` | String | required | The validation error message to display. Must not be empty. |

### Building the errors

Add errors incrementally with `add_error()`, which returns `self` so calls can be chained:

```python?partial=True
effect = CommandValidationErrorEffect()
effect.add_error("Narrative is required").add_error("Please provide details about the plan")

return [effect.apply()]
```

Or pass a list of `ValidationError` objects to the constructor:

```python?partial=True
from canvas_sdk.commands.validation import CommandValidationErrorEffect, ValidationError

errors = [
    ValidationError("Narrative is required"),
    ValidationError("Narrative must be at least 10 characters long"),
]

effect = CommandValidationErrorEffect(errors=errors)

return [effect.apply()]
```

## Validate a command

Use `CommandValidationErrorEffect` with a command's `__POST_VALIDATION` event to check the command as it is entered and surface problems before it is committed. Every command type fires this event, following the pattern:

`{COMMAND_KEY}_COMMAND__POST_VALIDATION`

For example:

- `PLAN_COMMAND__POST_VALIDATION`
- `PRESCRIBE_COMMAND__POST_VALIDATION`
- `DIAGNOSE_COMMAND__POST_VALIDATION`

The following handler validates a Plan command to ensure it meets specific requirements:

```python
from canvas_sdk.commands import PlanCommand
from canvas_sdk.commands.validation import CommandValidationErrorEffect
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from logger import log

class MyHandler(BaseHandler):
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

When validation errors are returned:

- they are displayed to the user in the Canvas UI,
- the command is not committed, and
- multiple errors can be returned at once, and all are displayed.

## Block a deletion

Return a `CommandValidationErrorEffect` from a command's `__PRE_DELETE` handler to block its deletion. The deletion is aborted, the surrounding transaction is rolled back, and the error messages are returned to whatever initiated the delete — the [`delete()`](/sdk/commands/) method in the SDK commands module, or a delete in the Canvas UI. Pre-delete events follow the pattern:

`{COMMAND_KEY}_COMMAND__PRE_DELETE`

The following handler prevents deletion of a Refer command once its priority has been set to `Urgent` or `STAT`, so high-priority referrals can't be removed by mistake. The command's field values are available on the event context, so no extra lookup is needed:

```python
from canvas_sdk.commands import ReferCommand
from canvas_sdk.commands.validation import CommandValidationErrorEffect
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class BlockUrgentReferralDeletionHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.REFER_COMMAND__PRE_DELETE)

    def compute(self) -> list[Effect]:
        priority = self.context["fields"].get("priority")

        protected = {ReferCommand.Priority.URGENT.value, ReferCommand.Priority.STAT.value}
        if priority in protected:
            effect = CommandValidationErrorEffect()
            effect.add_error(
                f"A {priority}-priority referral can't be deleted. "
                "Lower its priority first if you need to remove it."
            )
            return [effect.apply()]

        return []
```

When a delete is attempted on an `Urgent` or `STAT` referral, it is blocked and the error message is returned to whoever initiated it.

For more information about command events and their context objects, see the [Events documentation](/sdk/events/).

<br/>
<br/>
<br/>
