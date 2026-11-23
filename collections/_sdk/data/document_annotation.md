---
title: "DocumentAnnotation"
slug: "data-document-annotation"
excerpt: "Canvas SDK DocumentAnnotation"
hidden: false
---

## Introduction

The `DocumentAnnotation` model holds the annotated versions of a document. When staff annotate or sign a document in Canvas, Canvas saves the result as a new PDF and records it as a `DocumentAnnotation`, leaving the original file unchanged. Each save adds another annotation, so a document can have several. The newest one is the current version of the document, and it's the version Canvas uses when it prints the document as a letter attachment.

An annotation links to the document it was made on: a [LabReport](/sdk/data-labs/#labreport), [ImagingReport](/sdk/data-imaging/#imagingreport), [ReferralReport](/sdk/data-referral/#referralreport), [PatientAdministrativeDocument](/sdk/data-patient-administrative-document/), or [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/). An annotation saved before the document was filed links to its [IntegrationTask](/sdk/data-integration-task/#integrationtask) instead.

## Basic usage

To get an annotation by identifier, use the `get` method on the `DocumentAnnotation` model manager:

```python
from canvas_sdk.v1.data import DocumentAnnotation

annotation = DocumentAnnotation.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")
```

A staff member's annotations are available from the [Staff](/sdk/data-staff/#staff) model. `document_annotations` holds the annotations they saved, and `signed_document_annotations` holds the annotations that carry their signature:

```python
from canvas_sdk.v1.data import Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")

created = staff.document_annotations.all()
signed = staff.signed_document_annotations.all()
```

The annotations saved on an incoming document before it was filed are available from its integration task:

```python
from canvas_sdk.v1.data import IntegrationTask

task = IntegrationTask.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
annotations = task.document_annotations.order_by("created")
```

## Filtering

Annotations can be filtered by any attribute that exists on the model.

### Annotations on a document

An annotation stores its document as a [ContentType](/sdk/data-content-type/) and an `object_id`. To find the annotations on a document, resolve the content type at runtime from its stable `app_label` and `model`, never the per-environment `dbid`, and match `object_id` against the document's `dbid`. The newest annotation is the document's current version:

```python
from canvas_sdk.v1.data import ContentType, DocumentAnnotation, LabReport

report = LabReport.objects.get(id="7c9e6679-7425-40de-944b-e07fc1f90ae7")

content_type = ContentType.objects.filter(app_label="api", model="labreport").first()

latest = (
    DocumentAnnotation.objects.filter(content_type=content_type, object_id=report.dbid)
    .order_by("created")
    .last()
)
```

{% include alert.html type="info" content="<code>object_id</code> holds the related record's integer <code>dbid</code>, not its UUID <code>id</code>. A document that no one has annotated has no annotations, so handle <code>None</code>." %}

### Annotations with a signature spot left

`has_signature_spot` is `True` when the annotated PDF still has a spot marked for a signature, such as a form sent for signature that the provider hasn't signed yet:

```python
from canvas_sdk.v1.data import DocumentAnnotation

awaiting_signature = DocumentAnnotation.objects.filter(has_signature_spot=True)
```

### Annotations signed by a staff member

```python
from canvas_sdk.v1.data import DocumentAnnotation, Staff

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")

signed = DocumentAnnotation.objects.filter(signers=staff)
```

## The annotated document

The `document_url` property returns a presigned S3 URL for the annotated PDF, or `None` when the annotation has no file. The URL is valid for one hour, so generate it when you need it rather than storing it.

The `related_object` property returns the document the annotation was made on, as its SDK model. It returns `None` when the annotation links to an integration task instead, or when the document isn't available through the SDK, such as when it was deleted.

```python
from canvas_sdk.v1.data import DocumentAnnotation

annotation = DocumentAnnotation.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")

# Presigned S3 URL to the annotated PDF, or None
url = annotation.document_url

# The LabReport, ImagingReport, ReferralReport, PatientAdministrativeDocument,
# or UncategorizedClinicalDocument, or None
document = annotation.related_object
```

## Attributes

### DocumentAnnotation

| Field Name         | Type                                                              | Notes |
|--------------------|-------------------------------------------------------------------|-------|
| id                 | UUID                                                              |       |
| dbid               | Integer                                                           |       |
| created            | DateTime                                                          | When this version was saved |
| modified           | DateTime                                                          |       |
| document           | File (S3 key)                                                     | The annotated PDF |
| created_by         | [Staff](/sdk/data-staff/#staff)                                   | The staff member who saved the annotation |
| signers            | [Staff](/sdk/data-staff/#staff)[]                                 | The staff members whose signatures were placed while annotating |
| has_signature_spot | Boolean                                                           | Whether the annotated PDF still has a spot marked for a signature |
| integration_task   | [IntegrationTask](/sdk/data-integration-task/#integrationtask)    | The incoming document the annotation was made on before it was filed, or `None` |
| content_type       | [ContentType](/sdk/data-content-type/)                            | The type of the annotated document, or `None` |
| object_id          | Integer                                                           | The `dbid` of the annotated document, or `None` |
| document_url       | String (computed)                                                 | Presigned S3 URL for `document`, or `None` if unset |
| related_object     | [LabReport](/sdk/data-labs/#labreport), [ImagingReport](/sdk/data-imaging/#imagingreport), [ReferralReport](/sdk/data-referral/#referralreport), [PatientAdministrativeDocument](/sdk/data-patient-administrative-document/), or [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/) (computed) | The annotated document, or `None` |
