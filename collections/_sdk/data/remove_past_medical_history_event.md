---
title: "Remove Past Medical History Event"
slug: "data-remove-past-medical-history-event"
excerpt: "Canvas SDK Remove Past Medical History Event"
hidden: false
---

## Introduction

The `RemovePastMedicalHistoryEvent` model records an entry being removed from a patient's past medical history. It is the anchor for the [Remove Past Medical History](/sdk/commands/#remove-past-medical-history) command. Use it to find which past medical history entries were removed, on which note, and why.

## Basic usage

To get a remove past medical history event by identifier, use the `get` method on the `RemovePastMedicalHistoryEvent` model manager:

```python?partial=true
from canvas_sdk.v1.data import RemovePastMedicalHistoryEvent

removal = RemovePastMedicalHistoryEvent.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
```

If you have a patient object, the remove past medical history events for a patient can be accessed with the `removed_past_medical_history` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
removals = patient.removed_past_medical_history.all()
```

The same records are reachable from the note they were recorded on, with the `removed_past_medical_history` attribute on a `Note` object:

```python
from canvas_sdk.v1.data.note import Note

note = Note.objects.get(id="89992c23-c298-4118-864a-26cb3e1ae822")
removals = note.removed_past_medical_history.all()
```

You can also access the removed entry with the `condition` attribute. It can be `None`, so check it before use:

```python?partial=true
from canvas_sdk.v1.data import RemovePastMedicalHistoryEvent

removal = RemovePastMedicalHistoryEvent.objects.get(id="61a1853f-168f-4ed3-80d2-44e5d144bcf3")
condition = removal.condition
```

Or for a given condition, you can access all of its removal events with the `past_medical_history_removals` attribute:

```python
from canvas_sdk.v1.data import Condition

condition = Condition.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
removals = condition.past_medical_history_removals.all()
```

## Filtering

The `committed` method returns remove past medical history events that have been committed and not entered in error. The `for_patient` method returns the events for one patient. You can chain them:

```python?partial=true
from canvas_sdk.v1.data import RemovePastMedicalHistoryEvent

committed_removals = RemovePastMedicalHistoryEvent.objects.committed()

patient_removals = RemovePastMedicalHistoryEvent.objects.for_patient(
    "1eed3ea2a8d546a1b681a2a45de1d790"
).committed()
```

## Attributes

### RemovePastMedicalHistoryEvent

| Field Name       | Type                                  | Description |
| ---------------- | ------------------------------------- | ----------- |
| id               | UUID                                  | |
| dbid             | Integer                               | |
| created          | DateTime                              | |
| modified         | DateTime                              | |
| originator       | [CanvasUser](/sdk/data-canvasuser)    | |
| committer        | [CanvasUser](/sdk/data-canvasuser)    | |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)    | |
| patient          | [Patient](/sdk/data-patient/#patient) | |
| note             | [Note](/sdk/data-note)                | |
| condition        | [Condition](/sdk/data-condition)      | The removed past medical history entry. Can be `None`. |
| rationale        | String                                | The reason for the removal, up to 512 characters. Empty when none was given. |

<br/>
<br/>
<br/>
