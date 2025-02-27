---
title: "SimpleAPI"
slug: "handlers-simpleapi"
excerpt: "Framework for defining HTTP APIs with the Canvas SDK."
---

## Introduction

The Canvas SDK provides a way to define an HTTP API with any number of endpoints in your instance.
Developers can define the routes and implement the code that will handle incoming HTTP requests.

This feature allows developers to create endpoints that can receive webhook events from other
services and act on them. This can be used to invoke Effects in a Canvas instance, send another
request to a different service, or simply return a response back to the requester.

## Quickstart

Follow the instructions in
[Your First Plugin](https://docs.canvasmedical.com/guides/your-first-plugin/) to create a Plugins
project. For this exercise, use `my_api` as your project name.

Open `CANVAS_MANIFEST.json` in your editor. You can modify filenames, directory structures, and
class names as you see fit in your project, but for this exercise, we are just going to set the
value at `components -> protocols -> 0 -> class` to be `my_api.protocols.my_protocol:MyAPI`.

Open `my_api/protocols/my_protocol.py` and replace the contents of the file with this code:

```python
from secrets import compare_digest

from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        provided_api_key = credentials.key
        api_key = self.secrets["my-api-key"]

        # compare_digest requires bytes, so we must encode the strings
        return compare_digest(provided_api_key.encode(), api_key.encode())

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```

You can see in the code above that the `authenticate` method is going to authenticate using a secret
that you have set on your instance. This endpoint is using API key authentication, which requires an
API key. You can generate an API key like this:

```shell
python -c "import secrets; print(secrets.token_hex(16))"
```

Copy the value that it prints out and set it as a Plugins secret on your instance called
`my-api-key`.

The last step is to deploy your plugin; the instructions for doing so are on the
[Your First Plugin](https://docs.canvasmedical.com/guides/your-first-plugin/) page.

After your plugin is deployed, you can send requests to your endpoint with `curl`. The `curl`
command would look like the following (note that you will need to supply your instance name and API
key):

```shell
curl --location 'https://<instance-name>.canvasmedical.com/plugin-io/api/my-api/hello-world' \
     --header 'Authorization: <api-key>'
```

## Defining APIs

The Canvas SDK offers two styles for defining API endpoints. To implement an API endpoint or set of
endpoints using one of the two styles, your handler will simply inherit from a specific base class.
The following HTTP verbs are supported:

* GET
* POST
* PUT
* DELETE
* PATCH

### SimpleAPIRoute

For handlers that inherit from **SimpleAPIRoute**, you set a class variable in your handler called
`PATH` as in the example above, and then implementations of the HTTP verbs you wish to support on
that path. The method names will match the names of the HTTP verbs, but lowercased.

The `PATH` value will be the unique part of the full URL for your endpoint. The format of the full
URL will be:

`https://<instance-name>.canvasmedical.com/plugio-io/api/<PATH>`

We can adapt the previous example to add a POST endpoint for the same route on the same handler:

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

The handler can now respond to both GET and POST requests at `/my-api/hello-world`.

### SimpleAPI

For handlers that inherit from **SimpleAPI**, the syntax is a little different. You can include any
number of endpoints in your handler class, and you can name your route handling methods anything you
wish. Here is an example:

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

This syntax will be familiar if you have used Python API frameworks like `Flask` or `FastAPI`. The
decorator functions are named for the HTTP verb you wish to implement on the route, and the URL path
is passed into the decorator function. If you have many endpoints that you wish to share the same
authentication, this syntax may be more convenient.

You can also specify a path `PREFIX` value for endpoint grouping purposes, as shown in the example
above. If you have multiple endpoints that will all have the same path prefix, you can specify it by
setting a value for `PREFIX`. With `PREFIX` set, each endpoint does not have to individually specify
the `/my-api` portion of the URL path.

### Request objects

When a handler is invoked to handle an incoming HTTP request, the request object is available as an
attribute on the handler. The request method, path, query parameters, content type, and body are all
available as attributes on the request object:

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
        headers = request.headers

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

### Responses

Endpoint handlers may return zero or one response objects and any number of Effects. Handlers that
return multiple response objects will return a **500 Internal Server Error** response back to the
requester. If your endpoint does not provide a response object, then the requester will receive a
**204 No Content** response.

#### Response types

Several response types are provided for convenience:

* HTMLResponse
* JSONResponse
* PlainTextResponse
* Response (for returning raw content)

In addition to the response body, you can also specify the response status code and the response
headers.

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
                b'{"message": "Hello world from my PATCH endpoint!"}'
                status_code=HTTPStatus.NOT_MODIFIED,
                headers={"My-Header", "my header value"},
                content_type="application/json"
            )
        ]
