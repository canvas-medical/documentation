---
title: 'api_samples'
slug: 'example-api_samples'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/api_samples' target='_blank'>View the source</a> for this plugin on GitHub." %}

API Samples
===========

## Description

Showcases the usage of the SimpleAPI handler. The sample requests below assume the value of my-api-key is configured to 'test123' in your Canvas instance plugin secrets via the UI or [Console](https://docs.canvasmedical.com/sdk/canvas_cli/#canvas-config-set).

GET
- Adds an API endpoint that returns "Hello World"

Sample request:
```
curl --request GET \
  --url https://xpc-dev.canvasmedical.com/plugin-io/api/api_samples/hello-world \
  --header 'authorization: test123'
```

POST
- Adds an API endpoint that accepts a JSON body and creates a Task in Canvas

Sample request:
```
curl --request POST \
  --url https://xpc-dev.canvasmedical.com/plugin-io/api/api_samples/crm-webhooks/email-bounce \
  --header 'authorization: test123' \
  --header 'content-type: application/json' \
  --data '{
  "mrn": "abc123",
  "email": "test@example.com"
}'
```

PUT
- Adds an API endpoint with a unique identifier in the url that accepts appointment data and calls an Appointment .update() effect.

Sample request:
```
curl --request PUT \
  --url https://xpc-dev.canvasmedical.com/plugin-io/api/api_samples/appointments/1140 \
  --header 'authorization: test123' \
  --header 'content-type: application/json' \
  --data '{
  "meetingLink": "https://www.example.com/video-link",
  "patientId": "d7af3e356368446c85b40a5d6ff7288e"
}'
```

## Configuration

Once installed, see the plugin configuration page to set credentials to make
authenticated requests.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.2",
    "name": "api_samples",
    "description": "Example usages of the SimpleAPI handler",
    "components": {
        "protocols": [
            {
                "class": "api_samples.routes.hello_world:HelloWorldAPI",
                "description": "Returns a json message"
            },
            {
                "class": "api_samples.routes.email_bounce:EmailBounceAPI",
                "description": "Creates a task to confirm patient contact info"
            },
            {
                "class": "api_samples.routes.appointment_updater:AppointmentAPI",
                "description": "Updates an existing appointment"
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

**Purpose**

This code defines a simple API endpoint using the Canvas SDK. The endpoint responds to HTTP GET requests by returning a JSON object that contains the message "Hello world!".

**Endpoint Details**

- The endpoint is available at the path: /hello-world
- It uses API key authentication: the request must include an Authorization header whose value matches the secret "my-api-key".
- Upon successful authentication, a GET request to this endpoint responds with:
  ```json
  {"message": "Hello world!"}
  ```

**Authentication Logic**

- The authenticate method checks if the API key provided in the request matches the one stored in the plugin's secrets under the key "my-api-key".

**Usage**

- This file would be part of a plugin for Canvas Medical that provides a demonstration endpoint for testing integrations, verifying connectivity, or serving as a template for further development.

**Summary**

In short, hello_world.py implements a secure, authenticated "Hello World" API endpoint as a quick example of using the Canvas SDK to create custom plugin routes.

```python
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute

# GET /plugin-io/api/api_samples/hello-world
# Headers: "Authorization <your value for 'my-api-key'>"

class HelloWorldAPI(SimpleAPIRoute):
    """API endpoint that returns 'Hello world!'."""
    PATH = "/hello-world"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        """Simple API key authentication."""
        return credentials.key == self.secrets["my-api-key"]

    def get(self) -> list[Response]:
        """Return a message."""
        return [JSONResponse({"message": "Hello world!"})]
```

### email_bounce.py

**Summary**

This file defines an API endpoint (using the Canvas SDK) to process "email bounce" webhook requests from a CRM system.

**API Endpoint Details**

- **Path**: `/crm-webhooks/email-bounce`
- **Method**: POST
- **Expected Request Body**: JSON containing a single key, `"mrn"`, which should be a valid patient Medical Record Number (MRN).
- **Headers**: Requires an `"Authorization"` header with an API key.

**Authentication**

- Uses API key-based authentication. The provided key is checked against a secret stored as `"my-api-key"`.

**Functionality**

- When a POST request with valid authentication is received:
    - Extracts the MRN from the JSON body.
    - Retrieves the corresponding `Patient` object from the database.
    - Calculates a due date five days in the future.
    - Creates a task for the patient with:
        - Title: "Please confirm contact information."
        - Due date: 5 days from now
        - Status: Open
        - Label: "CRM"
    - Applies (creates) the task using the Canvas task system.
    - Returns a JSON response confirming that the task was created.

**Dependencies and SDK Usage**

- Uses parts of the Canvas SDK for authentication, routing, processing tasks, and serializing responses.
- Uses the Arrow library to manipulate date and time.
- Relies on the Canvas data model for retrieving a patient by MRN.

**Intended Purpose**

- To allow external CRM systems to notify Canvas when an email sent to a patient bounces, so that clinic staff can follow up and confirm or update the patient’s contact information.

```python
import arrow

from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.effects.task import AddTask, TaskStatus
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute
from canvas_sdk.v1.data import Patient

# POST /plugin-io/api/api_samples/crm-webhooks/email-bounce
# Body: { "mrn": "valid patient MRN" }
# Headers: "Authorization <your value for 'my-api-key'>"

class EmailBounceAPI(SimpleAPIRoute):
    """API endpoint to handle email bounce webhooks from a CRM system."""
    PATH = "/crm-webhooks/email-bounce"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        """Simple API key authentication."""
        return credentials.key == self.secrets["my-api-key"]

    def post(self) -> list[Response]:
        """Create a task for the patient with the given MRN."""
        mrn_from_json = self.request.json()["mrn"]
        patient = Patient.objects.get(mrn=mrn_from_json)
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

### appointment_updater.py

**Purpose**

This file defines an API endpoint, using the Canvas SDK, for updating appointment records in a plugin for Canvas Medical.

**Endpoint Definition**

- Route: `PUT /appointments/<id>`
- Authentication: API Key (checked in request headers via APIKeyAuthMixin)

**Core Logic**

- Retrieves the appointment ID from the request URL.
- Extracts the "meetingLink" value from the JSON request body.
- Looks up the appointment record(s) in the database whose `note_id` matches the provided ID.
    - Uses the most recent record if there are multiple.
- If no appointment is found, returns a 404 Not Found error.
- Otherwise:
    - Creates an effect object for updating the appointment.
    - Sets the new meeting link on the appointment.
    - Adds (for demonstration) an external identifier to the appointment (e.g., links to an external scheduling system).
    - Returns a list with two items:
        - An effect instructing Canvas to perform the update.
        - A response with HTTP 202 (Accepted) status to indicate the update request is being processed.

**Key Canvas SDK Features Used**

- `SimpleAPIRoute`/`APIKeyAuthMixin` for simplified, authenticated API route definition.
- `AppointmentData` to query appointment objects.
- `Appointment` effect to build the update operation.
- `AppointmentIdentifier` to attach external identifiers to the appointment.
- `Response` for HTTP response construction.

**Summary**

This module handles update requests for appointments, allowing specific fields (like meeting links and external identifiers) to be set or updated through a simple, authenticated API endpoint using the Canvas SDK. If the appointment is found, it schedules the update and replies with HTTP 202; if not, it responds with HTTP 404.

```python
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.note.appointment import Appointment
from canvas_sdk.effects.note.base import AppointmentIdentifier
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPIRoute
from canvas_sdk.v1.data.appointment import Appointment as AppointmentData

# PUT /plugin-io/api/api_samples/appointments/<id>
# Headers: "Authorization <your value for 'my-api-key'>"

# Authentication is handled by the APIKeyAuthMixin, which checks the API key in the request headers
# https://docs.canvasmedical.com/sdk/handlers-simple-api-http/#api-key-1

class AppointmentAPI(APIKeyAuthMixin, SimpleAPIRoute):
    """API for managing appointment updates."""
    PATH = "/appointments/<id>"

    def put(self) -> list[Response | Effect]:
        """Update an existing appointment."""
        note_dbid = self.request.path_params.get("id")
        body = self.request.json()

        meeting_link = str(body.get("meetingLink"))

        appointments = AppointmentData.objects.filter(note_id=note_dbid)
        # or this can be a UUID if you have it
        # appointment = AppointmentData.objects.get(note__id=note_uuid)
        # the current appointment is the last one after any reschedules / updates
        appointment = appointments.last()

        if not appointment:
            return [Response(status_code=HTTPStatus.NOT_FOUND, content={"error": "Appointment not found"})]

        # set up the meeting effect to update the appointment
        appointment_effect = Appointment(instance_id=appointment.id)

        # add the meeting link to the appointment
        appointment_effect.meeting_link = meeting_link

        # let's also add some external identifiers for fun
        # for example, this could be an ID from an external scheduling system
        external_identifiers=[
            AppointmentIdentifier(system="https://www.example.com", value="123TEST")
        ]

        appointment_effect.external_identifiers = external_identifiers

        return [appointment_effect.update(), Response(status_code=HTTPStatus.ACCEPTED)]
```

<br/>
<br/>
<br/>
