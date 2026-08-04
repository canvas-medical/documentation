---
title: 'LLM'
slug: 'example-llm'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/llm' target='_blank'>View the source</a> for this plugin on GitHub." %}


## Description

Plugin that provides a SimpleAPI for interacting with multiple LLM providers (Anthropic, Google, OpenAI) through the Canvas SDK's unified LLM client. It supports image analysis with structured JSON output, multi-turn chat conversations, and file content analysis. Includes a chart application that renders a form interface for LLM interactions directly from the chart.

## Configuration

This example plugin defines the following "secrets" in the manifest file:

```
    "variables": [
        {"name": "AnthropicKey", "sensitive": true},
        {"name": "GoogleKey", "sensitive": true},
        {"name": "OpenaiKey", "sensitive": true}
    ],
```
Once defined in the `MANIFEST.json`, set the secrets for your plugin in the Admin UI of your Canvas EMR. [Read more](https://docs.canvasmedical.com/sdk/secrets/)

### AnthropicKey
Your [Anthropic API key](https://console.anthropic.com/settings/keys).

### GoogleKey
Your [Google AI API key](https://aistudio.google.com/apikey).

### OpenaiKey
Your [OpenAI API key](https://platform.openai.com/api-keys).

## CANVAS_MANIFEST.json

```json
{
  "sdk_version": "0.81.0",
  "plugin_version": "0.0.1",
  "name": "llm_manip",
  "description": "use LLM to interact with the user",
  "components": {
    "handlers": [
      {
        "class": "llm_manip.handlers.llm_manip:LlmManip",
        "description": "LLM communication wrapper"
      }
    ],
    "applications": [
      {
        "class": "llm_manip.handlers.llm_form_app:LlmFormApp",
        "name": "LLM Interactions",
        "description": "LLM interactions with the user",
        "icon": "static/llm_manip.png",
        "scope": "patient_specific",
        "show_in_panel": false
      }
    ],
    "commands": [],
    "content": [],
    "effects": [],
    "views": []
  },
  "variables": [
    {"name": "AnthropicKey", "sensitive": true},
    {"name": "GoogleKey", "sensitive": true},
    {"name": "OpenaiKey", "sensitive": true}
  ],
  "tags": {},
  "references": [],
  "license": "",
  "diagram": false,
  "readme": "./README.md"
}
```

## handlers/

### llm_manip.py

**Purpose**

This code defines a SimpleAPI handler that exposes REST endpoints for interacting with LLM providers using the Canvas SDK's unified LLM client.

**Class Overview**

- The main class, `LlmManip`, extends `SimpleAPI`.
- It supports three LLM providers: Anthropic (Claude), Google (Gemini), and OpenAI (GPT Models).
- It demonstrates structured JSON output using Pydantic models (`LlmResponse`, `Result`).

**Main Workflow**

- `POST /animals_count/<llm_provider>` — Analyzes an image URL to count animals using LLM vision capabilities with structured JSON output.
- `POST /chat/<llm_provider>` — Processes a multi-turn chat conversation with system, user, and model roles.
- `POST /file/<llm_provider>` — Analyzes uploaded file content using multipart form data.

**LLM Client Integration**

- The `_llm_client` method creates provider-specific clients (`LlmAnthropic`, `LlmGoogle`, `LlmOpenai`) with their respective settings classes.
- Structured output is configured via `client.set_schema()` with Pydantic models extending `BaseModelLlmJson`.
- File attachments are supported via `LlmFileUrl` for URLs and `FileContent` for binary content.

```python
import base64
from http import HTTPStatus

from pydantic import Field

from canvas_sdk.clients.llms.constants import FileType
from canvas_sdk.clients.llms.libraries import LlmAnthropic, LlmApi, LlmGoogle, LlmOpenai
from canvas_sdk.clients.llms.structures import BaseModelLlmJson, FileContent, LlmFileUrl
from canvas_sdk.clients.llms.structures.settings import (
    LlmSettingsAnthropic,
    LlmSettingsGemini,
    LlmSettingsGpt4,
)
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, PlainTextResponse, Response
from canvas_sdk.handlers.simple_api import Credentials, SimpleAPI, api
from canvas_sdk.handlers.simple_api.api import FileFormPart, StringFormPart
from llm_manip.constants.secrets import Secrets


class Result(BaseModelLlmJson):
    """Structured response model for animal counting results."""

    count_dogs: int = Field(description="the number of dogs")
    count_cats: int = Field(description="the number of cats")
    count_total: int = Field(description="the number of animals")


class LlmResponse(BaseModelLlmJson):
    """Structured response model for LLM animal analysis with optional result."""

    comment: str = Field(description="the comment")
    result: Result | None


class LlmManip(SimpleAPI):
    """Simple API handler for LLM-based image analysis and chat operations."""

    PREFIX = None
    LLM_ANTHROPIC = 0
    LLM_GOOGLE = 1
    LLM_OPENAI = 2

    def authenticate(self, credentials: Credentials) -> bool:
        """Authenticate API requests."""
        return True

    def _llm_client(self, provider: int) -> LlmApi:
        """Create and configure a LLM client with credentials from secrets."""
        if provider == self.LLM_ANTHROPIC:
            return LlmAnthropic(
                LlmSettingsAnthropic(
                    api_key=self.secrets[Secrets.anthropic_key],
                    model="claude-sonnet-4-5",
                    temperature=1.0,
                    max_tokens=8192,
                )
            )
        elif provider == self.LLM_GOOGLE:
            return (
                LlmGoogle(
                    LlmSettingsGemini(
                        api_key=self.secrets[Secrets.anthropic_key],
                        model="models/gemini-2.5-flash",
                        temperature=1.0,
                    )
                ),
            )
        else:
            return LlmOpenai(
                LlmSettingsGpt4(
                    api_key=self.secrets[Secrets.openai_key],
                    model="gpt-4o",
                    temperature=2.0,
                )
            )

    @api.post("/animals_count/<llm_provider>")
    def animals_count(self) -> list[Response | Effect]:
        """Analyze an image URL to count animals using LLM vision capabilities."""
        client = self._llm_client(self.request.path_params["llm_provider"])
        url = self.request.json().get("url")
        if not url:
            url = "https://images.unsplash.com/photo-1563460716037-460a3ad24ba9?w=125"

        client.set_schema(LlmResponse)
        client.set_system_prompt(
            ["Your task is to read the pictures provided by the user and count the animals in it."]
        )
        client.set_user_prompt(["Identify the content of the provided picture."])
        client.add_url_file(LlmFileUrl(url=url, type=FileType.IMAGE))
        responses = client.attempt_requests(attempts=2)
        content = [r.to_dict() for r in responses]
        return [JSONResponse(content, status_code=HTTPStatus(HTTPStatus.OK))]

    @api.post("/chat/<llm_provider>")
    def chat(self) -> list[Response | Effect]:
        """Process a multi-turn chat conversation with the LLM."""
        client = self._llm_client(self.request.path_params["llm_provider"])
        for turn in self.request.json():
            if not isinstance(turn, dict):
                continue
            if turn.get("role") == "system":
                client.set_system_prompt([turn.get("prompt", "")])
            elif turn.get("role") == "user":
                client.set_user_prompt([turn.get("prompt", "")])
            else:
                client.set_model_prompt([turn.get("prompt", "")])

        response = client.attempt_requests(attempts=1)[0]
        return [PlainTextResponse(response.response, status_code=response.code)]

    @api.post("/file/<llm_provider>")
    def file(self) -> list[Response | Effect]:
        """Analyze file content using LLM."""
        content = b""
        mime_type = ""
        user_input = ""
        form_data = self.request.form_data()
        if "file" in form_data and isinstance(form_data["file"], FileFormPart):
            content = form_data["file"].content
            mime_type = form_data["file"].content_type
        if "input" in form_data and isinstance(form_data["input"], StringFormPart):
            user_input = form_data["input"].value

        if not (content and mime_type and user_input):
            return [PlainTextResponse("nothing to do", status_code=HTTPStatus(HTTPStatus.OK))]

        client = self._llm_client(self.request.path_params["llm_provider"])
        file = FileContent(
            mime_type=mime_type,
            content=base64.b64encode(content),
            size=len(content),
        )
        client.file_contents.append(file)
        client.set_system_prompt(["Answer to the question about the file, clearly and concisely."])
        client.set_user_prompt([user_input or "what is in the file?"])

        response = client.attempt_requests(attempts=1)[0]
        return [PlainTextResponse(response.response, status_code=response.code)]
```

### llm_form_app.py

**Purpose**

This code defines an Application handler that launches a modal form in the right chart pane for interacting with the LLM API endpoints.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application
from canvas_sdk.templates import render_to_string


class LlmFormApp(Application):
    """Application handler for launching the LLM interaction form interface."""

    PLUGIN_API_BASE_ROUTE = "/plugin-io/api/llm_manip"

    def on_open(self) -> Effect:
        """Render and launch the LLM interaction modal form."""
        content = render_to_string(
            "templates/llm_form.html",
            {
                "animalsCountURL": f"{self.PLUGIN_API_BASE_ROUTE}/animals_count",
                "chatURL": f"{self.PLUGIN_API_BASE_ROUTE}/chat",
                "fileURL": f"{self.PLUGIN_API_BASE_ROUTE}/file",
            },
        )

        return LaunchModalEffect(
            content=content,
            target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
        ).apply()
```

<br/>
<br/>
<br/>
