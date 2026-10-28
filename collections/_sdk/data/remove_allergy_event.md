---
title: "Remove Allergy Event"
slug: "data-remove-allergy-event"
excerpt: "Canvas SDK Remove Allergy Event"
hidden: false
---

## Introduction

The `RemoveAllergyEvent` model represents a record of an allergy being removed from a patient's allergy list — the anchor for the [Remove Allergy](/sdk/commands/#removeallergy) command.

## Basic usage

To get a remove allergy event by identifier, use the `get` method on the `RemoveAllergyEvent` model manager:

```python?partial=true
from canvas_sdk.v1.data import RemoveAllergyEvent

removal = RemoveAllergyEvent.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
```

If you have a patient object, the remove allergy events for a patient can be accessed with the `removed_allergies` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
removals = patient.removed_allergies.all()
```

The same records are reachable from the note they were recorded on, with the `removed_allergies` attribute on a `Note` object:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
removals = note.removed_allergies.all()
```

You can also access the removed allergy with the `allergy` attribute:

```python?partial=true
from canvas_sdk.v1.data import RemoveAllergyEvent

removal = RemoveAllergyEvent.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
allergy = removal.allergy
```

Or for a given allergy, you can access all of its removal events with the `remove_allergy_events` attribute:

```python
from canvas_sdk.v1.data import AllergyIntolerance

allergy = AllergyIntolerance.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
removals = allergy.remove_allergy_events.all()
```

## Committed records

The `committed` method returns remove allergy events that have been committed and not entered in error:

```python?partial=true
from canvas_sdk.v1.data import RemoveAllergyEvent

committed_removals = RemoveAllergyEvent.objects.committed()
```

## Attributes

### RemoveAllergyEvent

| Field Name       | Type                                                       |
| ---------------- | ---------------------------------------------------------- |
| id               | UUID                                                       |
| dbid             | Integer                                                    |
| created          | DateTime                                                   |
| modified         | DateTime                                                   |
| originator       | [CanvasUser](/sdk/data-canvasuser)                        |
| committer        | [CanvasUser](/sdk/data-canvasuser)                        |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)                        |
| patient          | [Patient](/sdk/data-patient/#patient)                     |
| note             | [Note](/sdk/data-note)                                    |
| allergy          | [AllergyIntolerance](/sdk/data-allergy-intolerance)       |
| rationale        | String                                                     |

<br/>
<br/>
<br/>
