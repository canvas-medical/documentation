---
title: "Effects"
---

Effects are instructions that plugins can return in order to perform an action
in the Canvas EMR. This makes it possible to define workflows that create
commands, show notifications, modify search results, etc.

Effects have a `type` and a `payload`. The `type` determines the action that
will be performed with the data provided in the `payload`.

## Using Effects

### Basic Usage

Effects are returned as a list from the `compute` method of a plugin that inherits from `BaseHandler`. For example:

```python
import json

from canvas_sdk.events import EventType
from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.handlers.base import BaseHandler

class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.MEDICATION_STATEMENT__MEDICATION__POST_SEARCH)

    def compute(self):
        results = self.context.get("results")

        post_processed_results = []
        ## custom results-modifying code here
        ...

        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(post_processed_results),
            )
        ]
```

In the above example, the `Effect` object is constructed manually, with the
`type` and `payload` set directly.

Some effects have helper classes that assist you by providing payload validation
and constructing the effect object for you. The example below shows the
[`PatientChartSummaryConfiguration`](/sdk/layout-effect/#patient-summary) class in use:

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.effects.patient_chart_summary_configuration import PatientChartSummaryConfiguration


class CustomChartLayout(BaseHandler):
    """
    This event handler rearranges the patient summary section and hides those
    not used by the installation's organization.
    """

    # This event fires when a patient's chart summary section is loading.
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION)

    def compute(self):
        layout = PatientChartSummaryConfiguration(sections=[
          PatientChartSummaryConfiguration.Section.SOCIAL_DETERMINANTS,
          PatientChartSummaryConfiguration.Section.ALLERGIES,
          PatientChartSummaryConfiguration.Section.VITALS,
          PatientChartSummaryConfiguration.Section.MEDICATIONS,
          PatientChartSummaryConfiguration.Section.CONDITIONS,
          PatientChartSummaryConfiguration.Section.IMMUNIZATIONS,
        ])

        return [layout.apply()]
