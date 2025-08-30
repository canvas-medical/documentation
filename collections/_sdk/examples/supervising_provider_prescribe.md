---
title: 'supervising_provider_prescribe'
slug: 'example-supervising_provider_prescribe'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/supervising_provider_prescribe' target='_blank'>View the source</a> for this plugin on GitHub." %}

supervising_provider_prescribe
==============================

## Description

This protocol responds to the PRESCRIBE_COMMAND__POST_ORIGINATE event.

It is used to test whether the supervising provider field is automatically populated
when the Prescribe command is triggered. The protocol reacts to the command's creation
and sets the field accordingly.

The same logic can be tested for Refill and Adjust Prescription commands by updating
the RESPONDS_TO event and the command class.

### Important Note!

The CANVAS_MANIFEST.json is used when installing your plugin. Please ensure it
gets updated if you add, remove, or rename protocols.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1a",
    "name": "supervising_provider_prescribe",
    "description": "This protocol responds to the PRESCRIBE_COMMAND__POST_ORIGINATE event.\n\n    It is used to test whether the supervising provider field is automatically populated\n    when the Prescribe command is triggered. The protocol reacts to the command's creation\n    and sets the field accordingly.\n\n    The same logic can be tested for Refill and Adjust Prescription commands by updating\n    the RESPONDS_TO event and the command class.",
    "components": {
        "protocols": [
            {
                "class": "supervising_provider_prescribe.protocols.my_protocol:Protocol",
                "description": "This protocol responds to the PRESCRIBE_COMMAND__POST_ORIGINATE event.\n\n    It is used to test whether the supervising provider field is automatically populated\n    when the Prescribe command is triggered. The protocol reacts to the command's creation\n    and sets the field accordingly.\n\n    The same logic can be tested for Refill and Adjust Prescription commands by updating\n    the RESPONDS_TO event and the command class.",
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

The code defines a custom protocol for a Canvas Medical plugin. Its main function is to automatically set (or test the auto-population of) the supervising provider field on a newly-created Prescribe command, triggered when a prescription is initiated.

**How It Works**

- Inherits from `BaseProtocol` in the Canvas SDK.
- Listens specifically for the `PRESCRIBE_COMMAND__POST_ORIGINATE` event, which occurs right after a prescription command is originated/created.
- When this event occurs, the protocol’s `compute` method runs.

**Detailed Flow**

1. **Event Subscription**
   - The protocol is set to respond only to the "PrescribeCommand Post Originate" event via the `RESPONDS_TO` class attribute.

2. **Logging**
   - When triggered, the protocol logs information about the event target (i.e., the specific prescription command) and the patient involved.

3. **Fetch Staff**
   - It queries all Staff objects and grabs the first available staff member.
   - If no staff exists, it logs a warning and exits (returns no effects).

4. **Supervising Provider Population**
   - Constructs a `PrescribeCommand` object, passing in the unique ID of the command and setting the `supervising_provider_id` to the found staff member’s ID.

5. **Edit Effect**
   - Calls `.edit()` on the command object. This returns an effect telling Canvas to update the prescription with the supervising provider’s information.

6. **Extensibility**
   - The code comment points out that changing which event and command the protocol responds to will allow similar logic to be applied to other prescription-related actions (like refills or adjustments).

**Use Case**

This is mainly for testing or enforcing workflows where a prescription’s supervising provider must always be set automatically. It’s useful in scenarios where provider oversight is required and should be explicitly logged in the system.

```python
from canvas_sdk.commands import PrescribeCommand
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import Staff
from logger import log


class Protocol(BaseProtocol):
    """
    This protocol responds to the PRESCRIBE_COMMAND__POST_ORIGINATE event.

    It is used to test whether the supervising provider field is automatically populated
    when the Prescribe command is triggered. The protocol reacts to the command's creation
    and sets the field accordingly.

    The same logic can be tested for Refill and Adjust Prescription commands by updating
    the RESPONDS_TO event and the command class.
    """

    RESPONDS_TO = EventType.Name(EventType.PRESCRIBE_COMMAND__POST_ORIGINATE)

    def compute(self) -> list[Effect]:
        """This method gets called when an event of the type RESPONDS_TO is fired."""
        log.info(f"Target {self.target} on patient {self.context['patient']['id']}")

        staff = Staff.objects.first()
        if not staff:
            log.warning("No staff found — skipping update.")
            return []

        prescription = PrescribeCommand(
            command_uuid=str(self.target),
            supervising_provider_id=staff.id,
        )

        return [prescription.edit()]
```

<br/>
<br/>
<br/>
