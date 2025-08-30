---
title: 'patient_portal_search_appointments_slots_plugin'
slug: 'example-patient_portal_search_appointments_slots_plugin'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_portal_search_appointments_slots_plugin' target='_blank'>View the source</a> for this plugin on GitHub." %}

patient_portal_search_appointments_slots_plugin
=========================================

## Description

This plugin is triggered when a patient searches for available appointments slots for the care team
members, mutating the response to exclude any provider that has no slots available for the search criteria.

### Events

This plugin responds to the following events:

- `PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH`

### Effects

This plugin has the following effects:

- `PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH_RESULTS`


### Important Note!

The CANVAS_MANIFEST.json is used when installing your plugin. Please ensure it
gets updated if you add, remove, or rename protocols.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "patient_portal_search_appointments_slots_plugin",
    "description": "Edit the description in CANVAS_MANIFEST.json",
    "components": {
        "protocols": [
            {
                "class": "patient_portal_search_appointments_slots_plugin.handlers.search_appointments_slots_handler:SearchAppointmentsSlotsHandler",
                "description": "",
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

## handlers/

### __init__.py

This file is empty.
### search_appointments_slots_handler.py

**Purpose and Context**

The code defines a handler in a Canvas Medical plugin for responding to search requests for available appointment slots in the patient portal. It uses the Canvas SDK.

**Class and Event Registration**

The core of the file is a class, SearchAppointmentsSlotsHandler, which inherits from BaseHandler. It is registered to respond only to a specific event: PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH. This event is triggered when a user searches for available appointment slots.

**Primary Logic (compute method)**

- The compute method retrieves a JSON object from self.context named "slots_by_provider". This object is expected to contain available appointment slots, grouped by provider.
- If no slots are found (i.e., slots_by_provider is empty or missing), the handler responds with a null payload.
- Otherwise, it filters the slots to only include providers who have at least one non-empty list of available slots for some date.
- The filtered results are wrapped in a new dictionary under the key "slots_by_provider" and returned as the response.

**Response Creation**

- The _respond_with helper method constructs an Effect, which packages the response payload for Canvas.
- The effect type is PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH_RESULTS, signaling to Canvas that appointment slot search results are being returned.
- The payload (possibly filtered) is converted to a JSON string and attached to the Effect.

**Summary**

The handler listens for appointment slot search events in the patient portal, processes and filters provider slot data to remove providers with no availability, then responds with the filtered set of available slots (or null if none exist) in the format expected by Canvas Medical.

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


# Inherit from BaseHandler to properly get registered for events
class SearchAppointmentsSlotsHandler(BaseHandler):
    """Handler responsible for processing search appointments slots events."""

    # Name the event type you wish to run in response to
    RESPONDS_TO = EventType.Name(
        EventType.PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH,
    )

    def compute(self) -> list[Effect]:
        """This method gets called when an event of the type RESPONDS_TO is fired."""
        slots_by_provider = json.loads(self.context.get("slots_by_provider") or "{}")

        if not slots_by_provider:
            return [self._respond_with(None)]

        filtered = {
            provider: dates
            for provider, dates in slots_by_provider.items()
            if any(slots for slots in dates.values())
        }

        payload = {
            "slots_by_provider": filtered
        }

        return [
            self._respond_with(payload),
        ]

    def _respond_with(self, payload: dict) -> Effect:
        """Helper method to create a response effect."""
        return Effect(
            type=EffectType.PATIENT_PORTAL__APPOINTMENTS__SLOTS__POST_SEARCH_RESULTS,
            payload=json.dumps(payload),
        )
```

<br/>
<br/>
<br/>
