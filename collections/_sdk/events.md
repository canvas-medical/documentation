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

The event `target` object can be accessed within the compute method of the plugin by `self.event.target`. If `self.event.target.type` exists, it provides the same type that would be imported from the Data module. For example, a type of `Condition` would be the same as what you can import from `canvas_sdk.v1.data.condition`.

The event `context` object can be accessed via `self.event.context`. The
content present in each event's context depends on the event type. The table
below shows what you can expect for event type, or you could take a look
yourself by logging it out.

```python
from canvas_sdk.events import EventType
from logger import log

class Protocol(BaseProtocol):
    RESPONDS_TO = [EventType.Name(EventType.ALLERGY_INTOLERANCE_CREATED)]

    def compute(self):
        log.info(self.event.context)
        return []
```

### Record lifecycle events

These events fire as a result of records being created, updated, or deleted.

#### Patients

<table>
  <thead>
    <tr><th colspan="2">PATIENT_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a patient is created.</td></tr>
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
    <tr><th colspan="2">PATIENT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a patient's data is updated.</td></tr>
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
    <tr><th colspan="2">CARE_TEAM_MEMBERSHIP_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a new care team member is added for a patient.</td></tr>
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
    <tr><th colspan="2">CARE_TEAM_MEMBERSHIP_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a care team member is adjusted for a patient.</td></tr>
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
    <tr><th colspan="2">CARE_TEAM_MEMBERSHIP_DELETED</th></tr>
    <tr><td colspan="2">Occurs when a care team member is removed for a patient.</td></tr>
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
    <tr><th colspan="2">PATIENT_ADDRESS_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an address is added for a patient.</td></tr>
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
    <tr><th colspan="2">PATIENT_ADDRESS_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when one of a patient's addresses is updated.</td></tr>
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
    <tr><th colspan="2">PATIENT_ADDRESS_DELETED</th></tr>
    <tr><td colspan="2">Occurs when one of a patient's addresses is removed.</td></tr>
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
    <tr><th colspan="2">PATIENT_CONTACT_PERSON_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a contact is added for a patient.</td></tr>
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
    <tr><th colspan="2">PATIENT_CONTACT_PERSON_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when one of a patient's contacts is updated.</td></tr>
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
    <tr><th colspan="2">PATIENT_CONTACT_PERSON_DELETED</th></tr>
    <tr><td colspan="2">Occurs when one of a patient's contacts is removed.</td></tr>
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
    <tr><th colspan="2">PATIENT_CONTACT_POINT_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a contact method for a patient is added.</td></tr>
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
    <tr><th colspan="2">PATIENT_CONTACT_POINT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a contact method for a patient is updated.</td></tr>
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
    <tr><th colspan="2">PATIENT_CONTACT_POINT_DELETED</th></tr>
    <tr><td colspan="2">Occurs when a contact method for a patient is removed.</td></tr>
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
    <tr><th colspan="2">ALLERGY_INTOLERANCE_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an allergy is created for a patient. Additional details for the allergy may become available with subsequent ALLERGY_INTOLERANCE_UPDATED events.</td></tr>
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
    <tr><th colspan="2">ALLERGY_INTOLERANCE_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when an allergy is updated for a patient.</td></tr>
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
    <tr><th colspan="2">APPOINTMENT_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an appointment is first created/booked.</td></tr>
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
    <tr><th colspan="2">APPOINTMENT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when details of an appointment are updated.</td></tr>
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
    <tr><th colspan="2">APPOINTMENT_CHECKED_IN</th></tr>
    <tr><td colspan="2">Occurs when a patient has arrived and been checked in for their appointment.</td></tr>
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
    <tr><th colspan="2">APPOINTMENT_RESTORED</th></tr>
    <tr><td colspan="2">Occurs when a cancelled appointment is restored to a non-cancelled status.</td></tr>
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
    <tr><th colspan="2">APPOINTMENT_CANCELED</th></tr>
    <tr><td colspan="2">Occurs when an appointment is cancelled.</td></tr>
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
    <tr><th colspan="2">APPOINTMENT_NO_SHOWED</th></tr>
    <tr><td colspan="2">Occurs when an appointment is marked as a no-show.</td></tr>
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
    <tr><th colspan="2">BILLING_LINE_ITEM_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a billing line item is created from adding a CPT code to a note.</td></tr>
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
    <tr><th colspan="2">BILLING_LINE_ITEM_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a billing line item is modified.</td></tr>
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
    <tr><th colspan="2">CONDITION_ASSESSED</th></tr>
    <tr><td colspan="2">Occurs when a condition is assessed through the Assess Condition command.</td></tr>
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
    <tr><th colspan="2">CONDITION_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a condition is diagnosed for a patient. Additional details for the condition may become available with subsequent CONDITION_UPDATED events.</td></tr>
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
    <tr><th colspan="2">CONDITION_RESOLVED</th></tr>
    <tr><td colspan="2">Occurs when a condition is resolved through the Resolve Condition command.</td></tr>
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
    <tr><th colspan="2">CONDITION_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a condition is updated for a patient.</td></tr>
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
    <tr><th colspan="2">CONSENT_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a patient consent is created.</td></tr>
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
    <tr><th colspan="2">CONSENT_DELETED</th></tr>
    <tr><td colspan="2">Occurs when a patient consent is removed/deleted.</td></tr>
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
    <tr><th colspan="2">CONSENT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a patient consent is updated.</td></tr>
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
    <tr><th colspan="2">COVERAGE_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a coverage for a patient is created.</td></tr>
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
    <tr><th colspan="2">COVERAGE_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a coverage for a patient is updated.</td></tr>
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
  <thead>
    <tr><th colspan="2">DETECTED_ISSUE_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a detected issue is created.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": detected_issue_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">DETECTED_ISSUE_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a detected issue is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": detected_issue_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">DETECTED_ISSUE_EVIDENCE_CREATED</th></tr>
    <tr><td colspan="2">Occurs when detected issue evidence is created.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": detected_issue_evidence_id
