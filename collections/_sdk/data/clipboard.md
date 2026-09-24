---
title: "Clipboard"
slug: "data-clipboard"
excerpt: "Canvas SDK Clipboard"
hidden: false
---

## Introduction

The `Clipboard` model is a read-only record of a Clipboard command. It holds free-text content staged on a patient's note, such as a pasted transcript or summary. A plugin queries it to read that content along with the patient and note the text belongs to.

Clipboards are included regardless of command state (staged or committed); use `committed()` to filter to only committed commands. A plugin does not write clipboard content through this model. That content is recorded through the Clipboard command.

## Basic usage

To get a clipboard by identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data import Clipboard

clipboard = Clipboard.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

The staged content is on the `text` attribute:

```python?partial=true
from canvas_sdk.v1.data import Clipboard

clipboard = Clipboard.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
text = clipboard.text
```

The manager is read-only, so there is no create or save. `get`, `filter`, and `committed` are available on it.

## Accessing clipboards from a patient or note

The clipboards for a patient or note are reachable through the `clipboards` reverse accessor, which is named the same on `Patient` and on `Note`:

```python
from canvas_sdk.v1.data import Note, Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
patient_clipboards = patient.clipboards.all()

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
note_clipboards = note.clipboards.all()
```

## Committed clipboards

The `committed` method returns records whose underlying command has been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import Clipboard

committed_clipboards = Clipboard.objects.committed()
```

## Filtering

Clipboards can be filtered by any attribute on the model with the `filter` method:

```python?partial=true
from canvas_sdk.v1.data import Clipboard

clipboards = Clipboard.objects.filter(note__id="2c91b0d8-7b9d-4ef1-89e2-1f9a3a8a2b14")
```

## Attributes

### Clipboard

| Field Name       | Type                                  |
| ---------------- | ------------------------------------- |
| id               | UUID                                  |
| dbid             | Integer                               |
| created          | DateTime                              |
| modified         | DateTime                              |
| originator       | [CanvasUser](/sdk/data-canvasuser)    |
| committer        | [CanvasUser](/sdk/data-canvasuser)    |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)    |
| patient          | [Patient](/sdk/data-patient/#patient) |
| note             | [Note](/sdk/data-note)                |
| text             | String                                |

<br/>
<br/>
<br/>
