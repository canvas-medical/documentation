---
title: 'Extend AI PDF'
slug: 'example-extend_ai_pdf'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/extend_ai_pdf' target='_blank'>View the source</a> for this plugin on GitHub." %}


## Description

Plugin that provides a SimpleAPI for intelligent document processing using the Extend AI client. It supports listing processors, running document extraction on PDF files, checking run status, managing stored files, and retrieving processing results. Includes a chart application that renders a form interface for PDF processing directly from the chart.

## Configuration

This example plugin defines the following "secrets" in the manifest file:

```
    "variables": [
        {"name": "ExtendAiKey", "sensitive": true}
    ],
```
Once defined in the `MANIFEST.json`, set the secrets for your plugin in the Admin UI of your Canvas EMR. [Read more](https://docs.canvasmedical.com/sdk/secrets/)

### ExtendAiKey
Your Extend AI API key.

## CANVAS_MANIFEST.json

```json
{
  "sdk_version": "0.81.0",
  "plugin_version": "0.0.1",
  "name": "pdf_manip",
  "description": "use extent.ai to extract information from a PDF document",
  "components": {
    "handlers": [
      {
        "class": "pdf_manip.handlers.pdf_manip:PdfManip",
        "description": "PDF extractor based on extent.ai"
      }
    ],
    "applications": [
      {
        "class": "pdf_manip.handlers.pdf_form_app:PdfFormApp",
        "name": "PDF Upload",
        "description": "Extend.ai manip",
        "icon": "static/pdf_manip.png",
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
    {"name": "ExtendAiKey", "sensitive": true}
  ],
  "tags": {},
  "references": [],
  "license": "",
  "diagram": false,
  "readme": "./README.md"
}
```

## handlers/

### pdf_manip.py

**Purpose**

This code defines a SimpleAPI handler that exposes REST endpoints for processing PDF documents using the Extend AI client from the Canvas SDK.

**Class Overview**

- The main class, `PdfManip`, extends `StaffSessionAuthMixin` and `SimpleAPI`.
- It creates an Extend AI client using an API key stored in plugin secrets.

**Main Workflow**

- `GET /processors` — Lists all available Extend AI processors.
- `GET /processors/<processor_id>` — Retrieves configuration for a specific processor.
- `POST /execute` — Starts a processor run on a document from a public S3 URL.
- `GET /status/<run_id>` — Checks the status of a run and cleans up files if completed.
- `GET /result/<run_id>` — Retrieves the processing result for a completed run.
- `GET /stored_files` — Lists all files stored in Extend AI.
- `POST /delete_files` — Deletes specified files from Extend AI storage.

**Extend AI Client Integration**

- The `_extend_client` method creates a `Client` instance from `canvas_sdk.clients.extend_ai.libraries`.
- Error handling uses the `RequestFailed` exception from the Extend AI client structures.

```python
from datetime import datetime
from http import HTTPStatus

from canvas_sdk.clients.extend_ai.constants import RunStatus, VersionName
from canvas_sdk.clients.extend_ai.libraries import Client
from canvas_sdk.clients.extend_ai.structures import RequestFailed
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import SimpleAPI, StaffSessionAuthMixin, api
from pdf_manip.constants.secrets import Secrets


class PdfManip(StaffSessionAuthMixin, SimpleAPI):
    """API handler for Extend AI PDF processing operations."""

    PREFIX = None
    USER_TYPE_STAFF = "Staff"

    def _extend_client(self) -> Client:
        """Create and return a configured Extend AI client."""
        return Client(self.secrets[Secrets.extend_ai_key])

    @api.get("/processors")
    def list_processors(self) -> list[Response | Effect]:
        """Retrieve all available Extend AI processors."""
        try:
            content: list | dict = [p.to_dict() for p in self._extend_client().list_processors()]
            status_code = HTTPStatus(HTTPStatus.OK)
        except RequestFailed as e:
            content = {"information": e.message}
            status_code = HTTPStatus(e.status_code)
        return [JSONResponse(content, status_code=status_code)]

    @api.get("/processors/<processor_id>")
    def get_processor(self) -> list[Response | Effect]:
        """Retrieve the configuration for a specific processor by ID."""
        try:
            processor_id = self.request.path_params["processor_id"]
            response = self._extend_client().processor(processor_id, VersionName.DRAFT.value)
            content = response.config.to_dict()
            status_code = HTTPStatus(HTTPStatus.OK)
        except RequestFailed as e:
            content = {"information": e.message}
            status_code = HTTPStatus(e.status_code)
        return [JSONResponse(content, status_code=status_code)]

    @api.get("/result/<run_id>")
    def run_result(self) -> list[Response | Effect]:
        """Retrieve the processing result for a completed run."""
        try:
            run_id = self.request.path_params["run_id"]
            response = self._extend_client().run_status(run_id)
            if response.status == RunStatus.PROCESSED:
                content = {"result": response.output.to_dict()}
                status_code = HTTPStatus(HTTPStatus.OK)
            else:
                content = {"result": response.status}
                status_code = HTTPStatus(HTTPStatus.UNPROCESSABLE_ENTITY)
        except RequestFailed as e:
            content = {"information": e.message}
            status_code = HTTPStatus(e.status_code)
        return [JSONResponse(content, status_code=status_code)]

    @api.get("/status/<run_id>")
    def run_status(self) -> list[Response | Effect]:
        """Check the status of a processor run and clean up files if completed."""
        try:
            run_id = self.request.path_params["run_id"]
            extend_ai = self._extend_client()
            response = extend_ai.run_status(run_id)
            if response.status == RunStatus.PROCESSED:
                for file in response.files:
                    extend_ai.delete_file(file.id)
            content = {"runId": response.id, "status": response.status.value}
            status_code = HTTPStatus(HTTPStatus.OK)
        except RequestFailed as e:
            content = {"information": e.message}
            status_code = HTTPStatus(e.status_code)
        return [JSONResponse(content, status_code=status_code)]

    @api.get("/stored_files")
    def extend_stored_files(self) -> list[Response | Effect]:
        """List all files stored in Extend AI."""
        try:
            content: list | dict = [f.to_dict() for f in self._extend_client().list_files()]
            status_code = HTTPStatus(HTTPStatus.OK)
        except RequestFailed as e:
            content = {"information": e.message}
            status_code = HTTPStatus(e.status_code)
        return [JSONResponse(content, status_code=status_code)]

    @api.post("/delete_files")
    def extend_delete_files(self) -> list[Response | Effect]:
        """Delete specified files from Extend AI storage."""
        try:
            content: list | dict = [
                {
                    "id": file_id,
                    "deleted": self._extend_client().delete_file(file_id),
                }
                for file_id in self.request.json().get("fileIds") or []
            ]
            status_code = HTTPStatus(HTTPStatus.OK)
        except RequestFailed as e:
            content = {"information": e.message}
            status_code = HTTPStatus(e.status_code)
        return [JSONResponse(content, status_code=status_code)]

    @api.post("/execute")
    def run_start(self) -> list[Response | Effect]:
        """Start a processor run on a document from a public S3 URL."""
        try:
            received = self.request.json()
            aws_s3_url = received.get("fileAwsS3Url")
            processor_id = received.get("processorId")

            response = self._extend_client().run_processor(
                processor_id=processor_id,
                file_name=f"processed-{datetime.now().isoformat(timespec='seconds')}",
                file_url=aws_s3_url,
                config=None,
            )
            content = {"runId": response.id, "status": response.status.value}
            status_code = HTTPStatus(HTTPStatus.OK)
        except RequestFailed as e:
            content = {"information": e.message}
            status_code = HTTPStatus(e.status_code)
        return [JSONResponse(content, status_code=status_code)]
```

### pdf_form_app.py

**Purpose**

This code defines an Application handler that launches a modal form in the right chart pane for interacting with the Extend AI PDF processing API endpoints.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application
from canvas_sdk.templates import render_to_string


class PdfFormApp(Application):
    """Application handler that displays the PDF processing form in a modal."""

    PLUGIN_API_BASE_ROUTE = "/plugin-io/api/pdf_manip"

    def on_open(self) -> Effect:
        """Render and launch the PDF processing form modal in the right chart pane."""
        content = render_to_string(
            "templates/pdf_form.html",
            {
                "processorsURL": f"{self.PLUGIN_API_BASE_ROUTE}/processors",
                "statusURL": f"{self.PLUGIN_API_BASE_ROUTE}/status",
                "executeURL": f"{self.PLUGIN_API_BASE_ROUTE}/execute",
                "resultURL": f"{self.PLUGIN_API_BASE_ROUTE}/result",
                "storedFilesURL": f"{self.PLUGIN_API_BASE_ROUTE}/stored_files",
                "deleteFilesURL": f"{self.PLUGIN_API_BASE_ROUTE}/delete_files",
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
