---
title: 'RemoveDocumentFromPatient Effect'
slug: 'effect-remove-document-from-patient'
excerpt: 'Remove patient link from a document in the Data Integration queue'
hidden: false
---

The `RemoveDocumentFromPatient` effect removes the patient association from a document in the Data Integration queue. This is useful when a document was incorrectly linked to a patient or needs to be reprocessed for matching.

## Overview

Documents in the Data Integration queue can be linked to patients for processing and review. This effect allows you to unlink a document from its currently associated patient, returning it to an unassigned state. The operation is idempotent - calling it on a document that has no patient association is safe and has no effect.

## Attributes

| Attribute           | Type   | Description                                        | Required |
| ------------------- | ------ | -------------------------------------------------- | -------- |
| `document_id`       | `str`  | The UUID of the IntegrationTask to unlink          | Yes      |
| `patient_id`        | `str`  | Patient ID for audit logging purposes              | No       |
| `confidence_scores` | `dict` | Optional confidence score for the removal decision | No       |

### Confidence Scores

The optional `confidence_scores` dictionary can contain:

| Key       | Type    | Description                               |
| --------- | ------- | ----------------------------------------- |
| `removal` | `float` | Confidence score for the removal decision |

This score is logged for monitoring and debugging purposes.

## Behavior

- **Idempotent**: Safe to call even if the document has no patient association
- **Audit Trail**: The previous patient ID is logged before removal for audit purposes
- **Immediate Effect**: The patient link is removed and the IntegrationTask is saved immediately

## Example Usage

### Basic Usage

```python
from canvas_sdk.effects.data_integration import RemoveDocumentFromPatient
from canvas_sdk.handlers.base import BaseHandler


class DocumentUnlinkHandler(BaseHandler):
    def compute(self):
        effect = RemoveDocumentFromPatient(
            document_id="550e8400-e29b-41d4-a716-446655440000"
        )

        return [effect.apply()]
```

### With Audit Information

```python
from typing import TypedDict

from canvas_sdk.effects.data_integration import RemoveDocumentFromPatient
from canvas_sdk.handlers.base import BaseHandler


class RemoveDocumentConfidenceScores(TypedDict, total=False):
    """Confidence scores for document removal decision."""

    removal: float


class DocumentReprocessHandler(BaseHandler):
    """Handler that unlinks a document for reprocessing."""

    def compute(self):
        document_id = self.context["document_id"]
        current_patient_id = self.context.get("current_patient_id")

        confidence_scores: RemoveDocumentConfidenceScores = {"removal": 0.95}

        effect = RemoveDocumentFromPatient(
            document_id=document_id,
            patient_id=current_patient_id,  # For audit logging
            confidence_scores=confidence_scores,
        )

        return [effect.apply()]
```

### Conditional Removal

```python
from canvas_sdk.effects.data_integration import RemoveDocumentFromPatient
from canvas_sdk.handlers.base import BaseHandler


class MismatchedDocumentHandler(BaseHandler):
    """Removes patient link when document demographics don't match."""

    def compute(self):
        document = self.context["document"]
        patient = self.context.get("patient")

        # Check if document demographics match the linked patient
        if patient and not self._demographics_match(document, patient):
            effect = RemoveDocumentFromPatient(
                document_id=document["id"],
                patient_id=patient["id"]
            )
            return [effect.apply()]

        return []

    def _demographics_match(self, document, patient):
        # Custom matching logic
        return (
            document.get("first_name", "").lower() == patient.get("first_name", "").lower()
            and document.get("last_name", "").lower() == patient.get("last_name", "").lower()
        )
```

## Error Handling

The effect raises `ValidationError` in the following cases:

| Error Condition            | Error Message                                 |
| -------------------------- | --------------------------------------------- |
| Missing `document_id`      | "document_id is required"                     |
| IntegrationTask not found  | "IntegrationTask with id {id} does not exist" |
| Invalid document_id format | "Invalid document_id format: {id}"            |

## Notes

- This effect only removes the patient link; it does not delete the document itself
- The document remains in the Data Integration queue after the patient link is removed
- Use [LinkDocumentToPatient](/sdk/effect-link-document-to-patient/) to associate the document with a different patient
- The `patient_id` parameter is optional and used only for logging purposes; the effect will remove whatever patient is currently linked regardless of this value

<br/>
<br/>
<br/>
