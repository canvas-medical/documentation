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

class Protocol(BaseHandler):
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

| Effect                                                   | Description                                                                                                                                                                                                 |
|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ADD_BANNER_ALERT                                         | Can be used to [add a banner alert](/sdk/effect-banner-alerts/#adding-a-banner-alert) to a patient's chart.                                                                                                 |
| REMOVE_BANNER_ALERT                                      | Can be used to [remove a banner alert](/sdk/effect-banner-alerts/#removing-a-banner-alert) from a patient's chart.                                                                                          |
| SHOW_PATIENT_CHART_SUMMARY_SECTIONS                      | Can be used to reorder or hide the summary sections in a patient chart. Check out [this effect class](/sdk/layout-effect/#patient-summary/).                                                                |
| PATIENT_CHART__GROUP_ITEMS                               | Can be used to group items within a specific patient chart section.                                                                                                                                         |
| SHOW_ACTION_BUTTON                                       | Can be used to show an action button. Check out [Action Buttons](/sdk/handlers-action-buttons/).                                                                                                            |
| LAUNCH_MODAL                                             | Can be used to launch a modal window. Check out [Modals](/sdk/layout-effect/#modals).                                                                                                                       |
| PORTAL_WIDGET                                            | Can be used to add widgets to patient portal landing page. Check out [Portal Landing Page Widgets](/sdk/layout-effect/#portal-landing-page-widgets)                                                         |
| ADD_OR_UPDATE_PROTOCOL_CARD                              | Can be used to generate a ProtocolCard in the Canvas UI. Use the [ProtocolCard](/sdk/effect-protocol-cards/) class in the effects module.                                                                   |
| ADD_BILLING_LINE_ITEM                                    | Can be used to generate a Billing Line Item in a note footer. Use the [AddBillingLineItem](/sdk/effect-billing-line-items/) class in the effects module.                                                    |
| UPDATE_BILLING_LINE_ITEM                                 | Can be used to update an existing Billing Line Item in a note footer. Use the [UpdateBillingLineItem](/sdk/effect-billing-line-items/) class in the effects module.                                         |
| REMOVE_BILLING_LINE_ITEM                                 | Can be used to remove a Billing Line Item in a note footer. Use the [RemoveBillingLineItem](/sdk/effect-billing-line-items/) class in the effects module.                                                   |
| ANNOTATE_CLAIM_CONDITION_RESULTS                         | Can be used to add annotations to the conditions appearing in a claim's detail view.                                                                                                                        |
| ANNOTATE_PATIENT_CHART_CONDITION_RESULTS                 | Add an annotation to a condition within the patient summary.                                                                                                                                                |
| ANNOTATE_PATIENT_CHART_DETECTED_ISSUE_RESULTS            | Add an annotation to a detected issue within the patient summary.                                                                                                                                           |
| AUTOCOMPLETE_SEARCH_RESULTS                              | Can be used to modify search results by re-ordering or adding text annotations to individual result records. To see how you can put this to use, check out [this guide](/guides/customize-search-results/). |
| PATIENT_PROFILE__ADD_PHARMACY__POST_SEARCH_RESULTS       | Can be used to modify pharmacy results when adding pharmacies in the patient profile.                                                                                                                       |
| CREATE_TASK                                              | Cause a task you define in a plugin to be created.                                                                                                                                                          |
| UPDATE_TASK                                              | Cause a task to be updated.                                                                                                                                                                                 |
| CREATE_TASK_COMMENT                                      | Add a comment to an existing task.                                                                                                                                                                          |
| COMMAND_AVAILABLE_ACTIONS_RESULTS                        | Can be used to sort or filter command available actions. Checkout command available [actions](sdk/commands/#command-actions)                                                                                |
| COMMAND_VALIDATION_ERRORS                                | Can be used to return validation errors for commands. Check out [Command Validation](/sdk/effect-command-validation/).                                                                                     |
| ORIGINATE_ALLERGY_COMMAND                                | Can be used to originate an allergy command in a note.                                                                                                                                                      |
| EDIT_ALLERGY_COMMAND                                     | Can be used to edit an allergy command in a note.                                                                                                                                                           |
| COMMIT_ALLERGY_COMMAND                                   | Can be used to commit an allergy command in a note.                                                                                                                                                         |
| ORIGINATE_REMOVE_ALLERGY_COMMAND                         | Can be used to originate a remove allergy command in a note.                                                                                                                                                |
| EDIT_REMOVE_ALLERGY_COMMAND                              | Can be used to edit a remove allergy command in a note.                                                                                                                                                     |
| COMMIT_REMOVE_ALLERGY_COMMAND                            | Can be used to commit a remove allergy command in a note.                                                                                                                                                   |
| ORIGINATE_GOAL_COMMAND                                   | Can be used to originate a goal command in a note.                                                                                                                                                          |
| EDIT_GOAL_COMMAND                                        | Can be used to edit a goal command in a note.                                                                                                                                                               |
| COMMIT_GOAL_COMMAND                                      | Can be used to commit a goal command in a note.                                                                                                                                                             |
| ORIGINATE_UPDATE_GOAL_COMMAND                            | Can be used to originate an update goal command in a note.                                                                                                                                                  |
| EDIT_UPDATE_GOAL_COMMAND                                 | Can be used to edit an update goal command in a note.                                                                                                                                                       |
| COMMIT_UPDATE_GOAL_COMMAND                               | Can be used to commit an update goal command in a note.                                                                                                                                                     |
| ORIGINATE_CLOSE_GOAL_COMMAND                             | Can be used to originate a close goal command in a note.                                                                                                                                                    |
| EDIT_CLOSE_GOAL_COMMAND                                  | Can be used to edit a close goal command in a note.                                                                                                                                                         |
| COMMIT_CLOSE_GOAL_COMMAND                                | Can be used to commit a close goal command in a note.                                                                                                                                                       |
| ORIGINATE_DIAGNOSE_COMMAND                               | Can be used to originate a diagnose command in a note.                                                                                                                                                      |
| EDIT_DIAGNOSE_COMMAND                                    | Can be used to edit a diagnose command in a note.                                                                                                                                                           |
| COMMIT_DIAGNOSE_COMMAND                                  | Can be used to commit a diagnose command in a note.                                                                                                                                                         |
| ORIGINATE_UPDATE_DIAGNOSIS_COMMAND                       | Can be used to originate an update diagnosis command in a note.                                                                                                                                             |
| EDIT_UPDATE_DIAGNOSIS_COMMAND                            | Can be used to edit an update diagnosis command in a note.                                                                                                                                                  |
| COMMIT_UPDATE_DIAGNOSIS_COMMAND                          | Can be used to commit an update diagnosis command in a note.                                                                                                                                                |
| ORIGINATE_CHANGE_MEDICATION_COMMAND                      | Can be used to originate a change medication command in a note.                                                                                                                                             |
| EDIT_CHANGE_MEDICATION_COMMAND                           | Can be used to edit a change medication command in a note.                                                                                                                                                  |
| COMMIT_CHANGE_MEDICATION_COMMAND                         | Can be used to commit a change medication command in a note.                                                                                                                                                |
| ORIGINATE_ASSESS_COMMAND                                 | Can be used to originate an assess command in a note.                                                                                                                                                       |
| EDIT_ASSESS_COMMAND                                      | Can be used to edit an assess command in a note.                                                                                                                                                            |
| COMMIT_ASSESS_COMMAND                                    | Can be used to commit an assess command in a note.                                                                                                                                                          |
| ORIGINATE_PRESCRIBE_COMMAND                              | Can be used to originate a prescribe command in a note.                                                                                                                                                     |
| EDIT_PRESCRIBE_COMMAND                                   | Can be used to edit a prescribe command in a note.                                                                                                                                                          |
| SEND_PRESCRIBE_COMMAND                                   | Can be used to send a committed prescribe command in a note.                                                                                                                                                |
| REVIEW_PRESCRIBE_COMMAND                                 | Can be used to set a prescribe command in review.                                                                                                                                                           |
| ORIGINATE_REFILL_COMMAND                                 | Can be used to originate a refill command in a note.                                                                                                                                                        |
| EDIT_REFILL_COMMAND                                      | Can be used to edit a refill command in a note.                                                                                                                                                             |
| SEND_REFILL_COMMAND                                      | Can be used to send a committed refill command in a note.                                                                                                                                                   |
| REVIEW_REFILL_COMMAND                                    | Can be used to set a refill command in review.                                                                                                                                                              |
| ORIGINATE_MEDICATION_STATEMENT_COMMAND                   | Can be used to originate a medication statement command in a note.                                                                                                                                          |
| EDIT_MEDICATION_STATEMENT_COMMAND                        | Can be used to edit a medication statement command in a note.                                                                                                                                               |
| COMMIT_MEDICATION_STATEMENT_COMMAND                      | Can be used to commit a medication statement command in a note.                                                                                                                                             |
| ORIGINATE_STOP_MEDICATION_COMMAND                        | Can be used to originate a stop medication command in a note.                                                                                                                                               |
| EDIT_STOP_MEDICATION_COMMAND                             | Can be used to edit a stop medication command in a note.                                                                                                                                                    |
| COMMIT_STOP_MEDICATION_COMMAND                           | Can be used to commit a stop medication command in a note.                                                                                                                                                  |
| ORIGINATE_PLAN_COMMAND                                   | Can be used to originate a plan command in a note.                                                                                                                                                          |
| EDIT_PLAN_COMMAND                                        | Can be used to edit a plan command in a note.                                                                                                                                                               |
| COMMIT_PLAN_COMMAND                                      | Can be used to commit a plan command in a note.                                                                                                                                                             |
| ORIGINATE_HPI_COMMAND                                    | Can be used to originate a history of present illness command in a note.                                                                                                                                    |
| EDIT_HPI_COMMAND                                         | Can be used to edit a history of present illness command in a note.                                                                                                                                         |
| COMMIT_HPI_COMMAND                                       | Can be used to commit a history of present illness command in a note.                                                                                                                                       |
| ORIGINATE_FAMILY_HISTORY_COMMAND                         | Can be used to originate a family history command in a note.                                                                                                                                                |
| EDIT_FAMILY_HISTORY_COMMAND                              | Can be used to edit a family history command in a note.                                                                                                                                                     |
| COMMIT_FAMILY_HISTORY_COMMAND                            | Can be used to commit a family history command in a note.                                                                                                                                                   |
| ORIGINATE_MEDICAL_HISTORY_COMMAND                        | Can be used to originate a medical history command in a note.                                                                                                                                               |
| EDIT_MEDICAL_HISTORY_COMMAND                             | Can be used to edit a medical history command in a note.                                                                                                                                                    |
| COMMIT_MEDICAL_HISTORY_COMMAND                           | Can be used to commit a medical history command in a note.                                                                                                                                                  |
| ORIGINATE_SURGICAL_HISTORY_COMMAND                       | Can be used to originate a surgical history command in a note.                                                                                                                                              |
| EDIT_SURGICAL_HISTORY_COMMAND                            | Can be used to edit a surgical history command in a note.                                                                                                                                                   |
| COMMIT_SURGICAL_HISTORY_COMMAND                          | Can be used to commit a surgical history command in a note.                                                                                                                                                 |
| ORIGINATE_INSTRUCT_COMMAND                               | Can be used to originate an instruct command in a note.                                                                                                                                                     |
| EDIT_INSTRUCT_COMMAND                                    | Can be used to edit an instruct command in a note.                                                                                                                                                          |
| COMMIT_INSTRUCT_COMMAND                                  | Can be used to commit an instruct command in a note.                                                                                                                                                        |
| ORIGINATE_LAB_ORDER_COMMAND                              | Can be used to originate a lab order command in a note.                                                                                                                                                     |
| EDIT_LAB_ORDER_COMMAND                                   | Can be used to edit a lab order command in a note.                                                                                                                                                          |
| COMMIT_LAB_ORDER_COMMAND                                 | Can be used to commit a lab order command in a note.                                                                                                                                                        |
| SEND_LAB_ORDER_COMMAND                                   | Can be used to send a committed lab order command in a note.                                                                                                                                                |
| ORIGINATE_PERFORM_COMMAND                                | Can be used to originate a perform command in a note.                                                                                                                                                       |
| EDIT_PERFORM_COMMAND                                     | Can be used to edit a perform command in a note.                                                                                                                                                            |
| COMMIT_PERFORM_COMMAND                                   | Can be used to commit a perform command in a note.                                                                                                                                                          |
| ORIGINATE_QUESTIONNAIRE_COMMAND                          | Can be used to originate a questionnaire command in a note.                                                                                                                                                 |
| EDIT_QUESTIONNAIRE_COMMAND                               | Can be used to edit a questionnaire command in a note.                                                                                                                                                      |
| COMMIT_QUESTIONNAIRE_COMMAND                             | Can be used to commit a questionnaire command in a note.                                                                                                                                                    |
| ORIGINATE_REASON_FOR_VISIT_COMMAND                       | Can be used to originate a reason for visit command in a note.                                                                                                                                              |
| EDIT_REASON_FOR_VISIT_COMMAND                            | Can be used to edit a reason for visit command in a note.                                                                                                                                                   |
| COMMIT_REASON_FOR_VISIT_COMMAND                          | Can be used to commit a reason for visit command in a note.                                                                                                                                                 |
| ORIGINATE_TASK_COMMAND                                   | Can be used to originate a task command in a note.                                                                                                                                                          |
| EDIT_TASK_COMMAND                                        | Can be used to edit a task command in a note.                                                                                                                                                               |
| COMMIT_TASK_COMMAND                                      | Can be used to commit a task command in a note.                                                                                                                                                             |
| ORIGINATE_VITALS_COMMAND                                 | Can be used to originate a vitals command in a note.                                                                                                                                                        |
| EDIT_VITALS_COMMAND                                      | Can be used to edit a vitals command in a note.                                                                                                                                                             |
| COMMIT_VITALS_COMMAND                                    | Can be used to commit a vitals command in a note.                                                                                                                                                           |
| ORIGINATE_FOLLOW_UP_COMMAND                              | Can be used to originate a follow up command in a note.                                                                                                                                                     |
| EDIT_FOLLOW_UP_COMMAND                                   | Can be used to edit a follow up command in a note.                                                                                                                                                          |
| COMMIT_FOLLOW_UP_COMMAND                                 | Can be used to commit a follow up command in a note.                                                                                                                                                        |
| ORIGINATE_IMAGING_ORDER_COMMAND                          | Can be used to originate a imaging order command in a note.                                                                                                                                                 |
| EDIT_IMAGING_ORDER_COMMAND                               | Can be used to edit a imaging order command in a note.                                                                                                                                                      |
| COMMIT_IMAGING_ORDER_COMMAND                             | Can be used to commit a imaging order command in a note.                                                                                                                                                    |
| ORIGINATE_REFER_COMMAND                                  | Can be used to originate a refer command in a note.                                                                                                                                                         |
| EDIT_REFER_COMMAND                                       | Can be used to edit a refer command in a note.                                                                                                                                                              |
| COMMIT_REFER_COMMAND                                     | Can be used to commit a refer command in a note.                                                                                                                                                            |
| ORIGINATE_ADJUST_PRESCRIPTION_COMMAND                    | Can be used to originate an adjust prescription command in a note.                                                                                                                                          |
| EDIT_ADJUST_PRESCRIPTION_COMMAND                         | Can be used to edit an adjust prescription command in a note.                                                                                                                                               |
| SEND_ADJUST_PRESCRIPTION_COMMAND                         | Can be used to send a adjust prescription command in a note.                                                                                                                                                |
| REVIEW_ADJUST_PRESCRIPTION_COMMAND                       | Can be used to set an adjust prescription command in review.                                                                                                                                                |
| ORIGINATE_RESOLVE_CONDITION_COMMAND                      | Can be used to originate a resolve condition command in a note.                                                                                                                                             |
| EDIT_RESOLVE_CONDITION_COMMAND                           | Can be used to edit a resolve condition command in a note.                                                                                                                                                  |
| COMMIT_RESOLVE_CONDITION_COMMAND                         | Can be used to commit a resolve condition command in a note.                                                                                                                                                |
| PATIENT_PORTAL__APPOINTMENT_SHOW_MEETING_LINK            | Can be used to show the 'join' button on the telehealth appointment card, allowing patients to easily join their appointments.                                                                              |
| PATIENT_PORTAL__APPOINTMENT_IS_CANCELABLE                | Can be used to show the 'cancel' button on the appointment card, allowing patients to easily cancel their appointments                                                                                      |
| PATIENT_PORTAL__APPOINTMENT_IS_RESCHEDULABLE             | Can be used to show the 'reschedule' button on the appointment card, allowing patients to easily reschedule their appointments                                                                              |
| UPDATE_USER                                              | Can be used to update a user                                                                                                                                                                                |
| PATIENT_PORTAL__SEND_INVITE                              | Can be used to trigger a portal invitation for a user                                                                                                                                                       |
| PATIENT_METADATA__CREATE_ADDITIONAL_FIELDS               | Can be used to show additional fields on the patient profile section                                                                                                                                        |
| APPOINTMENT__FORM__PROVIDERS__PRE_SEARCH_RESULTS         | Can be used to modify the list of providers shown in the appointment scheduling form before a search is performed                                                                                           |
| APPOINTMENT__FORM__LOCATIONS__PRE_SEARCH_RESULTS         | Can be used to modify the list of locations shown in the appointment scheduling form before a search is performed                                                                                           |
| APPOINTMENT__FORM__VISIT_TYPES__PRE_SEARCH_RESULTS       | Can be used to modify the list of visit types shown in the appointment scheduling form before a search is performed                                                                                         |
| APPOINTMENT__FORM__DURATIONS__PRE_SEARCH_RESULTS         | Can be used to modify the list of durations shown in the appointment scheduling form before a search is performed                                                                                           |
| APPOINTMENT__FORM__REASON_FOR_VISIT__PRE_SEARCH_RESULTS  | Can be used to modify the reason for visit field in the appointment scheduling form before a search is performed                                                                                            |
| APPOINTMENT__FORM__PROVIDERS__POST_SEARCH_RESULTS        | Can be used to modify the list of providers shown in the appointment scheduling form after a search is performed                                                                                            |
| APPOINTMENT__FORM__LOCATIONS__POST_SEARCH_RESULTS        | Can be used to modify the list of locations shown in the appointment scheduling form after a search is performed                                                                                            |
| APPOINTMENT__FORM__VISIT_TYPES__POST_SEARCH_RESULTS      | Can be used to modify the list of visit types shown in the appointment scheduling form after a search is performed                                                                                          |
| APPOINTMENT__FORM__DURATIONS__POST_SEARCH_RESULTS        | Can be used to modify the list of durations shown in the appointment scheduling form after a search is performed                                                                                            |
| APPOINTMENT__FORM__REASON_FOR_VISIT__POST_SEARCH_RESULTS | Can be used to modify the reason for visit field in the appointment scheduling form after a search is performed                                                                                             |
| APPOINTMENT__FORM__CREATE_ADDITIONAL_FIELDS              | Can be used to show additional fields on the appointment scheduling form                                                                                                                                    |
| UPSERT_APPOINTMENT_METADATA                              | Can be used to add additional metadata when creating or updating an appointment                                                                                                                             |
| RESCHEDULE_APPOINTMENT                                   | Can be used to reschedule an appointment. Check out [Appointment Effects](/sdk/effect-notes/#reschedule-appointment).                                                                                       |
| RESCHEDULE_SCHEDULE_EVENT                                | Can be used to reschedule a schedule event. Check out [Schedule Event Effects](/sdk/effect-notes/#reschedule-schedule-event).                                                                               |
| APPOINTMENT__SLOTS__POST_SEARCH_RESULTS                  | Can be used to modify slot availability when scheduling an appointment                                                                                                                                      |

<br/>
<br/>
<br/>
