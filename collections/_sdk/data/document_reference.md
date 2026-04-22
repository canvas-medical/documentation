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
