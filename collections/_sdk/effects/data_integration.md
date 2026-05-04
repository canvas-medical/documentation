---
title: "Data Integration"
slug: "effect-data-integration"
excerpt: "Manage documents in the Data Integration queue."
hidden: false
---

The Canvas SDK allows you to manage documents in the Data Integration queue.

## Categorizing a Document

To categorize a document in the Data Integration queue into a specific document type, import the `CategorizeDocument` class from `canvas_sdk.effects.data_integration` and create an instance of it.

| Attribute       |          | Type                            | Description                                                        |
|-----------------|----------|---------------------------------|--------------------------------------------------------------------|
| document_id     | required | string                          | The ID of the IntegrationTask document to categorize.              |
| document_type   | required | [DocumentType](#documenttype)   | Document type information for categorizing the document.           |
| annotations     | optional | list                            | List of annotations for display in the UI. See [Annotations](#annotations). |
| source_protocol | optional | string                          | Identifier for the protocol/plugin that generated this effect.     |

### DocumentType

The `document_type` parameter is a dictionary with the following fields:

| Key           |          | Type   | Description                                                                                                                                        |
|---------------|----------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| key           | required | string | The unique key identifying the document type.                                                                                                      |
| name          | required | string | The human-readable name of the document type.                                                                                                      |
| report_type   | required | string | The type of report. Must be `"CLINICAL"` or `"ADMINISTRATIVE"`.                                                                                    |
| template_type | optional | string | The template type. Can be `"LabReportTemplate"`, `"ImagingReportTemplate"`, `"SpecialtyReportTemplate"`, or `null` for administrative documents.  |

### Annotations

The `annotations` parameter accepts a list of dictionaries with the following keys:

| Key   | Type   | Description                                      |
|-------|--------|--------------------------------------------------|
| text  | string | The annotation text to display (e.g., "AI 95%"). |
| color | string | Hex color code (e.g., "#4CAF50" for green).      |

An example of categorizing a clinical document:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import CategorizeDocument
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class CategorizeDocumentHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        document_id = self.event.context.get("document", {}).get("id")

        categorize = CategorizeDocument(
            document_id=document_id,
            document_type={
                "key": "cbc-panel",
                "name": "Complete Blood Count",
                "report_type": "CLINICAL",
                "template_type": "LabReportTemplate",
            },
        )

        return [categorize.apply()]
```

An example of categorizing an administrative document:

```python
from canvas_sdk.effects.data_integration import CategorizeDocument

categorize = CategorizeDocument(
    document_id="d2194110-5c9a-4842-8733-ef09ea5ead11",
    document_type={
        "key": "insurance-eob",
        "name": "Insurance Explanation of Benefits",
        "report_type": "ADMINISTRATIVE",
        "template_type": None,
    },
)
```

An example of categorizing with annotations and source protocol:

```python
from canvas_sdk.effects.data_integration import CategorizeDocument

categorize = CategorizeDocument(
    document_id="d2194110-5c9a-4842-8733-ef09ea5ead11",
    document_type={
        "key": "cbc-panel",
        "name": "Complete Blood Count",
        "report_type": "CLINICAL",
        "template_type": "LabReportTemplate",
    },
    annotations=[
        {"text": "AI Categorized", "color": "#4CAF50"},
    ],
    source_protocol="my_categorization_plugin",
)
```

<br/>
<br/>
<br/>
