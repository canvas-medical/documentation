---
title: "Customize Search Results"
last_modified_at: "2024-05-17"
guide_for:
- /sdk/events/
- /sdk/effects/
- /sdk/protocols/
---
In a typical visit note, it's common for clinicians to make 20, 30, even 50 or more selections from structured terminologies with commands like Diagnose, Prescribe, Family History, and many more. You can help clinicians make faster and more accurate selections with Canvas plugins. Write simple plugin code to apply custom filtering, sorting, and search result annotations in real time with near zero latency.

This search modification can help clinicians:

- Choose the most appropriate medication that is also covered by insurance
- Prioritize in-network specialists
- Consider appropriate risk adjustment factors when selecting diagnosis codes

Canvas supports modifying search results in [all refactored commands](/product-updates/commands-module/#progress).

{% include alert.html type="info" content=" <b>Plugins are new.</b> If you are interested in enabling plugins for your Canvas instance, please reach out to <a href='mailto:support@canvasmedical.com'>support@canvasmedical.com</a>)." %}

First, we'll show you a complete example of customizing the search results for
choosing a medication in a Medication Statement command, then we'll break it
down piece by piece so you can adapt the example to your own needs.

## The Complete Example

This example checks for the presence of a particular medication in the search
results and, if present, annotates that medication option with additional
information and adjusts its position to the top of the search results.

For reference, here's the difference in behavior with the plugin inactive vs
active:

**Inactive (normal behavior):**

![With the plugin inactive, the results are unaltered](/assets/images/customize-search-results/plugin-inactive.png){: style='width: 400px'}

**Active (modified behavior):**

![With the plugin active, the preferred result is listed first, and with additional context](/assets/images/customize-search-results/plugin-active.png){: style='width: 400px'}


Here's the code in its entirety:

```python
import json

from canvas_sdk.events import EventType
from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.protocols import BaseProtocol


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.MEDICATION_STATEMENT__MEDICATION__POST_SEARCH)

    def compute(self):
        results = self.context.get("results")

        if results is None:
            return [Effect(type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS, payload=json.dumps(None))]

        post_processed_results = []
        for result in results:
            should_float_to_top = False
            for coding in result.get("extra", {}).get("coding", []):
                if (
                    coding.get("code") == 554704
                    and coding.get("system") == "http://www.fdbhealth.com/"
                ):
                    if result.get("annotations") is None:
                        result["annotations"] = []
                    result["annotations"].append("Kirkland Signature")
                    should_float_to_top = True
            if should_float_to_top:
                post_processed_results.insert(0, result)
            else:
                post_processed_results.append(result)

        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(post_processed_results),
            )
        ]
```

## Anatomy of the Example
This code can be broken down into the following sections:
- Register interest in the correct search event
- Decide whether to make any changes
- Loop through the results, making modifications as appropriate
- Return the modified results as a properly typed effect

### Register interest in the correct search event
```python
class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.MEDICATION_STATEMENT__MEDICATION__POST_SEARCH)

    def compute(self):
        results = self.context.get("results")
```

The class inherits from `BaseProtocol`, which clues the plugin-runner into
registering your code as interested in the event or events listed in the
`RESPONDS_TO` class constant. We only specify one event here,
`MEDICATION_STATEMENT__MEDICATION__POST_SEARCH`, but you could make this value
a list to fire on multiple events. The event we've chosen to listen for can be
read backwards to understand when it fires. This event is emitted after ("_post_") the
normal _search_ results are found for the _medication_ autocomplete field of the
_medication statement_ command. This event comes with a context that contains the
search results that would be served to the user if there were no
modifications.

### Decide whether to make any changes
```python
        if results is None:
            return [Effect(type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS, payload=json.dumps(None))]
```

If the value of the results `is None`, we bail out early. There is a subtle
difference between results of `None` and an empty result set (`[]`). Results
being `None` means "make no changes, present the results without modification",
whereas an empty result set means "present no options to the user".

### Loop through the results, making modifications as appropriate
```python
        post_processed_results = []
        for result in results:
            should_float_to_top = False
            for coding in result.get("extra", {}).get("coding", []):
                if (
                    coding.get("code") == 554704
                    and coding.get("system") == "http://www.fdbhealth.com/"
                ):
                    if result.get("annotations") is None:
                        result["annotations"] = []
                    result["annotations"].append("Kirkland Signature")
                    should_float_to_top = True
            if should_float_to_top:
                post_processed_results.insert(0, result)
            else:
                post_processed_results.append(result)
```

In this block of code, we create a new list named `post_processed_results` to
hold our modified result set. We then loop through each result in the
unmodified results set, and check to see if the current medication result matches our
chosen criteria (FDB code 554704).

If it does match, we first check to see if any
annotations already exist and initialize the annotations list if needed. We
then append our chosen annotation to the result's annotation list and flag it
as needing to be floated to the top (we had defaulted it to not be floated
earlier on).

Finally, we add the result to our parallel list, `post_processed_results`. If
it matched and was marked as being floated to the top, we insert it into the
list at position 0. If it did not match, we append the result to the end of
the list.

### Return the modified results as a properly typed effect
```python
        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(post_processed_results),
            )
        ]
```

With our list of modified results in place, we just need to return an effect
of type `AUTOCOMPLETE_SEARCH_RESULTS` with our modified list as the payload.

The dropdown of options presented to the user now reflects our modifications!

## Watch Me Build It

<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/d3b696bdb482401c82aad2a2347c11ea?sid=07417cab-cb22-4165-ba16-2a2dcc2b3ce5" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div> 

<br />
<br />
<br />