```

### Disallowed Effect/Event Combinations

Canvas prevents certain combinations of events and effects to avoid infinite loops that could occur when an effect triggers the same event that generated it. The following combinations are specifically disallowed:

| Event Type | Disallowed Effect Types |
|------------|------------------------|
| `PATIENT_CHART__CONDITIONS` | `ADD_BANNER_ALERT`<br/>`ADD_OR_UPDATE_PROTOCOL_CARD` |
| `PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION` | `ADD_BANNER_ALERT`<br/>`ADD_OR_UPDATE_PROTOCOL_CARD` |

For example, if you have a plugin that responds to `PATIENT_CHART__CONDITIONS` events, you cannot return `ADD_BANNER_ALERT` or `ADD_OR_UPDATE_PROTOCOL_CARD` effects from that plugin, as this could create an infinite loop where the effect triggers another conditions event.

## Effect Classes

<div class="sdk-card-list">
{% for item in site.menus.effects_module %}
    <a href="{{ item.url }}">
        <div class="sdk-card">
            <span class="cardHeading">{{ item.title }}</span>
            <p>{{ item.description }}</p>
        </div>
    </a>

{% endfor %}
<a href="/sdk/commands/">

<div class="sdk-card">
<span class="cardHeading">Commands</span>
<p>The building blocks of many end-user workflows in Canvas, including nearly all clinical workflows for documentation.</p>
</div>
</a>

</div>

## Effect Types

The following effects are available to be applied in Canvas.

### Banner Alerts & Protocol Cards

| Effect | Description |
|---|---|
| ADD_BANNER_ALERT | Can be used to [add a banner alert](/sdk/effect-banner-alerts/#adding-a-banner-alert) to a patient's chart. |
| REMOVE_BANNER_ALERT | Can be used to [remove a banner alert](/sdk/effect-banner-alerts/#removing-a-banner-alert) from a patient's chart. |
| ADD_OR_UPDATE_PROTOCOL_CARD | Can be used to generate a ProtocolCard in the Canvas UI. Use the [ProtocolCard](/sdk/effect-protocol-cards/) class in the effects module. |

### Layout & Navigation

| Effect                                      | Description |
|---------------------------------------------|---|
| SHOW_PATIENT_CHART_SUMMARY_SECTIONS         | Can be used to reorder or hide the summary sections in a patient chart. Check out [this effect class](/sdk/layout-effect/#patient-summary). |
| PATIENT_CHART_SUMMARY__CUSTOM_SECTION       | Can be used to serve content for a custom patient chart summary section. Check out [Patient Chart Summary Custom Section](/sdk/patient-chart-summary-custom-section-effect/). |
| SHOW_PATIENT_PROFILE_SECTIONS               | Can be used to reorder or hide sections in the patient profile. Check out [Layout Effects](/sdk/layout-effect/#patient-profile). |
| SHOW_PANEL_SECTIONS                         | Can be used to reorder or hide sections in the side panel. Check out [Layout Effects](/sdk/layout-effect/#panel-configuration). |
| SHOW_PATIENT_NOTE_HEADER_DROPDOWN_SECTIONS  | Can be used to hide items in the note header triple dot button dropdown. Check out [this effect class](/sdk/layout-effect/#patient-note-header-dropdown-configuration/).                                    |
| PATIENT_CHART__GROUP_ITEMS                  | Can be used to group items within a specific patient chart section. Check out [Patient Chart Group](/sdk/patient-chart-group-effect/). |
| PATIENT_TIMELINE__CONFIGURATION             | Can be used to configure the patient timeline display. Check out [Patient Timeline](/sdk/effect-patient-timeline/). |
| HOMEPAGE_CONFIGURATION                      | Can be used to configure the homepage layout. Check out [Default Homepage](/sdk/default-homepage-effect/). |
| SHOW_ACTION_BUTTON                          | Can be used to show an action button. Check out [Action Buttons](/sdk/handlers-action-buttons/) and [LaunchModalEffects](/sdk/layout-effect/#modals). |
| SHOW_APPLICATION                            | Can be used to show a custom application. Check out [Applications](/sdk/handlers-applications/)  and [LaunchModalEffects](/sdk/layout-effect/#modals). |
| REDIRECT_CONTEXT                            | Can be used to redirect the user to a different context. Check out [Layout Effects](/sdk/handlers-applications/#context-change-events). |


### Search Results

| Effect | Description |
|---|---|
| AUTOCOMPLETE_SEARCH_RESULTS | Can be used to modify search results by re-ordering or adding text annotations to individual result records. To see how you can put this to use, check out [this guide](/guides/customize-search-results/). |
| PATIENT_PROFILE__ADD_PHARMACY__POST_SEARCH_RESULTS | Can be used to modify pharmacy results when adding pharmacies in the patient profile. |


### Annotations

Check out [this guide](/guides/improve-hcc-coding-accuracy/#adding-annotations-to-conditions-and-detected-issues) for examples of using annotation effects.

| Effect | Description |
|---|---|
| ANNOTATE_CLAIM_CONDITION_RESULTS | Add annotations to conditions appearing in a claim's detail view. |
| ANNOTATE_PATIENT_CHART_CONDITION_RESULTS | Add an annotation to a condition within the patient summary. |
| ANNOTATE_PATIENT_CHART_DETECTED_ISSUE_RESULTS | Add an annotation to a detected issue within the patient summary. |


### Billing Line Items

Check out the [Billing Line Items](/sdk/effect-billing-line-items/) effect class documentation.

| Effect | Description |
|---|---|
| ADD_BILLING_LINE_ITEM | Generate a Billing Line Item in a note footer. |
| UPDATE_BILLING_LINE_ITEM | Update an existing Billing Line Item in a note footer. |
| REMOVE_BILLING_LINE_ITEM | Remove a Billing Line Item from a note footer. |


### Tasks

Check out the [Task Effects](/sdk/effect-tasks/) and [Task Metadata](/sdk/effect-task-metadata/) documentation.

| Effect | Description |
|---|---|
| CREATE_TASK | Create a task from a plugin. |
| UPDATE_TASK | Update an existing task. |
| CREATE_TASK_COMMENT | Add a comment to an existing task. |
| UPSERT_TASK_METADATA | Add or update metadata on a task. |


### Command Metadata & Validation

| Effect | Description |
|---|---|
| UPSERT_COMMAND_METADATA | Add or update metadata on a command. Check out [Command Metadata](/sdk/effect-command-metadata/). |
| COMMAND_AVAILABLE_ACTIONS_RESULTS | Sort or filter command available actions. Check out [Command Actions](/sdk/commands/#command-actions). |
| COMMAND_VALIDATION_ERRORS | Return validation errors for commands. Check out [Command Validation](/sdk/effect-command-validation/). |
| EVENT_VALIDATION_ERROR | Return validation errors for events. Check out [Event Validation Error](/sdk/effect-event-validation-error/). |
| BATCH_ORIGINATE_COMMANDS | Originate multiple commands in a note at once. Check out [Batch Originate](/sdk/effect-batch-originate/). |


### Notes

Check out the [Note Effects](/sdk/effect-notes/) documentation.

| Effect | Description |
|---|---|
| CREATE_NOTE | Create a note. |
| UPDATE_NOTE | Update a note. |
| LOCK_NOTE | Lock a note. |
| UNLOCK_NOTE | Unlock a note. |
| SIGN_NOTE | Sign a note. |
| CHECK_IN_NOTE | Check in a note. |
| NO_SHOW_NOTE | Mark a note as no-show. |
| FAX_NOTE | Fax a note to an external recipient. |
| PUSH_NOTE_CHARGES | Push note charges for billing. |
| UPSERT_NOTE_METADATA | Add or update metadata on a note. |
| GENERATE_FULL_CHART_PDF | Generate a full chart PDF for a patient. |


### Appointments

Check out the [Appointment Effects](/sdk/effect-notes/#appointment-effect), [Appointment Labels](/sdk/effect-appointment-labels/), and [Appointment Metadata](/sdk/effect-appointment-metadata/) documentation.

| Effect | Description |
|---|---|
| CREATE_APPOINTMENT | Create an appointment. |
| UPDATE_APPOINTMENT | Update an appointment. |
| RESCHEDULE_APPOINTMENT | Reschedule an appointment. |
| CANCEL_APPOINTMENT | Cancel an appointment. |
| ADD_APPOINTMENT_LABEL | Add one or more labels to an appointment (max 3 total). |
| REMOVE_APPOINTMENT_LABEL | Remove one or more labels from an appointment. |
| UPSERT_APPOINTMENT_METADATA | Add or update metadata on an appointment. |


### Appointment Scheduling Form

Check out the [Appointment Metadata Create Form](/sdk/appointment-metadata-create-form-effect/) documentation.

| Effect | Description |
|---|---|
| APPOINTMENT__FORM__PROVIDERS__PRE_SEARCH_RESULTS | Modify the list of providers before a search. |
| APPOINTMENT__FORM__LOCATIONS__PRE_SEARCH_RESULTS | Modify the list of locations before a search. |
| APPOINTMENT__FORM__VISIT_TYPES__PRE_SEARCH_RESULTS | Modify the list of visit types before a search. |
| APPOINTMENT__FORM__DURATIONS__PRE_SEARCH_RESULTS | Modify the list of durations before a search. |
| APPOINTMENT__FORM__REASON_FOR_VISIT__PRE_SEARCH_RESULTS | Modify the reason for visit field before a search. |
| APPOINTMENT__FORM__PROVIDERS__POST_SEARCH_RESULTS | Modify the list of providers after a search. |
| APPOINTMENT__FORM__LOCATIONS__POST_SEARCH_RESULTS | Modify the list of locations after a search. |
| APPOINTMENT__FORM__VISIT_TYPES__POST_SEARCH_RESULTS | Modify the list of visit types after a search. |
| APPOINTMENT__FORM__DURATIONS__POST_SEARCH_RESULTS | Modify the list of durations after a search. |
| APPOINTMENT__FORM__REASON_FOR_VISIT__POST_SEARCH_RESULTS | Modify the reason for visit field after a search. |
| APPOINTMENT__FORM__CREATE_ADDITIONAL_FIELDS | Show additional fields on the appointment scheduling form. |
| APPOINTMENT__SLOTS__POST_SEARCH_RESULTS | Modify slot availability when scheduling an appointment. |


### Schedule Events

Check out the [Schedule Event Effects](/sdk/effect-notes/#schedule-event-effects) documentation.

| Effect | Description |
|---|---|
| CREATE_SCHEDULE_EVENT | Create a schedule event. |
| UPDATE_SCHEDULE_EVENT | Update a schedule event. |
| DELETE_SCHEDULE_EVENT | Delete a schedule event. |
| RESCHEDULE_SCHEDULE_EVENT | Reschedule a schedule event. |


### Calendar

Check out the [Create Calendar](/sdk/calendar-create-effect/) and [Manage Calendar Events](/sdk/calendar-event-management-effects/) documentation.

| Effect | Description |
|---|---|
| CALENDAR__CREATE | Create a calendar. |
| CALENDAR__EVENT__CREATE | Create a calendar event. |
| CALENDAR__EVENT__UPDATE | Update a calendar event. |
| CALENDAR__EVENT__DELETE | Delete a calendar event. |


### Patients

Check out the [Patient Effects](/sdk/effect-patient/), [Patient Metadata](/sdk/effect-patient-metadata/), [Patient External ID](/sdk/effect-create-patient-external-identifier/), and [Patient Facility Address](/sdk/effect-patient-facility-address/) documentation.

| Effect | Description |
|---|---|
| CREATE_PATIENT | Create a patient. |
| UPDATE_PATIENT | Update a patient. |
| UPDATE_USER | Update a user. |
| PATIENT_METADATA__CREATE_ADDITIONAL_FIELDS | Show additional fields on the patient profile section. |
| UPSERT_PATIENT_METADATA | Add or update metadata on a patient. |
| CREATE_PATIENT_EXTERNAL_IDENTIFIER | Create an external identifier for a patient. |
| CREATE_PATIENT_PREFERRED_PHARMACIES | Set preferred pharmacies for a patient. |
| CREATE_PATIENT_FACILITY_ADDRESS | Create a facility address for a patient. |
| UPDATE_PATIENT_FACILITY_ADDRESS | Update a facility address for a patient. |
| DELETE_PATIENT_FACILITY_ADDRESS | Delete a facility address for a patient. |


### Patient Groups

Check out the [Patient Group](/sdk/effect-patient-group/) documentation.

| Effect | Description |
|---|---|
| PATIENT_GROUP__ADD_MEMBER | Add a member to a patient group. |
| PATIENT_GROUP__DEACTIVATE_MEMBER | Deactivate a member from a patient group. |


### Messages

Check out the [Message Effects](/sdk/effect-messages/) documentation.

| Effect | Description |
|---|---|
| CREATE_MESSAGE | Create a message. |
| SEND_MESSAGE | Send a message. |
| CREATE_AND_SEND_MESSAGE | Create and send a message in one step. |
| EDIT_MESSAGE | Edit a message. |


### Observations

Check out the [Observation Effects](/sdk/effect-observation/) documentation.

| Effect | Description |
|---|---|
| CREATE_OBSERVATION | Create an observation. |
| UPDATE_OBSERVATION | Update an observation. |


### Questionnaire

Check out the [Questionnaire Effects](/sdk/effect-questionnaires/) documentation.

| Effect | Description |
|---|---|
| CREATE_QUESTIONNAIRE_RESULT | Create a questionnaire result. |


### Compound Medications

Check out the [Compound Medication Effects](/sdk/effect-compound-medication/) documentation.

| Effect | Description |
|---|---|
| CREATE_COMPOUND_MEDICATION | Create a compound medication. |
| UPDATE_COMPOUND_MEDICATION | Update a compound medication. |


### External Events

Check out the [External Event Effects](/sdk/effect-external-event/) documentation.

| Effect | Description |
|---|---|
| CREATE_EXTERNAL_EVENT | Create an external event. |
| UPDATE_EXTERNAL_EVENT | Update an external event. |


### CCDA

Check out the [C-CDA Export](/sdk/effect-create-ccda-export/) documentation.

| Effect | Description |
|---|---|
| CREATE_CCDA | Create a CCDA document. |


### Claims

Check out the [Claims Effects](/sdk/effect-claims/) documentation.

| Effect | Description |
|---|---|
| POST_CLAIM_PAYMENT | Post a payment to a claim. |
| MOVE_CLAIM_TO_QUEUE | Move a claim to a different queue. |
| ADD_CLAIM_LABEL | Add a label to a claim. |
| REMOVE_CLAIM_LABEL | Remove a label from a claim. |
| ADD_CLAIM_COMMENT | Add a comment to a claim. |
| ADD_CLAIM_BANNER_ALERT | Add a banner alert to a claim. |
| REMOVE_CLAIM_BANNER_ALERT | Remove a banner alert from a claim. |
| UPDATE_CLAIM_PROVIDER | Update the provider on a claim. |
| UPSERT_CLAIM_METADATA | Add or update metadata on a claim. |
| UPDATE_CLAIM_LINE_ITEM | Update a line item on a claim. |


### Patient Portal

Check out the [Patient Portal](/sdk/patient-portal/) and [Form Result](/sdk/form-result-effect/) documentation.

| Effect | Description |
|---|---|
| PORTAL_WIDGET | Add widgets to the patient portal landing page. |
| SHOW_PATIENT_PORTAL_MENU_ITEMS | Configure menu items in the patient portal. |
| PATIENT_PORTAL__APPLICATION_CONFIGURATION | Configure the patient portal application. |
| PATIENT_PORTAL__FORM_RESULT | Return form results in the patient portal. |
| PATIENT_PORTAL__APPOINTMENT_SHOW_MEETING_LINK | Show the 'join' button on the telehealth appointment card. |
| PATIENT_PORTAL__APPOINTMENT_IS_CANCELABLE | Show the 'cancel' button on the appointment card. |
| PATIENT_PORTAL__APPOINTMENT_IS_RESCHEDULABLE | Show the 'reschedule' button on the appointment card. |
| PATIENT_PORTAL__SEND_INVITE | Trigger a portal invitation for a user. |
| PATIENT_PORTAL__SEND_CONTACT_VERIFICATION | Send a contact verification in the patient portal. |
| PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH_RESULTS | Modify slot availability in the patient portal appointment scheduler. |
| PATIENT_PORTAL__APPOINTMENTS__FORM_APPOINTMENT_TYPES__PRE_SEARCH_RESULTS | Modify appointment types in the patient portal before a search. |
| PATIENT_PORTAL__APPOINTMENTS__FORM_APPOINTMENT_TYPES__POST_SEARCH_RESULTS | Modify appointment types in the patient portal after a search. |
| PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__PRE_SEARCH_RESULTS | Modify locations in the patient portal before a search. |
| PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH_RESULTS | Modify locations in the patient portal after a search. |
| PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__PRE_SEARCH_RESULTS | Modify providers in the patient portal before a search. |
| PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH_RESULTS | Modify providers in the patient portal after a search. |


### Simple API

Check out the [HTTP](/sdk/handlers-simple-api-http/) and [WebSocket](/sdk/handlers-simple-api-websocket/) SimpleAPI documentation.

| Effect | Description |
|---|---|
| SIMPLE_API_RESPONSE | Return a response from a SimpleAPI HTTP endpoint. |
| SIMPLE_API_WEBSOCKET_BROADCAST | Broadcast a message to WebSocket connections. |


### Revenue / Payment Processor

| Effect | Description |
|---|---|
| REVENUE__PAYMENT_PROCESSOR__METADATA | Can be used to provide payment processor metadata. |
| REVENUE__PAYMENT_PROCESSOR__FORM | Can be used to provide a payment processor form. |
| REVENUE__PAYMENT_PROCESSOR__CREDIT_CARD_TRANSACTION | Can be used to process a credit card transaction. |
| REVENUE__PAYMENT_PROCESSOR__PAYMENT_METHOD | Can be used to manage a payment method. |
| REVENUE__PAYMENT_PROCESSOR__PAYMENT_METHOD__ADD_RESPONSE | Can be used to respond to an add payment method request. |
| REVENUE__PAYMENT_PROCESSOR__PAYMENT_METHOD__REMOVE_RESPONSE | Can be used to respond to a remove payment method request. |


### Surescripts

| Effect | Description |
|---|---|
| SEND_SURESCRIPTS_ELIGIBILITY_REQUEST | Can be used to send a Surescripts eligibility request. |
| SEND_SURESCRIPTS_MEDICATION_HISTORY_REQUEST | Can be used to send a Surescripts medication history request. |
| SEND_SURESCRIPTS_BENEFITS_REQUEST | Can be used to send a Surescripts benefits request. |


### Commands

Check out the [Commands documentation](/sdk/commands/) for full details.

Command effects follow a consistent naming pattern: `{ACTION}_{COMMAND_TYPE}_COMMAND`. The available actions are:

| Action | Description |
|---|---|
| ORIGINATE | Create and open a new command in a note. Supports an optional `commit` flag to also commit the command in the same operation if the command is commit-able via SDK. |
| EDIT | Modify field values on an existing command. |
| DELETE | Remove an uncommitted command from a note. |
| COMMIT | Finalize and save a command. |
| ENTER_IN_ERROR | Mark a committed command as entered in error. |
| SEND | Transmit a committed command to an external system (prescribe, refill, adjust prescription, lab orders only). |
| REVIEW | Place a command into review status (prescribe, refill, adjust prescription only). |

The following command types support `ORIGINATE`, `EDIT`, `DELETE`, `COMMIT`, and `ENTER_IN_ERROR` actions unless noted otherwise:

| Command Type | Effect Prefix | Notes |
|---|---|---|
| Adjust Prescription | `*_ADJUST_PRESCRIPTION_COMMAND` | No COMMIT. Supports SEND and REVIEW |
| Allergy | `*_ALLERGY_COMMAND` | |
| Assess | `*_ASSESS_COMMAND` | |
| Change Medication | `*_CHANGE_MEDICATION_COMMAND` | |
| Chart Section Review | `*_CHART_SECTION_REVIEW_COMMAND` | ORIGINATE only |
| Close Goal | `*_CLOSE_GOAL_COMMAND` | |
| Custom Command | `*_CUSTOM_COMMAND_COMMAND` | ORIGINATE only |
| Diagnose | `*_DIAGNOSE_COMMAND` | |
| Exam | `*_EXAM_COMMAND` | |
| Family History | `*_FAMILY_HISTORY_COMMAND` | |
| Follow Up | `*_FOLLOW_UP_COMMAND` | |
| Goal | `*_GOAL_COMMAND` | |
| HPI | `*_HPI_COMMAND` | |
| Imaging Order | `*_IMAGING_ORDER_COMMAND` | No COMMIT or SEND |
| Imaging Review | `*_IMAGING_REVIEW_COMMAND` | |
| Immunization Statement | `*_IMMUNIZATION_STATEMENT_COMMAND` | |
| Instruct | `*_INSTRUCT_COMMAND` | |
| Lab Order | `*_LAB_ORDER_COMMAND` | Also supports SEND |
| Lab Review | `*_LAB_REVIEW_COMMAND` | |
| Medical History | `*_MEDICAL_HISTORY_COMMAND` | |
| Medication Statement | `*_MEDICATION_STATEMENT_COMMAND` | |
| Perform | `*_PERFORM_COMMAND` | |
| Plan | `*_PLAN_COMMAND` | |
| Prescribe | `*_PRESCRIBE_COMMAND` | No COMMIT. Supports SEND and REVIEW |
| Questionnaire | `*_QUESTIONNAIRE_COMMAND` | |
| Reason For Visit | `*_REASON_FOR_VISIT_COMMAND` | ORIGINATE, EDIT, DELETE only |
| Refer | `*_REFER_COMMAND` | No COMMIT |
| Referral Review | `*_REFERRAL_REVIEW_COMMAND` | |
| Refill | `*_REFILL_COMMAND` | No COMMIT. Supports SEND and REVIEW |
| Remove Allergy | `*_REMOVE_ALLERGY_COMMAND` | |
| Resolve Condition | `*_RESOLVE_CONDITION_COMMAND` | |
| Review of Systems | `*_ROS_COMMAND` | |
| Stop Medication | `*_STOP_MEDICATION_COMMAND` | |
| Structured Assessment | `*_STRUCTURED_ASSESSMENT_COMMAND` | |
| Surgical History | `*_SURGICAL_HISTORY_COMMAND` | |
| Task | `*_TASK_COMMAND` | |
| Uncategorized Document Review | `*_UNCATEGORIZED_DOCUMENT_REVIEW_COMMAND` | |
| Update Diagnosis | `*_UPDATE_DIAGNOSIS_COMMAND` | |
| Update Goal | `*_UPDATE_GOAL_COMMAND` | |
| Vitals | `*_VITALS_COMMAND` | |



<br/>
<br/>
<br/>
