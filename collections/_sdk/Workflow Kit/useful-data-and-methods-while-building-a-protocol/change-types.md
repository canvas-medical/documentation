---
title: "Change Types"
---
Change types tell the system when to recompute this protocol. You can specify specific types of data you would like the protocol to be triggered. Include only the types that are used to compute whether the protocol is used to  
ensure the system processes data in an optimized manner.

For example  the below example would try to recalculate the protocol for a patient if any condition or lab reports were added/updated. It would also recompute if any patient demographic information info was changed.

```text
from canvas_workflow_sdk.constants import CHANGE_TYPE

class ClinicalQualityMeasure122v6(ClinicalQualityMeasure):

    ...

    compute_on_change_types = [
        CHANGE_TYPE.CONDITION,
        CHANGE_TYPE.LAB_REPORT,
        CHANGE_TYPE.PATIENT,
    ]
```

Here is a list of all the change types that are currently supported in Canvas:

| CHANGE_TYPE        | Description                                                                                                                          |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| ALLERGY_INTOLERANCE | Recompute a protocol after any Allergy Intolerance information has been added or changed through our [allergy command](exclude_attribtues_in
https://canvas-medical.help.usepylon.com/articles/9964004914-document-allergies) |
| APPOINTMENT         | Recompute a protocol after any Appointments have been made or changed via our [UI](https://canvas-medical.help.usepylon.com/articles/3191656079-appointments) or via our [Appointment Create](/api/appointment/#create) or [Appointment Update](/api/appointment/#update) FHIR endpoints. This includes changes to our NoteStateChangeEvents as you click the Book, Reschedule, Cancel, No Show, Check In, Restore buttons related to an appointment. See [Appointment Notification](/sdk/notification-protocol/#appointment-notification-example) for an example |
| BILLING_LINE_ITEM   | Recompute a protocol after additions/changes to the [Billing Footer](https://canvas-medical.help.usepylon.com/articles/8743381058-chart-note-billing-footer) |
| CONDITION           | Recompute a protocol after any new conditions or updates to existing conditions are made via our commands [diagnosis](https://canvas-medical.help.usepylon.com/articles/7998893827-managing-conditions#diagnosing-a-condition-2), [assess condition](https://canvas-medical.help.usepylon.com/articles/7998893827-managing-conditions#assessing-a-condition-8), [resolve condition](https://canvas-medical.help.usepylon.com/articles/7998893827-managing-conditions#resolving-a-condition-13), or [surgical history](https://canvas-medical.help.usepylon.com/articles/5682206573-command-surgical-history) |
| CONSENT            | Recompute a protocol after a Patient's [consent](https://canvas-medical.help.usepylon.com/articles/8727821967-patient-consents) is added, updated, or deleted. |
| COVERAGE           | Recompute a protocol after adding or updating a patient's coverages via [UI](https://canvas-medical.help.usepylon.com/articles/5877696655-patient-coverages) or [Coverage Create](/api/coverage/#create) / [Coverage Update](/api/coverage/#update) |
| ENCOUNTER          | Recompute a protocol after an encounter was added or updated |
| EXTERNAL_EVENTS    | Recompute a protocol after an external event for a patient was created via ADT integration messages |
| IMAGING_REPORT     | Recompute a protocol after an Imaging Report was linked to a patient via [Data Integrations](https://canvas-medical.help.usepylon.com/articles/4180848054-) or an [Imaging Review](https://canvas-medical.help.usepylon.com/articles/7566748234-process-image-results) |
| IMMUNIZATION       | Recompute a protocol after updates to a Patient's immunization records via [immunize](https://canvas-medical.help.usepylon.com/articles/4155771468-command-immunize) or [immunization statement](https://canvas-medical.help.usepylon.com/articles/1379672479-command-immunization-statement) |
| INSTRUCTION        | Recompute a protocol after instructions have been added or updated via [instruct command](https://canvas-medical.help.usepylon.com/articles/4244748724-command-instruct) |
| INTERVIEW          | Recompute a protocol after filling out the commands [questionnaire](https://canvas-medical.help.usepylon.com/articles/5651999344-command-questionnaire), [structured assessment](https://canvas-medical.help.usepylon.com/articles/8805008571-command-structured-assessment) or [physical exam](https://canvas-medical.help.usepylon.com/articles/1745103290-command-physical-exam). You can also update these using [QuestionnaireResponse Create](/api/questionnaireresponse/#create) |
| LAB_ORDER          | Recompute a protocol after filling out a [Lab Order](https://canvas-medical.help.usepylon.com/articles/3065191197-placing-a-lab-order) command |
| LAB_REPORT         | Recompute a protocol after linking a [Lab Report](https://canvas-medical.help.usepylon.com/articles/1652834476-labs-lab-reports) via Data Integrations or using Lab Review. It will also recompute after the POC Lab Test Command is used. |
| MEDICATION         |  Recompute a protocol after adding or updating medication information via [prescribe, refill, medication statement, or stop medication](https://canvas-medical.help.usepylon.com/articles/5128727084-managing-medication-commands#stopping-a-medication-59) |
| MESSAGE            | Recompute a protocol after any new [messages](https://canvas-medical.help.usepylon.com/articles/6255444430-patient-message-inbox) have been communicated. This will also be triggered after [Communication Create](/api/communication/#create) |
| PATIENT            | Recompute a protocol after patient information has been updated on the [Registration Page](https://canvas-medical.help.usepylon.com/articles/9555344303-demographics-registration) left side. This includes patient demographics, care team, addresses, contacts, phone numbers, or addresses. This also will be triggered after a [FHIR Patient Create](/api/patient/#create) and [Patient Update](/api/patient/#update). This change type will also recompute a protocol after a deletion of patient's care team members, addresses, phone numbers, or contact. |
| PRESCRIPTION       | Recompute a protocol after adding or updating prescription information via [prescribe, refill, adjust prescription commands, deny change, or approve change commands](https://canvas-medical.help.usepylon.com/articles/5128727084-managing-medication-commands) |
| PROTOCOL_OVERRIDE  | Recompute a protocol after using [snooze protocol](https://canvas-medical.help.usepylon.com/articles/3693225186-protocol-snooze-protocol) |
| REFERRAL_REPORT    | Recompute a protocol after uploading a [Specialty Consult Report](https://canvas-medical.help.usepylon.com/articles/8163023191-data-integration-specialist-consult-reports) |
| SUSPECT_HCC        | Recompute a protocol after any SuspectHCC data for a patient has changed |
| TASK               | Recompute a protocol after a [Task](https://canvas-medical.help.usepylon.com/articles/8460447495-task-management) is created or updated for a patient. This includes when a new comment was added to a task. This also will be triggered after a FHIR [Task Create](/api/task/#create) and [Task Update](/api/task/#update) |
| VITAL_SIGN         | Recompute a protocol after using the [vitals command](https://canvas-medical.help.usepylon.com/articles/9426091672-command-vitals). This includes when a vital observation is created via [FHIR Observation Create](/api/observation/#create) |
