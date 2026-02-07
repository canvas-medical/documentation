---
title: LLMs
slug: clients-llms
hidden: false
---

The Canvas SDK LLMs client provides a unified interface for interacting with multiple Large Language Model (LLM) providers including OpenAI (GPT Models), Anthropic (Claude), and Google (Gemini). It supports text conversations, file attachments (images, PDFs, text), and structured JSON output.

## Requirements

Depending on which LLM provider you use:

- **OpenAI**: API key from https://platform.openai.com/api-keys
- **Anthropic**: API key from https://console.anthropic.com/settings/keys
- **Google**: API key from https://aistudio.google.com/apikey

---

## Imports

The LLMs client is included in the Canvas SDK. Import the necessary components:

```python
from canvas_sdk.clients.llms import (
    LlmOpenai,
    LlmAnthropic,
    LlmGoogle,
    LlmResponse,
    LlmTokens,
    LlmTurn,
)
from canvas_sdk.clients.llms.structures.settings import (
    LlmSettingsGpt4,
    LlmSettingsAnthropic,
    LlmSettingsGemini,
)
from canvas_sdk.clients.llms.constants import FileType
from canvas_sdk.clients.llms.structures import LlmFileUrl, FileContent, BaseModelLlmJson
```

## Initialize the Clients

### OpenAI (GPT Models)

```python
from canvas_sdk.clients.llms import LlmOpenai
from canvas_sdk.clients.llms.structures.settings import LlmSettingsGpt4

client = LlmOpenai(LlmSettingsGpt4(
    api_key="your_openai_api_key",
    model="gpt-4o",
    temperature=0.7,
))
```

### Anthropic (Claude)

```python
from canvas_sdk.clients.llms import LlmAnthropic
from canvas_sdk.clients.llms.structures.settings import LlmSettingsAnthropic

client = LlmAnthropic(LlmSettingsAnthropic(
    api_key="your_anthropic_api_key",
    model="claude-sonnet-4-5-20250929",
    temperature=0.7,
    max_tokens=8192,
))
```

### Google (Gemini)

```python
from canvas_sdk.clients.llms import LlmGoogle
from canvas_sdk.clients.llms.structures.settings import LlmSettingsGemini

client = LlmGoogle(LlmSettingsGemini(
    api_key="your_google_api_key",
    model="models/gemini-2.0-flash",
    temperature=0.7,
))
```

## Simple Text Conversation

```python
from http import HTTPStatus
from canvas_sdk.clients.llms import LlmOpenai
from canvas_sdk.clients.llms.structures.settings import LlmSettingsGpt4

# Initialize client
client = LlmOpenai(LlmSettingsGpt4(
    api_key="your_api_key",
    model="gpt-4o",
    temperature=0.7,
))

# Set up the conversation
client.set_system_prompt(["You are a helpful assistant."])
client.set_user_prompt(["What is the capital of France?"])

# Make the request
response = client.request()

if response.code == HTTPStatus.OK:
    print(f"Response: {response.response}")
    print(f"Tokens used - Prompt: {response.tokens.prompt}, Generated: {response.tokens.generated}")
else:
    print(f"Error: {response.response}")
```

## Multi-turn Conversation

```python
# Initialize client
client = LlmOpenai(LlmSettingsGpt4(
    api_key="your_api_key",
    model="gpt-4o",
    temperature=0.7,
))

# Build a multi-turn conversation
client.set_system_prompt(["You are a helpful math tutor."])
client.set_user_prompt(["What is 2 + 2?"])
client.set_model_prompt(["2 + 2 equals 4."])
client.set_user_prompt(["And what is that multiplied by 3?"])

# Get the response
response = client.request()
print(response.response)  # "4 multiplied by 3 equals 12."
```

## Using Retry Logic

```python
# Attempt multiple requests until success or max attempts
responses = client.attempt_requests(attempts=3)

# Check the last response
last_response = responses[-1]
if last_response.code == HTTPStatus.OK:
    print(f"Success: {last_response.response}")
else:
    print(f"Failed after {len(responses)} attempts")
```

