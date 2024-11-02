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

## Event Types

The following Canvas events are able to trigger a plugin to execute.

### Record lifecycle events

These events fire as a result of records being created, updated, or deleted.

#### Patients

| Event | Description |
| ----- | ----------- |
| PATIENT_CREATED | Occurs when a patient is created. |
| PATIENT_UPDATED | Occurs when a patient's data is updated. |
| CARE_TEAM_MEMBERSHIP_CREATED | Occurs when a new care team member is added for a patient. |
| CARE_TEAM_MEMBERSHIP_UPDATED | Occurs when a care team member is adjusted for a patient. |
| CARE_TEAM_MEMBERSHIP_DELETED | Occurs when a care team member is removed for a patient. |
| PATIENT_ADDRESS_CREATED | Occurs when an address is added for a patient. |
| PATIENT_ADDRESS_UPDATED | Occurs when one of a patient's addresses are updated. |
| PATIENT_ADDRESS_DELETED | Occurs when one of a patient's addresses are removed. |
| PATIENT_CONTACT_PERSON_CREATED | Occurs when a contact is added for a patient. |
| PATIENT_CONTACT_PERSON_UPDATED | Occurs when one of a patient's contacts is updated. |
| PATIENT_CONTACT_PERSON_DELETED | Occurs when one of a patient's contacts is removed. |
| PATIENT_CONTACT_POINT_CREATED | Occurs when a contact method for a patient is added. |
| PATIENT_CONTACT_POINT_UPDATED | Occurs when a contact method for a patient is updated. |
| PATIENT_CONTACT_POINT_DELETED | Occurs when a contact method for a patient is removed. |

#### Allergy Intolerances

| Event | Description |
| ----- | ----------- |
| ALLERGY_INTOLERANCE_CREATED | Occurs when an allergy is created for a patient. Additional details for the allergy may become available with subsequent ALLERGY_INTOLERANCE_UPDATED events. |
| ALLERGY_INTOLERANCE_UPDATED | Occurs when an allergy is updated for a patient. |

#### Appointments

| Event | Description |
| ----- | ----------- |
| APPOINTMENT_CREATED | Occurs when an appointment is first created/booked. |
| APPOINTMENT_UPDATED | Occurs when details of an appointment are updated. |
| APPOINTMENT_CHECKED_IN | Occurs when a patient has arrived and been checked in for their appointment. |
| APPOINTMENT_RESCHEDULED | Occurs when an appointment is rescheduled. In this case, a new appointment is created that is linked to the appointment it was rescheduled from. |
| APPOINTMENT_RESTORED | Occurs when a cancelled appointment is restored to a non-cancelled status. |
| APPOINTMENT_CANCELED | Occurs when an appointment is cancelled. |
| APPOINTMENT_NO_SHOWED | Occurs when an appointment is marked as a no-show. |

#### Billing Line Items

| Event | Description |
| ----- | ----------- |
| BILLING_LINE_ITEM_CREATED | Occurs when a billing line item is created from adding a CPT code to a note. |
| BILLING_LINE_ITEM_UPDATED | Occurs when a billing line item is modified. |

#### Conditions

| Event | Description |
| ----- | ----------- |
| CONDITION_ASSESSED | Occurs when a condition is assessed through the Assess Condition command. |
| CONDITION_CREATED | Occurs when a condition is diagnosed for a patient. Additional details for the condition may become available with subsequent CONDITION_UPDATED events. |
| CONDITION_RESOLVED | Occurs when a condition is resolved through the Resolve Condition command. |
| CONDITION_UPDATED | Occurs when a condition is updated for a patient. |

#### Consents

| Event | Description |
| ----- | ----------- |
| CONSENT_CREATED | Occurs when a patient consent is created. |
| CONSENT_DELETED | Occurs when a patient consent is removed/deleted. |
| CONSENT_UPDATED | Occurs when a patient consent is updated. |

#### Coverages

| Event | Description |
| ----- | ----------- |
| COVERAGE_CREATED | Occurs when a coverage for a patient is created. |
| COVERAGE_UPDATED | Occurs when a coverage for a patient is updated. |

#### Devices

| Event | Description |
| ----- | ----------- |
| DEVICE_CREATED | Occurs when a device is created. |
| DEVICE_UPDATED | Occurs when a device is updated. |

#### Encounters

| Event | Description |
| ----- | ----------- |
| ENCOUNTER_CREATED | Occurs when an encounter is created. |
| ENCOUNTER_UPDATED | Occurs when an encounter is updated. |

#### Imaging Reports

| Event | Description |
| ----- | ----------- |
| IMAGING_REPORT_CREATED | Occurs when an imaging report is entered into the Data Integration section of Canvas. |
| IMAGING_REPORT_UPDATED | Occurs when an imaging report is updated. |

#### Immunizations

| Event | Description |
| ----- | ----------- |
| IMMUNIZATION_CREATED | Occurs when an immunization is created. Additional details for the immunization may become available with subsequent IMMUNIZATION_UPDATED events. |
| IMMUNIZATION_STATEMENT_CREATED | Occurs when an immunization statement is created. Additional details for the immunization statement may become available with subsequent IMMUNIZATION_STATEMENT_UPDATED events. |
| IMMUNIZATION_STATEMENT_UPDATED | Occurs when an immunization statement is updated. |
| IMMUNIZATION_UPDATED | Occurs when an immunization is updated. |

#### Instructions

| Event | Description |
| ----- | ----------- |
| INSTRUCTION_CREATED | Occurs when an instruction is created using the Instruct command. Additional details for the instruction may become available with subsequent INSTRUCTION_UPDATED events. |
| INSTRUCTION_UPDATED | Occurs when an instruction is updated. |

#### Interviews

| Event | Description |
| ----- | ----------- |
| INTERVIEW_CREATED | Occurs when an interview is created using the Questionnaire command or through the Questionnaire endpoint in the FHIR API. Additional details for the interview may become available with subsequent INTERVIEW_UPDATED events. |
| INTERVIEW_UPDATED | Occurs when an interview is updated. |

#### Labs

| Event | Description |
| ----- | ----------- |
| LAB_ORDER_CREATED | Occurs when a lab order is created via the Lab Order command. Additional details for the lab order may become available with subsequent LAB_ORDER_UPDATED events. |
| LAB_ORDER_UPDATED | Occurs when a lab order is updated. |
| LAB_REPORT_CREATED | Occurs when a lab report is created either through Data Integration, electronic ingestion or the FHIR API. |
| LAB_REPORT_UPDATED | Occurs when a lab report is updated. |

