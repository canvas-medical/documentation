---
title: "Pre-filling Questionnaires with an AI Scribe Parser"
guide_for:
- /sdk/events/
- /sdk/effects/
- /sdk/questionnaires/
---

<!-- sources: discussion #992 -->

This guide extends [Creating, Implementing, and Extending an AI Scribe Parser](/guides/scribe-ai-parser/). The base AI Scribe parser only ever *originates* commands. To pre-fill a [Questionnaire](/sdk/questionnaires/) command with parsed values — so the answers actually appear in the note UI — a section parser must return command *effects* in a specific order, and the event handler must be taught to pass those effects through.

## Why originate alone is not enough

Adding responses with `question.add_response(...)` updates the command object, but those responses only render in the UI if the command is both originated **and** edited. Pre-filling therefore requires two effects: `originate()` to create the command and `edit()` to apply the responses. The handler that invokes the parser reverses the effect order, so the parser returns them in reverse — `edit()` before `originate()` — so they end up in the correct order after the reversal.

## The custom section parser

Set `note_uuid` from the nested context location — `context["note"]["uuid"]`, not a top-level key — populate each question by its label, and return the edit before the originate:

```python
import uuid

from typing import Any, Sequence

from ai_scribe.parsers.base import CommandParser, ParsedContent
from canvas_sdk.commands.commands.questionnaire import QuestionnaireCommand
from canvas_sdk.v1.data.questionnaire import Questionnaire


class WoundAssessmentParser(CommandParser):
    """Parses the wound assessment section of a transcript."""

    def parse(
        self, content: ParsedContent, context: dict[str, Any] | None = None
    ) -> Sequence[QuestionnaireCommand]:
        """Parse the section and create a QuestionnaireCommand with populated responses."""

        wound_data = self.parse_wound_data(content.get("arguments", []))

        wound_questionnaire = Questionnaire.objects.get(name="Wound Assessment")
        questionnaire_command = QuestionnaireCommand(
            note_uuid=str(context.get("note", {}).get("uuid")),
            command_uuid=str(uuid.uuid4()),
            questionnaire_id=str(wound_questionnaire.id),
        )

        for question in questionnaire_command.questions:
            question.add_response(
                text=str(wound_data.get(question.label.lower().replace(" ", "_"), ""))
            )

        # The handler that invokes the parser reverses the order of effects,
        # so we return the edit before the originate here.
        return [questionnaire_command.edit(), questionnaire_command.originate(line_number=1)]

    def parse_wound_data(self, lines: list) -> dict:
        wound_data = {}
        for line in lines:
            label, value = line.split(": ")
            label = label.strip("- ").lower().replace(" ", "_")
            wound_data[label] = value
        return wound_data
```

A couple of details that are easy to get wrong:

- **`note_uuid` lives in a nested object.** The context is shaped `{"note": {"uuid": "..."}}`, so read it as `context.get("note", {}).get("uuid")`.
- **Responses are matched by question label.** This parser normalizes each label (lowercase, spaces to underscores) to look up the parsed value, so the keys you produce in `parse_wound_data` must match the questionnaire's labels after the same normalization.

## Teaching the handler to pass effects through

The base AI Scribe handler assumes every item the parser returns is a command object, assigns it a `note_uuid`, and calls `.originate()`. That breaks for a parser that returns effects (which are not command objects and already carry their `note_uuid`). Update the handler to detect effects and append them directly:

```python
from ai_scribe.parsers import ScribeParser

from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log


class Protocol(BaseProtocol):
    """A plugin for interpreting clipboard transcripts."""

    RESPONDS_TO = EventType.Name(EventType.CLIPBOARD_COMMAND__POST_INSERTED_INTO_NOTE)

    def compute(self) -> list[Effect]:
        transcript = self.context["fields"]["text"]
        log.debug(f"Processing received transcript: {transcript}")
        parser = ScribeParser()

        parsed_transcript = parser.parse(transcript, self.context)
        note_uuid = self.context["note"]["uuid"]

        effects = []
        for commands in parsed_transcript.values():
            for command in commands:
                if isinstance(command, Effect):
                    # The parser already set the note_uuid on this effect.
                    effects.append(command)
                else:
                    command.note_uuid = note_uuid
                    effects.append(command.originate(line_number=1))

        effects.reverse()
        return effects
```

The `isinstance(command, Effect)` check is what makes pre-filling work: effects produced by a parser (the `edit()`/`originate()` pair above) are appended as-is, while plain command objects are still originated as in the base example. The final `effects.reverse()` is why the parser returns `edit()` before `originate()` — after reversal, the command is originated first and then edited with the parsed responses.
