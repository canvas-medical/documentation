---
title: "Effects"
---

**What is an Effect?**

Effects are sent from plugins back to Canvas in order to perform an action. Effects can be used to react to events that are received in plugins and then send Canvas instructions to 'do something'.

**Why should I use them?**

Effects are useful because they can perform pre-determined actions in the Canvas EMR. This makes it possible to define workflows that, for example, create elements, show notifications or modify search results.

**How do I use them?**

Effects can be returned as a list from the `compute` method of a plugin that inherits from `BaseProtocol`. For example:

```python
import json

from canvas_sdk.events import EventType
from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.protocols import BaseProtocol

class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.MEDICATION_STATEMENT__MEDICATION__POST_SEARCH)

    def compute(self):
        results = self.context.get("results")

        post_processed_results = []
        ## custom results modifying code here
        ...

        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(post_processed_results),
            )
        ]
```

For more information on writing plugins, see the guide [here](/guides/your-first-plugin/).

## Effect Types

The following effects are available to be applied in Canvas.

| Effect | Description |
| ----- | ----------- |
| AUTOCOMPLETE_SEARCH_RESULTS | Can be used to modify search results by re-ordering or adding text annotations to individual result records. To see how you can put this to use, check out [this guide](/guides/customize-search-results/). |
| ADD_BANNER_ALERT | Can be used to add a banner alert to a patient's chart. |
| REMOVE_BANNER_ALERT | Can be used to remove a banner alert from a patient's chart. |
| ORIGINATE_ASSESS_COMMAND | Can be used to originate an assess command in a note. |
| ORIGINATE_DIAGNOSE_COMMAND | Can be used to originate a diagnose command in a note. |
| ORIGINATE_GOAL_COMMAND | Can be used to originate a goal command in a note. |
| ORIGINATE_HPI_COMMAND | Can be used to originate a history of present illness command in a note. |
| ORIGINATE_MEDICATION_STATEMENT_COMMAND | Can be used to originate a medication statement command in a note. |
| ORIGINATE_PLAN_COMMAND | Can be used to originate a plan command in a note. |
| ORIGINATE_PRESCRIBE_COMMAND | Can be used to originate a prescribe command in a note. |
| ORIGINATE_QUESTIONNAIRE_COMMAND | Can be used to originate a questionnaire command in a note. |
| ORIGINATE_REASON_FOR_VISIT_COMMAND | Can be used to originate a reason for visit command in a note. |
| ORIGINATE_STOP_MEDICATION_COMMAND | Can be used to originate a stop medication command in a note. |
| ORIGINATE_UPDATE_GOAL_COMMAND | Can be used to originate an update goal command in a note. |
| CREATE_TASK | Cause a task you define in a plugin to be created. Use the [Task class](/sdk/data-task/) in the data module. |
| UPDATE_TASK | Cause a task to be updated. Use the [Task class](/sdk/data-task/) in the data module. |
| CREATE_TASK_COMMENT | Add a comment to an existing task. Use the [Task class](/sdk/data-task/) in the data module. |
| ANNOTATE_PATIENT_CHART_CONDITION_RESULTS| Add an annotation to a condition within the patient summary |
| ADD_OR_UPDATE_PROTOCOL_CARD | Can be used to generate a ProtocolCard in the Canvas UI. Use the ProtocolCard class in the effects module. 

<br/>
<br/>
<br/>

## Protocol Card

Protocol cards appear on the right-hand-side of a patient's chart, and can be accessed by clicking on the Protocols filter button in the filter menu. 

{:refdef: style="text-align: center;"}
![protocol card](/assets/images/protocol-card.png){:width="95%"}
{: refdef}


A Protocol card consists of three main parts:
- A title, which appears at the top in bold
- A narrative, which appears just below the title to add any additional clarifying information
- A list of recommendations, which each have a title and optionally a button that can either:
    - open a new tab and navigate to another site
    - insert a command into a note

| Name           | Type     | Required                               | Description                                                             |
| :------------- | :------- | :------------------------------------- | :---------------------------------------------------------------------- |
| `patient_id`      | _string_ | `true`                                 | The patient key  |
| `key`      | _string_ | `true`       | A unique identifier for the protocol card |
| `title` | _string_ | `true` | The title for the protocol card, which appears at the top in bold   |
| `narrative` | _string_ | `false` | The narrative for the protocol card, which appears just below the title   |
| `recommendations` | list[_Recommendation_] | `false` | The recommendations to appear in the protocol card   |
|  |  |  |    |


| `Recommendation`     |      |      |         |
| :------------- | :------- | :------------------------------------- | :---------------------------------------------------------------------- |
| `title`      | _string_ | `true`                                 | The description of the recommendation |
| `button`      | _string_ | `false`       | The text to appear on the button |
| `href` | _string_ | `false` | The url for the button to navigate to   |
|  |  |  |    |

To include an command recommendation, we recommend you import the command from the [commands module](/sdk/commands/), instantiate the command with all the values you wish to populate, and then call `.recommend(title: str = "", button: str | None)` on the command to generate the recommendation that you can append to the protocol card's recommendations.
</br>
</br>
For non-command recommendations, you can either use the `Recommendation` class, or the `.add_recommendation(title: str = "", button: str = "", href: str | None)` method on the protocol card. 

**Example**:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from datetime import date
from canvas_sdk.effects.protocol_card import ProtocolCard, Recommendation
from canvas_sdk.commands import DiagnoseCommand


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self):
        p = ProtocolCard(
            patient_id=self.target,
            key="testing-protocol-cards",
            title="This is a ProtocolCard title",
            narrative="this is the narrative",
            recommendations=[Recommendation(title="this recommendation has no action, just words!")]
        )

        p.add_recommendation(
            title="this is a recommendation", button="go here", href="https://canvasmedical.com/"
        )

        diagnose = DiagnoseCommand(
            icd10_code="I10",
            background="feeling bad for many years",
            approximate_date_of_onset=date(2020, 1, 1),
            today_assessment="still not great",
        )
        p.recommendations.append(diagnose.recommend(title="this inserts a diagnose command"))

        return [p.apply()]
```