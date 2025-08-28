---
title: 'upsert_patient_metadata'
slug: 'example-upsert_patient_metadata'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/upsert_patient_metadata' target='_blank'>View the source</a> for this plugin on GitHub." %}

upsert_patient_metadata
=======================

## Description

Extracts key-value pairs from plan update narratives and stores them as patient metadata.

Parses narrative text for patterns like "key=somekey*value=somevalue" where the separator
can be any non-alphanumeric character. If both key and value are found, creates or updates
the corresponding patient metadata entry.

Triggers on: PLAN_COMMAND__POST_UPDATE events
Effects: PatientMetadata upsert operations

### Important Note!

The CANVAS_MANIFEST.json is used when installing your plugin. Please ensure it
gets updated if you add, remove, or rename protocols.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "upsert_patient_metadata",
    "description": "Edit the description in CANVAS_MANIFEST.json",
    "components": {
        "protocols": [
            {
                "class": "upsert_patient_metadata.protocols.my_protocol:Protocol",
                "description": "A protocol that does xyz...",
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

**Purpose**

This code defines a protocol handler for a Canvas plugin that listens for specific events ("plan command post-update") and parses the accompanying narrative text to extract key-value pairs. These pairs are then stored in the patient's metadata.

**How It Works**

- The class `Protocol` inherits from `BaseHandler` and responds to the `PLAN_COMMAND__POST_UPDATE` event.
- When triggered, it looks for the patient's ID and the narrative text in the event context.
- It uses regular expressions to find patterns like `key=somekey` and `value=somevalue` in the narrative text. The key and value must not include certain separator characters (`*`, `#`, `_`, space).
- If both a key and value are found, it logs an upsert (update or insert) operation and creates a corresponding `PatientMetadata` upsert effect, which will store or update the key-value pair in the patient's metadata.
- If either key or value is missing, it does nothing.

**Key Features**

- **Event-driven**: Only runs after plan command updates, i.e., when new plan narrative text is posted.
- **Flexible Parsing**: Accepts any non-alphanumeric separator between fields; only expects specific "key=" and "value=" patterns.
- **Metadata Management**: Automatically updates or inserts custom patient metadata based on the narrative's content.
- **Logging**: Logs every attempted metadata upsert for traceability.

**Dependencies**

- Uses Canvas SDK effect and handler classes.
- Uses a logger module (assumed to be in the same codebase).
- Relies on Python's `re` for pattern matching within the narrative.

**Typical Use Case**

This handler is ideal for workflows needing structured patient metadata extracted from clinicians' narrative comments, allowing dynamic storage of custom patient attributes with minimal UI interaction.

```python
import re

from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_metadata import PatientMetadata
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from logger import log


class Protocol(BaseHandler):
    """
    Extracts key-value pairs from plan update narratives and stores them as patient metadata.

    Parses narrative text for patterns like "key=somekey*value=somevalue" where the separator
    can be any non-alphanumeric character. If both key and value are found, creates or updates
    the corresponding patient metadata entry.

    Triggers on: PLAN_COMMAND__POST_UPDATE events
    Effects: PatientMetadata upsert operations
    """

    RESPONDS_TO = EventType.Name(EventType.PLAN_COMMAND__POST_UPDATE)

    def compute(self) -> list[Effect]:
        """This method gets called when an event of the type RESPONDS_TO is fired."""
        patient_id = self.context["patient"]["id"]
        fields = self.context.get("fields", {})
        narrative = fields.get("narrative", "")

        key_match = re.search(r"key=([^*#_\s]+)", narrative)
        value_match = re.search(r"value=([^*#_\s]+)", narrative)

        key = key_match.group(1) if key_match else None
        value = value_match.group(1) if value_match else None

        log.info(
            f"Upserting patient metadata for patient {patient_id} with key: {key} and value: {value}"
        )

        if not key or not value:
            return []

        return [PatientMetadata(patient_id=patient_id, key=str(key)).upsert(str(value))]
```

<br/>
<br/>
<br/>
