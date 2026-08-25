---
title: "Instruction"
slug: "data-instruction"
excerpt: "Canvas SDK Instruction"
hidden: false
---

## Introduction

The `Instruction` model represents an `Instruct` command in a patient's note — for example, "cessation of smoking" counseling, dietary instructions, or any other piece of clinical guidance recorded as an Instruct command. Instructions are included regardless of command state (staged or committed); use `.committed()` to filter to only committed commands.

Querying `Instruction` from a plugin is the recommended way to ask "has this patient been given an instruction in this value set?" — for example, when computing quality measures that look for tobacco cessation counseling or dialysis education.

## Basic usage

To get an instruction by identifier, use the `get` method on the `Instruction` model manager:

```python
from canvas_sdk.v1.data.instruction import Instruction

instruction = Instruction.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the instructions for a patient can be accessed with the `instructions` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")

# Returns all instructions for the patient, regardless of command state (staged or committed)
instructions = patient.instructions.all()
```

If you have a patient ID, you can get the instructions for the patient with the `for_patient` method on the `Instruction` model manager:

```python
from canvas_sdk.v1.data.instruction import Instruction

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"

# All instructions for the patient, regardless of command state (staged or committed)
instructions = Instruction.objects.for_patient(patient_id)

# Only committed instructions for the patient
committed_instructions = Instruction.objects.for_patient(patient_id).committed()
```

## Codings

The codings for an instruction can be accessed with the `codings` attribute on an `Instruction` object:

```python
from canvas_sdk.v1.data.instruction import Instruction
from logger import log

instruction = Instruction.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in instruction.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

Instruct commands originated through the SDK use either the SNOMED CT code system or an internal "unstructured" system for free-text instructions. See the [InstructCommand](/sdk/commands/#instruct) effect for the write-side details.

## Committed instructions

The `committed` method returns instructions whose underlying command has been committed and not entered in error:

```python
from canvas_sdk.v1.data.instruction import Instruction

committed_instructions = Instruction.objects.committed()
```

## Filtering

Instructions can be filtered by any attribute that exists on the model.

Filtering for instructions is done with the `filter` method on the `Instruction` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.instruction import Instruction

instructions = Instruction.objects.filter(note__id="2c91b0d8-7b9d-4ef1-89e2-1f9a3a8a2b14")
```

### By ValueSet

See [Value Sets](/sdk/data-value-sets/) for the library of built-in value sets and how to create your own.

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.instruction import Instruction
from canvas_sdk.value_set.v2022.intervention import TobaccoUseCessationCounseling

cessation_counseling = (
    Instruction.objects
    .for_patient("1eed3ea2a8d546a1b681a2a45de1d790")
    .committed()
    .find(TobaccoUseCessationCounseling)
)
```

`find` joins through the `codings` reverse relation and filters on `(system, code)` pairs from the value set, so it composes naturally with `for_patient` and `committed`.

## Attributes

### Instruction

| Field Name       | Type                                        |
|------------------|---------------------------------------------|
| id               | UUID                                        |
| dbid             | Integer                                     |
| created          | DateTime                                    |
| modified         | DateTime                                    |
| originator       | [CanvasUser](/sdk/data-canvasuser)          |
| committer        | [CanvasUser](/sdk/data-canvasuser)          |
| entered_in_error | [CanvasUser](/sdk/data-canvasuser)          |
| patient          | [Patient](/sdk/data-patient/#patient)       |
| note             | [Note](/sdk/data-note/#note)                |
| narrative        | String                                      |
| codings          | [InstructionCoding](#instructioncoding)[]   |

### InstructionCoding

| Field Name    | Type                        |
|---------------|-----------------------------|
| dbid          | Integer                     |
| system        | String                      |
| version       | String                      |
| code          | String                      |
| display       | String                      |
| user_selected | Boolean                     |
| instruction   | [Instruction](#instruction) |

<br/>
<br/>
<br/>
