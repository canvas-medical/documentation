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
