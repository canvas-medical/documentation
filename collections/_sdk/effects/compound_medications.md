---
title: "Compound Medication Effects"
slug: "effect-compound-medication"
excerpt: "Effects for managing compound medications"
hidden: false
---

The Compound Medication effects enable the creation and management of compound medication formulations within the Canvas
system. These effects support the customization of medications prepared by compounding pharmacies according to
prescriptions.

Build a `CompoundMedication` with the [attributes](#attributes) you want to set, then return one of its two methods from your handler: `create()` for a new compound medication, or `update()` for an existing one.

## Methods

### create() → Effect

Creates a compound medication.

- `formulation`, `potency_unit_code`, and `controlled_substance` are required.
- `controlled_substance_ndc` is also required when `controlled_substance` is anything other than `"N"`.

See [Creating a compound medication](#creating-a-compound-medication) for an example.

### update() → Effect

Updates an existing compound medication.

- `instance_id` is required, and must be the id of an existing compound medication.
- Only the attributes you set on the effect are changed. Attributes you leave unset keep their current values.

See [Updating a compound medication](#updating-a-compound-medication) for an example.

## Attributes

| Attribute                  | Type             | Description                                                    | Required |
|----------------------------|------------------|----------------------------------------------------------------|----------|
| `instance_id`              | `str` or `None`  | The id of the compound medication to update                    | For `update()` |
| `formulation`              | `str` or `None`  | The compound medication formulation (max 105 characters)       | For `create()` |
| `potency_unit_code`        | `str` or `None`  | The unit of measurement for the medication                     | For `create()` |
| `controlled_substance`     | `str` or `None`  | The controlled substance schedule                              | For `create()` |
| `controlled_substance_ndc` | `str` or `None`  | NDC code for controlled substances (dashes removed)            | When `controlled_substance` is not `"N"` |
| `active`                   | `bool` or `None` | Whether the compound medication is active. Defaults to `True` on creation. | No       |

## Example Usage

### Creating a compound medication

```python
from canvas_sdk.effects.compound_medications import CompoundMedication as CompoundMedicationEffect
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType

from canvas_sdk.v1.data.compound_medication import CompoundMedication as CompoundMedicationModel


class CompoundMedicationCreator(BaseHandler):
  RESPONDS_TO = [EventType.Name(EventType.PATIENT_CREATED)]

  def compute(self):
    # Create a non-controlled compound medication
    compound_med = CompoundMedicationEffect(
      formulation="Testosterone 200mg/mL in Grapeseed Oil",
      potency_unit_code=CompoundMedicationModel.PotencyUnit.Milliliter,
      controlled_substance=CompoundMedicationModel.ControlledSubstanceSchedule.SCHEDULE_NOT_SCHEDULED,
      active=True
    )

    # Create a controlled substance compound medication
    controlled_compound = CompoundMedicationEffect(
      formulation="Hydrocodone 5mg/Acetaminophen 325mg Capsule",
      potency_unit_code=CompoundMedicationModel.PotencyUnit.Capsule,
      controlled_substance=CompoundMedicationModel.ControlledSubstanceSchedule.SCHEDULE_II,
      controlled_substance_ndc="12345678901",
      active=True
    )

    return [compound_med.create(), controlled_compound.create()]
```

### Updating a compound medication

```python
from canvas_sdk.effects.compound_medications import CompoundMedication as CompoundMedicationEffect
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.compound_medication import CompoundMedication as CompoundMedicationModel
from canvas_sdk.events import EventType


class CompoundMedicationUpdater(BaseHandler):
  RESPONDS_TO = [EventType.Name(EventType.PLUGIN_CREATED)]

  def compute(self):
    # Find a compound medication to update
    compound_med = CompoundMedicationModel.objects.filter(
        formulation__contains="Testosterone"
    ).first()

    if compound_med:
        # Update to make it a controlled substance
        update_effect = CompoundMedicationEffect(
            instance_id=str(compound_med.id),
            controlled_substance="III",
            controlled_substance_ndc="98765432101"
        )

        return [update_effect.update()]

    return []
```

## Implementation Details

- **Formulation Validation**: The formulation field is limited to 105 characters
- **NDC Formatting**: Any dashes in the NDC code are automatically removed during processing
- **Cross-field Validation**: When a controlled substance schedule is specified (anything other than "N"), an NDC code
  must be provided
- **Default Values**: If not specified, `active` defaults to `True` for new compound medications
- **Potency Unit Codes**: Must use valid codes as defined in
  the [PotencyUnit](/sdk/data-compound-medication/#potencyunit) enumeration
- **Controlled Substance Schedules**: Must use valid values as defined in
  the [ControlledSubstanceSchedule](/sdk/data-compound-medication/#controlledsubstanceschedule) enumeration

## Validation

Both methods perform validation before execution:

### Create Effect Validation:

- Validates all required fields are provided
- Ensures `potency_unit_code` is a valid value from the PotencyUnit enumeration
- Ensures `controlled_substance` is a valid schedule from the ControlledSubstanceSchedule enumeration
- Validates NDC is provided for controlled substances (when schedule is not "N")
- Checks formulation length does not exceed 105 characters

### Update Effect Validation:

- Verifies the compound medication exists before updating
- Validates any provided fields follow the same rules as creation
- Ensures NDC is provided if updating to a controlled substance
- Only updates fields that are explicitly provided (partial updates supported)

## Error Handling

If validation fails, a `ValidationError` is raised with detailed error messages indicating which fields failed
validation and why. Error messages are aggregated to provide comprehensive feedback about all validation failures at
once.

<br/>
<br/>
<br/>
