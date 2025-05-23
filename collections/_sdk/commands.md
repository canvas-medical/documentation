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

Command-specific details for each command class can be found below.

## AdjustPrescription

**Command-specific parameters**:

| Name           | Type     | Required | Description                          |
|:---------------|:---------|:---------|:-------------------------------------|
| `new_fdb_code` | _string_ | `true`   | The FDB code for the new medication. |

Check the [Prescribe](#prescribe) command for the other parameters used in the Refill command.

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
from canvas_sdk.commands import AllergyCommand, AllergenType, Allergen 
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
from canvas_sdk.commands import ChangeMedicationCommand

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
| `coding`         | _Coding_ or _UUID (str)_ | `true` if structured=True | The coding for the structured RFV. Either a full Coding object (with `code`, `system`, `display`) or a UUID string referencing a verified coding record. If a Coding is provided, it is validated against existing records |
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
| `service_provider`      | _ServiceProvider_ | `true`   | Service provider of the imaging order.                                        |
| `comment`               | _string_          | `false`  | Additional comments.                                                          |
| `ordering_provider_key` | _string_          | `true`   | The key for the provider ordering the imaging.                                |
| `linked_items_urns`     | _list[string]_    | `false`  | List of URNs for items linked to the imaging order command.                   |

**Enums and Types**:

**`Priority`**

| Priority  | Description                |
|:----------|:---------------------------|
| `ROUTINE` | Indicates a routine order. |
| `URGENT`  | Indicates un urgent order. |

**`ServiceProvider`**:

Represents the detailed information of the service provider.

| Field Name       | Type               | Description                                            |
|------------------|--------------------|--------------------------------------------------------|
| first_name       | _string_           | Service provider's first name (max length 512)         |
| last_name        | _string_           | Service provider's last name (max length 512)          |
| specialty        | _string_           | Provider's specialty (max length 512)                  |
| practice_name    | _string_           | Name of the practice (max length 512)                  |
| business_fax     | _Optional[string]_ | Business fax number (optional, max length 512)         |
| business_phone   | _Optional[string]_ | Business phone number (optional, max length 512)       |
| business_address | _Optional[string]_ | Business address (optional, max length 512)            |
| notes            | _Optional[string]_ | Additional notes (optional, max length 512)            |
 
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

## Instruct

**Command-specific parameters**:

| Name      | Type       | Required | Description                                                           |
|-----------|------------|----------|-----------------------------------------------------------------------|
| `coding`  | __Coding__ | `true`   | The SNOMED code or UNSTRUCTURED code that represents the instruction. |
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

**Command-specific parameters**:

| Name                    | Type           | Required | Description                                                                                                                                                      |
|-------------------------|----------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `lab_partner`           | _string_       | `true`   | The lab partner processing the order. Accepts either the lab partner’s name or its unique identifier (ID).                                                       |
| `tests_order_codes`     | _list[string]_ | `true`   | A list of codes or IDs for the tests being ordered. The system verifies that each provided value corresponds to an available test for the specified lab partner. |
| `ordering_provider_key` | _string_       | `false`  | The key for the provider ordering the tests.                                                                                                                     |
| `diagnosis_codes`       | _list[string]_ | `false`  | ICD-10 Diagnosis codes justifying the lab order.                                                                                                                 |
| `fasting_required`      | _boolean_      | `false`  | Indicates if fasting is required for the tests.                                                                                                                  |
| `comment`               | _string_       | `false`  | Additional comments related to the lab order.                                                                                                                    |

## Validations

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
| `fdb_code` | _string_ | `true`   | The fdb code of the medication.           |
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

**Command-specific parameters**:

| Name                   | Type                          | Required | Description                                                        |
|------------------------|-------------------------------|----------|--------------------------------------------------------------------|
| `fdb_code`             | _string_                      | `true`   | FDB code for the medication.                                       |
| `icd10_codes`          | _list[string]_                | `false`  | List of ICD-10 codes (maximum 2) associated with the prescription. |
| `sig`                  | _string_                      | `true`   | Administration instructions/details of the medication.             |
| `days_supply`          | _integer_                     | `false`  | Number of days the prescription is intended to cover.              |
| `quantity_to_dispense` | _Decimal \| float \| integer_ | `true`   | The amount of medication to dispense.                              |
| `type_to_dispense`     | _ClinicalQuantity_            | `true`   | Information about the form or unit of the medication to dispense.  |
| `refills`              | _integer_                     | `true`   | Number of refills allowed for the prescription.                    |
| `substitutions`        | _Substitutions Enum_          | `true`   | Specifies whether substitutions (e.g., generic drugs) are allowed. |
| `pharmacy`             | _string_                      | `false`  | The NCPDP ID of the pharmacy where the prescription should be sent.    |
| `prescriber_id`        | _string_                      | `true`   | The key of the prescriber.                     |
| `supervising_provider_id` | _string_                   | `true`   | The key of the supervising provider of the presciber.           |
| `note_to_pharmacist`   | _string_                      | `false`  | Additional notes or instructions for the pharmacist.               |

**Enums and Types**

| Substitutions | Value           | Description                                      |
|---------------|-----------------|--------------------------------------------------|
| `ALLOWED`     | `"allowed"`     | Generic or substitute medications are permitted. |
| `NOT_ALLOWED` | `"not_allowed"` | Only the prescribed brand is allowed.            |

**ClinicalQuantity**:

Represents the detailed information about the form or unit of the medication.

| Field Name                      | Type     | Description                                           |
|---------------------------------|----------|-------------------------------------------------------|
| `representative_ndc`            | _string_ | National Drug Code (NDC) representing the medication. |
| `ncpdp_quantity_qualifier_code` | _string_ | NCPDP code indicating the quantity qualifier.         |


**Example**

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

---

## PhysicalExam

**Command-specific parameters**:

| Name               | Type     | Required | Description                                                                     |
|:-------------------|:---------|:---------|:--------------------------------------------------------------------------------|
| `questionnaire_id` | _string_ | `true`   | The externally exposable id of the questionnaire being answered by the patient. |
| `result`           | _string_ | `false`  | A summary of the result of the patient's answers.                               |

**Example**:

```python
from canvas_sdk.commands import PhysicalExamCommand

questionnaire = PhysicalExamCommand(
    note_uuid='rk786p',
    questionnaire_id='g73hd9',
    result='The patient is feeling average today.'
)
```

**Note:** The PhysicalExamCommand is a subclass of the QuestionnaireCommand, so it supports all the questionnaire features (including response recording, question mapping, etc.). For detailed information on these features, please refer to the [Questionnaire Command Documentation](#questionnaire).

---


## Questionnaire

### Overview

The `QuestionnaireCommand` is used to present a questionnaire to a patient and commit their responses to an interview. It requires the ID of the questionnaire

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

## Usage Example

Below is an example that demonstrates how to instantiate a `QuestionnaireCommand`, retrieve the questions, and add responses to them based on their type:

```python
import uuid
from canvas_sdk.commands.questionnaire import QuestionnaireCommand
from canvas_sdk.commands.questionnaire.question import ResponseOption
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Note

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
          if question.type == RO.TYPE_TEXT:
              # For text questions, pass a 'text' keyword argument.
              question.add_response(text=f"Thanks for all the fish")
          elif question.type == RO.TYPE_INTEGER:
              # For integer questions, pass an 'integer' keyword argument.
              question.add_response(integer=42)
          elif question.type == RO.TYPE_RADIO:
              # For radio questions, pass an 'option' keyword argument (a ResponseOption instance).
              first_option = question.options[0]
              question.add_response(option=first_option)
          elif question.type == RO.TYPE_CHECKBOX:
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

---

## ReasonForVisit

**Command-specific parameters**:

| Name         | Type                     | Required                  | Description                                                                                                                                                                                                                |
|:-------------|:-------------------------|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `structured` | _boolean_                | `false`                   | Whether the RFV is structured or not. Defaults to False.                                                                                                                                                                   |
| `coding`     | _Coding_ or _UUID (str)_ | `true` if structured=True | The coding for the structured RFV. Either a full Coding object (with `code`, `system`, `display`) or a UUID string referencing a verified coding record. If a Coding is provided, it is validated against existing records |
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
| `service_provider`    | _ServiceProvider_       | `true`   | The service provider associated with the referral command.                                   |
| `diagnosis_codes`     | _list[string]_          | `true`   | A list of relevant ICD-10 Diagnosis.                                                         |
| `clinical_question`   | _ClinicalQuestion enum_ | `true`   | The clinical question prompting the referral. Must be one of `ReferCommand.ClinicalQuestion` |
| `priority`            | _Priority enum_         | `false`  | Priority of the imaging order. Must be one of `ReferCommand.Priority`.                       |
| `notes_to_specialist` | _string_                | `true`   | Notes or additional information directed to the specialist.                                  | 
| `include_visit_note`  | _boolean_               | `false`  | Flag indicating whether the visit note should be included in the referral.                   |
| `comment`             | _string_                | `false`  | An optional comment providing further details about the referral.                            |
| `linked_items_urns`   | _list[string]_          | `false`  | List of URNs for items linked to the referral command.                                       |

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


**`ServiceProvider`**:

Represents the detailed information of the service provider.

| Field Name       | Type               | Description                                            |
|------------------|--------------------|--------------------------------------------------------|
| first_name       | _string_           | Service provider's first name (max length 512)         |
| last_name        | _string_           | Service provider's last name (max length 512)          |
| specialty        | _string_           | Provider's specialty (max length 512)                  |
| practice_name    | _string_           | Name of the practice (max length 512)                  |
| business_fax     | _Optional[string]_ | Business fax number (optional, max length 512)         |
| business_phone   | _Optional[string]_ | Business phone number (optional, max length 512)       |
| business_address | _Optional[string]_ | Business address (optional, max length 512)            |
| notes            | _Optional[string]_ | Additional notes (optional, max length 512)            |
 
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
from canvas_sdk.commands.commands import ResolveConditionCommand
from canvas_sdk.v1.data import Condition

patient_condition = Condition.objects.for_patient(self.event.context["patient"]["id"]).committed().active().first()

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

**Example**:

```python
from canvas_sdk.commands import ReviewOfSystemsCommand

questionnaire = ReviewOfSystemsCommand(
    note_uuid='rk786p',
    questionnaire_id='g73hd9',
    result='The patient is feeling average today.'
)
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
