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

The event `target` object can be accessed within the compute method of the plugin by `self.event.target`. If `self.event.target.type` exists, it provides the same type that would be imported from the Data module. For example, a type of `Condition` would be the same as what you can import from `canvas_sdk.v1.data.condition`. <br><br>
The event `context` object can be accessed via `self.event.context`.

### Record lifecycle events

These events fire as a result of records being created, updated, or deleted.

#### Patients

<table>
  <thead>
    <td colspan="2"><b>PATIENT_CREATED </b><span> - occurs when a patient is created.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": pt_id
"type": <a href='/sdk/data-patient/'>Patient</a></pre></td>
    <td><pre>empty</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_UPDATED </b><span> - occurs when a patient's data is updated.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": pt_id
"type": <a href='/sdk/data-patient/'>Patient</a></pre></td>
    <td><pre>empty</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>CARE_TEAM_MEMBERSHIP_CREATED </b><span> - occurs when a new care team member is added for a patient.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": care_team_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>CARE_TEAM_MEMBERSHIP_UPDATED </b><span> - occurs when a care team member is adjusted for a patient.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": care_team_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>CARE_TEAM_MEMBERSHIP_DELETED </b><span> - occurs when a care team member is removed for a patient.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": care_team_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_ADDRESS_CREATED </b><span> - occurs when an address is added for a patient.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": address_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_ADDRESS_UPDATED </b><span> - occurs when one of a patient's addresses is updated.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": address_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_ADDRESS_DELETED </b><span> - occurs when one of a patient's addresses is removed.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": address_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_CONTACT_PERSON_CREATED </b><span> - occurs when a contact is added for a patient.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": contact_person_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_CONTACT_PERSON_UPDATED </b><span> - occurs when one of a patient's contacts is updated.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": contact_person_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_CONTACT_PERSON_DELETED </b><span> - occurs when one of a patient's contacts is removed.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": contact_person_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_CONTACT_POINT_CREATED </b><span> - occurs when a contact method for a patient is added.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": contact_point_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_CONTACT_POINT_UPDATED </b><span> - occurs when a contact method for a patient is updated.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": contact_point_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>PATIENT_CONTACT_POINT_DELETED </b><span> - occurs when a contact method for a patient is removed.</span></td>
  </thead>
  <tbody>
  <tr>
    <td>Target object</td>
    <td>Context object</td>
  </tr>
  <tr>
    <td><pre>"id": contact_point_id
"type": None</pre></td>
    <td><pre>"patient":
    "id": pt_id</pre></td>
  </tr>
  </tbody>
</table>

#### Allergy Intolerances

<table>
  <thead>
    <td colspan="2"><b>ALLERGY_INTOLERANCE_CREATED </b><span> - occurs when an allergy is created for a patient. Additional details for the allergy may become available with subsequent ALLERGY_INTOLERANCE_UPDATED events.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": allergy_id
"type": None</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>ALLERGY_INTOLERANCE_UPDATED </b><span> - occurs when an allergy is updated for a patient.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": allergy_id
"type": None</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Appointments

<table>
  <thead>
    <td colspan="2"><b>APPOINTMENT_CREATED </b><span> - occurs when an appointment is first created/booked.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
       <td><pre>"id": appointment_id
"type": None</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>
     
<table>
  <thead>
    <td colspan="2"><b>APPOINTMENT_UPDATED </b><span> - occurs when details of an appointment are updated.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
       <td><pre>"id": appointment_id
"type": None</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>APPOINTMENT_CHECKED_IN </b><span> - occurs when a patient has arrived and been checked in for their appointment.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
       <td><pre>"id": appointment_id
"type": None</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>APPOINTMENT_RESTORED </b><span> - occurs when a cancelled appointment is restored to a non-cancelled status.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
       <td><pre>"id": appointment_id
"type": None</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>APPOINTMENT_CANCELED </b><span> - occurs when an appointment is cancelled.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
       <td><pre>"id": appointment_id
"type": None</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>APPOINTMENT_NO_SHOWED </b><span> - occurs when an appointment is marked as a no-show.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
       <td><pre>"id": appointment_id
