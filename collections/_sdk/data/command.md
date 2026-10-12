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
| `addCondition` | [Condition](/sdk/data-condition/#condition) |
| `adjustDiagnosis` | [Assessment](/sdk/data-assessment/#assessment) |
| `adjustPrescription` | [Prescription](/sdk/data-prescription/#prescription) |
| `adjustProtocol` | [ProtocolOverride](/sdk/data-protocol-override/#protocoloverride) |
| `allergy` | [AllergyIntolerance](/sdk/data-allergy-intolerance/#allergyintolerance) |
| `approveChange` | [PrescriptionChangeResponse](/sdk/data-prescription-change-response/#prescriptionchangeresponse) |
| `approveRefill` | [Prescription](/sdk/data-prescription/#prescription) |
| `assess` | [Assessment](/sdk/data-assessment/#assessment) |
| `assessCodingGap` | [AssessCodingGapEvent](/sdk/data-coding-gap-event/#assesscodinggapevent) |
| `cancelPrescription` | [CancelPrescription](/sdk/data-cancel-prescription/#cancelprescription) |
| `changeMedication` | [ChangeMedication](/sdk/data-change-medication/#changemedication) |
| `chartSectionReview` | [ChartSectionReview](/sdk/data-chart-section-review/#chartsectionreview) |
| `clipboard` | [Clipboard](/sdk/data-clipboard/#clipboard) |
| `closeGoal` | [UpdateGoal](/sdk/data-goal/#updategoal) |
| `createCodingGap` | [CreateCodingGapEvent](/sdk/data-coding-gap-event/#createcodinggapevent) |
| `deferCodingGap` | [DeferCodingGapEvent](/sdk/data-coding-gap-event/#defercodinggapevent) |
| `denyChange` | [PrescriptionChangeResponse](/sdk/data-prescription-change-response/#prescriptionchangeresponse) |
| `denyRefill` | [Prescription](/sdk/data-prescription/#prescription) |
| `device` | [Device](/sdk/data-device/#device) |
| `diagnose` | [Condition](/sdk/data-condition/#condition) |
| `educationalMaterial` | [EducationalMaterial](/sdk/data-educational-material/#educationalmaterial) |
| `exam` | [Interview](/sdk/data-questionnaire/#interview) |
| `familyHistory` | [FamilyHistory](/sdk/data-family-history/#familyhistory) |
| `followUp` | [FollowUp](/sdk/data-follow-up/#followup) |
| `goal` | [Goal](/sdk/data-goal/#goal) |
| `hpi` | [HistoryOfPresentIllness](/sdk/data-history-present-illness/#historyofpresentillness) |
| `imagingOrder` | [ImagingOrder](/sdk/data-imaging/#imagingorder) |
| `imagingReview` | [ImagingReview](/sdk/data-imaging/#imagingreview) |
| `immunizationStatement` | [ImmunizationStatement](/sdk/data-immunization/#immunizationstatement) |
| `immunize` | [Immunization](/sdk/data-immunization/#immunization) |
| `instruct` | [Instruction](/sdk/data-instruction/#instruction) |
| `labOrder` | [LabOrder](/sdk/data-labs/#laborder) |
| `labReview` | [LabReview](/sdk/data-labs/#labreview) |
| `medicalHistory` | [Condition](/sdk/data-condition/#condition) |
| `medicationStatement` | [MedicationStatement](/sdk/data-medication-statement/#medicationstatement) |
| `perform` | [Procedure](/sdk/data-procedure/#procedure) |
| `plan` | [Plan](/sdk/data-plan/#plan) |
| `pocLabTest` | [LabReport](/sdk/data-labs/#labreport) |
| `prescribe` | [Prescription](/sdk/data-prescription/#prescription) |
| `questionnaire` | [Interview](/sdk/data-questionnaire/#interview) |
| `reasonForVisit` | [ReasonForVisit](/sdk/data-reason-for-visit/#reasonforvisit) |
| `refer` | [Referral](/sdk/data-referral/#referral) |
| `reference` | [Reference](/sdk/data-reference/#reference) |
| `referralReview` | [ReferralReview](/sdk/data-referral/#referralreview) |
| `refill` | [Prescription](/sdk/data-prescription/#prescription) |
| `removeAllergy` | [RemoveAllergyEvent](/sdk/data-remove-allergy-event/#removeallergyevent) |
| `removePastMedicalHistory` | [RemovePastMedicalHistoryEvent](/sdk/data-remove-past-medical-history-event/#removepastmedicalhistoryevent) |
| `resolveCondition` | [ResolveConditionEvent](/sdk/data-resolve-condition-event/#resolveconditionevent) |
| `ros` | [Interview](/sdk/data-questionnaire/#interview) |
| `snoozeProtocol` | [ProtocolOverride](/sdk/data-protocol-override/#protocoloverride) |
| `stopMedication` | [StopMedicationEvent](/sdk/data-stop-medication-event/#stopmedicationevent) |
| `structuredAssessment` | [Interview](/sdk/data-questionnaire/#interview) |
| `surgicalHistory` | [Condition](/sdk/data-condition/#condition) |
| `task` | [NoteTask](/sdk/data-task/#notetask) |
| `updateDiagnosis` | [Condition](/sdk/data-condition/#condition) |
| `updateGoal` | [UpdateGoal](/sdk/data-goal/#updategoal) |
| `validateCodingGap` | [ValidateCodingGapEvent](/sdk/data-coding-gap-event/#validatecodinggapevent) |
| `visualExamFinding` | [VisualExamFinding](/sdk/data-visual-exam-finding/#visualexamfinding) |
| `vitals` | [VitalSignReading](/sdk/data-vital-sign-reading/#vitalsignreading) |
| Custom commands | [CustomCommand](/sdk/data-custom-command/#customcommand) |

{% include alert.html type="warning" content="<code>anchor_object</code> does not yet support the <code>uncategorizedDocumentReview</code> command, and reading it raises <code>LookupError</code>. Support is coming in an upcoming release. Until then, look the record up directly as shown below." %}

The `uncategorizedDocumentReview` anchor is available as [UncategorizedClinicalDocumentReview](/sdk/data-uncategorized-clinical-document/#uncategorizedclinicaldocumentreview); `anchor_object` cannot find it because the model goes by a different name. Look it up from `anchor_object_dbid` instead:

```python
from canvas_sdk.v1.data import UncategorizedClinicalDocumentReview
from canvas_sdk.v1.data.command import Command

command = Command.objects.get(id="c1b5a4d2-7e3f-4a8b-9c6d-2f1e0a9b8c7d")
review = UncategorizedClinicalDocumentReview.objects.get(dbid=command.anchor_object_dbid)
```

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
