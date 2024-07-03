---
title: "Events"
---

**What is an Event?**

An event is an occurrence of an action that happens within Canvas. For example, a patient being prescribed a medication, a user searching for a condition or an appointment being created are all examples of events.

**Why should I use them?**

By writing plugins that respond to events, plugin code is notified and can react to events that occur in Canvas. This enables plugin authors to create custom workflows whenever a relevant event takes place, such as making a POST request to a webhook.

**How do I use them?**

To make plugin code react to an event, you can add the event types listed below into the `RESPONDS_TO` list of a plugin that inherits from `BaseProtocol`. For example:

```python
from canvas_sdk.events import EventType

class Protocol(BaseProtocol):
    RESPONDS_TO = [EventType.Name(EventType.ALLERGY_INTOLERANCE_CREATED)]

    def compute(self):
        ....
```

The plugin author can enter custom workflow code into the `compute` method that will execute every time an Allergy Intolerance is created in Canvas.

For more information on writing plugins, see the guide [here](/guides/your-first-plugin/).

### Event Types

The following Canvas events are able to trigger a plugin to execute.

| Event | Description |
| ----- | ----------- |
| ALLERGY_INTOLERANCE_CREATED | Occurs when an allergy is created for a patient. Additional details for the allergy may become available with subsequent ALLERGY_INTOLERANCE_UPDATED events. |
| ALLERGY_INTOLERANCE_UPDATED | Occurs when an allergy is updated for a patient. |
| APPOINTMENT_CANCELED | Occurs when an appointment is cancelled. |
| APPOINTMENT_CHECKED_IN | Occurs when a patient has arrived and been checked in for their appointment. |
| APPOINTMENT_CREATED | Occurs when an appointment is first created/booked. |
| APPOINTMENT_NO_SHOWED | Occurs when an appointment is marked as a no-show. |
| APPOINTMENT_RESCHEDULED | Occurs when an appointment is rescheduled. In this case, a new appointment is created that is linked to the appointment it was rescheduled from. |
| APPOINTMENT_RESTORED | Occurs when a cancelled appointment is restored to a non-cancelled status. |
| APPOINTMENT_UPDATED | Occurs when details of an appointment are updated. |
| BILLING_LINE_ITEM_CREATED | Occurs when a billing line item is created from adding a CPT code to a note. |
| BILLING_LINE_ITEM_UPDATED | Occurs when a billing line item is modified. |
| CONDITION_ASSESSED | Occurs when a condition is assessed through the Assess Condition command. |
| CONDITION_CREATED | Occurs when a condition is diagnosed for a patient. Additional details for the condition may become available with subsequent CONDITION_UPDATED events. |
| CONDITION_RESOLVED | Occurs when a condition is resolved through the Resolve Condition command. |
| CONDITION_UPDATED | Occurs when a condition is updated for a patient. |
| CONSENT_CREATED | Occurs when a patient consent is created. |
| CONSENT_DELETED | Occurs when a patient consent is removed/deleted. |
| CONSENT_UPDATED | Occurs when a patient consent is updated. |
| COVERAGE_CREATED | Occurs when a coverage for a patient is created. |
| COVERAGE_UPDATED | Occurs when a coverage for a patient is updated. |
| ENCOUNTER_CREATED | Occurs when an encounter is created. |
| ENCOUNTER_UPDATED | Occurs when an encounter is updated. |
| IMAGING_REPORT_CREATED | Occurs when an imaging report is entered into the Data Integration section of Canvas. |
| IMAGING_REPORT_UPDATED | Occurs when an imaging report is updated. |
| IMMUNIZATION_CREATED | Occurs when an immunization is created. Additional details for the immunization may become available with subsequent IMMUNIZATION_UPDATED events. |
| IMMUNIZATION_STATEMENT_CREATED | Occurs when an immunization statement is created. Additional details for the immunization statement may become available with subsequent IMMUNIZATION_STATEMENT_UPDATED events. |
| IMMUNIZATION_STATEMENT_UPDATED | Occurs when an immunization statement is updated. |
| IMMUNIZATION_UPDATED | Occurs when an immunization is updated. |
| INSTRUCTION_CREATED | Occurs when an instruction is created using the Instruct command. Additional details for the instruction may become available with subsequent INSTRUCTION_UPDATED events. |
| INSTRUCTION_UPDATED | Occurs when an instruction is updated. |
| INTERVIEW_CREATED | Occurs when an interview is created using the Questionnaire command or through the Questionnaire endpoint in the FHIR API. Additional details for the interview may become available with subsequent INTERVIEW_UPDATED events. |
| INTERVIEW_UPDATED | Occurs when an interview is updated. |
| LAB_ORDER_CREATED | Occurs when a lab order is created via the Lab Order command. Additional details for the lab order may become available with subsequent LAB_ORDER_UPDATED events. |
| LAB_ORDER_UPDATED | Occurs when a lab order is updated. |
| LAB_REPORT_CREATED | Occurs when a lab report is created either through Data Integration, electronic ingestion or the FHIR API. |
| LAB_REPORT_UPDATED | Occurs when a lab report is updated. |
| MEDICATION_LIST_ITEM_CREATED | Occurs when a medication is added for a patient. |
| MEDICATION_LIST_ITEM_UPDATED | Occurs when a medication is updated for a patient. |
| MESSAGE_CREATED | Occurs when a message (patient/practitioner communication) is created. |
| PATIENT_CREATED | Occurs when a patient is created. |
| PATIENT_UPDATED | Occurs when a patient's data is updated. |
| PRESCRIPTION_CREATED | Occurs when a prescription is created. |
| PRESCRIPTION_UPDATED | Occurs when a prescription is created for a patient using the Prescribe command. Additional details for the prescription become available with subsequent PRESCRIPTION_UPDATED events. |
| REFERRAL_REPORT_CREATED | Occurs when a specialist consult report is created in Data Integration. |
| REFERRAL_REPORT_UPDATED | Occurs when a specialist consult report is updated. |
| TASK_COMMENT_CREATED | Occurs when a comment is added to a task. |
| TASK_CREATED | Occurs when a task is created. |
| TASK_LABELS_ADJUSTED |  |
| TASK_UPDATED | Occurs when a task is updated. |
| VITAL_SIGN_CREATED | Occurs when a vitals entry is created for a patient using the Vitals command. Additional details for the vitals become available with subsequent VITAL_SIGN_UPDATED events. |
| VITAL_SIGN_UPDATED | Occurs when a vitals entry is updated for a patient. |
| PRE_COMMAND_ORIGINATE | Occurs before any command is entered into a note. |
| POST_COMMAND_ORIGINATE | Occurs after any command is entered into a note. |
| PRE_COMMAND_UPDATE | Occurs before the data in any command is updated. |
| POST_COMMAND_UPDATE | Occurs after the data in any command is updated. |
| PRE_COMMAND_COMMIT | Occurs before any command is committed. |
| POST_COMMAND_COMMIT | Occurs after any command is committed. |
| PRE_COMMAND_DELETE | Occurs before any command is deleted. |
| POST_COMMAND_DELETE | Occurs after any command is deleted. |
| PRE_COMMAND_ENTER_IN_ERROR | Occurs before any command is marked as entered in error. |
| POST_COMMAND_ENTER_IN_ERROR | Occurs after any command is marked as entered in error. |
| PRE_COMMAND_EXECUTE_ACTION | Occurs before an action is executed on any command. |
| POST_COMMAND_EXECUTE_ACTION | Occurs after an action is executed on any command. |
| ASSESS_COMMAND__CONDITION_SELECTED | Occurs after a condition is selected in the Assess command. |
| MEDICATION_STATEMENT__MEDICATION__PRE_SEARCH | Occurs before a medication statement search for a medication. |
| MEDICATION_STATEMENT__MEDICATION__POST_SEARCH | Occurs after the initial results are fetched for the medication search in the medication statement command. |
| MEDICATION_STATEMENT__MEDICATION__SELECTED | Occurs when a medication is selected from Medication Statement search results. |
| ASSESS_COMMAND__PRE_ORIGINATE | Occurs before the Assess command is first entered into a note. |
| ASSESS_COMMAND__POST_ORIGINATE | Occurs after the Assess command is first entered into a note. |
| ASSESS_COMMAND__PRE_UPDATE | Occurs before data for the Assess command is updated. |
| ASSESS_COMMAND__POST_UPDATE | Occurs after data for the Assess command is updated. |
| ASSESS_COMMAND__PRE_COMMIT | Occurs before the Assess command is committed. |
| ASSESS_COMMAND__POST_COMMIT | Occurs after the Assess command is committed. |
| ASSESS_COMMAND__PRE_DELETE | Occurs before the Assess command is deleted. |
| ASSESS_COMMAND__POST_DELETE | Occurs after the Assess command is deleted. |
| ASSESS_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Assess command is marked as entered in error. |
| ASSESS_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Assess command is marked as entered in error. |
| ASSESS_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Assess command. |
| ASSESS_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Assess command. |
| ASSESS__CONDITION__POST_SEARCH | Occurs after the initial results are fetched for the condition search in the Assess command. |
| DIAGNOSE__DIAGNOSE__POST_SEARCH | Occurs after the initial results are fetched for the diagnosis search in the Diagnose command. |
| GOAL_COMMAND__PRE_ORIGINATE | Occurs before the Goal command is first entered into a note. |
| GOAL_COMMAND__POST_ORIGINATE | Occurs after the Goal command is first entered into a note. |
| GOAL_COMMAND__PRE_UPDATE | Occurs before data for the Goal command is updated. |
| GOAL_COMMAND__POST_UPDATE | Occurs after data for the Goal command is updated. |
| GOAL_COMMAND__PRE_COMMIT | Occurs before the Goal command is committed. |
| GOAL_COMMAND__POST_COMMIT | Occurs after the Goal command is committed. |
| GOAL_COMMAND__PRE_DELETE | Occurs before the Assess command is deleted. |
| GOAL_COMMAND__POST_DELETE | Occurs after the Assess command is deleted. |
| GOAL_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Goal command is marked as entered in error. |
| GOAL_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Goal command is marked as entered in error. |
| GOAL_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Goal command. |
| GOAL_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Goal command. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_ORIGINATE | Occurs before the History of Present Illness command is first entered into a note. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_ORIGINATE | Occurs after the History of Present Illness command is first entered into a note. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_UPDATE | Occurs before data for the History of Present Illness command is updated. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_UPDATE | Occurs after data for the History of Present Illness command is updated. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_COMMIT | Occurs before the History of Present Illness command is committed. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_COMMIT | Occurs after the History of Present Illness command is committed. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_DELETE | Occurs before the History of Present Illness command is deleted. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_DELETE | Occurs after the History of Present Illness command is deleted. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the History of Present Illness command is marked as entered in error. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_ENTER_IN_ERROR | Occurs after the History of Present Illness command is marked as entered in error. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the History of Present Illness command. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the History of Present Illness command. |
| MEDICATION_STATEMENT_COMMAND__PRE_ORIGINATE | Occurs before the Medication Statement command is first entered into a note. |
| MEDICATION_STATEMENT_COMMAND__POST_ORIGINATE | Occurs after the Medication Statement command is first entered into a note. |
| MEDICATION_STATEMENT_COMMAND__PRE_UPDATE | Occurs before data for the Medication Statement command is updated. |
| MEDICATION_STATEMENT_COMMAND__POST_UPDATE | Occurs after data for the Medication Statement command is updated. |
| MEDICATION_STATEMENT_COMMAND__PRE_COMMIT | Occurs before the Medication Statement command is committed. |
| MEDICATION_STATEMENT_COMMAND__POST_COMMIT | Occurs after the Medication Statement command is committed. |
| MEDICATION_STATEMENT_COMMAND__PRE_DELETE | Occurs before the Medication Statement command is deleted. |
| MEDICATION_STATEMENT_COMMAND__POST_DELETE | Occurs after the Medication Statement command is deleted. |
| MEDICATION_STATEMENT_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Medication Statement command is marked as entered in error. |
| MEDICATION_STATEMENT_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Medication Statement command is marked as entered in error. |
| MEDICATION_STATEMENT_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Medication Statement command. |
| MEDICATION_STATEMENT_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Medication Statement command. |
| PLAN_COMMAND__PRE_ORIGINATE | Occurs before the Plan command is first entered into a note. |
| PLAN_COMMAND__POST_ORIGINATE | Occurs after the Plan command is first entered into a note. |
| PLAN_COMMAND__PRE_UPDATE | Occurs before data for the Plan command is updated. |
| PLAN_COMMAND__POST_UPDATE | Occurs after data for the Plan command is updated. |
| PLAN_COMMAND__PRE_COMMIT | Occurs before the Plan command is committed. |
| PLAN_COMMAND__POST_COMMIT | Occurs after the Plan command is committed. |
| PLAN_COMMAND__PRE_DELETE | Occurs before the Plan command is deleted. |
| PLAN_COMMAND__POST_DELETE | Occurs after the Plan command is deleted. |
| PLAN_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Plan command is marked as entered in error. |
| PLAN_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Plan command is marked as entered in error. |
| PLAN_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Plan command. |
| PLAN_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Plan command. |
| PRESCRIBE_COMMAND__PRE_ORIGINATE | Occurs before the Prescribe command is first entered into a note. |
| PRESCRIBE_COMMAND__POST_ORIGINATE | Occurs after the Prescribe command is first entered into a note. |
| PRESCRIBE_COMMAND__PRE_UPDATE | Occurs before data for the Prescribe command is updated. |
| PRESCRIBE_COMMAND__POST_UPDATE | Occurs after data for the Prescribe command is updated. |
| PRESCRIBE_COMMAND__PRE_COMMIT | Occurs before the Prescribecommand is committed. |
| PRESCRIBE_COMMAND__POST_COMMIT | Occurs after the Prescribe command is committed. |
| PRESCRIBE_COMMAND__PRE_DELETE | Occurs before the Prescribe command is deleted. |
| PRESCRIBE_COMMAND__POST_DELETE | Occurs after the Prescribe command is deleted. |
| PRESCRIBE_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Prescribe command is marked as entered in error. |
| PRESCRIBE_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Prescribe command is marked as entered in error. |
| PRESCRIBE_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Prescribe command. |
| PRESCRIBE_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Prescribe command. |
| PRESCRIBE__PRESCRIBE__POST_SEARCH | Occurs after the initial results are fetched for the medication search in the Prescribe command. |
| QUESTIONNAIRE_COMMAND__PRE_ORIGINATE | Occurs before the Questionnaire command is first entered into a note. |
| QUESTIONNAIRE_COMMAND__POST_ORIGINATE | Occurs after the Questionnaire command is first entered into a note. |
| QUESTIONNAIRE_COMMAND__PRE_UPDATE | Occurs before data for the Questionnaire command is updated. |
| QUESTIONNAIRE_COMMAND__POST_UPDATE | Occurs after data for the Questionnaire command is updated. |
| QUESTIONNAIRE_COMMAND__PRE_COMMIT | Occurs before the Questionnaire command is committed. |
| QUESTIONNAIRE_COMMAND__POST_COMMIT | Occurs after the Questionnaire command is committed. |
| QUESTIONNAIRE_COMMAND__PRE_DELETE | Occurs before the Questionnaire command is deleted. |
| QUESTIONNAIRE_COMMAND__POST_DELETE | Occurs after the Questionnaire command is deleted. |
| QUESTIONNAIRE_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Questionnaire command is marked as entered in error. |
| QUESTIONNAIRE_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Questionnaire command is marked as entered in error. |
| QUESTIONNAIRE_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Questionnaire command. |
| QUESTIONNAIRE_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Questionnaire command. |
| QUESTIONNAIRE__QUESTIONNAIRE__POST_SEARCH | Occurs after the initial results are fetched for the questionnaire search in the Questionnaire command. |
| REASON_FOR_VISIT_COMMAND__PRE_ORIGINATE | Occurs before the Reason for Visit command is first entered into a note. |
| REASON_FOR_VISIT_COMMAND__POST_ORIGINATE | Occurs after the Reason for Visit command is first entered into a note. |
| REASON_FOR_VISIT_COMMAND__PRE_UPDATE | Occurs before data for the Reason for Visit command is updated. |
| REASON_FOR_VISIT_COMMAND__POST_UPDATE | Occurs after data for the Reason for Visit command is updated. |
| REASON_FOR_VISIT_COMMAND__PRE_COMMIT | Occurs before the Reason for Visit command is committed. |
| REASON_FOR_VISIT_COMMAND__POST_COMMIT | Occurs after the Reason for Visit command is committed. |
| REASON_FOR_VISIT_COMMAND__PRE_DELETE | Occurs before the Reason for Visit command is deleted. |
| REASON_FOR_VISIT_COMMAND__POST_DELETE | Occurs after the Reason for Visit command is deleted. |
| REASON_FOR_VISIT_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Reason for Visit command is marked as entered in error. |
| REASON_FOR_VISIT_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Reason for Visit command is marked as entered in error. |
| REASON_FOR_VISIT_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Reason for Visit command. |
| REASON_FOR_VISIT_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Reason for Visit command. |
| REASON_FOR_VISIT__CODING__POST_SEARCH | Occurs after the initial results are fetched for the reason search in the Reason for Visit command. |
| STOP_MEDICATION_COMMAND__PRE_ORIGINATE | Occurs before the Stop Medication command is first entered into a note. |
| STOP_MEDICATION_COMMAND__POST_ORIGINATE | Occurs after the Stop Medication command is first entered into a note. |
| STOP_MEDICATION_COMMAND__PRE_UPDATE | Occurs before data for the Stop Medication command is updated. |
| STOP_MEDICATION_COMMAND__POST_UPDATE | Occurs after data for the Stop Medication command is updated. |
| STOP_MEDICATION_COMMAND__PRE_COMMIT | Occurs before the Stop Medication command is committed. |
| STOP_MEDICATION_COMMAND__POST_COMMIT | Occurs after the Stop Medication command is committed. |
| STOP_MEDICATION_COMMAND__PRE_DELETE | Occurs before the Stop Medication command is deleted. |
| STOP_MEDICATION_COMMAND__POST_DELETE | Occurs after the Stop Medication command is deleted. |
| STOP_MEDICATION_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Stop Medication command is marked as entered in error. |
| STOP_MEDICATION_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Stop Medication command is marked as entered in error. |
| STOP_MEDICATION_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Stop Medication command. |
| STOP_MEDICATION_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Stop Medication command. |
| STOP_MEDICATION__MEDICATION__POST_SEARCH | Occurs after the initial results are fetched for the medication search in the Stop Medication command. |
| TASK_COMMAND__PRE_ORIGINATE | Occurs before the Task command is first entered into a note. |
| TASK_COMMAND__POST_ORIGINATE | Occurs after the Task command is first entered into a note. |
| TASK_COMMAND__PRE_UPDATE | Occurs before data for the Task command is updated. |
| TASK_COMMAND__POST_UPDATE | Occurs after data for the Task command is updated. |
| TASK_COMMAND__PRE_COMMIT | Occurs before the Task command is committed. |
| TASK_COMMAND__POST_COMMIT | Occurs after the Task command is committed. |
| TASK_COMMAND__PRE_DELETE | Occurs before the Task command is deleted. |
| TASK_COMMAND__POST_DELETE | Occurs after the Task command is deleted. |
| TASK_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Task command is marked as entered in error. |
| TASK_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Task command is marked as entered in error. |
| TASK_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Task command. |
| TASK_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Task command. |
| UPDATE_GOAL_COMMAND__PRE_ORIGINATE | Occurs before the Update Goal command is first entered into a note. |
| UPDATE_GOAL_COMMAND__POST_ORIGINATE | Occurs after the Update Goal command is first entered into a note. |
| UPDATE_GOAL_COMMAND__PRE_UPDATE | Occurs before data for the Update Goal command is updated. |
| UPDATE_GOAL_COMMAND__POST_UPDATE | Occurs after data for the Update Goal command is updated. |
| UPDATE_GOAL_COMMAND__PRE_COMMIT | Occurs before the Update Goal command is committed. |
| UPDATE_GOAL_COMMAND__POST_COMMIT | Occurs after the Update Goal command is committed. |
| UPDATE_GOAL_COMMAND__PRE_DELETE | Occurs before the Update Goal command is deleted. |
| UPDATE_GOAL_COMMAND__POST_DELETE | Occurs after the Update Goal command is deleted. |
| UPDATE_GOAL_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Update Goal command is marked as entered in error. |
| UPDATE_GOAL_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Update Goal command is marked as entered in error. |
| UPDATE_GOAL_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Update Goal command. |
| UPDATE_GOAL_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Update Goal command. |
| UPDATE_GOAL__GOAL_STATEMENT__POST_SEARCH | Occurs after the initial results are fetched for the goal search in the Update Goal command. |