#### Medications

| Event | Description |
| ----- | ----------- |
| MEDICATION_LIST_ITEM_CREATED | Occurs when a medication is added for a patient. |
| MEDICATION_LIST_ITEM_UPDATED | Occurs when a medication is updated for a patient. |
| PRESCRIPTION_CREATED | Occurs when a prescription is created. |
| PRESCRIPTION_UPDATED | Occurs when a prescription is created for a patient using the Prescribe command. Additional details for the prescription become available with subsequent PRESCRIPTION_UPDATED events. |

#### Messaging

| Event | Description |
| ----- | ----------- |
| MESSAGE_CREATED | Occurs when a message (patient/practitioner communication) is created. |

#### Notes

| Event | Description |
| ----- | ----------- |
| NOTE_STATE_CHANGE_EVENT_CREATED |  |
| NOTE_STATE_CHANGE_EVENT_UPDATED |  |

#### Observations

| Event | Description |
| ----- | ----------- |
| OBSERVATION_CREATED | Occurs when an observation is created. |
| OBSERVATION_UPDATED | Occurs when an observation is updated. |

#### Protocol Overrides

| Event | Description |
| ----- | ----------- |
| PROTOCOL_OVERRIDE_CREATED |  |
| PROTOCOL_OVERRIDE_UPDATED |  |
| PROTOCOL_OVERRIDE_DELETED |  |

#### Referral Reports

| Event | Description |
| ----- | ----------- |
| REFERRAL_REPORT_CREATED | Occurs when a specialist consult report is created in Data Integration. |
| REFERRAL_REPORT_UPDATED | Occurs when a specialist consult report is updated. |

#### Tasks

| Event | Description |
| ----- | ----------- |
| TASK_CREATED | Occurs when a task is created. |
| TASK_UPDATED | Occurs when a task is updated. |
| TASK_COMMENT_CREATED | Occurs when a comment is added to a task. |
| TASK_COMMENT_UPDATED |  |
| TASK_COMMENT_DELETED |  |
| TASK_LABELS_ADJUSTED | Occurs when a task's labels are changed. |

#### Vital Signs

| Event | Description |
| ----- | ----------- |
| VITAL_SIGN_CREATED | Occurs when a vitals entry is created for a patient using the Vitals command. Additional details for the vitals become available with subsequent VITAL_SIGN_UPDATED events. |
| VITAL_SIGN_UPDATED | Occurs when a vitals entry is updated for a patient. |


### Command lifecycle events

These events fire during the command lifecycle.

#### Generic events

| Event | Description |
| ----- | ----------- |
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

#### Allergy Command

| Event | Description |
| ----- | ----------- |
| ALLERGY_COMMAND__POST_COMMIT |  |
| ALLERGY_COMMAND__POST_DELETE |  |
| ALLERGY_COMMAND__POST_ENTER_IN_ERROR |  |
| ALLERGY_COMMAND__POST_EXECUTE_ACTION |  |
| ALLERGY_COMMAND__POST_ORIGINATE |  |
| ALLERGY_COMMAND__POST_UPDATE |  |
| ALLERGY_COMMAND__PRE_COMMIT |  |
| ALLERGY_COMMAND__PRE_DELETE |  |
| ALLERGY_COMMAND__PRE_ENTER_IN_ERROR |  |
| ALLERGY_COMMAND__PRE_EXECUTE_ACTION |  |
| ALLERGY_COMMAND__PRE_ORIGINATE |  |
| ALLERGY_COMMAND__PRE_UPDATE |  |
| ALLERGY__ALLERGY__POST_SEARCH |  |
| ALLERGY__ALLERGY__PRE_SEARCH |  |

#### Assess Command

| Event | Description |
| ----- | ----------- |
| ASSESS_COMMAND__CONDITION_SELECTED | Occurs after a condition is selected in the Assess command. |
| ASSESS_COMMAND__POST_COMMIT | Occurs after the Assess command is committed. |
| ASSESS_COMMAND__POST_DELETE | Occurs after the Assess command is deleted. |
| ASSESS_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Assess command is marked as entered in error. |
| ASSESS_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Assess command. |
| ASSESS_COMMAND__POST_ORIGINATE | Occurs after the Assess command is first entered into a note. |
| ASSESS_COMMAND__POST_UPDATE | Occurs after data for the Assess command is updated. |
| ASSESS_COMMAND__PRE_COMMIT | Occurs before the Assess command is committed. |
| ASSESS_COMMAND__PRE_DELETE | Occurs before the Assess command is deleted. |
| ASSESS_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Assess command is marked as entered in error. |
| ASSESS_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Assess command. |
| ASSESS_COMMAND__PRE_ORIGINATE | Occurs before the Assess command is first entered into a note. |
| ASSESS_COMMAND__PRE_UPDATE | Occurs before data for the Assess command is updated. |
| ASSESS__CONDITION__POST_SEARCH | Occurs after the initial results are fetched for the condition search in the Assess command. |
| ASSESS__CONDITION__PRE_SEARCH |  |

#### Clipboard Command

| Event | Description |
| ----- | ----------- |
| CLIPBOARD_COMMAND__POST_COMMIT |  |
| CLIPBOARD_COMMAND__POST_DELETE |  |
| CLIPBOARD_COMMAND__POST_ENTER_IN_ERROR |  |
| CLIPBOARD_COMMAND__POST_EXECUTE_ACTION |  |
| CLIPBOARD_COMMAND__POST_ORIGINATE |  |
| CLIPBOARD_COMMAND__POST_UPDATE |  |
| CLIPBOARD_COMMAND__PRE_COMMIT |  |
| CLIPBOARD_COMMAND__PRE_DELETE |  |
| CLIPBOARD_COMMAND__PRE_ENTER_IN_ERROR |  |
| CLIPBOARD_COMMAND__PRE_EXECUTE_ACTION |  |
| CLIPBOARD_COMMAND__PRE_ORIGINATE |  |
| CLIPBOARD_COMMAND__PRE_UPDATE |  |

#### Close Goal Command

