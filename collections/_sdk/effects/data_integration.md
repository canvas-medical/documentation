---
title: "Data Integration"
slug: "effect-data-integration"
excerpt: "Manage documents in the Data Integration queue."
hidden: false
---

Plugins can automate triage of inbound clinical documents in the [Data Integration queue](/sdk/data-integration-task/) — lab reports, imaging reports, faxes, clinical and administrative documents, and other uploaded files awaiting staff review before they're attached to a patient's chart.

Most of these effects work by writing a **prefill suggestion** to the IntegrationTask. The Data Integration UI surfaces that suggestion as a pre-populated value in the staff member's review form — the suggested patient, document type, template values, or reviewer assignment — along with optional [annotation](#annotations) badges. A staff member still reviews and commits the change; the plugin doesn't directly mutate the IntegrationTask.

The exceptions are `JunkDocument` and `RemoveDocumentFromPatient`, which act on the IntegrationTask's status or patient link immediately without writing a prefill.

## Assigning a Reviewer

To assign a staff member or team as the reviewer for a document in the Data Integration queue, import the `AssignDocumentReviewer` class from `canvas_sdk.effects.data_integration` and create an instance of it.

| Attribute     |          | Type                      | Description                                                                              |
|---------------|----------|---------------------------|------------------------------------------------------------------------------------------|
| `document_id` | required | string                    | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document. |
| `reviewer_id` | optional | string                    | The `id` of the [Staff](/sdk/data-staff/#staff) member to assign as reviewer.            |
| `team_id`     | optional | string                    | The `id` of the [Team](/sdk/data-team/#team) to assign as reviewer.                      |
| `review_mode` | optional | [ReviewMode](#reviewmode) | Review mode. Defaults to `ReviewMode.REVIEW_REQUIRED`.                                   |
| `annotations` | optional | list                      | List of annotations for display in the UI. See [Annotations](#annotations).              |

Supply either `reviewer_id` or `team_id`, not both. If both are supplied, the staff reviewer is used and the team is ignored when the Data Integration UI pre-populates the reviewer field. Supplying neither makes the effect a no-op.

### ReviewMode

| Value                                  | Description                             |
|----------------------------------------|-----------------------------------------|
| `ReviewMode.REVIEW_REQUIRED` (default) | Document requires explicit review.      |
| `ReviewMode.ALREADY_REVIEWED`          | Document is marked as already reviewed. |
| `ReviewMode.REVIEW_NOT_REQUIRED`       | Document does not require review.       |

An example of assigning a staff reviewer. Annotations render as colored badges next to the reviewer field in the Data Integration UI — useful for surfacing why the plugin chose this reviewer:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import AssignDocumentReviewer, ReviewMode
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class AssignReviewerHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        return [
            AssignDocumentReviewer(
                document_id=self.event.target.id,
                reviewer_id="4150cd20de8a470aa570a852859ac87e",
                review_mode=ReviewMode.ALREADY_REVIEWED,
                annotations=[
                    {"text": "Team lead", "color": "#4CAF50"},
                    {"text": "Auto-assigned", "color": "#FF9800"},
                ],
            ).apply()
        ]
```

An example of assigning a team instead of an individual reviewer:

```python
from canvas_sdk.effects.data_integration import AssignDocumentReviewer

assign_reviewer = AssignDocumentReviewer(
    document_id="d2194110-5c9a-4842-8733-ef09ea5ead11",
    team_id="3f8a2e1c-9b4d-4f5a-8c7e-1d2b3a4c5d6e",
    annotations=[
        {"text": "Routed to Coding team", "color": "#2196F3"},
    ],
)
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

| Key             |          | Type            | Description                                                                                                                                       |
|-----------------|----------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `key`           | required | string          | The unique key identifying the document type. Must match a key from the [Supported Document Types](#supported-document-types) table below.        |
| `name`          | required | string          | The human-readable name of the document type. Should match the catalog's `Name` for that key.                                                     |
| `report_type`   | required | string          | The type of report. Must be `"CLINICAL"` or `"ADMINISTRATIVE"`.                                                                                   |
| `template_type` | required | string \| null  | Must be `"LabReportTemplate"`, `"ImagingReportTemplate"`, `"SpecialtyReportTemplate"`, or `null`.                                                  |

### Supported Document Types

Canvas's built-in document type catalog. Use the `Key` value in your `document_type` dict; the other columns show the catalog's `report_type` and the matching parse template (when applicable).

| Name                                                  | Key                                | Report Type    | Template Type           |
|-------------------------------------------------------|------------------------------------|----------------|-------------------------|
| Advance Beneficiary Notice                            | `5375e6ae238e41b4972717174be99d10` | ADMINISTRATIVE | `null`                  |
| Advance Directive / Living Will                       | `1d5a4821140dab935e90d9d73bfd7a35` | ADMINISTRATIVE | `null`                  |
| CDL (Commercial Driver License)                       | `7639c58fb4b75e2ff74270787eda80a7` | ADMINISTRATIVE | `null`                  |
| Care Management                                       | `6b4b539a233145fe871e8ac703f39fcb` | CLINICAL       | `null`                  |
| Disability Form                                       | `a5fd8d81026747c0b01f757b7935f82a` | ADMINISTRATIVE | `null`                  |
| Emergency Department Report                           | `67037fd377654984b8b368b47d0ab0e4` | CLINICAL       | `null`                  |
| External Medical Records                              | `b61d0a4ebf4316a1a3beea32bec88052` | CLINICAL       | `null`                  |
| Handicap Parking Permit                               | `649a852657357c20491856f4eb7a2690` | ADMINISTRATIVE | `null`                  |
| Home Care Report                                      | `d368eaa8f1b2419cb792bb7876bfac8a` | CLINICAL       | `null`                  |
| Hospital Discharge Summary                            | `6be998e1335a4d9689cae33ec7ed6968` | CLINICAL       | `null`                  |
| Hospital History & Physical                           | `d9060893790744589c5252ddb81b785e` | CLINICAL       | `null`                  |
| Imaging Report                                        | `87041869c5954337b84fd10094fe5c0a` | CLINICAL       | `ImagingReportTemplate` |
| In-Office Testing                                     | `372e7248ba944dbeab54712078c0ec44` | CLINICAL       | `null`                  |
| Insurance Card                                        | `2551841bcfd34e1aa839cb1e3b7ef48f` | ADMINISTRATIVE | `null`                  |
| Insurer Prior Authorization                           | `0394e7a3a5c847f495414e7511d12543` | ADMINISTRATIVE | `null`                  |
| Lab Report                                            | `f605e084dcad4beca16c0f62e6586d76` | CLINICAL       | `LabReportTemplate`     |
| Medicaid Documents                                    | `e02e0f6dc76d42aaa61384c85ca90830` | ADMINISTRATIVE | `null`                  |
| Nursing Home                                          | `fc14824cdc9fdcd1e2ce005aa3019d20` | CLINICAL       | `null`                  |
| Operative Report                                      | `7f118206607248b7b13409e69c638eba` | CLINICAL       | `null`                  |
| POLST (Provider Order for Life Sustaining Treatment)  | `cf72e522dd95fa1da1297cf3bf5e54e8` | ADMINISTRATIVE | `null`                  |
| Patient Administrative Intake Form                    | `b25601a3e8ac543f5f2d7a85006de223` | ADMINISTRATIVE | `null`                  |
| Patient Agreement                                     | `2e16ccd7ad5a4bcf9d21dd51b4d16cb9` | ADMINISTRATIVE | `null`                  |
| Patient Assistance                                    | `ebd8c4f6f35b4c008e512d0e3c666e95` | ADMINISTRATIVE | `null`                  |
| Patient Clinical Intake Form                          | `8c9ca86c76704d57a775cd6f48a02b6c` | CLINICAL       | `null`                  |
| Patient Consent                                       | `7ce5a6eefedcff89a5a460f6be89d308` | ADMINISTRATIVE | `null`                  |
| Physical Exams                                        | `b1146b76cd2c4b488c964cf497fb1dce` | CLINICAL       | `null`                  |
| Power of Attorney                                     | `1ff5f640868528e633a5d45f2142161e` | ADMINISTRATIVE | `null`                  |
| Prescription Card                                     | `0d002c5fe86c44b0a63c08e70e0df37c` | ADMINISTRATIVE | `null`                  |
| Prescription Refill Request                           | `714a8229339b4af3989403a308bdcbfb` | CLINICAL       | `null`                  |
| Rehabilitation Report                                 | `660f6fce32a64b3f9817f4bad3d56c79` | CLINICAL       | `null`                  |
| Release of Information Request                        | `2283372cb0fa4962a6fcff2eb3ca080b` | ADMINISTRATIVE | `null`                  |
| Specialist Consult Report                             | `f0f1398f6f4640d29e4ff80d5481eb3f` | CLINICAL       | `SpecialtyReportTemplate` |
| Uncategorized Administrative Document                 | `7ebe754f4c3b860cf80d3aa9ebd8494c` | ADMINISTRATIVE | `null`                  |
| Uncategorized Clinical Document                       | `52ef59487ecabc9cdd645c21c7a35458` | CLINICAL       | `null`                  |
| Worker's Compensation Documents                       | `54a06a3f06b48cbebf8dec88707272c3` | ADMINISTRATIVE | `null`                  |

### Example

The `DOCUMENT_RECEIVED` event context includes `available_document_types`, a list of every document type the instance supports — each entry carries the `key`, `name`, `report_type`, and `template_type` you'll need to construct a `CategorizeDocument` effect. The idiomatic pattern is to read from that list rather than hardcode catalog values, so a plugin keeps working as the catalog changes.

The handler below matches by `name` (using the [Supported Document Types](#supported-document-types) table above as a reference for what names to expect) and forwards the matched values to the effect. `ReportType` and `TemplateType` enum instances are constructed explicitly from the context's string values — the SDK rejects raw strings.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import CategorizeDocument
from canvas_sdk.effects.data_integration.types import ReportType, TemplateType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class CategorizeLabReports(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        available = self.event.context.get("available_document_types", [])
        lab_report = next((dt for dt in available if dt["name"] == "Lab Report"), None)

        if not lab_report:
            return []

        template_type = lab_report.get("template_type")

        return [
            CategorizeDocument(
                document_id=self.event.target.id,
                document_type={
                    "key": lab_report["key"],
                    "name": lab_report["name"],
                    "report_type": ReportType(lab_report["report_type"]),
                    "template_type": TemplateType(template_type) if template_type else None,
                },
                annotations=[
                    {"text": "AI Categorized", "color": "#4CAF50"},
                ],
            ).apply()
        ]
```

For full end-to-end usage including discovery, error handling, and the other Data Integration effects in a single handler, see the [`data_integration_example` plugin](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/data_integration_example) in canvas-plugins.

## Linking a Document to a Patient

To link a document in the Data Integration queue to a patient, import the `LinkDocumentToPatient` class from `canvas_sdk.effects.data_integration` and create an instance of it. The plugin is responsible for matching the patient and supplying their key — the interpreter does not search for matching patients itself.

| Attribute     |          | Type   | Description                                                                 |
|---------------|----------|--------|-----------------------------------------------------------------------------|
| `document_id` | required | string | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document.                                     |
| `patient_key` | required | string | The `id` of the [Patient](/sdk/data-patient/#patient) to link the document to. |
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
        document_id = self.event.target.id
        document_title = self.event.context.get("document", {}).get("title", "")

        # Plugin-specific matching logic — e.g., parse the document title or
        # call an OCR/LLM service to extract patient demographics, then look
        # up the patient via the SDK data module.
        patient = Patient.objects.filter(...).first()
        if not patient:
            return []

        return [
            LinkDocumentToPatient(
                document_id=document_id,
                patient_key=patient.id,
                annotations=[
                    {"text": "AI 92%", "color": "#4CAF50"},
                    {"text": f"Matched from '{document_title}'", "color": "#2196F3"},
                ],
            ).apply()
        ]
```

## Marking a Document as Junk

To mark a document in the Data Integration queue as junk (spam), import the `JunkDocument` class and create an instance of it.

| Attribute     |          | Type   | Description                                                                                            |
|---------------|----------|--------|--------------------------------------------------------------------------------------------------------|
| `document_id` | required | string | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document to mark as junk. |

`JunkDocument` only works on IntegrationTasks in early-stage states: **Unread**, **Read**, **Error**, **Unread error**, or **Junk** (already). IntegrationTasks in **Processed** or **Reviewed** states cannot be junked — attempting to do so raises a validation error. The effect also validates that `document_id` resolves to an existing IntegrationTask and is a well-formed UUID; missing, malformed, or unknown IDs raise validation errors before the IntegrationTask is touched.

To avoid the validation error for tasks that have moved past the early-stage states, you can read the [`status`](/sdk/data-integration-task/#integrationtask) field from the SDK data module and preflight-check before emitting the effect.

An example that preflight-checks the IntegrationTask status before junking:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import JunkDocument
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.integration_task import IntegrationTask, IntegrationTaskStatus


class JunkDocumentHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        document_id = self.event.target.id
        task = IntegrationTask.objects.get(id=document_id)

        # Skip tasks that have already been processed or reviewed
        if task.status in (IntegrationTaskStatus.PROCESSED, IntegrationTaskStatus.REVIEWED):
            return []

        return [JunkDocument(document_id=document_id).apply()]
```

## Prefilling Document Fields

`PrefillDocumentFields` pre-populates the parse-template fields on an IntegrationTask. **Only three document types support field prefill** — those whose `template_type` is a known parse-template family:

| Document type             | `template_type`           | SDK data module                                            |
|---------------------------|---------------------------|------------------------------------------------------------|
| Lab Report                | `LabReportTemplate`       | [`LabReportTemplate`](/sdk/data-lab-report-template/)   |
| Imaging Report            | `ImagingReportTemplate`   | [`ImagingReportTemplate`](/sdk/data-imaging-report-template/) |
| Specialist Consult Report | `SpecialtyReportTemplate` | [`SpecialtyReportTemplate`](/sdk/data-specialty-report-template/) |

Document types with inline fields (Patient Consent, Power of Attorney, the Uncategorized variants, and the other ~30 entries in the [Supported Document Types](#supported-document-types) catalog) cannot have their fields prefilled by this effect.

> The wire-level effect type for this class is `UPDATE_DOCUMENT_FIELDS`, which is what appears in event logs and the [effects table](/sdk/effects/#data-integration). The class name is `PrefillDocumentFields`.

| Attribute     |          | Type                                      | Description                                                                              |
|---------------|----------|-------------------------------------------|------------------------------------------------------------------------------------------|
| `document_id` | required | string                                    | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document. |
| `templates`   | required | list[[PrefillTemplate](#prefilltemplate)] | One or more templates to prefill. Must contain at least one entry.                       |
| `annotations` | optional | list                                      | List of annotations for display in the UI. See [Annotations](#annotations).              |

### PrefillTemplate

A `PrefillTemplate` is a dictionary with the following keys:

| Key             |          | Type                                                             | Description                                                                                                                                  |
|-----------------|----------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `template_id`   | required | int                                                              | The integer `dbid` of a `LabReportTemplate`, `ImagingReportTemplate`, or `SpecialtyReportTemplate` record. (Note: this is the integer primary key, not the `id` UUID.) Look this up via the SDK data module — see the [example](#example) below. |
| `template_name` | required | string                                                           | The matching template's `.name`.                                                                                                              |
| `fields`        | required | dict[str, [PrefillDocumentFieldData](#prefilldocumentfielddata)] | Map of field name to field data. Keys must match the `label` of a field on the chosen template — iterate `template.fields.all()` to discover the available labels, units, types, and required-ness. |

### PrefillDocumentFieldData

A `PrefillDocumentFieldData` is a dictionary with the following keys:

| Key               |          | Type   | Description                                                       |
|-------------------|----------|--------|-------------------------------------------------------------------|
| `value`           | required | string | The field value, stringified into the form field at render time. The same rules apply to all three template families (`LabReportTemplateField`, `ImagingReportTemplateField`, `SpecialtyReportTemplateField`). Currently supported are fields whose `type` is `"float"`, `"text"`, `"date"`, `"select"`, or `"radio"`. For `"select"` and `"radio"`, the value must exactly match one of the field's `options[*].key` for the dropdown to pre-select. |
| `unit`            | optional | string | Unit of measurement. Should match the corresponding template field's `units` (`LabReportTemplateField.units`, `ImagingReportTemplateField.units`, or `SpecialtyReportTemplateField.units`). |
| `reference_range` | optional | string | Reference range for the value.                                    |
| `abnormal`        | optional | bool   | Whether the value is abnormal.                                    |
| `annotations`     | optional | list   | Per-field annotations. Same shape as [Annotations](#annotations). |

### Discovering Available Fields

Before constructing a `PrefillDocumentFields` payload, you can inspect the template to see what labels, units, types, and option keys it defines. The same approach works for `ImagingReportTemplate` and `SpecialtyReportTemplate`.

```python
from canvas_sdk.v1.data import LabReportTemplate
from logger import log


def inspect_lab_template(template_name) -> None:
    template = (
        LabReportTemplate.objects
        .active()
        .filter(name=template_name)
        .first()
    )
    if not template:
        log.info(f"No template found with name {template_name}")
        return

    log.info(f"Template: {template.name} (dbid={template.dbid})")
    for field in template.fields.all().order_by("sequence"):
        log.info(
            f"  {field.label}",
            type=field.type,
            units=field.units,
            required=field.required,
            code=field.code,
            code_system=field.code_system,
        )
        for opt in field.options.all():
            log.info(f"    option", key=opt.key, label=opt.label)
```

Sample output for a CBC Panel template:

```text
Template: CBC Panel (dbid=42)
  Hemoglobin   type=float  units=g/dL    required=True   code=718-7   code_system=LOINC
  WBC          type=float  units=10^3/uL required=True   code=6690-2  code_system=LOINC
  Differential type=select units=        required=False  code=        code_system=
    option key=NORMAL    label=Normal
    option key=ABNORMAL  label=Abnormal
```

With that you can see which labels go into the `fields` dict's keys, what `unit` value to send, and — for `select`/`radio` fields — which `option.key` values are valid for the `value` field.

### Example

An example of prefilling a Lab Report. The plugin looks up the CBC Panel template via the [`LabReportTemplate`](/sdk/data-lab-report-template/) SDK data module, then iterates the template's `fields` relation to discover which labels and units are available before filling in the values it extracted from the document.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import PrefillDocumentFields
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import LabReportTemplate


class PrefillLabReportHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        cbc = (
            LabReportTemplate.objects
            .active()
            .filter(name__icontains="CBC")
            .first()
        )
        if not cbc:
            return []

        # Values the plugin extracted from the document via OCR/LLM.
        # Hardcoded here for clarity.
        extracted = {
            "Hemoglobin": ("13.5", False),
            "WBC": ("11.2", True),
        }

        # Iterate the template's fields to discover which labels and units
        # the template defines, then fill in only the ones the plugin has
        # values for. Each field exposes `label`, `units`, `type`, and
        # `required` (see LabReportTemplateField).
        prefill_fields: dict[str, dict] = {}
        for field in cbc.fields.all():
            if field.label not in extracted:
                continue
            value, abnormal = extracted[field.label]
            prefill_fields[field.label] = {
                "value": value,
                "unit": field.units or "",
                "abnormal": abnormal,
            }

        return [
            PrefillDocumentFields(
                document_id=self.event.target.id,
                templates=[
                    {
                        "template_id": cbc.dbid,
                        "template_name": cbc.name,
                        "fields": prefill_fields,
                    },
                ],
                annotations=[
                    {"text": "Prefilled via AI", "color": "#FF9800"},
                ],
            ).apply()
        ]
```

## Removing a Document from a Patient

To unlink a document from its currently-linked patient in the Data Integration queue, import the `RemoveDocumentFromPatient` class and create an instance of it. An IntegrationTask carries at most one patient link at a time, so this effect simply clears that link.

| Attribute     |          | Type   | Description                                                                                                         |
|---------------|----------|--------|---------------------------------------------------------------------------------------------------------------------|
| `document_id` | required | string | The `id` of the [IntegrationTask](/sdk/data-integration-task/#integrationtask) document to unlink from its patient. |

An example of unlinking a document from its patient:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import RemoveDocumentFromPatient
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class RemoveDocumentHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_LINKED_TO_PATIENT)

    def compute(self) -> list[Effect]:
        return [
            RemoveDocumentFromPatient(
                document_id=self.event.target.id,
            ).apply()
        ]
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
