---
title: "Creating, Implementing, and Extending an AI Scribe Parser"
guide_for:
- /sdk/quickstart/
- /sdk/canvas_cli/
- /sdk/events/
- /sdk/effects/
---

The [AI Scribe Parser Plugin](https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/ai-scribe) was designed to help streamline clinical documentation by parsing structured transcripts into commands. With healthcare providers increasingly adopting AI-driven solutions, this guide provides developers with the insights and instructions needed to integrate and extend our example plugin to meet diverse documentation needs. In this guide, you'll learn how to:

  - Intercept [`CLIPBOARD_COMMAND__POST_INSERTED_INTO_NOTE`](/sdk/events/#clipboard-command).
  - Use `ScribeParser` (or custom parsers) to process transcripts.
  - Generate commands for each section.
  - Add or replace section parsers for custom sections.
  - Implement a fully custom parser for alternate formats.

## Understanding the Transcript Parsing Flow. 
The workflow is triggered by pasting a transcript into a note. Doing so will automatically insert the content in the form of a clipboard command. We can then respond to that event and transform the content into the appropriate commands. 

### Input Transcript Example

Our example transcript includes many structured sections. The sections listed below were flagged as being formatted in a way that makes them easy to translate into Canvas commands.

- Chief complaint
- History of present illness
- Past medical history
- Vitals
- Plan

Each section contains specific information that can be parsed. For example:
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


### AI Scribe Plugin Architecture
Once the content is pasted in, the plugin does the rest. Here's how. 

#### 1. Protocol Class

The `Protocol` class intercepts events and processes the transcript using a parser.

```python
class Protocol(BaseProtocol):
    """A Plugin for interpreting transcripts."""

    RESPONDS_TO = EventType.Name(EventType.CLIPBOARD_COMMAND__POST_INSERTED_INTO_NOTE)

    def compute(self) -> list[Effect]:
        """Parse the transcript and generate effects to originate commands."""
        transcript = self.context["fields"]["text"]
        parser = ScribeParser()
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

#### 2. ScribeParser

The `ScribeParser` delegates the parsing of each transcript section to specific section parsers.

```python
class ScribeParser(TranscriptParser):
    """A parser for scribe transcripts."""

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

#### 3. Section Parsers

Each section parser extracts relevant information from its section and produces commands.
```python
from typing import Any, Sequence
from ai_scribe.parsers.base import CommandParser, ParsedContent
from canvas_sdk.commands.commands.plan import PlanCommand

class PlanParser(CommandParser):
    """Parses the plan section of a transcript."""

    def parse(self, content: ParsedContent, context: Any = None) -> Sequence[PlanCommand]:
        """Parses the plan section of a transcript."""
        return [PlanCommand(narrative=line) for line in content["arguments"]]
```

## Extending the Parser
### 1. Adding a New Section Parser

Suppose you want to parse the "Appointments" section into a `TaskCommand` for follow-up tasks.

#### Define the Parser

```python
from typing import Sequence, Any
from canvas_sdk.commands import TaskCommand
from ai_scribe.parsers.base import CommandParser, ParsedContent


class AppointmentsParser(CommandParser):
    """Parses the 'Appointments' section of a transcript."""

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
class ScribeParser:
    """A parser for transcripts."""
    
    section_parsers = {
        "plan": PlanParser(),
        "vitals": VitalsParser(),
        "chief_complaint": ReasonForVisitParser(),
        "history_of_present_illness": HistoryPresentIllnessParser(),
        "past_medical_history": PastMedicalHistoryParser(),
        "assessment": AssessmentParser(),
        "appointments": AppointmentsParser()
    }
```

### 2. Customizing the Entire Parser

To replace `ScribeParser`, define your custom parser.

```python
from ai_scribe.parsers.base import (
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
## Watch the Workflow in Action

<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/fd129849fc784bb0850b93977d76ce07?sid=f0ccbd1b-5687-4f8a-baa5-2efe9494f18d" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## Conclusion

With robust parsing capabilities and extensibility, this example plugin equips developers to support clinicians in reclaiming their time for what matters most: patient care. By following the steps in this guide, developers can ensure seamless integration into clinical workflows, while also tailoring the tool to suit specific needs.





