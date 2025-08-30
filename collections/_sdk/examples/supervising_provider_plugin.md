---
title: 'supervising_provider_plugin'
slug: 'example-supervising_provider_plugin'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/supervising_provider_plugin' target='_blank'>View the source</a> for this plugin on GitHub." %}

supervising_provider_plugin
===========================

## Description

Add annotations to the supervising provider dropdown in Prescribe, Refill, and Adjust Prescription Commands

### Important Note!

The CANVAS_MANIFEST.json is used when installing your plugin. Please ensure it
gets updated if you add, remove, or rename protocols.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1a",
    "name": "supervising_provider_plugin",
    "description": "Add annotations to the supervising provider dropdown in Prescribe, Refill, and Adjust Prescription Commands",
    "components": {
        "protocols": [
            {
                "class": "supervising_provider_plugin.protocols.my_protocol:Protocol",
                "description": "Add annotations to the supervising provider dropdown in Prescribe, Refill, and Adjust Prescription Commands",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": [],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## protocols/

### __init__.py

This file is empty.
### my_protocol.py

**Summary**

This file defines a custom protocol for a Canvas Medical plugin, designed to modify the behavior of search results related to supervising providers in prescription workflows. It logs activity, post-processes search results, and adds annotations when appropriate.

**RESPONDS_TO Configuration**

The protocol listens to several specific Canvas event types associated with searching for supervising providers:
- PRESCRIBE__SUPERVISING_PROVIDER__PRE_SEARCH
- PRESCRIBE__SUPERVISING_PROVIDER__POST_SEARCH
- REFILL__SUPERVISING_PROVIDER__PRE_SEARCH
- REFILL__SUPERVISING_PROVIDER__POST_SEARCH
- ADJUST_PRESCRIPTION__SUPERVISING_PROVIDER__PRE_SEARCH
- ADJUST_PRESCRIPTION__SUPERVISING_PROVIDER__POST_SEARCH

**Core Functionality (`compute` method)**

- When any of those events are fired, the `compute` method is executed.
- It first logs a narrative string indicating that the protocol was triggered.
- It retrieves the search results from the protocol's context.

**Results Handling**

- If no results are found, it returns an autocomplete effect with a payload of `None`.
- If results exist:
    - For each result:
        - It looks up the corresponding `Staff` object using the database ID.
        - If the staff member has an `spi_number`, it adds an annotation "SPI: <spi_number>" to that result.
        - It logs the processed result.
    - It then returns an autocomplete effect containing the post-processed result list as a JSON payload.

**Logging**

- There is integrated logging at both the narrative and per-result level for auditing or debugging purposes.

**External Dependencies**

- Uses the Canvas SDK's effects, events, and staff data access.
- Relies on a custom logging utility (`logger.log`).

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data.staff import Staff
from logger import log


class Protocol(BaseProtocol):
    """You should put a helpful description of this protocol's behavior here."""

    RESPONDS_TO = [
        EventType.Name(EventType.PRESCRIBE__SUPERVISING_PROVIDER__POST_SEARCH),
        EventType.Name(EventType.PRESCRIBE__SUPERVISING_PROVIDER__PRE_SEARCH),
        EventType.Name(EventType.REFILL__SUPERVISING_PROVIDER__POST_SEARCH),
        EventType.Name(EventType.REFILL__SUPERVISING_PROVIDER__PRE_SEARCH),
        EventType.Name(EventType.ADJUST_PRESCRIPTION__SUPERVISING_PROVIDER__POST_SEARCH),
        EventType.Name(EventType.ADJUST_PRESCRIPTION__SUPERVISING_PROVIDER__PRE_SEARCH),
    ]

    NARRATIVE_STRING = "I was inserted from my supervising provider plugin's protocol."

    def compute(self) -> list[Effect]:
        """This method gets called when an event of the type RESPONDS_TO is fired."""
        log.info(self.NARRATIVE_STRING)

        results = self.context.get("results")

        if results is None:
            return [Effect(type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS, payload=json.dumps(None))]

        post_processed_results = []
        for result in results:
            staff = Staff.objects.get(dbid=result["value"])
            if staff.spi_number:
                result["annotations"] = [f"SPI: {staff.spi_number}"]
            log.info(result)
            post_processed_results.append(result)

        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(post_processed_results),
            )
        ]
```

<br/>
<br/>
<br/>
