---
title: "Effects"
---

Effects are instructions that plugins can return in order to perform an action
in the Canvas EMR. This makes it possible to define workflows that create
commands, show notifications, modify search results, etc.

Effects have a `type` and a `payload`. The `type` determines the action that
will be performed with the data provided in the `payload`.

## Using Effects

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

| Effect                                             | Description                                                                                                                                                                                                 |
|----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ADD_BANNER_ALERT                                   | Can be used to [add a banner alert](/sdk/effect-banner-alerts/#adding-a-banner-alert) to a patient's chart.                                                                                                 |
| REMOVE_BANNER_ALERT                                | Can be used to [remove a banner alert](/sdk/effect-banner-alerts/#removing-a-banner-alert) from a patient's chart.                                                                                          |
| SHOW_PATIENT_CHART_SUMMARY_SECTIONS                | Can be used to reorder or hide the summary sections in a patient chart. Check out [this effect class](/sdk/layout-effect/#patient-summary/).                                                                |
| SHOW_ACTION_BUTTON                                 | Can be used to show an action button. Check out [Action Buttons](/sdk/handlers-action-buttons/).                                                                                                            |
| LAUNCH_MODAL                                       | Can be used to launch a modal window. Check out [Modals](/sdk/layout-effect/#modals).                                                                                                                       |
| ADD_OR_UPDATE_PROTOCOL_CARD                        | Can be used to generate a ProtocolCard in the Canvas UI. Use the [ProtocolCard](/sdk/effect-protocol-cards/) class in the effects module.                                                                   |
| ANNOTATE_CLAIM_CONDITION_RESULTS                   | Can be used to add annotations to the conditions appearing in a claim's detail view.                                                                                                                        |
| ANNOTATE_PATIENT_CHART_CONDITION_RESULTS           | Add an annotation to a condition within the patient summary.                                                                                                                                                |
| AUTOCOMPLETE_SEARCH_RESULTS                        | Can be used to modify search results by re-ordering or adding text annotations to individual result records. To see how you can put this to use, check out [this guide](/guides/customize-search-results/). |
| PATIENT_PROFILE__ADD_PHARMACY__POST_SEARCH_RESULTS | Can be used to modify pharmacy results when adding pharmacies in the patient profile.                                                                                                                       |
| CREATE_TASK                                        | Cause a task you define in a plugin to be created.                                                                                                                                                          |
| UPDATE_TASK                                        | Cause a task to be updated.                                                                                                                                                                                 |
| CREATE_TASK_COMMENT                                | Add a comment to an existing task.                                                                                                                                                                          |
| ORIGINATE_ALLERGY_COMMAND                          | Can be used to originate an allergy command in a note.                                                                                                                                                      |
| COMMIT_ALLERGY_COMMAND                             | Can be used to commit an allergy command in a note.                                                                                                                                                         |
| ORIGINATE_REMOVE_ALLERGY_COMMAND                   | Can be used to originate a remove allergy command in a note.                                                                                                                                                |
| COMMIT_REMOVE_ALLERGY_COMMAND                      | Can be used to commit a remove allergy command in a note.                                                                                                                                                   |
| ORIGINATE_GOAL_COMMAND                             | Can be used to originate a goal command in a note.                                                                                                                                                          |
| COMMIT_GOAL_COMMAND                                | Can be used to commit a goal command in a note.                                                                                                                                                             |
| ORIGINATE_UPDATE_GOAL_COMMAND                      | Can be used to originate an update goal command in a note.                                                                                                                                                  |
| COMMIT_UPDATE_GOAL_COMMAND                         | Can be used to commit an update goal command in a note.                                                                                                                                                     |
| ORIGINATE_CLOSE_GOAL_COMMAND                       | Can be used to originate a close goal command in a note.                                                                                                                                                    |
| COMMIT_CLOSE_GOAL_COMMAND                          | Can be used to commit a close goal command in a note.                                                                                                                                                       |
| ORIGINATE_DIAGNOSE_COMMAND                         | Can be used to originate a diagnose command in a note.                                                                                                                                                      |
| COMMIT_DIAGNOSE_COMMAND                            | Can be used to commit a diagnose command in a note.                                                                                                                                                         |
| ORIGINATE_UPDATE_DIAGNOSIS_COMMAND                 | Can be used to originate an update diagnosis command in a note.                                                                                                                                             |
| COMMIT_UPDATE_DIAGNOSIS_COMMAND                    | Can be used to commit an update diagnosis command in a note.                                                                                                                                                |
| ORIGINATE_ASSESS_COMMAND                           | Can be used to originate an assess command in a note.                                                                                                                                                       |
| COMMIT_ASSESS_COMMAND                              | Can be used to commit an assess command in a note.                                                                                                                                                          |
| ORIGINATE_PRESCRIBE_COMMAND                        | Can be used to originate a prescribe command in a note.                                                                                                                                                     |
| ORIGINATE_REFILL_COMMAND                           | Can be used to originate a refill command in a note.                                                                                                                                                        |
| ORIGINATE_MEDICATION_STATEMENT_COMMAND             | Can be used to originate a medication statement command in a note.                                                                                                                                          |
| COMMIT_MEDICATION_STATEMENT_COMMAND                | Can be used to commit a medication statement command in a note.                                                                                                                                             |
| ORIGINATE_STOP_MEDICATION_COMMAND                  | Can be used to originate a stop medication command in a note.                                                                                                                                               |
| COMMIT_STOP_MEDICATION_COMMAND                     | Can be used to commit a stop medication command in a note.                                                                                                                                                  |
| ORIGINATE_PLAN_COMMAND                             | Can be used to originate a plan command in a note.                                                                                                                                                          |
| COMMIT_PLAN_COMMAND                                | Can be used to commit a plan command in a note.                                                                                                                                                             |
| ORIGINATE_HPI_COMMAND                              | Can be used to originate a history of present illness command in a note.                                                                                                                                    |
| COMMIT_HPI_COMMAND                                 | Can be used to commit a history of present illness command in a note.                                                                                                                                       |
| ORIGINATE_FAMILY_HISTORY_COMMAND                   | Can be used to originate a family history command in a note.                                                                                                                                                |
| COMMIT_FAMILY_HISTORY_COMMAND                      | Can be used to commit a family history command in a note.                                                                                                                                                   |
| ORIGINATE_MEDICAL_HISTORY_COMMAND                  | Can be used to originate a medical history command in a note.                                                                                                                                               |
| COMMIT_MEDICAL_HISTORY_COMMAND                     | Can be used to commit a medical history command in a note.                                                                                                                                                  |
| ORIGINATE_SURGICAL_HISTORY_COMMAND                 | Can be used to originate a surgical history command in a note.                                                                                                                                              |
| COMMIT_SURGICAL_HISTORY_COMMAND                    | Can be used to commit a surgical history command in a note.                                                                                                                                                 |
| ORIGINATE_INSTRUCT_COMMAND                         | Can be used to originate an instruct command in a note.                                                                                                                                                     |
| COMMIT_INSTRUCT_COMMAND                            | Can be used to commit an instruct command in a note.                                                                                                                                                        |
| ORIGINATE_LAB_ORDER_COMMAND                        | Can be used to originate a lab order command in a note.                                                                                                                                                     |
| ORIGINATE_PERFORM_COMMAND                          | Can be used to originate a perform command in a note.                                                                                                                                                       |
| COMMIT_PERFORM_COMMAND                             | Can be used to commit a perform command in a note.                                                                                                                                                          |
| ORIGINATE_QUESTIONNAIRE_COMMAND                    | Can be used to originate a questionnaire command in a note.                                                                                                                                                 |
| COMMIT_QUESTIONNAIRE_COMMAND                       | Can be used to commit a questionnaire command in a note.                                                                                                                                                    |
| ORIGINATE_REASON_FOR_VISIT_COMMAND                 | Can be used to originate a reason for visit command in a note.                                                                                                                                              |
| COMMIT_REASON_FOR_VISIT_COMMAND                    | Can be used to commit a reason for visit command in a note.                                                                                                                                                 |
| ORIGINATE_TASK_COMMAND                             | Can be used to originate a task command in a note.                                                                                                                                                          |
| COMMIT_TASK_COMMAND                                | Can be used to commit a task command in a note.                                                                                                                                                             |
| ORIGINATE_VITALS_COMMAND                           | Can be used to originate a vitals command in a note.                                                                                                                                                        |
| COMMIT_VITALS_COMMAND                              | Can be used to commit a vitals command in a note.                                                                                                                                                           |
| ORIGINATE_FOLLOW_UP_COMMAND                        | Can be used to originate a follow up command in a note.                                                                                                                                                     |
| COMMIT_FOLLOW_UP_COMMAND                           | Can be used to commit a follow up command in a note.                                                                                                                                                        |
| ORIGINATE_IMAGING_ORDER_COMMAND                    | Can be used to originate a imaging order command in a note.                                                                                                                                                 |
| COMMIT_IMAGING_ORDER_COMMAND                       | Can be used to commit a imaging order command in a note.                                                                                                                                                    |
| ORIGINATE_REFER_COMMAND                            | Can be used to originate a refer command in a note.                                                                                                                                                         |
| COMMIT_REFER_COMMAND                               | Can be used to commit a refer command in a note.                                                                                                                                                            |
| ORIGINATE_ADJUST_PRESCRIPTION_COMMAND              | Can be used to originate an adjust prescription command in a note.                                                                                                                                          |
| COMMIT_ADJUST_PRESCRIPTION_COMMAND                 | Can be used to commit a adjust prescription command in a note.                                                                                                                                              |
| ORIGINATE_RESOLVE_CONDITION_COMMAND                | Can be used to originate a resolve condition command in a note.                                                                                                                                             |
| COMMIT_RESOLVE_CONDITION_COMMAND                   | Can be used to commit a resolve condition command in a note.                                                                                                                                                |

<br/>
<br/>
<br/>