| Event | Description |
| ----- | ----------- |
| CLOSE_GOAL_COMMAND__POST_COMMIT |  |
| CLOSE_GOAL_COMMAND__POST_DELETE |  |
| CLOSE_GOAL_COMMAND__POST_ENTER_IN_ERROR |  |
| CLOSE_GOAL_COMMAND__POST_EXECUTE_ACTION |  |
| CLOSE_GOAL_COMMAND__POST_ORIGINATE |  |
| CLOSE_GOAL_COMMAND__POST_UPDATE |  |
| CLOSE_GOAL_COMMAND__PRE_COMMIT |  |
| CLOSE_GOAL_COMMAND__PRE_DELETE |  |
| CLOSE_GOAL_COMMAND__PRE_ENTER_IN_ERROR |  |
| CLOSE_GOAL_COMMAND__PRE_EXECUTE_ACTION |  |
| CLOSE_GOAL_COMMAND__PRE_ORIGINATE |  |
| CLOSE_GOAL_COMMAND__PRE_UPDATE |  |
| CLOSE_GOAL__GOAL_ID__POST_SEARCH |  |
| CLOSE_GOAL__GOAL_ID__PRE_SEARCH |  |

#### Diagnose Command

| Event | Description |
| ----- | ----------- |
| DIAGNOSE_COMMAND__POST_COMMIT |  |
| DIAGNOSE_COMMAND__POST_DELETE |  |
| DIAGNOSE_COMMAND__POST_ENTER_IN_ERROR |  |
| DIAGNOSE_COMMAND__POST_EXECUTE_ACTION |  |
| DIAGNOSE_COMMAND__POST_ORIGINATE |  |
| DIAGNOSE_COMMAND__POST_UPDATE |  |
| DIAGNOSE_COMMAND__PRE_COMMIT |  |
| DIAGNOSE_COMMAND__PRE_DELETE |  |
| DIAGNOSE_COMMAND__PRE_ENTER_IN_ERROR |  |
| DIAGNOSE_COMMAND__PRE_EXECUTE_ACTION |  |
| DIAGNOSE_COMMAND__PRE_ORIGINATE |  |
| DIAGNOSE_COMMAND__PRE_UPDATE |  |
| DIAGNOSE__DIAGNOSE__POST_SEARCH | Occurs after the initial results are fetched for the diagnosis search in the Diagnose command. |
| DIAGNOSE__DIAGNOSE__PRE_SEARCH |  |

#### Educational Material Command

| Event | Description |
| ----- | ----------- |
| EDUCATIONAL_MATERIAL_COMMAND__POST_COMMIT |  |
| EDUCATIONAL_MATERIAL_COMMAND__POST_DELETE |  |
| EDUCATIONAL_MATERIAL_COMMAND__POST_ENTER_IN_ERROR |  |
| EDUCATIONAL_MATERIAL_COMMAND__POST_EXECUTE_ACTION |  |
| EDUCATIONAL_MATERIAL_COMMAND__POST_ORIGINATE |  |
| EDUCATIONAL_MATERIAL_COMMAND__POST_UPDATE |  |
| EDUCATIONAL_MATERIAL_COMMAND__PRE_COMMIT |  |
| EDUCATIONAL_MATERIAL_COMMAND__PRE_DELETE |  |
| EDUCATIONAL_MATERIAL_COMMAND__PRE_ENTER_IN_ERROR |  |
| EDUCATIONAL_MATERIAL_COMMAND__PRE_EXECUTE_ACTION |  |
| EDUCATIONAL_MATERIAL_COMMAND__PRE_ORIGINATE |  |
| EDUCATIONAL_MATERIAL_COMMAND__PRE_UPDATE |  |
| EDUCATIONAL_MATERIAL__LANGUAGE__POST_SEARCH |  |
| EDUCATIONAL_MATERIAL__LANGUAGE__PRE_SEARCH |  |
| EDUCATIONAL_MATERIAL__TITLE__POST_SEARCH |  |
| EDUCATIONAL_MATERIAL__TITLE__PRE_SEARCH |  |

#### Family History Command

| Event | Description |
| ----- | ----------- |
| FAMILY_HISTORY_COMMAND__POST_COMMIT |  |
| FAMILY_HISTORY_COMMAND__POST_DELETE |  |
| FAMILY_HISTORY_COMMAND__POST_ENTER_IN_ERROR |  |
| FAMILY_HISTORY_COMMAND__POST_EXECUTE_ACTION |  |
| FAMILY_HISTORY_COMMAND__POST_ORIGINATE |  |
| FAMILY_HISTORY_COMMAND__POST_UPDATE |  |
| FAMILY_HISTORY_COMMAND__PRE_COMMIT |  |
| FAMILY_HISTORY_COMMAND__PRE_DELETE |  |
| FAMILY_HISTORY_COMMAND__PRE_ENTER_IN_ERROR |  |
| FAMILY_HISTORY_COMMAND__PRE_EXECUTE_ACTION |  |
| FAMILY_HISTORY_COMMAND__PRE_ORIGINATE |  |
| FAMILY_HISTORY_COMMAND__PRE_UPDATE |  |
| FAMILY_HISTORY__FAMILY_HISTORY__POST_SEARCH |  |
| FAMILY_HISTORY__FAMILY_HISTORY__PRE_SEARCH |  |
| FAMILY_HISTORY__RELATIVE__POST_SEARCH |  |
| FAMILY_HISTORY__RELATIVE__PRE_SEARCH |  |

#### Goal Command

| Event | Description |
| ----- | ----------- |
| GOAL_COMMAND__POST_COMMIT | Occurs after the Goal command is committed. |
| GOAL_COMMAND__POST_DELETE | Occurs after the Assess command is deleted. |
| GOAL_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Goal command is marked as entered in error. |
| GOAL_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Goal command. |
| GOAL_COMMAND__POST_ORIGINATE | Occurs after the Goal command is first entered into a note. |
| GOAL_COMMAND__POST_UPDATE | Occurs after data for the Goal command is updated. |
| GOAL_COMMAND__PRE_COMMIT | Occurs before the Goal command is committed. |
| GOAL_COMMAND__PRE_DELETE | Occurs before the Assess command is deleted. |
| GOAL_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Goal command is marked as entered in error. |
| GOAL_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Goal command. |
| GOAL_COMMAND__PRE_ORIGINATE | Occurs before the Goal command is first entered into a note. |
| GOAL_COMMAND__PRE_UPDATE | Occurs before data for the Goal command is updated. |

#### History of Present Illness Command

