---
title: "Categorize Document"
slug: "effect-categorize-document"
excerpt: "Categorize documents in the Data Integration queue."
hidden: false
---

The `CategorizeDocument` effect categorizes a document in the Data Integration queue into a specific document type.

## Attributes

| Attribute           | Type                                          | Description                                              | Required |
| ------------------- | --------------------------------------------- | -------------------------------------------------------- | -------- |
| `document_id`       | `str` or `int`                                | The ID of the IntegrationTask document to categorize     | Yes      |
| `document_type`     | [DocumentType](#documenttype)                 | Document type information                                | Yes      |
| `confidence_scores` | [ConfidenceScores](#confidencescores)         | Confidence scores for extracted fields (e.g., from OCR)  | No       |

## DocumentType

The `DocumentType` dict contains the classification information for the document.

### Attributes

| Attribute       | Type            | Description                                                                                      | Required |
| --------------- | --------------- | ------------------------------------------------------------------------------------------------ | -------- |
| `key`           | `str`           | The unique key identifying the document type                                                     | Yes      |
| `name`          | `str`           | The human-readable name of the document type                                                     | Yes      |
| `report_type`   | `str`           | Must be `"CLINICAL"` or `"ADMINISTRATIVE"`                                                       | Yes      |
| `template_type` | `str` or `None` | One of `"LabReportTemplate"`, `"ImagingReportTemplate"`, `"SpecialtyReportTemplate"`, or `None`  | No       |

## ConfidenceScores

The `ConfidenceScores` dict contains optional confidence values for document fields extracted from the document (e.g., from OCR). All values must be floats between 0.0 and 1.0.

### Attributes

| Attribute       | Type                                                          | Description                                 | Required |
| --------------- | ------------------------------------------------------------- | ------------------------------------------- | -------- |
| `document_id`   | `float`                                                       | Confidence in the document_id extraction    | No       |
| `document_type` | [DocumentTypeConfidenceScores](#documenttypeconfidencescores) | Confidence scores for document_type fields  | No       |

## DocumentTypeConfidenceScores

The `DocumentTypeConfidenceScores` dict contains confidence values for individual document type fields.

### Attributes

| Attribute       | Type    | Description                            | Required |
| --------------- | ------- | -------------------------------------- | -------- |
| `key`           | `float` | Confidence in key match (0.0-1.0)      | No       |
| `name`          | `float` | Confidence in name match (0.0-1.0)     | No       |
| `report_type`   | `float` | Confidence in report_type (0.0-1.0)    | No       |
| `template_type` | `float` | Confidence in template_type (0.0-1.0)  | No       |

## Validation

The effect performs validation before execution to ensure data integrity:

1. **Required Fields**:
   - `document_id` and `document_type` must be provided
   - `document_type.key` must be a non-empty string (whitespace-only is invalid)
   - `document_type.name` must be a non-empty string (whitespace-only is invalid)
2. **Enumerated Values**:
   - `report_type` must be one of `"CLINICAL"` or `"ADMINISTRATIVE"`
   - `template_type` if provided, must be one of `"LabReportTemplate"`, `"ImagingReportTemplate"`, or `"SpecialtyReportTemplate"`, or `None`
3. **Confidence Scores Validation**:
   - If provided, only `document_id` and `document_type` are valid keys
   - All values must be floats between 0.0 and 1.0

## Example Usage

```python
from canvas_sdk.effects.categorize_document import CategorizeDocument
from canvas_sdk.handlers.base import BaseHandler


class Protocol(BaseHandler):
    def compute(self):
        effect = CategorizeDocument(
            document_id="12345",
            document_type={
                "key": "lab_report",
                "name": "Lab Report",
                "report_type": "CLINICAL",
                "template_type": "LabReportTemplate",
            },
        )

        return [effect.apply()]
```

### With Confidence Scores

```python?partial=true
effect = CategorizeDocument(
    document_id="12345",
    document_type={
        "key": "imaging_report",
        "name": "Imaging Report",
        "report_type": "CLINICAL",
        "template_type": "ImagingReportTemplate",
    },
    confidence_scores={
        "document_id": 0.95,
        "document_type": {
            "key": 0.90,
            "name": 0.85,
            "report_type": 0.92,
            "template_type": 0.88,
        },
    },
)
```

### Administrative Document

```python?partial=true
effect = CategorizeDocument(
    document_id="67890",
    document_type={
        "key": "insurance_form",
        "name": "Insurance Form",
        "report_type": "ADMINISTRATIVE",
        "template_type": None,
    },
)
```

<br/>
<br/>
<br/>
