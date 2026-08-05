---
title: "PatientAdministrativeDocument"
slug: "data-patient-administrative-document"
excerpt: "Patient-facing administrative documents, such as signed consent forms and statements."
hidden: false
---

# PatientAdministrativeDocument

The `PatientAdministrativeDocument` model represents patient-facing administrative documents — for example the signed consent document a `PatientConsent` points at. Each carries a document file and an optional `DocumentCoding`.

## Basic Usage

`PatientAdministrativeDocument` records do not have a UUID `id`; retrieve them by their integer `dbid`, or filter by patient.

```python
from canvas_sdk.v1.data import PatientAdministrativeDocument

# Get all administrative documents
documents = PatientAdministrativeDocument.objects.all()

# Get a specific record by its integer dbid
document = PatientAdministrativeDocument.objects.get(dbid=42)

# Get a patient's administrative documents
patient_documents = PatientAdministrativeDocument.objects.filter(
    patient__id="1eed3ea2a8d546a1b681a2a45de1d790"
)
```

## Accessing the document file

The `document_url` property returns a presigned S3 URL for securely accessing the document file, or `None` when no file is present.

```python
from canvas_sdk.v1.data import PatientAdministrativeDocument

document = PatientAdministrativeDocument.objects.exclude(document="").first()

# Returns a presigned S3 URL (valid for 1 hour)
url = document.document_url
```

## Attributes

### PatientAdministrativeDocument

| Field Name              | Type                                                                  |
|-------------------------|-----------------------------------------------------------------------|
| dbid                    | Integer                                                               |
| created                 | DateTime                                                              |
| modified                | DateTime                                                              |
| patient                 | [Patient](/sdk/data-patient/#patient)                                 |
| originator              | [CanvasUser](/sdk/data-canvasuser)                                    |
| assigned_by             | [CanvasUser](/sdk/data-canvasuser)                                    |
| team                    | [Team](/sdk/data-team/#team)                                          |
| integration_task_review | [IntegrationTaskReview](/sdk/data-integration-task/)                  |
| code                    | [DocumentCoding](#documentcoding)                                     |
| name                    | String                                                                |
| review_mode             | [DocumentReviewMode](/sdk/data-enumeration-types/#documentreviewmode) |
| junked                  | Boolean                                                               |
| assigned_date           | DateTime                                                              |
| team_assigned_date      | DateTime                                                              |
| original_date           | Date                                                                  |
| comment                 | String                                                                |
| priority                | Boolean                                                               |
| document                | String                                                                |
| document_url            | String (property) — presigned S3 URL or None                          |

### DocumentCoding

| Field Name    | Type    |
|---------------|---------|
| dbid          | Integer |
| system        | String  |
| version       | String  |
| code          | String  |
| display       | String  |
| user_selected | Boolean |
