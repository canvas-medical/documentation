---
title: "SimpleAPI WebSocket"
slug: "handlers-simple-api-websocket"
excerpt: "Framework for defining HTTP APIs with the Canvas SDK."
---

WebSocket APIs in Canvas let you define **channels** that clients can connect to. These APIs support one-way, server-to-client communication, and are designed for use cases such as real-time notifications.

### Defining a WebSocket API

To define a WebSocket handler, subclass `WebSocketAPI`. You must implement an `authenticate` method that determines whether the connection should be accepted.

```python
from canvas_sdk.handlers.simple_api.websocket import WebSocketAPI

class MyWebSocketAPI(WebSocketAPI):
    def authenticate(self) -> bool:
        ...
```

If `authenticate()` returns `True`, the connection is accepted. Otherwise, it is denied.


Clients should connect using a URL that maps to your plugin and channel name:

```
wss://<instance>.canvasmedical.com/plugin-io/ws/<plugin_name>/<channel_name>/
```


### WebSocket Object

When a handler is invoked, the `websocket` object is available as an attribute on the handler. This object provides details about the connection, including:
- `channel`: The channel name from the connection URL
- `headers`: A dictionary of headers associated with the connection
- `api_key`: The api key, if present
- `logged_in_user`: A dictionary like `{ "id": ..., "type": ... }` if a logged-in user is present

You can access this object within your handler methods using `self.websocket`.

### Authentication

You must implement the `authenticate()` method in your handler class. Two authentication methods are supported:

##### Session-Based (Internal Clients)
For connections initiated from within the Canvas browser UI by a logged-in user:

```python
def authenticate(self) -> bool:
  logged_in_user = self.websocket.logged_in_user
  # Structure looks like:
  # {
  #     "id": "abc123",
  #     "type": "Staff"
  # }
  # Where "type" is "Staff" or "Patient"
  # You could authenticate based on type or check to see if the
  # individual is in a particular group or team.
  ...
```

##### APIKey-Based (External Clients)
For external tools or scripts, pass an auth key as a query parameter:

```python
wss://<instance>.canvasmedical.com/plugin-io/ws/<plugin>/<channel>?api_key=<key>
```

The key is made available in your handler via `self.websocket.api_key`. You can store this key as a secret.

```python
def authenticate(self) -> bool:
  provided_token = self.websocket.api_key
  
  # Validate provided key against an API key in self.secrets
  ...
```


### Broadcasting Messages

To send a message to all connected clients on a WebSocket channel, use the `Broadcast` effect. This effect can be returned from any handler.

The `Broadcast` effect takes the following parameters:

- `message`: A JSON-serializable Python dictionary or value.
- `channel`: The target channel name as a string.

Here’s an example using a SimpleAPI HTTP POST route to trigger a broadcast:

```python
from http import HTTPStatus
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.effects.websocket import Broadcast
from canvas_sdk.handlers.simple_api import Credentials, SimpleAPI, api

class WebhookAPI(SimpleAPI):
    @api.post("/callback")
    def broadcast_message(self) -> list[Response | Effect]:
        body = self.request.json()

        return [
            Broadcast(message=body, channel="notifications").apply(),
            JSONResponse({"status": "ok"}, status_code=HTTPStatus.ACCEPTED),
        ]
```
In this example, when the `/callback` endpoint receives a POST request, it broadcasts the request body as a message to all clients subscribed to the `notifications` channel.