"type": None</pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">DETECTED_ISSUE_EVIDENCE_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a detected issue evidence is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": detected_issue_evidence_id
"type": None</pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

#### Devices

<table>
  <thead>
    <tr><th colspan="2">DEVICE_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a device is created.</td></tr>
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
    <tr><th colspan="2">DEVICE_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a device is updated.</td></tr>
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
    <tr><th colspan="2">ENCOUNTER_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an encounter is created.</td></tr>
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
    <tr><th colspan="2">ENCOUNTER_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when an encounter is updated.</td></tr>
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
    <tr><th colspan="2">IMAGING_REPORT_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an imaging report is entered into the data integration section of canvas.</td></tr>
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
    <tr><th colspan="2">IMAGING_REPORT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when an imaging report is updated.</td></tr>
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
    <tr><th colspan="2">IMMUNIZATION_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an immunization is created. Additional details for the immunization may become available with subsequent IMMUNIZATION_STATEMENT_UPDATED events.</td></tr>
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
    <tr><th colspan="2">IMMUNIZATION_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when an immunization is updated.</td></tr>
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
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an immunization statement is created. Additional details for the immunization statement may become available with subsequent IMMUNIZATION_STATEMENT_UPDATED events.</td></tr>
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
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when an immunization statement is updated.</td></tr>
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

#### Instructions

<table>
  <thead>
    <tr><th colspan="2">INSTRUCTION_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an instruction is created using the Instruct command. Additional details for the instruction may become available with subsequent INSTRUCTION_UPDATED events.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": instruction_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCTION_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when an instruction is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": instruction_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Interviews

<table>
  <thead>
    <tr><th colspan="2">INTERVIEW_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an interview is created using the Questionnaire command or through the Questionnaire endpoint in the FHIR API. Additional details for the interview may become available with subsequent INTERVIEW_UPDATED events.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": interview_id
