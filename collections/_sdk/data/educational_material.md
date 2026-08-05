---
title: "EducationalMaterial"
slug: "data-educational-material"
excerpt: "Canvas SDK EducationalMaterial"
hidden: false
---

## Introduction

The `EducationalMaterial` model represents an Educational Material command recorded on a patient's chart, backed by a coded material from a Canvas-hosted materials library. `EducationalMaterial` is a read-only data model. It carries a title, an abstract, a selected display language, and the list of languages the material is available in. Records are included regardless of command state (staged or committed); use `.committed()` to filter to only committed commands. When shared, the material surfaces to the patient portal as a FHIR [DocumentReference](/api/documentreference/) with category `educationalmaterial`.

## Basic usage

To get an educational material by identifier, use the `get` method on the `EducationalMaterial` model manager:

```python
from canvas_sdk.v1.data import EducationalMaterial

educational_material = EducationalMaterial.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the educational materials for a patient can be accessed with the `education_material` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
educational_materials = patient.education_material.all()
```

## Filtering

Educational materials can be filtered by any attribute that exists on the model.

Filtering for educational materials is done with the `filter` method on the `EducationalMaterial` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data import EducationalMaterial

educational_materials = EducationalMaterial.objects.filter(selected_language="en-us")
```

### Committed educational materials

The `committed` method returns educational materials whose underlying command has been committed and not entered in error:

```python
from canvas_sdk.v1.data import EducationalMaterial

committed_educational_materials = EducationalMaterial.objects.committed()
```

## Attributes

### EducationalMaterial

| Field Name        | Type                                                                    |
|-------------------|-------------------------------------------------------------------------|
| id                | UUID                                                                    |
| dbid              | Integer                                                                 |
| created           | DateTime                                                                |
| modified          | DateTime                                                                |
| originator        | [CanvasUser](/sdk/data-canvasuser)                                      |
| committer         | [CanvasUser](/sdk/data-canvasuser)                                      |
| entered_in_error  | [CanvasUser](/sdk/data-canvasuser)                                      |
| deleted           | Boolean                                                                 |
| patient           | [Patient](/sdk/data-patient/#patient)                                   |
| note              | [Note](/sdk/data-note/#note)                                            |
| article_id        | String                                                                  |
| selected_language | [EducationalMaterialLanguage](#educationalmateriallanguage)             |
| title             | String                                                                  |
| languages         | [EducationalMaterialLanguage](#educationalmateriallanguage)[]           |
| abstract          | String                                                                  |

## Enumeration types

### EducationalMaterialLanguage

`EducationalMaterialLanguage` is a `TextChoices` enumeration of 26 locale codes; `selected_language` holds one of these values, while `languages` holds a list of such codes. The `languages` field is a plain character array and is not enum-validated against `EducationalMaterialLanguage`.

A representative sample of the available values:

| Value | Language                  |
|-------|---------------------------|
| en-us | English (United States)   |
| es-us | Spanish (United States)   |
| fr-ca | French (Canada)           |
| ar-eg | Arabic (Egypt)            |
| zh-cn | Chinese (China)           |

<br/>
<br/>
<br/>
