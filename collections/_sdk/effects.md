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

<br/>
<br/>
<br/>
