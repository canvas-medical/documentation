---
title: "Field Action Value"
slug: "effect-field-action-value"
excerpt: "Supply the text a command field action, such as Use standard sig, fills into its field."
hidden: false
---

Some command fields carry an action button that fills the field with suggested text. The sig field of a prescription shows **Use standard sig**, which fills in First Databank's (FDB) standard sig for the selected drug. Use the `FieldActionValue` effect to supply your own text for that button, such as your organization's preferred sig for a drug, or to hide the button.

Return a `FieldActionValue` from a handler for the `COMMAND__FIELD_ACTION__VALUE` [event](/sdk/events/).

## Where field actions appear

The standard sig action, named `standard_sig`, is on the `sig` field of these commands:

- Prescribe
- Refill
- Adjust Prescription
- Medication Statement
- Change Medication

A plugin can supply the value of an action a field already has. It can't add an action to a field.

## How Canvas picks the value

Canvas sends `COMMAND__FIELD_ACTION__VALUE` when a command with a field action loads in a note, and again after a change to one of the command's other fields saves. Selecting a new drug, for example, asks for the sig again.

- When a handler returns a `FieldActionValue`, its `value` is what the button fills in. If several handlers return one, Canvas uses the last.
- A `value` of `None` hides the button for that command.
- When no handler returns a `FieldActionValue`, Canvas uses its own value: FDB's standard sig for the drug, or none when the drug has no FDB code or FDB has no sig for it.

The button shows only when it has text to fill in, and hovering over it previews that text. When the field already holds different text, Canvas asks the user before replacing it. The button is hidden while the field can't be edited.

## Event context

The event target is the command, and `self.event.target.id` is its id. The context holds:

| Key          | Type   | Description                                                        |
|--------------|--------|--------------------------------------------------------------------|
| `schema_key` | `str`  | The command's schema key, such as `"prescribe"`.                   |
| `field`      | `str`  | The field the action fills, such as `"sig"`.                       |
| `action`     | `str`  | The action's name, such as `"standard_sig"`.                       |
| `fields`     | `dict` | The command's current field values, as saved.                      |

The event also carries the [actor](/sdk/events/#event-actor), the user viewing the command.

## Attributes

| Attribute | Type          | Description                                                          | Required |
|-----------|---------------|----------------------------------------------------------------------|----------|
| `value`   | `str \| None` | The text the action fills into the field. `None` hides the action.  | Yes      |

## Methods

### apply() → Effect

Returns the effect with the payload `{"data": {"value": ...}}`.

## Example

The following handler fills Prescribe's sig with a house sig for drugs in a formulary, keyed by FDB code. For any other drug it returns nothing, so Canvas falls back to FDB's standard sig.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.field_action_value import FieldActionValue
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler

FDB_SYSTEM = "http://www.fdbhealth.com/"

# FDB code -> the sig your organization prefers for that drug.
HOUSE_SIGS = {
    "206813": "Take 1 tablet by mouth every 6 hours as needed for pain. Max 6 tablets a day.",
}


class HouseStandardSig(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.COMMAND__FIELD_ACTION__VALUE)

    def compute(self) -> list[Effect]:
        context = self.event.context
        if context["schema_key"] != "prescribe" or context["action"] != "standard_sig":
            return []

        # The Prescribe command keeps the selected drug in its "prescribe" field.
        medication = context["fields"].get("prescribe") or {}
        codings = (medication.get("extra") or {}).get("coding") or []
        fdb_code = next(
            (str(coding["code"]) for coding in codings if coding.get("system") == FDB_SYSTEM),
            None,
        )

        if fdb_code not in HOUSE_SIGS:
            return []

        return [FieldActionValue(value=HOUSE_SIGS[fdb_code]).apply()]
```

To hide the button instead, return `FieldActionValue(value=None).apply()`.
