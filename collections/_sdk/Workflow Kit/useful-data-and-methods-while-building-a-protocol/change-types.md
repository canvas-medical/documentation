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
| ALLERGY_INTOLERANCE | Recompute a protocol after any Allergy Intolerance information has been added or changed through our [allergy command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056920593-Document-an-Allergy) |
| APPOINTMENT         | Recompute a protocol after any Appointments have been made or changed via our [UI](https://canvas-medical.zendesk.com/hc/en-us/articles/360056430014-Appointments) or via our [Appointment Create](ref:create) or [Appointment Update](ref:update) FHIR endpoints. This includes changes to our NoteStateChangeEvents as you click the Book, Reschedule, Cancel, No Show, Check In, Restore buttons related to an appointment. See [Appointment Notification](doc:appointment-notification) for an example |
| BILLING_LINE_ITEM   | Recompute a protocol after additions/changes to the [Billing Footer](https://canvas-medical.zendesk.com/hc/en-us/articles/4416815562387-Billing-Footer-) or via [Charges](https://canvas-medical.zendesk.com/hc/en-us/articles/1500009684402-Charges-and-Diagnosis-) |
| CONDITION           | Recompute a protocol after any new conditions or updates to existing conditions are made via our commands [diagnosis](https://canvas-medical.zendesk.com/hc/en-us/articles/360057089133-Command-Diagnose), [assess condition](https://canvas-medical.zendesk.com/hc/en-us/articles/360055230394-Command-Assess-Condition), [resolve condition](https://canvas-medical.zendesk.com/hc/en-us/articles/360055709554-Command-Resolve-Condition), or [surgical history](https://canvas-medical.zendesk.com/hc/en-us/articles/360055625854-Document-Past-Surgical-History) |
| CONSENT            | Recompute a protocol after a Patient's [consent](https://canvas-medical.zendesk.com/hc/en-us/articles/5524511564947-Patient-Consents#h_01G0ZN8S1HWG71DKDXWPNEGC6T) is added, updated, or deleted. |
| COVERAGE           | Recompute a protocol after adding or updating a patient's coverages via [UI](https://canvas-medical.zendesk.com/hc/en-us/articles/4408206355603-Patient-Coverages-2-0) or [Coverage Create](ref:coverage-create) / [Coverage Update](ref:coverage-update) |
| ENCOUNTER          | Recompute a protocol after an encounter was added or updated |
| EXTERNAL_EVENTS    | Recompute a protocol after an external event for a patient was created via ADT integration messages |
| IMAGING_REPORT     | Recompute a protocol after an Imaging Report was linked to a patient via [Data Integrations](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918193-Imaging-Reports) or an [Imaging Review](https://canvas-medical.zendesk.com/hc/en-us/articles/1500006006942-Imaging-Report-Review) |
| IMMUNIZATION       | Recompute a protocol after updates to a Patient's immunization records via [immunize](https://canvas-medical.zendesk.com/hc/en-us/articles/360057140293-Documenting-an-Immunization) or [immunization statement](https://canvas-medical.zendesk.com/hc/en-us/articles/360057139673-Record-a-Previous-Immunization) |
| INSTRUCTION        | Recompute a protocol after instructions have been added or updated via [instruct command](https://canvas-medical.zendesk.com/hc/en-us/articles/360055309574-Command-Instruct) |
| INTERVIEW          | Recompute a protocol after filling out the commands [questionnaire](https://canvas-medical.zendesk.com/hc/en-us/articles/360057544593-Command-Questionnaire), [structured assessment](https://canvas-medical.zendesk.com/hc/en-us/articles/4415631833875-Structured-Assessment) or [physical exam](https://canvas-medical.zendesk.com/hc/en-us/articles/360055628474-Documenting-a-Patient-Physical-Exam). You can also update these using [QuestionnaireResponse Create](ref:questionnaireresponse-create) |
| LAB_ORDER          | Recompute a protocol after filling out a [Lab Order](https://canvas-medical.zendesk.com/hc/en-us/articles/360056890753-Placing-a-Lab-Order) command |
| LAB_REPORT         | Recompute a protocol after linking a [Lab Report](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918713-Lab-Reports) via Data
