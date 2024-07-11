---
title: "Commands"
---

{% include alert.html type="info" content= "<b>Work in progress: </b> The effects returned by these objects will be of limited value until commands update live in the note. We are working on this in order to enable you to create co-charting plugins."  %}

The commands module lets you define commands within a specific note in Canvas, which capture and display data. Each command can be imported into a plugin and used to build a new, or reference an existing, command instance within a specific note.

The following commands are available for use in this module:

- [Assess](#assess)
- [Diagnose](#diagnose)
- [Goal](#goal)
- [HistoryOfPresentIllness](#historyofpresentillness)
- [MedicationStatement](#medicationstatement)
- [Plan](#plan)
- [Prescribe](#prescribe)
- [Questionnaire](#questionnaire)
- [ReasonForVisit](#reasonforvisit)
- [StopMedication](#stopmedication)
- [UpdateGoal](#updategoal)

## Common Attributes

### Parameters

All commands share the following init kwarg parameters:

| Name           | Type     | Required                               | Description                                                             |
| :------------- | :------- | :------------------------------------- | :---------------------------------------------------------------------- |
| `user_id`      | _string_ | `true`                                 | The externally exposable id of the user performing the command action.  |
| `note_uuid`      | _string_ | `true` if creating a new command       | The externally exposable id of the note in which to insert the command. |
| `command_uuid` | _string_ | `true` if updating an existing command | The externally exposable id of the command which is being referenced.   |

All parameters can be set upon initialization, and also updated on the class instance.

### Methods

All commands have the following methods:

#### originate

Returns an Effect that originates a new command in the note body.

#### edit

Returns an Effect that edits an existing command with the values set on the command class instance.

#### delete

Returns an Effect that deletes an existing, non-committed command from the note body.

#### commit

Returns an Effect that commits an existing, non-committed command to the note body.

#### enter_in_error

Returns an effect that enter-in-errors an existing, committed command in the note body.

**Example**:

```python
from canvas.commands import PlanCommand

def compute():

    existing_plan = PlanCommand(user_id='fg787uu', command_uuid='63hdik', narrative='something new')
    new_plan = PlanCommand(user_id='fg787uu', note_uuid='rk786p', narrative='new')
    new_plan.narrative = 'newer'

    return [existing_plan.edit(), new_plan.originate()]
```

Command-specific details for each command class can be found below.

## Assess

**Command-specific parameters**:

| Name           | Type          | Required | Description                                                                |
| :------------- | :------------ | :------- | :------------------------------------------------------------------------- |
| `condition_id` | _string_      | `true`   | The externally exposable id of the condition being assessed.               |
| `background`   | _string_      | `false`  | Background information about the diagnosis.                                |
| `status`       | _Status enum_ | `false`  | The current status of the diagnosis. Must be one of `AssessCommand.Status` |
| `narrative`    | _string_      | `false`  | The narrative for the current assessment.                                  |
|                |

| `Status`     |                |
| :----------- | :------------- |
| IMPROVED     | "improved"     |
| STABLE       | "stable"       |
| DETERIORATED | "deteriorated" |

**Example**:

```python
from canvas.commands import AssessCommand

assess = AssessCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    condition_id='hu38rlo',
    background='started in 2012',
    status=AssessCommand.Status.STABLE,
    narrative='experiencing more pain lately'
)
```

## Diagnose

**Command-specific parameters**:

| Name                        | Type       | Required | Description                                                |
| :-------------------------- | :--------- | :------- | :--------------------------------------------------------- |
| `icd10_code`                | _string_   | `true`   | ICD-10 code of the condition being diagnosed.              |
| `background`                | _string_   | `false`  | Background information about the diagnosis.                |
| `approximate_date_of_onset` | _datetime_ | `false`  | The approximate date the condition began.                  |
| `today_assessment`          | _string_   | `false`  | The narrative for the initial assessment of the condition. |
|                             |

**Example**:

```python
from canvas.commands import DiagnoseCommand
from datetime import datetime

diagnose = DiagnoseCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    icd10_code='M54.50',
    background='lifted heavy box',
    approximate_date_of_onset=datetime(2012, 1, 1),
    today_assessment='unable to sleep lately'
)
```

## Goal

**Command-specific parameters**:

| Name                 | Type                     | Required | Description                                               |
| :------------------- | :----------------------- | :------- | :-------------------------------------------------------- |
| `goal_statement`     | _string_                 | `true`   | Description of the goal.                                  |
| `start_date`         | _datetime_               | `false`  | The date the goal begins.                                 |
| `due_date`           | _datetime_               | `false`  | The date the goal is due.                                 |
| `achievement_status` | _AchievementStatus enum_ | `false`  | The current achievement status of the goal.               |
| `priority`           | _Priority enum_          | `false`  | The priority of the goal.                                 |
| `progress`           | _string_                 | `false`  | A narrative about the patient's progress toward the goal. |
|                      |

| `AchievementStatus` |                  |
| :------------------ | :--------------- |
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
| :--------- | :---------------- |
| HIGH       | "high-priority"   |
| MEDIUM     | "medium-priority" |
| LOW        | "low-priority"    |

**Example**:

```python
from canvas.commands import GoalCommand
from datetime import datetime

goal = GoalCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    goal_statement='Eat more healthy vegetables.',
    start_date=datetime(2024, 1, 1),
    due_date=datetime(2024, 12, 31),
    achievement_status=GoalCommand.AchievementStatus.IN_PROGRESS,
    priority=GoalCommand.Priority.HIGH,
    progress='patient is frequenting local farmers market to find healthy options'
)
```

## HistoryOfPresentIllness

**Command-specific parameters**:

| Name        | Type     | Required | Description                                                |
| :---------- | :------- | :------- | :--------------------------------------------------------- |
| `narrative` | _string_ | `true`   | The narrative of the patient's history of present illness. |
|             |          |          |                                                            |

**Example**:

```python
from canvas.commands import HistoryOfPresentIllnessCommand

hpi = HistoryOfPresentIllnessCommand(
        user_id='fg787uu',
        note_uuid='rk786p',
        narrative='presents with chronic back pain and headaches'
    )
```

## MedicationStatement

**Command-specific parameters**:

| Name       | Type     | Required | Description                               |
| :--------- | :------- | :------- | :---------------------------------------- |
| `fdb_code` | _string_ | `true`   | The fdb code of the medication.           |
| `sig`      | _string_ | `false`  | Administration details of the medication. |
|            |          |          |                                           |

**Example**:

```python
from canvas.commands import MedicationStatementCommand

medication_statement = MedicationStatementCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    fdb_code='198698',
    sig='two pills taken orally'
)
```

## Plan

**Command-specific parameters**:

| Name        | Type     | Required | Description                          |
| :---------- | :------- | :------- | :----------------------------------- |
| `narrative` | _string_ | `true`   | The narrative of the patient's plan. |
|             |          |          |                                      |

**Example**:

```python
from canvas.commands import PlanCommand

plan = PlanCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    narrative='will return in 2 weeks to check on pain management'
)
```

## Prescribe

**Command-specific parameters**:

| Name                   | Type                 | Required | Description                                                                 |
| :--------------------- | :------------------- | :------- | :-------------------------------------------------------------------------- |
| `fdb_code`             | _string_             | `true`   | The fdb code of the medication.                                             |
| `icd10_codes`          | _list[string]_       | `false`  | A list of ICD-10 codes representing the indications for the prescription.   |
| `sig`                  | _string_             | `true`   | Administration instructions/details of the medication.                      |
| `days_supply`          | _integer_            | `false`  | The number of days that the prescription should last.                       |
| `quantity_to_dispense` | _Decimal_            | `true`   | How much of the medication to dispense.                                     |
| `type_to_dispense`     | _string_             | `true`   | The unit which is dispensed.                                                |
| `refills`              | _integer_            | `true`   | The number of refills available to the patient.                             |
| `substitutions`        | _Substitutions enum_ | `false`  | The substitution status of the medication.                                  |
| `pharmacy`             | _string_             | `false`  | The name of the pharmacy to send the prescription to.                       |
| `prescriber_id`        | _string_             | `true`   | The externally exposable id of the provider prescribing the medication.     |
| `note_to_pharmacist`   | _string_             | `false`  | A freetext note to include for the pharmacist with additional instructions. |
|                        |                      |          |                                                                             |

| `Substitutions` |               |
| :-------------- | :------------ |
| ALLOWED         | "allowed"     |
| NOT_ALLOWED     | "not_allowed" |

**Example**:

```python
from canvas.commands import PrescribeCommand
from decimal import Decimal

prescribe = PrescribeCommand(
        user_id='fg787uu',
        note_uuid='rk786p',
        fdb_code='198698',
        icd10_codes=['M54.50'],
        sig='1 po bid pc',
        days_supply=10,
        quantity_to_dispense=Decimal(10),
        type_to_dispense='tablet',
        refills=1,
        substitutions=PrescribeCommand.Substitutions.NOT_ALLOWED,
        pharmacy='Main Street in Spring Lake',
        prescriber_id='298uhh',
        note_to_pharmacist='please give patient oral instructions'
    )
```

## Questionnaire

**Command-specific parameters**:

| Name               | Type     | Required | Description                                                                     |
| :----------------- | :------- | :------- | :------------------------------------------------------------------------------ |
| `questionnaire_id` | _string_ | `true`   | The externally exposable id of the questionnaire being answered by the patient. |
| `result`           | _string_ | `false`  | A summary of the result of the patient's answers.                               |
|                    |          |          |                                                                                 |

**Example**:

```python
from canvas.commands import QuestionnaireCommand

questionnaire = QuestionnaireCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    questionnaire_id='g73hd9',
    result='The patient is feeling average today.'
)
```

## ReasonForVisit

**Command-specific parameters**:

| Name         | Type      | Required                  | Description                                              |
| :----------- | :-------- | :------------------------ | :------------------------------------------------------- |
| `structured` | _boolean_ | `false`                   | Whether the RFV is structured or not. Defaults to False. |
| `coding`     | _Coding_  | `true` if structured=True | The coding of the structured RFV.                        |
| `comment`    | _string_  | `false`                   | Additional commentary on the RFV.                        |
|              |           |                           |                                                          |

**Example**:

```python
from canvas.commands import ReasonForVisitCommand

structured_rfv = ReasonForVisitCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    structured=True,
    coding={'code': '', 'system': '', 'display': ''},
    comment='also wants to discuss treament options'
)
unstructured_rfv = ReasonForVisitCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    comment='also wants to discuss treatment options'
)
```

## StopMedication

**Command-specific parameters**:

| Name            | Type     | Required | Description                                                        |
| :-------------- | :------- | :------- | :----------------------------------------------------------------- |
| `medication_id` | _string_ | `true`   | Externally exposable id of the patient's medication being stopped. |
| `rationale`     | _string_ | `false`  | The reason for stopping the medication.                            |
|                 |          |          |

**Example**:

```python
from canvas.commands import StopMedicationCommand

stop_medication = StopMedicationCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    medication_id='2u309j',
    rationale='In remission'
)
```

## UpdateGoal

**Command-specific parameters**:

goal_id: str = Field(json_schema_extra={"commands_api_name": "goal_statement"})
due_date: datetime | None = None
achievement_status: AchievementStatus | None = None
priority: Priority | None = None
progress: str | None = None

| Name                 | Type                     | Required | Description                                               |
| :------------------- | :----------------------- | :------- | :-------------------------------------------------------- |
| `goal_id`            | _string_                 | `true`   | Externally exposable id of the goal being updated.        |
| `due_date`           | _datetime_               | `false`  | The date the goal is due.                                 |
| `achievement_status` | _AchievementStatus enum_ | `false`  | The current achievement status of the goal.               |
| `priority`           | _Priority enum_          | `false`  | The priority of the goal.                                 |
| `progress`           | _string_                 | `false`  | A narrative about the patient's progress toward the goal. |
|                      |

| `AchievementStatus` |                  |
| :------------------ | :--------------- |
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
| :--------- | :---------------- |
| HIGH       | "high-priority"   |
| MEDIUM     | "medium-priority" |
| LOW        | "low-priority"    |

**Example**:

```python
from canvas.commands import UpdateGoalCommand
from datetime import datetime

update_goal = UpdateGoalCommand(
    user_id='fg787uu',
    note_uuid='rk786p',
    goal_id='0j9whjjk',
    due_date=datetime(2025, 3, 31),
    achievement_status=GoalCommand.AchievementStatus.WORSENING,
    priority=GoalCommand.Priority.MEDIUM,
    progress='patient has slowed down progress and requesting to move due date out'
)
```
