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

### Effect Types

The following effects are available to be applied in Canvas.

| Effect | Description |
| ----- | ----------- |
| AUTOCOMPLETE_SEARCH_RESULTS | Can be used to modify search results by re-ordering or adding text annotations to individual result records. To see how you can put this to use, check out [this guide](/guides/customize-search-results/). |
| ADD_PLAN_COMMAND | Can be used to insert a plan command into a note. |
| ADD_BANNER_ALERT | Can be used to add a banner alert to a patient's chart. |
| REMOVE_BANNER_ALERT | Can be used to remove a banner alert from a patient's chart. |

<br/>
<br/>
<br/>
