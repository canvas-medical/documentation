---
title: 'Upsert Patient Metadata'
slug: 'example-upsert_patient_metadata'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/upsert_patient_metadata' target='_blank'>View the source</a> for this plugin on GitHub." %}

This plugin showcases how to store patient metadata key/value pairs from a plugin using the Canvas SDK.

In this example, we extract key-value pairs from a plan command's narrative and store them as patient metadata.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "upsert_patient_metadata",
    "description": "Edit the description in CANVAS_MANIFEST.json",
    "components": {
        "handlers": [
            {
                "class": "upsert_patient_metadata.handlers.my_handler:MyHandler",
                "description": "A handler that does xyz..."
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "variables": [],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## handlers/

### my_handler.py

This file defines a Canvas plugin handler that uses the update of a plan command as an excuse to trigger. When a user updates a plan command and includes certain key-value data in the narrative, this handler extracts that information and saves it as patient metadata.

**Narrative Parsing**

The handler retrieves the narrative text from the event context. It uses regular expressions to look for patterns of the form:

- `key=somekey`
- `value=somevalue`

The separator between key/value and their contents can be any character except alphanumerics, underscores, asterisks, hashes, or whitespace. For example, `key=blood_pressure*value=120/80`.

**Action Taken**

If both a key and value are found in the narrative:

- It logs an informational message including the patient id, key, and value.
- It returns a list containing one Effect: an upsert (create or update) of patient metadata (via PatientMetadata) for that patient, saving the found key and value.

If either the key or value is missing, no action is performed.

```python
import re

from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_metadata import PatientMetadata
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from logger import log


class MyHandler(BaseHandler):
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
