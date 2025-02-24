---
title: "Command"
slug: "data-command"
excerpt: "Canvas SDK Command"
hidden: false
---

## Introduction

The `Command` model represents a [command](/sdk/commands/) in a note.

## Basic usage

To get a command by identifier, use the `get` method on the `Command` model manager:

```python
from canvas_sdk.v1.data.command import Command

command = Command.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

## Filtering

Commands can be filtered by any attribute that exists on the model.

Filtering for commands is done with the `filter` method on the `Command` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.command import Command

commands = Command.objects.filter(state="committed")
```

## Command types and data

When events are fired as part of [Command Lifecycle Events](/sdk/events/#command-lifecycle-events), the `self.target` value that is available within a plugin will contain the `id` value of the command. For example:

```python
class Protocol(BaseProtocol):
    RESPONDS_TO = [
        EventType.Name(EventType.REASON_FOR_VISIT_COMMAND__POST_UPDATE),
    ]

    def compute(self) -> list[Effect]:
        log.info(self.target) # logs the Command id
```

Using this value, the `Command` model can be queried to fetch additional data about the command. Two main fields to pay attention to here are the `schema_key` and `data` fields. The `schema_key` field contains the type of the command, while the `data` field contains a JSON object with command data as key/value pairs:

```python
    command_instance = Command.objects.get(id=self.target)
    log.info(command_instance.schema_key)
    log.info(command_instance.data)
```

For example, for a _Reason For Visit_ command, the preceding code would log the following lines:

```
reasonForVisit

{'coding': {'text': 'Accident-prone', 'extra': None, 'value': '165002', 'disabled': False, 'annotations': None, 'description': None},
'comment': 'Patient would like to discuss condition.'}
```

The following table shows the different command `schema_key` values with links to their respective [Command Modules](/sdk/commands). The attributes shown in each corresponding entry contain the structure that will appear in the `data` JSON field of each `Command`.

| Schema Key          | Command Data                                                     |
|---------------------|------------------------------------------------------------------|
| adjustPrescription  | [AdjustPrescription](/sdk/commands/#adjustprescription)          |
| allergy             | [Allergy](/sdk/commands/#allergy)                                |
| assess              | [Assess](/sdk/commands/#assess)                                  |
| closeGoal           | [CloseGoal](/sdk/commands/#closegoal)                            |
| diagnose            | [Diagnose](/sdk/commands/#diagnose)                              |
| familyHistory       | [FamilyHistory](/sdk/commands/#familyhistory)                    |
| followUp            | [FollowUp](/sdk/commands/#followUp)                              |
| goal                | [Goal](/sdk/commands/#goal)                                      |
| hpi                 | [HistoryOfPresentIllness](/sdk/commands/#historyofpresentillness) |
| imagingOrder        | [ImagingOrder](/sdk/commands/#imagingorder)                      |
| instruct            | [Instruct](/sdk/commands/#instruct)                              |
| labOrder            | [LabOrder](/sdk/commands/#laborder)                              |
| medicalHistory      | [MedicalHistory](/sdk/commands/#medicalhistory)                  |
| medicationStatement | [MedicationStatement](/sdk/commands/#medicationstatement)        |
| perform             | [Perform](/sdk/commands/#perform)                                |
| plan                | [Plan](/sdk/commands/#plan)                                      |
| prescribe           | [Prescribe](/sdk/commands/#prescribe)                            |
| questionnaire       | [Questionnaire](/sdk/commands/#questionnaire)                    |
| reasonForVisit      | [ReasonForVisit](/sdk/commands/#reasonforvisit)                  |
| refer               | [Refer](/sdk/commands/#refer)                                    |
| refill              | [Refill](/sdk/commands/#refill)                                  |
| removeAllergy       | [RemoveAllergy](/sdk/commands/#removeallergy)                    |
| resolveCondition    | [ResolveCondition](/sdk/commands/#resolvecondition)              |
| stopMedication      | [StopMedication](/sdk/commands/#stopmedication)                  |
| surgicalHistory     | [SurgicalHistory](/sdk/commands/#surgicalhistory)                |
| task                | [Task](/sdk/commands/#task)                                      |
| updateDiagnosis     | [UpdateDiagnosis](/sdk/commands/#updatediagnosis)                |
| updateGoal          | [UpdateGoal](/sdk/commands/#updategoal)                          |
| vitals              | [Vitals](/sdk/commands/#vitals)                                  |

__PLEASE NOTE__ the Commands Module is under development and Canvas is working to migrate all commands to be available. This means that some commands are not able to emit events available in plugins, and historical commands created prior to their Commands Module availability may not be able to be queried using the data module. [This product updates table](/product-updates/commands-module/) shows the commands and their release statuses.  If a command in a chart is not available by querying the `Command` data model, the data is still available to be queried using corresponding data models (i.e. [Questionnaire](/sdk/data-questionnaire/), [ImagingOrder](/sdk/data-imaging/), etc.).

## Attributes

### Command

| Field Name         | Type                                  |
|--------------------|---------------------------------------|
| id                 | UUID                                  |
| dbid               | Integer                               |
| created            | DateTime                              |
| modified           | DateTime                              |
| originator         | CanvasUser                            |
| committer          | CanvasUser                            |
| entered_in_error   | CanvasUser                            |
| state              | String                                |
| patient            | [Patient](/sdk/data-patient/#patient) |
| note               | [Note](/sdk/data-note/#note)          |
| schema_key         | String                                |
| data               | JSON                                  |
| origination_source | String                                |

<br/>
<br/>
<br/>
