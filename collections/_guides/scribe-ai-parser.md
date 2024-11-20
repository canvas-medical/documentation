---
title: "Creating, Implementing, and Extending a Scribe Parser"
guide_for:
- /sdk/quickstart/
- /sdk/canvas_cli/
- /sdk/events/
- /sdk/effects/
---

This guide explains how to work with the [Nabla Transcript Parser Plugin](https://github.com/Medical-Software-Foundation/canvas/tree/main/protocols/nabla-ai-parser) to parse structured transcripts, like the provided example, and generate commands from their sections. It also demonstrates how to create and integrate custom parsers to handle alternate transcript formats.

---

## Understanding the Transcript Parsing Flow

### Input Transcript Example

The transcript is structured into sections such as:
- **Chief complaint**
- **History of present illness**
- **Past medical history**
- **Vitals**
- **Plan**

Each section contains specific information that can be parsed into commands. For example:
- The **Vitals** section includes data like weight, heart rate, and blood pressure, which can be converted into a `VitalsCommand`.
- The **Assessment** section provides diagnoses and clinical impressions, which can be mapped to an `AssessCommand`.

<details markdown="1">
  <summary><b>Complete Example</b></summary>

    Chief complaint
    - Concern about potential diabetes
    - Hypertension
    
    History of present illness
    - Patient named Ken, age and gender not mentioned
    - Has sleep apnea, uses CPAP machine
    - Has hyperlipidemia
    - Has hypertension, on medication but doesn't remember the names
    - No other symptoms or issues reported
    - No shortness of breath or pain reported

    Past medical history
    - Sleep apnea
    - Hyperlipidemia
    - Hypertension

    Family history
    No known family history of hypertension

    Social history
    Travels a lot

    Current medications
    Medication for hypertension, names not provided

    Vitals
    - Weight: 244 lbs
    - Height: 5'10"
    - Heart rate: 80
    - Oxygen saturation: 94%
    - Blood pressure: 167/106

    Lab results
    A1C: 5.2 (Normal range, neither prediabetic nor diabetic)

    Physical exam
    CARDIOVASCULAR: Heart sounds good.
    LUNGS: Lungs sound good.

    Assessment
    - Hypertension, not well controlled
    - Sleep apnea, using CPAP machine
    - Hyperlipidemia
    - Elevated BMI, potential for weight loss intervention
    - No diabetes or prediabetes

    Plan
    - Recommendation for weight loss services
    - Recommendation to address hypertension, either at this clinic or with primary care
    - Potential adjustment of hypertension medication
    - Offered subscription program with unlimited office visits and access to a nutritionist
    - Potential telemedicine consultations due to patient's frequent travel

    Appointments
    No specific appointment made, patient to contact clinic after discussing with wife

    ICD-10 codes (3)
    - Sleep apnea, unspecified [G47.30]
    - Hyperlipidemia, unspecified [E78.5]
    - Essential (primary) hypertension [I10]
</details>

---

## Nabla Transcript Parser Plugin Architecture

### 1. Protocol Class

The `Protocol` class intercepts events and processes the transcript using a parser.

```python
class Protocol(BaseProtocol):
    """A Plugin for interpreting Nabla transcripts."""

    RESPONDS_TO = EventType.Name(EventType.CLIPBOARD_COMMAND__POST_ORIGINATE)

    def compute(self) -> list[Effect]:
        """Parse the transcript and generate effects to originate commands."""
        transcript = self.context["fields"]["text"]
        parser = NablaParser()
        parsed_transcript = parser.parse(transcript, self.context)
        note_uuid = self.context["note"]["uuid"]

        effects = []
        for commands in parsed_transcript.values():
            for command in commands:
                command.note_uuid = note_uuid
                effects.append(command.originate(line_number=1))

        effects.reverse()
        return effects
```

### 2. NablaParser

The `NablaParser` delegates the parsing of each transcript section to specific section parsers.

```python
class NablaParser(TranscriptParser):
    """A parser for Nabla transcripts."""

    section_parsers = {
        "chief_complaint": ChiefComplaintParser(),
        "history_of_present_illness": HistoryOfPresentIllnessParser(),
        "past_medical_history": PastMedicalHistoryParser(),
        "vitals": VitalsParser(),
        "plan": PlanParser(),
    }

    def parse(self, transcript: str, context: dict) -> dict:
        """Parse the transcript into commands grouped by sections."""
        parsed_sections = {}
        for section, parser in self.section_parsers.items():
            parsed_sections[section] = parser.parse(transcript, context)
        return parsed_sections
```

### 3. Section Parsers

Each section parser extracts relevant information from its section and produces commands.
```python
from typing import Any, Sequence
from nabla_ai_parser.parsers.base import CommandParser, ParsedContent
from canvas_sdk.commands.commands.plan import PlanCommand

class NablaPlanParser(CommandParser):
    """Parses the plan section of a Nabla transcript."""

    def parse(self, content: ParsedContent, context: Any = None) -> Sequence[PlanCommand]:
        """Parses the plan section of a Nabla transcript."""
        return [PlanCommand(narrative=line) for line in content["arguments"]]
````
---

## Extending the Parser

### 1. Adding a New Section Parser

Suppose you want to parse the "Appointments" section into a `TaskCommand` for follow-up tasks.

#### Define the Parser

```python
from typing import Sequence, Any
from canvas_sdk.commands import TaskCommand
from nabla_ai_parser.parsers.base import CommandParser, ParsedContent


class AppointmentsParser(CommandParser):
    """Parses the 'Appointments' section of a Nabla transcript."""

    def parse(self, content: ParsedContent, context: Any = None) -> Sequence[TaskCommand]:
        """Parses the Appointments section and generates TaskCommands."""
        tasks = []
        for line in content["arguments"]:
            tasks.append(TaskCommand(title=line))
        return tasks
```

#### Register the Parser

Add the `AppointmentsParser` to the `section_parsers` dictionary.

```python
class NablaParser:
    """A parser for Nabla transcripts."""
    
    section_parsers = {
        "plan": NablaPlanParser(),
        "vitals": NablaVitalsParser(),
        "chief_complaint": NablaReasonForVisitParser(),
        "history_of_present_illness": NablaHistoryPresentIllnessParser(),
        "past_medical_history": NablaPastMedicalHistoryParser(),
        "assessment": AssessmentParser(),
        "appointments": AppointmentsParser()
    }
```

---

### 2. Customizing the Entire Parser

To replace `NablaParser`, define your custom parser.

```python
from nabla_ai_parser.parsers.base import (
    ParsedContent,
    TranscriptParser,
    TranscriptParserOutput,
)

class CustomParser(TranscriptParser):
    """Custom parser for alternative transcript formats."""

    def parse(self, transcript: str, context: dict) -> dict:
        """Parse the transcript and produce commands."""
        # Implement custom parsing logic
        ...
```

Replace the parser in the `Protocol` class:

```python
class Protocol(BaseProtocol):
    """Protocol using a custom parser."""

    def compute(self) -> list[Effect]:
        transcript = self.context["fields"]["text"]
        parser = CustomParser()  # Use custom parser
        parsed_transcript = parser.parse(transcript, self.context)
        note_uuid = self.context["note"]["uuid"]

        effects = []
        for commands in parsed_transcript.values():
            for command in commands:
                command.note_uuid = note_uuid
                effects.append(command.originate(line_number=1))

        effects.reverse()
        return effects
```

---

## Summary

- **Parsing Workflow**:
  - Intercept [`CLIPBOARD_COMMAND__POST_ORIGINATE`](/sdk/events/#clipboard-command).
  - Use `NablaParser` (or custom parsers) to process transcripts.
  - Generate commands for each section.

- **Extensibility**:
  - Add or replace section parsers for custom sections.
  - Implement a fully custom parser for alternate formats.

