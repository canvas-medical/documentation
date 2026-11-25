---
title: "Letter"
slug: "data-letter"
excerpt: "Canvas SDK Letter"
hidden: false
---

## Introduction

The `Letter` model represents patient correspondence letters created within Canvas. Letters are associated with a [Note](/sdk/data-note/) and contain rendered content that can be printed or sent to patients.

## Basic Usage

### Retrieve a specific letter

To get a letter by identifier, use the `get` method on the `Letter` model manager:

```python
from canvas_sdk.v1.data.letter import Letter

letter = Letter.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")
```

### Find a letter for a specific note

If you have a note object, you can access its associated letter using the `letter` attribute:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
letter = note.letter
```

### Find all letters created by a staff member

If you have a staff object, you can find all letters they created using the `letters` attribute:

```python
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="a1b2c3d4e5f6")
staff_letters = staff.letters.all()
```

## Filtering

Letters can be filtered by any attribute that exists on the model.

### By attribute

Filtering for letters is done with the `filter` method on the `Letter` model manager:

```python
from canvas_sdk.v1.data.letter import Letter

# Find all printed letters
printed_letters = Letter.objects.filter(printed__isnull=False)

# Find letters created by a specific staff member
staff_letters = Letter.objects.filter(staff_id="a1b2c3d4e5f6")
```

## The printed attachments

`printed_document` holds the letter's attachments, merged into one PDF, not the letter body. Canvas saves it the first time the letter is printed or faxed, and reuses it for later prints and faxes. The `printed_document_url` property returns a presigned S3 URL for that PDF, or `None` when the letter hasn't been printed or faxed. The URL is valid for one hour, so generate it when you need it rather than storing it.

```python
from canvas_sdk.v1.data.letter import Letter

letter = Letter.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")

# Presigned S3 URL to the merged attachments PDF, or None
attachments_url = letter.printed_document_url
```

To read the full letter as it went out, use its document reference.

## The document reference

`content` holds the letter's body, not the document that goes out. Canvas renders the letter — including anything attached to it — to a PDF and stores it on a [DocumentReference](/sdk/data-document-reference/#the-related-object) pointing back at the letter.

To read that PDF, resolve the [ContentType](/sdk/data-content-type/) at runtime from its stable `app_label` and `model` — never hardcode the per-environment `dbid` — and match `object_id` against the letter's `dbid`:

```python
from canvas_sdk.v1.data import ContentType, DocumentReference, Letter

letter = Letter.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

content_type = ContentType.objects.filter(app_label="api", model="letter").first()

document = DocumentReference.objects.filter(
    content_type=content_type, object_id=letter.dbid
).first()

url = document.document_url if document else None
```

{% include alert.html type="info" content="<code>object_id</code> holds the related record's integer <code>dbid</code>, not its UUID <code>id</code>. The PDF is rendered after the letter is created rather than with it, so handle <code>None</code>." %}

## Attached documents

Each document attached to a letter is a `LetterDocument`, available through the letter's `documents` attribute. `label` holds the name shown for the attachment. The `related_object` property returns the attached record as its SDK model: a [LabReport](/sdk/data-labs/#labreport), [ImagingReport](/sdk/data-imaging/#imagingreport), [ReferralReport](/sdk/data-referral/#referralreport), [PatientAdministrativeDocument](/sdk/data-patient-administrative-document/), [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/), [Note](/sdk/data-note/), [PatientChartDocument](#patientchartdocument), [Coverage](/sdk/data-coverage/#coverage), or [PatientIdentificationCard](/sdk/data-patient/#patientidentificationcard). It returns `None` when the record isn't available through the SDK, such as when it was deleted.

```python
from canvas_sdk.v1.data import Letter

letter = Letter.objects.prefetch_related("documents").get(
    id="b5a0c1d2-e3f4-5678-9abc-def012345678"
)

for attachment in letter.documents.all():
    record = attachment.related_object
    print(attachment.label, type(record).__name__ if record else None)
```

A `PatientChartDocument` is a page of the patient's chart that staff can attach to a letter. Every instance has the same four pages, all active:

| `name` | `url` |
|--------|-------|
| `Chart summary` | `api/Patient/{key}.html?&usage=chart_summary&audience=care_team` |
| `Basic information` | `api/Patient/{key}.html?&usage=patient_basic_information&audience=care_team` |
| `Medications and allergies` | `api/Patient/{key}.html?&usage=medication_allergy_list&audience=care_team` |
| `Integrated care plan` | `api/CarePlan/{key}.html` |

`{key}` in `url` is a placeholder for the patient's `id`. To find which chart page a letter attachment is, compare its `name`:

```python
from canvas_sdk.v1.data import Letter, PatientChartDocument

letter = Letter.objects.prefetch_related("documents").get(
    id="b5a0c1d2-e3f4-5678-9abc-def012345678"
)

for attachment in letter.documents.all():
    record = attachment.related_object
    if isinstance(record, PatientChartDocument) and record.name == "Chart summary":
        print("The letter includes the chart summary")
```

When an attached lab, imaging, or referral report, or an administrative or uncategorized clinical document, has been annotated, Canvas prints its newest [DocumentAnnotation](/sdk/data-document-annotation/) in place of the original file.

## Letter templates

A letter written from a template points to it through `template`. That's a `LetterLanguageTemplate`: the header, content, and footer of a [LetterTemplate](#lettertemplate) in one language. `template` is `None` for a letter that wasn't written from a template. A [Message](/sdk/data-message/#message) written from a template points to one the same way.

```python
from canvas_sdk.v1.data import Letter