| Event | Description |
| ----- | ----------- |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_COMMIT | Occurs after the History of Present Illness command is committed. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_DELETE | Occurs after the History of Present Illness command is deleted. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_ENTER_IN_ERROR | Occurs after the History of Present Illness command is marked as entered in error. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the History of Present Illness command. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_ORIGINATE | Occurs after the History of Present Illness command is first entered into a note. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_UPDATE | Occurs after data for the History of Present Illness command is updated. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_COMMIT | Occurs before the History of Present Illness command is committed. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_DELETE | Occurs before the History of Present Illness command is deleted. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the History of Present Illness command is marked as entered in error. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the History of Present Illness command. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_ORIGINATE | Occurs before the History of Present Illness command is first entered into a note. |
| HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_UPDATE | Occurs before data for the History of Present Illness command is updated. |

#### Imaging Order Command

| Event | Description |
| ----- | ----------- |
| IMAGING_ORDER_COMMAND__POST_COMMIT |  |
| IMAGING_ORDER_COMMAND__POST_DELETE |  |
| IMAGING_ORDER_COMMAND__POST_ENTER_IN_ERROR |  |
| IMAGING_ORDER_COMMAND__POST_EXECUTE_ACTION |  |
| IMAGING_ORDER_COMMAND__POST_ORIGINATE |  |
| IMAGING_ORDER_COMMAND__POST_UPDATE |  |
| IMAGING_ORDER_COMMAND__PRE_COMMIT |  |
| IMAGING_ORDER_COMMAND__PRE_DELETE |  |
| IMAGING_ORDER_COMMAND__PRE_ENTER_IN_ERROR |  |
| IMAGING_ORDER_COMMAND__PRE_EXECUTE_ACTION |  |
| IMAGING_ORDER_COMMAND__PRE_ORIGINATE |  |
| IMAGING_ORDER_COMMAND__PRE_UPDATE |  |
| IMAGING_ORDER__IMAGE__POST_SEARCH |  |
| IMAGING_ORDER__IMAGE__PRE_SEARCH |  |
| IMAGING_ORDER__IMAGING_CENTER__POST_SEARCH |  |
| IMAGING_ORDER__IMAGING_CENTER__PRE_SEARCH |  |
| IMAGING_ORDER__INDICATIONS__POST_SEARCH |  |
| IMAGING_ORDER__INDICATIONS__PRE_SEARCH |  |
| IMAGING_ORDER__ORDERING_PROVIDER__POST_SEARCH |  |
| IMAGING_ORDER__ORDERING_PROVIDER__PRE_SEARCH |  |

#### Immunization Statement Command

| Event | Description |
| ----- | ----------- |
| IMMUNIZATION_STATEMENT_COMMAND__POST_COMMIT |  |
| IMMUNIZATION_STATEMENT_COMMAND__POST_DELETE |  |
| IMMUNIZATION_STATEMENT_COMMAND__POST_ENTER_IN_ERROR |  |
| IMMUNIZATION_STATEMENT_COMMAND__POST_EXECUTE_ACTION |  |
| IMMUNIZATION_STATEMENT_COMMAND__POST_ORIGINATE |  |
| IMMUNIZATION_STATEMENT_COMMAND__POST_UPDATE |  |
| IMMUNIZATION_STATEMENT_COMMAND__PRE_COMMIT |  |
| IMMUNIZATION_STATEMENT_COMMAND__PRE_DELETE |  |
| IMMUNIZATION_STATEMENT_COMMAND__PRE_ENTER_IN_ERROR |  |
| IMMUNIZATION_STATEMENT_COMMAND__PRE_EXECUTE_ACTION |  |
| IMMUNIZATION_STATEMENT_COMMAND__PRE_ORIGINATE |  |
| IMMUNIZATION_STATEMENT_COMMAND__PRE_UPDATE |  |
| IMMUNIZATION_STATEMENT__STATEMENT__POST_SEARCH |  |
| IMMUNIZATION_STATEMENT__STATEMENT__PRE_SEARCH |  |

#### Immunize Command

| Event | Description |
| ----- | ----------- |
| IMMUNIZE_COMMAND__POST_COMMIT |  |
| IMMUNIZE_COMMAND__POST_DELETE |  |
| IMMUNIZE_COMMAND__POST_ENTER_IN_ERROR |  |
| IMMUNIZE_COMMAND__POST_EXECUTE_ACTION |  |
| IMMUNIZE_COMMAND__POST_ORIGINATE |  |
| IMMUNIZE_COMMAND__POST_UPDATE |  |
| IMMUNIZE_COMMAND__PRE_COMMIT |  |
| IMMUNIZE_COMMAND__PRE_DELETE |  |
| IMMUNIZE_COMMAND__PRE_ENTER_IN_ERROR |  |
| IMMUNIZE_COMMAND__PRE_EXECUTE_ACTION |  |
| IMMUNIZE_COMMAND__PRE_ORIGINATE |  |
| IMMUNIZE_COMMAND__PRE_UPDATE |  |
| IMMUNIZE__CODING__POST_SEARCH |  |
| IMMUNIZE__CODING__PRE_SEARCH |  |
| IMMUNIZE__GIVEN_BY__POST_SEARCH |  |
| IMMUNIZE__GIVEN_BY__PRE_SEARCH |  |
| IMMUNIZE__LOT_NUMBER__POST_SEARCH |  |
| IMMUNIZE__LOT_NUMBER__PRE_SEARCH |  |

#### Instruct Command

| Event | Description |
| ----- | ----------- |
| INSTRUCT_COMMAND__POST_COMMIT |  |
| INSTRUCT_COMMAND__POST_DELETE |  |
| INSTRUCT_COMMAND__POST_ENTER_IN_ERROR |  |
| INSTRUCT_COMMAND__POST_EXECUTE_ACTION |  |
| INSTRUCT_COMMAND__POST_ORIGINATE |  |
| INSTRUCT_COMMAND__POST_UPDATE |  |
| INSTRUCT_COMMAND__PRE_COMMIT |  |
| INSTRUCT_COMMAND__PRE_DELETE |  |
| INSTRUCT_COMMAND__PRE_ENTER_IN_ERROR |  |
| INSTRUCT_COMMAND__PRE_EXECUTE_ACTION |  |
| INSTRUCT_COMMAND__PRE_ORIGINATE |  |
| INSTRUCT_COMMAND__PRE_UPDATE |  |
| INSTRUCT__INSTRUCT__POST_SEARCH |  |
| INSTRUCT__INSTRUCT__PRE_SEARCH |  |

#### Lab Order Command

