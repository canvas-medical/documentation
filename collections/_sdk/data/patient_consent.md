---
title: "PatientConsent"
slug: "data-patient-consent"
excerpt: "Canvas SDK PatientConsent"
hidden: false
---

## Introduction

The `PatientConsent` model represents documented patient consents in Canvas that ensure legal compliance and protect patient rights. Each `PatientConsent` is linked to a `Patient`, has a category (which is a `PatientConsentCoding`), and optionally a rejection reason (which is a `PatientConsentRejectionCoding`).

## Usage

The `PatientConsent` model can be used to find all of the patient consents for a given patient and organization:

```python
>>> from canvas_sdk.v1.data import PatientConsent, Patient, Organization
>>> patient_1 = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> organization_1 = Organization.objects.first()
>>> patient_1_consents = PatientConsent.objects.filter(patient=patient_1, organization=organization_1)
>>> print([consent.category.display for consent in patient_1_consents])
['Surgical Consent Form', 'Telehealth', 'HIPAA']
```

You can also access a patient's consents from the `Patient` model:

```python
>>> from canvas_sdk.v1.data import PatientConsent, Patient
>>> patient_1 = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> patient_1_consents = patient_1.patient_consent.all()
>>> print([consent.category.display for consent in patient_1_consents])
['Surgical Consent Form', 'Telehealth', 'HIPAA']
```

And you can also access all of the PatientConsents for a given PatientConsentCoding (aka category):

```python
>>> from canvas_sdk.v1.data import PatientConsentCoding
>>> coding = PatientConsentCoding.objects.get(code='59284-0', system='LOINC')
>>> consents = coding.patient_consent.all()
>>> print([consent.state for consent in consents])
['accepted', 'accepted_via_patient_portal', 'rejected']
```

Each `PatientConsentCoding` has a `document` field containing the URL to the consent template document:

```python
>>> from canvas_sdk.v1.data import PatientConsentCoding
>>> coding = PatientConsentCoding.objects.first()
>>> print(coding.document)
'consent_templates/hipaa_consent.pdf'
```

## Accessing Document Files

The `document_url` property returns a presigned S3 URL for securely accessing the consent form.

```python
from canvas_sdk.v1.data import PatientConsentCoding

consent_coding = PatientConsentCoding.objects.first()

# Returns a presigned S3 URL (valid for 1 hour)
url = consent_coding.document_url
```

## Signed consent documents

The `document` and `document_url` on a [PatientConsentCoding](#patientconsentcoding) (covered above) point at the blank consent *template*. The `documents`, `active_document`, and `document_references` attributes on a `PatientConsent` reach the patient's *signed* copies instead, stored as [PatientAdministrativeDocument](/sdk/data-patient-administrative-document/) records.

`documents` is a manager over the signed documents for a consent, so it supports the usual queryset methods:

```python
>>> from canvas_sdk.v1.data import PatientConsent
>>> consent = PatientConsent.objects.get(id="4c8f2a1e-6b3d-4f5a-9c21-8e7d0a1b2c3d")
>>> signed_documents = consent.documents.all()
>>> print([document.name for document in signed_documents])
['Signed HIPAA Consent', 'Signed Telehealth Consent']
```

`active_document` returns the most recent signed document that hasn't been junked (discarded), or `None` when the consent has none:

```python
>>> from canvas_sdk.v1.data import PatientConsent
>>> consent = PatientConsent.objects.get(id="4c8f2a1e-6b3d-4f5a-9c21-8e7d0a1b2c3d")
>>> active_document = consent.active_document
>>> print(active_document.name if active_document else None)
'Signed HIPAA Consent'
```

`document_references` returns the FHIR [DocumentReference](/sdk/data-document-reference/) records that point at those signed documents. Each one's [`related_object`](/sdk/data-document-reference/#the-related-object) resolves back to the `PatientAdministrativeDocument` it references:

```python
>>> from canvas_sdk.v1.data import PatientConsent
>>> consent = PatientConsent.objects.get(id="4c8f2a1e-6b3d-4f5a-9c21-8e7d0a1b2c3d")
>>> references = consent.document_references
>>> print([reference.related_object.name for reference in references])
['Signed HIPAA Consent', 'Signed Telehealth Consent']
```

## Attributes

### PatientConsent

| Field Name          | Type                                                                                                                                  |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| id                  | UUID                                                                                                                                  |
| dbid                | Integer                                                                                                                               |
| patient             | [Patient](/sdk/data-patient)                                                                                                          |
| category            | [PatientConsentCoding](#patientconsentcoding)                                                                                         |
| state               | [PatientConsentStatus](#patientconsentstatus)                                                                                         |
| effective_date      | DateTime                                                                                                                              |
| expired_date        | DateTime                                                                                                                              |
| rejection_reason    | [PatientConsentRejectionCoding](#patientconsentrejectioncoding)                                                                       |
| originator          | [CanvasUser](/sdk/data-canvasuser)                                                                                                    |
| documents           | QuerySet[[PatientAdministrativeDocument](/sdk/data-patient-administrative-document/)]                                                 |
| active_document     | [PatientAdministrativeDocument](/sdk/data-patient-administrative-document/) (property) — the current signed consent document, or None |
| document_references | QuerySet[[DocumentReference](/sdk/data-document-reference/)] (property) — DocumentReference records for the signed documents          |

### PatientConsentCoding

| Field Name             | Type                                                          |
| ---------------------- | ------------------------------------------------------------- |
| dbid                   | Integer                                                       |
| system                 | String                                                        |
| version                | String                                                        |
| code                   | String                                                        |
| display                | String                                                        |
| user_selected          | Boolean                                                       |
| expiration_rule        | [PatientConsentExpirationRule](#patientconsentexpirationrule) |
| is_mandatory           | Boolean                                                       |
| is_proof_required      | Boolean                                                       |
| show_in_patient_portal | Boolean                                                       |
| summary                | String                                                        |
| document               | String                                                        |
| document_url           | String (property) — presigned S3 URL                          |
| patient_consent        | QuerySet[[PatientConsent](#patientconsent)]                   |


### PatientConsentRejectionCoding

| Field Name    | Type    |
| ------------- | ------- |
| dbid          | Integer |
| system        | String  |
| version       | String  |
| code          | String  |
| display       | String  |
| user_selected | Boolean |
| patient_consents | QuerySet[[PatientConsent](#patientconsent)] |

## Enumeration types

### PatientConsentStatus

| Value                       | Label                       |
| --------------------------- | --------------------------- |
| accepted                    | Accepted                    |
| accepted_via_patient_portal | Accepted Via Patient Portal |
| rejected                    | Rejected                    |
| rejected_via_patient_portal | Rejected Via Patient Portal |

### PatientConsentExpirationRule

| Value       | Label       |
| ----------- | ----------- |
| never       | Never       |
| in_one_year | In one year |
| end_of_year | End of year |
