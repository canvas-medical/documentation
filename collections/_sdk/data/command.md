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
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from logger import log


class MyHandler(BaseHandler):
    RESPONDS_TO = [
        EventType.Name(EventType.REASON_FOR_VISIT_COMMAND__POST_UPDATE),
    ]

    def compute(self) -> list[Effect]:
        log.info(self.target) # logs the Command id
```

Using this value, the `Command` model can be queried to fetch additional data about the command. Two main fields to pay attention to here are the `schema_key` and `data` fields. The `schema_key` field contains the type of the command, while the `data` field contains a JSON object with command data as key/value pairs:

```python
import json
from canvas_sdk.effects import Effect
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.command import Command
from logger import log


class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        command_instance = Command.objects.get(id=self.target)
        log.info(command_instance.schema_key)
        log.info(json.dumps(command_instance.data, indent=2))
```

For example, for a _Reason For Visit_ command, the preceding code would log the following lines:

```sh
reasonForVisit

{
  "coding": {
    "text": "Accident-prone",
    "extra": null,
    "value": "165002",
    "disabled": false,
    "annotations": null,
    "description": null
  },
  "comment": "Patient would like to discuss condition."
}
```

The following table shows the different command `schema_key` values with links to their respective [Command Modules](/sdk/commands). The attributes shown in each corresponding entry contain the structure that will appear in the `data` JSON field of each `Command`.

| Schema Key          | Command Data                                                     |
|---------------------|------------------------------------------------------------------|
| addCondition        | [AddCondition](/sdk/commands/#addcondition)                      |
| adjustPrescription  | [AdjustPrescription](/sdk/commands/#adjustprescription)          |
| allergy             | [Allergy](/sdk/commands/#allergy)                                |
| assess              | [Assess](/sdk/commands/#assess)                                  |
| changeMedication    | [ChangeMedication](/sdk/commands/#changemedication)              |
| closeGoal           | [CloseGoal](/sdk/commands/#closegoal)                            |
| diagnose            | [Diagnose](/sdk/commands/#diagnose)                              |
| familyHistory       | [FamilyHistory](/sdk/commands/#familyhistory)                    |
| followUp            | [FollowUp](/sdk/commands/#followup)                              |
| goal                | [Goal](/sdk/commands/#goal)                                      |
| hpi                 | [HistoryOfPresentIllness](/sdk/commands/#historyofpresentillness) |
| imagingOrder        | [ImagingOrder](/sdk/commands/#imagingorder)                      |
| instruct            | [Instruct](/sdk/commands/#instruct)                              |
| labOrder            | [LabOrder](/sdk/commands/#laborder)                              |
| medicalHistory      | [MedicalHistory](/sdk/commands/#medicalhistory)                  |
| medicationStatement | [MedicationStatement](/sdk/commands/#medicationstatement)        |
| perform             | [Perform](/sdk/commands/#perform)                                |
| plan                | [Plan](/sdk/commands/#plan)                                      |
| pocLabTest          | [POCLabTest](/sdk/commands/#poclabtest)                          |
| prescribe           | [Prescribe](/sdk/commands/#prescribe)                            |
| questionnaire       | [Questionnaire](/sdk/commands/#questionnaire)                    |
| reasonForVisit      | [ReasonForVisit](/sdk/commands/#reasonforvisit)                  |
| refer               | [Refer](/sdk/commands/#refer)                                    |
| refill              | [Refill](/sdk/commands/#refill)                                  |
| removeAllergy       | [RemoveAllergy](/sdk/commands/#removeallergy)                    |
| removePastMedicalHistory | [RemovePastMedicalHistory](/sdk/commands/#remove-past-medical-history) |
| resolveCondition    | [ResolveCondition](/sdk/commands/#resolve-condition)              |
| stopMedication      | [StopMedication](/sdk/commands/#stopmedication)                  |
| surgicalHistory     | [SurgicalHistory](/sdk/commands/#surgicalhistory)                |
| task                | [Task](/sdk/commands/#task)                                      |
| updateDiagnosis     | [UpdateDiagnosis](/sdk/commands/#updatediagnosis)                |
| updateGoal          | [UpdateGoal](/sdk/commands/#updategoal)                          |
| vitals              | [Vitals](/sdk/commands/#vitals)                                  |

__PLEASE NOTE__ the Commands Module is under development and Canvas is working to migrate all commands to be available. This means that some commands are not able to emit events available in plugins, and historical commands created prior to their Commands Module availability may not be able to be queried using the data module. [This product updates table](/product-updates/commands-module/) shows the commands and their release statuses.  If a command in a chart is not available by querying the `Command` data model, the data is still available to be queried using corresponding data models (i.e. [Questionnaire](/sdk/data-questionnaire/), [ImagingOrder](/sdk/data-imaging/), etc.).

## The anchor object

Most commands write a record of their own when they are entered: a Diagnose command creates a `Condition`, a Prescribe command creates a `Prescription`, and so on. That record is the command's anchor object, and `anchor_object` returns it as an instance of the matching data model:

```python
from canvas_sdk.v1.data.command import Command