"type": <a href='/sdk/data-questionnaire/'>Interview</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">INTERVIEW_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when an interview is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": interview_id
"type": <a href='/sdk/data-questionnaire/'>Interview</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Labs

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a lab order is created via the Lab Order command. Additional details for the lab order may become available with subsequent LAB_ORDER_UPDATED events.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": laborder_id
"type": <a href='/sdk/data-labs/'>LabOrder</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a lab order is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": laborder_id
"type": <a href='/sdk/data-labs/'>LabOrder</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_REPORT_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a lab report is created either through Data Integration, electronic ingestion or the FHIR API.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": labreport_id
"type": <a href='/sdk/data-labs/'>LabReport</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_REPORT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a lab report is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": labreport_id
"type": <a href='/sdk/data-labs/'>LabReport</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Medications

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_LIST_ITEM_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a medication is added for a patient.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": medication_id
"type": <a href='/sdk/data-medication/'>Medication</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_LIST_ITEM_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a medication is updated for a patient.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": medication_id
"type": <a href='/sdk/data-medication/'>Medication</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIPTION_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a prescription is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": prescription_id
"type": <a href='/sdk/data-medication/'>Medication</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIPTION_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a prescription is created for a patient using the Prescribe command. Additional details for the prescription become available with subsequent PRESCRIPTION_UPDATED events.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": prescription_id
"type": <a href='/sdk/data-medication/'>Medication</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Messaging

<table>
  <thead>
    <tr><th colspan="2">MESSAGE_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a message (patient/practitioner communication) is created.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": message_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Notes

<table>
  <thead>
    <tr><th colspan="2">NOTE_STATE_CHANGE_EVENT_CREATED</th></tr>
    <tr><td colspan="2">Occurs as a note traverses through its state machine.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": nsce_id
"type": NoteStateChangeEvent</pre></td>
      <td><pre>"note_id": note_id,
"patient_id": pt_id,
"state": str</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">NOTE_STATE_CHANGE_EVENT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs if a note state change event is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": nsce_id
"type": NoteStateChangeEvent</pre></td>
      <td><pre>"note_id": note_id,
"patient_id": pt_id,
"state": str</pre></td>
    </tr>
  </tbody>
</table>

#### Observations

<table>
  <thead>
    <tr><th colspan="2">OBSERVATION_CREATED</th></tr>
    <tr><td colspan="2">Occurs when an observation is created.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": observation_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">OBSERVATION_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when an observation is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": observation_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Protocol Overrides

<table>
  <thead>
    <tr><th colspan="2">PROTOCOL_OVERRIDE_CREATED</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": protocoloverride_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">PROTOCOL_OVERRIDE_UPDATED</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": protocoloverride_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">PROTOCOL_OVERRIDE_DELETED</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": protocoloverride_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Referral Reports

<table>
  <thead>
    <tr><th colspan="2">REFERRAL_REPORT_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a specialist consult report is created in Data Integration.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": referralreport_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">REFERRAL_REPORT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a specialist consult report is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": referralreport_id
"type": None</pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Tasks

<table>
  <thead>
    <tr><th colspan="2">TASK_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a task is created.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": task_id
"type": <a href='/sdk/data-task/'>Task</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a task is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": task_id
"type": <a href='/sdk/data-task/'>Task</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMENT_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a comment is added to a task.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": taskcomment_id
"type": <a href='/sdk/data-task/'>TaskComment</a></pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMENT_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a comment for a task is updated.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": taskcomment_id
"type": <a href='/sdk/data-task/'>TaskComment</a></pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMENT_DELETED</th></tr>
    <tr><td colspan="2">Occurs when a comment for a task is removed.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": taskcomment_id
"type": <a href='/sdk/data-task/'>TaskComment</a></pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_LABELS_ADJUSTED</th></tr>
    <tr><td colspan="2">Occurs when a task's labels are changed.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": user_seelcted_tasklabel_id