"type": None</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Billing Line Items

<table>
  <thead>
    <td colspan="2"><b>BILLING_LINE_ITEM_CREATED </b><span> - occurs when a billing line item is created from adding a CPT code to a note.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": billing_line_item_id
"type": BillingLineItem</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>BILLING_LINE_ITEM_UPDATED </b><span> - occurs when a billing line item is modified.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": billing_line_item_id
"type": BillingLineItem</pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Conditions

<table>
  <thead>
    <td colspan="2"><b>CONDITION_ASSESSED </b><span> - occurs when a condition is assessed through the Assess Condition command.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": condition_id
"type": <a href='/sdk/data-condition/'>Condition</a></pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>CONDITION_CREATED </b><span> - occurs when a condition is diagnosed for a patient. Additional details for the condition may become available with subsequent CONDITION_UPDATED events.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": condition_id
"type": <a href='/sdk/data-condition/'>Condition</a></pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>CONDITION_RESOLVED </b><span> - occurs when a condition is resolved through the Resolve Condition command.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": condition_id
"type": <a href='/sdk/data-condition/'>Condition</a></pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>CONDITION_UPDATED </b><span> - occurs when a condition is updated for a patient.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": condition_id
"type": <a href='/sdk/data-condition/'>Condition</a></pre></td>
      <td><pre>"patient":
    "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Consents

<table>
  <thead>
    <td colspan="2"><b>CONSENT_CREATED </b><span> - occurs when a patient consent is created.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": consent_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>CONSENT_DELETED </b><span> - occurs when a patient consent is removed/deleted.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": consent_id
type: None</pre></td>
      <td><pre>"patient":
   id: pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>CONSENT_UPDATED </b><span> - occurs when a patient consent is updated.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": consent_id
type: None</pre></td>
      <td><pre>"patient":
   id: pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Coverages

<table>
  <thead>
    <td colspan="2"><b>COVERAGE_CREATED </b><span> - occurs when a coverage for a patient is created.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": coverage_id
type: None</pre></td>
      <td><pre>"patient":
   id: pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>COVERAGE_UPDATED </b><span> - occurs when a coverage for a patient is updated.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": coverage_id
type: None</pre></td>
      <td><pre>"patient":
   id: pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Detected Issues

<table>
  <colgroup>
    <col width="40%"/>
    <col width="60%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Description</th>
  </thead>
  <tbody>
    <tr>
      <td>DETECTED_ISSUE_CREATED</td>
      <td>Occurs when a detected issue is created.</td>
    </tr>
    <tr>
      <td>DETECTED_ISSUE_UPDATED</td>
      <td>Occurs when a detected issue is updated.</td>
    </tr>
    <tr>
      <td>DETECTED_ISSUE_EVIDENCE_CREATED</td>
      <td>Occurs when detected issue evidence is created.</td>
    </tr>
    <tr>
      <td>DETECTED_ISSUE_EVIDENCE_UPDATED</td>
      <td>Occurs when a detected issue evidence is updated.</td>
    </tr>
  </tbody>
</table>

#### Devices

<table>
  <thead>
    <td colspan="2"><b>DEVICE_CREATED </b><span> - occurs when a device is created.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": device_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>DEVICE_UPDATED </b><span> - occurs when a device is updated.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": device_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Encounters

<table>
  <thead>
    <td colspan="2"><b>ENCOUNTER_CREATED </b><span> - occurs when an encounter is created.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": encounter_id
"type": None</pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>ENCOUNTER_UPDATED </b><span> - occurs when an encounter is updated.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": encounter_id
"type": None</pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

#### Imaging Reports

<table>
  <thead>
    <td colspan="2"><b>IMAGING_REPORT_CREATED </b><span> - occurs when an imaging report is entered into the data integration section of canvas.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": report_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>IMAGING_REPORT_UPDATED </b><span> - occurs when an imaging report is updated.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": report_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Immunizations

