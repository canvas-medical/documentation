---
title: "HTTP Request"
slug: "effect-http-request"
excerpt: "Make HTTP requests from plugins with optional effect chaining"
hidden: false
---

The `HttpRequest` effect enables plugins to make HTTP requests to external services. Use `on_success` and `on_failure` to chain additional effects based on the response status.

## Making an HTTP Request

To make an HTTP request, import the `HttpRequest` class and create an instance with the request details.

| Attribute  |          | Type         | Description                                                                                   |
|------------|----------|--------------|-----------------------------------------------------------------------------------------------|
| url        | required | string       | The URL to send the request to. Must be included in the plugin's `url_permissions`.           |
| method     | optional | string       | The HTTP method: `GET`, `POST`, `PUT`, `PATCH`, or `DELETE`. Defaults to `GET`.               |
| headers    | optional | dict         | HTTP headers to include with the request.                                                     |
| body       | optional | string       | The request body. For JSON payloads, use `json.dumps()` to serialize.                         |
| on_success | optional | list[Effect] | Effects to execute when the response status is 2xx.                                           |
| on_failure | optional | list[Effect] | Effects to execute when the response status is non-2xx or the request fails with an error.    |

```python?partial=true
import json

from canvas_sdk.effects.http_request import HttpRequest
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.CLAIM_CREATED)

    def compute(self):
        http_effect = HttpRequest(
            url="https://api.example.com/notify",
            method="POST",
            headers={
                "Authorization": "Bearer my-api-token",
                "Content-Type": "application/json",
            },
            body=json.dumps({"claim_id": self.target}),
        )

        return [http_effect.apply()]
```

## URL Permissions

The URL must be included in your plugin's `url_permissions` in `CANVAS_MANIFEST.json`. If the URL is not permitted, the effect will fail.

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "0.0.1",
  "name": "my_plugin",
  "description": "My plugin description",
  "url_permissions": [
    "https://api.example.com/*"
  ]
}
```

## Effect Chaining

Use `on_success` to chain effects that run when the response status is 2xx, and `on_failure` for effects that run when the response fails (non-2xx status or network error).

```python?partial=true
import json

from canvas_sdk.effects.http_request import HttpRequest
from canvas_sdk.effects.claim import AddClaimComment, MoveClaimToQueue
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.CLAIM_CREATED)

    def compute(self):
        claim_id = self.target

        http_effect = HttpRequest(
            url="https://api.example.com/submit-claim",
            method="POST",
            headers={"Authorization": "Bearer token"},
            body=json.dumps({"claim_id": claim_id}),
            on_success=[
                MoveClaimToQueue(claim_id=claim_id, queue="Filed").apply(),
            ],
            on_failure=[
                AddClaimComment(claim_id=claim_id, comment="External submission failed").apply(),
            ],
        )

        return [http_effect.apply()]
```

### Chained Effects with Delays

Chained effects preserve `delay_seconds` values, letting you schedule follow-up actions after a delay:

```python?partial=true
http_effect = HttpRequest(
    url="https://api.example.com/submit",
    method="POST",
    body=json.dumps({"data": "value"}),
    on_success=[
        # This effect will run 5 minutes after the HTTP request succeeds
        AddTask(
            title="Review submission result",
            patient_id=patient_id,
        ).apply(delay_seconds=300),
    ],
)
```

## Supported HTTP Methods

| Method   | Description                              |
|----------|------------------------------------------|
| `GET`    | Retrieve data from the server (default)  |
| `POST`   | Submit data to create a new resource     |
| `PUT`    | Replace an existing resource entirely    |
| `PATCH`  | Partially update an existing resource    |
| `DELETE` | Remove a resource from the server        |

<br/>
<br/>
<br/>