"type": None</pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMPLETED</th></tr>
    <tr><td colspan="2">Occurs when a task is set to completed.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": task_id
"type": <a href='/sdk/data-task/'>Task</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_CLOSED</th></tr>
    <tr><td colspan="2">Occurs when a task is set to closed.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": task_id
"type": <a href='/sdk/data-task/'>Task</a></pre></td>
      <td><pre>"patient":
   "id": pt_id</pre></td>
    </tr>
  </tbody>
</table>

#### Vital Signs

<table>
  <thead>
    <tr><th colspan="2">VITAL_SIGN_CREATED</th></tr>
    <tr><td colspan="2">Occurs when a vitals entry is created for a patient using the vitals command. Additional details for the vitals become available with subsequent VITAL_SIGN_UPDATED events.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": vitalsign_id
"type": None</pre></td>
      <td><pre>empty</pre></td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">VITAL_SIGN_UPDATED</th></tr>
    <tr><td colspan="2">Occurs when a vitals entry is updated for a patient.</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
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

#### Adjust Prescription Command

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "prescribe": dict
  "change_medication_to": dict
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION__INDICATIONS__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION__INDICATIONS__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION__PHARMACY__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION__PHARMACY__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION__PRESCRIBE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION__PRESCRIBE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION__CHANGE_MEDICATION_TO__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ADJUST_PRESCRIPTION__CHANGE_MEDICATION_TO__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Allergy Command

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr>
    <tr>
      <td><pre>"id": command_uuid
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY__ALLERGY__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ALLERGY__ALLERGY__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Assess Command

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__CONDITION_SELECTED</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS__CONDITION__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ASSESS__CONDITION__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Cancel Prescription Command

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
      <td>CANCEL_PRESCRIPTION_COMMAND__PRE_ORIGINATE</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__POST_ORIGINATE</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__PRE_UPDATE</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__POST_UPDATE</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__PRE_COMMIT</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__POST_COMMIT</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__PRE_DELETE</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__POST_DELETE</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__POST_ENTER_IN_ERROR</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__PRE_EXECUTE_ACTION</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION_COMMAND__POST_EXECUTE_ACTION</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION__SELECTED_PRESCRIPTION__PRE_SEARCH</td>
      <td></td>
    </tr>
    <tr>
      <td>CANCEL_PRESCRIPTION__SELECTED_PRESCRIPTION__POST_SEARCH</td>
      <td></td>
    </tr>
  </tbody>
</table>

