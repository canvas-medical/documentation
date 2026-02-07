---
title: 'AWS S3'
slug: 'example-aws_s3'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/aws_s3' target='_blank'>View the source</a> for this plugin on GitHub." %}


## Description

Plugin that provides a SimpleAPI for managing AWS S3 objects, including listing, uploading, downloading, deleting files, and generating presigned URLs. It also includes a chart application that renders a form interface for interacting with S3 directly from the chart.

## Configuration

This example plugin defines the following "secrets" in the manifest file:

```
    "secrets": [
        "S3Key",
        "S3Secret",
        "S3Region",
        "S3Bucket"
    ],
```
Once defined in the `MANIFEST.json`, set the secrets for your plugin in the Admin UI of your Canvas EMR. [Read more](https://docs.canvasmedical.com/sdk/secrets/)

### S3Key
Your AWS Access Key ID.

### S3Secret
Your AWS Secret Access Key.

### S3Region
The AWS region where your S3 bucket is located (e.g., `us-east-1`).

### S3Bucket
The name of your S3 bucket.

## CANVAS_MANIFEST.json

```json
{
  "sdk_version": "0.81.0",
  "plugin_version": "0.0.1",
  "name": "aws_manip",
  "description": "use AWS S3 to store, retrieve and delete documents",
  "components": {
    "protocols": [
      {
        "class": "aws_manip.handlers.aws_manip:AwsManip",
        "description": "AWS extractor based on AWS S3"
      }
    ],
    "applications": [
      {
        "class": "aws_manip.handlers.aws_form_app:AwsFormApp",
        "name": "AWS S3 Document Management",
        "description": "AWS S3 manip",
        "icon": "static/aws_manip.png",
        "scope": "patient_specific",
        "show_in_panel": false
      }
    ],
    "commands": [],
    "content": [],
    "effects": [],
    "views": []
  },
  "secrets": [
    "S3Key",
    "S3Secret",
    "S3Region",
    "S3Bucket"
  ],
  "tags": {},
  "references": [],
  "license": "",
  "diagram": false,
  "readme": "./README.md"
}
```

## handlers/

### aws_manip.py

**Purpose**

This code defines a SimpleAPI handler that exposes REST endpoints for managing objects in an Amazon S3 bucket using the Canvas SDK's AWS S3 client.

**Class Overview**

- The main class, `AwsManip`, extends `SimpleAPI`.
- It creates an S3 client using credentials stored in plugin secrets.

**Main Workflow**

- `GET /list_items` — Lists all objects in the configured S3 bucket.
- `GET /get_item/<item_key>` — Retrieves an object's content by its key.
- `GET /presigned_url/<item_key>` — Generates a presigned URL for temporary (1-hour) access to an object.
- `POST /upload_item/<item_key>` — Uploads content to S3, handling both text and binary content types.
- `DELETE /delete_item/<item_key>` — Deletes an object from S3 by key.

**S3 Client Integration**

- The `_s3_client` method creates an `S3` client instance from `canvas_sdk.clients.aws.libraries`, configured with `S3Credentials` from plugin secrets.
- Each endpoint checks `client.is_ready()` before performing operations.

```python?partial=true
from http import HTTPStatus

from aws_manip.constants.secrets import Secrets
from canvas_sdk.clients.aws.libraries import S3
from canvas_sdk.clients.aws.structures import Credentials as S3Credentials
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, PlainTextResponse, Response
from canvas_sdk.handlers.simple_api import Credentials, SimpleAPI, api


class AwsManip(SimpleAPI):
    """Simple API handler for AWS S3 object management operations."""

    PREFIX = None
    USER_TYPE_STAFF = "Staff"

    def authenticate(self, credentials: Credentials) -> bool:
        """Authenticate API requests.

        Args:
            credentials: The credentials provided with the request.

        Returns:
            True to allow all requests (authentication bypassed).
        """
        return True

    def _s3_client(self) -> S3:
        """Create and configure an S3 client with credentials from secrets.

        Returns:
            Configured S3 client instance.
        """
        return S3(
            S3Credentials(
                key=self.secrets[Secrets.s3_key],
                secret=self.secrets[Secrets.s3_secret],
                region=self.secrets[Secrets.s3_region],
                bucket=self.secrets[Secrets.s3_bucket],
            )
        )

    @api.get("/list_items")
    def list_items(self) -> list[Response | Effect]:
        """List all objects in the S3 bucket."""
        client = self._s3_client()
        if client.is_ready():
            content = [p.key for p in client.list_s3_objects("")]
            status_code = HTTPStatus(HTTPStatus.OK)
            return [JSONResponse(content, status_code=status_code)]
        return []

    @api.get("/get_item/<item_key>")
    def get_item(self) -> list[Response | Effect]:
        """Retrieve an object's content from S3 by key."""
        item_key = self.request.path_params["item_key"]
        client = self._s3_client()
        if client.is_ready() and item_key:
            content = client.access_s3_object(item_key).content
            status_code = HTTPStatus(HTTPStatus.OK)
            return [Response(content, status_code=status_code)]
        return []

    @api.get("/presigned_url/<item_key>")
    def presigned_url(self) -> list[Response | Effect]:
        """Generate a presigned URL for temporary access to an S3 object."""
        item_key = self.request.path_params["item_key"]
        client = self._s3_client()
        if client.is_ready() and item_key:
            content = client.generate_presigned_url(item_key, 3600)
            status_code = HTTPStatus(HTTPStatus.OK)
            return [PlainTextResponse(content, status_code=status_code)]
        return []

    @api.post("/upload_item/<item_key>")
    def upload_item(self) -> list[Response | Effect]:
        """Upload content to S3 with the specified key."""
        item_key = self.request.path_params["item_key"]
        client = self._s3_client()
        content = self.request.body
        content_type = self.request.content_type
        if client.is_ready() and item_key:
            if content_type == "text/plain":
                response = client.upload_text_to_s3(item_key, content.decode("utf-8"))
            else:
                response = client.upload_binary_to_s3(item_key, content, content_type)
            return [Response(response.content, status_code=response.status_code)]
        return []

    @api.delete("/delete_item/<item_key>")
    def delete_item(self) -> list[Response | Effect]:
        """Delete an object from S3 by key."""
        item_key = self.request.path_params["item_key"]
        client = self._s3_client()
        if client.is_ready() and item_key:
            content = client.delete_object(item_key).content
            status_code = HTTPStatus(HTTPStatus.OK)
            return [Response(content, status_code=status_code)]
        return []
```

### aws_form_app.py

**Purpose**

This code defines an Application handler that launches a modal form in the right chart pane for interacting with the S3 management API endpoints.

```python?partial=true
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application
from canvas_sdk.templates import render_to_string


class AwsFormApp(Application):
    """Application handler for launching the AWS S3 management form interface."""

    PLUGIN_API_BASE_ROUTE = "/plugin-io/api/aws_manip"

    def on_open(self) -> Effect:
        """Render and launch the AWS S3 management modal form."""
        content = render_to_string(
            "templates/aws_form.html",
            {
                "listItemsURL": f"{self.PLUGIN_API_BASE_ROUTE}/list_items",
                "getItemURL": f"{self.PLUGIN_API_BASE_ROUTE}/get_item",
                "presignedUrlURL": f"{self.PLUGIN_API_BASE_ROUTE}/presigned_url",
                "uploadItemURL": f"{self.PLUGIN_API_BASE_ROUTE}/upload_item",
                "deleteItemURL": f"{self.PLUGIN_API_BASE_ROUTE}/delete_item",
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
