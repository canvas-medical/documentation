---
title: 'api_samples'
slug: 'example-api_samples'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/api_samples' target='_blank'>View the source</a> for this plugin on GitHub." %}

API Samples
===========

## Description

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

### hello_world.py

**File Purpose**

The code defines an API endpoint for a Canvas Medical plugin using the Canvas SDK. The endpoint responds to HTTP GET requests with a simple JSON hello world message. The endpoint includes API key authentication.

**Authentication**

- The endpoint uses the APIKeyCredentials mechanism.
- In the authenticate method, it checks if the provided credentials key matches the value stored as "my-api-key" in the plugin's secrets.
- Only requests with the correct API key in the Authorization header will succeed.

**API Endpoint**

- The route provided by the class is "/hello-world".
- When a GET request is made to this endpoint, it returns a JSON response containing: {"message": "Hello world!"}

**Response**

- The response is always an HTTP 200 JSON object with the specified message.
- Only authenticated requests (correct API key) receive the JSON hello world message.

**Summary**

- The file implements a secure, authenticated GET endpoint in a Canvas plugin.
- When accessed with the proper API key, it returns a simple "Hello world!" message in JSON format.

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

### email_bounce.py

**Purpose**

This code defines an API endpoint (using the Canvas SDK) that listens for email bounce webhooks related to patients (identified by MRN). When this endpoint is called, it attempts to create a follow-up task for that patient.

**Authentication**

Before processing, the endpoint checks that the API key in the `Authorization` header matches the secret value `"my-api-key"`.

**Endpoint Details**

- **URL:** `/crm-webhooks/email-bounce`
- **Method:** POST
- **Expected Body:** JSON object containing a `"mrn"` field (patient's MRN)
- **Headers:** Must include a valid API key

**Processing Logic**

1. **Look Up Patient:** Retrieves the Patient object using the supplied MRN from the incoming JSON request.
2. **Calculate Due Date:** Sets a due date for the task five days from the current UTC time, using `arrow`.
3. **Create Task:** Instantiates a new task for the identified patient with:
    - Title: `"Please confirm contact information."`
    - Due date: five days from now
    - Status: OPEN
    - Label: `"CRM"`
4. **Apply Effects:** Applies the task creation, then returns a JSON response indicating success (`{"message": "Task Created"}`).

**Outputs**

Returns two effects:
- The result of applying the AddTask effect (creating the task)
- A JSON response confirming task creation

**Typical Usage**

This endpoint would commonly be hooked up to an external CRM or email delivery service, so that when an email sent to a patient bounces, a follow-up task is automatically created for staff to verify the patient's contact information.

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

<br/>
<br/>
<br/>
