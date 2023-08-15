---
title: "Change Types"
slug: "change-types"
excerpt: "Events are specified to allow the system to know when to compute the protocol."
hidden: false
createdAt: "2021-09-22T20:04:01.682Z"
updatedAt: "2023-05-17T21:48:12.779Z"
---
# CHANGE_TYPE

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

[block:parameters]
{
  "data": {
    "h-0": "CHANGE_TYPE",
    "h-1": "Description",
    "0-0": "ALLERGY_INTOLERANCE",
    "0-1": "Recompute a protocol after any Allergy Intolerance information has been added or changed through our [allergy command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056920593-Document-an-Allergy)",
    "1-0": "APPOINTMENT",
    "1-1": "Recompute a protocol after any Appointments have been made or changed via our [UI](https://canvas-medical.zendesk.com/hc/en-us/articles/360056430014-Appointments) or via our [Appointment Create](ref:create) or [Appointment Update](ref:update) FHIR endpoints. This includes changes to our NoteStateChangeEvents as you click the Book, Reschedule, Cancel, No Show, Check In, Restore buttons related to an appointment. See [Appointment Notification](doc:appointment-notification) for an example",
    "2-0": "BILLING_LINE_ITEM",
    "2-1": "Recompute a protocol after additions/changes to the [Billing Footer](https://canvas-medical.zendesk.com/hc/en-us/articles/4416815562387-Billing-Footer-) or via [Charges](https://canvas-medical.zendesk.com/hc/en-us/articles/1500009684402-Charges-and-Diagnosis-)",
    "3-0": "CONDITION",
    "3-1": "Recompute a protocol after any new conditions or updates to existing conditions are made via our commands [diagnosis](https://canvas-medical.zendesk.com/hc/en-us/articles/360057089133-Command-Diagnose), [assess condition](https://canvas-medical.zendesk.com/hc/en-us/articles/360055230394-Command-Assess-Condition), [resolve condition](https://canvas-medical.zendesk.com/hc/en-us/articles/360055709554-Command-Resolve-Condition), or [surgical history](https://canvas-medical.zendesk.com/hc/en-us/articles/360055625854-Document-Past-Surgical-History)",
    "4-0": "CONSENT",
    "4-1": "Recompute a protocol after a Patient's [consent](https://canvas-medical.zendesk.com/hc/en-us/articles/5524511564947-Patient-Consents#h_01G0ZN8S1HWG71DKDXWPNEGC6T) is added, updated, or deleted.",
    "5-0": "COVERAGE",
    "5-1": "Recompute a protocol after adding or updating a patient's coverages via [UI](https://canvas-medical.zendesk.com/hc/en-us/articles/4408206355603-Patient-Coverages-2-0) or [Coverage Create](ref:coverage-create) / [Coverage Update](ref:coverage-update)",
    "6-0": "ENCOUNTER",
    "6-1": "Recompute a protocol after an encounter was added or updated",
    "7-0": "EXTERNAL_EVENTS",
    "7-1": "Recompute a protocol after an external event for a patient was created via ADT integration messages",
    "8-0": "IMAGING_REPORT",
    "8-1": "Recompute a protocol after an Imaging Report was linked to a patient via [Data Integrations](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918193-Imaging-Reports) or an [Imaging Review](https://canvas-medical.zendesk.com/hc/en-us/articles/1500006006942-Imaging-Report-Review)",
    "9-0": "IMMUNIZATION",
    "9-1": "Recompute a protocol after updates to a Patient's immunization records via [immunize](https://canvas-medical.zendesk.com/hc/en-us/articles/360057140293-Documenting-an-Immunization) or [immunization statement](https://canvas-medical.zendesk.com/hc/en-us/articles/360057139673-Record-a-Previous-Immunization)",
    "10-0": "INSTRUCTION",
    "10-1": "Recompute a protocol after instructions have been added or update via [instruct command](https://canvas-medical.zendesk.com/hc/en-us/articles/360055309574-Command-Instruct)",
    "11-0": "INTERVIEW",
    "11-1": "Recompute a protocol after filling out the commands [questionnaire](https://canvas-medical.zendesk.com/hc/en-us/articles/360057544593-Command-Questionnaire), [structured assessment](https://canvas-medical.zendesk.com/hc/en-us/articles/4415631833875-Structured-Assessment) or [physical exam](https://canvas-medical.zendesk.com/hc/en-us/articles/360055628474-Documenting-a-Patient-Physical-Exam). You can also update these using [QuestionnaireResponse Create](ref:questionnaireresponse-create)",
    "12-0": "LAB_ORDER",
    "12-1": "Recompute a protocol after filling out a [Lab Order](https://canvas-medical.zendesk.com/hc/en-us/articles/360056890753-Placing-a-Lab-Order) command ",
    "13-0": "LAB_REPORT",
    "13-1": "Recompute a protocol after linking a [Lab Report](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918713-Lab-Reports) via Data Integrations or using [Lab Review](https://canvas-medical.zendesk.com/hc/en-us/articles/360061321073-Reviewing-Lab-Results). It will also recompute after the [POC Lab Test Command](https://canvas-medical.zendesk.com/hc/en-us/articles/360055629214-Point-of-Care-POC-Tests) is used.",
    "14-0": "MEDICATION",
    "14-1": "Recompute a protocol after adding or updating medication information via [prescribe](https://canvas-medical.zendesk.com/hc/en-us/articles/360063523313-Prescribing-a-Medication), [refill](https://canvas-medical.zendesk.com/hc/en-us/articles/360057482354-Refill-Medications),  [medication statement](https://canvas-medical.zendesk.com/hc/en-us/articles/1500004007942-Documenting-a-Historical-Medication), or [stop medication](https://canvas-medical.zendesk.com/hc/en-us/articles/1500001227761-Stopping-a-Current-Medication)",
    "15-0": "MESSAGE",
    "15-1": "Recompute a protocol after any new [messages](https://canvas-medical.zendesk.com/hc/en-us/articles/1500001593221-Patient-Message-Inbox-) have been communicated. This will also be triggered after [Communication Create](ref:communication-create)",
    "16-0": "PATIENT",
    "16-1": "Recompute a protocol after patient information has been updated on the [Registration Page](https://canvas-medical.zendesk.com/hc/en-us/articles/360059207093-Patient-Registration-Information) left side. This includes patient demographics, care team, addresses, contacts, phone numbers, or addresses. This also will be triggered after a [Patient Create](ref:patient-create) and [Patient Update](ref:patient-update)  \n  \n**Coming Soon**  \nReleasing on July 20, 2022. This change type will also recompute a protocol after a deletion of patient's care team members, addresses, phone numbers, contact, or addresses.",
    "17-0": "PRESCRIPTION",
    "17-1": "Recompute a protocol after adding or updating prescription information via [prescribe](https://canvas-medical.zendesk.com/hc/en-us/articles/360063523313-Prescribing-a-Medication), [refill](https://canvas-medical.zendesk.com/hc/en-us/articles/360057482354-Refill-Medications),  [adjust prescription](https://canvas-medical.zendesk.com/hc/en-us/articles/360061706154-Adjust-an-Existing-Medication)",
    "18-0": "PROTOCOL_OVERRIDE",
    "18-1": "Recompute a protocol after using [snooze protocol](https://canvas-medical.zendesk.com/hc/en-us/articles/1500002775922-Snoozing-a-Protocol-in-Canvas)",
    "19-0": "REFERRAL_REPORT",
    "19-1": "Recompute a protocol after uploading a [Specialty Consult Report](https://canvas-medical.zendesk.com/hc/en-us/articles/360057919273-Specialist-Consult-Reports)",
    "20-0": "SUSPECT_HCC",
    "20-1": "Recompute a protocol after any SuspectHCC data for a patient has changed",
    "21-0": "TASK",
    "21-1": "Recompute a protocol after a [Task](https://canvas-medical.zendesk.com/hc/en-us/articles/360057545873-Tasks) is created or updated for a patient. This includes when a new comment was added to a task. This also will be triggered after a [Task Create](ref:task-create) and [Task Update](ref:task-update)",
    "22-0": "VITAL_SIGN",
    "22-1": "Recompute a protocol after using the [vitals command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056077654-Logging-Vital-Signs)"
  },
  "cols": 2,
  "rows": 23,
  "align": [
    "left",
    "left"
  ]
}
[/block]