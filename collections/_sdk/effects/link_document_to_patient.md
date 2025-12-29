---
title: 'LinkDocumentToPatient Effect'
slug: 'effect-link-document-to-patient'
excerpt: 'Link a document to a patient using demographic matching'
hidden: false
---

The `LinkDocumentToPatient` effect links a document in the Data Integration queue to a patient based on patient demographics (first name, last name, date of birth). This is useful for automating document-to-patient matching in workflows that process incoming clinical documents.

## Overview

When documents arrive in the Data Integration queue, they often need to be associated with the correct patient record. This effect performs demographic matching to find and link the appropriate patient. The matching logic:

- Uses case-insensitive matching for first and last names
- Requires an exact match on date of birth
- Excludes inactive patients from consideration
- Requires exactly one matching patient (fails if zero or multiple matches)

## Attributes

| Attribute           | Type   | Description                                                     | Required |
| ------------------- | ------ | --------------------------------------------------------------- | -------- |
| `document_id`       | `str`  | The UUID of the IntegrationTask (document) to link              | Yes      |
| `first_name`        | `str`  | Patient's first name for matching                               | Yes      |
| `last_name`         | `str`  | Patient's last name for matching                                | Yes      |
| `date_of_birth`     | `str`  | Patient's date of birth in ISO 8601 format (e.g., "1990-05-15") | Yes      |
| `confidence_scores` | `dict` | Optional confidence scores from OCR/extraction                  | No       |

### Confidence Scores

The optional `confidence_scores` dictionary can contain the following keys:

| Key             | Type    | Description                                   |
| --------------- | ------- | --------------------------------------------- |
| `first_name`    | `float` | Confidence score for first name extraction    |
| `last_name`     | `float` | Confidence score for last name extraction     |
| `date_of_birth` | `float` | Confidence score for date of birth extraction |

These scores are logged for monitoring and debugging purposes but do not affect the matching logic.

## Implementation Details

### Patient Matching

The effect searches for patients matching all three demographic criteria:

1. **First Name**: Case-insensitive match (e.g., "John" matches "JOHN" or "john")
2. **Last Name**: Case-insensitive match
3. **Date of Birth**: Exact date match

Names are trimmed of leading/trailing whitespace before matching. Inactive patients (`active=False`) are excluded from the search.

### Validation

The effect validates:

- The `document_id` corresponds to an existing IntegrationTask
- All required demographic fields are provided
- The `date_of_birth` is in valid ISO 8601 format

## Example Usage

### Basic Usage

```python
from canvas_sdk.effects.data_integration import LinkDocumentToPatient
from canvas_sdk.handlers.base import BaseHandler


class DocumentMatchingHandler(BaseHandler):
    def compute(self):
        effect = LinkDocumentToPatient(
            document_id="550e8400-e29b-41d4-a716-446655440000",
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-05-15"
        )

        return [effect.apply()]
```

### With Confidence Scores

```python
from typing import TypedDict

from canvas_sdk.effects.data_integration import LinkDocumentToPatient
from canvas_sdk.handlers.base import BaseHandler


class LinkDocumentConfidenceScores(TypedDict, total=False):
    """Confidence scores for extracted patient demographics."""

    first_name: float
    last_name: float
    date_of_birth: float


class OCRDocumentHandler(BaseHandler):
    """Handler that processes OCR-extracted patient demographics."""

    def compute(self):
        # Demographics extracted from document via OCR
        extracted_data = self.context.get("extracted_demographics", {})

        confidence_scores: LinkDocumentConfidenceScores = {
            "first_name": extracted_data.get("first_name_confidence", 0.0),
            "last_name": extracted_data.get("last_name_confidence", 0.0),
            "date_of_birth": extracted_data.get("dob_confidence", 0.0),
        }

        effect = LinkDocumentToPatient(
            document_id=self.context["document_id"],
            first_name=extracted_data["first_name"],
            last_name=extracted_data["last_name"],
            date_of_birth=extracted_data["date_of_birth"],
            confidence_scores=confidence_scores,
        )

        return [effect.apply()]
```

## Error Handling

The effect raises `ValidationError` in the following cases:

| Error Condition            | Error Message                                                  |
| -------------------------- | -------------------------------------------------------------- |
| Missing `document_id`      | "document_id is required"                                      |
| Missing `first_name`       | "first_name is required"                                       |
| Missing `last_name`        | "last_name is required"                                        |
| Missing `date_of_birth`    | "date_of_birth is required"                                    |
| Invalid date format        | "date_of_birth must be a valid ISO 8601 date format"           |
| IntegrationTask not found  | "IntegrationTask with id {id} does not exist"                  |
| No matching patients       | "No patient found matching demographics: ..."                  |
| Multiple matching patients | "Multiple patients ({count}) found matching demographics: ..." |

When multiple patients match, the error message includes the patient IDs to help with troubleshooting.

## Notes

- The effect modifies the IntegrationTask by setting its `patient` field to the matched patient
- If you need to remove a patient link, use the [RemoveDocumentFromPatient](/sdk/effect-remove-document-from-patient/) effect
- For documents that require manual review when matching fails, consider implementing fallback logic in your handler

<br/>
<br/>
<br/>
