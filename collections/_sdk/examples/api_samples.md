---
title: 'API Samples'
slug: 'example-api_samples'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/api_samples' target='_blank'>View the source</a> for this plugin on GitHub." %}

Showcases the usage of the SimpleAPI handler

## Configuration

Once installed, see the plugin configuration page to set credentials to make
authenticated requests.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "api_samples",
    "description": "Example usages of the SimpleAPI handler",
    "components": {
        "protocols": [
            {
                "class": "api_samples.routes.hello_world:HelloWorldAPI",
                "description": "Returns a json message",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            },
            {
                "class": "api_samples.routes.email_bounce:EmailBounceAPI",
                "description": "Creates a task to confirm patient contact info",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": ["my-api-key"],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## routes/

### email_bounce.py

The code defines an endpoint for handling bounced email events.

**Endpoint**

- **Path:** `/crm-webhooks/email-bounce`
- **Method:** POST
- **Expected Body:** JSON containing `{"mrn": "valid patient MRN"}`
- **Authorization:** Requires an API key in the `Authorization` header that matches the plugin secret `'my-api-key'`.

**Core Functionality**

- When a POST request is received:
  - It authenticates the request by verifying the provided API key against a stored secret.
  - It retrieves the `Patient` object from the database with the given MRN (Medical Record Number) from the request body.
  - It schedules a new open task for that patient:
    - **Title:** `"Please confirm contact information."`
    - **Due Date:** 5 days from the current UTC date
    - **Label:** `"CRM"`
- Returns a response indicating both the creation of the task and a confirmation JSON message.

**Intended Use**

This endpoint provides an automated workflow to prompt staff to confirm and update patient contact information in response to an email bounce event, improving contact data quality in clinical operations.

```python
import arrow

from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.effects.task import AddTask, TaskStatus
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute
from canvas_sdk.v1.data import Patient

#
# POST /plugin-io/api/api_samples/crm-webhooks/email-bounce
# Body: { "mrn": "valid patient MRN" }
# Headers: "Authorization <your value for 'my-api-key'>"
#


class EmailBounceAPI(SimpleAPIRoute):
    PATH = "/crm-webhooks/email-bounce"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        return credentials.key == self.secrets["my-api-key"]

    def post(self) -> list[Response]:
        patient = Patient.objects.get(mrn=self.request.json()["mrn"])
        five_days_from_now = arrow.utcnow().shift(days=5).datetime

        task_effect = AddTask(
            patient_id=patient.id,
            title="Please confirm contact information.",
            due=five_days_from_now,
            status=TaskStatus.OPEN,
            labels=["CRM"],
        )

        return [task_effect.apply(), JSONResponse({"message": "Task Created"})]
```

### hello_world.py

This code defines a simple API endpoint which handles requests to the path `/hello-world`. When a GET request is made to this endpoint, the API responds with a JSON message that says "Hello world!".

**Authentication**

The endpoint requires an API key for authentication. The client must provide an API key (as a header called `Authorization`). The provided key is compared to a value stored in `self.secrets["my-api-key"]`. If the keys match, authentication is successful and the request is allowed; otherwise, it will be denied.

**Response**

A GET request to `/plugin-io/api/api_samples/hello-world` (when authenticated) returns a JSON response in the following format:

```json
{
  "message": "Hello world!"
}
```

```python
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute

#
# GET /plugin-io/api/api_samples/hello-world
# Headers: "Authorization <your value for 'my-api-key'>"
#


class HelloWorldAPI(SimpleAPIRoute):
    PATH = "/hello-world"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        return credentials.key == self.secrets["my-api-key"]

    def get(self) -> list[Response]:
        return [JSONResponse({"message": "Hello world!"})]
```

<br/>
<br/>
<br/>