```

#### Returning Effects

**SimpleAPI** endpoints can return any number of Effects just like any Canvas plugin; this is why
**SimpleAPI** endpoints return a list of items rather than just a single response object.

Any effects present in the list returned by an endpoint will be processed by your Canvas instance,
and the response object, if provided, will be sent back to the original requester.

### Authentication

Defining an `authenticate` method on your handler is required. By default, **SimpleAPI** handlers
will return a **401 Unauthorized** response if no `authenticate` method is defined. The
`authenticate` method should return `True` or `False` depending on whether the requester is
authenticated.

Please keep in mind that while setting Plugins secrets on your instance is out of scope for this
guide, best practices would dictate that most `authenticate` methods would use these secrets to
authenticate credentials in a request (OAuth being a notable exception). Your secrets can be
accessed through the `secrets` attribute on the handler.

Additionally, to assist with adhering to security and cryptography best practices, the Python
`hashlib`, `hmac`, and `secrets` modules are available for use.

Examples of how to define `authenticate` methods for various authentication schemes are shown in the
next section, but if you are interested in something that is more "batteries included", please skip
ahead to the [Authentication mixins](#authentication-mixins) section below. The
[API key authentication mixin](#api-key-1) is a good choice that offers simplicity and good security
if you need something to get started.

#### Authentication schemes

The Canvas SDK can parse and validate the format of the Authentication header automatically for
several authentication schemes, but you must authenticate the credentials in your `authenticate`
method. You can specify which authentication scheme you want to use for your route or API in the
method signature of your `authenticate` method.

##### Basic

For Basic authentication, use `BasicCredentials`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import BasicCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: BasicCredentials) -> bool:
        provided_username = credentials.username
        provided_password = credentials.password

        # Validate provided username and password against a username and password in self.secrets
        ...

    def get(self) -> list[Response | Effect]:
        ...
```

##### Bearer

For Bearer authentication, use `BearerCredentials`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import BearerCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: BearerCredentials) -> bool:
        provided_token = credentials.token

        # Validate provided access token via OAuth
        ...

    def get(self) -> list[Response | Effect]:
        ...
```

##### API key

For API key authentication, use `APIKeyCredentials`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        provided_api_key = credentials.key

        # Validate provided key against an API key in self.secrets
        ...

    def get(self) -> list[Response | Effect]:
        ...
```

##### Custom

It's also possible to create custom authentication schemes. There are two ways to do this.

The first way is to access authentication headers on the request object directly. If you wish to do
this, then you would define your authenticate method to take a `Credentials` object, and pull the
authentication values from the request headers:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import Credentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: Credentials) -> bool:
        provided_api_key = self.request.headers["My-API-Key"]
        provided_app_key = self.request.headers["My-App-Key"]

        # Validate provided credentials against the credentials in self.secrets
        ...

    def get(self) -> list[Response | Effect]:
        ...
```

Another way to do this is by defining your own `Credentials` subclass which obtains the
authentication values out of the request headers:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import Credentials, SimpleAPIRoute


class MyCredentials(Credentials):
    def __init__(self, request: Request) -> None:
        self.api_key = self.request.headers['My-API-Key']
        self.app_key = self.request.headers['My-App-Key']


class MyAPI(SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def authenticate(self, credentials: MyCredentials) -> bool:
        provided_api_key = credentials.api_key
        provided_app_key = credentials.app_key

        # Validate provided credentials against the credentials in self.secrets
        ...

    def get(self) -> list[Response | Effect]:
        ...
```

#### Authentication mixins

The Canvas SDK offers several "batteries included" authentication mixins that you can use to implement your authentication method. If you choose to use these, then the only action you must take is to ensure that you set the appropriate secrets on your instance.

Make sure you always list the mixin class to the left of the base class, which is **SimpleAPIRoute** in the examples below.

##### Basic

If you want an implementation of Basic authentication, you can use the `BasicAuthMixin`. You will need to set the `simpleapi-basic-username` and `simpleapi-basic-password` secrets on your instance.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import BasicAuthMixin, SimpleAPIRoute


class MyAPI(BasicAuthMixin, SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```

##### API key

If you want an implementation of API key authentication, you can use the `APIKeyAuthMixin`.

You will need to set the API key secret on your instance. You can generate a secure, random API key
like this:

```shell
python -c "import secrets; print(secrets.token_hex(16))"
```

Copy the output from that command, and set the `simpleapi-api-key` secret on your instance.

After you set your secret, you can use the `APIKeyAuthMixin`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPIRoute


class MyAPI(APIKeyAuthMixin, SimpleAPIRoute):
    PATH = "/my-api/hello-world"

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```
