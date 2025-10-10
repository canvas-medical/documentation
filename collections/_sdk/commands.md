---
title: "Commands"
---

The commands module lets you create and update commands within a specific note in Canvas. Commands are the building blocks of many end-user workflows in Canvas, including nearly all clinical workflows for documentation, like HPIs and questionnaires, as well as orders like prescriptions, labs, and referrals. Each Command class can be instantiated in your plugin and used to build a new command instance within a specific note or update an existing instance. The commands are then displayed in real time within the end user's workflow.

Common objectives that can be met by using Command classes include dynamic note templates, clinical decision support, order set composition, care gap closure, and care coordination automation.

## Common Attributes

### Parameters

All commands share the following init kwarg parameters:

| Name           | Type     | Required                               | Description                                                             |
|:---------------|:---------|:---------------------------------------|:------------------------------------------------------------------------|
| `note_uuid`    | _string_ | `true` if creating a new command       | The externally exposable id of the note in which to insert the command. |
| `command_uuid` | _string_ | `true` if updating an existing command | The externally exposable id of the command which is being referenced.   |

All parameters can be set upon initialization, and also updated on the class instance.

### Methods

All commands have the following methods:

#### originate

Returns an Effect that originates a new command in the note body.

#### edit

Returns an Effect that edits an existing command with the values set on the command class instance.

**Behavior and Considerations:**
- **Partial Edits:** If you update only some fields of the command, any fields not explicitly modified will retain their existing values.
- **No Changes:** Calling `edit()` without making any changes will result in a no-op; the command remains unchanged.
- **Invalid Values:** If you attempt to set an invalid value, you should receive a validation error.

#### delete

Returns an Effect that deletes an existing, non-committed command from the note body.

#### commit

Returns an Effect that commits an existing, non-committed command to the note body.

#### send

Returns an Effect that sends a signed command.