command = Command.objects.get(id="c1b5a4d2-7e3f-4a8b-9c6d-2f1e0a9b8c7d")
anchor = command.anchor_object
```

`anchor_object_type` and `anchor_object_dbid` identify the record, and `anchor_object` looks it up for you. It returns `None` when the command has no anchor recorded.

| `schema_key` | `anchor_object` returns |
| --- | --- |
| `addCondition` | `Condition` |
| `adjustDiagnosis` | `Assessment` |
| `adjustPrescription` | `Prescription` |
| `adjustProtocol` | `ProtocolOverride` |
| `allergy` | `AllergyIntolerance` |
| `approveChange` | `PrescriptionChangeResponse` |
| `approveRefill` | `Prescription` |
| `assess` | `Assessment` |
| `assessCodingGap` | `AssessCodingGapEvent` |
| `cancelPrescription` | `CancelPrescription` |
| `changeMedication` | `ChangeMedication` |
| `chartSectionReview` | `ChartSectionReview` |
| `clipboard` | `Clipboard` |
| `closeGoal` | `UpdateGoal` |
| `createCodingGap` | `CreateCodingGapEvent` |
| `deferCodingGap` | `DeferCodingGapEvent` |
| `denyChange` | `PrescriptionChangeResponse` |
| `denyRefill` | `Prescription` |
| `device` | `Device` |
| `diagnose` | `Condition` |
| `educationalMaterial` | `EducationalMaterial` |
| `exam` | `Interview` |
| `familyHistory` | `FamilyHistory` |
| `followUp` | `FollowUp` |
| `goal` | `Goal` |
| `hpi` | `HistoryOfPresentIllness` |
| `imagingOrder` | `ImagingOrder` |
| `imagingReview` | `ImagingReview` |
| `immunizationStatement` | `ImmunizationStatement` |
| `immunize` | `Immunization` |
| `instruct` | `Instruction` |
| `labOrder` | `LabOrder` |
| `labReview` | `LabReview` |
| `medicalHistory` | `Condition` |
| `medicationStatement` | `MedicationStatement` |
| `perform` | `Procedure` |
| `plan` | `Plan` |
| `pocLabTest` | `LabReport` |
| `prescribe` | `Prescription` |
| `questionnaire` | `Interview` |
| `reasonForVisit` | `ReasonForVisit` |
| `refer` | `Referral` |
| `reference` | `Reference` |
| `referralReview` | `ReferralReview` |
| `refill` | `Prescription` |
| `removeAllergy` | `RemoveAllergyEvent` |
| `removePastMedicalHistory` | `RemovePastMedicalHistoryEvent` |
| `resolveCondition` | `ResolveConditionEvent` |
| `ros` | `Interview` |
| `snoozeProtocol` | `ProtocolOverride` |
| `stopMedication` | `StopMedicationEvent` |
| `structuredAssessment` | `Interview` |
| `surgicalHistory` | `Condition` |
| `task` | `NoteTask` |
| `updateDiagnosis` | `Condition` |
| `updateGoal` | `UpdateGoal` |
| `validateCodingGap` | `ValidateCodingGapEvent` |
| `visualExamFinding` | `VisualExamFinding` |
| `vitals` | `VitalSignReading` |
| Custom commands | `CustomCommand` |

{% include alert.html type="warning" content="<code>anchor_object</code> is not supported for the <code>uncategorizedDocumentReview</code> and <code>privateNotes</code> commands. Their anchor records have no matching data model, so reading <code>anchor_object</code> on either raises <code>LookupError</code>. Use <code>anchor_object_type</code> and <code>anchor_object_dbid</code> to identify the record instead." %}

If a command's anchor record has been deleted, `anchor_object` raises the data model's `DoesNotExist` rather than returning `None`.

## Attributes

### Command

| Field Name         | Type                                  |
|--------------------|---------------------------------------|
| id                 | UUID                                  |
| dbid               | Integer                               |
| created            | DateTime                              |
| modified           | DateTime                              |
| originator         | [CanvasUser](/sdk/data-canvasuser)    |
| committer          | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error   | [CanvasUser](/sdk/data-canvasuser)    |
| state              | String                                |
| patient            | [Patient](/sdk/data-patient/#patient) |
| note               | [Note](/sdk/data-note/#note)          |
| schema_key         | String                                |
| data               | JSON                                  |
| origination_source | String                                |
| custom_html        | String (optional)                     |
| anchor_object_type | String                                |
| anchor_object_dbid | Integer                               |
| anchor_object      | Model (optional)                      |
| metadata           | QuerySet[[CommandMetadata](/sdk/data-command/#commandmetadata)] |

The `custom_html` field stores HTML content that is rendered alongside the command in the note. This field is optional and defaults to `None`. Use the [`set_custom_html`](/sdk/commands/#set_custom_html) method to set or clear this field on a staged command.

### CommandMetadata

`CommandMetadata` stores custom key-value pairs associated with a command. Metadata can be upserted using the `upsert_metadata` method on any command effect class — see [CommandMetadata Effect](/sdk/effect-command-metadata/) for full details.

```python
from canvas_sdk.v1.data.command import CommandMetadata

# Get all metadata for a command
metadata_entries = CommandMetadata.objects.filter(command__id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

# Get a specific metadata value
entry = CommandMetadata.objects.get(command__id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35", key="my_plugin:priority")
print(entry.value)
```

| Field Name | Type                                    |
|------------|-----------------------------------------|
| id         | UUID                                    |
| dbid       | Integer                                 |
| created    | DateTime                                |
| modified   | DateTime                                |
| command    | [Command](/sdk/data-command/#command)   |
| key        | String                                  |
| value      | String                                  |

<br/>
<br/>
<br/>