## Analyze an Image

```python
from canvas_sdk.clients.llms import LlmOpenai
from canvas_sdk.clients.llms.structures.settings import LlmSettingsGpt4
from canvas_sdk.clients.llms.constants import FileType
from canvas_sdk.clients.llms.structures import LlmFileUrl

client = LlmOpenai(LlmSettingsGpt4(
    api_key="your_api_key",
    model="gpt-4o",
    temperature=0.5,
))

# Set up prompts
client.set_system_prompt(["You are an image analysis assistant."])
client.set_user_prompt(["Describe what you see in this image."])

# Add an image file
client.add_url_file(LlmFileUrl(
    url="https://example.com/image.jpg",
    type=FileType.IMAGE
))

# Get the analysis
response = client.request()
print(response.response)
```

## Analyze a PDF Document

```python
from canvas_sdk.clients.llms import LlmAnthropic
from canvas_sdk.clients.llms.structures.settings import LlmSettingsAnthropic
from canvas_sdk.clients.llms.constants import FileType
from canvas_sdk.clients.llms.structures import LlmFileUrl

client = LlmAnthropic(LlmSettingsAnthropic(
    api_key="your_api_key",
    model="claude-sonnet-4-5-20250929",
    temperature=0.5,
    max_tokens=4096,
))

# Set up prompts
client.set_system_prompt(["You are a document analysis assistant."])
client.set_user_prompt(["Summarize the key points in this document."])

# Add a PDF file
client.add_url_file(LlmFileUrl(
    url="https://example.com/document.pdf",
    type=FileType.PDF
))

# Get the summary
response = client.request()
print(response.response)
```

## Upload File Content Directly

Instead of providing a URL, you can upload file content directly using `FileContent`. This is useful when you have the file data in memory (e.g., from a form upload).

```python
import base64
from canvas_sdk.clients.llms import LlmOpenai
from canvas_sdk.clients.llms.structures.settings import LlmSettingsGpt4
from canvas_sdk.clients.llms.structures import FileContent

client = LlmOpenai(LlmSettingsGpt4(
    api_key="your_api_key",
    model="gpt-4o",
    temperature=0.5,
))

# Read file content from disk or form upload
with open("document.pdf", "rb") as f:
    file_bytes = f.read()

# Create FileContent with base64-encoded data
file_content = FileContent(
    mime_type="application/pdf",
    content=base64.b64encode(file_bytes),
    size=len(file_bytes),
)

# Add to the client's file_content list
client.file_content.append(file_content)

# Set up prompts
client.set_system_prompt(["Analyze the provided document."])
client.set_user_prompt(["What are the main topics covered in this document?"])

# Get the analysis
response = client.request()
print(response.response)
```

**Supported MIME types for direct file content:**

| MIME Type Pattern     | Description                    |
|-----------------------|--------------------------------|
| `image/*`             | Images (PNG, JPEG, GIF, etc.)  |
| `application/pdf`     | PDF documents                  |
| `text/*`              | Text files (Anthropic only)    |

## Structured JSON Output

```python
from pydantic import Field
from canvas_sdk.clients.llms import LlmOpenai
from canvas_sdk.clients.llms.structures.settings import LlmSettingsGpt4
from canvas_sdk.clients.llms.structures import BaseModelLlmJson

# Define your response schema
class PersonInfo(BaseModelLlmJson):
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years")
    occupation: str = Field(description="The person's job or profession")

# Initialize client
client = LlmOpenai(LlmSettingsGpt4(
    api_key="your_api_key",
    model="gpt-4o",
    temperature=0.3,
))

# Set the schema for structured output
client.set_schema(PersonInfo)

# Set up prompts
client.set_system_prompt(["Extract person information from the text."])
client.set_user_prompt(["John Smith is a 35-year-old software engineer."])

# Get structured response
response = client.request()
# Response will be valid JSON matching the PersonInfo schema
print(response.response)  # {"name": "John Smith", "age": 35, "occupation": "software engineer"}
```

