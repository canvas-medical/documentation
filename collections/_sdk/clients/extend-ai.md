---
title: "Extend AI"
slug: "clients-extend-ai"
hidden: false
---

The Canvas SDK Extend AI client provides an interface for document processing using AI-powered extraction, classification, and splitting capabilities through the Extend AI API.

## Requirements

- **Extend AI API Key**: Obtain from your [Extend AI dashboard](https://app.extend.ai/)

## What is Extend AI?

Extend AI provides intelligent document processing (IDP) capabilities:

- **Extraction**: Extract structured data from documents based on a defined schema
- **Classification**: Classify documents into predefined categories
- **Splitting**: Split multi-page documents into logical sections

## Imports

The Extend AI client is included in the Canvas SDK. Import the necessary components:

```python
from canvas_sdk.clients.extend_ai.libraries import Client
from canvas_sdk.clients.extend_ai.constants import RunStatus, VersionName
from canvas_sdk.clients.extend_ai.structures import RequestFailed
```

## Initialize the Client

```python
client = Client(key="your_extend_ai_api_key")
```

## Extract Data from a Document (Using an Existing Processor)

The most common use case is running an existing processor on a document. Here's a complete example:

```python
import time
from canvas_sdk.clients.extend_ai.libraries import Client
from canvas_sdk.clients.extend_ai.constants import RunStatus
from canvas_sdk.clients.extend_ai.structures import RequestFailed

# Initialize the client
client = Client(key="your_api_key")

# Your processor ID (created in the Extend AI dashboard)
processor_id = "proc_xxxxxxxxxxxxxxxxx"

# URL to the document (must be publicly accessible)
document_url = "https://your-bucket.s3.amazonaws.com/document.pdf"

try:
    # Start the processor run
    run = client.run_processor(
        processor_id=processor_id,
        file_name="my-document.pdf",
        file_url=document_url,
        config=None,  # Use processor's default configuration
    )
    print(f"Run started! ID: {run.id}, Status: {run.status.value}")

    # Poll for completion
    while run.status in (RunStatus.PENDING, RunStatus.PROCESSING):
        time.sleep(2)  # Wait 2 seconds between checks
        run = client.run_status(run.id)
        print(f"Status: {run.status.value}")

    # Check result
    if run.status == RunStatus.PROCESSED:
        print("Extraction successful!")
        print(f"Extracted data: {run.output.value}")
    else:
        print(f"Processing failed with status: {run.status.value}")

except RequestFailed as e:
    print(f"Error: {e.message} (HTTP {e.status_code})")
```

## List Available Processors

```python
# List all processors in your account
for processor in client.list_processors():
    print(f"ID: {processor.id}")
    print(f"Name: {processor.name}")
    print(f"Type: {processor.type.value}")
    print("---")
```

## Get Processor Configuration

```python
from canvas_sdk.clients.extend_ai.constants import VersionName

# Get the draft version of a processor
processor_version = client.processor(
    processor_id="proc_xxxxxxxxxxxxxxxxx",
    version=VersionName.DRAFT.value
)

print(f"Processor: {processor_version.processor.name}")
print(f"Version: {processor_version.version}")
print(f"Type: {processor_version.processor.type.value}")

# Access the schema (for extraction processors)
if hasattr(processor_version.config, 'schema'):
    print(f"Schema: {processor_version.config.schema}")
```

## Check Run Status and Get Results

```python
# Check the status of a run
run = client.run_status("run_xxxxxxxxxxxxxxxxx")

print(f"Status: {run.status.value}")
print(f"Credits used: {run.usage}")

if run.status == RunStatus.PROCESSED:
    # For extraction processors
    if hasattr(run.output, 'value'):
        extracted_data = run.output.value
        print(f"Extracted: {extracted_data}")

    # For classification processors
    if hasattr(run.output, 'type'):
        print(f"Classification: {run.output.type}")
        print(f"Confidence: {run.output.confidence}")

    # For splitter processors
    if hasattr(run.output, 'splits'):
        for split in run.output.splits:
            print(f"Split: {split.type}, Pages {split.startPage}-{split.endPage}")
```

## Clean Up Files After Processing

```python
# After processing, delete the uploaded files to save storage
run = client.run_status("run_xxxxxxxxxxxxxxxxx")

if run.status == RunStatus.PROCESSED:
    for file in run.files:
        deleted = client.delete_file(file.id)
        print(f"Deleted file {file.name}: {deleted}")
```

## Complete Workflow Example

```python
import time
from canvas_sdk.clients.extend_ai.libraries import Client
from canvas_sdk.clients.extend_ai.constants import RunStatus
from canvas_sdk.clients.extend_ai.structures import RequestFailed

def extract_from_document(api_key: str, processor_id: str, document_url: str) -> dict:
    """
    Extract structured data from a document using Extend AI.

    Args:
        api_key: Your Extend AI API key
        processor_id: The processor ID to use
        document_url: Public URL to the document

    Returns:
        Dictionary containing the extracted data

    Raises:
        RequestFailed: If the API request fails
        RuntimeError: If processing fails or times out
    """
    client = Client(key=api_key)

    # Start processing
    run = client.run_processor(
        processor_id=processor_id,
        file_name="document.pdf",
        file_url=document_url,
        config=None,
    )

    # Wait for completion (with timeout)
    max_attempts = 30  # 60 seconds max
    attempts = 0

    while run.status in (RunStatus.PENDING, RunStatus.PROCESSING):
        if attempts >= max_attempts:
            raise RuntimeError("Processing timed out")
        time.sleep(2)
        run = client.run_status(run.id)
        attempts += 1

    # Handle result
    if run.status == RunStatus.PROCESSED:
        # Clean up files
        for file in run.files:
            client.delete_file(file.id)

        return run.output.value if hasattr(run.output, 'value') else run.output.to_dict()

    raise RuntimeError(f"Processing failed: {run.status.value}")


# Usage
result = extract_from_document(
    api_key="your_api_key",
    processor_id="proc_xxxxxxxxxxxxxxxxx",
    document_url="https://example.com/document.pdf"
)
print(result)
```

## Client

The main class for interacting with the Extend AI API.

### Constructor

```python
Client(key: str)
```

| Parameter | Type  | Description              |
|-----------|-------|--------------------------|
| `key`     | `str` | Extend AI API key        |

### File Management

#### `list_files() -> Iterator[StoredFile]`

List all files stored in Extend AI.

```python
for file in client.list_files():
    print(f"{file.id}: {file.name} ({file.type})")
```

**Returns:** Iterator of `StoredFile` objects

**Raises:** `RequestFailed` on error

#### `delete_file(file_id: str) -> bool`

Delete a file from Extend AI storage.

```python
deleted = client.delete_file("file_xxxxxxxxxxxxxxxxx")
print(f"Deleted: {deleted}")
```

| Parameter | Type  | Description                   |
|-----------|-------|-------------------------------|
| `file_id` | `str` | Unique identifier of the file |

**Returns:** `True` on success

**Raises:** `RequestFailed` on error

### Processor Management

#### `list_processors() -> Iterator[ProcessorMeta]`

List all processors in the account.

```python
for processor in client.list_processors():
    print(f"{processor.name}: {processor.type.value}")
```

**Returns:** Iterator of `ProcessorMeta` objects

**Raises:** `RequestFailed` on error

#### `processor(processor_id: str, version: str) -> ProcessorVersion`

Get details for a specific processor version.

```python
from canvas_sdk.clients.extend_ai.constants import VersionName

# Get draft version
processor = client.processor("proc_xxx", VersionName.DRAFT.value)

# Get latest published version
processor = client.processor("proc_xxx", VersionName.LATEST.value)

# Get specific version
processor = client.processor("proc_xxx", "v1")
```

| Parameter      | Type  | Description                              |
|----------------|-------|------------------------------------------|
| `processor_id` | `str` | Unique identifier of the processor       |
| `version`      | `str` | Version name (`draft`, `latest`, or `vN`)|

**Returns:** `ProcessorVersion` object

**Raises:** `RequestFailed` on error

#### `create_processor(name: str, config: ConfigBase) -> ProcessorMeta`

Create a new processor with the specified configuration.

```python
from canvas_sdk.clients.extend_ai.constants import BaseProcessor
from canvas_sdk.clients.extend_ai.structures.config import (
    ConfigExtraction,
    AdvancedOptionsExtraction,
    Parser,
)

config = ConfigExtraction(
    base_processor=BaseProcessor.EXTRACTION_PERFORMANCE,
    extraction_rule="Extract all relevant fields",
    schema={
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "date": {"type": "string"},
            "amount": {"type": "number"},
        }
    },
    advanced_options=AdvancedOptionsExtraction.from_dict({}),
    parser=Parser.from_dict({}),
)

processor = client.create_processor("Invoice Extractor", config)
print(f"Created: {processor.id}")
```

| Parameter | Type         | Description                    |
|-----------|--------------|--------------------------------|
| `name`    | `str`        | Name for the new processor     |
| `config`  | `ConfigBase` | Processor configuration object |

**Returns:** `ProcessorMeta` object

**Raises:** `RequestFailed` on error

### Running Processors

#### `run_processor(processor_id, file_name, file_url, config) -> ProcessorRun`

Execute a processor on a document.

```python
run = client.run_processor(
    processor_id="proc_xxxxxxxxxxxxxxxxx",
    file_name="invoice.pdf",
    file_url="https://bucket.s3.amazonaws.com/invoice.pdf",
    config=None,  # Use processor defaults
)
print(f"Run ID: {run.id}, Status: {run.status.value}")
```

| Parameter      | Type                       | Description                                   |
|----------------|----------------------------|-----------------------------------------------|
| `processor_id` | `str`                      | Processor to run                              |
| `file_name`    | `str`                      | Name for the file                             |
| `file_url`     | `str`                      | Public URL to the document                    |
| `config`       | `ConfigExtraction \| None` | Optional config override (extraction only)    |

**Returns:** `ProcessorRun` object with initial status

**Raises:** `RequestFailed` on error

#### `run_status(run_id: str) -> ProcessorRun`

Get the current status and results of a processor run.

```python
run = client.run_status("run_xxxxxxxxxxxxxxxxx")

if run.status == RunStatus.PROCESSED:
    print(f"Result: {run.output.to_dict()}")
elif run.status == RunStatus.FAILED:
    print("Processing failed")
else:
    print(f"Still processing: {run.status.value}")
```

| Parameter | Type  | Description                       |
|-----------|-------|-----------------------------------|
| `run_id`  | `str` | Unique identifier of the run      |

**Returns:** `ProcessorRun` object with current status and results

**Raises:** `RequestFailed` on error

---

## Data Structures

### ProcessorMeta

Metadata about a processor.

| Field        | Type                | Description                      |
|--------------|---------------------|----------------------------------|
| `id`         | `str`               | Unique processor identifier      |
| `name`       | `str`               | Processor name                   |
| `type`       | `ProcessorType`     | Type (EXTRACT, CLASSIFY, SPLITTER) |
| `created_at` | `datetime \| None`  | Creation timestamp               |
| `updated_at` | `datetime \| None`  | Last update timestamp            |

### ProcessorVersion

A specific version of a processor with full configuration.

| Field        | Type                                                         | Description                    |
|--------------|--------------------------------------------------------------|--------------------------------|
| `id`         | `str`                                                        | Version identifier             |
| `version`    | `str`                                                        | Version name (draft, v1, etc.) |
| `description`| `str`                                                        | Version description            |
| `processor`  | `ProcessorMeta`                                              | Processor metadata             |
| `config`     | `ConfigClassification \| ConfigExtraction \| ConfigSplitter` | Processor configuration        |
| `created_at` | `datetime`                                                   | Creation timestamp             |
| `updated_at` | `datetime`                                                   | Last update timestamp          |

### ProcessorRun

Represents a single execution of a processor.

| Field      | Type                                                              | Description                    |
|------------|-------------------------------------------------------------------|--------------------------------|
| `id`       | `str`                                                             | Run identifier                 |
| `processor`| `ProcessorMeta`                                                   | Processor that was executed    |
| `output`   | `ResultClassification \| ResultExtraction \| ResultSplitter \| None` | Processing results          |
| `status`   | `RunStatus`                                                       | Current run status             |
| `files`    | `list[StoredFile]`                                                | Associated files               |
| `usage`    | `int`                                                             | Total credits consumed         |

### StoredFile

A file stored in Extend AI.

| Field  | Type  | Description              |
|--------|-------|--------------------------|
| `id`   | `str` | Unique file identifier   |
| `type` | `str` | MIME type / file type    |
| `name` | `str` | File name                |

### Classification

A classification category definition.

| Field         | Type  | Description                        |
|---------------|-------|------------------------------------|
| `id`          | `str` | Classification identifier          |
| `type`        | `str` | Classification type/category name  |
| `description` | `str` | Description of this classification |

---

## Result Structures

### ResultExtraction

Output from an extraction processor.

| Field   | Type   | Description                            |
|---------|--------|----------------------------------------|
| `value` | `dict` | Dictionary of extracted field values   |

**Example:**

```python
if run.status == RunStatus.PROCESSED:
    extracted = run.output.value
    print(f"Name: {extracted.get('name')}")
    print(f"Amount: {extracted.get('amount')}")
```

### ResultClassification

Output from a classification processor.

| Field        | Type           | Description                            |
|--------------|----------------|----------------------------------------|
| `type`       | `str`          | Assigned classification type           |
| `confidence` | `float`        | Confidence score (0.0 to 1.0)          |
| `insights`   | `list[Insight]`| Extracted insights                     |

**Example:**

```python
if run.status == RunStatus.PROCESSED:
    print(f"Type: {run.output.type}")
    print(f"Confidence: {run.output.confidence:.2%}")
    for insight in run.output.insights:
        print(f"  {insight.type}: {insight.content}")
```

### ResultSplitter

Output from a splitter processor.

| Field    | Type          | Description                    |
|----------|---------------|--------------------------------|
| `splits` | `list[Split]` | List of identified splits      |

**Example:**

```python
if run.status == RunStatus.PROCESSED:
    for split in run.output.splits:
        print(f"Section: {split.type}")
        print(f"  Pages: {split.startPage} - {split.endPage}")
        print(f"  Observation: {split.observation}")
```

### Split

A document split/section identified by a splitter.

| Field              | Type  | Description                      |
|--------------------|-------|----------------------------------|
| `id`               | `str` | Split identifier                 |
| `type`             | `str` | Split type/category              |
| `observation`      | `str` | Observations about this split    |
| `identifier`       | `str` | Unique identifier                |
| `startPage`        | `int` | Starting page number             |
| `endPage`          | `int` | Ending page number               |
| `classificationId` | `str` | Associated classification ID     |
| `fileId`           | `str` | File this split belongs to       |
| `name`             | `str` | Split name                       |

### Insight

An insight extracted during classification.

| Field     | Type  | Description           |
|-----------|-------|-----------------------|
| `type`    | `str` | Insight type/category |
| `content` | `str` | Insight text content  |

---

## Configuration Structures

### ConfigExtraction

Configuration for extraction processors.

| Field              | Type                       | Description                           |
|--------------------|----------------------------|---------------------------------------|
| `base_processor`   | `BaseProcessor`            | Performance or light variant          |
| `extraction_rule`  | `str`                      | Custom extraction instructions        |
| `schema`           | `dict`                     | JSON Schema for extracted data        |
| `advanced_options` | `AdvancedOptionsExtraction`| Advanced settings                     |
| `parser`           | `Parser`                   | Document parser settings              |

### ConfigClassification

Configuration for classification processors.

| Field                 | Type                           | Description                       |
|-----------------------|--------------------------------|-----------------------------------|
| `classifications`     | `list[Classification]`         | Possible classification categories|
| `base_processor`      | `BaseProcessor`                | Performance or light variant      |
| `classification_rule` | `str`                          | Custom classification rules       |
| `advanced_options`    | `AdvancedOptionsClassification`| Advanced settings                 |
| `parser`              | `Parser`                       | Document parser settings          |

### ConfigSplitter

Configuration for splitter processors.

| Field                  | Type                      | Description                        |
|------------------------|---------------------------|------------------------------------|
| `split_classifications`| `list[Classification]`    | Classification categories for splits|
| `base_processor`       | `BaseProcessor`           | Performance or light variant       |
| `split_rules`          | `str`                     | Custom splitting rules             |
| `advanced_options`     | `AdvancedOptionsSplitter` | Advanced settings                  |
| `parser`               | `Parser`                  | Document parser settings           |

---

## Constants (Enums)

### ProcessorType

Types of processors available.

| Value      | Description                                    |
|------------|------------------------------------------------|
| `EXTRACT`  | Extracts structured data based on a schema     |
| `CLASSIFY` | Classifies documents into categories           |
| `SPLITTER` | Splits documents into sections                 |

### RunStatus

Status values for processor runs.

| Value        | Description                              |
|--------------|------------------------------------------|
| `PENDING`    | Run is queued and waiting to start       |
| `PROCESSING` | Run is currently being processed         |
| `PROCESSED`  | Run completed successfully               |
| `FAILED`     | Run encountered an error                 |
| `CANCELLED`  | Run was cancelled before completion      |

### VersionName

Standard version names for processors.

| Value    | Description                          |
|----------|--------------------------------------|
| `LATEST` | Latest published version             |
| `DRAFT`  | Draft/working version                |

### BaseProcessor

Base processor variants (performance vs speed trade-off).

| Value                        | Description                              |
|------------------------------|------------------------------------------|
| `CLASSIFICATION_PERFORMANCE` | High accuracy classification             |
| `CLASSIFICATION_LIGHT`       | Fast classification                      |
| `EXTRACTION_PERFORMANCE`     | High accuracy extraction                 |
| `EXTRACTION_LIGHT`           | Fast extraction                          |
| `SPLITTING_PERFORMANCE`      | High accuracy splitting                  |
| `SPLITTING_LIGHT`            | Fast splitting                           |

---

## Error Handling

### RequestFailed

Exception raised when an Extend AI API request fails (extends `RuntimeError`).

| Attribute     | Type  | Description                    |
|---------------|-------|--------------------------------|
| `status_code` | `int` | HTTP status code               |
| `message`     | `str` | Error message from Extend AI   |

**Example:**

```python
try:
    run = client.run_processor(...)
except RequestFailed as e:
    print(f"API Error {e.status_code}: {e.message}")
```

---

## Polling Pattern

Since document processing is asynchronous, use this pattern to wait for results:

```python
import time
from canvas_sdk.clients.extend_ai.constants import RunStatus

def wait_for_completion(client, run_id: str, timeout_seconds: int = 120) -> ProcessorRun:
    """
    Wait for a processor run to complete.

    Args:
        client: Extend AI client instance
        run_id: The run ID to monitor
        timeout_seconds: Maximum time to wait

    Returns:
        ProcessorRun with final status

    Raises:
        TimeoutError: If processing exceeds timeout
    """
    start_time = time.time()
    poll_interval = 2  # seconds

    while True:
        run = client.run_status(run_id)

        # Check if done
        if run.status not in (RunStatus.PENDING, RunStatus.PROCESSING):
            return run

        # Check timeout
        if time.time() - start_time > timeout_seconds:
            raise TimeoutError(f"Processing timed out after {timeout_seconds}s")

        time.sleep(poll_interval)


# Usage
run = client.run_processor(processor_id, file_name, file_url, None)
final_run = wait_for_completion(client, run.id)

if final_run.status == RunStatus.PROCESSED:
    print(final_run.output.to_dict())
```

---

## Additional Resources

- [Extend AI Documentation](https://docs.extend.ai/)
- [Example Plugin](/sdk/example-extend_ai_pdf/) - Documentation for the example plugin
- [Source Code](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/extend_ai_pdf) - View the source on GitHub
