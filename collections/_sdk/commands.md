---
title: "Commands"
---

The commands module lets you create and update commands within a specific note in Canvas. Commands are the building blocks of many end-user workflows in Canvas, including nearly all clinical workflows for documentation, like HPIs and questionnaires, as well as orders like prescriptions, labs, and referrals. Each Command class can be instantiated in your plugin and used to build a new command instance within a specific note or update an existing instance. The commands are then displayed in real time within the end user's workflow.

Common objectives that can be met by using Command classes include dynamic note templates, clinical decision support, order set composition, care gap closure, and care coordination automation.

{% include alert.html type="info" content="New to command fields? Fields that are autocompletes, dropdowns, or enums in the Canvas UI take a raw code, id, or enum value in the SDK — you have to look the value up first. See <a href='/guides/populating-command-fields/'>Populating Command Fields</a> for where each value comes from." %}

## Common Attributes

### Parameters

All commands share the following init kwarg parameters:

| Name           | Type     | Required                               | Description                                                             |
|:---------------|:---------|:---------------------------------------|:------------------------------------------------------------------------|
| `note_uuid`    | _string_ | `true` if creating a new command       | The id of the [Note](/sdk/data-note/#note) in which to insert the command. |
| `command_uuid` | _string_ | `true` if updating an existing command | The id of the [Command](/sdk/data-command/#command). On `originate` you can pass your own value to set it the first time; when updating, it references an existing command. |

All parameters can be set upon initialization, and also updated on the class instance.

### Methods

All commands have the following methods:

#### originate

Returns an Effect that originates a new command in the note body.

**Parameters:**

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `commit` | `bool` | No | `False` | When `True`, the command is automatically committed after origination. This is a simpler alternative to returning separate `originate()` and `commit()` effects. **Note:** This only applies to command types that support the COMMIT action. Commands that do not support committing (Reason For Visit, Prescribe, Refill, Adjust Prescription, Refer, and Order commands) will ignore this parameter. See the [command type table](/sdk/effects/#commands) for which commands support COMMIT. |
| `line_number` | `int` | No | `-1` | The line number in the note where the command should be inserted. By default the command will insert at the bottom of the note. |

**See also:** For efficiently inserting multiple commands at once, see [Batch Originate Commands](/sdk/effect-batch-originate/).

**Examples**:

```python
from canvas_sdk.commands import PlanCommand

def compute():
    new_plan = PlanCommand(note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47', narrative='new')
    new_plan.narrative = 'newer'

    return [new_plan.originate()]
```

To originate and commit in a single effect:

```python
from canvas_sdk.commands import DiagnoseCommand

def compute():
    diagnose_command = DiagnoseCommand(
        note_uuid='550e8400-e29b-41d4-a716-446655440000',
        icd10_code='E11.9'
    )

    return [diagnose_command.originate(commit=True)]
```

#### edit

Returns an Effect that edits an existing command with the values set on the command class instance.

**Behavior and Considerations:**
- **Partial Edits:** If you update only some fields of the command, any fields not explicitly modified will retain their existing values.
- **No Changes:** Calling `edit()` without making any changes will result in a no-op; the command remains unchanged.
- **Invalid Values:** If you attempt to set an invalid value, you should receive a validation error.

**Example**:

```python
from canvas_sdk.commands import PlanCommand

def compute():
    existing_plan = PlanCommand(command_uuid='2b9d1f0a-4c3e-4b5a-9d8c-7e6f5a4b3c2d', narrative='something new')

    return [existing_plan.edit()]
```

#### delete

Returns an Effect that deletes an existing, non-committed command from the note body.

**Example**:

```python
from canvas_sdk.commands import PlanCommand

def compute():
    existing_plan = PlanCommand(command_uuid='2b9d1f0a-4c3e-4b5a-9d8c-7e6f5a4b3c2d')

    return [existing_plan.delete()]
```

#### commit

Returns an Effect that commits an existing, non-committed command to the note body.

To block a command from committing and surface a message to the user — for example, enforcing your own business rules before a command is entered — return a [Command Validation effect](/sdk/effect-command-validation/) from a handler on the command's validation event.

**Example**:

```python
from canvas_sdk.commands import PlanCommand

def compute():
    existing_plan = PlanCommand(command_uuid='2b9d1f0a-4c3e-4b5a-9d8c-7e6f5a4b3c2d')

    return [existing_plan.commit()]
```

#### review

Returns an Effect that sets a command in review.

**Limited availability** The `review()` method can only be called on [Prescribe](#prescribe) commands objects. Other command types do not support this operation.

**Example**:

```python
from canvas_sdk.commands import PrescribeCommand

def compute():
    existing_prescribe = PrescribeCommand(command_uuid='e32b85d9-ccb7-4e4f-a0e5-8783ed2d9528')

    return [existing_prescribe.review()]
```

#### send

Returns an Effect that sends a signed command.

**Limited availability** The `send()` method can only be called on [LabOrder](#laborder) and [Prescribe](#prescribe) command objects. Other command types do not support this operation.

**Parameters:**

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `practice_location_override` | `str \| UUID` | No | `None` | [Prescribe](#prescribe) only. The `id` of a [PracticeLocation](/sdk/data-practicelocation/#practicelocation) whose address is used as the prescriber address on the outgoing prescription, overriding the prescriber's primary location. See [Prescribe](#prescribe) for behavior and limitations. |

**Example**:

```python
from canvas_sdk.commands import PrescribeCommand

def compute():
    existing_prescribe = PrescribeCommand(command_uuid='e32b85d9-ccb7-4e4f-a0e5-8783ed2d9528')

    return [existing_prescribe.send()]
```

To send the prescription using a specific practice location's address (see [Prescribe](#prescribe)):

```python
from canvas_sdk.commands import PrescribeCommand

def compute():
    existing_prescribe = PrescribeCommand(command_uuid='e32b85d9-ccb7-4e4f-a0e5-8783ed2d9528')

    return [existing_prescribe.send(practice_location_override='a1b2c3d4-e5f6-7890-abcd-ef1234567890')]
```

#### enter_in_error

Returns an effect that enter-in-errors an existing, committed command in the note body.

**Example**:

```python
from canvas_sdk.commands import PlanCommand

def compute():
    existing_plan = PlanCommand(command_uuid='2b9d1f0a-4c3e-4b5a-9d8c-7e6f5a4b3c2d')

    return [existing_plan.enter_in_error()]
```

#### delegate

Returns an Effect that delegates an existing, staged command by creating a task.

**Limited availability** The `delegate()` method can only be called on [ImagingOrder](#imagingorder) and [Refer](#refer) command objects. Other command types do not support this operation.

**Example**:

```python
from canvas_sdk.commands import ReferCommand

def compute():
    existing_refer = ReferCommand(command_uuid='e32b85d9-ccb7-4e4f-a0e5-8783ed2d9528')

    return [existing_refer.delegate()]
```

#### sign

Returns an Effect that signs an existing, staged command, transitioning it to a committed state.

**Limited availability** The `sign()` method can only be called on [ImagingOrder](#imagingorder) and [Refer](#refer) command objects. Other command types do not support this operation.

**Example**:

```python
from canvas_sdk.commands import ImagingOrderCommand

def compute():
    existing_imaging_order = ImagingOrderCommand(command_uuid='e32b85d9-ccb7-4e4f-a0e5-8783ed2d9528')

    return [existing_imaging_order.sign()]
```

#### upsert_metadata

Returns a [CommandMetadata effect](/sdk/effect-command-metadata/) that creates or updates a metadata key-value pair on a command. If metadata with the given key already exists on the command, its value will be updated. Otherwise, a new metadata record will be created.

The `command_uuid` field must be set on the command object before calling `upsert_metadata`.

To make this metadata **visible and editable as fields on the command in the note** — rather than only stored behind the scenes — use the [Command Metadata Create Form effect](/sdk/command-metadata-create-form-effect/), which renders additional fields on the command whose values are saved as command metadata.

| Parameter | Type     | Description                                      |
|-----------|----------|--------------------------------------------------|
| `key`     | _string_ | The metadata key (max 256 characters).           |
| `value`   | _string_ | The metadata value.                              |

**Example**:

```python
from canvas_sdk.commands import PlanCommand

def compute():
    existing_plan = PlanCommand(command_uuid='2b9d1f0a-4c3e-4b5a-9d8c-7e6f5a4b3c2d')

    return [existing_plan.upsert_metadata(key="priority", value="high")]
```

#### set_custom_html

Returns an effect that sets or clears custom HTML content on a command. The HTML is stored on the command and rendered alongside it in the note.

The `command_uuid` field must be set on the command object before calling `set_custom_html`. The command must be in a staged (not committed) state—calling this method on a committed command will raise a validation error.

| Parameter     | Type              | Description                                                      |
|---------------|-------------------|------------------------------------------------------------------|
| `custom_html` | _string_ or _None_ | The HTML content to set on the command, or `None` to clear it.  |

**Example**:

```python
from canvas_sdk.commands import PlanCommand

def compute():
    existing_plan = PlanCommand(command_uuid='2b9d1f0a-4c3e-4b5a-9d8c-7e6f5a4b3c2d')

    return [existing_plan.set_custom_html("<div class='highlight'>Important note</div>")]
```

To clear existing custom HTML from a command:

```python
from canvas_sdk.commands import PlanCommand

def compute():
    existing_plan = PlanCommand(command_uuid='2b9d1f0a-4c3e-4b5a-9d8c-7e6f5a4b3c2d')

    return [existing_plan.set_custom_html(None)]
```

## Originating and Committing Together

The simplest way to originate and commit a command in a single plugin action is to pass `commit=True` to the `originate()` method:

```python
from canvas_sdk.commands import DiagnoseCommand

def compute():
    diagnose_command = DiagnoseCommand(
        note_uuid='550e8400-e29b-41d4-a716-446655440000',
        icd10_code='E11.9'
    )

    return [diagnose_command.originate(commit=True)]
```

This handles the origination and commit in a single effect, without needing to manage a `command_uuid` yourself.

### Chaining Methods with a User-set UUID

If you need more control over the process — for example, to edit a command between origination and commit — you can chain separate effects by setting the `command_uuid` manually. This is also required for questionnaire-based commands, where `originate()` creates the command but does not add the answers — you must chain an `edit()` to populate the responses (see [Usage Example](#usage-example)). This chaining is necessary because the `originate` method executes asynchronously, so there is no way to get the `command_uuid` back from the originate action and use it for subsequent actions in the same operation.

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

## Command Actions

All commands support user-triggered actions through the Canvas UI. These actions appear as buttons or menu items that users can click to perform operations on a command.

Commands have two types of actions:

- **Generic actions** — available on all commands (listed below).
- **Command-specific actions** — vary by command type and are documented in each command's section below.

| Action | Description |
|--------|-------------|
| `print` | Generates a printable version of the command for documentation or external sharing. |
| `audit_history` | Displays the complete audit trail for the command, showing all modifications, state changes, and user interactions over time. |
| `carry_forward` | Populates the command with the last known data for this command type and patient, letting users quickly recreate a similar command from a previous entry. |

{% include alert.html type="info" content="The send action is the only command action available through the SDK and is limited to LabOrder and Prescribe commands only." %}

### Customizing Action Availability

You can programmatically control which actions appear on a command — and in what order — by responding to that command's `AVAILABLE_ACTIONS` event. Common uses:

- **Hide actions** based on user permissions, role, or command state.
- **Reorder actions** to prioritize commonly used operations.
- **Conditionally show actions** depending on workflow or business logic.

**How it works:**

1. When Canvas renders a command, it fires that command's `<COMMAND>_COMMAND__AVAILABLE_ACTIONS` event (e.g. `PLAN_COMMAND__AVAILABLE_ACTIONS`).
2. Your handler receives the default action list in `self.context["actions"]` and the acting user in `self.context["user"]`.
3. Return a single `COMMAND_AVAILABLE_ACTIONS_RESULTS` effect whose payload is the action list you want rendered. The returned list **replaces** the default set, so include every action the user should see — returning the original list unchanged is a no-op.

**Example** — hide the `print` action for a specific user:

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

        try:
            staff = Staff.objects.get(id=user_id)
            # Hide the print action for this user; everyone else keeps the full set
            if staff.first_name == "Larry":
                filtered_actions = [a for a in actions if a["name"] != "print"]
            else:
                filtered_actions = actions
        except Staff.DoesNotExist:
            filtered_actions = actions

        return [
            Effect(
                type=EffectType.COMMAND_AVAILABLE_ACTIONS_RESULTS,
                payload=json.dumps(filtered_actions),
            )
        ]
```

## Command Validation

Beyond the built-in validation each command performs on its own fields, you can add your **own** validation rules to a command and surface error messages to the user directly in the Canvas UI. A handler responds to a command's validation event (for example, `PLAN_COMMAND__POST_VALIDATION`) and returns a [Command Validation effect](/sdk/effect-command-validation/) containing one or more error messages. This is useful for enforcing organization-specific business rules — such as requiring a field, restricting certain combinations, or blocking a command until an external condition is met — before the command can be committed.

See the [Command Validation effect](/sdk/effect-command-validation/) documentation for the full API and examples.

## Commands

The sections below document each command class. See [Common Attributes](#common-attributes) for the parameters and methods shared by all commands.

### Custom Commands

For creating custom commands with HTML-rendered content that can be inserted into patient charts, see the [CustomCommand](/sdk/commands-custom-command/) documentation.

Custom commands are different from standard commands:
- They allow you to display read-only HTML content in the patient chart
- They must be configured in your plugin's manifest before use
- They support both display and print versions of content
- They are designed for displaying formatted data, not for capturing user input

Learn more: [CustomCommand Reference](/sdk/commands-custom-command/)

---

### AdjustPrescription

**Command-specific parameters**:

| Name           | Type     | Required to review / send | Description                          |
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
    pharmacy="pharmacy_ncpdp_id",
    prescriber_id="a7c2e9d1-3b4f-4a6c-8e0d-5f1a2b3c4d5e",
    supervising_provider_id="c3d4e5f6-7a8b-4c9d-0e1f-2a3b4c5d6e7f",
    note_to_pharmacist="Please verify patient's insurance before processing."
)
```

---

### Allergy

**Command-specific parameters**:

| Name               | Type            | Required to commit | Description                                                                      |
|:-------------------|:----------------|:---------|:---------------------------------------------------------------------------------|
| `allergy`          | _[Allergen](#allergy-allergen)_      | `false`  | Represents the allergen. See details in the [Allergen](#allergy-allergen) type below. Search allergens with the [ontologies allergen search](/sdk/utils/#get-fdballergy--full-text-search).                 |
| `severity`         | _[Severity](#allergy-severity) enum_ | `false`  | The severity of the allergic reaction. Must be one of [`AllergyCommand.Severity`](#allergy-severity). |
| `narrative`        | _string_        | `false`  | A narrative or free-text description of the allergy.                             |
| `approximate_date` | _datetime_      | `false`  | The approximate date the allergy was identified.                                 |

**Enums and Types**:

<a id="allergy-allergen"></a>

**`Allergen`**

| Attribute      | Type                | Description                                            |
|:---------------|:--------------------|:-------------------------------------------------------|
| `concept_id`   | _integer_           | The identifier for the allergen concept.               |
| `concept_type` | _[AllergenType](#allergy-allergentype) enum_ | The type of allergen. See [`AllergenType`](#allergy-allergentype) values below. |



<a id="allergy-allergentype"></a>

| AllergenType     | Value | Description                        |
|:-----------------|:------|:-----------------------------------|
| `ALLERGEN_GROUP` | `1`   | Represents a group of allergens.   |
| `MEDICATION`     | `2`   | Represents a medication allergen.  |
| `INGREDIENT`     | `6`   | Represents an ingredient allergen. |


<a id="allergy-severity"></a>

| Severity   | Value        | Description                    |
|:-----------|:-------------|:-------------------------------|
| `MILD`     | `"mild"`     | Indicates a mild reaction.     |
| `MODERATE` | `"moderate"` | Indicates a moderate reaction. |
| `SEVERE`   | `"severe"`   | Indicates a severe reaction.   |

**Example**:

```python
from canvas_sdk.commands.commands.allergy import AllergyCommand, AllergenType, Allergen
from datetime import date

allergy = AllergyCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    allergy=Allergen(concept_id=12345, concept_type=AllergenType.MEDICATION),
    severity=AllergyCommand.Severity.SEVERE,
    narrative="Severe rash and difficulty breathing after penicillin.",
    approximate_date=date(2023, 6, 15)
)
```

---

### Assess

**Command-specific parameters**:

| Name           | Type          | Required to commit | Description                                                                |
|:---------------|:--------------|:---------|:---------------------------------------------------------------------------|
| `condition_id` | _string_      | `true`   | The id of the [Condition](/sdk/data-condition/#condition) being assessed. Must be a condition already recorded on that patient's chart.               |
| `background`   | _string_      | `false`  | Background information about the diagnosis.                                |
| `status`       | _Status enum_ | `false`  | The current status of the diagnosis. Must be one of [`AssessCommand.Status`](#assess-status). |
| `narrative`    | _string_      | `false`  | The narrative for the current assessment (max 2048 characters; values exceeding the limit raise a validation error instead of being truncated). |

<a id="assess-status"></a>

| `Status`       | Value            | Description                     |
|:---------------|:-----------------|:--------------------------------|
| `IMPROVED`     | `"improved"`     | The condition has improved.     |
| `STABLE`       | `"stable"`       | The condition is stable.        |
| `DETERIORATED` | `"deteriorated"` | The condition has deteriorated. |

**Example**:

```python
from canvas_sdk.commands import AssessCommand

assess = AssessCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    condition_id='a1c2e3d4-5b6f-4a7c-8e9d-0f1a2b3c4d5e',
    background='started in 2012',
    status=AssessCommand.Status.STABLE,
    narrative='experiencing more pain lately'
)
```

**Validation**:

`condition_id` has to belong to the patient whose chart the command is being written to. `originate` and `edit` both check it: the patient comes from `note_uuid` when you originate the command, and from the existing command's note when you edit one. A condition on another patient's chart — or an id that matches no condition at all — fails validation, and the command is neither created nor updated.

---

### ChangeMedication

**Command-specific parameters**:

| Name            | Type     | Required to commit | Description                                                        |
|:----------------|:---------|:---------|:-------------------------------------------------------------------|
| `medication_id` | _string_ | `true`   | The id of the [Medication](/sdk/data-medication/#medication) being changed. Must be a medication on that patient's chart. |
| `sig`           | _string_ | `false`  | Administration details of the medication.                          |

**Example**:

```python
from canvas_sdk.commands.commands.change_medication import ChangeMedicationCommand

change_medication = ChangeMedicationCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    medication_id='f0a1b2c3-d4e5-4f6a-8b9c-0d1e2f3a4b5c',
    sig='two pills taken orally'
)
```

---

### CloseGoal

**Command-specific parameters**:

| Name                 | Type                     | Required to commit | Description                                                                               |
|:---------------------|:-------------------------|:---------|:------------------------------------------------------------------------------------------|
| `goal_id`            | _int_                    | `true`   | The `dbid` of the [Goal](/sdk/data-goal/#goal) being closed. Must be a goal on that patient's chart.                                     |
| `achievement_status` | _[AchievementStatus](#goal-achievementstatus) enum_ | `false`  | The final achievement status of the goal. Must be one of [`GoalCommand.AchievementStatus`](#goal-achievementstatus). |
| `progress`           | _string_                 | `false`  | A narrative about the patient's progress toward the goal.                                 |

**Example**:

```python
from canvas_sdk.commands import CloseGoalCommand, GoalCommand

close_goal = CloseGoalCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    goal_id=12345,
    achievement_status=GoalCommand.AchievementStatus.ACHIEVED,
    progress="Patient has achieved the target weight goal of 150 lbs."
)
```

### Diagnose

**Command-specific parameters**:

| Name                        | Type       | Required to commit | Description                                                |
|:----------------------------|:-----------|:---------|:-----------------------------------------------------------|
| `icd10_code`                | _string_   | `true`   | ICD-10 code of the condition being diagnosed. Search with the [ICD-10 condition endpoint](/sdk/utils/#get-icdcondition--icd-10-conditions).              |
| `background`                | _string_   | `false`  | Background information about the diagnosis.                |
| `approximate_date_of_onset` | _datetime_ | `false`  | The approximate date the condition began.                  |
| `today_assessment`          | _string_   | `false`  | The narrative for the initial assessment of the condition (max length: 2048 characters). |

**Example**:

```python
from canvas_sdk.commands import DiagnoseCommand
from datetime import datetime

diagnose = DiagnoseCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    icd10_code='M54.50',
    background='lifted heavy box',
    approximate_date_of_onset=datetime(2012, 1, 1),
    today_assessment='unable to sleep lately'
)
```

---

### FamilyHistory

**Command-specific parameters**:

| Name             | Type                 | Required to commit | Description                                           |
|:-----------------|:---------------------|:---------|:------------------------------------------------------|
| `family_history` | _string_ or _[Coding](#coding)_ | `true`   | A description of the family history being documented. Search with the [family-history endpoint](/sdk/utils/#get-snomedfamily-history--family-history-conditions). |
| `relative`       | _string_             | `false`  | A description of the relative (e.g., mother, uncle). Search with the [family-relation endpoint](/sdk/utils/#get-snomedfamily-relation--family-relationships).  |
| `note`           | _string_             | `false`  | Additional notes or context about the family history. |

**Coding Support**:

The `family_history` parameter accepts either:
- **String**: Searches for matching family history conditions and selects the first result.
- **Coding object**: Allows structured or unstructured coding
  - Supported systems: `SNOMED`, `UNSTRUCTURED`
  - Required fields: `system`, `code`
  - Optional field: `display`

The `relative` parameter also searches and selects the first result when a string is provided. Use specific terms (e.g., `"Paternal Grandfather"`, `"Maternal Grandfather"`) to avoid ambiguous matches.

**Example**:

```python
from canvas_sdk.commands import FamilyHistoryCommand
from canvas_sdk.commands.constants import CodeSystems, Coding


# Using a string (searches and takes the first result — may be ambiguous)
family_history = FamilyHistoryCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    family_history="Diabetes Type 2",
    relative="Mother",
    note="Diagnosed at age 45"
)

# Using a SNOMED code
family_history_snomed = FamilyHistoryCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    family_history=Coding(
        system=CodeSystems.SNOMED,
        code="44054006",
        display="Diabetes Type 2"
    ),
    relative="Mother",
    note="Diagnosed at age 45"
)

# Using unstructured (free text)
family_history_unstructured = FamilyHistoryCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    family_history=Coding(
        system=CodeSystems.UNSTRUCTURED,
        code="Family history of heart disease"
    ),
    relative="Father"
)
```
---

### FollowUp

**Command-specific parameters**:

| Name             | Type                     | Required to commit        | Description                                                                                                                                                                                                                |
|:-----------------|:-------------------------|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `structured`     | _boolean_                | `false`                   | Whether the RFV is structured or not. Defaults to False.                                                                                                                                                                   |
| `requested_date` | _date_                   | `false`                   | The desired follow up date.                                                                                                                                                                                                |
| `note_type_id`   | _UUID (str)_             | `false`                   | The desired type of appointment. See [NoteType](/sdk/data-note/#notetype).                                                                                                                                                                                           |
| `coding`         | _[Coding](#coding)_ or _UUID (str)_ | `true` if structured=True | The coding for the structured RFV. Either a full [Coding](#coding) object (with `code`, `system`, `display`) or a UUID string referencing a verified coding record. If a [Coding](#coding) is provided, it is validated against existing [ReasonForVisitSettingCoding](/sdk/data-reason-for-visit/#reasonforvisitsettingcoding) records |
| `comment`        | _string_                 | `false`                   | Additional commentary on the RFV.                                                                                                                                                                                          |

**Example**:

```python
from canvas_sdk.commands import FollowUpCommand
from datetime import date

structured = FollowUpCommand(
  note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
  structured=True,
  requested_date=date(2025, 3, 2),
  note_type_id="d1e2f3a4-b5c6-4d7e-8f9a-0b1c2d3e4f5a",
  coding={'code': '49727002', 'system': 'http://snomed.info/sct', 'display': 'Cough'},
  comment='also wants to discuss treatment options'
)

# Example with a UUID string referencing a Coding record
structured2 = FollowUpCommand(
  note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
  structured=True,
  requested_date=date(2025, 3, 2),
  note_type_id="d1e2f3a4-b5c6-4d7e-8f9a-0b1c2d3e4f5a",
  coding="e2b1e1e3-3f52-4a0a-bb3a-123456789abc",  # Must correspond to an existing coding record
  comment="Discuss treatment options"
)

unstructured = FollowUpCommand(
  note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
  requested_date=date(2025, 3, 2),
  note_type_id="d1e2f3a4-b5c6-4d7e-8f9a-0b1c2d3e4f5a",
  comment='also wants to discuss treatment options'
)

```

---

### Goal

**Command-specific parameters**:

| Name                 | Type                     | Required to commit | Description                                               |
|:---------------------|:-------------------------|:---------|:----------------------------------------------------------|
| `goal_statement`     | _string_                 | `true`   | Description of the goal.                                  |
| `start_date`         | _datetime_               | `false`  | The date the goal begins.                                 |
| `due_date`           | _datetime_               | `false`  | The date the goal is due.                                 |
| `achievement_status` | _[AchievementStatus](#goal-achievementstatus) enum_ | `false`  | The current achievement status of the goal.               |
| `priority`           | _[Priority](#goal-priority) enum_          | `false`  | The priority of the goal.                                 |
| `progress`           | _string_                 | `false`  | A narrative about the patient's progress toward the goal. |


<a id="goal-achievementstatus"></a>

| `AchievementStatus` | Value              | Description                                |
|:--------------------|:-------------------|:-------------------------------------------|
| `IN_PROGRESS`       | `"in-progress"`    | The goal is being pursued.                 |
| `IMPROVING`         | `"improving"`      | Progress toward the goal is improving.     |
| `WORSENING`         | `"worsening"`      | Progress toward the goal is worsening.     |
| `NO_CHANGE`         | `"no-change"`      | No change in progress toward the goal.     |
| `ACHIEVED`          | `"achieved"`       | The goal has been achieved.                |
| `SUSTAINING`        | `"sustaining"`     | The achieved goal is being sustained.      |
| `NOT_ACHIEVED`      | `"not-achieved"`   | The goal was not achieved.                 |
| `NO_PROGRESS`       | `"no-progress"`    | No progress has been made toward the goal. |
| `NOT_ATTAINABLE`    | `"not-attainable"` | The goal is not attainable.                |

<a id="goal-priority"></a>

| `Priority` | Value               | Description      |
|:-----------|:--------------------|:-----------------|
| `HIGH`     | `"high-priority"`   | High priority.   |
| `MEDIUM`   | `"medium-priority"` | Medium priority. |
| `LOW`      | `"low-priority"`    | Low priority.    |

**Example**:

```python
from canvas_sdk.commands import GoalCommand
from datetime import datetime

goal = GoalCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    goal_statement='Eat more healthy vegetables.',
    start_date=datetime(2024, 1, 1),
    due_date=datetime(2024, 12, 31),
    achievement_status=GoalCommand.AchievementStatus.IN_PROGRESS,
    priority=GoalCommand.Priority.HIGH,
    progress='patient is frequenting local farmers market to find healthy options'
)
```

---

### HistoryOfPresentIllness

**Command-specific parameters**:

| Name        | Type     | Required to commit | Description                                                |
|:------------|:---------|:---------|:-----------------------------------------------------------|
| `narrative` | _string_ | `true`   | The narrative of the patient's history of present illness. |

**Example**:

```python
from canvas_sdk.commands import HistoryOfPresentIllnessCommand

hpi = HistoryOfPresentIllnessCommand(
        note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
        narrative='presents with chronic back pain and headaches'
    )
```

---


### ImagingOrder

**Command-specific parameters**:

| Name                    | Type              | Required to delegate / sign | Description                                                                   |
|:------------------------|:------------------|:---------|:------------------------------------------------------------------------------|
| `image_code`            | _string_          | `true`   | Code identifier of the imaging order. Search with the [imaging-codes endpoint](/sdk/utils/#searching-for-imaging-codes).                                         |
| `diagnosis_codes`       | _list[string]_    | `true`   | ICD-10 Diagnosis codes justifying the imaging order. Search with the [ICD-10 condition endpoint](/sdk/utils/#get-icdcondition--icd-10-conditions).                          |
| `priority`              | _[Priority](#imagingorder-priority) enum_   | `false`  | Priority of the imaging order. Must be one of [`ImagingOrderCommand.Priority`](#imagingorder-priority). |
| `additional_details`    | _string_          | `false`  | Additional details or instructions related to the imaging order.              |
| `service_provider`      | _[ServiceProvider](#serviceprovider)_ | `true`   | Service provider of the imaging order. Search with the [contacts endpoint](/sdk/utils/#searching-for-contacts-and-service-providers).                                        |
| `comment`               | _string_          | `false`  | Additional comments.                                                          |
| `ordering_provider_key` | _string_          | `true`   | The [Staff](/sdk/data-staff/#staff) `id` of the provider ordering the imaging.                                |
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

<a id="imagingorder-priority"></a>

**`Priority`**

| Priority  | Value       | Description               |
|:----------|:------------|:--------------------------|
| `ROUTINE` | `"Routine"` | A routine order.          |
| `URGENT`  | `"Urgent"`  | An urgent order.          |
| `STAT`    | `"STAT"`    | A STAT (immediate) order. |

**Example**:

```python
from canvas_sdk.commands import ImagingOrderCommand
from canvas_sdk.commands.constants import ServiceProvider

imaging_order = ImagingOrderCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    image_code="G0204",
    diagnosis_codes=["E119"],
    priority=ImagingOrderCommand.Priority.ROUTINE,
    comment="this is a comment",
    additional_details="more details",
    ordering_provider_key="b8a7c6d5-4e3f-4a2b-9c1d-0e8f7a6b5c4d",
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

### ImagingReview

**Command-specific parameters**:

| Name                     | Type                                     | Required to commit | Description                                                                                                    |
|--------------------------|:-----------------------------------------|:---------|:---------------------------------------------------------------------------------------------------------------|
| `report_ids`             | _list[string]_                           | `true`   | List of [ImagingReport](/sdk/data-imaging/#imagingreport) IDs to review. Must be reports on that patient's chart.                                                                          |
| `message_to_patient`     | _string_                                 | `false`  | Message to communicate findings to the patient.                                                                |
| `communication_method`   | _[ReportReviewCommunicationMethod](#reportreviewcommunicationmethod) enum_   | `false`  | Method for patient communication. Must be one of [`ReportReviewCommunicationMethod`](#reportreviewcommunicationmethod).       |
| `linked_items_urns`      | _list[string]_                           | `false`  | List of URNs for items linked to the review.                                                                   |
| `comment`                | _string_                                 | `false`  | Internal comment about the review.                                                                             |

**Example**:

```python
from canvas_sdk.commands import ImagingReviewCommand
from canvas_sdk.commands.commands.review import ReportReviewCommunicationMethod
from canvas_sdk.v1.data import ImagingReport, Patient

patient = Patient.objects.get(id="patient-id")
# Get imaging reports to review
imaging_reports = ImagingReport.objects.filter(patient=patient, review__isnull=True, review_mode='RR')
report_ids = [str(report.id) for report in imaging_reports]

imaging_review = ImagingReviewCommand(
    note_uuid="a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
    report_ids=report_ids,
    message_to_patient="Your imaging results show no abnormalities.",
    communication_method=ReportReviewCommunicationMethod.DELEGATED_CALL_CAN_LEAVE_MESSAGE,
    comment="All clear, no follow-up needed."
)
```

---

### ImmunizationStatement

**Command-specific parameters**:

| Name               | Type                 | Required to commit | Description                                                                                                         |
|--------------------|----------------------|----------|---------------------------------------------------------------------------------------------------------------------|
| `cpt_code`         | _string_ or _[Coding](#coding)_ | `false`* | The CPT code for the immunization procedure. Used with CVX code to search against ontologies server for validation. Search with the [immunization endpoint](/sdk/utils/#get-cptimmunization--search-immunizations). |
| `cvx_code`         | _string_ or _[Coding](#coding)_ | `false`* | The CVX code for the vaccine administered. Used with CPT code to search against ontologies server for validation. Search with the [immunization endpoint](/sdk/utils/#get-cptimmunization--search-immunizations).   |
| `unstructured`     | _[Coding](#coding)_             | `false`* | Free-text immunization description.                                                                                 |
| `approximate_date` | _date_               | `false`  | The approximate date when the immunization was administered.                                                        |
| `comments`         | _string_             | `false`  | Additional comments about the immunization (max 255 characters).                                                    |

*Must provide either both `cpt_code` and `cvx_code` together, or `unstructured` alone (cannot mix structured and unstructured).

**Coding Support**:

The `cpt_code` and `cvx_code` parameters accept either:
- **String**: Looks up the code in the respective system (CPT or CVX)
- **Coding object**: Allows structured coding
  - `cpt_code` must use system: `CPT`
  - `cvx_code` must use system: `CVX`
  - Required fields: `system`, `code`
  - Optional field: `display`

The `unstructured` parameter:
- **Coding object**: For free-text immunizations
  - Required system: `UNSTRUCTURED`
  - Required fields: `system`, `code`
  - Optional field: `display`

**Examples**:

```python
from canvas_sdk.commands.commands.immunization_statement import ImmunizationStatementCommand
from canvas_sdk.commands.constants import CodeSystems, Coding
from datetime import date

immunization_statement = ImmunizationStatementCommand(
    cpt_code="90724",
    cvx_code="88",
    approximate_date=date(2024, 1, 15),
    comments="Patient received influenza vaccine"
)

# Using Coding objects for structured codes
immunization_statement_coded = ImmunizationStatementCommand(
    cpt_code=Coding(
        system=CodeSystems.CPT,
        code="90724"
    ),
    cvx_code=Coding(
        system=CodeSystems.CVX,
        code="88"
    ),
    approximate_date=date(2024, 1, 15),
    comments="Patient received influenza vaccine"
)

# Using unstructured (free text immunization)
immunization_statement_unstructured = ImmunizationStatementCommand(
    unstructured=Coding(
        system=CodeSystems.UNSTRUCTURED,
        code="COVID-19 booster at pharmacy"
    ),
    approximate_date=date(2024, 1, 15)
)
```

---

### Instruct

**Command-specific parameters**:

| Name      | Type       | Required to commit | Description                                                           |
|-----------|------------|----------|-----------------------------------------------------------------------|
| `coding`  | __[Coding](#coding)__ | `true`   | The SNOMED code or UNSTRUCTURED code that represents the instruction. Search SNOMED with the [instruction endpoint](/sdk/utils/#get-snomedinstruction--instructions). |
| `comment` | _string_   | `false`  | Additional comments related to the instruction.                       |

**Example**:

```python
from canvas_sdk.commands import InstructCommand
from canvas_sdk.commands.constants import CodeSystems, Coding

# SNOMED code
InstructCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    coding=Coding(system=CodeSystems.SNOMED, code="65921008"),
    comment="To address mild dehydration symptoms"
)

# UNSTRUCTURED code
InstructCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    coding=Coding(system=CodeSystems.UNSTRUCTURED, code="Physical medicine neuromuscular training"),
)
```

---

### LabOrder

The `LabOrderCommand` is used to initiate a lab order through the Canvas system.
This command requires detailed information about the lab partner, the tests being ordered, and the provider placing the
order.
Built-in validations ensure that:

- The specified lab partner exists (whether provided by name or ID).
- The ordered tests are available for the chosen lab partner.

**Electronic ordering:** LabOrder commands support the `send()` method for electronic ordering of signed orders directly to lab partners. However, electronic ordering has additional requirements:

- Only lab partners with electronic ordering enabled support the `send()` method.
- The command must be committed/signed before it can be sent electronically.
- The patient must have an address and phone number on file.
- The ordering provider must have an NPI.

**Command-specific parameters**:

| Name                    | Type           | Required to send | Description                                                                                                                                                      |
|-------------------------|----------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `lab_partner`           | _string_       | `true`   | The [lab partner](/sdk/data-lab-partner-and-test/#labpartner) processing the order. Accepts either the lab partner’s name or its unique identifier (ID).                                                       |
| `tests_order_codes`     | _list[string]_ | `true`   | A list of codes or IDs for the [tests](/sdk/data-lab-partner-and-test/#labpartnertest-attributes) being ordered. The system verifies that each provided value corresponds to an available test for the specified lab partner. |
| `ordering_provider_key` | _string_       | `false`  | The [Staff](/sdk/data-staff/#staff) `id` of the provider ordering the tests.                                                                                                                     |
| `diagnosis_codes`       | _list[string]_ | `false`  | ICD-10 Diagnosis codes justifying the lab order. Search with the [ICD-10 condition endpoint](/sdk/utils/#get-icdcondition--icd-10-conditions).                                                                                                                 |
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

#### Validations

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
  ordering_provider_key="b8a7c6d5-4e3f-4a2b-9c1d-0e8f7a6b5c4d",
  diagnosis_codes=["E119"],
  fasting_required=True,
  comment="Patient should fast for 8 hours before the test."
)
```

---

### LabReview

**Command-specific parameters**:

| Name                     | Type                                     | Required to commit | Description                                                                                                    |
|--------------------------|:-----------------------------------------|:---------|:---------------------------------------------------------------------------------------------------------------|
| `report_ids`             | _list[string]_                           | `true`   | List of [LabReport](/sdk/data-labs/#labreport) IDs to review. Must be reports on that patient's chart.                                                                              |
| `message_to_patient`     | _string_                                 | `false`  | Message to communicate findings to the patient.                                                                |
| `communication_method`   | _[ReportReviewCommunicationMethod](#reportreviewcommunicationmethod) enum_   | `false`  | Method for patient communication. Must be one of [`ReportReviewCommunicationMethod`](#reportreviewcommunicationmethod).           |
| `linked_items_urns`      | _list[string]_                           | `false`  | List of URNs for items linked to the review.                                                                   |
| `comment`                | _string_                                 | `false`  | Internal comment about the review.                                                                             |

**Example**:

```python
from canvas_sdk.commands import LabReviewCommand
from canvas_sdk.commands.commands.review import ReportReviewCommunicationMethod
from canvas_sdk.v1.data import LabReport, Patient

patient = Patient.objects.get(id="patient-id")
# Get lab reports to review
lab_reports = LabReport.objects.filter(patient=patient, review__isnull=True, review_mode='RR')
report_ids = [str(report.id) for report in lab_reports]

lab_review = LabReviewCommand(
    note_uuid="a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
    report_ids=report_ids,
    message_to_patient="Your lab results are within normal range.",
    communication_method=ReportReviewCommunicationMethod.DELEGATED_CALL_CAN_LEAVE_MESSAGE,
    comment="All values normal, no follow-up needed."
)
```

---

### MedicalHistory

**Command-specific parameters**:

| Name                     | Type      | Required to commit | Description                                                |
|--------------------------|-----------|----------|------------------------------------------------------------|
| `past_medical_history`   | _string_  | `true`   | An ICD-10 code or description of the past medical condition. ICD-10 codes are strongly preferred (see note below). Search with the [ICD-10 condition endpoint](/sdk/utils/#get-icdcondition--icd-10-conditions). |
| `approximate_start_date` | _date_    | `false`  | Approximate start date of the condition.                   |
| `approximate_end_date`   | _date_    | `false`  | Approximate end date of the condition.                     |
| `show_on_condition_list` | _boolean_ | `false`  | Whether the condition should appear on the condition list. |
| `comments`               | _string_  | `false`  | Additional comments (max length: 1000 characters).         |

**Important: Use ICD-10 codes for accurate matching.** The `past_medical_history` field searches for matching conditions and selects the first result. When a text description is provided, similar conditions may match first. To guarantee the correct condition, pass the ICD-10 code directly (e.g., `"I1010"`).

**Example**:

```python
from canvas_sdk.commands import MedicalHistoryCommand
from datetime import date

# Preferred: use the ICD-10 code for exact matching
MedicalHistoryCommand(
    past_medical_history="I1010",  # Resistant Hypertension
    approximate_start_date=date(2015, 1, 1),
    show_on_condition_list=True,
    comments="Controlled with medication."
)

# Also works but may match a different condition if the description is ambiguous
MedicalHistoryCommand(
    past_medical_history="Resistant Hypertension",
    approximate_start_date=date(2015, 1, 1),
    show_on_condition_list=True,
    comments="Controlled with medication."
)
```

---

### MedicationStatement

**Command-specific parameters**:

| Name       | Type                 | Required to commit | Description                                            |
|:-----------|:---------------------|:---------|:-------------------------------------------------------|
| `fdb_code` | _string_ or _[Coding](#coding)_ | `true`   | The [FDB code](/sdk/utils/#fdb_code) of the medication |
| `sig`      | _string_             | `false`  | Administration details of the medication.              |

**Coding Support**:

The `fdb_code` parameter accepts either:
- **String (FDB code)**: Looks up the medication in the FDB system
- **Coding object**: Allows structured or unstructured coding
  - Supported systems: `FDB`, `UNSTRUCTURED`
  - Required fields: `system`, `code`
  - Optional field: `display`

**Example**:

```python
from canvas_sdk.commands import MedicationStatementCommand
from canvas_sdk.commands.constants import CodeSystems, Coding

# Using an FDB code string (recommended for FDB medications)
medication_statement = MedicationStatementCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    fdb_code='198698',
    sig='two pills taken orally'
)

# Using an FDB Coding object
medication_statement_fdb = MedicationStatementCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    fdb_code=Coding(
        system=CodeSystems.FDB,
        code='198698',
        display='aspirin 81 mg oral tablet'
    ),
    sig='two pills taken orally'
)

# Using unstructured (free text medication)
medication_statement_unstructured = MedicationStatementCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    fdb_code=Coding(
        system=CodeSystems.UNSTRUCTURED,
        code='Herbal supplement for joint health'
    )
)
```

---

### SurgicalHistory

**Command-specific parameters**:

| Name                    | Type                 | Required to commit | Description                                        |
|-------------------------|----------------------|----------|----------------------------------------------------|
| `past_surgical_history` | _string_ or _[Coding](#coding)_ | `true`   | A description of the past surgical procedure. Search with the [procedures endpoint](/sdk/utils/#get-snomedprocedures--surgical-history-procedures).      |
| `approximate_date`      | _date_               | `false`  | Approximate date of the surgery.                   |
| `comment`               | _string_             | `false`  | Additional comments (max length: 1000 characters). |

**Coding Support**:

The `past_surgical_history` parameter accepts either:
- **String**: Searches for matching surgical procedures and selects the first result.
- **Coding object**: Allows structured or unstructured coding
  - Supported systems: `SNOMED`, `UNSTRUCTURED`
  - Required fields: `system`, `code`
  - Optional field: `display`

**Example**:

```python
from canvas_sdk.commands import PastSurgicalHistoryCommand
from canvas_sdk.commands.constants import CodeSystems, Coding
from datetime import date

# Using a string (searches and takes the first result)
PastSurgicalHistoryCommand(
    past_surgical_history="Appendectomy",
    approximate_date=date(2008, 6, 15),
    comment="No complications reported."
)

# Using a SNOMED code
surgical_history_snomed = PastSurgicalHistoryCommand(
    past_surgical_history=Coding(
        system=CodeSystems.SNOMED,
        code="80146002",
        display="Appendectomy"
    ),
    approximate_date=date(2008, 6, 15),
    comment="No complications reported."
)

# Using unstructured (free text)
surgical_history_unstructured = PastSurgicalHistoryCommand(
    past_surgical_history=Coding(
        system=CodeSystems.UNSTRUCTURED,
        code="Minor outpatient procedure on left knee"
    ),
    approximate_date=date(2020, 3, 10)
)
```

---

### Perform

**Command-specific parameters**:

| Name       | Type                 | Required to commit | Description                                          |
|------------|----------------------|----------|------------------------------------------------------|
| `cpt_code` | _string_ or _[Coding](#coding)_ | `true`   | The CPT code of the procedure or action performed. Look it up in the [Charge Description Master](/sdk/data-charge-description-master/#chargedescriptionmaster).   |
| `notes`    | _string_             | `false`  | Additional notes related to the performed procedure. |

**Coding Support**:

The `cpt_code` parameter accepts either:
- **String**: Searches for matching procedures
- **Coding object**: Allows structured or unstructured coding
  - Supported systems: `CPT`, `UNSTRUCTURED`
  - Required fields: `system`, `code`
  - Optional field: `display`

**Example**:

```python
from canvas_sdk.commands import PerformCommand
from canvas_sdk.commands.constants import CodeSystems, Coding

# Using a string (searches for matching procedures)
PerformCommand(
    cpt_code="99213",
    notes="Patient presented with a common cold."
)

# Using a CPT code
perform_cpt = PerformCommand(
    cpt_code=Coding(
        system=CodeSystems.CPT,
        code="99213",
        display="Office visit, established patient"
    ),
    notes="Annual wellness visit"
)

# Using unstructured (free text)
perform_unstructured = PerformCommand(
    cpt_code=Coding(
        system=CodeSystems.UNSTRUCTURED,
        code="Custom procedure performed"
    ),
    notes="Non-standard procedure documentation"
)
```

---

### Plan

**Command-specific parameters**:

| Name        | Type     | Required to commit | Description                          |
|:------------|:---------|:---------|:-------------------------------------|
| `narrative` | _string_ | `true`   | The narrative of the patient's plan. |

**Example**:

```python
from canvas_sdk.commands import PlanCommand

plan = PlanCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    narrative='will return in 2 weeks to check on pain management'
)
```

---

### POCLabTest

The `POCLabTestCommand` is used to document the results of a Point-of-Care (POC) lab test performed
in the clinic — distinct from `LabOrder` (which sends tests to an external lab partner) and
`LabReview` (which reviews returned results). The command captures the template used, the
indications, individual measured values, and a free-text remarks field.

Built-in validations ensure that:

- The provided `template` UUID resolves to an active POC [`LabReportTemplate`](/sdk/data-lab-report-template/#labreporttemplate).
- Each `test_values` entry's `label` matches one of the template's [field labels](/sdk/data-lab-report-template/#labreporttemplatefield) (case-insensitive).

**Command-specific parameters**:

| Name          | Type              | Required to commit | Description                                                                                                          |
|---------------|-------------------|--------------------|----------------------------------------------------------------------------------------------------------------------|
| `template`    | _UUID \| string_  | `true`             | The UUID of the active POC [`LabReportTemplate`](/sdk/data-lab-report-template/#labreporttemplate). Accepts UUID instances or UUID-formatted strings.                    |
| `indications` | _list[string]_    | `false`            | ICD-10 diagnosis codes justifying the test. Search with the [ICD-10 condition endpoint](/sdk/utils/#get-icdcondition--icd-10-conditions).                                                                          |
| `test_values` | _list[[TestValue](#poclabtest-testvalue)]_ | `false`            | The measured values, each tagged with its template-field label. See [`TestValue`](#poclabtest-testvalue) below.                               |
| `remarks`     | _string (≤512)_   | `false`            | Free-text comments from the clinician.                                                                               |

**Enums and Types**:

<a id="poclabtest-testvalue"></a>
**`TestValue`**

A dataclass representing a single measured value within a POC lab test result.

| Attribute | Type     | Description                                                       |
|-----------|----------|-------------------------------------------------------------------|
| `label`   | _string_ | The template field's label (must match a field on the template).  |
| `value`   | _string_ | The measured value (as a string).                                 |

`TestValue.to_dict()` returns the `{"label": ..., "value": ...}` dict shape consumed by the runtime.

**Helper methods**:

- `set_test_value(label, value)` — Adds or replaces a test value by label. If a `TestValue` with
  the same `label` already exists on the command, it is replaced (so calling `set_test_value` twice
  with the same label leaves a single entry).

#### Validations

- **Template Validation:** The `template` UUID must resolve to a [`LabReportTemplate`](/sdk/data-lab-report-template/#labreporttemplate) that is
  `active=True` and `poc=True`. Templates from external lab partners or inactive templates are
  rejected.
- **Test Values Validation:** Each `TestValue.label` must match (case-insensitive) the `label` of
  one of the resolved template's [fields](/sdk/data-lab-report-template/#labreporttemplatefield). Unknown labels cause a validation error.

The valid labels are the `label` of each [`LabReportTemplateField`](/sdk/data-lab-report-template/#labreporttemplatefield) on the template's [`fields`](/sdk/data-lab-report-template/#labreporttemplate) relation:

```python
from canvas_sdk.v1.data import LabReportTemplate

template = LabReportTemplate.objects.active().point_of_care().first()
valid_labels = [field.label for field in template.fields.all()]
```

**Example**:

```python
from canvas_sdk.commands import POCLabTestCommand
from canvas_sdk.commands.commands.poc_lab_test import TestValue
from canvas_sdk.v1.data import LabReportTemplate

template = LabReportTemplate.objects.active().point_of_care().first()

command = POCLabTestCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    template=template.id,
    indications=["E11.9"],
    test_values=[
        TestValue(label="pH", value="6.5"),
        TestValue(label="Glucose", value="120"),
    ],
    remarks="Sample collected mid-stream",
)

# Or via the helper (overwrites by label):
command.set_test_value("pH", "6.8")
```

---

### Prescribe

**Electronic prescribing:** Prescribe commands support the `send()` method for electronic transmission of signed prescriptions. However, electronic prescribing has additional validations:

- A pharmacy must be specified on the command before it can be sent.
- The command must be committed/signed before it can be sent electronically.

**Overriding the prescriber address:** By default, the prescriber address transmitted on the prescription is derived from the prescriber's primary practice location. For workflows where a provider works across multiple offices — for example white bagging, where the medication ships to the office where the patient is being seen — pass a `practice_location_override` to [`send()`](#send) to use a specific practice location's address instead:

```python
from canvas_sdk.commands import PrescribeCommand

def compute():
    existing_prescribe = PrescribeCommand(command_uuid='e32b85d9-ccb7-4e4f-a0e5-8783ed2d9528')

    return [existing_prescribe.send(practice_location_override='a1b2c3d4-e5f6-7890-abcd-ef1234567890')]
```

- `practice_location_override` is the `id` of a [PracticeLocation](/sdk/data-practicelocation/#practicelocation). When set, that location's business name, phone, fax, and street address replace the prescriber's default on the outgoing prescription.
- If the id does not correspond to an existing practice location, the send raises an error rather than falling back to the default address.
- The override applies only to `send()`-initiated (plugin-driven) prescriptions. It does not affect prescriptions a clinician sends from the charting UI.


**Command-specific parameters**:

| Name                        | Type                          | Required to review / send | Description                                                         |
|-----------------------------|-------------------------------|----------|---------------------------------------------------------------------|
| `fdb_code`                  | _string_                      | `false`* | The [FDB code](/sdk/utils/#fdb_code) of the medication.             |
| `compound_medication_id`    | _string_                      | `false`* | The id of an existing [CompoundMedication](/sdk/data-compound-medication/#compoundmedication) to prescribe.             |
| `compound_medication_data`  | [`CompoundMedicationData`](#prescribe-compoundmedicationdata)      | `false`* | Data for creating a new compound medication inline.                 |
| `icd10_codes`               | _list[string]_                | `false`  | List of ICD-10 codes (maximum 2) associated with the prescription. Must be [Conditions](/sdk/data-condition/#condition) on the patient's active problem list.  |
| `sig`                       | _string_                      | `true`   | Administration instructions/details of the medication.              |
| `days_supply`               | _integer_                     | `false`  | Number of days the prescription is intended to cover.               |
| `quantity_to_dispense`      | _Decimal \| float \| integer_ | `true`   | The amount of medication to dispense.                               |
| `type_to_dispense`          | _[ClinicalQuantity](#clinicalquantity)_            | `true`** | Information about the form or unit of the medication to dispense. Get the available quantities from the [medication search](/sdk/utils/#searching-for-medications)'s `clinical_quantities`.   |
| `refills`                   | _integer_                     | `true`   | Number of refills allowed for the prescription.                     |
| `substitutions`             | _[Substitutions](#prescribe-substitutions) enum_          | `true`   | Specifies whether substitutions (e.g., generic drugs) are allowed.  |
| `pharmacy`                  | _string_                      | `false`  | The NCPDP ID of the pharmacy where the prescription should be sent. [Look it up via the pharmacy search](/sdk/utils/#searching-for-pharmacies). |
| `prescriber_id`             | _string_                      | `true`   | The [Staff](/sdk/data-staff/#staff) id of the prescriber.                                          |
| `supervising_provider_id`   | _string_                      | `false`   | The [Staff](/sdk/data-staff/#staff) id of the supervising provider of the prescriber.               |
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

<a id="prescribe-substitutions"></a>

| Substitutions | Value           | Description                                      |
|---------------|-----------------|--------------------------------------------------|
| `ALLOWED`     | `"allowed"`     | Generic or substitute medications are permitted. |
| `NOT_ALLOWED` | `"not_allowed"` | Only the prescribed brand is allowed.            |


<a id="prescribe-compoundmedicationdata"></a>

**CompoundMedicationData**:
Data for creating a compound medication inline within a prescription.

| Field Name                 | Type     | Description                                               | Required |
|----------------------------|----------|-----------------------------------------------------------|----------|
| `formulation`              | _string_ | The compound medication formulation (max 105 characters)  | `true`   |
| `potency_unit_code`        | _[PotencyUnit](/sdk/data-compound-medication/#potencyunit) value_ | The unit of measurement for the medication. | `true`   |
| `controlled_substance`     | _[ControlledSubstanceSchedule](/sdk/data-compound-medication/#controlledsubstanceschedule) value_ | The controlled substance schedule (`N` for none). | `true`   |
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
    pharmacy="pharmacy_ncpdp_id",
    prescriber_id="a7c2e9d1-3b4f-4a6c-8e0d-5f1a2b3c4d5e",
    supervising_provider_id='c3d4e5f6-7a8b-4c9d-0e1f-2a3b4c5d6e7f',
    note_to_pharmacist="Please verify patient's insurance before processing."
)
```

***Option 2: Existing Compound Medication (by ID)***

Note: `type_to_dispense` should not be provided for compound medications as this field will auto-populate in the command when it is inserted in the note
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
    refills=3,
    substitutions=PrescribeCommand.Substitutions.ALLOWED,
    pharmacy="pharmacy_ncpdp_id",
    prescriber_id="a7c2e9d1-3b4f-4a6c-8e0d-5f1a2b3c4d5e",
    supervising_provider_id='c3d4e5f6-7a8b-4c9d-0e1f-2a3b4c5d6e7f',
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
    refills=3,
    substitutions=PrescribeCommand.Substitutions.ALLOWED,
    pharmacy="pharmacy_ncpdp_id",
    prescriber_id="a7c2e9d1-3b4f-4a6c-8e0d-5f1a2b3c4d5e",
    supervising_provider_id='c3d4e5f6-7a8b-4c9d-0e1f-2a3b4c5d6e7f',
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

### PhysicalExam

**Note:** The PhysicalExamCommand is a subclass of the QuestionnaireCommand, so it supports all the questionnaire features (including response recording, question mapping, etc.). For detailed information on these features, please refer to the [Questionnaire Command Documentation](#questionnaire).

**Command-specific parameters**:

| Name               | Type     | Required to commit | Description                                                                     |
|:-------------------|:---------|:---------|:--------------------------------------------------------------------------------|
| `questionnaire_id` | _string_ | `true`   | The id of the [Questionnaire](/sdk/data-questionnaire/#questionnaire) being answered by the patient. |

<a id="toggle-questions"></a>
#### Toggle Questions Feature

The PhysicalExamCommand and the [ReviewOfSystemsCommand](#review-of-systems) both support toggling questions on/off, so practitioners can enable or disable specific questions based on patient relevance. The methods, property, and behavior described here are identical for both commands.

The following methods are available. In each, `question_id` is the [Question](/sdk/data-questionnaire/#question) `dbid` (an integer, accepted as `int` or `str`):

**Methods**:

| Method                      | Parameters                                 | Returns   | Description                                                |
|:----------------------------|:-------------------------------------------|:----------|:-----------------------------------------------------------|
| `is_question_enabled`       | `question_id: str` or `int`                | `bool`    | Check if a specific question is enabled (not skipped).     |
| `set_question_enabled`      | `question_id: str` or `int, enabled: bool` | `None`    | Enable or disable a specific question.                     |

**Properties**:

| Property           | Type   | Description                                            |
|:-------------------|:-------|:-------------------------------------------------------|
| `question_toggles` | `dict` | All current toggle states, mapping `question_id` → `enabled` — e.g. `{"12": True, "13": False, "14": True}`. |

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
        question_id = question.dbid
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
        question_id = question.dbid
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
existing_exam = PhysicalExamCommand(command_uuid='d4e5f6a7-8b9c-4d0e-1f2a-3b4c5d6e7f80')
# All previously set toggle states are automatically loaded
```

---


### Questionnaire

#### Overview

The `QuestionnaireCommand` is used to present a questionnaire to a patient and commit their responses to an interview. It requires the ID of the questionnaire

**Automatic Questionnaire ID Loading**: When instantiating a QuestionnaireCommand with an existing `command_uuid`, the questionnaire_id will be automatically loaded from the database if not explicitly provided. This means you don't need to specify the questionnaire_id when working with existing commands.

In addition to the basic parameters, this command supports a dynamic response interface. Once instantiated, you can retrieve the list of questions via the `questions` property, and then record responses for each question using the question object's `add_response()` method. Each question type enforces its expected response format:

- **Text questions (TYPE_TEXT):** Accept a keyword argument `text` (a string).
- **Integer questions (TYPE_INTEGER):** Accept a keyword argument `integer` (a value convertible to an integer; a non-convertible value raises an error).
- **Radio questions (TYPE_RADIO):** Accept a keyword argument `option` (a `ResponseOption` instance); only one option may be selected.
- **Checkbox questions (TYPE_CHECKBOX):** Accept a keyword argument `option` (a `ResponseOption` instance) along with an optional boolean `selected` (defaulting to True) and an optional string `comment`. Multiple responses can be recorded.


**Command-specific parameters**:

| Name               | Type     | Required to commit | Description                                                                     |
|:-------------------|:---------|:---------|:--------------------------------------------------------------------------------|
| `questionnaire_id` | _string_ | `true`   | The id of the [Questionnaire](/sdk/data-questionnaire/#questionnaire) being answered by the patient. |

**Example** — instantiating an empty questionnaire:

```python
from canvas_sdk.commands import QuestionnaireCommand

questionnaire = QuestionnaireCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    questionnaire_id='c1a2b3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d'
)
```

#### Usage Example

Below is an example that demonstrates how to instantiate a `QuestionnaireCommand`, retrieve the questions, and add responses to them based on their type:

```python
import uuid
from canvas_sdk.commands.commands.questionnaire import QuestionnaireCommand
from canvas_sdk.commands.commands.questionnaire.question import ResponseOption
from canvas_sdk.effects import Effect
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Note, Questionnaire

class MyHandler(BaseHandler):

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

#### Explanation

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

### ReasonForVisit

**Command-specific parameters**:

| Name         | Type                     | Required                  | Description                                                                                                                                                                                                                |
|:-------------|:-------------------------|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `structured` | _boolean_                | `false`                   | Whether the RFV is structured or not. Defaults to False.                                                                                                                                                                   |
| `coding`     | _[Coding](#coding)_ or _UUID (str)_ | `true` if structured=True | The coding for the structured RFV. Either a full [Coding](#coding) object (with `code`, `system`, `display`) or a UUID string referencing a verified coding record. If a [Coding](#coding) is provided, it is validated against existing [ReasonForVisitSettingCoding](/sdk/data-reason-for-visit/#reasonforvisitsettingcoding) records |
| `comment`    | _string_                 | `false`                   | Additional commentary on the RFV.                                                                                                                                                                                          |

**Example**:

```python
from canvas_sdk.commands import ReasonForVisitCommand

structured_rfv = ReasonForVisitCommand(
  note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
  structured=True,
  coding={'code': '49727002', 'system': 'http://snomed.info/sct', 'display': 'Cough'},
  comment='also wants to discuss treatment options'
)

# Example with a UUID string referencing a Coding record
structured_rfv2 = ReasonForVisitCommand(
  note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
  structured=True,
  coding="e2b1e1e3-3f52-4a0a-bb3a-123456789abc",  # Must correspond to an existing coding record
  comment="Discuss treatment options"
)

unstructured_rfv = ReasonForVisitCommand(
  note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
  comment='also wants to discuss treatment options'
)
```

### Refer

**Command-specific parameters**:

| Name                  | Type                    | Required to delegate / sign | Description                                                                                  |
|:----------------------|:------------------------|:---------|:---------------------------------------------------------------------------------------------|
| `service_provider`    | _[ServiceProvider](#serviceprovider)_       | `true`   | The service provider associated with the referral command. Search with the [contacts endpoint](/sdk/utils/#searching-for-contacts-and-service-providers).                                   |
| `diagnosis_codes`     | _list[string]_          | `true`   | A list of relevant ICD-10 Diagnosis. Search with the [ICD-10 condition endpoint](/sdk/utils/#get-icdcondition--icd-10-conditions).                                                         |
| `clinical_question`   | _[ClinicalQuestion](#refer-clinicalquestion) enum_ | `true`   | The clinical question prompting the referral. Must be one of [`ReferCommand.ClinicalQuestion`](#refer-clinicalquestion) |
| `priority`            | _[Priority](#refer-priority) enum_         | `false`  | Priority of the imaging order. Must be one of [`ReferCommand.Priority`](#refer-priority).                       |
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

<a id="refer-priority"></a>

**`Priority`**

| Priority  | Value       | Description                  |
|:----------|:------------|:-----------------------------|
| `ROUTINE` | `"Routine"` | A routine referral.          |
| `URGENT`  | `"Urgent"`  | An urgent referral.          |
| `STAT`    | `"STAT"`    | A STAT (immediate) referral. |

<a id="refer-clinicalquestion"></a>

**`ClinicalQuestion`**

| Clinical Question                    | Value                                      | Description                             |
|:-------------------------------------|:-------------------------------------------|:----------------------------------------|
| `COGNITIVE_ASSISTANCE`               | `"Cognitive Assistance (Advice/Guidance)"` | Cognitive assistance (advice/guidance). |
| `ASSISTANCE_WITH_ONGOING_MANAGEMENT` | `"Assistance with Ongoing Management"`     | Assistance with ongoing management.     |
| `SPECIALIZED_INTERVENTION`           | `"Specialized intervention"`               | Specialized intervention.               |
| `DIAGNOSTIC_UNCERTAINTY`             | `"Diagnostic Uncertainty"`                 | Diagnostic uncertainty.                 |


**Example**:

```python
from canvas_sdk.commands import ReferCommand
from canvas_sdk.commands.constants import ServiceProvider

refer_command = ReferCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
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

### ReferralReview

**Command-specific parameters**:

| Name                     | Type                                     | Required to commit | Description                                                                                                    |
|--------------------------|:-----------------------------------------|:---------|:---------------------------------------------------------------------------------------------------------------|
| `report_ids`             | _list[string]_                           | `true`   | List of [ReferralReport](/sdk/data-referral/#referralreport) IDs to review. Must be reports on that patient's chart.                                                                         |
| `message_to_patient`     | _string_                                 | `false`  | Message to communicate findings to the patient.                                                                |
| `communication_method`   | _[ReportReviewCommunicationMethod](#reportreviewcommunicationmethod) enum_   | `false`  | Method for patient communication. Must be one of [`ReportReviewCommunicationMethod`](#reportreviewcommunicationmethod).      |
| `linked_items_urns`      | _list[string]_                           | `false`  | List of URNs for items linked to the review.                                                                   |
| `comment`                | _string_                                 | `false`  | Internal comment about the review.                                                                             |

**Example**:

```python
from canvas_sdk.commands import ReferralReviewCommand
from canvas_sdk.commands.commands.review import ReportReviewCommunicationMethod
from canvas_sdk.v1.data import Patient, ReferralReport

patient = Patient.objects.get(id="patient-id")
# Get referral reports to review
referral_reports = ReferralReport.objects.filter(patient=patient, review__isnull=True, review_mode='RR')
report_ids = [str(report.id) for report in referral_reports]

referral_review = ReferralReviewCommand(
    note_uuid="a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
    report_ids=report_ids,
    message_to_patient="Your referral has been reviewed and approved.",
    communication_method=ReportReviewCommunicationMethod.DELEGATED_CALL_CAN_LEAVE_MESSAGE,
    comment="Referral approved, patient notified."
)
```

---

### Refill

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
    pharmacy="pharmacy_ncpdp_id",
    prescriber_id="a7c2e9d1-3b4f-4a6c-8e0d-5f1a2b3c4d5e",
    supervising_provider_id="c3d4e5f6-7a8b-4c9d-0e1f-2a3b4c5d6e7f",
    note_to_pharmacist="Please verify patient's insurance before processing."
)
```

---

### RemoveAllergy

**Command-specific parameters**:

| Name         | Type     | Required to commit | Description                                      |
|--------------|----------|----------|--------------------------------------------------|
| `allergy_id` | _string_ | `true`   | The id of the [AllergyIntolerance](/sdk/data-allergy-intolerance/#allergyintolerance) to remove. Must be an allergy already recorded on that patient's chart.        |
| `narrative`  | _string_ | `false`  | Additional context or narrative for the removal. |

**Example**:

```python
from canvas_sdk.commands import RemoveAllergyCommand

RemoveAllergyCommand(
    allergy_id="e5f6a7b8-9c0d-4e1f-a2b3-c4d5e6f7a8b9",
    narrative="Allergy no longer applies after reassessment."
)
```

---

### Resolve Condition

**Command-specific parameters**:

| Name                     | Type      | Required to commit | Description                                                                |
|--------------------------|-----------|----------|----------------------------------------------------------------------------|
| `condition_id`           | _string_  | `true`   | The id of the [Condition](/sdk/data-condition/#condition) being resolved. Must be a condition already recorded on that patient's chart.               |
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
   note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
)
```

---

### Review of Systems

**Command-specific parameters**:

| Name               | Type     | Required to commit | Description                                                                     |
|:-------------------|:---------|:---------|:--------------------------------------------------------------------------------|
| `questionnaire_id` | _string_ | `true`   | The id of the [Questionnaire](/sdk/data-questionnaire/#questionnaire) being answered by the patient. |


#### Toggle Questions Feature

The ReviewOfSystemsCommand supports the same question-toggling functionality as the PhysicalExamCommand, allowing practitioners to enable or disable specific system-review questions based on patient relevance. The available methods (`is_question_enabled`, `set_question_enabled`) and the `question_toggles` property are documented once under the [PhysicalExam Toggle Questions Feature](#toggle-questions) — they behave identically here.

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
existing_ros = ReviewOfSystemsCommand(command_uuid='d4e5f6a7-8b9c-4d0e-1f2a-3b4c5d6e7f80')
# All previously set toggle states are automatically loaded
```

**Note:** The ReviewOfSystemsCommand is a subclass of the QuestionnaireCommand, so it supports all the questionnaire features (including response recording, question mapping, etc.). For detailed information on these features, please refer to the [Questionnaire Command Documentation](#questionnaire).

---


### StopMedication

**Command-specific parameters**:

| Name            | Type     | Required to commit | Description                                                        |
|:----------------|:---------|:---------|:-------------------------------------------------------------------|
| `medication_id` | _string_ | `true`   | The id of the [Medication](/sdk/data-medication/#medication) being stopped. Must be a medication already recorded on that patient's chart. |
| `rationale`     | _string_ | `false`  | The reason for stopping the medication.                            |

**Example**:

```python
from canvas_sdk.commands import StopMedicationCommand

stop_medication = StopMedicationCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    medication_id='f0a1b2c3-d4e5-4f6a-8b9c-0d1e2f3a4b5c',
    rationale='In remission'
)
```

---

### StructuredAssessment

**Command-specific parameters**:

| Name               | Type     | Required to commit | Description                                                                     |
|:-------------------|:---------|:---------|:--------------------------------------------------------------------------------|
| `questionnaire_id` | _string_ | `true`   | The id of the [Questionnaire](/sdk/data-questionnaire/#questionnaire) being answered by the patient. |

**Note:** The StructuredAssessmentCommand is a subclass of the QuestionnaireCommand, so it supports all the questionnaire features (including response recording, question mapping, etc.). For detailed information on these features, please refer to the [Questionnaire Command Documentation](#questionnaire).

**Example**:

```python
from canvas_sdk.commands import StructuredAssessmentCommand

questionnaire = StructuredAssessmentCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    questionnaire_id='c1a2b3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d'
)
```

---

### Task

**Command-specific parameters**:

| Name                | Type           | Required to commit | Description                                         |
|---------------------|----------------|----------|-----------------------------------------------------|
| `title`             | _string_       | `true`   | The title or summary of the task.                   |
| `assign_to`         | _[TaskAssigner](#taskassigner)_ | `true`   | Specifies the assignee (role, team, or individual). |
| `due_date`          | _date_         | `false`  | Due date for completing the task.                   |
| `priority`          | _[TaskPriority](#taskpriority) enum_ | `false` | Priority of the task. Must be one of [`TaskPriority`](#taskpriority). |
| `comment`           | _string_       | `false`  | Additional comments or notes about the task.        |
| `labels`            | _list[string]_ | `false`  | Labels to apply to the task. Each value is matched (case-insensitive) against an existing [TaskLabel](/sdk/data-task/#tasklabel) by name; values that don't match an existing label are ignored. |
| `linked_items_urns` | _list[string]_ | `false`  | URNs for items linked to the task.                  |

**Enums and Types**:

<a id="taskpriority"></a>
**`TaskPriority`**

| Priority  | Description                                                                                |
|-----------|--------------------------------------------------------------------------------------------|
| `STAT`    | The request should be actioned immediately — highest possible priority. E.g. an emergency. |
| `URGENT`  | The request should be actioned promptly — higher priority than routine.                    |
| `ROUTINE` | The request has normal priority.                                                           |

<a id="taskassigner"></a>
**TaskAssigner Type**:

| Key  | Type           | Required | Description                                |
|------|----------------|----------|--------------------------------------------|
| `to` | _[AssigneeType](#assigneetype)_ | `true`   | Type of assignee (e.g., role, team, etc.). |
| `id` | _integer_      | `false`  | The `dbid` of the assignee, in the table selected by `to`: a [CareTeamRole](/sdk/data-care-team/#careteamrole) when `to` is `ROLE`, a [Team](/sdk/data-team/#team) when `to` is `TEAM`, or a [Staff](/sdk/data-staff/#staff) when `to` is `STAFF`. Omit when `to` is `UNASSIGNED`. |

<a id="assigneetype"></a>

| AssigneeType | Value          | Description                               |
|--------------|----------------|-------------------------------------------|
| `ROLE`       | `"role"`       | Task assigned to a specific [CareTeamRole](/sdk/data-care-team/#careteamrole) (`id` is the role's `dbid`). |
| `TEAM`       | `"team"`       | Task assigned to a specific [Team](/sdk/data-team/#team) (`id` is the team's `dbid`).         |
| `UNASSIGNED` | `"unassigned"` | Task is unassigned.                       |
| `STAFF`      | `"staff"`      | Task assigned to a specific [Staff](/sdk/data-staff/#staff) member (`id` is the staff member's `dbid`). |


**Example**:

```python
from canvas_sdk.commands import TaskCommand
from canvas_sdk.commands.commands.task import TaskAssigner, AssigneeType
from canvas_sdk.v1.data.task import TaskPriority
from datetime import date

TaskCommand(
    title="Follow-up appointment scheduling",
    assign_to=TaskAssigner(to=AssigneeType.STAFF, id=123),
    due_date=date(2024, 12, 15),
    priority=TaskPriority.URGENT,
    comment="Ensure the patient schedules a follow-up within 30 days.",
    labels=["Urgent"],
    linked_items_urns=["urn:task:123", "urn:note:456"]
)
```


---

### UncategorizedDocumentReview

**Command-specific parameters**:

| Name                     | Type                                     | Required to commit | Description                                                                                                    |
|--------------------------|:-----------------------------------------|:---------|:---------------------------------------------------------------------------------------------------------------|
| `report_ids`             | _list[string]_                           | `true`   | List of [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/#uncategorizedclinicaldocument) ids to review. Must be documents already on that patient's chart.                                                                  |
| `message_to_patient`     | _string_                                 | `false`  | Message to communicate findings to the patient.                                                                |
| `communication_method`   | _[ReportReviewCommunicationMethod](#reportreviewcommunicationmethod) enum_   | `false`  | Method for patient communication. Must be one of [`ReportReviewCommunicationMethod`](#reportreviewcommunicationmethod).                            |
| `linked_items_urns`      | _list[string]_                           | `false`  | List of URNs for items linked to the review.                                                                   |
| `comment`                | _string_                                 | `false`  | Internal comment about the review.                                                                             |

**Example**:

```python
from canvas_sdk.commands import UncategorizedDocumentReviewCommand
from canvas_sdk.v1.data import UncategorizedClinicalDocument, Patient
from canvas_sdk.commands.commands.review import ReportReviewCommunicationMethod

patient = Patient.objects.last()
# Get uncategorized documents to review
uncategorized_documents = UncategorizedClinicalDocument.objects.filter(patient=patient, review__isnull=True, review_mode='RR')
report_ids = [str(doc.id) for doc in uncategorized_documents]

uncategorized_review = UncategorizedDocumentReviewCommand(
    note_uuid="a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
    report_ids=report_ids,
    message_to_patient="Your document has been reviewed.",
    communication_method=ReportReviewCommunicationMethod.DELEGATED_CALL_CAN_LEAVE_MESSAGE,
    comment="Document reviewed, no further action needed."
)
```

---

### UpdateDiagnosis

**Command-specific parameters**:

| Name                 | Type     | Required to commit | Description                                                       |
|----------------------|----------|----------|-------------------------------------------------------------------|
| `condition_code`     | _string_ | `true`   | The ICD-10 code of the existing diagnosis to update. Must match a [Condition](/sdk/data-condition/#condition) already on that patient's chart.              |
| `new_condition_code` | _string_ | `true`   | The new ICD-10 code to replace the existing diagnosis, looked up via [`GET /icd/condition/`](/sdk/utils/#get-icdcondition--icd-10-conditions).  |
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

### UpdateGoal

**Command-specific parameters**:

| Name                 | Type                     | Required to commit | Description                                               |
|:---------------------|:-------------------------|:---------|:----------------------------------------------------------|
| `goal_id`            | _string_                 | `true`   | The `dbid` of the [Goal](/sdk/data-goal/#goal) being updated. Must be a goal on that patient's chart.        |
| `due_date`           | _datetime_               | `false`  | The date the goal is due.                                 |
| `achievement_status` | _[AchievementStatus](#updategoal-achievementstatus) enum_ | `false`  | The current achievement status of the goal.               |
| `priority`           | _[Priority](#updategoal-priority) enum_          | `false`  | The priority of the goal.                                 |
| `progress`           | _string_                 | `false`  | A narrative about the patient's progress toward the goal. |

<a id="updategoal-achievementstatus"></a>

| `AchievementStatus` | Value              | Description                                |
|:--------------------|:-------------------|:-------------------------------------------|
| `IN_PROGRESS`       | `"in-progress"`    | The goal is being pursued.                 |
| `IMPROVING`         | `"improving"`      | Progress toward the goal is improving.     |
| `WORSENING`         | `"worsening"`      | Progress toward the goal is worsening.     |
| `NO_CHANGE`         | `"no-change"`      | No change in progress toward the goal.     |
| `ACHIEVED`          | `"achieved"`       | The goal has been achieved.                |
| `SUSTAINING`        | `"sustaining"`     | The achieved goal is being sustained.      |
| `NOT_ACHIEVED`      | `"not-achieved"`   | The goal was not achieved.                 |
| `NO_PROGRESS`       | `"no-progress"`    | No progress has been made toward the goal. |
| `NOT_ATTAINABLE`    | `"not-attainable"` | The goal is not attainable.                |

<a id="updategoal-priority"></a>

| `Priority` | Value               | Description      |
|:-----------|:--------------------|:-----------------|
| `HIGH`     | `"high-priority"`   | High priority.   |
| `MEDIUM`   | `"medium-priority"` | Medium priority. |
| `LOW`      | `"low-priority"`    | Low priority.    |

**Example**:

```python
from canvas_sdk.commands import UpdateGoalCommand, GoalCommand
from datetime import datetime

update_goal = UpdateGoalCommand(
    note_uuid='8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47',
    goal_id='b7c8d9e0-1a2b-4c3d-5e6f-7a8b9c0d1e2f',
    due_date=datetime(2025, 3, 31),
    achievement_status=GoalCommand.AchievementStatus.WORSENING,
    priority=GoalCommand.Priority.MEDIUM,
    progress='patient has slowed down progress and requesting to move due date out'
)
```

---

### Vitals

**Command-specific parameters**:

| Name                               | Type      | Required to commit | Description                                      |
|------------------------------------|-----------|----------|--------------------------------------------------|
| `height`                           | _integer_ | `false`  | Height in inches.                                |
| `weight_lbs`                       | _integer_ | `false`  | Weight in pounds.                                |
| `weight_oz`                        | _integer_ | `false`  | Weight in ounces.                                |
| `waist_circumference`              | _integer_ | `false`  | Waist circumference in inches.                   |
| `body_temperature`                 | _float_   | `false`  | Body temperature in Fahrenheit.                  |
| `body_temperature_site`            | _[BodyTemperatureSite](#bodytemperaturesite)_    | `false`  | Site of body temperature measurement.            |
| `blood_pressure_systole`           | _integer_ | `false`  | Systolic blood pressure.                         |
| `blood_pressure_diastole`          | _integer_ | `false`  | Diastolic blood pressure.                        |
| `blood_pressure_position_and_site` | _[BloodPressureSite](#bloodpressuresite)_    | `false`  | Position and site of blood pressure measurement. |
| `pulse`                            | _integer_ | `false`  | Pulse rate in beats per minute.                  |
| `pulse_rhythm`                     | _[PulseRhythm](#pulserhythm)_    | `false`  | Rhythm of the pulse.                             |
| `respiration_rate`                 | _integer_ | `false`  | Respiration rate in breaths per minute.          |
| `oxygen_saturation`                | _integer_ | `false`  | Oxygen saturation in percentage.                 |
| `supplemental_oxygen`              | _[SupplementalOxygen](#supplementaloxygen)_    | `false`  | Type of supplemental oxygen the patient is receiving. |
| `note`                             | _string_  | `false`  | Additional notes (max length: 150 characters).   |

**Enums and Types**:

<a id="bodytemperaturesite"></a>

| BodyTemperatureSite | Value | Description                          |
|---------------------|-------|--------------------------------------|
| `AXILLARY`          | `0`   | Measurement taken from the armpit.   |
| `ORAL`              | `1`   | Measurement taken from the mouth.    |
| `RECTAL`            | `2`   | Measurement taken from the rectum.   |
| `TEMPORAL`          | `3`   | Measurement taken from the forehead. |
| `TYMPANIC`          | `4`   | Measurement taken from the ear.      |


<a id="bloodpressuresite"></a>

| BloodPressureSite      | Value | Description                         |
|------------------------|-------|-------------------------------------|
| `SITTING_RIGHT_UPPER`  | `0`   | Sitting position, right upper arm.  |
| `SITTING_LEFT_UPPER`   | `1`   | Sitting position, left upper arm.   |
| `STANDING_RIGHT_UPPER` | `4`   | Standing position, right upper arm. |
| `SUPINE_LEFT_LOWER`    | `11`  | Supine position, left lower arm.    |


<a id="pulserhythm"></a>

| PulseRhythm             | Value | Description                  |
|-------------------------|-------|------------------------------|
| `REGULAR`               | `0`   | Regular rhythm.              |
| `IRREGULARLY_IRREGULAR` | `1`   | Completely irregular rhythm. |
| `REGULARLY_IRREGULAR`   | `2`   | Regularly irregular rhythm.  |


<a id="supplementaloxygen"></a>

| SupplementalOxygen     | Value           | Description                               |
|------------------------|-----------------|-------------------------------------------|
| `CONTINUOUS_HIGH_FLOW` | `"LA28684-1"`   | Continuous high-flow supplemental oxygen. |
| `CONTINUOUS_LOW_FLOW`  | `"LA28685-8"`   | Continuous low-flow supplemental oxygen.  |
| `INTERMITTENT`         | `"LA28686-6"`   | Intermittent supplemental oxygen.         |

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
    supplemental_oxygen=VitalsCommand.SupplementalOxygen.INTERMITTENT,
    note="Vitals are within normal range."
)
```

## Command Constants

The `canvas_sdk.commands.constants` module provides essential classes and enumerations used across various Canvas SDK command implementations. These constants ensure consistency and provide structured data types for common medical and administrative elements.

### ClinicalQuantity

`ClinicalQuantity` represents detailed information about the form or unit of medication, particularly for prescription-related commands.

| Field Name                      | Type     | Required | Description                                           |
|---------------------------------|----------|----------|-------------------------------------------------------|
| `representative_ndc`            | _string_ | `true`   | National Drug Code (NDC) representing the medication. |
| `ncpdp_quantity_qualifier_code` | _string_ | `true`   | NCPDP code indicating the quantity qualifier.         |
| `description`                   | _string_ | `false`  | The clinical quantity description to dispense (e.g. `"0.5 mL vial"`). Use this field to narrow the selection to the correct clinical quantity when multiple options are available for the same NDC and qualifier code. If omitted, the first available clinical quantity is used. |

These values come from the `clinical_quantities` array returned by the [medication search](/sdk/utils/#searching-for-medications): `representative_ndc` ← `representative_ndc`, `ncpdp_quantity_qualifier_code` ← `erx_ncpdp_script_quantity_qualifier_code`, and `description` ← `clinical_quantity_description`.

**Usage Example**:

```python
from canvas_sdk.commands import PrescribeCommand
from canvas_sdk.commands.constants import ClinicalQuantity

# Without description — selects the first available clinical quantity
clinical_quantity = ClinicalQuantity(
    representative_ndc="12843016128",
    ncpdp_quantity_qualifier_code="C48542"
)

# With description — narrows to the correct clinical quantity when multiple options share the same NDC and qualifier code
clinical_quantity = ClinicalQuantity(
    representative_ndc="00002024304",
    ncpdp_quantity_qualifier_code="C28254",
    description="0.5 mL vial"
)

prescribe = PrescribeCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
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
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
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

| Code System        | System URI                                          | Description                                                         |
|--------------------|-----------------------------------------------------|---------------------------------------------------------------------|
| `SNOMED`           | `http://snomed.info/sct`                            | Systematized Nomenclature of Medicine Clinical Terms                |
| `RXNORM`           | `http://www.nlm.nih.gov/research/umls/rxnorm`       | RxNorm — standardized nomenclature for medications                  |
| `LOINC`            | `http://loinc.org`                                  | Logical Observation Identifiers Names and Codes (labs/observations) |
| `FDB`              | `http://www.fdbhealth.com/`                         | First Databank drug knowledge base                                  |
| `ICD10`            | `ICD-10`                                            | International Classification of Diseases, 10th Revision             |
| `CVX`              | `http://hl7.org/fhir/sid/cvx`                       | CDC codes for administered vaccines                                 |
| `CPT`              | `http://www.ama-assn.org/go/cpt`                    | Current Procedural Terminology (AMA procedure codes)                |
| `NUCC`             | `http://www.nucc.org/`                              | National Uniform Claim Committee provider taxonomy codes            |
| `NDC`              | `http://hl7.org/fhir/sid/ndc`                       | National Drug Code                                                  |
| `HCPCS`            | `http://www.cms.gov/medicare/coding/medhcpcsgeninfo`| Healthcare Common Procedure Coding System                           |
| `UNITS_OF_MEASURE` | `http://unitsofmeasure.org`                         | Unified Code for Units of Measure (UCUM)                            |
| `FULLSCRIPT`       | `http://fullscript.com`                             | Fullscript supplement/dispensary code system                        |
| `UNSTRUCTURED`     | `UNSTRUCTURED`                                      | Canvas-specific system for unstructured or custom codes             |

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
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    coding=Coding(
        system=CodeSystems.SNOMED,
        code="65921008",
        display="Drink plenty of fluids"
    ),
    comment="To address mild dehydration symptoms"
)

# Using unstructured coding for custom instructions
instruct_custom = InstructCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    coding=Coding(
        system=CodeSystems.UNSTRUCTURED,
        code="Physical medicine neuromuscular training"
    )
)
```

### ReportReviewCommunicationMethod

The `communication_method` value shared by the review commands — [ImagingReview](#imagingreview), [LabReview](#labreview), [ReferralReview](#referralreview), and [UncategorizedDocumentReview](#uncategorizeddocumentreview).

```python
from canvas_sdk.commands.commands.review import ReportReviewCommunicationMethod
```

| Communication Method                | Value | Description                                                |
|:------------------------------------|:------|:-----------------------------------------------------------|
| `DELEGATED_CALL_CAN_LEAVE_MESSAGE`  | `"DM"`| Delegated call - can leave message                         |
| `DELEGATED_CALL_NEED_ANSWER`        | `"DA"`| Delegated call - need answer                               |
| `DELEGATED_LETTER`                  | `"DL"`| Delegated letter to be sent to patient                     |
| `ALREADY_LEFT_MESSAGE`              | `"AM"`| Already left message for patient                           |
| `ALREADY_REVIEWED_WITH_PATIENT`     | `"AR"`| Already reviewed with patient                              |

<br/>
<br/>
<br/>