## Nested Structured Output

```python
from pydantic import Field
from canvas_sdk.clients.llms.structures import BaseModelLlmJson

# Define nested schemas (all must extend BaseModelLlmJson)
class Address(BaseModelLlmJson):
    street: str = Field(description="Street address")
    city: str = Field(description="City name")
    country: str = Field(description="Country name")

class Person(BaseModelLlmJson):
    name: str = Field(description="Full name")
    address: Address = Field(description="Home address")

# Use with client
client.set_schema(Person)
client.set_system_prompt(["Extract person and address information."])
client.set_user_prompt(["Jane Doe lives at 123 Main St, New York, USA."])

response = client.request()
```

---

## LLM Clients

All LLM clients inherit from `LlmApi` and share the same interface.

### Available Clients

| Client        | Provider  | Settings Class        | API Endpoint                              |
|---------------|-----------|----------------------|-------------------------------------------|
| `LlmOpenai`   | OpenAI    | `LlmSettingsGpt4`    | `https://us.api.openai.com`               |
| `LlmAnthropic`| Anthropic | `LlmSettingsAnthropic`| `https://api.anthropic.com`              |
| `LlmGoogle`   | Google    | `LlmSettingsGemini`  | `https://generativelanguage.googleapis.com`|

### Constructor

```python
LlmOpenai(settings: LlmSettingsGpt4)
LlmAnthropic(settings: LlmSettingsAnthropic)
LlmGoogle(settings: LlmSettingsGemini)
```

### Attributes

| Attribute      | Type                       | Description                                        |
|----------------|----------------------------|----------------------------------------------------|
| `settings`     | `LlmSettings`              | Configuration settings for the LLM API             |
| `prompts`      | `list[LlmTurn]`            | List of conversation turns                         |
| `file_urls`    | `list[LlmFileUrl]`         | Files to attach via URL (use `add_url_file()`)     |
| `file_content` | `list[FileContent]`        | Files to attach via direct content                 |
| `schema`       | `type[BaseModelLlmJson]`   | Schema for structured JSON output                  |

### Methods

#### `set_system_prompt(text: list[str]) -> None`

Set or replace the system prompt. The system prompt is always placed at the beginning of the conversation.

**Parameters:**

| Parameter | Type        | Description                        |
|-----------|-------------|------------------------------------|
| `text`    | `list[str]` | List of text strings for the prompt|

#### `set_user_prompt(text: list[str]) -> None`

Add a user message to the conversation.

**Parameters:**

| Parameter | Type        | Description                        |
|-----------|-------------|------------------------------------|
| `text`    | `list[str]` | List of text strings for the prompt|

#### `set_model_prompt(text: list[str]) -> None`

Add a model/assistant response to the conversation history.

**Parameters:**

| Parameter | Type        | Description                             |
|-----------|-------------|-----------------------------------------|
| `text`    | `list[str]` | List of text strings for the response   |

#### `add_prompt(prompt: LlmTurn) -> None`

Add a conversation turn using an `LlmTurn` object.

**Parameters:**

| Parameter | Type      | Description                    |
|-----------|-----------|--------------------------------|
| `prompt`  | `LlmTurn` | The conversation turn to add   |

#### `add_url_file(url_file: LlmFileUrl) -> None`

Add a file attachment to the next user message.

**Parameters:**

| Parameter  | Type        | Description                        |
|------------|-------------|------------------------------------|
| `url_file` | `LlmFileUrl`| File URL and type information      |

#### `set_schema(schema: type[BaseModelLlmJson] | None) -> None`

Set a schema for structured JSON output. Pass `None` to disable structured output.

**Parameters:**

| Parameter | Type                           | Description                     |
|-----------|--------------------------------|---------------------------------|
| `schema`  | `type[BaseModelLlmJson] | None`| Pydantic model for JSON schema  |

#### `reset_prompts() -> None`

Clear all stored prompts from the conversation.

#### `request() -> LlmResponse`

