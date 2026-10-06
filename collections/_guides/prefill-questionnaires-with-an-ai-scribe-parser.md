---
title: "Pre-filling Questionnaires with an AI Scribe Parser"
guide_for:
- /sdk/events/
- /sdk/effects/
- /sdk/effect-questionnaires/
---

<!-- sources: discussion #992 -->

This guide extends [Creating, Implementing, and Extending an AI Scribe Parser](/guides/scribe-ai-parser/). To pre-fill a [Questionnaire](/sdk/commands/#questionnaire) command with parsed values, so the answers appear in the note, a section parser records the responses on the command it returns.

## How the responses reach the note

Responses you record on a questionnaire command, with `question.add_response(...)` or the `answers` parameter, travel with its `originate()` effect. The base AI Scribe handler already originates every command a parser returns, so a parser that fills in the responses needs no change to the handler.

## The custom section parser

Look the questionnaire up, populate each question by its label, and return the command:

```python?partial=true
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
            questionnaire_id=str(wound_questionnaire.id),
        )

        for question in questionnaire_command.questions:
            question.add_response(
                text=str(wound_data.get(question.label.lower().replace(" ", "_"), ""))
            )

        # The handler sets note_uuid and originates the command, responses included.
        return [questionnaire_command]

    def parse_wound_data(self, lines: list) -> dict:
        wound_data = {}
        for line in lines:
            label, value = line.split(": ")
            label = label.strip("- ").lower().replace(" ", "_")
            wound_data[label] = value
        return wound_data
```

Responses are matched by question label. This parser normalizes each label (lowercase, spaces to underscores) to look up the parsed value, so the keys you produce in `parse_wound_data` must match the questionnaire's labels after the same normalization.
