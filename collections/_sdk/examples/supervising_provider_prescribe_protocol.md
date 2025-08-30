---
title: 'supervising_provider_prescribe_protocol'
slug: 'example-supervising_provider_prescribe_protocol'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/supervising_provider_prescribe_protocol' target='_blank'>View the source</a> for this plugin on GitHub." %}

supervising_provider_prescribe_protocol
=======================================

## Description

This protocol responds to the NOTE_STATE_CHANGE_EVENT_CREATED event.

It inserts a ProtocolCard containing a recommended Prescribe command. When the user triggers
this command, the supervising provider field will be automatically populated.

This plugin is primarily used to test and validate that the supervising provider is correctly
set during command initialization from a protocol.

### Important Note!

The CANVAS_MANIFEST.json is used when installing your plugin. Please ensure it
gets updated if you add, remove, or rename protocols.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1a",
    "name": "supervising_provider_prescribe_protocol",
    "description": "This protocol responds to the NOTE_STATE_CHANGE_EVENT_CREATED event.\n\n    It inserts a ProtocolCard containing a recommended Prescribe command. When the user triggers\n    this command, the supervising provider field will be automatically populated.\n\n    This plugin is primarily used to test and validate that the supervising provider is correctly\n    set during command initialization from a protocol.",
    "components": {
        "protocols": [
            {
                "class": "supervising_provider_prescribe_protocol.protocols.my_protocol:Protocol",
                "description": "This protocol responds to the NOTE_STATE_CHANGE_EVENT_CREATED event.\n\n    It inserts a ProtocolCard containing a recommended Prescribe command. When the user triggers\n    this command, the supervising provider field will be automatically populated.\n\n    This plugin is primarily used to test and validate that the supervising provider is correctly\n    set during command initialization from a protocol.",
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

## __init__.py

This file is empty.
## protocols/

### __init__.py

This file is empty.
### my_protocol.py

**Summary**

This file defines a Canvas plugin protocol that is triggered by the creation of a new note (the `NOTE_STATE_CHANGE_EVENT_CREATED` event). When triggered, it creates a protocol card containing a recommendation to run a prescription command, automatically setting the supervising provider.

**Key Functionality**

- Listens for the "note created" event in Canvas.
- When the event occurs, logs the note and patient IDs.
- Retrieves the first `Staff` member from the database.
    - If no staff member is found, logs a warning and does nothing.
- Constructs a `ProtocolCard` for the patient, which includes:
    - A recommendation featuring the `PrescribeCommand`.
    - The `supervising_provider_id` is set to the retrieved staff member's ID.
    - The recommendation is presented as a "Prescribe" button with an explanatory title.
- Returns the card as an `Effect`, meaning it will be rendered to the user in the Canvas UI.

**Purpose**

The main purpose is to test/validate that when the protocol recommends prescribing, the supervising provider field is automatically and correctly set during command initialization from the protocol.

**Logging**

The code includes logging for both informative (note and patient IDs) and warning (if no staff found) scenarios for easier debugging and validation.

**User Interaction**

- When the protocol is triggered, a "Prescribe" button will appear for the user.
- If the user accepts the recommendation, the supervising provider is pre-populated.

**Usage Context**

- Mainly intended for test and validation purposes regarding the supervising provider functionality within the workflow commands of Canvas.

```python
from canvas_sdk.commands import PrescribeCommand
from canvas_sdk.effects import Effect
from canvas_sdk.effects.protocol_card import ProtocolCard
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import Staff
from logger import log


class Protocol(BaseProtocol):
    """
    This protocol responds to the NOTE_STATE_CHANGE_EVENT_CREATED event.

    It inserts a ProtocolCard containing a recommended Prescribe command. When the user triggers
    this command, the supervising provider field will be automatically populated.

    This plugin is primarily used to test and validate that the supervising provider is correctly
    set during command initialization from a protocol.
    """

    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def compute(self) -> list[Effect]:
        """This method gets called when an event of the type RESPONDS_TO is fired."""
        log.info(f"Note {self.context['note_id']} on patient {self.context['patient_id']}")

        protocol_card = ProtocolCard(
            patient_id=self.context["patient_id"],
            key="test-supervising-provider-prescribe",
            title="Test Prescribe Command with Supervising Provider",
        )

        staff = Staff.objects.first()
        if not staff:
            log.warning("No staff found — skipping update.")
            return []

        prescribe_command = PrescribeCommand(
            supervising_provider_id=staff.id,
        )
        protocol_card.recommendations.append(
            prescribe_command.recommend(
                title="This inserts a prescribe command", button="Prescribe"
            )
        )

        return [protocol_card.apply()]
```

<br/>
<br/>
<br/>
