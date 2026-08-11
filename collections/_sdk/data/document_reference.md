---
title: "DocumentReference"
slug: "data-document-reference"
excerpt: "References to documents stored in Canvas, with presigned URL support for secure access."
hidden: false
---

# DocumentReference

The `DocumentReference` model represents references to documents stored in Canvas, such as uploaded PDFs, scanned files, and other clinical documents. Each document reference can link to a file stored in S3 and provides secure access via presigned URLs.

## Basic Usage

```python
from canvas_sdk.v1.data import DocumentReference

# Get a specific document reference
doc_ref = DocumentReference.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

# Get all document references
all_docs = DocumentReference.objects.all()
```

## Filtering

### By patient

```python
from canvas_sdk.v1.data import DocumentReference

patient_docs = DocumentReference.objects.for_patient("b80b1cdc2e6a4aca90ccebc02e683f35")
```

### By status

```python
from canvas_sdk.v1.data import DocumentReference, DocumentReferenceStatus

current_docs = DocumentReference.objects.filter(status=DocumentReferenceStatus.CURRENT)
```

### By category or type

```python
from canvas_sdk.v1.data import DocumentReference

docs = DocumentReference.objects.filter(category__code="clinical-note")
```

## Accessing Document Files

The `document_url` property returns a presigned S3 URL for securely accessing the document file. If no S3 file is present, it falls back to the `document_absolute_url` field.

```python
from canvas_sdk.v1.data import DocumentReference

doc_ref = DocumentReference.objects.exclude(document="").first()

# Returns a presigned S3 URL (valid for 1 hour)
url = doc_ref.document_url
```

## Attributes

### DocumentReference

| Field Name                       | Type                                                        |
|----------------------------------|-------------------------------------------------------------|
| id                               | UUID                                                        |
| dbid                             | Integer                                                     |
| created                          | DateTime                                                    |
| modified                         | DateTime                                                    |
| document                         | String                                                      |
| document_absolute_url            | String                                                      |
| document_content_type            | String                                                      |
| business_identifier              | String                                                      |
| originator                       | [CanvasUser](/sdk/data-canvasuser)                          |
| subject                          | [CanvasUser](/sdk/data-canvasuser)                          |
| type                             | [DocumentReferenceCoding](#documentreferencecoding)         |
| category                         | [DocumentReferenceCategory](#documentreferencecategory)     |
| status                           | [DocumentReferenceStatus](#documentreferencestatus)         |
| date                             | Date                                                        |
| encounter                        | [Encounter](/sdk/data-encounter)                            |
| team                             | [Team](/sdk/data-team/#team)                                |
| related_object_document_title    | String                                                      |
| related_object_document_comment  | String                                                      |
| content_type                     | [ContentType](/sdk/data-content-type/) (the related object's type)          |
| object_id                        | Integer (the related object's `dbid`)                                       |
| related_object                   | Model (property) — the SDK object the document is attached to, or `None`    |
| document_url                     | String (property) — presigned S3 URL or absolute URL        |

### DocumentReferenceCoding

A coding entry representing the type of a document reference.

| Field Name     | Type    |
|----------------|---------|
| dbid           | Integer |
| system         | String  |
| version        | String  |
| code           | String  |
| display        | String  |
| user_selected  | Boolean |

### DocumentReferenceCategory

A coding entry representing the category of a document reference.

| Field Name     | Type    |
|----------------|---------|
| dbid           | Integer |
| system         | String  |
| version        | String  |
| code           | String  |
| display        | String  |
| user_selected  | Boolean |

### DocumentReferenceStatus

An enum representing the status of a document reference.

| Member            | Value              | Description      |
|-------------------|--------------------|------------------|
| `CURRENT`         | `current`          | Current          |
| `SUPERSEDED`      | `superseded`       | Superseded       |
| `ENTERED_IN_ERROR`| `entered-in-error` | Entered in Error |

## The related object

Most document references point back at the record they were generated from — a lab report, a letter, a locked-note PDF, a patient statement, and so on. `content_type` and `object_id` form that generic link: `content_type` identifies the linked model by its stable `app_label` and lowercased `model` name, and `object_id` is that record's `dbid`.

The `related_object` property resolves the link for you, returning the corresponding SDK data model instance:

```python
from canvas_sdk.v1.data import DocumentReference

doc_ref = DocumentReference.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

# The SDK object this document is attached to (a LabReport, Letter, ImagingReport, ...), or None.
source = doc_ref.related_object
```

`related_object` returns `None` when the document has no related object (`content_type` or `object_id` is unset) or when the linked content type has no SDK data model equivalent. The content types it resolves today:

| `app_label` / `model`                    | SDK data model                |
|-------------------------------------------|-------------------------------|
| `api` / `labreport`                       | LabReport                     |
| `api` / `imagingreport`                   | ImagingReport                 |
| `api` / `letter`                          | Letter                        |
| `api` / `notestatechangeevent`            | NoteStateChangeEvent          |
| `api` / `uncategorizedclinicaldocument`   | UncategorizedClinicalDocument |
| `api` / `referralreport`                  | ReferralReport                |
| `api` / `educationalmaterial`             | EducationalMaterial           |
| `api` / `patientadministrativedocument`   | PatientAdministrativeDocument |
| `quality_and_revenue` / `invoicefull`     | Invoice                       |

To go the other way — find every document reference for a given source type — resolve the [ContentType](/sdk/data-content-type/) at runtime from its stable `app_label` and `model` (never hardcode the per-environment `dbid`) and filter on it:

```python
from canvas_sdk.v1.data import ContentType, DocumentReference

content_type = ContentType.objects.filter(
    app_label="api", model="patientadministrativedocument"
).first()

references = DocumentReference.objects.filter(content_type=content_type)
```
