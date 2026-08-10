---
title: "PatientAdministrativeDocument"
slug: "data-patient-administrative-document"
excerpt: "Canvas SDK PatientAdministrativeDocument"
hidden: false
---

## Introduction

The `PatientAdministrativeDocument` model is a read-only Canvas SDK data model representing administrative documents associated with a patient, such as intake confirmations and insurance cards.

The companion `DocumentCoding` model provides the value of the `code` field and describes the type of administrative document.

## Basic Usage

```python
from canvas_sdk.v1.data import PatientAdministrativeDocument, DocumentCoding

# Get a specific patient administrative document
document = PatientAdministrativeDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

# Get all patient administrative documents
all_documents = PatientAdministrativeDocument.objects.all()

# Access the document's coding
coding = document.code
```

## Filtering

Patient administrative documents can be filtered by any attribute that exists on the model.

### By patient

```python
from canvas_sdk.v1.data import PatientAdministrativeDocument, Patient

patient = Patient.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")
documents = PatientAdministrativeDocument.objects.filter(patient=patient)
```

## Accessing Document Files

The `document_url` property returns a presigned S3 URL for securely accessing the stored document. The URL is valid for one hour. If no file is present, the property returns `None`.

```python
from canvas_sdk.v1.data import PatientAdministrativeDocument

document = PatientAdministrativeDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

# Returns a presigned S3 URL (valid for 1 hour)
url = document.document_url
```

## Attributes

### PatientAdministrativeDocument

| Field Name              | Type                                                                     |
|-------------------------|--------------------------------------------------------------------------|
| id                      | UUID                                                                     |
| dbid                    | Integer                                                                  |
| created                 | DateTime                                                                 |
| modified                | DateTime                                                                 |
| patient                 | [Patient](/sdk/data-patient/#patient)                                    |
| originator              | [CanvasUser](/sdk/data-canvasuser)                                       |
| assigned_by             | [CanvasUser](/sdk/data-canvasuser)                                       |
| team                    | [Team](/sdk/data-team/#team)                                             |
| integration_task_review | [IntegrationTaskReview](/sdk/data-integration-task/#integrationtaskreview) |
| code                    | [DocumentCoding](#documentcoding)                                        |
| name                    | String                                                                   |
| review_mode             | [DocumentReviewMode](/sdk/data-enumeration-types/#documentreviewmode)    |
| junked                  | Boolean                                                                  |
| assigned_date           | DateTime                                                                 |
| team_assigned_date      | DateTime                                                                 |
| original_date           | Date                                                                     |
| comment                 | String                                                                   |
| priority                | Boolean                                                                  |
| document                | String                                                                   |
| document_url            | String (property) — presigned S3 URL or None                            |

### DocumentCoding

A coding entry representing the type of a patient administrative document.

| Field Name    | Type    |
|---------------|---------|
| dbid          | Integer |
| system        | String  |
| version       | String  |
| code          | String  |
| display       | String  |
| user_selected | Boolean |
