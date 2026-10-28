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

## Attributes

### Letter

| Field Name | Type                            | Notes                              |
|------------|---------------------------------|------------------------------------|
| id         | UUID                            |                                    |
| dbid       | Integer                         |                                    |
| created    | DateTime                        |                                    |
| modified   | DateTime                        |                                    |
| content    | String                          | The rendered letter content        |
| printed    | DateTime                        | When the letter was printed (null if not printed) |
| printed_document | File (S3 key)             | The letter's attachments merged into one PDF, saved when the letter is first printed or faxed (null until then) |
| printed_document_url | String (computed)     | Presigned S3 URL for `printed_document`, or `None` if unset |
| note       | [Note](/sdk/data-note/)         | The note this letter is associated with |
| staff      | [Staff](/sdk/data-staff/#staff) | The staff member who created the letter (nullable) |
| letter_action_events | QuerySet[LetterActionEvent] | Action events (e.g. printed, faxed) recorded for this letter |