---
title: "Data Integration"
slug: "effect-data-integration"
excerpt: "Manage documents in the Data Integration queue."
hidden: false
---

The Canvas SDK allows you to manage documents in the Data Integration queue.

## Linking a Document to a Patient

To link a document in the Data Integration queue to a patient, import the `LinkDocumentToPatient` class and create an instance of it. The plugin is responsible for finding/matching the patient and providing their key.

| Attribute       |          | Type          | Description                                                                                      |
|-----------------|----------|---------------|--------------------------------------------------------------------------------------------------|
| document_id     | required | string        | The ID of the IntegrationTask document to link.                                                  |
| patient_key     | required | string        | The patient's key.                                                                               |
| annotations     | optional | list          | List of annotations for display in the UI. See [Annotations](#annotations).                      |
| source_protocol | optional | string        | Protocol/plugin identifier (e.g., "llm_v1").                                                     |

### Annotations

The `annotations` parameter accepts a list of dictionaries with the following keys:

| Key   | Type   | Description                                           |
|-------|--------|-------------------------------------------------------|
| text  | string | The annotation text to display (e.g., "AI 95%").      |
| color | string | Hex color code (e.g., "#4CAF50" for green).           |

An example of linking a document to a patient:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import LinkDocumentToPatient
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

from canvas_sdk.v1.data.patient import Patient


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        document_id = self.event.context.get("document", {}).get("id")
        patient = Patient.objects.first()

        link_document = LinkDocumentToPatient(
            document_id=document_id,
            patient_key=str(patient.id),
        )

        return [link_document.apply()]
```

An example of linking a document with annotations:

```python
from canvas_sdk.effects.data_integration import LinkDocumentToPatient

link_document = LinkDocumentToPatient(
    document_id="d2194110-5c9a-4842-8733-ef09ea5ead11",
    patient_key="8d84776879de49518a4bc3bb81d96dd4",
    annotations=[
        {"text": "AI 95%", "color": "#4CAF50"},
        {"text": "Auto-linked", "color": "#2196F3"},
    ],
    source_protocol="llm_v1",
)
```

<br/>
<br/>
<br/>