| Event | Description |
| ----- | ----------- |
| LAB_ORDER_COMMAND__POST_COMMIT |  |
| LAB_ORDER_COMMAND__POST_DELETE |  |
| LAB_ORDER_COMMAND__POST_ENTER_IN_ERROR |  |
| LAB_ORDER_COMMAND__POST_EXECUTE_ACTION |  |
| LAB_ORDER_COMMAND__POST_ORIGINATE |  |
| LAB_ORDER_COMMAND__POST_UPDATE |  |
| LAB_ORDER_COMMAND__PRE_COMMIT |  |
| LAB_ORDER_COMMAND__PRE_DELETE |  |
| LAB_ORDER_COMMAND__PRE_ENTER_IN_ERROR |  |
| LAB_ORDER_COMMAND__PRE_EXECUTE_ACTION |  |
| LAB_ORDER_COMMAND__PRE_ORIGINATE |  |
| LAB_ORDER_COMMAND__PRE_UPDATE |  |
| LAB_ORDER__DIAGNOSIS__POST_SEARCH |  |
| LAB_ORDER__DIAGNOSIS__PRE_SEARCH |  |
| LAB_ORDER__LAB_PARTNER__POST_SEARCH |  |
| LAB_ORDER__LAB_PARTNER__PRE_SEARCH |  |
| LAB_ORDER__ORDERING_PROVIDER__POST_SEARCH |  |
| LAB_ORDER__ORDERING_PROVIDER__PRE_SEARCH |  |
| LAB_ORDER__TESTS__POST_SEARCH |  |
| LAB_ORDER__TESTS__PRE_SEARCH |  |

#### Medical History Command

| Event | Description |
| ----- | ----------- |
| MEDICAL_HISTORY_COMMAND__POST_COMMIT |  |
| MEDICAL_HISTORY_COMMAND__POST_DELETE |  |
| MEDICAL_HISTORY_COMMAND__POST_ENTER_IN_ERROR |  |
| MEDICAL_HISTORY_COMMAND__POST_EXECUTE_ACTION |  |
| MEDICAL_HISTORY_COMMAND__POST_ORIGINATE |  |
| MEDICAL_HISTORY_COMMAND__POST_UPDATE |  |
| MEDICAL_HISTORY_COMMAND__PRE_COMMIT |  |
| MEDICAL_HISTORY_COMMAND__PRE_DELETE |  |
| MEDICAL_HISTORY_COMMAND__PRE_ENTER_IN_ERROR |  |
| MEDICAL_HISTORY_COMMAND__PRE_EXECUTE_ACTION |  |
| MEDICAL_HISTORY_COMMAND__PRE_ORIGINATE |  |
| MEDICAL_HISTORY_COMMAND__PRE_UPDATE |  |
| MEDICAL_HISTORY__APPROXIMATE_END_DATE__POST_SEARCH |  |
| MEDICAL_HISTORY__APPROXIMATE_END_DATE__PRE_SEARCH |  |
| MEDICAL_HISTORY__APPROXIMATE_START_DATE__POST_SEARCH |  |
| MEDICAL_HISTORY__APPROXIMATE_START_DATE__PRE_SEARCH |  |
| MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__POST_SEARCH |  |
| MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__PRE_SEARCH |  |

#### Medication Statement Command

| Event | Description |
| ----- | ----------- |
| MEDICATION_STATEMENT_COMMAND__POST_COMMIT | Occurs after the Medication Statement command is committed. |
| MEDICATION_STATEMENT_COMMAND__POST_DELETE | Occurs after the Medication Statement command is deleted. |
| MEDICATION_STATEMENT_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Medication Statement command is marked as entered in error. |
| MEDICATION_STATEMENT_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Medication Statement command. |
| MEDICATION_STATEMENT_COMMAND__POST_ORIGINATE | Occurs after the Medication Statement command is first entered into a note. |
| MEDICATION_STATEMENT_COMMAND__POST_UPDATE | Occurs after data for the Medication Statement command is updated. |
| MEDICATION_STATEMENT_COMMAND__PRE_COMMIT | Occurs before the Medication Statement command is committed. |
| MEDICATION_STATEMENT_COMMAND__PRE_DELETE | Occurs before the Medication Statement command is deleted. |
| MEDICATION_STATEMENT_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Medication Statement command is marked as entered in error. |
| MEDICATION_STATEMENT_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Medication Statement command. |
| MEDICATION_STATEMENT_COMMAND__PRE_ORIGINATE | Occurs before the Medication Statement command is first entered into a note. |
| MEDICATION_STATEMENT_COMMAND__PRE_UPDATE | Occurs before data for the Medication Statement command is updated. |
| MEDICATION_STATEMENT__MEDICATION__POST_SEARCH | Occurs after the initial results are fetched for the medication search in the medication statement command. |
| MEDICATION_STATEMENT__MEDICATION__PRE_SEARCH | Occurs before a medication statement search for a medication. |
| MEDICATION_STATEMENT__MEDICATION__SELECTED | Occurs when a medication is selected from Medication Statement search results. |

#### Perfom Command

| Event | Description |
| ----- | ----------- |
| PERFORM_COMMAND__POST_COMMIT |  |
| PERFORM_COMMAND__POST_DELETE |  |
| PERFORM_COMMAND__POST_ENTER_IN_ERROR |  |
| PERFORM_COMMAND__POST_EXECUTE_ACTION |  |
| PERFORM_COMMAND__POST_ORIGINATE |  |
| PERFORM_COMMAND__POST_UPDATE |  |
| PERFORM_COMMAND__PRE_COMMIT |  |
| PERFORM_COMMAND__PRE_DELETE |  |
| PERFORM_COMMAND__PRE_ENTER_IN_ERROR |  |
| PERFORM_COMMAND__PRE_EXECUTE_ACTION |  |
| PERFORM_COMMAND__PRE_ORIGINATE |  |
| PERFORM_COMMAND__PRE_UPDATE |  |
| PERFORM__PERFORM__POST_SEARCH |  |
| PERFORM__PERFORM__PRE_SEARCH |  |

#### Physical Exam Command