letter = Letter.objects.get(id="b5a0c1d2-e3f4-5678-9abc-def012345678")

if letter.template:
    template_name = letter.template.template.name
    language_code = letter.template.language.code
```

A `LetterTemplate` holds one `LetterLanguageTemplate` per language in `template_languages`. `template_type` lists the kinds of document the template is for, as [LetterTemplateType](#lettertemplatetype) values. `locations` lists the `dbid` values, as strings, of the [practice locations](/sdk/data-practicelocation/#practicelocation) the template is limited to. An empty list means the template is available at every active practice location.

```python
from canvas_sdk.v1.data import LetterTemplate, LetterTemplateType

templates = LetterTemplate.objects.filter(
    active=True, template_type__contains=[LetterTemplateType.LETTER]
)

for template in templates:
    english = template.template_languages.filter(language__code="en").first()
```

## Attributes

### Letter

| Field Name | Type                            | Notes                              |
|------------|---------------------------------|------------------------------------|
| id         | UUID                            |                                    |
| dbid       | Integer                         |                                    |
| created    | DateTime                        |                                    |
| modified   | DateTime                        |                                    |
| content    | String                          | The rendered letter content        |
| printed    | DateTime                        | When the letter was last printed, set after its print PDF renders (null if not printed). A print that fails to render leaves it unchanged. |
| printed_document | File (S3 key)             | The letter's attachments merged into one PDF, saved when the letter is first printed or faxed (null until then) |
| printed_document_url | String (computed)     | Presigned S3 URL for `printed_document`, or `None` if unset |
| note       | [Note](/sdk/data-note/)         | The note this letter is associated with |
| staff      | [Staff](/sdk/data-staff/#staff) | The staff member who created the letter (nullable) |
| template   | [LetterLanguageTemplate](#letterlanguagetemplate) | The template the letter was written from (nullable) |
| letter_action_events | QuerySet[LetterActionEvent] | Action events (e.g. printed, faxed) recorded for this letter |
| documents  | [LetterDocument](#letterdocument)[] | The documents attached to the letter |

### LetterDocument

| Field Name     | Type                                   | Notes |
|----------------|----------------------------------------|-------|
| dbid           | Integer                                |       |
| created        | DateTime                               |       |
| modified       | DateTime                               |       |
| letter         | [Letter](#letter)                      | The letter the document is attached to |
| label          | String                                 | The name shown for the attachment |
| category       | String                                 |       |
| content_type   | [ContentType](/sdk/data-content-type/) | The type of the attached record |
| object_id      | Integer                                | The `dbid` of the attached record |
| related_object | [LabReport](/sdk/data-labs/#labreport), [ImagingReport](/sdk/data-imaging/#imagingreport), [ReferralReport](/sdk/data-referral/#referralreport), [PatientAdministrativeDocument](/sdk/data-patient-administrative-document/), [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/), [Note](/sdk/data-note/), [PatientChartDocument](#patientchartdocument), [Coverage](/sdk/data-coverage/#coverage), or [PatientIdentificationCard](/sdk/data-patient/#patientidentificationcard) (computed) | The attached record, or `None` |

### PatientChartDocument

| Field Name | Type     | Notes |
|------------|----------|-------|
| dbid       | Integer  |       |
| created    | DateTime |       |
| modified   | DateTime |       |
| name       | String   | The chart page's name: `Chart summary`, `Basic information`, `Medications and allergies`, or `Integrated care plan` |
| url        | String   | A path template with a `{key}` placeholder for the patient's `id`. See [Attached documents](#attached-documents). |
| is_active  | Boolean  | Whether staff can attach the page to a letter. `True` for all four pages. |

### LetterTemplate

| Field Name         | Type                                                        | Notes |
|--------------------|-------------------------------------------------------------|-------|
| id                 | UUID                                                        |       |
| dbid               | Integer                                                     |       |
| created            | DateTime                                                    |       |
| modified           | DateTime                                                    |       |
| name               | String                                                      |       |
| active             | Boolean                                                     |       |
| restrict_editing   | Boolean                                                     | When `True`, users can't change the template's text in a letter written from it |
| template_type      | [LetterTemplateType](#lettertemplatetype)[]                 | The kinds of document the template is for |
| locations          | String[]                                                    | `dbid` values of the practice locations the template is limited to. Empty means every active practice location. |
| template_languages | QuerySet[[LetterLanguageTemplate](#letterlanguagetemplate)] | The template's content in each language |

### LetterLanguageTemplate

| Field Name | Type                              | Notes |
|------------|-----------------------------------|-------|
| id         | UUID                              |       |
| dbid       | Integer                           |       |
| created    | DateTime                          |       |
| modified   | DateTime                          |       |
| template   | [LetterTemplate](#lettertemplate) |       |
| language   | Language                          | Has a `code`, such as `en`, and a `description` |
| header     | String                            |       |
| content    | String                            |       |
| footer     | String                            |       |
| letters    | QuerySet[[Letter](#letter)]       | Letters written from this template |
| messages   | QuerySet[[Message](/sdk/data-message/#message)] | Messages written from this template |

## Enumeration types

### LetterTemplateType

| Value          | Label        |
|----------------|--------------|
| `intervention` | Intervention |
| `letter`       | Letter       |
| `message`      | Message      |