Make a single request to the LLM API.

**Returns:** `LlmResponse` containing status code, response text, and token usage.

#### `attempt_requests(attempts: int) -> list[LlmResponse]`

Attempt multiple requests until success or max attempts reached.

**Parameters:**

| Parameter  | Type  | Description                          |
|------------|-------|--------------------------------------|
| `attempts` | `int` | Maximum number of request attempts   |

**Returns:** List of all `LlmResponse` objects from each attempt.

---

## Settings Classes

### LlmSettings (Base)

Base configuration class for LLM APIs.

| Field     | Type  | Description                    |
|-----------|-------|--------------------------------|
| `api_key` | `str` | API authentication key         |
| `model`   | `str` | Model name or identifier       |

### LlmSettingsGpt4

Settings for OpenAI API.

| Field         | Type    | Description                              |
|---------------|---------|------------------------------------------|
| `api_key`     | `str`   | OpenAI API key                           |
| `model`       | `str`   | Model name (e.g., `gpt-4o`, `gpt-4-turbo`)|
| `temperature` | `float` | Randomness control (0.0-2.0)             |

**Example:**

```python
LlmSettingsGpt4(
    api_key="sk-...",
    model="gpt-4o",
    temperature=0.7,
)
```

### LlmSettingsAnthropic

Settings for Anthropic Claude API.

| Field         | Type    | Description                                      |
|---------------|---------|--------------------------------------------------|
| `api_key`     | `str`   | Anthropic API key                                |
| `model`       | `str`   | Model name (e.g., `claude-sonnet-4-5-20250929`)  |
| `temperature` | `float` | Randomness control (0.0-1.0)                     |
| `max_tokens`  | `float` | Maximum tokens to generate                       |

**Example:**

```python
LlmSettingsAnthropic(
    api_key="sk-ant-...",
    model="claude-sonnet-4-5-20250929",
    temperature=0.7,
    max_tokens=8192,
)
```

### LlmSettingsGemini

Settings for Google Gemini API.

| Field         | Type    | Description                                  |
|---------------|---------|----------------------------------------------|
| `api_key`     | `str`   | Google API key                               |
| `model`       | `str`   | Model name (e.g., `models/gemini-2.0-flash`) |
| `temperature` | `float` | Randomness control (0.0-2.0)                 |

**Example:**

```python
LlmSettingsGemini(
    api_key="AIza...",
    model="models/gemini-2.0-flash",
    temperature=0.7,
)
```

---

## Data Structures

### LlmResponse

Response from an LLM API call.

| Field      | Type         | Description                          |
|------------|--------------|--------------------------------------|
| `code`     | `HTTPStatus` | HTTP status code of the response     |
| `response` | `str`        | Text content returned by the LLM     |
| `tokens`   | `LlmTokens`  | Token usage information              |

**Methods:**

| Method      | Returns | Description                          |
|-------------|---------|--------------------------------------|
| `to_dict()` | `dict`  | Convert response to dictionary       |

### LlmTokens

Token usage information for LLM API calls.

| Field       | Type  | Description                              |
|-------------|-------|------------------------------------------|
| `prompt`    | `int` | Number of tokens in the prompt           |
| `generated` | `int` | Number of tokens in the generated response|

**Methods:**

| Method              | Returns | Description                          |
|---------------------|---------|--------------------------------------|
| `add(counts)`       | `None`  | Add token counts from another instance|
| `to_dict()`         | `dict`  | Convert to dictionary                |

### LlmTurn

A single conversation turn in an LLM interaction.

| Field  | Type        | Description                                    |
|--------|-------------|------------------------------------------------|
| `role` | `str`       | Role of the speaker (`system`, `user`, `model`)|
| `text` | `list[str]` | List of text strings for this turn             |

**Methods:**

| Method                        | Returns         | Description                       |
|-------------------------------|-----------------|-----------------------------------|
| `to_dict()`                   | `dict`          | Convert turn to dictionary        |
| `load_from_dict(dict_list)`   | `list[LlmTurn]` | Create turns from list of dicts   |

