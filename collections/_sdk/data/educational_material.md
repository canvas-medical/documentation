---
title: "EducationalMaterial"
slug: "data-educational-material"
excerpt: "Patient educational material shared from a note via the Educational Material command."
hidden: false
---

## Introduction

The `EducationalMaterial` model represents patient educational material recorded on a note through the Educational Material command — the selected article, its title and abstract, and the languages it is available in. It is a read-only data model.

Records are returned regardless of command state, so staged commands are included; use `committed()` to limit results to committed commands.

## Basic Usage

`EducationalMaterial` records can be retrieved by their UUID `id`, their integer `dbid`, or through a patient.

```python
from canvas_sdk.v1.data import EducationalMaterial

# Get all educational material records
materials = EducationalMaterial.objects.all()

# Get a specific record by its UUID id
material = EducationalMaterial.objects.get(id="c9a7b1e2-d4f3-4e6a-8b5c-0d1e2f3a4b5c")
```

If you have a `Patient` object, its educational material records can be accessed with the `education_material` reverse relation:

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
materials = patient.education_material.all()
```

## Filtering

### By attribute

```python
from canvas_sdk.v1.data import EducationalMaterial

materials = EducationalMaterial.objects.filter(selected_language="en-us")
```

### Committed records

The `committed` method returns records that have been committed and not entered in error:

```python
from canvas_sdk.v1.data import EducationalMaterial

committed = EducationalMaterial.objects.committed()
```

## Accessing the article PDF

`EducationalMaterial` holds the article's metadata — its title, abstract, and languages — not the article file itself. When the command is committed, Canvas renders the article to a PDF and attaches it to a [DocumentReference](/sdk/data-document-reference/) with the LOINC type `34895-3` (Education note).

To read a patient's education note PDFs, filter `DocumentReference` by that type and use its `document_url`:

```python
from canvas_sdk.v1.data import DocumentReference

education_notes = DocumentReference.objects.for_patient(
    "1eed3ea2a8d546a1b681a2a45de1d790"
).filter(type__code="34895-3")

for note in education_notes:
    url = note.document_url
```

To resolve the PDF for one specific record, filter on the document's [related object](/sdk/data-document-reference/#the-related-object) instead. Resolve the [ContentType](/sdk/data-content-type/) at runtime from its stable `app_label` and `model` — never hardcode the per-environment `dbid` — and match `object_id` against the material's `dbid`:

```python
from canvas_sdk.v1.data import ContentType, DocumentReference, EducationalMaterial

material = EducationalMaterial.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

content_type = ContentType.objects.filter(
    app_label="api", model="educationalmaterial"
).first()

document = DocumentReference.objects.filter(
    content_type=content_type, object_id=material.dbid
).first()

url = document.document_url if document else None
```

{% include alert.html type="info" content="<code>object_id</code> holds the related record's integer <code>dbid</code>, not its UUID <code>id</code>, so filter on <code>material.dbid</code>." %}

## Attributes

### EducationalMaterial

| Field Name        | Type                                                        |
|-------------------|-------------------------------------------------------------|
| id                | UUID                                                        |
| dbid              | Integer                                                     |
| created           | DateTime                                                    |
| modified          | DateTime                                                    |
| originator        | [CanvasUser](/sdk/data-canvasuser)                          |
| committer         | [CanvasUser](/sdk/data-canvasuser)                          |
| entered_in_error  | [CanvasUser](/sdk/data-canvasuser)                          |
| patient           | [Patient](/sdk/data-patient/#patient)                       |
| note              | [Note](/sdk/data-note/#note)                                |
| article_id        | String                                                      |
| selected_language | [EducationalMaterialLanguage](#educationalmateriallanguage) |
| title             | String                                                      |
| languages         | String[]                                                    |
| abstract          | String                                                      |

`selected_language` defaults to `en-us`.

`languages` holds the locale codes the article is available in, drawn from the same set of codes as [EducationalMaterialLanguage](#educationalmateriallanguage). It is stored as a plain array of strings rather than an enum, so compare against the code values (`"es-us"`) rather than expecting enum members.

## Enumeration types

### EducationalMaterialLanguage

| Value | Label       |
|-------|-------------|
| en-us | English     |
| es-us | Spanish     |
| en-ca | English CA  |
| fr-ca | French CA   |
| fr-fr | French FR   |
| da-dk | Danish DK   |
| ar-eg | Arabic Egypt|
| ar-us | Arabic      |
| bn-us | Bengali     |
| bs-ba | Bosnian     |
| bs-us | Bosnian     |
| fa-ir | Farsi Iran  |
| fa-us | Farsi       |
| hr-hr | Croatian    |
| ht-us | Haitian     |
| ko-us | Korean      |
| ru-ru | Russian     |
| ru-us | Russian     |
| sr-us | Serbian     |
| so-so | Somalia     |
| so-us | Somalia     |
| tl-us | Tagalog     |
| vi-vn | Vietnamese  |
| vi-us | Vietnamese  |
| zh-cn | Chinese     |
| zh-us | Chinese     |
