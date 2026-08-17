---
title: "PatientAdministrativeDocument"
slug: "data-patient-administrative-document"
excerpt: "Patient-facing administrative documents, such as signed consent forms and statements."
hidden: false
---

# PatientAdministrativeDocument

The `PatientAdministrativeDocument` model represents patient-facing administrative documents: prior authorizations, advance directives and beneficiary notices, signed consent forms and agreements, insurance and prescription cards, driver's licenses, intake forms, releases of information, powers of attorney, and workers' compensation attachments. Each carries a document file and an optional `DocumentCoding`. A signed consent form links back through `patient_consents` to the patient consent(s) it satisfies.

## Basic Usage

```python
from canvas_sdk.v1.data import PatientAdministrativeDocument

# Get all administrative documents
documents = PatientAdministrativeDocument.objects.all()

# Get a specific record by its id
document = PatientAdministrativeDocument.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

# Get a patient's administrative documents
patient_documents = PatientAdministrativeDocument.objects.filter(
    patient__id="1eed3ea2a8d546a1b681a2a45de1d790"
)
```

## Filtering

Patient administrative documents can be filtered by any attribute that exists on the model.

### By patient

```python
from canvas_sdk.v1.data import PatientAdministrativeDocument, Patient

patient = Patient.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")
documents = PatientAdministrativeDocument.objects.filter(patient=patient)
```

## Accessing the document file

The `document_url` property returns a presigned S3 URL for securely accessing the document file, or `None` when no file is present.

```python
from canvas_sdk.v1.data import PatientAdministrativeDocument

document = PatientAdministrativeDocument.objects.exclude(document="").first()

# Returns a presigned S3 URL (valid for 1 hour)
url = document.document_url
```

## The document reference

Each record also has a [DocumentReference](/sdk/data-document-reference/#the-related-object) pointing back at it — the record that carries the document's coding, category and status, and that represents it in the FHIR API. `document_url` above is the direct route to the file itself; reach for the document reference when you want that surrounding metadata.

Resolve the [ContentType](/sdk/data-content-type/) at runtime from its stable `app_label` and `model` — never hardcode the per-environment `dbid` — and match `object_id` against the record's `dbid`:

```python
from canvas_sdk.v1.data import ContentType, DocumentReference, PatientAdministrativeDocument

record = PatientAdministrativeDocument.objects.get(
    id="d2194110-5c9a-4842-8733-ef09ea5ead11"
)

content_type = ContentType.objects.filter(
    app_label="api", model="patientadministrativedocument"
).first()

document = DocumentReference.objects.filter(
    content_type=content_type, object_id=record.dbid
).first()
```

{% include alert.html type="info" content="<code>object_id</code> holds the related record's integer <code>dbid</code>, not its UUID <code>id</code>." %}

## Document codings

The `code` field comes from the document's type, which is drawn from a fixed list rather than set freely — either the type selected in Data Integration, or, when a document is created through the FHIR [DocumentReference](/api/documentreference/) endpoint, the LOINC code supplied in `type.coding`, which must match one of the codes below. Every coding uses the LOINC system (`http://loinc.org`). The document types stored as patient administrative documents are:

| Document type                         | Code     | Display                        |
|---------------------------------------|----------|--------------------------------|
| Advance Beneficiary Notice            | 53243-2  | Advanced beneficiary notice    |
| Advance Directive                     | 42348-3  | Advance directives             |
| Commercial Driver License             | 53245-7  | Driver license                 |
| Insurance Card Image                  | 64290-0  | Health insurance card          |
| Insurer Prior Authorization           | 52034-6  | Payer letter                   |
| Patient Agreement                     | 80570-5  | Agreement                      |
| Patient Consent Documents             | 59284-0  | Consent Document               |
| Power of Attorney                     | 64298-3  | Power of attorney              |
| Provider Order                        | 46209-3  | Provider orders                |
| Release of Information Request        | 101904-1 | Release of Information request |
| Uncategorized Administrative Document | 51851-4  | Administrative note            |
| Workers Compensation Documents        | 52070-0  | Workers compensation attachment |
| Disability Form                       | —        | none                           |
| Handicap Parking Permit               | —        | none                           |
| Medicaid Documents                    | —        | none                           |
| Patient Assistance Documents          | —        | none                           |
| Patient Intake Form                   | —        | none                           |
| Prescription Card Documents           | —        | none                           |

{% include alert.html type="warning" content="Six of these document types have no coding assigned, so their <code>code</code> is <code>None</code>. Filtering on <code>code</code> silently excludes them — check for a null <code>code</code> if you need to catch every administrative document. Because the FHIR endpoint identifies a document's type by its LOINC code, these six can only be created through Data Integration." %}

Clinical document types are stored as [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/) instead. Lab reports, imaging reports and specialist consult reports have their own models, so their codings never appear here.

## Attributes

### PatientAdministrativeDocument

| Field Name              | Type                                                                  |
|-------------------------|-----------------------------------------------------------------------|
| id                      | UUID                                                                  |
| dbid                    | Integer                                                               |
| created                 | DateTime                                                              |
| modified                | DateTime                                                              |
| patient                 | [Patient](/sdk/data-patient/#patient)                                 |
| originator              | [CanvasUser](/sdk/data-canvasuser)                                    |
| assigned_by             | [CanvasUser](/sdk/data-canvasuser)                                    |
| team                    | [Team](/sdk/data-team/#team)                                          |
| integration_task_review | [IntegrationTaskReview](/sdk/data-integration-task/#integrationtaskreview) |
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
| patient_consents        | QuerySet[[PatientConsent](/sdk/data-patient-consent/)]                |

### DocumentCoding

A coding entry representing the type of document. Also used by [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/#uncategorizedclinicaldocument).

| Field Name    | Type    |
|---------------|---------|
| dbid          | Integer |
| system        | String  |
| version       | String  |
| code          | String  |
| display       | String  |
| user_selected | Boolean |