**Limited availability** The `send()` method can only be called on [LabOrder](#laborder) and [Prescribe](#prescribe) command objects. Other command types do not support this operation.

#### enter_in_error

Returns an effect that enter-in-errors an existing, committed command in the note body.

**Example**:

```python
from canvas_sdk.commands import PlanCommand

def compute():

    existing_plan = PlanCommand(command_uuid='63hdik', narrative='something new')
    new_plan = PlanCommand(note_uuid='rk786p', narrative='new')
    new_plan.narrative = 'newer'

    return [existing_plan.edit(), new_plan.originate()]
```

## Command Constants

The `canvas_sdk.commands.constants` module provides essential classes and enumerations used across various Canvas SDK command implementations. These constants ensure consistency and provide structured data types for common medical and administrative elements.

### ClinicalQuantity

`ClinicalQuantity` represents detailed information about the form or unit of medication, particularly for prescription-related commands.

| Field Name                      | Type     | Description                                           |
|---------------------------------|----------|-------------------------------------------------------|
| `representative_ndc`            | _string_ | National Drug Code (NDC) representing the medication. |
| `ncpdp_quantity_qualifier_code` | _string_ | NCPDP code indicating the quantity qualifier.         |

**Usage Example**:

```python
from canvas_sdk.commands import PrescribeCommand
from canvas_sdk.commands.constants import ClinicalQuantity

# Using ClinicalQuantity in a prescription
clinical_quantity = ClinicalQuantity(
    representative_ndc="12843016128",
    ncpdp_quantity_qualifier_code="C48542"
)

prescribe = PrescribeCommand(
    note_uuid="rk786p",
    fdb_code="216092",
    icd10_codes=["R51"],
    sig="Take one tablet daily after meals",
    days_supply=30,
    quantity_to_dispense=30,
    type_to_dispense=clinical_quantity,
    refills=3,
    substitutions=PrescribeCommand.Substitutions.ALLOWED
)
```

### ServiceProvider

`ServiceProvider` represents detailed information about healthcare service providers, used in referral and imaging order commands.

| Field Name       | Type               | Description                                            |
|------------------|--------------------|--------------------------------------------------------|
| `first_name`     | _string_           | Service provider's first name (max length 512)         |
| `last_name`      | _string_           | Service provider's last name (max length 512)          |
| `specialty`      | _string_           | Provider's specialty (max length 512)                  |
| `practice_name`  | _string_           | Name of the practice (max length 512)                  |
| `business_fax`   | _Optional[string]_ | Business fax number (optional, max length 512)         |
| `business_phone` | _Optional[string]_ | Business phone number (optional, max length 512)       |
| `business_address` | _Optional[string]_ | Business address (optional, max length 512)          |
| `notes`          | _Optional[string]_ | Additional notes (optional, max length 512)            |

**Usage Example**:

```python
from canvas_sdk.commands import ReferCommand
from canvas_sdk.commands.constants import ServiceProvider

# Creating a referral with service provider information
service_provider = ServiceProvider(
    first_name="John",
    last_name="Smith",
    specialty="Cardiology",
    practice_name="Heart Health Center",
    business_phone="555-0123",
    business_address="123 Medical Plaza, Suite 100"
)

refer = ReferCommand(
    note_uuid="rk786p",
    diagnosis_codes=["E119"],
    priority=ReferCommand.Priority.ROUTINE,
    clinical_question=ReferCommand.ClinicalQuestion.DIAGNOSTIC_UNCERTAINTY,
    notes_to_specialist="Patient needs cardiac evaluation",
    service_provider=service_provider
)
```

### CodeSystems

`CodeSystems` provides standardized medical coding system identifiers used throughout Canvas for consistent medical code classification.

**Available Code Systems**:

| Code System    | Description                                                    |
|----------------|----------------------------------------------------------------|
| `ICD10`        | International Classification of Diseases, 10th Revision       |
| `SNOMED`       | Systematized Nomenclature of Medicine Clinical Terms           |
| `RXNORM`       | RxNorm - standardized nomenclature for medications            |
| `UNSTRUCTURED` | Canvas-specific system for unstructured or custom codes       |

**Usage Example**:

```python
from canvas_sdk.commands.constants import CodeSystems, Coding

# Using different code systems
icd10_coding = Coding(
    system=CodeSystems.ICD10, 
    code="E11.9", 
    display="Type 2 diabetes mellitus without complications"
)

snomed_coding = Coding(
    system=CodeSystems.SNOMED, 
    code="65921008", 
    display="Drink plenty of fluids"
)

unstructured_coding = Coding(
    system=CodeSystems.UNSTRUCTURED, 
    code="Custom instruction text"
)
```

### Coding

`Coding` represents a coded value from a medical terminology system, providing structured representation of medical concepts.

| Field Name | Type     | Description                                    |
|------------|----------|------------------------------------------------|
| `system`   | _string_ | The coding system identifier (e.g., ICD-10, SNOMED) |
| `code`     | _string_ | The specific code within the system            |
| `display`  | _Optional[string]_ | Human-readable description of the code   |

**Usage Example**:

```python
from canvas_sdk.commands import InstructCommand
from canvas_sdk.commands.constants import CodeSystems, Coding

# Using structured coding with SNOMED
instruct_snomed = InstructCommand(
    note_uuid="rk786p",
    coding=Coding(
        system=CodeSystems.SNOMED,
        code="65921008",
        display="Drink plenty of fluids"
    ),
    comment="To address mild dehydration symptoms"
)

# Using unstructured coding for custom instructions
instruct_custom = InstructCommand(
    note_uuid="rk786p",
    coding=Coding(
        system=CodeSystems.UNSTRUCTURED,
        code="Physical medicine neuromuscular training"
    )
)
```

## Command Actions

All commands support user-triggered actions through the Canvas UI.
These actions appear as buttons or menu items that users can click to perform specific operations on commands.

Commands have two types of actions:
- **Generic actions** (available on all commands): print, audit history
- **Command-specific actions** (vary by command type): documented in each command's respective section below

### Customizing Action Availability

Developers can programmatically control command actions by:
- **Hiding actions** based on user permissions, roles, or command state
- **Reordering actions** to prioritize commonly used operations
- **Conditional display** depending on workflow requirements or business logic

Action customization is handled through plugin code that modifies the available action set accordingly.

### Generic Actions

The following actions are available on all command types:

#### print
Generates a printable version of the command for documentation or external sharing purposes.

#### audit_history
Displays the complete audit trail for the command, showing all modifications, state changes, and user interactions over time.

#### carry_forward
Populates the command with the last known data for this command type and patient, allowing users to quickly recreate similar commands based on previous entries.

### Command-Specific Actions

Individual command types have additional actions tailored to their functionality. These actions are documented in each command's respective section below.

{% include alert.html type="info" content="The send action is the only command action available through the SDK and is limited to LabOrder and Prescribe commands only." %}

### Example
```python
import json
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.v1.data import Staff

class Handler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PLAN_COMMAND__AVAILABLE_ACTIONS)
    def compute(self) -> list[Effect]:
        actions = self.context["actions"]
        user_id = self.context["user"]["staff"]

        # Filter actions based on user permissions
        try:
            staff = Staff.objects.get(id=user_id)

            # Example: Hide print action for specific user
            if staff.first_name == "Larry":
                filtered_actions = [
                    action for action in actions
                    if action["name"] != "print"
                ]
            else:
                filtered_actions = actions

        except Staff.DoesNotExist:
            # If staff not found, return original actions
            filtered_actions = actions

        return [Effect(
            type=EffectType.COMMAND_AVAILABLE_ACTIONS_RESULTS,
            payload=json.dumps(filtered_actions)
        )]

 ```

## Chaining Methods with a User-set UUID

A common use case is to originate and also commit a command in a single plugin action. However, attempting to commit a command without a `command_uuid` will throw an error. Because the `originate` method executes asynchronously, there is not currently a clean way to get the `command_uuid` back from the originate action and use it for the commit action in the same operation.

The solution is to set the UUID in the plugin -- using a valid Version 4 UUID -- and pass it through to both the originate and commit actions. This is accomplished by manually setting the `command_uuid` before calling the methods:

```python
from uuid import uuid4
from canvas_sdk.commands import DiagnoseCommand

def compute():
    note_uuid = '550e8400-e29b-41d4-a716-446655440000'

    diagnose_command = DiagnoseCommand(
        note_uuid=note_uuid,
        icd10_code='E11.9'
    )

    # To chain command effects, you must know what the command's id
    # is. To accomplish that, we set the id ourselves rather than
    # allow the database to assign one.
    diagnose_command.command_uuid = str(uuid4())

    # Now we can both originate and commit in a single operation
    return [diagnose_command.originate(), diagnose_command.commit()]
```

This pattern ensures that both the originate and commit operations use the same `command_uuid`, allowing them to be chained together reliably in a single plugin execution.

Command-specific details for each command class can be found below.

## AdjustPrescription

**Command-specific parameters**:

| Name           | Type     | Required | Description                          |
|:---------------|:---------|:---------|:-------------------------------------|
| `new_fdb_code` | _string_ | `true`   | The [FDB code](/sdk/utils/#fdb_code) of the new medication. |

Check the [Prescribe](#prescribe) command for the other parameters used in the Adjust Prescription command.

```python
from canvas_sdk.commands import AdjustPrescriptionCommand, PrescribeCommand
from canvas_sdk.commands.constants import ClinicalQuantity

AdjustPrescriptionCommand(
    fdb_code="172480",
    new_fdb_code="216092",
    icd10_codes=["R51"],
    sig="Take one tablet daily after meals",
    days_supply=30,
    quantity_to_dispense=30,
    type_to_dispense=ClinicalQuantity(
        representative_ndc="12843016128",
        ncpdp_quantity_qualifier_code="C48542"
    ),
    refills=3,
    substitutions=PrescribeCommand.Substitutions.ALLOWED,
    pharmacy="Main Street Pharmacy",
    prescriber_id="provider_123",
    supervising_provider_id="provider_456",
    note_to_pharmacist="Please verify patient's insurance before processing."
)
```

---

## Allergy

**Command-specific parameters**:

| Name               | Type            | Required | Description                                                                      |
|:-------------------|:----------------|:---------|:---------------------------------------------------------------------------------|
| `allergy`          | _Allergen_      | `false`  | Represents the allergen. See details in the Allergen type below.                 |
| `severity`         | _Severity enum_ | `false`  | The severity of the allergic reaction. Must be one of `AllergyCommand.Severity`. |
| `narrative`        | _string_        | `false`  | A narrative or free-text description of the allergy.                             |
| `approximate_date` | _datetime_      | `false`  | The approximate date the allergy was identified.                                 |

**Enums and Types**:

**`Allergen`**

| Attribute      | Type                | Description                                            |
|:---------------|:--------------------|:-------------------------------------------------------|
| `concept_id`   | _integer_           | The identifier for the allergen concept.               |
| `concept_type` | _AllergenType enum_ | The type of allergen. See `AllergenType` values below. |



| AllergenType     | Description                        |
|:-----------------|:-----------------------------------|
| `ALLERGEN_GROUP` | Represents a group of allergens.   |
| `MEDICATION`     | Represents a medication allergen.  |
| `INGREDIENT`     | Represents an ingredient allergen. |


| Severity   | Description                    |
|:-----------|:-------------------------------|
| `MILD`     | Indicates a mild reaction.     |
| `MODERATE` | Indicates a moderate reaction. |
| `SEVERE`   | Indicates a severe reaction.   |

**Example**:

```python
from canvas_sdk.commands.commands.allergy import AllergyCommand, AllergenType, Allergen
from datetime import date

allergy = AllergyCommand(
    note_uuid="rk786p",
    allergy=Allergen(concept_id=12345, concept_type=AllergenType.MEDICATION),
    severity=AllergyCommand.Severity.SEVERE,
    narrative="Severe rash and difficulty breathing after penicillin.",
    approximate_date=date(2023, 6, 15)
)
```

---

## Assess

**Command-specific parameters**:

| Name           | Type          | Required | Description                                                                |
|:---------------|:--------------|:---------|:---------------------------------------------------------------------------|
| `condition_id` | _string_      | `true`   | The externally exposable id of the condition being assessed.               |
| `background`   | _string_      | `false`  | Background information about the diagnosis.                                |
| `status`       | _Status enum_ | `false`  | The current status of the diagnosis. Must be one of `AssessCommand.Status` |
| `narrative`    | _string_      | `false`  | The narrative for the current assessment.                                  |

| `Status`     | Value          |
|:-------------|:---------------|
| IMPROVED     | "improved"     |
| STABLE       | "stable"       |
| DETERIORATED | "deteriorated" |

**Example**:

```python
from canvas_sdk.commands import AssessCommand

assess = AssessCommand(
    note_uuid='rk786p',
    condition_id='hu38rlo',
    background='started in 2012',
    status=AssessCommand.Status.STABLE,
    narrative='experiencing more pain lately'
)
```

---

## ChangeMedication

**Command-specific parameters**:

| Name            | Type     | Required | Description                                                        |
|:----------------|:---------|:---------|:-------------------------------------------------------------------|
| `medication_id` | _string_ | `true`   | Externally exposable id of the patient's medication being changed. |
| `sig`           | _string_ | `false`  | Administration details of the medication.                          |

**Example**:

```python
from canvas_sdk.commands.commands.change_medication import ChangeMedicationCommand

change_medication = ChangeMedicationCommand(
    note_uuid='rk786p',
    medication_id='2u309j',
    sig='two pills taken orally'
)
```

---

## CloseGoal

**Command-specific parameters**:

| Name                 | Type                     | Required | Description                                                                               |
|:---------------------|:-------------------------|:---------|:------------------------------------------------------------------------------------------|
| `goal_id`            | _int_                    | `true`   | The externally exposable ID of the goal being closed.                                     |
| `achievement_status` | _AchievementStatus enum_ | `false`  | The final achievement status of the goal. Must be one of `GoalCommand.AchievementStatus`. |
| `progress`           | _string_                 | `false`  | A narrative about the patient's progress toward the goal.                                 |

**Example**:

```python
from canvas_sdk.commands import CloseGoalCommand, GoalCommand

close_goal = CloseGoalCommand(
    note_uuid="rk786p",
    goal_id=12345,
    achievement_status=GoalCommand.AchievementStatus.ACHIEVED,
    progress="Patient has achieved the target weight goal of 150 lbs."
)
```

---

## Diagnose

**Command-specific parameters**:

| Name                        | Type       | Required | Description                                                |
|:----------------------------|:-----------|:---------|:-----------------------------------------------------------|
| `icd10_code`                | _string_   | `true`   | ICD-10 code of the condition being diagnosed.              |
| `background`                | _string_   | `false`  | Background information about the diagnosis.                |
| `approximate_date_of_onset` | _datetime_ | `false`  | The approximate date the condition began.                  |
| `today_assessment`          | _string_   | `false`  | The narrative for the initial assessment of the condition. |

**Example**:

```python
from canvas_sdk.commands import DiagnoseCommand
from datetime import datetime

diagnose = DiagnoseCommand(
    note_uuid='rk786p',
    icd10_code='M54.50',
    background='lifted heavy box',
    approximate_date_of_onset=datetime(2012, 1, 1),
    today_assessment='unable to sleep lately'
)
```

---

## FamilyHistory

**Command-specific parameters**:

| Name             | Type     | Required | Description                                           |
|:-----------------|:---------|:---------|:------------------------------------------------------|
| `family_history` | _string_ | `true`   | A description of the family history being documented. |
| `relative`       | _string_ | `false`  | A description of the relative (e.g., mother, uncle).  |
| `note`           | _string_ | `false`  | Additional notes or context about the family history. |

**Example**:

```python
from canvas_sdk.commands import FamilyHistoryCommand

family_history = FamilyHistoryCommand(
    note_uuid="rk786p",
    family_history="Diabetes Type 2",
    relative="Mother",
    note="Diagnosed at age 45"
)
```

---

## FollowUp

**Command-specific parameters**:

| Name             | Type                     | Required                  | Description                                                                                                                                                                                                                |
|:-----------------|:-------------------------|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `structured`     | _boolean_                | `false`                   | Whether the RFV is structured or not. Defaults to False.                                                                                                                                                                   |
| `requested_date` | _date_                   | `false`                   | The desired follow up date.                                                                                                                                                                                                |
| `note_type_id`   | _UUID (str)_             | `false`                   | The desired type of appointment.                                                                                                                                                                                           |
| `coding`         | _[Coding](#coding)_ or _UUID (str)_ | `true` if structured=True | The coding for the structured RFV. Either a full [Coding](#coding) object (with `code`, `system`, `display`) or a UUID string referencing a verified coding record. If a [Coding](#coding) is provided, it is validated against existing records |
| `comment`        | _string_                 | `false`                   | Additional commentary on the RFV.                                                                                                                                                                                          |

**Example**:

```python
from canvas_sdk.commands import FollowUpCommand
from datetime import date

structured = FollowUpCommand(
  note_uuid='rk786p',
  structured=True,
  requested_date=date(2025, 3, 2),
  note_type_id="kz986a",
  coding={'code': '', 'system': '', 'display': ''},
  comment='also wants to discuss treatment options'
)

# Example with a UUID string referencing a Coding record
structured2 = FollowUpCommand(
  note_uuid='rk786p',
  structured=True,
  requested_date=date(2025, 3, 2),
  note_type_id="kz986a",
  coding="e2b1e1e3-3f52-4a0a-bb3a-123456789abc",  # Must correspond to an existing coding record
  comment="Discuss treatment options"
)

unstructured = FollowUpCommand(
  note_uuid='rk786p',
  requested_date=date(2025, 3, 2),
  note_type_id="kz986a",
  comment='also wants to discuss treatment options'
)

```

---

## Goal

**Command-specific parameters**:

| Name                 | Type                     | Required | Description                                               |
|:---------------------|:-------------------------|:---------|:----------------------------------------------------------|
| `goal_statement`     | _string_                 | `true`   | Description of the goal.                                  |
| `start_date`         | _datetime_               | `false`  | The date the goal begins.                                 |
| `due_date`           | _datetime_               | `false`  | The date the goal is due.                                 |
| `achievement_status` | _AchievementStatus enum_ | `false`  | The current achievement status of the goal.               |
| `priority`           | _Priority enum_          | `false`  | The priority of the goal.                                 |
| `progress`           | _string_                 | `false`  | A narrative about the patient's progress toward the goal. |


| `AchievementStatus` | Value            |
|:--------------------|:-----------------|
| IN_PROGRESS         | "in-progress"    |
| IMPROVING           | "improving"      |
| WORSENING           | "worsening"      |
| NO_CHANGE           | "no-change"      |
| ACHIEVED            | "achieved"       |
| SUSTAINING          | "sustaining"     |
| NOT_ACHIEVED        | "not-achieved"   |
| NO_PROGRESS         | "no-progress"    |
| NOT_ATTAINABLE      | "not-attainable" |

| `Priority` | Value             |
|:-----------|:------------------|
| HIGH       | "high-priority"   |
| MEDIUM     | "medium-priority" |
| LOW        | "low-priority"    |

**Example**:

```python
from canvas_sdk.commands import GoalCommand
from datetime import datetime

goal = GoalCommand(
    note_uuid='rk786p',
    goal_statement='Eat more healthy vegetables.',
    start_date=datetime(2024, 1, 1),
    due_date=datetime(2024, 12, 31),
    achievement_status=GoalCommand.AchievementStatus.IN_PROGRESS,
    priority=GoalCommand.Priority.HIGH,
    progress='patient is frequenting local farmers market to find healthy options'
)
```

---

## HistoryOfPresentIllness

**Command-specific parameters**:

| Name        | Type     | Required | Description                                                |
|:------------|:---------|:---------|:-----------------------------------------------------------|
| `narrative` | _string_ | `true`   | The narrative of the patient's history of present illness. |

**Example**:

```python
from canvas_sdk.commands import HistoryOfPresentIllnessCommand

hpi = HistoryOfPresentIllnessCommand(
        note_uuid='rk786p',
        narrative='presents with chronic back pain and headaches'
    )
```

---


## ImagingOrder

**Command-specific parameters**:

| Name                    | Type              | Required | Description                                                                   |
|:------------------------|:------------------|:---------|:------------------------------------------------------------------------------|
| `image_code`            | _string_          | `true`   | Code identifier of the imaging order.                                         |
| `diagnosis_codes`       | _list[string]_    | `true`   | ICD-10 Diagnosis codes justifying the imaging order.                          |
| `priority`              | _Priority enum_   | `false`  | Priority of the imaging order. Must be one of `ImagingOrderCommand.Priority`. |
| `additional_details`    | _string_          | `false`  | Additional details or instructions related to the imaging order.              |
| `service_provider`      | _[ServiceProvider](#serviceprovider)_ | `true`   | Service provider of the imaging order.                                        |
| `comment`               | _string_          | `false`  | Additional comments.                                                          |
| `ordering_provider_key` | _string_          | `true`   | The key for the provider ordering the imaging.                                |
| `linked_items_urns`     | _list[string]_    | `false`  | List of URNs for items linked to the imaging order command.                   |

**Command-specific actions**:

| Action Name        | Available When       | Description                                                       |
|--------------------|----------------------|-------------------------------------------------------------------|
| `delegate_action`  | command is staged    | Delegates the order by creating a task.                           |
| `sign_action`      | command is staged    | Signs the order, transitioning it from staged to committed state. |
| `print_specialist` | command is committed | Prints the order using a specialist-focused template.             |
| `print_patient`    | command is committed | Prints the order using a patient-friendly template.               |
| `fax`              | command is committed | Transmits the order electronically via fax.                       |



**Enums and Types**:

**`Priority`**

| Priority  | Description                |
|:----------|:---------------------------|
| `ROUTINE` | Indicates a routine order. |
| `URGENT`  | Indicates un urgent order. |

**Example**:

```python
from canvas_sdk.commands import ImagingOrderCommand
from canvas_sdk.commands.constants import ServiceProvider

imaging_order = ImagingOrderCommand(
    note_uuid="rk786p",
    image_code="G0204",
    diagnosis_codes=["E119"],
    priority=ImagingOrderCommand.Priority.ROUTINE,
    comment="this is a comment",
    additional_details="more details",
    ordering_provider_key="pk3920p",
    service_provider=ServiceProvider(
      first_name="Clinic",
      last_name="Imaging",
      practice_name="Clinic Imaging",
      specialty="radiology",
      business_address="Street Address",
      business_phone="1234569874",
      business_fax="1234569874"
 ),
)
```

---

## ImmunizationStatement

**Command-specific parameters**:

| Name               | Type    | Required | Description                                                      |
|--------------------|---------|----------|------------------------------------------------------------------|
| `cpt_code`         | _string_| `true`   | The CPT code for the immunization procedure. Used with CVX code to search against ontologies server for validation. |
| `cvx_code`         | _string_| `true`   | The CVX code for the vaccine administered. Used with CPT code to search against ontologies server for validation. |
| `approximate_date` | _date_  | `false`  | The approximate date when the immunization was administered.     |
| `comments`         | _string_| `false`  | Additional comments about the immunization (max 255 characters). |

**Example**:

```python
from canvas_sdk.commands.commands.immunization_statement import ImmunizationStatementCommand
from datetime import date

immunization_statement = ImmunizationStatementCommand(
    cpt_code="90724",
    cvx_code="88",
    approximate_date=date(2024, 1, 15),
    comments="Patient received influenza vaccine"
)
```

---

## Instruct

**Command-specific parameters**:

| Name      | Type       | Required | Description                                                           |
|-----------|------------|----------|-----------------------------------------------------------------------|
| `coding`  | __[Coding](#coding)__ | `true`   | The SNOMED code or UNSTRUCTURED code that represents the instruction. |
| `comment` | _string_   | `false`  | Additional comments related to the instruction.                       |

**Example**:

```python
from canvas_sdk.commands import InstructCommand
from canvas_sdk.commands.constants import CodeSystems, Coding

# SNOMED code
InstructCommand(
    note_uuid='rk786p',
    coding=Coding(system=CodeSystems.SNOMED, code="65921008"),
    comment="To address mild dehydration symptoms"
)

# UNSTRUCTURED code
InstructCommand(
    note_uuid='rk786p',
    coding=Coding(system=CodeSystems.UNSTRUCTURED, code="Physical medicine neuromuscular training"),
)
```

---

## LabOrder

The `LabOrderCommand` is used to initiate a lab order through the Canvas system.
This command requires detailed information about the lab partner, the tests being ordered, and the provider placing the
order.
Built-in validations ensure that:

- The specified lab partner exists (whether provided by name or ID).
- The ordered tests are available for the chosen lab partner.

**Electronic ordering:** LabOrder commands support the `send()` method for electronic ordering of signed orders directly to lab partners. However, electronic ordering has additional requirements:

- Only lab partners with electronic ordering enabled support the `send()` method.
- The command must be committed/signed before it can be sent electronically.

**Command-specific parameters**:

| Name                    | Type           | Required | Description                                                                                                                                                      |
|-------------------------|----------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `lab_partner`           | _string_       | `true`   | The lab partner processing the order. Accepts either the lab partner’s name or its unique identifier (ID).                                                       |
| `tests_order_codes`     | _list[string]_ | `true`   | A list of codes or IDs for the tests being ordered. The system verifies that each provided value corresponds to an available test for the specified lab partner. |
| `ordering_provider_key` | _string_       | `false`  | The key for the provider ordering the tests.                                                                                                                     |
| `diagnosis_codes`       | _list[string]_ | `false`  | ICD-10 Diagnosis codes justifying the lab order.                                                                                                                 |
| `fasting_required`      | _boolean_      | `false`  | Indicates if fasting is required for the tests.                                                                                                                  |
| `comment`               | _string_       | `false`  | Additional comments related to the lab order.                                                                                                                    |

**Command-specific actions**:

| Action Name              | Available When       | Description                                                               |
|--------------------------|----------------------|---------------------------------------------------------------------------|
| `sign_send_action`       | command is staged    | Signs and immediately sends the order electronically to the lab partner.  |
| `send_action`            | command is staged    | Sends the order electronically to the chosen lab partner.                 |
| `sign_action`            | command is staged    | Signs the order, transitioning it from staged to committed state.         |
| `print_requisition_form` | command is committed | Prints the order using a requisition-focused template for lab submission. |
| `print_specimen_label`   | command is committed | Prints the template using a specimen-focused template.                    |
| `fax_requisition_form`   | command is committed | Transmits the order electronically via fax.                               |

**ABN Workflow Actions**

When the ABN (Advance Beneficiary Notice) workflow is enabled, additional actions become available:

| Action Name       | Available When    | Description                                                       |
|-------------------|-------------------|-------------------------------------------------------------------|
| `send_abn_signed` | command is staged | Sends the order electronically after ABN requirements are met.    |
| `make_changes`    | command is staged | Allows modifications to complete ABN requirements before sending. |

### Validations

- **Lab Partner Validation:**
  The system checks that the provided `lab_partner` (by name or ID) exists in the system. If no matching lab partner is
  found, a validation error is raised.

- **Tests Order Codes Validation:**
  Each test code or ID in `tests_order_codes` is verified against the tests available for the specified lab partner. If
  one or more tests cannot be found, the error will indicate which codes or IDs are missing.

**Example**:

```python
from canvas_sdk.commands import LabOrderCommand
from canvas_sdk.v1.data.lab import LabPartner, LabPartnerTest

partner = LabPartner.objects.first()
tests = [test.order_code for test in LabPartnerTest.objects.filter(lab_partner=partner)]

LabOrderCommand(
  lab_partner=str(partner.id),
  tests_order_codes=tests,
  ordering_provider_key="provider_key_123",
  diagnosis_codes=["E119"],
  fasting_required=True,
  comment="Patient should fast for 8 hours before the test."
)
```

---

## MedicalHistory

**Command-specific parameters**:

| Name                     | Type      | Required | Description                                                |
|--------------------------|-----------|----------|------------------------------------------------------------|
| `past_medical_history`   | _string_  | `true`   | A description of the past medical condition or history.    |
| `approximate_start_date` | _date_    | `false`  | Approximate start date of the condition.                   |
| `approximate_end_date`   | _date_    | `false`  | Approximate end date of the condition.                     |
| `show_on_condition_list` | _boolean_ | `false`  | Whether the condition should appear on the condition list. |
| `comments`               | _string_  | `false`  | Additional comments (max length: 1000 characters).         |

**Example**:

```python
from canvas_sdk.commands import MedicalHistoryCommand
from datetime import date

MedicalHistoryCommand(
    past_medical_history="Resistant Hypertension",
    approximate_start_date=date(2015, 1, 1),
    show_on_condition_list=True,
    comments="Controlled with medication."
)
```

---

## MedicationStatement

**Command-specific parameters**:

| Name       | Type     | Required | Description                               |
|:-----------|:---------|:---------|:------------------------------------------|
| `fdb_code` | _string_ | `true`   | The [FDB code](/sdk/utils/#fdb_code) of the medication.           |
| `sig`      | _string_ | `false`  | Administration details of the medication. |

**Example**:

```python
from canvas_sdk.commands import MedicationStatementCommand

medication_statement = MedicationStatementCommand(
    note_uuid='rk786p',
    fdb_code='198698',
    sig='two pills taken orally'
)
```

---

## SurgicalHistory

**Command-specific parameters**:

| Name                    | Type     | Required | Description                                        |
|-------------------------|----------|----------|----------------------------------------------------|
| `past_surgical_history` | _string_ | `true`   | A description of the past surgical procedure.      |
| `approximate_date`      | _date_   | `false`  | Approximate date of the surgery.                   |
| `comment`               | _string_ | `false`  | Additional comments (max length: 1000 characters). |

**Example**:

```python
from canvas_sdk.commands import PastSurgicalHistoryCommand
from datetime import date

PastSurgicalHistoryCommand(
    past_surgical_history="Appendectomy",
    approximate_date=date(2008, 6, 15),
    comment="No complications reported."
)
```

---

## Perform

**Command-specific parameters**:

| Name       | Type     | Required | Description                                          |
|------------|----------|----------|------------------------------------------------------|
| `cpt_code` | _string_ | `true`   | The CPT code of the procedure or action performed.   |
| `notes`    | _string_ | `false`  | Additional notes related to the performed procedure. |

**Example**:

```python
from canvas_sdk.commands import PerformCommand

PerformCommand(
    cpt_code="99213",
    notes="Patient presented with a common cold."
)
```

---

## Plan

**Command-specific parameters**:

| Name        | Type     | Required | Description                          |
|:------------|:---------|:---------|:-------------------------------------|
| `narrative` | _string_ | `true`   | The narrative of the patient's plan. |

**Example**:

```python
from canvas_sdk.commands import PlanCommand

plan = PlanCommand(
    note_uuid='rk786p',
    narrative='will return in 2 weeks to check on pain management'
)
```

---

## Prescribe

**Electronic prescribing:** Prescribe commands support the `send()` method for electronic transmission of signed prescriptions. However, electronic prescribing has additional validations:

- A pharmacy must be specified on the command before it can be sent.
- The command must be committed/signed before it can be sent electronically.


**Command-specific parameters**:

| Name                        | Type                          | Required | Description                                                         |
|-----------------------------|-------------------------------|----------|---------------------------------------------------------------------|
| `fdb_code`                  | _string_                      | `false`* | The [FDB code](/sdk/utils/#fdb_code) of the medication.             |
| `compound_medication_id`    | _string_                      | `false`* | The ID of an existing compound medication to prescribe.             |
| `compound_medication_data`  | `CompoundMedicationData`      | `false`* | Data for creating a new compound medication inline.                 |
| `icd10_codes`               | _list[string]_                | `false`  | List of ICD-10 codes (maximum 2) associated with the prescription.  |
| `sig`                       | _string_                      | `true`   | Administration instructions/details of the medication.              |
| `days_supply`               | _integer_                     | `false`  | Number of days the prescription is intended to cover.               |
| `quantity_to_dispense`      | _Decimal \| float \| integer_ | `true`   | The amount of medication to dispense.                               |
| `type_to_dispense`          | _[ClinicalQuantity](#clinicalquantity)_            | `true`** | Information about the form or unit of the medication to dispense.   |
| `refills`                   | _integer_                     | `true`   | Number of refills allowed for the prescription.                     |
| `substitutions`             | _Substitutions Enum_          | `true`   | Specifies whether substitutions (e.g., generic drugs) are allowed.  |
| `pharmacy`                  | _string_                      | `false`  | The NCPDP ID of the pharmacy where the prescription should be sent. |
| `prescriber_id`             | _string_                      | `true`   | The key of the prescriber.                                          |
| `supervising_provider_id`   | _string_                      | `false`   | The key of the supervising provider of the prescriber.               |
| `note_to_pharmacist`        | _string_                      | `false`  | Additional notes or instructions for the pharmacist.                |

*Must provide exactly one of: fdb_code, compound_medication_id, or compound_medication_data

**[ClinicalQuantity](#clinicalquantity) is only required when `fdb_code` is provided. It is optional for compound medications.

**Command-specific actions**:

| Action Name        | Available When       | Description                                                              |
|--------------------|----------------------|--------------------------------------------------------------------------|
| `sign_send_action` | command is in review | Signs and immediately sends the prescription electronically.             |
| `sign_action`      | command is in review | Signs the prescription, transitioning it from staged to committed state. |
| `print_action`     | command is in review | Prints and commits the command.                                          |
| `make_changes`     | command is in review | Allow users to revert the command to staged state and make changes.      |
| `send_action`      | command is committed | Sends the prescription electronically.                                   |

**Enums and Types**

| Substitutions | Value           | Description                                      |
|---------------|-----------------|--------------------------------------------------|
| `ALLOWED`     | `"allowed"`     | Generic or substitute medications are permitted. |
| `NOT_ALLOWED` | `"not_allowed"` | Only the prescribed brand is allowed.            |


**CompoundMedicationData**:
Data for creating a compound medication inline within a prescription.

| Field Name                 | Type     | Description                                               | Required |
|----------------------------|----------|-----------------------------------------------------------|----------|
| `formulation`              | _string_ | The compound medication formulation (max 105 characters)  | `true`   |
| `potency_unit_code`        | _string_ | The unit of measurement for the medication                | `true`   |
| `controlled_substance`     | _string_ | The controlled substance schedule                         | `true`   |
| `controlled_substance_ndc` | _string_ | NDC for controlled substances (dashes removed)            | `false`* |
| `active`                   | _bool_   | Whether the compound medication is active (default: true) | `false`  |


*Required when controlled_substance is not "N" (None)


**Examples**

***Option 1: Standard Prescription (FDB Code)***
```python
from canvas_sdk.commands.constants import ClinicalQuantity
from canvas_sdk.commands import PrescribeCommand

prescription = PrescribeCommand(
    fdb_code="216092",
    icd10_codes=["R51"],
    sig="Take one tablet daily after meals",
    days_supply=30,
    quantity_to_dispense=30,
    type_to_dispense=ClinicalQuantity(
        representative_ndc="12843016128",
        ncpdp_quantity_qualifier_code="C48542"
    ),
    refills=3,
    substitutions=PrescribeCommand.Substitutions.ALLOWED,
    pharmacy="Main Street Pharmacy",
    prescriber_id="provider_123",
    supervising_provider_id='provider_456',
    note_to_pharmacist="Please verify patient's insurance before processing."
)
```

***Option 2: Existing Compound Medication (by ID)***
```python
from canvas_sdk.commands.constants import ClinicalQuantity
from canvas_sdk.commands import PrescribeCommand

from canvas_sdk.v1.data.compound_medication import CompoundMedication as CompoundMedicationModel

# Get an existing compound medication (let's assume it exists in the database)
compound_med = CompoundMedicationModel.objects.filter(
    active=True,
    formulation="Testosterone 200mg/mL in Grapeseed Oil"
).first()

prescription = PrescribeCommand(
    compound_medication_id=str(compound_med.id),
    icd10_codes=["R51"],
    sig="Take one tablet daily after meals",
    days_supply=30,
    quantity_to_dispense=30,
    type_to_dispense=ClinicalQuantity(
        representative_ndc="12843016128",
        ncpdp_quantity_qualifier_code="C48542"
    ),
    refills=3,
    substitutions=PrescribeCommand.Substitutions.ALLOWED,
    pharmacy="Main Street Pharmacy",
    prescriber_id="provider_123",
    supervising_provider_id='provider_456',
    note_to_pharmacist="Please verify patient's insurance before processing."
)
```

***Option 3: Create New Compound Medication Inline***
```python
from canvas_sdk.commands.constants import ClinicalQuantity
from canvas_sdk.commands.commands.prescribe import PrescribeCommand, CompoundMedicationData

from canvas_sdk.v1.data.compound_medication import CompoundMedication

compound_medication_data = CompoundMedicationData(
    formulation="Testosterone 200mg/mL in Grapeseed Oil",
    potency_unit_code=CompoundMedication.PotencyUnits.GRAM,
    controlled_substance=CompoundMedication.ControlledSubstanceOptions.SCHEDULE_III,
    controlled_substance_ndc="12345678901",
    active=True,
)

prescription = PrescribeCommand(
    compound_medication_data=compound_medication_data,
    icd10_codes=["M79.3"],
    sig="Apply thin layer to affected area twice daily",
    days_supply=30,
    quantity_to_dispense=30,
    type_to_dispense=ClinicalQuantity(
        representative_ndc="12843016128",
        ncpdp_quantity_qualifier_code="C48542"
    ),
    refills=3,
    substitutions=PrescribeCommand.Substitutions.ALLOWED,
    pharmacy="Main Street Pharmacy",
    prescriber_id="provider_123",
    supervising_provider_id='provider_456',
    note_to_pharmacist="Please verify patient's insurance before processing."
)
```

**Validation Notes**

* Medication Type Validation: Exactly one of fdb_code, compound_medication_id, or compound_medication_data must be provided
* Compound Medication ID: When using compound_medication_id, the system validates that the compound medication exists
* Compound Medication Data: When using compound_medication_data:
  * All required fields in the dataclass must be provided
  * If controlled substance is not "N" (None), then controlled_substance_ndc is required
  * The formulation is limited to 105 characters
  * Any dashes in the NDC are automatically removed
  * Before creating a new compound medication, the system checks if a compound with the same formulation and potency unit code already exists. If it does, it reuses the existing compound medication instead of creating a new one.
* Potency Unit and Controlled Substance Values: Must use valid enum values from PotencyUnit and ControlledSubstanceSchedule

---

## PhysicalExam

**Command-specific parameters**:

| Name               | Type     | Required | Description                                                                     |
|:-------------------|:---------|:---------|:--------------------------------------------------------------------------------|
| `questionnaire_id` | _string_ | `true`   | The externally exposable id of the questionnaire being answered by the patient. |
| `result`           | _string_ | `false`  | A summary of the result of the patient's answers.                               |

### Toggle Questions Feature

The PhysicalExamCommand includes special functionality for toggling questions on/off.
When working with a PhysicalExam Command, the following methods are available:

**Methods**:

| Method                      | Parameters                                 | Returns   | Description                                                |
|:----------------------------|:-------------------------------------------|:----------|:-----------------------------------------------------------|
| `is_question_enabled`       | `question_id: str` or `int`                | `bool`    | Check if a specific question is enabled (not skipped).     |
| `set_question_enabled`      | `question_id: str` or `int, enabled: bool` | `None`    | Enable or disable a specific question.                     |
| `question_toggles`          | _property_                                 | `dict`    | Get all current toggle states (question_id → enabled).     |

**Example - Working with Existing Commands**:

A common use case is retrieving existing PhysicalExam commands from a note and modifying their toggle states. Here's how to work with the Canvas SDK data objects:

```python
from canvas_sdk.commands import PhysicalExamCommand
from canvas_sdk.v1.data import Command, Note
from logger import log

# Get existing physical exam commands from a note
note = Note.objects.get(id="ff287601-fff4-46c4-b21f-04760e88adf1")
physical_exam_commands = Command.objects.filter(
    note=note,
    schema_key="exam"  # Physical exam commands have schema_key "exam"
).all()

effects = []
for command in physical_exam_commands:
    # The command.data contains the question responses and skip states
    # Example structure of command.data:
    # {
    #     "questionnaire": {"value": "83d93454-25a9-404d-83a5-e0ed2ec3af00"},
    #     "question-12": "70",  # Body length response
    #     "question-13": None,   # Head circumference (no response)
    #     "skip-12": True,   # Body length is enabled (counterintuitive: skip=True means enabled)
    #     "skip-13": False,  # Head circumference is disabled
    # }

    # Create a PhysicalExamCommand instance from the existing command
    exam = PhysicalExamCommand(command_uuid=str(command.id))

    # The exam.questions property gives you access to all questions with their IDs
    log.info(f"Processing Physical Exam Command: {exam.command_uuid}")
    for question in exam.questions:
        # Each question object has an 'id' property with the question ID
        question_id = question.id
        if exam.is_question_enabled(question_id):
            log.info(f"Question {question_id} is enabled")

            # Check if there's a response in the command data
            question_key = f"question-{question_id}"
            if question_key in command.data:
                response = command.data[question_key]
                if response:
                    log.info(f"Response: {response}")

    # Example: Enable all questions that have responses, disable those without
    for question in exam.questions:
        question_id = question.id
        question_key = f"question-{question_id}"
        # Check if question has a response in command.data
        has_response = question_key in command.data and command.data[question_key]

        if has_response:
            exam.set_question_enabled(question_id, True)
        else:
            # Optionally disable questions without responses
            exam.set_question_enabled(question_id, False)

    effects.append(exam.edit())
```


**Example - Creating a New Physical Exam**:

```python
from canvas_sdk.commands import PhysicalExamCommand

# Create a new physical exam
exam = PhysicalExamCommand(
  note_uuid='a229456f-c10d-4f85-a04e-e8675d4e56dd',
  questionnaire_id='83d93454-25a9-404d-83a5-e0ed2ec3af00',
)

questions = exam.questions  # Retrieve the list of questions
# Returns: [
#               Question(
#                       self.name='question-12',
#                       self.label='Body length (in)',
#                       self.type='TXT',
#                       self.options=[ResponseOption(self.dbid=38, self.name='Body length (in)', self.code='8306-3', self.value='')],
#                       self.response=None
#               ),
#               Question(
#                       self.name='question-13',
#                       self.label='Head circumference (cm)',
#                       self.type='TXT', self.options=[ResponseOption(self.dbid=39, self.name='Head circumference (cm)', self.code='8287-5', self.value='')],
#                       self.response=None
#               )

# Check if a question is enabled
if exam.is_question_enabled("12"):
  print("Body length question is enabled.")

# Disable irrelevant questions
exam.set_question_enabled("13", False)

# Get all toggle states
states = exam.question_toggles
# Returns: {"12": True, "13": False, "14": True, ...}, where keys are question IDs and values are enabled states.

# Working with existing exam - toggle states are preserved
existing_exam = PhysicalExamCommand(command_uuid='existing-exam-uuid')
# All previously set toggle states are automatically loaded
```

**Note:** The PhysicalExamCommand is a subclass of the QuestionnaireCommand, so it supports all the questionnaire features (including response recording, question mapping, etc.). For detailed information on these features, please refer to the [Questionnaire Command Documentation](#questionnaire).

---


## Questionnaire

### Overview

The `QuestionnaireCommand` is used to present a questionnaire to a patient and commit their responses to an interview. It requires the ID of the questionnaire

**Automatic Questionnaire ID Loading**: When instantiating a QuestionnaireCommand with an existing `command_uuid`, the questionnaire_id will be automatically loaded from the database if not explicitly provided. This means you don't need to specify the questionnaire_id when working with existing commands.

In addition to the basic parameters, this command supports a dynamic response interface. Once instantiated, you can retrieve the list of questions via the `questions` property, and then record responses for each question using the question object's `add_response()` method. Each question type enforces its expected response format:

- **Text questions (TYPE_TEXT):** Accept a keyword argument `text` (a string).
- **Integer questions (TYPE_INTEGER):** Accept a keyword argument `integer` (an integer or a value convertible to an integer).
- **Radio questions (TYPE_RADIO):** Accept a keyword argument `option` (a `ResponseOption` instance); only one option may be selected.
- **Checkbox questions (TYPE_CHECKBOX):** Accept a keyword argument `option` (a `ResponseOption` instance) along with an optional boolean `selected` (defaulting to True) and an optional string `comment`. Multiple responses can be recorded.


**Command-specific parameters**:

| Name               | Type     | Required | Description                                                                     |
|:-------------------|:---------|:---------|:--------------------------------------------------------------------------------|
| `questionnaire_id` | _string_ | `true`   | The externally exposable id of the questionnaire being answered by the patient. |
| `result`           | _string_ | `false`  | A summary of the result of the patient's answers.                               |

**Example**:

```python
from canvas_sdk.commands import QuestionnaireCommand

questionnaire = QuestionnaireCommand(
    note_uuid='rk786p',
    questionnaire_id='g73hd9',
    result='The patient is feeling average today.'
)
```

### Usage Example

Below is an example that demonstrates how to instantiate a `QuestionnaireCommand`, retrieve the questions, and add responses to them based on their type:

```python
import uuid
from canvas_sdk.commands.commands.questionnaire import QuestionnaireCommand
from canvas_sdk.commands.commands.questionnaire.question import ResponseOption
from canvas_sdk.effects import Effect
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Note, Questionnaire

class Protocol(BaseHandler):

    def compute(self) -> list[Effect]:
      q = Questionnaire.objects.filter(name="Exercise").first()
      note = Note.objects.last()
      # Create a QuestionnaireCommand instance.
      command = QuestionnaireCommand(questionnaire_id=str(q.id))
      command.note_uuid = str(note.id)
      command.command_uuid = str(uuid.uuid4())

      # Alternatively you can just retrieve an existing questionnaire command, and only return an `edit` effect.

      # Retrieve the list of questions.
      questions = command.questions

      # Record responses for each question.
      for question in questions:
          if question.type == ResponseOption.TYPE_TEXT:
              # For text questions, pass a 'text' keyword argument.
              question.add_response(text=f"Thanks for all the fish")
          elif question.type == ResponseOption.TYPE_INTEGER:
              # For integer questions, pass an 'integer' keyword argument.
              question.add_response(integer=42)
          elif question.type == ResponseOption.TYPE_RADIO:
              # For radio questions, pass an 'option' keyword argument (a ResponseOption instance).
              first_option = question.options[0]
              question.add_response(option=first_option)
          elif question.type == ResponseOption.TYPE_CHECKBOX:
              # For checkbox questions, add responses with option, selected flag, and optionally a comment.
              first_option = question.options[0]
              last_option = question.options[-1]
              question.add_response(option=first_option, selected=True, comment="Don't panic")
              question.add_response(option=last_option, selected=True)

      # Because we're directly setting a command_uuid, we can return both originate and edit.
      return [command.originate(), command.edit()]
```

### Explanation

- **Retrieving Questions:**
  The `questions` property returns a list of question objects created from the questionnaire's data.


- **Recording Responses:**
  Each question object provides an `add_response()` method that enforces the correct response format:
  - For **TextQuestion**, you must pass a `text` parameter.
  - For **IntegerQuestion**, you must pass an `integer` parameter.
  - For **RadioQuestion**, you must pass an `option` parameter (a `ResponseOption` instance) that corresponds to one of the allowed options.
  - For **CheckboxQuestion**, you must pass an `option` parameter along with an optional `selected` flag (defaulting to True) and an optional `comment`. Multiple responses can be recorded for checkbox questions.
  - **Note for Checkboxes:** Only the responses explicitly provided in the command payload will be updated in the UI. If a checkbox response is already selected and is not sent as unselected in the payload, its state remains unchanged.


 - **Creating and Editing:**
   When creating a new questionnaire command, you must explicitly set a unique `command_uuid`. Providing this UUID enables you to originate the command within the note and then subsequently edit it with detailed responses in the same protocol execution.

 - This approach is necessary because given the dynamic nature of the questionnaire command, the initial creation (origination) only includes the questionnaire ID. Once the command has been originated, you can immediately follow up with an edit to populate it with the patient's responses.
 - If you are looking to insert a committed questionnaire command, you'll need to return three effects:
   - An `.originate()` to insert the command and select the questionnaire
   - An `.edit()` to populate the responses
   - A `.commit()` to commit the command

---

## ReasonForVisit

**Command-specific parameters**:

| Name         | Type                     | Required                  | Description                                                                                                                                                                                                                |
|:-------------|:-------------------------|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `structured` | _boolean_                | `false`                   | Whether the RFV is structured or not. Defaults to False.                                                                                                                                                                   |
| `coding`     | _[Coding](#coding)_ or _UUID (str)_ | `true` if structured=True | The coding for the structured RFV. Either a full [Coding](#coding) object (with `code`, `system`, `display`) or a UUID string referencing a verified coding record. If a [Coding](#coding) is provided, it is validated against existing records |
| `comment`    | _string_                 | `false`                   | Additional commentary on the RFV.                                                                                                                                                                                          |

**Example**:

```python
from canvas_sdk.commands import ReasonForVisitCommand

structured_rfv = ReasonForVisitCommand(
  note_uuid='rk786p',
  structured=True,
  coding={'code': '', 'system': '', 'display': ''},
  comment='also wants to discuss treatment options'
)

# Example with a UUID string referencing a Coding record
structured_rfv2 = ReasonForVisitCommand(
  note_uuid='rk786p',
  structured=True,
  coding="e2b1e1e3-3f52-4a0a-bb3a-123456789abc",  # Must correspond to an existing coding record
  comment="Discuss treatment options"
)

unstructured_rfv = ReasonForVisitCommand(
  note_uuid='rk786p',
  comment='also wants to discuss treatment options'
)
```

## Refer

**Command-specific parameters**:

| Name                  | Type                    | Required | Description                                                                                  |
|:----------------------|:------------------------|:---------|:---------------------------------------------------------------------------------------------|
| `service_provider`    | _[ServiceProvider](#serviceprovider)_       | `true`   | The service provider associated with the referral command.                                   |
| `diagnosis_codes`     | _list[string]_          | `true`   | A list of relevant ICD-10 Diagnosis.                                                         |
| `clinical_question`   | _ClinicalQuestion enum_ | `true`   | The clinical question prompting the referral. Must be one of `ReferCommand.ClinicalQuestion` |
| `priority`            | _Priority enum_         | `false`  | Priority of the imaging order. Must be one of `ReferCommand.Priority`.                       |
| `notes_to_specialist` | _string_                | `true`   | Notes or additional information directed to the specialist.                                  |
| `include_visit_note`  | _boolean_               | `false`  | Flag indicating whether the visit note should be included in the referral.                   |
| `comment`             | _string_                | `false`  | An optional comment providing further details about the referral.                            |
| `linked_items_urns`   | _list[string]_          | `false`  | List of URNs for items linked to the referral command.                                       |

**Command-specific actions**:

| Action Name        | Available When       | Description                                                       |
|--------------------|----------------------|-------------------------------------------------------------------|
| `delegate_action`  | command is staged    | Delegates the order by creating a task.                           |
| `sign_action`      | command is staged    | Signs the order, transitioning it from staged to committed state. |
| `print_specialist` | command is committed | Prints the order using a specialist-focused template.             |
| `print_patient`    | command is committed | Prints the order using a patient-friendly template.               |
| `fax`              | command is committed | Transmits the order electronically via fax.                       |

**Enums and Types**:

**`Priority`**

| Priority  | Description                |
|:----------|:---------------------------|
| `ROUTINE` | Indicates a routine order. |
| `URGENT`  | Indicates un urgent order. |

**`ClinicalQuestion`**

| Clinical Question                  | Description                            |
|------------------------------------|----------------------------------------|
| COGNITIVE_ASSISTANCE               | Cognitive Assistance (Advice/Guidance) |
| ASSISTANCE_WITH_ONGOING_MANAGEMENT | Assistance with Ongoing Management     |
| SPECIALIZED_INTERVENTION           | Specialized intervention               |
| DIAGNOSTIC_UNCERTAINTY             | Diagnostic Uncertainty                 |


**Example**:

```python
from canvas_sdk.commands import ReferCommand
from canvas_sdk.commands.constants import ServiceProvider

refer_command = ReferCommand(
    note_uuid="rk786p",
    diagnosis_codes=["E119"],
    priority=ReferCommand.Priority.ROUTINE,
    clinical_question=ReferCommand.ClinicalQuestion.DIAGNOSTIC_UNCERTAINTY,
    comment="this is a comment",
    notes_to_specialist="This is a note to specialist",
    include_visit_note=True,
    service_provider=ServiceProvider(
      first_name="Clinic",
      last_name="Acupuncture",
      practice_name="Clinic Acupuncture",
      specialty="Acupuncture",
      business_address="Street Address",
      business_phone="1234569874",
      business_fax="1234569874"
 ),
)
```

---

## Refill

**Command-specific parameters**:

Check the [Prescribe](#prescribe) command for the parameters used in the Refill command.

**Example**:

```python
from canvas_sdk.commands import RefillCommand, PrescribeCommand
from canvas_sdk.commands.constants import ClinicalQuantity

RefillCommand(
    fdb_code="216092",
    icd10_codes=["R51"],
    sig="Take one tablet daily after meals",
    days_supply=30,
    quantity_to_dispense=30,
    type_to_dispense=ClinicalQuantity(
        representative_ndc="12843016128",
        ncpdp_quantity_qualifier_code="C48542"
    ),
    refills=3,
    substitutions=PrescribeCommand.Substitutions.ALLOWED,
    pharmacy="Main Street Pharmacy",
    prescriber_id="provider_123",
    supervising_provider_id="provider_456",
    note_to_pharmacist="Please verify patient's insurance before processing."
)
```

---

## RemoveAllergy

**Command-specific parameters**:

| Name         | Type     | Required | Description                                      |
|--------------|----------|----------|--------------------------------------------------|
| `allergy_id` | _string_ | `true`   | The external ID of the allergy to remove.        |
| `narrative`  | _string_ | `false`  | Additional context or narrative for the removal. |

**Example**:

```python
from canvas_sdk.commands import RemoveAllergyCommand

RemoveAllergyCommand(
    allergy_id="123",
    narrative="Allergy no longer applies after reassessment."
)
```

---

## Resolve Condition

**Command-specific parameters**:

| Name                     | Type      | Required | Description                                                                |
|--------------------------|-----------|----------|----------------------------------------------------------------------------|
| `condition_id`           | _string_  | `true`   | The externally exposable id of the condition being resolved.               |
| `show_in_condition_list` | _boolean_ | `false`  | Determines whether the condition remains visible in patient chart summary. |
| `rationale`              | _string_  | `false`  | Additional context.                                                        |

```python
from canvas_sdk.commands.commands.resolve_condition import ResolveConditionCommand
from canvas_sdk.v1.data import Condition

patient_id = '<a patient ID from your instance>'

patient_condition = Condition.objects.for_patient(patient_id).committed().active().first()

ResolveConditionCommand(
   condition_id=patient_condition.id,
   show_in_condition_list=True,
   rationale="Additional notes.",
   note_uuid="rk786p",
)
```

---

## Review of Systems

**Command-specific parameters**:

| Name               | Type     | Required | Description                                                                     |
|:-------------------|:---------|:---------|:--------------------------------------------------------------------------------|
| `questionnaire_id` | _string_ | `true`   | The externally exposable id of the questionnaire being answered by the patient. |
| `result`           | _string_ | `false`  | A summary of the result of the patient's answers.                               |


### Toggle Questions Feature

The ReviewOfSystemsCommand includes the same toggle functionality as PhysicalExamCommand,
allowing practitioners to enable or disable specific system review questions based on patient relevance.
You can find an extra example of this functionality on the [Physical Exam Command Documentation](#physicalexam).


**Methods**:

| Method                      | Parameters                                 | Returns   | Description                                                |
|:----------------------------|:-------------------------------------------|:----------|:-----------------------------------------------------------|
| `is_question_enabled`       | `question_id: str` or `int`                | `bool`    | Check if a specific question is enabled (not skipped).     |
| `set_question_enabled`      | `question_id: str` or `int, enabled: bool` | `None`    | Enable or disable a specific question.                     |
| `question_toggles`          | _property_                                 | `dict`    | Get all current toggle states (question_id → enabled).     |

**Example**:

```python
from canvas_sdk.commands import ReviewOfSystemsCommand

# Create a new review of systems
ros = ReviewOfSystemsCommand(
  note_uuid='8a18931a-acd9-474b-9070-ccd6fd472313',
  questionnaire_id='ed92577b-a023-4370-bc85-2b57e8afc4d8',
)

questions = ros.questions  # Retrieve the list of questions
# Returns: [
#               Question(
#                       self.name='question-14',
#                       self.label='Recurrent fever or chills',
#                       self.type='TXT',
#                       self.options=[]],
#                       self.response=None
#               ),
#               Question(
#                       self.name='question-25',
#                       self.label='Other',
#                       self.type='TXT', self.options=[],
#                       self.response=None
#               )

# Check if a question is enabled
if ros.is_question_enabled("14"):
  print("Recurrent fever or chills question is enabled.")

# Disable irrelevant questions
ros.set_question_enabled("25", False)

# Get all toggle states
states = ros.question_toggles
# Returns: {"14": True, "25": False, "26": True, ...}, where keys are question IDs and values are enabled states.

# Working with existing ros - toggle states are preserved
existing_ros = ReviewOfSystemsCommand(command_uuid='existing-exam-uuid')
# All previously set toggle states are automatically loaded
```

**Note:** The ReviewOfSystemsCommand is a subclass of the QuestionnaireCommand, so it supports all the questionnaire features (including response recording, question mapping, etc.). For detailed information on these features, please refer to the [Questionnaire Command Documentation](#questionnaire).

---


## StopMedication

**Command-specific parameters**:

| Name            | Type     | Required | Description                                                        |
|:----------------|:---------|:---------|:-------------------------------------------------------------------|
| `medication_id` | _string_ | `true`   | Externally exposable id of the patient's medication being stopped. |
| `rationale`     | _string_ | `false`  | The reason for stopping the medication.                            |

**Example**:

```python
from canvas_sdk.commands import StopMedicationCommand

stop_medication = StopMedicationCommand(
    note_uuid='rk786p',
    medication_id='2u309j',
    rationale='In remission'
)
```

---

## StructuredAssessment

**Command-specific parameters**:

| Name               | Type     | Required | Description                                                                     |
|:-------------------|:---------|:---------|:--------------------------------------------------------------------------------|
| `questionnaire_id` | _string_ | `true`   | The externally exposable id of the questionnaire being answered by the patient. |
| `result`           | _string_ | `false`  | A summary of the result of the patient's answers.                               |

**Example**:

```python
from canvas_sdk.commands import StructuredAssessmentCommand

questionnaire = StructuredAssessmentCommand(
    note_uuid='rk786p',
    questionnaire_id='g73hd9',
    result='The patient is feeling average today.'
)
```

**Note:** The StructuredAssessmentCommand is a subclass of the QuestionnaireCommand, so it supports all the questionnaire features (including response recording, question mapping, etc.). For detailed information on these features, please refer to the [Questionnaire Command Documentation](#questionnaire).

---

## Task

**Command-specific parameters**:

| Name                | Type           | Required | Description                                         |
|---------------------|----------------|----------|-----------------------------------------------------|
| `title`             | _string_       | `true`   | The title or summary of the task.                   |
| `assign_to`         | _TaskAssigner_ | `true`   | Specifies the assignee (role, team, or individual). |
| `due_date`          | _date_         | `false`  | Due date for completing the task.                   |
| `comment`           | _string_       | `false`  | Additional comments or notes about the task.        |
| `labels`            | _list[string]_ | `false`  | Labels associated with the task.                    |
| `linked_items_urns` | _list[string]_ | `false`  | URNs for items linked to the task.                  |

**Enums and Types**:

**TaskAssigner Type**:

| Key  | Type           | Required | Description                                |
|------|----------------|----------|--------------------------------------------|
| `to` | _AssigneeType_ | `true`   | Type of assignee (e.g., role, team, etc.). |
| `id` | _integer_      | `false`  | Identifier of the specific assignee.       |

| AssigneeType | Value          | Description                               |
|--------------|----------------|-------------------------------------------|
| `ROLE`       | `"role"`       | Task assigned to a specific role.         |
| `TEAM`       | `"team"`       | Task assigned to a specific team.         |
| `UNASSIGNED` | `"unassigned"` | Task is unassigned.                       |
| `STAFF`      | `"staff"`      | Task assigned to a specific staff member. |


**Example**:

```python
from canvas_sdk.commands import TaskCommand
from canvas_sdk.commands.commands.task import TaskAssigner, AssigneeType
from datetime import date

TaskCommand(
    title="Follow-up appointment scheduling",
    assign_to=TaskAssigner(to=AssigneeType.STAFF, id=123),
    due_date=date(2024, 12, 15),
    comment="Ensure the patient schedules a follow-up within 30 days.",
    labels=["Urgent"],
    linked_items_urns=["urn:task:123", "urn:note:456"]
)
```

---

## UpdateDiagnosis

**Command-specific parameters**:

| Name                 | Type     | Required | Description                                                       |
|----------------------|----------|----------|-------------------------------------------------------------------|
| `condition_code`     | _string_ | `true`   | The ICD-10 code of the existing diagnosis to update.              |
| `new_condition_code` | _string_ | `true`   | The new condition ICD-10 code to replace the existing diagnosis.  |
| `background`         | _string_ | `false`  | Background information or notes related to the updated diagnosis. |
| `narrative`          | _string_ | `false`  | A narrative or explanation about the update.                      |

---

**Example**

```python
from canvas_sdk.commands import UpdateDiagnosisCommand

UpdateDiagnosisCommand(
    condition_code="E119",
    new_condition_code="E109",
    background="Patient previously diagnosed with diabetes type 2; now updated to diabetes type 1.",
    narrative="Updating condition based on recent clinical findings."
)
```

---

## UpdateGoal

**Command-specific parameters**:

| Name                 | Type                     | Required | Description                                               |
|:---------------------|:-------------------------|:---------|:----------------------------------------------------------|
| `goal_id`            | _string_                 | `true`   | Externally exposable id of the goal being updated.        |
| `due_date`           | _datetime_               | `false`  | The date the goal is due.                                 |
| `achievement_status` | _AchievementStatus enum_ | `false`  | The current achievement status of the goal.               |
| `priority`           | _Priority enum_          | `false`  | The priority of the goal.                                 |
| `progress`           | _string_                 | `false`  | A narrative about the patient's progress toward the goal. |

| `AchievementStatus` |                  |
|:--------------------|:-----------------|
| IN_PROGRESS         | "in-progress"    |
| IMPROVING           | "improving"      |
| WORSENING           | "worsening"      |
| NO_CHANGE           | "no-change"      |
| ACHIEVED            | "achieved"       |
| SUSTAINING          | "sustaining"     |
| NOT_ACHIEVED        | "not-achieved"   |
| NO_PROGRESS         | "no-progress"    |
| NOT_ATTAINABLE      | "not-attainable" |

| `Priority` |                   |
|:-----------|:------------------|
| HIGH       | "high-priority"   |
| MEDIUM     | "medium-priority" |
| LOW        | "low-priority"    |

**Example**:

```python
from canvas_sdk.commands import UpdateGoalCommand, GoalCommand
from datetime import datetime

update_goal = UpdateGoalCommand(
    note_uuid='rk786p',
    goal_id='0j9whjjk',
    due_date=datetime(2025, 3, 31),
    achievement_status=GoalCommand.AchievementStatus.WORSENING,
    priority=GoalCommand.Priority.MEDIUM,
    progress='patient has slowed down progress and requesting to move due date out'
)
```

---

## Vitals

**Command-specific parameters**:

| Name                               | Type      | Required | Description                                      |
|------------------------------------|-----------|----------|--------------------------------------------------|
| `height`                           | _integer_ | `false`  | Height in inches.                                |
| `weight_lbs`                       | _integer_ | `false`  | Weight in pounds.                                |
| `weight_oz`                        | _integer_ | `false`  | Weight in ounces.                                |
| `waist_circumference`              | _integer_ | `false`  | Waist circumference in inches.                   |
| `body_temperature`                 | _integer_ | `false`  | Body temperature in Fahrenheit.                  |
| `body_temperature_site`            | _enum_    | `false`  | Site of body temperature measurement.            |
| `blood_pressure_systole`           | _integer_ | `false`  | Systolic blood pressure.                         |
| `blood_pressure_diastole`          | _integer_ | `false`  | Diastolic blood pressure.                        |
| `blood_pressure_position_and_site` | _enum_    | `false`  | Position and site of blood pressure measurement. |
| `pulse`                            | _integer_ | `false`  | Pulse rate in beats per minute.                  |
| `pulse_rhythm`                     | _enum_    | `false`  | Rhythm of the pulse.                             |
| `respiration_rate`                 | _integer_ | `false`  | Respiration rate in breaths per minute.          |
| `oxygen_saturation`                | _integer_ | `false`  | Oxygen saturation in percentage.                 |
| `note`                             | _string_  | `false`  | Additional notes (max length: 150 characters).   |

**Enums and Types**:

| BodyTemperatureSite | Value | Description                          |
|---------------------|-------|--------------------------------------|
| `AXILLARY`          | `0`   | Measurement taken from the armpit.   |
| `ORAL`              | `1`   | Measurement taken from the mouth.    |
| `RECTAL`            | `2`   | Measurement taken from the rectum.   |
| `TEMPORAL`          | `3`   | Measurement taken from the forehead. |
| `TYMPANIC`          | `4`   | Measurement taken from the ear.      |


| BloodPressureSite      | Value | Description                         |
|------------------------|-------|-------------------------------------|
| `SITTING_RIGHT_UPPER`  | `0`   | Sitting position, right upper arm.  |
| `SITTING_LEFT_UPPER`   | `1`   | Sitting position, left upper arm.   |
| `STANDING_RIGHT_UPPER` | `4`   | Standing position, right upper arm. |
| `SUPINE_LEFT_LOWER`    | `11`  | Supine position, left lower arm.    |


| PulseRhythm             | Value | Description                  |
|-------------------------|-------|------------------------------|
| `REGULAR`               | `0`   | Regular rhythm.              |
| `IRREGULARLY_IRREGULAR` | `1`   | Completely irregular rhythm. |
| `REGULARLY_IRREGULAR`   | `2`   | Regularly irregular rhythm.  |

**Example**:

```python
from canvas_sdk.commands import VitalsCommand

VitalsCommand(
    height=70,
    weight_lbs=150,
    body_temperature=98,
    body_temperature_site=VitalsCommand.BodyTemperatureSite.ORAL,
    blood_pressure_systole=120,
    blood_pressure_diastole=80,
    blood_pressure_position_and_site=VitalsCommand.BloodPressureSite.SITTING_RIGHT_UPPER,
    pulse=72,
    pulse_rhythm=VitalsCommand.PulseRhythm.REGULAR,
    oxygen_saturation=98,
    note="Vitals are within normal range."
)
```