#### Change Medication Command

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION__MEDICATION__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CHANGE_MEDICATION__MEDICATION__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Clipboard Command

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "text": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLIPBOARD_COMMAND__POST_INSERTED_INTO_NOTE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "goal_id": dict
  "achievement_status": str
  "progress": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL__GOAL_ID__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">CLOSE_GOAL__GOAL_ID__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Diagnose Command

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE__DIAGNOSE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">DIAGNOSE__DIAGNOSE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Educational Material Command

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL__LANGUAGE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL__LANGUAGE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL__TITLE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">EDUCATIONAL_MATERIAL__TITLE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Family History Command

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "family_history": dict
  "relative": dict
  "note": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY__FAMILY_HISTORY__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY__FAMILY_HISTORY__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY__RELATIVE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FAMILY_HISTORY__RELATIVE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Follow Up Command

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "requested_date": dict
  "note_type": dict
  "coding": dict
  "reason_for_visit": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP__CODING__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP__CODING__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP__NOTE_TYPE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">FOLLOW_UP__NOTE_TYPE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Goal Command

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">GOAL_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">HISTORY_OF_PRESENT_ILLNESS_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER__IMAGE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER__IMAGE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER__IMAGING_CENTER__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER__IMAGING_CENTER__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER__INDICATIONS__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER__INDICATIONS__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER__ORDERING_PROVIDER__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMAGING_ORDER__ORDERING_PROVIDER__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Immunization Statement Command

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT__STATEMENT__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZATION_STATEMENT__STATEMENT__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Immunize Command

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE__CODING__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE__CODING__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE__GIVEN_BY__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE__GIVEN_BY__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE__LOT_NUMBER__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">IMMUNIZE__LOT_NUMBER__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Instruct Command

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "instruct": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT__INSTRUCT__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">INSTRUCT__INSTRUCT__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Lab Order Command

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER__DIAGNOSIS__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER__DIAGNOSIS__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER__LAB_PARTNER__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER__LAB_PARTNER__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER__ORDERING_PROVIDER__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER__ORDERING_PROVIDER__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER__TESTS__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">LAB_ORDER__TESTS__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Medical History Command

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY__APPROXIMATE_END_DATE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY__APPROXIMATE_END_DATE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY__APPROXIMATE_START_DATE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY__APPROXIMATE_START_DATE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Medication Statement Command

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT__MEDICATION__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">MEDICATION_STATEMENT__MEDICATION__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Perfom Command

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "perform": dict
  "notes": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM__PERFORM__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PERFORM__PERFORM__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Physical Exam Command

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM__QUESTIONNAIRE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PHYSICAL_EXAM__QUESTIONNAIRE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Plan Command

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PLAN_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE__INDICATIONS__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE__INDICATIONS__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE__PHARMACY__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE__PHARMACY__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE__PRESCRIBE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">PRESCRIBE__PRESCRIBE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Questionnaire Command

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
  "result": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE__QUESTIONNAIRE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">QUESTIONNAIRE__QUESTIONNAIRE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Reason for Visit Command

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "coding": dict
  "comment": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT__CODING__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REASON_FOR_VISIT__CODING__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Refer Command

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "refer_to": dict
  "indications": list[dict]
  "clinical_question": str
  "priority": str
  "notes_to_specialist": str
  "include_visit_note": bool
  "internal_comment": str
  "documents_to_include": dict
  "linked_items": list[dict]
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND__REFER_TO__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND__REFER_TO__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND__INDICATIONS__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND__INDICATIONS__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND__DOCUMENTS_TO_INCLUDE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND__DOCUMENTS_TO_INCLUDE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND__LINKED_ITEMS__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFER_COMMAND__LINKED_ITEMS__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Refill Prescription Command

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL__INDICATIONS__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL__INDICATIONS__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL__PHARMACY__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL__PHARMACY__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL__PRESCRIBE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REFILL__PRESCRIBE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Remove Allergy Command

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "allergy": dict
  "narrative": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY__ALLERGY__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">REMOVE_ALLERGY__ALLERGY__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Resolve Condition Command

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "condition": dict
  "show_in_condition_list": bool
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION__CONDITION__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">RESOLVE_CONDITION__CONDITION__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Review of Systems Command

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS__QUESTIONNAIRE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ROS__QUESTIONNAIRE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Snooze Protocol Command

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
    <td>SNOOZE_PROTOCOL_COMMAND__PRE_ORIGINATE</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__POST_ORIGINATE</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__PRE_UPDATE</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__POST_UPDATE</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__PRE_COMMIT</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__POST_COMMIT</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__PRE_DELETE</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__POST_DELETE</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__PRE_ENTER_IN_ERROR</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__POST_ENTER_IN_ERROR</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__PRE_EXECUTE_ACTION</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL_COMMAND__POST_EXECUTE_ACTION</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL__PROTOCOL__PRE_SEARCH</td>
    <td></td>
  </tr>
  <tr>
    <td>SNOOZE_PROTOCOL__PROTOCOL__POST_SEARCH</td>
    <td></td>
  </tr>

  </tbody>
</table>

#### Stop Medication Command

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "medication": dict
  "rationale": str
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION__MEDICATION__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STOP_MEDICATION__MEDICATION__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Structured Assessment Command

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"fields":
  "questionnaire": dict
"note":
  "uuid": note_id