| Event | Description |
| ----- | ----------- |
| PHYSICAL_EXAM_COMMAND__POST_COMMIT |  |
| PHYSICAL_EXAM_COMMAND__POST_DELETE |  |
| PHYSICAL_EXAM_COMMAND__POST_ENTER_IN_ERROR |  |
| PHYSICAL_EXAM_COMMAND__POST_EXECUTE_ACTION |  |
| PHYSICAL_EXAM_COMMAND__POST_ORIGINATE |  |
| PHYSICAL_EXAM_COMMAND__POST_UPDATE |  |
| PHYSICAL_EXAM_COMMAND__PRE_COMMIT |  |
| PHYSICAL_EXAM_COMMAND__PRE_DELETE |  |
| PHYSICAL_EXAM_COMMAND__PRE_ENTER_IN_ERROR |  |
| PHYSICAL_EXAM_COMMAND__PRE_EXECUTE_ACTION |  |
| PHYSICAL_EXAM_COMMAND__PRE_ORIGINATE |  |
| PHYSICAL_EXAM_COMMAND__PRE_UPDATE |  |
| PHYSICAL_EXAM__QUESTIONNAIRE__POST_SEARCH |  |
| PHYSICAL_EXAM__QUESTIONNAIRE__PRE_SEARCH |  |

#### Plan Command

| Event | Description |
| ----- | ----------- |
| PLAN_COMMAND__POST_COMMIT | Occurs after the Plan command is committed. |
| PLAN_COMMAND__POST_DELETE | Occurs after the Plan command is deleted. |
| PLAN_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Plan command is marked as entered in error. |
| PLAN_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Plan command. |
| PLAN_COMMAND__POST_ORIGINATE | Occurs after the Plan command is first entered into a note. |
| PLAN_COMMAND__POST_UPDATE | Occurs after data for the Plan command is updated. |
| PLAN_COMMAND__PRE_COMMIT | Occurs before the Plan command is committed. |
| PLAN_COMMAND__PRE_DELETE | Occurs before the Plan command is deleted. |
| PLAN_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Plan command is marked as entered in error. |
| PLAN_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Plan command. |
| PLAN_COMMAND__PRE_ORIGINATE | Occurs before the Plan command is first entered into a note. |
| PLAN_COMMAND__PRE_UPDATE | Occurs before data for the Plan command is updated. |

#### Prescribe Command

| Event | Description |
| ----- | ----------- |
| PRESCRIBE_COMMAND__POST_COMMIT | Occurs after the Prescribe command is committed. |
| PRESCRIBE_COMMAND__POST_DELETE | Occurs after the Prescribe command is deleted. |
| PRESCRIBE_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Prescribe command is marked as entered in error. |
| PRESCRIBE_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Prescribe command. |
| PRESCRIBE_COMMAND__POST_ORIGINATE | Occurs after the Prescribe command is first entered into a note. |
| PRESCRIBE_COMMAND__POST_UPDATE | Occurs after data for the Prescribe command is updated. |
| PRESCRIBE_COMMAND__PRE_COMMIT | Occurs before the Prescribecommand is committed. |
| PRESCRIBE_COMMAND__PRE_DELETE | Occurs before the Prescribe command is deleted. |
| PRESCRIBE_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Prescribe command is marked as entered in error. |
| PRESCRIBE_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Prescribe command. |
| PRESCRIBE_COMMAND__PRE_ORIGINATE | Occurs before the Prescribe command is first entered into a note. |
| PRESCRIBE_COMMAND__PRE_UPDATE | Occurs before data for the Prescribe command is updated. |
| PRESCRIBE__INDICATIONS__POST_SEARCH |  |
| PRESCRIBE__INDICATIONS__PRE_SEARCH |  |
| PRESCRIBE__PHARMACY__POST_SEARCH |  |
| PRESCRIBE__PHARMACY__PRE_SEARCH |  |
| PRESCRIBE__PRESCRIBE__POST_SEARCH | Occurs after the initial results are fetched for the medication search in the Prescribe command. |
| PRESCRIBE__PRESCRIBE__PRE_SEARCH |  |

#### Questionnaire Command

| Event | Description |
| ----- | ----------- |
| QUESTIONNAIRE_COMMAND__POST_COMMIT | Occurs after the Questionnaire command is committed. |
| QUESTIONNAIRE_COMMAND__POST_DELETE | Occurs after the Questionnaire command is deleted. |
| QUESTIONNAIRE_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Questionnaire command is marked as entered in error. |
| QUESTIONNAIRE_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Questionnaire command. |
| QUESTIONNAIRE_COMMAND__POST_ORIGINATE | Occurs after the Questionnaire command is first entered into a note. |
| QUESTIONNAIRE_COMMAND__POST_UPDATE | Occurs after data for the Questionnaire command is updated. |
| QUESTIONNAIRE_COMMAND__PRE_COMMIT | Occurs before the Questionnaire command is committed. |
| QUESTIONNAIRE_COMMAND__PRE_DELETE | Occurs before the Questionnaire command is deleted. |
| QUESTIONNAIRE_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Questionnaire command is marked as entered in error. |
| QUESTIONNAIRE_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Questionnaire command. |
| QUESTIONNAIRE_COMMAND__PRE_ORIGINATE | Occurs before the Questionnaire command is first entered into a note. |
| QUESTIONNAIRE_COMMAND__PRE_UPDATE | Occurs before data for the Questionnaire command is updated. |
| QUESTIONNAIRE__QUESTIONNAIRE__POST_SEARCH | Occurs after the initial results are fetched for the questionnaire search in the Questionnaire command. |
| QUESTIONNAIRE__QUESTIONNAIRE__PRE_SEARCH |  |

#### Reason for Visit Command

| Event | Description |
| ----- | ----------- |
| REASON_FOR_VISIT_COMMAND__POST_COMMIT | Occurs after the Reason for Visit command is committed. |
| REASON_FOR_VISIT_COMMAND__POST_DELETE | Occurs after the Reason for Visit command is deleted. |
| REASON_FOR_VISIT_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Reason for Visit command is marked as entered in error. |
| REASON_FOR_VISIT_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Reason for Visit command. |
| REASON_FOR_VISIT_COMMAND__POST_ORIGINATE | Occurs after the Reason for Visit command is first entered into a note. |
| REASON_FOR_VISIT_COMMAND__POST_UPDATE | Occurs after data for the Reason for Visit command is updated. |
| REASON_FOR_VISIT_COMMAND__PRE_COMMIT | Occurs before the Reason for Visit command is committed. |
| REASON_FOR_VISIT_COMMAND__PRE_DELETE | Occurs before the Reason for Visit command is deleted. |
| REASON_FOR_VISIT_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Reason for Visit command is marked as entered in error. |
| REASON_FOR_VISIT_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Reason for Visit command. |
| REASON_FOR_VISIT_COMMAND__PRE_ORIGINATE | Occurs before the Reason for Visit command is first entered into a note. |
| REASON_FOR_VISIT_COMMAND__PRE_UPDATE | Occurs before data for the Reason for Visit command is updated. |
| REASON_FOR_VISIT__CODING__POST_SEARCH | Occurs after the initial results are fetched for the reason search in the Reason for Visit command. |
| REASON_FOR_VISIT__CODING__PRE_SEARCH |  |