<table>
  <thead>
    <td colspan="2"><b>IMMUNIZATION_CREATED </b><span> - occurs when an immunization is created. additional details for the immunization may become available with subsequent immunization_updated events.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": immunization_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>IMMUNIZATION_UPDATED </b><span> - occurs when an immunization is updated.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": immunization_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <td colspan="2"><b>IMMUNIZATION_STATEMENT_CREATED </b><span> - occurs when an immunization statement is created. additional details for the immunization statement may become available with subsequent immunization_statement_updated events.</span></td>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": immunization_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th  colspan="2">IMMUNIZATION_STATEMENT_UPDATED</th></tr>
    <td>occurs when an immunization statement is updated.</td>
    <tr>
      <th>Target object</th>
      <th>Context object</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><pre>"id": immunization_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Instructions

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>INSTRUCTION_CREATED</td>
      <td>An instruction is created using the Instruct command. Additional details for the instruction may become available with subsequent INSTRUCTION_UPDATED events.</td>
      <td><pre>"id": instruction_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCTION_UPDATED</td>
      <td>An instruction is updated.</td>
      <td><pre>"id": instruction_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Interviews

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>INTERVIEW_CREATED</td>
      <td>An interview is created using the Questionnaire command or through the Questionnaire endpoint in the FHIR API. Additional details for the interview may become available with subsequent INTERVIEW_UPDATED events.</td>
      <td><pre>"id": interview_id
