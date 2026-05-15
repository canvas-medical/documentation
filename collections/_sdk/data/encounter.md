---
title: "Encounter"
slug: "data-encounter"
excerpt: "Canvas SDK Encounter"
hidden: false
---

## Introduction

The `Encounter` model represents a patient encounter connected to a Note in Canvas.

## Basic usage

To get an encounter by identifier, use the `get` method on the `Encounter` model manager:

```python
from canvas_sdk.v1.data import Encounter

encounter = Encounter.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

To get an encounter from a note, use the `encounter` attribute on the `Note` object:

```python
from canvas_sdk.v1.data import Note

note = Note.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
encounter = note.encounter
```

Keep in mind that not all notes have an associated encounter, so sometimes `note.encounter` will be `None`.

Similary, you can get a note from an `Encounter` object by using the `note` attribute:

```python
from canvas_sdk.v1.data import Encounter

encounter = Encounter.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
note = encounter.note
```

All encounters will have an associated note, which means `encounter.note` will never be `None`.

## Filtering

Encounters can be filtered by any attribute that exists on the model.

Filtering for encounters is done with the `filter` method on the `Encounter` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.encounter import Encounter, EncounterState

encounters = Encounter.objects.filter(state=EncounterState.CONCLUDED)
```

## Attributes

### Encounter

| Field Name | Type                                |
| ---------- | ----------------------------------- |
| id         | UUID                                |
| dbid       | Integer                             |
| created    | DateTime                            |
| modified   | DateTime                            |
| note       | [Note](/sdk/data-note/)             |
| state      | [EncounterState](#encounterstate)   |
| medium     | [EncounterMedium](#encountermedium) |
| start_time | DateTime                            |
| end_time   | DateTime                            |

## Enumeration types

### EncounterState

| Name      | Value |
| --------- | ----- |
| STARTED   | STA   |
| PLANNED   | PLA   |
| CONCLUDED | CON   |
| CANCELLED | CAN   |

### EncounterMedium

| Name    | Value   |
| ------- | ------- |
| VOICE   | voice   |
| VIDEO   | video   |
| OFFICE  | office  |
| HOME    | home    |
| OFFSITE | offsite |
| LAB     | lab     |

<br/>
<br/>
<br/>
