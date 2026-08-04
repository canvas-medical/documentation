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

Use `CommandValidationErrorEffect` with a command's `__POST_VALIDATION` event to check the command as it is entered and surface problems before it is committed. These events follow the pattern:

`{COMMAND_KEY}_COMMAND__POST_VALIDATION`

The following command types fire `__POST_VALIDATION` and can be validated with this effect:

- `ADJUST_PRESCRIPTION_COMMAND__POST_VALIDATION`
- `ALLERGY_COMMAND__POST_VALIDATION`
- `APPROVE_REFILL_COMMAND__POST_VALIDATION`
- `ASSESS_CODING_GAP_COMMAND__POST_VALIDATION`
- `ASSESS_COMMAND__POST_VALIDATION`
- `CANCEL_PRESCRIPTION_COMMAND__POST_VALIDATION`
- `CHANGE_MEDICATION_COMMAND__POST_VALIDATION`
- `CHART_SECTION_REVIEW_COMMAND__POST_VALIDATION`
- `CLIPBOARD_COMMAND__POST_VALIDATION`
- `CLOSE_GOAL_COMMAND__POST_VALIDATION`
- `CREATE_CODING_GAP_COMMAND__POST_VALIDATION`
- `DEFER_CODING_GAP_COMMAND__POST_VALIDATION`
- `DENY_REFILL_COMMAND__POST_VALIDATION`
- `DIAGNOSE_COMMAND__POST_VALIDATION`
- `EDUCATIONAL_MATERIAL_COMMAND__POST_VALIDATION`
- `FAMILY_HISTORY_COMMAND__POST_VALIDATION`
- `FOLLOW_UP_COMMAND__POST_VALIDATION`
- `GOAL_COMMAND__POST_VALIDATION`
- `HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_VALIDATION`
- `IMAGING_ORDER_COMMAND__POST_VALIDATION`
- `IMMUNIZATION_STATEMENT_COMMAND__POST_VALIDATION`
- `IMMUNIZE_COMMAND__POST_VALIDATION`
- `INSTRUCT_COMMAND__POST_VALIDATION`
- `LAB_ORDER_COMMAND__POST_VALIDATION`
- `MEDICAL_HISTORY_COMMAND__POST_VALIDATION`
- `MEDICATION_STATEMENT_COMMAND__POST_VALIDATION`
- `PERFORM_COMMAND__POST_VALIDATION`
- `PHYSICAL_EXAM_COMMAND__POST_VALIDATION`
- `PLAN_COMMAND__POST_VALIDATION`
- `POC_LAB_TEST_COMMAND__POST_VALIDATION`
- `PRESCRIBE_COMMAND__POST_VALIDATION`
- `QUESTIONNAIRE_COMMAND__POST_VALIDATION`
- `REASON_FOR_VISIT_COMMAND__POST_VALIDATION`
- `REFERENCE_COMMAND__POST_VALIDATION`
- `REFER_COMMAND__POST_VALIDATION`
- `REFILL_COMMAND__POST_VALIDATION`
- `REMOVE_ALLERGY_COMMAND__POST_VALIDATION`
- `RESOLVE_CONDITION_COMMAND__POST_VALIDATION`
- `ROS_COMMAND__POST_VALIDATION`
- `SNOOZE_PROTOCOL_COMMAND__POST_VALIDATION`
- `STOP_MEDICATION_COMMAND__POST_VALIDATION`
- `STRUCTURED_ASSESSMENT_COMMAND__POST_VALIDATION`
- `SURGICAL_HISTORY_COMMAND__POST_VALIDATION`
- `TASK_COMMAND__POST_VALIDATION`
- `UPDATE_DIAGNOSIS_COMMAND__POST_VALIDATION`
- `UPDATE_GOAL_COMMAND__POST_VALIDATION`
- `VALIDATE_CODING_GAP_COMMAND__POST_VALIDATION`
- `VISUAL_EXAM_FINDING_COMMAND__POST_VALIDATION`
- `VITALS_COMMAND__POST_VALIDATION`