"type": [Interview](/sdk/data-questionnaire/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INTERVIEW_UPDATED</td>
      <td>An interview is updated.</td>
      <td><pre>"id": interview_id
"type": [Interview](/sdk/data-questionnaire/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Labs

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>LAB_ORDER_CREATED</td>
      <td>A lab order is created via the Lab Order command. Additional details for the lab order may become available with subsequent LAB_ORDER_UPDATED events.</td>
      <td><pre>"id": laborder_id
"type": [LabOrder](/sdk/data-labs/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_UPDATED</td>
      <td>A lab order is updated.</td>
      <td><pre>"id": laborder_id
"type": [LabOrder](/sdk/data-labs/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_REPORT_CREATED</td>
      <td>A lab report is created either through Data Integration, electronic ingestion or the FHIR API.</td>
      <td><pre>"id": labreport_id
"type": [LabReport](/sdk/data-labs/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_REPORT_UPDATED</td>
      <td>A lab report is updated.</td>
      <td><pre>"id": labreport_id
"type": [LabReport](/sdk/data-labs/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Medications

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>MEDICATION_LIST_ITEM_CREATED</td>
      <td>A medication is added for a patient.</td>
      <td><pre>"id": medication_id
"type": [Medication](/sdk/data-medication/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_LIST_ITEM_UPDATED</td>
      <td>A medication is updated for a patient.</td>
      <td><pre>"id": medication_id
"type": [Medication](/sdk/data-medication/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIPTION_CREATED</td>
      <td>A prescription is created.</td>
      <td><pre>"id": prescription_id
"type": [Medication](/sdk/data-medication/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIPTION_UPDATED</td>
      <td>A prescription is created for a patient using the Prescribe command. Additional details for the prescription become available with subsequent PRESCRIPTION_UPDATED events.</td>
      <td><pre>"id": prescription_id
"type": [Medication](/sdk/data-medication/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Messaging

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>MESSAGE_CREATED</td>
      <td>A message (patient/practitioner communication) is created.</td>
      <td><pre>"id": message_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<!-- #### Notes

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>NOTE_STATE_CHANGE_EVENT_CREATED</td>
      <td></td>
    </tr>
    <tr>
      <td>NOTE_STATE_CHANGE_EVENT_UPDATED</td>
      <td></td>
    </tr>
  </tbody>
</table> -->

#### Observations

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>OBSERVATION_CREATED</td>
      <td>An observation is created.</td>
      <td><pre>"id": observation_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>OBSERVATION_UPDATED</td>
      <td>An observation is updated.</td>
      <td><pre>"id": observation_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Protocol Overrides

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>PROTOCOL_OVERRIDE_CREATED</td>
      <td></td>
      <td><pre>"id": protocoloverride_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PROTOCOL_OVERRIDE_UPDATED</td>
      <td></td>
      <td><pre>"id": protocoloverride_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PROTOCOL_OVERRIDE_DELETED</td>
      <td></td>
      <td><pre>"id": protocoloverride_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Referral Reports

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>REFERRAL_REPORT_CREATED</td>
      <td>A specialist consult report is created in Data Integration.</td>
      <td><pre>"id": referralreport_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFERRAL_REPORT_UPDATED</td>
      <td>A specialist consult report is updated.</td>
      <td><pre>"id": referralreport_id
"type": None</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Tasks

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>TASK_CREATED</td>
      <td>A task is created.</td>
      <td><pre>"id": task_id
"type": [Task](/sdk/data-task/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_UPDATED</td>
      <td>A task is updated.</td>
      <td><pre>"id": task_id
"type": [Task](/sdk/data-task/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMENT_CREATED</td>
      <td>A comment is added to a task.</td>
      <td><pre>"id": taskcomment_id
"type": [Task](/sdk/data-task/)Comment</pre></td>
      <td><pre>empty</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMENT_UPDATED</td>
      <td></td>
      <td><pre>"id": taskcomment_id
"type": [Task](/sdk/data-task/)Comment</pre></td>
      <td><pre>empty</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMENT_DELETED</td>
      <td></td>
      <td><pre>"id": taskcomment_id
"type": [Task](/sdk/data-task/)Comment</pre></td>
      <td><pre>empty</pre></td>
    </tr>
    <tr>
      <td>TASK_LABELS_ADJUSTED</td>
      <td>A task's labels are changed.</td>
      <td><pre>"id": user_seelcted_tasklabel_id
"type": None</pre></td>
      <td><pre>empty</pre></td>
    </tr>
    <tr>
      <td>TASK_COMPLETED</td>
      <td>A task is set to completed.</td>
      <td><pre>"id": task_id
"type": [Task](/sdk/data-task/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_CLOSED</td>
      <td>A task is set to closed.</td>
      <td><pre>"id": task_id
"type": [Task](/sdk/data-task/)</pre></td>
      <td><pre>"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Vital Signs

<table>
  <colgroup>
    <col width="10%"/>
    <col width="30%"/>
    <col width="35%"/>
    <col width="25%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>VITAL_SIGN_CREATED</td>
      <td>A vitals entry is created for a patient using the Vitals command. Additional details for the vitals become available with subsequent VITAL_SIGN_UPDATED events.</td>
      <td><pre>"id": vitalsign_id
"type": None</pre></td>
      <td><pre>empty</pre></td>
    </tr>
    <tr>
      <td>VITAL_SIGN_UPDATED</td>
      <td>A vitals entry is updated for a patient.</td>
      <td><pre>"id": vitalsign_id
"type": None</pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

### Command lifecycle events

These events fire during the command lifecycle.

#### Generic events

<table>
  <colgroup>
    <col width="40%"/>
    <col width="60%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
  </thead>
  <tbody>
    <tr>
      <td>PRE_COMMAND_ORIGINATE</td>
      <td>Before any command is entered into a note.</td>
    </tr>
    <tr>
      <td>POST_COMMAND_ORIGINATE</td>
      <td>After any command is entered into a note.</td>
    </tr>
    <tr>
      <td>PRE_COMMAND_UPDATE</td>
      <td>Before the data in any command is updated.</td>
    </tr>
    <tr>
      <td>POST_COMMAND_UPDATE</td>
      <td>After the data in any command is updated.</td>
    </tr>
    <tr>
      <td>PRE_COMMAND_COMMIT</td>
      <td>Before any command is committed.</td>
    </tr>
    <tr>
      <td>POST_COMMAND_COMMIT</td>
      <td>After any command is committed.</td>
    </tr>
    <tr>
      <td>PRE_COMMAND_DELETE</td>
      <td>Before any command is deleted.</td>
    </tr>
    <tr>
      <td>POST_COMMAND_DELETE</td>
      <td>After any command is deleted.</td>
    </tr>
    <tr>
      <td>PRE_COMMAND_ENTER_IN_ERROR</td>
      <td>Before any command is marked as entered in error.</td>
    </tr>
    <tr>
      <td>POST_COMMAND_ENTER_IN_ERROR</td>
      <td>After any command is marked as entered in error.</td>
    </tr>
    <tr>
      <td>PRE_COMMAND_EXECUTE_ACTION</td>
      <td>Before an action is executed on any command.</td>
    </tr>
    <tr>
      <td>POST_COMMAND_EXECUTE_ACTION</td>
      <td>After an action is executed on any command.</td>
    </tr>
    <tr>
      <td>POST_COMMAND_INSERTED_INTO_NOTE</td>
      <td>After a command is added to a note in the UI.</td>
    </tr>
  </tbody>
</table>

##### Context Overview

Each command lifecycle event provides specific context to the handler, depending on the stage of the command lifecycle.

**Base Context (All Events Except `PRE_COMMAND_ORIGINATE`)**:

```json
{
  "note": { "uuid": "note-123" },
  "patient": { "id": "patient-123" },
  "fields": { "key": "value" }
}
```

- `note.uuid`: The unique identifier of the note associated with the command.
- `patient.id`: The unique identifier of the patient associated with the note.
- `fields`: A dictionary containing command-specific details. See examples for each command.

**`PRE_COMMAND_ORIGINATE` Context**:
Since the command is not yet connected to a note, the `PRE_COMMAND_ORIGINATE` event context only includes:

```json
{
  "fields": { "key": "value" }
}
```

- `fields`: Contains details specific to the command being originated.

---

#### Allergy Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>ALLERGY_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "severity": str
  "narrative": str
  "approximate_date":
    "input": str
    "date": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ALLERGY__ALLERGY__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>ALLERGY__ALLERGY__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Assess Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>ASSESS_COMMAND__CONDITION_SELECTED</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "condition": dict
  "background": str
  "status": str
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ASSESS__CONDITION__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>ASSESS__CONDITION__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Clipboard Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>CLIPBOARD_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLIPBOARD_COMMAND__POST_INSERTED_INTO_NOTE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

##### Clipboard Fields Context

The Clipboard Command provides the following fields in its context:

| Field  | Type     | Description                                   |
| ------ | -------- | --------------------------------------------- |
| `text` | _string_ | The raw text content copied to the clipboard. |

Refer to the [base context documentation](#context-overview) for additional details about the full context structure.

```json
{
  "note": { "uuid": "note-123" },
  "patient": { "id": "patient-123" },
  "fields": {
    "text": "Patient complains of persistent headaches for the past two weeks."
  }
}
```

---

#### Close Goal Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>CLOSE_GOAL_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL__GOAL_ID__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>CLOSE_GOAL__GOAL_ID__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Diagnose Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>DIAGNOSE_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "diagnose": dict
  "background": str
  "approximate_date_of_onset":
    "input": str
    "date": str
  "today_assessment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE__DIAGNOSE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>DIAGNOSE__DIAGNOSE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Educational Material Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL__LANGUAGE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL__LANGUAGE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL__TITLE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>EDUCATIONAL_MATERIAL__TITLE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Family History Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY__FAMILY_HISTORY__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY__FAMILY_HISTORY__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY__RELATIVE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>FAMILY_HISTORY__RELATIVE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Goal Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>GOAL_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>GOAL_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": str
  "start_date": str
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### History of Present Illness Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Imaging Order Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>IMAGING_ORDER_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "image": dict
  "indications": list[dict]
  "priority": str
  "additional_details": str
  "imaging_center": dict
  "comment": str
  "ordering_provider": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER__IMAGE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER__IMAGE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER__IMAGING_CENTER__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER__IMAGING_CENTER__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER__INDICATIONS__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER__INDICATIONS__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER__ORDERING_PROVIDER__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMAGING_ORDER__ORDERING_PROVIDER__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Immunization Statement Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "statement": dict
  "date":
    "date": str
    "input": str
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT__STATEMENT__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZATION_STATEMENT__STATEMENT__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Immunize Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>IMMUNIZE_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "lot_number": dict
  "manufacturer": str
  "exp_date_original": str
  "sig_original": str
  "consent_given": bool
  "given_by": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE__CODING__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE__CODING__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE__GIVEN_BY__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE__GIVEN_BY__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE__LOT_NUMBER__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>IMMUNIZE__LOT_NUMBER__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Instruct Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>INSTRUCT_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT__INSTRUCT__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>INSTRUCT__INSTRUCT__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Lab Order Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>LAB_ORDER_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "lab_partner": dict
  "tests": list[dict]
  "ordering_provider": dict
  "diagnosis": list[dict]
  "fasting_status": bool
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER__DIAGNOSIS__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER__DIAGNOSIS__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER__LAB_PARTNER__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER__LAB_PARTNER__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER__ORDERING_PROVIDER__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER__ORDERING_PROVIDER__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER__TESTS__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>LAB_ORDER__TESTS__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Medical History Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_medical_history": dict
  "approximate_start_date":
    "date": str
    "input": str
  "approximate_end_date":
    "date": str
    "input": str
  "show_on_condition_list": bool
  "comments": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY__APPROXIMATE_END_DATE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY__APPROXIMATE_END_DATE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY__APPROXIMATE_START_DATE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY__APPROXIMATE_START_DATE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Medication Statement Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT__MEDICATION__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT__MEDICATION__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>MEDICATION_STATEMENT__MEDICATION__SELECTED</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "sig": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Perfom Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>PERFORM_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PERFORM__PERFORM__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>PERFORM__PERFORM__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Physical Exam Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM__QUESTIONNAIRE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>PHYSICAL_EXAM__QUESTIONNAIRE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Plan Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>PLAN_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PLAN_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Prescribe Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>PRESCRIBE_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE__INDICATIONS__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE__INDICATIONS__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE__PHARMACY__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE__PHARMACY__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE__PRESCRIBE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>PRESCRIBE__PRESCRIBE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Questionnaire Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE__QUESTIONNAIRE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>QUESTIONNAIRE__QUESTIONNAIRE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Reason for Visit Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT__CODING__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>REASON_FOR_VISIT__CODING__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Refill Prescription Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>REFILL_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "indications": list[dict]
  "sig": str
  "days_supply": int
  "quantity_to_dispense": int
  "type_to_dispense": dict
  "refills": int
  "substitutions": str
  "pharmacy": dict
  "prescriber": dict
  "note_to_pharmacist": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REFILL__INDICATIONS__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>REFILL__INDICATIONS__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>REFILL__PHARMACY__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>REFILL__PHARMACY__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>REFILL__PRESCRIBE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>REFILL__PRESCRIBE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Remove Allergy Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY__ALLERGY__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>REMOVE_ALLERGY__ALLERGY__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Review of Systems Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>ROS_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>ROS__QUESTIONNAIRE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>ROS__QUESTIONNAIRE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Stop Medication Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>STOP_MEDICATION_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION__MEDICATION__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>STOP_MEDICATION__MEDICATION__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Structured Assessment Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT__QUESTIONNAIRE__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>STRUCTURED_ASSESSMENT__QUESTIONNAIRE__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Surgical History Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "past_surgical_history": dict
  "approximate_date":
    "input": str
    "date": str
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY__PAST_SURGICAL_HISTORY__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>SURGICAL_HISTORY__PAST_SURGICAL_HISTORY__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Task Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>TASK_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "title": str
  "assign_to": dict
  "due_date": str
  "comment": str
  "labels": list[dict]
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>TASK__ASSIGN_TO__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>TASK__ASSIGN_TO__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>TASK__LABELS__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>TASK__LABELS__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Update Goal Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>UPDATE_GOAL_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "goal_statement": dict
  "due_date": str
  "achievement_status": str
  "priority": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL__GOAL_STATEMENT__POST_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
    <tr>
      <td>UPDATE_GOAL__GOAL_STATEMENT__PRE_SEARCH</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>
</table>

#### Vitals Command

<table>
  <colgroup>
    <col width="10%"/>
    <col width="35%"/>
    <col width="55%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Target object</th>
    <th>Context object</th>
  </thead>
  <tbody>
    <tr>
      <td>VITALS_COMMAND__POST_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__POST_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__POST_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__POST_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__POST_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__POST_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__PRE_COMMIT</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__PRE_DELETE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__PRE_EXECUTE_ACTION</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__PRE_ORIGINATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
    <tr>
      <td>VITALS_COMMAND__PRE_UPDATE</td>
      <td><pre>"id": command_uuid
"type": [Command](/sdk/data-command/)</pre></td>
      <td><pre>"fields":
  "height": str
  "weight_lbs": str
  "weight_oz": str
  "waist_circumference": str
  "body_temperature": str
  "body_temperature_site": str
  "blood_pressure_systole": int
  "blood_pressure_diastole": str
  "blood_pressure_position_and_site": str
  "pulse": str
  "pulse_rhythm": str
  "respiration_rate": int
  "oxygen saturation": str
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

### Action Buttons Events

For more information on handling these events, see <a href="/sdk/handlers-action-buttons" target="_blank">Action Buttons</a>.

<table>
  <colgroup>
    <col width="40%"/>
    <col width="60%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Description</th>
  </thead>
  <tbody>
    <tr>
      <td>SHOW_NOTE_HEADER_BUTTON</td>
      <td>Occurs when patient notes are being loaded.</td>
    </tr>
    <tr>
      <td>SHOW_NOTE_FOOTER_BUTTON</td>
      <td>Occurs when patient notes are being loaded.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_SOCIAL_DETERMINANTS_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for social determinants section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_GOALS_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for goals section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_CONDITIONS_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for conditions section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_MEDICATIONS_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for medications section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_ALLERGIES_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for allergies section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_CARE_TEAMS_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for care teams section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_VITALS_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for vitals section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_IMMUNIZATIONS_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for immunizations section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_SURGICAL_HISTORY_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for surgical history section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_FAMILY_HISTORY_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for family history section.</td>
    </tr>
    <tr>
      <td>SHOW_CHART_SUMMARY_CODING_GAPS_SECTION_BUTTON</td>
      <td>Occurs when patient chart summary is being loaded, specifically for coding gaps section.</td>
    </tr>
  </tbody>
</table>

### Other Events

<table>
  <colgroup>
    <col width="30%"/>
    <col width="70%"/>
  </colgroup>
  <thead>
    <th>Event</th>
    <th>Occurs when</th>
  </thead>
  <tbody>
    <tr>
      <td>UNKNOWN</td>
      <td>Default event type unlikely to ever be emitted.</td>
    </tr>
    <tr>
      <td>CRON</td>
      <td>This event fires regularly and can be used for scheduled tasks. See [CronTask](/sdk/handlers-crontask/).</td>
    </tr>
    <tr>
      <td>CLAIM__CONDITIONS</td>
      <td>The conditions are loaded within the claim summary.</td>
    </tr>
    <tr>
      <td>PATIENT_CHART__CONDITIONS</td>
      <td>The conditions are loaded within the patient summary</td>
    </tr>
    <tr>
      <td>PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION</td>
      <td>A patient chart's summary section is loading.</td>
    </tr>
    <tr>
      <td>PLUGIN_CREATED</td>
      <td>A plugin is uploaded for the first time. See <a href="{% link _sdk/effects/protocol_cards.md %}" target="_blank">ProtocolCards</a> and <a href="{% link _sdk/effects/banner_alerts.md %}" target="_blank">BannerAlerts</a> for examples of how to use this event.</td>
    </tr>
    <tr>
      <td>PLUGIN_UPDATED</td>
      <td>A plugin is enabled or when the plugin code has changed. See <a href="{% link _sdk/effects/protocol_cards.md %}" target="_blank">ProtocolCards</a> and <a href="{% link _sdk/effects/banner_alerts.md %}" target="_blank">BannerAlerts</a> for examples of how to use this event.</td>
    </tr>
    <tr>
      <td>PATIENT_PROFILE__ADD_PHARMACY__POST_SEARCH_RESULTS</td>
      <td>Adding a pharmacy for a patient in their profile.</td>
    </tr>
  </tbody>
</table>