"patient":
  "id": pt_id</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT__QUESTIONNAIRE__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">STRUCTURED_ASSESSMENT__QUESTIONNAIRE__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Surgical History Command

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY__PAST_SURGICAL_HISTORY__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SURGICAL_HISTORY__PAST_SURGICAL_HISTORY__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Task Command

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK__ASSIGN_TO__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK__ASSIGN_TO__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK__LABELS__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">TASK__LABELS__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Update Diagnosis Command

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
      <td>UPDATE_DIAGNOSIS_COMMAND__PRE_ORIGINATE</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__POST_ORIGINATE</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__PRE_UPDATE</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__POST_UPDATE</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__PRE_COMMIT</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__POST_COMMIT</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__PRE_DELETE</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__POST_DELETE</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__PRE_ENTER_IN_ERROR</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__POST_ENTER_IN_ERROR</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__PRE_EXECUTE_ACTION</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS_COMMAND__POST_EXECUTE_ACTION</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS__CONDITION__PRE_SEARCH</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS__CONDITION__POST_SEARCH</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS__NEW_CONDITION__PRE_SEARCH</td>
      <td></td>
    </tr>
    <tr>
      <td>UPDATE_DIAGNOSIS__NEW_CONDITION__POST_SEARCH</td>
      <td></td>
    </tr>
  </tbody>
</table>

#### Update Goal Command

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2"></th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL__GOAL_STATEMENT__POST_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">UPDATE_GOAL__GOAL_STATEMENT__PRE_SEARCH</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
      <td><pre>"search_term": str
"results": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

#### Vitals Command

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__POST_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__POST_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__POST_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__POST_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__POST_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__POST_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__PRE_COMMIT</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__PRE_DELETE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__PRE_ENTER_IN_ERROR</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__PRE_EXECUTE_ACTION</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__PRE_ORIGINATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

<table>
  <thead>
    <tr><th colspan="2">VITALS_COMMAND__PRE_UPDATE</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target object</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>"id": command_uuid 
"type": <a href='/sdk/data-command/'>Command</a></pre></td>
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

### Patient Portal lifecycle events

The following events are emitted during the lifecycle of a patient portal session.

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENT_CANCELED</th></tr>
    <tr><td colspan="3">Occurs after an appointment is canceled</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>appt_id</pre></td>
      <td><pre><a href='/sdk/data-appointment/'>Appointment</a></pre></td>
      <td><pre>None</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENT_RESCHEDULED</th></tr>
    <tr><td colspan="3">Occurs after an appointment is rescheduled</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>appt_id</pre></td>
      <td><pre><a href='/sdk/data-appointment/'>Appointment</a></pre></td>
      <td><pre>None</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENT_CAN_BE_CANCELED</th></tr>
    <tr><td colspan="3">Occurs when checking if an appointment can be canceled</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>appt_id</pre></td>
      <td><pre><a href='/sdk/data-appointment/'>Appointment</a></pre></td>
      <td><pre>None</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENT_CAN_BE_RESCHEDULED</th></tr>
    <tr><td colspan="3">Occurs when checking if an appointment can be rescheduled</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>appt_id</pre></td>
      <td><pre><a href='/sdk/data-appointment/'>Appointment</a></pre></td>
      <td><pre>None</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH</th></tr>
    <tr><td colspan="3">Occurs after the appointment slots search has been done, allowing the values to be modified</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
      <td><pre>"slots_by_provider": dict</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENTS__FORM_APPOINTMENT_TYPES__PRE_SEARCH</th></tr>
    <tr><td colspan="3">Occurs before appointment types are resolved, allowing the internal values to be bypassed</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENTS__FORM_APPOINTMENT_TYPES__POST_SEARCH</th></tr>
    <tr><td colspan="3">Occurs after appointment types are resolved, allowing the internal values to be modified</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
      <td><pre>"appointment_types": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__PRE_SEARCH</th></tr>
    <tr><td colspan="3">Occurs before appointment locations are resolved, allowing the internal values to be bypassed</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH</th></tr>
    <tr><td colspan="3">Occurs after appointment locations are resolved, allowing the internal values to be modified</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
      <td><pre>"locations": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__PRE_SEARCH</th></tr>
    <tr><td colspan="3">Occurs before appointment providers are resolved, allowing the internal values to be bypassed</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH</th></tr>
    <tr><td colspan="3">Occurs after appointment providers are resolved, allowing the internal values to be modified</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>None</pre></td>
      <td><pre>None</pre></td>
      <td><pre>"providers": list[dict]</pre></td>
    </tr>
  </tbody>  