### LlmFileUrl

Container for file URL and type information.

| Field  | Type       | Description                          |
|--------|------------|--------------------------------------|
| `url`  | `str`      | URL where the file can be accessed   |
| `type` | `FileType` | Type of file (IMAGE, PDF, TEXT)      |

### FileContent

Container for file content, used for direct file uploads to LLM providers. Add instances to `client.file_content` list.

| Field       | Type    | Description                                      |
|-------------|---------|--------------------------------------------------|
| `mime_type` | `str`   | MIME type of the content (e.g., `image/png`)     |
| `content`   | `bytes` | Base64-encoded file content                      |
| `size`      | `int`   | Size of the original file in bytes               |

**Example:**

```python
import base64
from canvas_sdk.clients.llms.structures import FileContent

# From file bytes
with open("image.png", "rb") as f:
    file_bytes = f.read()

file_content = FileContent(
    mime_type="image/png",
    content=base64.b64encode(file_bytes),
    size=len(file_bytes),
)

# Add to client
client.file_contents.append(file_content)
```

### BaseModelLlmJson

Base class for structured JSON output schemas. Extends Pydantic's `BaseModel` with:
- `additionalProperties: false` in JSON schema
- Automatic camelCase field name conversion

**Usage:**

```python
from pydantic import Field
from canvas_sdk.clients.llms.structures import BaseModelLlmJson

class MySchema(BaseModelLlmJson):
    field_name: str = Field(description="Description for the LLM")
    another_field: int = Field(description="Another description")
```

---

## Constants (Enums)

### FileType

Supported file types for LLM file attachments.

| Value   | Description                      |
|---------|----------------------------------|
| `IMAGE` | Image files (PNG, JPEG, GIF)     |
| `PDF`   | PDF documents                    |
| `TEXT`  | Plain text files                 |

### Role Constants

Available on all LLM client classes:

| Constant     | Value      | Description                    |
|--------------|------------|--------------------------------|
| `ROLE_SYSTEM`| `"system"` | System/instruction role        |
| `ROLE_USER`  | `"user"`   | User message role              |
| `ROLE_MODEL` | `"model"`  | Model/assistant response role  |

---

## Complete Plugin Example

Here's a complete example of using the LLMs client in a Canvas plugin:

```python
import base64
from http import HTTPStatus

from pydantic import Field

from canvas_sdk.clients.llms import LlmOpenai
from canvas_sdk.clients.llms.constants import FileType
from canvas_sdk.clients.llms.structures import BaseModelLlmJson, FileContent, LlmFileUrl
from canvas_sdk.clients.llms.structures.settings import LlmSettingsGpt4
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, PlainTextResponse, Response
from canvas_sdk.handlers.simple_api import Credentials, SimpleAPI, api
from canvas_sdk.handlers.simple_api.api import FileFormPart, StringFormPart


class AnimalCount(BaseModelLlmJson):
    """Structured response for animal counting."""
    dogs: int = Field(description="Number of dogs in the image")
    cats: int = Field(description="Number of cats in the image")
    total: int = Field(description="Total number of animals")


class LlmHandler(SimpleAPI):
    """Simple API handler for LLM operations."""

    def authenticate(self, credentials: Credentials) -> bool:
        return True

    def _llm_client(self) -> LlmOpenai:
        """Create LLM client from plugin secrets."""
        return LlmOpenai(LlmSettingsGpt4(
            api_key=self.secrets["LlmKey"],
            model="gpt-4o",
            temperature=0.5,
        ))

    @api.post("/chat")
    def chat(self) -> list[Response | Effect]:
        """Handle a chat conversation."""
        client = self._llm_client()

        # Process conversation turns from request
        for turn in self.request.json():
            if turn.get("role") == "system":
                client.set_system_prompt([turn.get("prompt", "")])
            elif turn.get("role") == "user":
                client.set_user_prompt([turn.get("prompt", "")])
            else:
                client.set_model_prompt([turn.get("prompt", "")])

        response = client.attempt_requests(attempts=2)[0]
        return [PlainTextResponse(response.response, status_code=response.code)]

    @api.post("/analyze_image")
    def analyze_image(self) -> list[Response | Effect]:
        """Analyze an image for animal content via URL."""
        client = self._llm_client()
        url = self.request.json().get("url")

        if not url:
            return [JSONResponse({"error": "URL required"}, status_code=HTTPStatus.BAD_REQUEST)]

        # Set up structured output
        client.set_schema(AnimalCount)
        client.set_system_prompt(["Count the animals in the provided image."])
        client.set_user_prompt(["Identify and count all animals in this image."])
        client.add_url_file(LlmFileUrl(url=url, type=FileType.IMAGE))

        responses = client.attempt_requests(attempts=2)
        content = [r.to_dict() for r in responses]
        return [JSONResponse(content, status_code=HTTPStatus.OK)]

    @api.post("/file")
    def file(self) -> list[Response | Effect]:
        """Analyze uploaded file content using LLM.

        Accepts multipart form data with 'file' and 'input' fields.
        """
        content = b""
        mime_type = ""
        user_input = ""

        # Parse form data
        form_data = self.request.form_data()
        if "file" in form_data and isinstance(form_data["file"], FileFormPart):
            content = form_data["file"].content
            mime_type = form_data["file"].content_type
        if "input" in form_data and isinstance(form_data["input"], StringFormPart):
            user_input = form_data["input"].value

        if not (content and mime_type and user_input):
            return [PlainTextResponse("Missing file or input", status_code=HTTPStatus.BAD_REQUEST)]

        client = self._llm_client()

        # Create FileContent with base64-encoded data
        file = FileContent(
            mime_type=mime_type,
            content=base64.b64encode(content),
            size=len(content),
        )
        client.file_content.append(file)

        client.set_system_prompt(["Answer the question about the file clearly and concisely."])
        client.set_user_prompt([user_input])

        response = client.attempt_requests(attempts=1)[0]
        return [PlainTextResponse(response.response, status_code=response.code)]
```

---

## Error Handling

The LLM clients return `LlmResponse` objects with HTTP status codes indicating success or failure.

```python
from http import HTTPStatus

response = client.request()

if response.code == HTTPStatus.OK:
    print(f"Success: {response.response}")
elif response.code == HTTPStatus.TOO_MANY_REQUESTS:
    print("Rate limited - try again later")
elif response.code == HTTPStatus.UNAUTHORIZED:
    print("Invalid API key")
elif response.code == HTTPStatus.BAD_REQUEST:
    print(f"Bad request: {response.response}")
else:
    print(f"Error {response.code}: {response.response}")
```

When using `attempt_requests`, the method will automatically retry on failure:

```python
responses = client.attempt_requests(attempts=3)

# Check if any attempt succeeded
successful = [r for r in responses if r.code == HTTPStatus.OK]
if successful:
    print(f"Success after {len(responses)} attempt(s)")
else:
    print(f"All {len(responses)} attempts failed")
```

---

## Provider-Specific Notes

### OpenAI

- Uses the Responses API (`/v1/responses`)
- Supports images and PDFs via URL (`add_url_file`) or direct content (`file_content`)
- System prompts are sent as `instructions`
- Direct file content uses `input_image` for images and `input_file` for PDFs

### Anthropic

- Uses the Messages API (`/v1/messages`)
- Supports images, PDFs, and text files via URL or direct content
- Text files are base64-decoded and sent as plain text
- Structured output uses tool calling

### Google Gemini

- Uses the Generative Language API
- Files via URL are downloaded and converted to base64 automatically
- Supports both URL-based and direct file content
- Maximum file size limit of 10MB per request (combined)
- Structured output uses `responseJsonSchema`

---

## Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Anthropic API Documentation](https://docs.anthropic.com/en/api)
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Example Plugin](/sdk/example-llm/) - Documentation for the example plugin
- [Source Code](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/llm) - View the source on GitHub
