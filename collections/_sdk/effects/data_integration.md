---
title: "Data Integration"
slug: "effect-data-integration"
excerpt: "Manage documents in the Data Integration queue."
hidden: false
---

Plugins can automate triage of inbound clinical documents in the [Data Integration queue](/sdk/data-integration-task/) — lab reports, imaging reports, faxes, and other uploaded files awaiting staff review before they're attached to a patient's chart. The effects below let a plugin categorize a document, link it to a patient, prefill template field values, assign a reviewer, mark it as junk, or unlink it from a patient.

## Assigning a Reviewer

To assign a staff member as the reviewer for a document in the Data Integration queue, import the `AssignDocumentReviewer` class from `canvas_sdk.effects.data_integration` and create an instance of it.

| Attribute     |          | Type   | Description                                                                              |
|---------------|----------|--------|------------------------------------------------------------------------------------------|
| `document_id` | required | string | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document. |
| `reviewer_id` | required | string | The `id` of the [Staff](/sdk/data-staff/#staff) member to assign as reviewer.            |
| `annotations` | optional | list   | List of annotations for display in the UI. See [Annotations](#annotations).              |

An example of assigning a reviewer. Annotations render as colored badges next to the reviewer field in the Data Integration UI — useful for surfacing why the plugin chose this reviewer:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import AssignDocumentReviewer
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class AssignReviewerHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        return [
            AssignDocumentReviewer(
                document_id=self.event.target.id,
                reviewer_id="4150cd20de8a470aa570a852859ac87e",
                annotations=[
                    {"text": "Team lead", "color": "#4CAF50"},
                    {"text": "Auto-assigned", "color": "#FF9800"},
                ],
            ).apply()
        ]
```

## Categorizing a Document

To categorize a document in the Data Integration queue into a specific document type, import the `CategorizeDocument` class from `canvas_sdk.effects.data_integration` and create an instance of it.

| Attribute         |          | Type                          | Description                                                                 |
|-------------------|----------|-------------------------------|-----------------------------------------------------------------------------|
| `document_id`     | required | string                        | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document to categorize.                       |
| `document_type`   | required | [DocumentType](#documenttype) | Document type information for categorizing the document.                    |
| `annotations`     | optional | list                          | List of annotations for display in the UI. See [Annotations](#annotations). |

### DocumentType

The `document_type` parameter is a dictionary with the following fields:

| Key             |          | Type   | Description                                                                                                                                       |
|-----------------|----------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `key`           | required | string | The unique key identifying the document type.                                                                                                     |
| `name`          | required | string | The human-readable name of the document type.                                                                                                     |
| `report_type`   | required | string | The type of report. Must be `"CLINICAL"` or `"ADMINISTRATIVE"`.                                                                                   |
| `template_type` | optional | string | The template type. Can be `"LabReportTemplate"`, `"ImagingReportTemplate"`, `"SpecialtyReportTemplate"`, or `null` for administrative documents.  |

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

## Linking a Document to a Patient

To link a document in the Data Integration queue to a patient, import the `LinkDocumentToPatient` class from `canvas_sdk.effects.data_integration` and create an instance of it. The plugin is responsible for matching the patient and supplying their key — the interpreter does not search for matching patients itself.

| Attribute     |          | Type   | Description                                                                 |
|---------------|----------|--------|-----------------------------------------------------------------------------|
| `document_id` | required | string | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document.                                     |
| `patient_key` | required | string | The `id` of the [Patient](/sdk/data-patient/#patient) to link the document to, resolved by the plugin's matching logic. |
| `annotations` | optional | list   | List of annotations for display in the UI. See [Annotations](#annotations). |

An example of linking a document to a patient:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import LinkDocumentToPatient
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.patient import Patient


class LinkDocumentHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        # Plugin-specific matching logic resolves the patient
        patient = Patient.objects.filter(...).first()
        if not patient:
            return []

        return [
            LinkDocumentToPatient(
                document_id=self.event.target.id,
                patient_key=patient.id,
            ).apply()
        ]
```

## Marking a Document as Junk

To mark a document in the Data Integration queue as junk (spam), import the `JunkDocument` class and create an instance of it.

| Attribute     |          | Type   | Description                                            |
|---------------|----------|--------|--------------------------------------------------------|
| `document_id` | required | string | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document to mark as junk |

An example of marking a document as junk:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import JunkDocument
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class JunkDocumentHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        document_id = self.event.target.id

        junk_document = JunkDocument(
            document_id=document_id,
        )

        return [junk_document.apply()]
```

## Prefilling Document Fields

To prefill template field values on a document in the Data Integration queue, import the `PrefillDocumentFields` class from `canvas_sdk.effects.data_integration` and create an instance of it.

> The wire-level effect type for this class is `UPDATE_DOCUMENT_FIELDS`, which is what appears in event logs and the [effects table](/sdk/effects/#data-integration). The class name is `PrefillDocumentFields`.

| Attribute     |          | Type                                      | Description                                                                 |
|---------------|----------|-------------------------------------------|-----------------------------------------------------------------------------|
| `document_id` | required | string                                    | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document.                                     |
| `templates`   | required | list[[PrefillTemplate](#prefilltemplate)] | One or more templates to prefill. Must contain at least one entry.          |
| `annotations` | optional | list                                      | List of annotations for display in the UI. See [Annotations](#annotations). |

### PrefillTemplate

A `PrefillTemplate` is a dictionary with the following keys:

| Key             |          | Type                                                             | Description                       |
|-----------------|----------|------------------------------------------------------------------|-----------------------------------|
| `template_id`   | required | int                                                              | The template's database ID.       |
| `template_name` | required | string                                                           | The human-readable template name. |
| `fields`        | required | dict[str, [PrefillDocumentFieldData](#prefilldocumentfielddata)] | Map of field name to field data.  |

### PrefillDocumentFieldData

A `PrefillDocumentFieldData` is a dictionary with the following keys:

| Key               |          | Type   | Description                                                       |
|-------------------|----------|--------|-------------------------------------------------------------------|
| `value`           | required | string | The field value.                                                  |
| `unit`            | optional | string | Unit of measurement.                                              |
| `reference_range` | optional | string | Reference range for the value.                                    |
| `abnormal`        | optional | bool   | Whether the value is abnormal.                                    |
| `annotations`     | optional | list   | Per-field annotations. Same shape as [Annotations](#annotations). |

An example of prefilling a lab report template:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import PrefillDocumentFields
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class PrefillLabReportHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        return [
            PrefillDocumentFields(
                document_id=self.event.target.id,
                templates=[
                    {
                        "template_id": 42,
                        "template_name": "CBC Panel",
                        "fields": {
                            "Hemoglobin": {
                                "value": "13.5",
                                "unit": "g/dL",
                                "reference_range": "12.0-15.5",
                                "abnormal": False,
                            },
                            "WBC": {
                                "value": "11.2",
                                "unit": "10^3/uL",
                                "reference_range": "4.5-11.0",
                                "abnormal": True,
                            },
                        },
                    },
                ],
            ).apply()
        ]
```

## Removing a Document from a Patient

To remove or unlink a document from a patient in the Data Integration queue, import the `RemoveDocumentFromPatient` class and create an instance of it.

| Attribute     |          | Type   | Description                                                                                                       |
|---------------|----------|--------|-------------------------------------------------------------------------------------------------------------------|
| `document_id` | required | string | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document to unlink from the patient.                                                |
| `patient_id`  | optional | string | The `id` of the [Patient](/sdk/data-patient/#patient) whose link to remove. If not provided, removes the current patient association. |

An example of removing a document from a patient:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import RemoveDocumentFromPatient
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class RemoveDocumentHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_LINKED_TO_PATIENT)

    def compute(self) -> list[Effect]:
        document_id = self.event.target.id

        remove_document = RemoveDocumentFromPatient(
            document_id=document_id,
        )

        return [remove_document.apply()]
```

If a document could be linked to multiple patients, you can specify which patient to unlink:

```python
from canvas_sdk.effects.data_integration import RemoveDocumentFromPatient

remove_document = RemoveDocumentFromPatient(
    document_id="d2194110-5c9a-4842-8733-ef09ea5ead11",
    patient_id="patient-uuid-here",
)
```

## Annotations

The `annotations` field on any data integration effect accepts a list of dictionaries with the following keys:

| Key     | Type   | Description                                      |
|---------|--------|--------------------------------------------------|
| `text`  | string | The annotation text to display (e.g., "AI 95%"). |
| `color` | string | Hex color code (e.g., "#4CAF50" for green).      |

<br/>
<br/>
<br/>