</table>

### Action Buttons Events

For more information on handling these events, see <a href="/sdk/handlers-action-buttons" target="_blank">Action Buttons</a>.

<table>
  <thead>
    <tr><th colspan="2">SHOW_NOTE_HEADER_BUTTON</th></tr>
    <tr><td colspan="2">Occurs when patient notes are being loaded</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre>
  "note_id": str
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">SHOW_NOTE_FOOTER_BUTTON</th></tr>
    <tr><td colspan="2">Occurs when patient notes are being loaded</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre>
  "note_id": str
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_SOCIAL_DETERMINANTS_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for social determinants section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_GOALS_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for goals section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_CONDITIONS_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for conditions section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_MEDICATIONS_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for medications section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_ALLERGIES_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for allergies section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_CARE_TEAMS_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for care teams section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_VITALS_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for vitals section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_IMMUNIZATIONS_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for immunizations section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_SURGICAL_HISTORY_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for surgical history section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_FAMILY_HISTORY_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for family history section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="3">SHOW_CHART_SUMMARY_CODING_GAPS_SECTION_BUTTON</th></tr>
    <tr><td colspan="3">Occurs when patient chart summary is being loaded, specifically for coding gaps section</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

<table>
  <thead>
    <tr><th colspan="2">ACTION_BUTTON_CLICKED</th></tr>
    <tr><td colspan="2">Occurs when an action button is clicked</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre>
  "key": action_button_key
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

### Application Events

For more information on these events, see <a href="/sdk/handlers-applications" target="_blank">Applications</a>.

<table>
  <thead>
    <tr><th colspan="2">APPLICATION__ON_OPEN</th></tr>
    <tr><td colspan="2">Occurs when a user clicks on an application icon to open it</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>application_id</pre></td>
      <td><pre>
  "patient":
    "id": str
  "user": 
    "id": str
    "type": <a href='/sdk/data-staff/'>Staff</a> | <a href='/sdk/data-patient/'>Patient</a></pre></td>
    </tr>
  </tbody>  
</table>

### Patient Portal Events

<table>
  <thead>
    <tr><th colspan="3">PATIENT_PORTAL__GET_FORMS</th></tr>
    <tr><td colspan="3">Occurs on every page load of the Patient Portal; It only accepts the `PATIENT_PORTAL__FORM_RESULT` effect as a return value</td></tr>
  </thead>
  <tbody>
    <tr>
      <td>Target</td>
      <td>Target type</td>
      <td>Context object</td>
    </tr> 
    <tr> 
      <td><pre>patient_id</pre></td>
      <td><pre><a href='/sdk/data-patient/'>Patient</a></pre></td>
      <td><pre>"requested_from": str["appointment" |
                      "labs" |
                      "login" |
                      "messaging" |
                      "my-health" |
                      "payment" |
                      "search-appointment"]</pre></td>
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
      <td>This event fires regularly and can be used for scheduled tasks. See <a href='/sdk/handlers-crontask/'>CronTask</a>.</td>
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
    <tr>
      <td>PATIENT_PORTAL__WIDGET_CONFIGURATION</td>
      <td>Patient Portal landing page is loading. See <a href="{% link _guides/custom-landing-page.md %}" target="_blank">Tailoring Portal Landing Page</a> for examples of how to use this event.</td>
    </tr>
  </tbody>
</table>