#### Refill Prescription Command

| Event | Description |
| ----- | ----------- |
| REFILL_COMMAND__POST_COMMIT |  |
| REFILL_COMMAND__POST_DELETE |  |
| REFILL_COMMAND__POST_ENTER_IN_ERROR |  |
| REFILL_COMMAND__POST_EXECUTE_ACTION |  |
| REFILL_COMMAND__POST_ORIGINATE |  |
| REFILL_COMMAND__POST_UPDATE |  |
| REFILL_COMMAND__PRE_COMMIT |  |
| REFILL_COMMAND__PRE_DELETE |  |
| REFILL_COMMAND__PRE_ENTER_IN_ERROR |  |
| REFILL_COMMAND__PRE_EXECUTE_ACTION |  |
| REFILL_COMMAND__PRE_ORIGINATE |  |
| REFILL_COMMAND__PRE_UPDATE |  |
| REFILL__INDICATIONS__POST_SEARCH |  |
| REFILL__INDICATIONS__PRE_SEARCH |  |
| REFILL__PHARMACY__POST_SEARCH |  |
| REFILL__PHARMACY__PRE_SEARCH |  |
| REFILL__PRESCRIBE__POST_SEARCH |  |
| REFILL__PRESCRIBE__PRE_SEARCH |  |

#### Remove Allergy Command

| Event | Description |
| ----- | ----------- |
| REMOVE_ALLERGY_COMMAND__POST_COMMIT |  |
| REMOVE_ALLERGY_COMMAND__POST_DELETE |  |
| REMOVE_ALLERGY_COMMAND__POST_ENTER_IN_ERROR |  |
| REMOVE_ALLERGY_COMMAND__POST_EXECUTE_ACTION |  |
| REMOVE_ALLERGY_COMMAND__POST_ORIGINATE |  |
| REMOVE_ALLERGY_COMMAND__POST_UPDATE |  |
| REMOVE_ALLERGY_COMMAND__PRE_COMMIT |  |
| REMOVE_ALLERGY_COMMAND__PRE_DELETE |  |
| REMOVE_ALLERGY_COMMAND__PRE_ENTER_IN_ERROR |  |
| REMOVE_ALLERGY_COMMAND__PRE_EXECUTE_ACTION |  |
| REMOVE_ALLERGY_COMMAND__PRE_ORIGINATE |  |
| REMOVE_ALLERGY_COMMAND__PRE_UPDATE |  |
| REMOVE_ALLERGY__ALLERGY__POST_SEARCH |  |
| REMOVE_ALLERGY__ALLERGY__PRE_SEARCH |  |

#### Review of Systems Command

| Event | Description |
| ----- | ----------- |
| ROS_COMMAND__POST_COMMIT |  |
| ROS_COMMAND__POST_DELETE |  |
| ROS_COMMAND__POST_ENTER_IN_ERROR |  |
| ROS_COMMAND__POST_EXECUTE_ACTION |  |
| ROS_COMMAND__POST_ORIGINATE |  |
| ROS_COMMAND__POST_UPDATE |  |
| ROS_COMMAND__PRE_COMMIT |  |
| ROS_COMMAND__PRE_DELETE |  |
| ROS_COMMAND__PRE_ENTER_IN_ERROR |  |
| ROS_COMMAND__PRE_EXECUTE_ACTION |  |
| ROS_COMMAND__PRE_ORIGINATE |  |
| ROS_COMMAND__PRE_UPDATE |  |
| ROS__QUESTIONNAIRE__POST_SEARCH |  |
| ROS__QUESTIONNAIRE__PRE_SEARCH |  |

#### Stop Medication Command

| Event | Description |
| ----- | ----------- |
| STOP_MEDICATION_COMMAND__POST_COMMIT | Occurs after the Stop Medication command is committed. |
| STOP_MEDICATION_COMMAND__POST_DELETE | Occurs after the Stop Medication command is deleted. |
| STOP_MEDICATION_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Stop Medication command is marked as entered in error. |
| STOP_MEDICATION_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Stop Medication command. |
| STOP_MEDICATION_COMMAND__POST_ORIGINATE | Occurs after the Stop Medication command is first entered into a note. |
| STOP_MEDICATION_COMMAND__POST_UPDATE | Occurs after data for the Stop Medication command is updated. |
| STOP_MEDICATION_COMMAND__PRE_COMMIT | Occurs before the Stop Medication command is committed. |
| STOP_MEDICATION_COMMAND__PRE_DELETE | Occurs before the Stop Medication command is deleted. |
| STOP_MEDICATION_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Stop Medication command is marked as entered in error. |
| STOP_MEDICATION_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Stop Medication command. |
| STOP_MEDICATION_COMMAND__PRE_ORIGINATE | Occurs before the Stop Medication command is first entered into a note. |
| STOP_MEDICATION_COMMAND__PRE_UPDATE | Occurs before data for the Stop Medication command is updated. |
| STOP_MEDICATION__MEDICATION__POST_SEARCH | Occurs after the initial results are fetched for the medication search in the Stop Medication command. |
| STOP_MEDICATION__MEDICATION__PRE_SEARCH |  |

#### Structured Assessment Command

| Event | Description |
| ----- | ----------- |
| STRUCTURED_ASSESSMENT_COMMAND__POST_COMMIT |  |
| STRUCTURED_ASSESSMENT_COMMAND__POST_DELETE |  |
| STRUCTURED_ASSESSMENT_COMMAND__POST_ENTER_IN_ERROR |  |
| STRUCTURED_ASSESSMENT_COMMAND__POST_EXECUTE_ACTION |  |
| STRUCTURED_ASSESSMENT_COMMAND__POST_ORIGINATE |  |
| STRUCTURED_ASSESSMENT_COMMAND__POST_UPDATE |  |
| STRUCTURED_ASSESSMENT_COMMAND__PRE_COMMIT |  |
| STRUCTURED_ASSESSMENT_COMMAND__PRE_DELETE |  |
| STRUCTURED_ASSESSMENT_COMMAND__PRE_ENTER_IN_ERROR |  |
| STRUCTURED_ASSESSMENT_COMMAND__PRE_EXECUTE_ACTION |  |
| STRUCTURED_ASSESSMENT_COMMAND__PRE_ORIGINATE |  |
| STRUCTURED_ASSESSMENT_COMMAND__PRE_UPDATE |  |
| STRUCTURED_ASSESSMENT__QUESTIONNAIRE__POST_SEARCH |  |
| STRUCTURED_ASSESSMENT__QUESTIONNAIRE__PRE_SEARCH |  |

