---
title: "Compound Medication"
slug: "effect-compound-medication"
excerpt: "Effects for managing compound medications"
hidden: false
---

# Compound Medication Effects

The Compound Medication effects enable the creation and management of compound medication formulations within the Canvas
system. These effects support the customization of medications prepared by compounding pharmacies according to
prescriptions.

## Create Compound Medication

The `CreateCompoundMedication` effect creates a new compound medication formulation in the system.

### Attributes

| Attribute                  | Type            | Description                                              | Required |
|----------------------------|-----------------|----------------------------------------------------------|----------|
| `formulation`              | `str`           | The compound medication formulation (max 105 characters) | Yes      |
| `potency_unit_code`        | `str`           | The unit of measurement for the medication               | Yes      |
| `controlled_substance`     | `str`           | The controlled substance schedule                        | Yes      |
| `controlled_substance_ndc` | `str` or `None` | NDC code for controlled substances (dashes removed)      | No*      |
| `active`                   | `bool`          | Whether the compound medication is active                | No       |

*Required when `controlled_substance` is not "N" (None)

### Example Usage

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

## Update Compound Medication

The `UpdateCompoundMedication` effect modifies an existing compound medication formulation.

### Attributes

| Attribute                  | Type             | Description                                              | Required |
|----------------------------|------------------|----------------------------------------------------------|----------|
| `compound_medication_id`   | `str`            | The ID of the compound medication to update              | Yes      |
| `formulation`              | `str` or `None`  | The compound medication formulation (max 105 characters) | No       |
| `potency_unit_code`        | `str` or `None`  | The unit of measurement for the medication               | No       |
| `controlled_substance`     | `str` or `None`  | The controlled substance schedule                        | No       |
| `controlled_substance_ndc` | `str` or `None`  | NDC code for controlled substances (dashes removed)      | No       |
| `active`                   | `bool` or `None` | Whether the compound medication is active                | No       |

### Example Usage

```python
from canvas_sdk.effects.compound_medication import CompoundMedication as CompoundMedicationEffect
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.compound_medication import CompoundMedication as CompoundMedicationModel
from canvas_sdk.events import EventType


class CompoundMedicationUpdater(BaseHandler):
  RESPONDS_TO = [EventType.Name(EventType.PLUGIN_CREATED)]

  def compute(self):
    # Find a compound medication to update
    compound_med_model = CompoundMedicationModel.objects.filter(
      formulation__contains="Testosterone"
    ).first()

    if compound_med:
      # Update to make it a controlled substance
      update_effect = CompoundMedicationEffect(
        compound_medication_id=str(compound_med_model.id),
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

Both effects perform validation before execution:

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
