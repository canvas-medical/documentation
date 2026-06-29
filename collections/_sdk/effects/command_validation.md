---
title: "Command Validation"
slug: "effect-command-validation"
excerpt: "Validate commands and return structured error messages to users."
hidden: false
---

The `CommandValidationErrorEffect` returns structured error messages that are displayed to users in the Canvas UI. It serves two purposes:

- **Validate a command** as it is entered in the Canvas UI, surfacing problems before it can be committed (`__POST_VALIDATION` events).
- **Block a deletion** by returning the effect from a command's `__PRE_DELETE` handler.

In both cases you build a `CommandValidationErrorEffect`, attach one or more error messages, and return it from your handler.

Where these errors are enforced differs by event: `__POST_VALIDATION` errors block a commit **only in the Canvas UI**, while `__PRE_DELETE` errors block a deletion through **both** the Canvas UI and the SDK [commands module](/sdk/commands/). Each section below covers the specifics.

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

When validation errors are returned, the Canvas UI shows them to the user — the command's action buttons are disabled and the messages appear as a tooltip — so the command can't be committed there. Multiple errors can be returned at once, and all are displayed.

> **Note:** `__POST_VALIDATION` only gates committing **in the Canvas UI**. A `.commit()` made through the SDK [commands module](/sdk/commands/) is **not** blocked by these errors — the command still commits. Use it as a UI guardrail, not as an enforced rule on SDK-driven commits. (Blocking a deletion, below, *does* work through both the UI and the SDK.)

## Block a deletion

Return a `CommandValidationErrorEffect` from a command's `__PRE_DELETE` handler to block its deletion. Unlike `__POST_VALIDATION`, this works through **both** the Canvas UI and the SDK [commands module](/sdk/commands/): the deletion is aborted, the surrounding transaction is rolled back, and the error messages are returned to whatever initiated the delete — a [`delete()`](/sdk/commands/) call or a delete in the UI. For SDK-initiated deletes, the error is written to `canvas logs`. Pre-delete events follow the pattern:

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