#### Surgical History Command

| Event | Description |
| ----- | ----------- |
| SURGICAL_HISTORY_COMMAND__POST_COMMIT |  |
| SURGICAL_HISTORY_COMMAND__POST_DELETE |  |
| SURGICAL_HISTORY_COMMAND__POST_ENTER_IN_ERROR |  |
| SURGICAL_HISTORY_COMMAND__POST_EXECUTE_ACTION |  |
| SURGICAL_HISTORY_COMMAND__POST_ORIGINATE |  |
| SURGICAL_HISTORY_COMMAND__POST_UPDATE |  |
| SURGICAL_HISTORY_COMMAND__PRE_COMMIT |  |
| SURGICAL_HISTORY_COMMAND__PRE_DELETE |  |
| SURGICAL_HISTORY_COMMAND__PRE_ENTER_IN_ERROR |  |
| SURGICAL_HISTORY_COMMAND__PRE_EXECUTE_ACTION |  |
| SURGICAL_HISTORY_COMMAND__PRE_ORIGINATE |  |
| SURGICAL_HISTORY_COMMAND__PRE_UPDATE |  |
| SURGICAL_HISTORY__PAST_SURGICAL_HISTORY__POST_SEARCH |  |
| SURGICAL_HISTORY__PAST_SURGICAL_HISTORY__PRE_SEARCH |  |

#### Task Command

| Event | Description |
| ----- | ----------- |
| TASK_COMMAND__POST_COMMIT | Occurs after the Task command is committed. |
| TASK_COMMAND__POST_DELETE | Occurs after the Task command is deleted. |
| TASK_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Task command is marked as entered in error. |
| TASK_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Task command. |
| TASK_COMMAND__POST_ORIGINATE | Occurs after the Task command is first entered into a note. |
| TASK_COMMAND__POST_UPDATE | Occurs after data for the Task command is updated. |
| TASK_COMMAND__PRE_COMMIT | Occurs before the Task command is committed. |
| TASK_COMMAND__PRE_DELETE | Occurs before the Task command is deleted. |
| TASK_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Task command is marked as entered in error. |
| TASK_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Task command. |
| TASK_COMMAND__PRE_ORIGINATE | Occurs before the Task command is first entered into a note. |
| TASK_COMMAND__PRE_UPDATE | Occurs before data for the Task command is updated. |
| TASK__ASSIGN_TO__POST_SEARCH |  |
| TASK__ASSIGN_TO__PRE_SEARCH |  |
| TASK__LABELS__POST_SEARCH |  |
| TASK__LABELS__PRE_SEARCH |  |

#### Update Goal Command

| Event | Description |
| ----- | ----------- |
| UPDATE_GOAL_COMMAND__POST_COMMIT | Occurs after the Update Goal command is committed. |
| UPDATE_GOAL_COMMAND__POST_DELETE | Occurs after the Update Goal command is deleted. |
| UPDATE_GOAL_COMMAND__POST_ENTER_IN_ERROR | Occurs after the Update Goal command is marked as entered in error. |
| UPDATE_GOAL_COMMAND__POST_EXECUTE_ACTION | Occurs after an action is executed on the Update Goal command. |
| UPDATE_GOAL_COMMAND__POST_ORIGINATE | Occurs after the Update Goal command is first entered into a note. |
| UPDATE_GOAL_COMMAND__POST_UPDATE | Occurs after data for the Update Goal command is updated. |
| UPDATE_GOAL_COMMAND__PRE_COMMIT | Occurs before the Update Goal command is committed. |
| UPDATE_GOAL_COMMAND__PRE_DELETE | Occurs before the Update Goal command is deleted. |
| UPDATE_GOAL_COMMAND__PRE_ENTER_IN_ERROR | Occurs before the Update Goal command is marked as entered in error. |
| UPDATE_GOAL_COMMAND__PRE_EXECUTE_ACTION | Occurs before an action is executed on the Update Goal command. |
| UPDATE_GOAL_COMMAND__PRE_ORIGINATE | Occurs before the Update Goal command is first entered into a note. |
| UPDATE_GOAL_COMMAND__PRE_UPDATE | Occurs before data for the Update Goal command is updated. |
| UPDATE_GOAL__GOAL_STATEMENT__POST_SEARCH | Occurs after the initial results are fetched for the goal search in the Update Goal command. |
| UPDATE_GOAL__GOAL_STATEMENT__PRE_SEARCH |  |

#### Vitals Command

| Event | Description |
| ----- | ----------- |
| VITALS_COMMAND__POST_COMMIT |  |
| VITALS_COMMAND__POST_DELETE |  |
| VITALS_COMMAND__POST_ENTER_IN_ERROR |  |
| VITALS_COMMAND__POST_EXECUTE_ACTION |  |
| VITALS_COMMAND__POST_ORIGINATE |  |
| VITALS_COMMAND__POST_UPDATE |  |
| VITALS_COMMAND__PRE_COMMIT |  |
| VITALS_COMMAND__PRE_DELETE |  |
| VITALS_COMMAND__PRE_ENTER_IN_ERROR |  |
| VITALS_COMMAND__PRE_EXECUTE_ACTION |  |
| VITALS_COMMAND__PRE_ORIGINATE |  |
| VITALS_COMMAND__PRE_UPDATE |  |


### Other Events


| Event | Description |
| ----- | ----------- |
| UNKNOWN | Default event type unlikely to ever be emitted. |
| CRON | This event fires regularly and can be used for scheduled tasks. See [CronTask](/sdk/handlers-crontask/). |
| CLAIM__CONDITIONS | Occurs when the conditions are loaded within the claim summary. |
| PATIENT_CHART__CONDITIONS | Occurs when the conditions are loaded within the patient summary |
| PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION | Occurs when a patient chart's summary section is loading. |
