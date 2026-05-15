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
| note       | [Note](/sdk/data-note/)         | The note this letter is associated with |
| staff      | [Staff](/sdk/data-staff/#staff) | The staff member who created the letter (nullable) |