---
title: "SimpleAPI"
slug: "handlers-simple-api"
excerpt: "Framework for defining HTTP APIs with the Canvas SDK."
---

# Introduction

The Canvas SDK provides a way to define an HTTP API with any number of endpoints in your instance.

# Quickstart

Follow the instructions in [Your First Plugin](https://docs.canvasmedical.com/guides/your-first-plugin/) to create a Plugins project. Use `my_api` as your project name.

Open `CANVAS_MANIFEST.json` in your editor. You can modify filenames, directory structures, and class names as you see fit in your project, but for this exercise, we are just going to rename the value `components -> protocols -> 0 -> class` to be `my_api.protocols.my_protocol:MyAPI`.

Open `my_api/protocols/my_protocol.py` and replace the contents of the file with this code:

```python
from secrets import compare_digest

from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        provided_api_key_bytes = credentials.key.encode()
        api_key_bytes = self.secrets["my-api-key"].encode()
        return compare_digest(provided_api_key_bytes, api_key_bytes)

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```

You can see in the code above that the `authenticate` method is going to authenticate using a secret that you have installed. This endpoint is using API key authentication, which requires an API key. You can generate an API key like this:

```shell
$ python -c "import secrets; print(secrets.token_hex(16))"
50b8f5813a87235ad0678211dc6e7c22
```

Copy that value and install it as a Plugins secret called `my-api-key`.

The last step is to deploy your plugin; the instructions for doing so are on the [Your First Plugin](https://docs.canvasmedical.com/guides/your-first-plugin/) page.

After your plugin is installed, you can send requests to your endpoint with `curl`. If we are using the API key generated above, the `curl` command would look like the following (note that you will need to supply your instance name):

```shell
curl --location 'https://<instance-name>/plugin-io/api/my-api/hello-world' \
     --header 'Authorization: 50b8f5813a87235ad0678211dc6e7c22'
```

# Defining APIs

The Canvas SDK offers two styles for defining API endpoints. Both styles allow for creating GET, POST, PUT, DELETE, and PATCH endpoints. To implement an API endpoint or set of endpoints using one of the two styles, your handler will simply inherit from a specific base class.

## SimpleAPIRoute

For handlers that inherit from SimpleAPIRoute, you supply a `PATH` value, like `/my-api/hello-world` above, and then implementations of the HTTP verbs you wish to support on that path.

I can adapt the previous example to add a POST endpoint on the same handler:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        ...

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world from my GET endpoint!"})
        ]

    def post(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world from my POST endpoint!"})
        ]
```

The handler can now respond to both GET and POST requests to `/my-api/hello-world`.

## SimpleAPI

For handlers that inherit from SimpleAPI, the syntax is a little different. You can include any number of endpoints in your handler class, and you can name your route handling methods anything you wish. Here is an example:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPI


class MyAPI(SimpleAPI):
    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        ...

    @api.get("/my-api/hello-world")
    def hello_world_get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world from my GET endpoint!"})
        ]

    @api.post("/my-api/hello-world")
    def hello_world_post(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world from my POST endpoint!"})
        ]

    @api.put("/my-api/hello-world")
    def hello_world_put(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world from my PUT endpoint!"})
        ]

    @api.get("/my-api/goodbye")
    def goodbye_get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Goodbye from my GET endpoint!"})
        ]

```

This syntax will be familiar if you are familiar with Python API frameworks like `Flask` or `FastAPI`. If you have many endpoints that you wish to share the same authentication, this syntax may be more convenient.

You can also specify a path `PREFIX` value for endpoint grouping purposes. If you have multiple endpoints that will all have the same path prefix, you can specify it by setting a value for `PREFIX`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPI


class MyAPI(SimpleAPI):
    PREFIX = "/my-api"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        ...

    @api.get("/hello-world")
    def hello_world_get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world from my GET endpoint!"})
        ]

    @api.post("/hello-world")
    def hello_world_post(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world from my POST endpoint!"})
        ]

    @api.get("/goodbye")
    def goodbye_get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Goodbye from my GET endpoint!"})
        ]
```

With `PREFIX` set, each endpoint does not have to individually specify the `/my-api` portion of the URL path.

## Request objects

When a handler is invoked to handle an incoming HTTP request, the request object is available as an attribute on the handler. The request method, path, query parameters, content type, and body are all available as attributes on the request object:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        ...

    def get(self) -> list[Response | Effect]:
        request = self.request

        # HTTP method
        method = request.method

        # URL path component
        path = request.path

        # Raw query string
        query_string = request.query_string

        # Query parameters as a Python dict
        query_params = request.query_params

        # Request headers
        headers = request.header

        # Request body content type
        content_type = request.content_type

        # Raw body
        body = request.body

        # JSON body as a Python dict (for requests with application/json content types)
        json_body = request.json()

        # Body as plain text
        text_body = request.text()

        return [
            JSONResponse({"message": "Hello world!"})
        ]
```

## Responses

Endpoint handlers may return zero or one response objects and any number of Effects. Handlers that return multiple response objects will return a **500 Internal Server Error** response back to the requester.

### Response types

Several response types are provided for convenience:

* HTMLResponse
* JSONResponse
* PlainTextResponse
* Response (for returning raw content)

In addition to the response body, you can also specify the response status code and the response headers.


```python
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import HTMLResponse, JSONResponse, PlainTextResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        ...

    def get(self) -> list[Response | Effect]:
        return [
            HTMLResponse(
                "<p>Hello world from my GET endpoint!</p>",
                status_code=HTTPStatus.OK,
                headers={"My-Header", "my header value"}
            )
        ]

    def post(self) -> list[Response | Effect]:
        return [
            JSONResponse(
                {"message": "Hello world from my POST endpoint!"},
                status_code=HTTPStatus.CREATED,
                headers={"My-Header", "my header value"}
            )
        ]

    def put(self) -> list[Response | Effect]:
        return [
            PlainTextResponse(
                "Hello world from my PUT endpoint!"},
                status_code=HTTPStatus.ACCEPTED,
                headers={"My-Header", "my header value"}
            )
        ]

    def patch(self) -> list[Response | Effect]:
        return [
            Response(
                b'{"message": "Hello world from my PUT endpoint!"}'
                status_code=HTTPStatus.NOT_MODIFIED,
                headers={"My-Header", "my header value"},
                content_type="application/json"
            )
        ]
```

### Returning Effects

SimpleAPI endpoints can return any number of Effects just like any Canvas plugin; this is why SimpleAPI endpoints return a list of items rather than just a response object.

Endpoints can also return Effects along with a response object, if you want your endpoint to invoke certain Effects and then also return an HTTP response. To do this, just return a list that includes your response object and all of the Effects you wish to invoke.

If your endpoint does not provide a response object, then the requester will receive a **204 No Content** response.

## Authentication

Defining an `authenticate` method on your handler is required. By default, SimpleAPI handlers will return a **401 Unauthorized** response.

Credentials, custom