The Custom Command, Imaging Review, Lab Review, Referral Review, Uncategorized Document Review commands do **not** fire `__POST_VALIDATION`, so they can't be validated with this effect.

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

`__PRE_DELETE` is fired by the following command types (every command except Chart Section Review):

- `ADJUST_PRESCRIPTION_COMMAND__PRE_DELETE`
- `ALLERGY_COMMAND__PRE_DELETE`
- `APPROVE_REFILL_COMMAND__PRE_DELETE`
- `ASSESS_CODING_GAP_COMMAND__PRE_DELETE`
- `ASSESS_COMMAND__PRE_DELETE`
- `CANCEL_PRESCRIPTION_COMMAND__PRE_DELETE`
- `CHANGE_MEDICATION_COMMAND__PRE_DELETE`
- `CLIPBOARD_COMMAND__PRE_DELETE`
- `CLOSE_GOAL_COMMAND__PRE_DELETE`
- `CREATE_CODING_GAP_COMMAND__PRE_DELETE`
- `CUSTOM_COMMAND_COMMAND__PRE_DELETE`
- `DEFER_CODING_GAP_COMMAND__PRE_DELETE`
- `DENY_REFILL_COMMAND__PRE_DELETE`
- `DIAGNOSE_COMMAND__PRE_DELETE`
- `EDUCATIONAL_MATERIAL_COMMAND__PRE_DELETE`
- `FAMILY_HISTORY_COMMAND__PRE_DELETE`
- `FOLLOW_UP_COMMAND__PRE_DELETE`
- `GOAL_COMMAND__PRE_DELETE`
- `HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_DELETE`
- `IMAGING_ORDER_COMMAND__PRE_DELETE`
- `IMAGING_REVIEW_COMMAND__PRE_DELETE`
- `IMMUNIZATION_STATEMENT_COMMAND__PRE_DELETE`
- `IMMUNIZE_COMMAND__PRE_DELETE`
- `INSTRUCT_COMMAND__PRE_DELETE`
- `LAB_ORDER_COMMAND__PRE_DELETE`
- `LAB_REVIEW_COMMAND__PRE_DELETE`
- `MEDICAL_HISTORY_COMMAND__PRE_DELETE`
- `MEDICATION_STATEMENT_COMMAND__PRE_DELETE`
- `PERFORM_COMMAND__PRE_DELETE`
- `PHYSICAL_EXAM_COMMAND__PRE_DELETE`
- `PLAN_COMMAND__PRE_DELETE`
- `POC_LAB_TEST_COMMAND__PRE_DELETE`
- `PRESCRIBE_COMMAND__PRE_DELETE`
- `QUESTIONNAIRE_COMMAND__PRE_DELETE`
- `REASON_FOR_VISIT_COMMAND__PRE_DELETE`
- `REFERENCE_COMMAND__PRE_DELETE`
- `REFERRAL_REVIEW_COMMAND__PRE_DELETE`
- `REFER_COMMAND__PRE_DELETE`
- `REFILL_COMMAND__PRE_DELETE`
- `REMOVE_ALLERGY_COMMAND__PRE_DELETE`
- `RESOLVE_CONDITION_COMMAND__PRE_DELETE`
- `ROS_COMMAND__PRE_DELETE`
- `SNOOZE_PROTOCOL_COMMAND__PRE_DELETE`
- `STOP_MEDICATION_COMMAND__PRE_DELETE`
- `STRUCTURED_ASSESSMENT_COMMAND__PRE_DELETE`
- `SURGICAL_HISTORY_COMMAND__PRE_DELETE`
- `TASK_COMMAND__PRE_DELETE`
- `UNCATEGORIZED_DOCUMENT_REVIEW_COMMAND__PRE_DELETE`
- `UPDATE_DIAGNOSIS_COMMAND__PRE_DELETE`
- `UPDATE_GOAL_COMMAND__PRE_DELETE`
- `VALIDATE_CODING_GAP_COMMAND__PRE_DELETE`
- `VISUAL_EXAM_FINDING_COMMAND__PRE_DELETE`
- `VITALS_COMMAND__PRE_DELETE`

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
