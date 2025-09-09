---
title: 'ai_note_titles'
slug: 'example-ai_note_titles'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/ai_note_titles' target='_blank'>View the source</a> for this plugin on GitHub." %}

AI Note Titles
==============

## Description

Plugin that renames Notes when locked using OpenAI and the contents of the Note.

## Configuration

This example plugin defines the following "secrets" in the manifest file:

```
    "secrets": [
        "OPENAI_API_KEY"
    ],
```
Once defined in the `MANIFEST.json`, set the secrets for your plugin in the Admin UI of your Canvas EMR. [Read more](https://docs.canvasmedical.com/sdk/secrets/)

### OPENAI_API_KEY
[OpenAI API Key](https://platform.openai.com/docs/api-reference/authentication)

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "ai_note_titles",
    "description": "Edit the description in CANVAS_MANIFEST.json",
    "components": {
        "protocols": [
            {
                "class": "ai_note_titles.handlers.rename_note:Handler",
                "description": "Renames Notes when locked using OpenAI and the contents of the Note"
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": ["OPENAI_API_KEY"],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## handlers/

### rename_note.py

**Purpose**

This code defines a handler in a Canvas SDK plugin that automatically renames clinical notes when they are locked, using the OpenAI API to generate new titles based on the note content.

**Class Overview**

- The main class, `Handler`, extends `BaseHandler`.
- The handler listens for `NOTE_STATE_CHANGE_EVENT_CREATED` events—specifically, when a note's state changes (e.g., gets locked).

**Main Workflow**

- When a relevant event fires, the `compute` method is triggered.
- It extracts the note ID from the context.
- If the note event corresponds to a locking action, it proceeds.
- It collects the note content and sends it (along with instructions) to OpenAI's API, requesting a concise, descriptive title.
- If a valid title is returned, it generates an `update` effect to rename the note in Canvas.

**OpenAI Integration**

- The `get_note_title` function prepares headers and a request payload from the note’s structured content and specific instructions.
- It POSTS this data to OpenAI's API (note: the endpoint used, `/v1/responses`, is likely a placeholder).
- It parses the response to extract the generated title.

**Supporting Functions**

- `get_model`: Returns the OpenAI model name (`gpt-4.1`).
- `get_input`: Serializes note commands (actions or entries inside the note) to JSON for use as the prompt to the language model.
- `get_instructions`: Supplies explicit instructions and examples to OpenAI, guiding it to create short, clinically meaningful titles.
- `is_locked_note_event`: Checks if the event is specifically a note being locked (not other state transitions).

**Error Handling**

- Logs issues if the note ID is missing, the OpenAI call fails, or expected fields are missing in the response.

**Effect on Canvas**

- If a new title is obtained, issues a `NoteEffect.update()` call to rename the note instance.

**Summary**

This file defines a Canvas plugin handler that listens for notes being locked, then uses OpenAI to generate and set a concise, relevant note title based on its clinical contents.

```python
import json

from canvas_sdk.effects import Effect
from canvas_sdk.effects.note import Note as NoteEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.utils.http import Http
from canvas_sdk.v1.data.command import Command
from canvas_sdk.v1.data.note import CurrentNoteStateEvent, NoteStates
from logger import log


class Handler(BaseHandler):
    """Renames Notes when locked using OpenAI and the contents of the Note."""

    RESPONDS_TO: list[str] = [
        EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED),
    ]

    def compute(self) -> list[Effect]:
        """This method gets called when an event of the type RESPONDS_TO is fired."""
        note_id: str | None = self.context.get("note_id")

        if not note_id:
            log.error("No note ID found in context")
            return []

        if not self.is_locked_note_event():
            return []

        new_title = self.get_note_title(note_id)

        if not new_title:
            return []

        return [NoteEffect(instance_id=note_id, title=new_title).update()]

    def get_note_title(self, note_id: str) -> str | None:
        """Get the new note title from the note."""
        headers = {
            "Authorization": f"Bearer {self.secrets.get('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        }
        payload = {
            "input": self.get_input(note_id),
            "instructions": self.get_instructions(),
            "model": self.get_model(),
            "temperature": 0,
        }
        response = Http().post(
            "https://api.openai.com/v1/responses", headers=headers, data=json.dumps(payload)
        )

        if not response.ok:
            log.error(
                f"Generate note title request failed: {response.status_code} - {response.text}"
            )
            return None

        response_json = response.json()

        new_title: str | None = None
        try:
            new_title = response_json.get("output")[0].get("content")[0].get("text")
        except Exception as e:
            log.error(f"Failed to get note title from response: {response.text} {e}")

        return new_title

    def get_model(self) -> str:
        """Get the OpenAI model to use."""
        return "gpt-4.1"

    def get_input(self, note_id: str) -> str:
        """Stringified commands within note to be used as input for OpenAI."""
        commands = Command.objects.filter(
            note__id=note_id, entered_in_error__isnull=True, committer__isnull=False
        )

        return json.dumps(list(commands.values("schema_key", "data")))

    def get_instructions(self) -> str:
        """Instructions for OpenAI to use to rename the note."""
        return """
        You are a clinical documentation specialist that generates a clinical note title using 10 words or less.
        This will read by a clinician looking to get a quick overview of the note.
        Return the exact title ONLY and nothing else.

        Examples:
        Ankle edema and amlodipine intolerance, medication change discussion
        Refilled metoprolol succinate ER and rosuvastatin 10 mg tablets
        Follow up call regarding elevated heart rate to 120
        Fall with back pain, unsteady gait, declined ER and HHA
        """

    def is_locked_note_event(self) -> bool:
        """Check if the note is locked."""
        return (
            CurrentNoteStateEvent.objects.values_list("state", flat=True).get(
                id=self.event.target.id
            )
            == NoteStates.LOCKED
        )
```

### __init__.py

This file is empty.
<br/>
<br/>
<br/>
