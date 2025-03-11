---
title: "SimpleAPI"
slug: "handlers-simpleapi"
excerpt: "Framework for defining HTTP APIs with the Canvas SDK."
---

The Canvas SDK provides a way to define an HTTP API with any number of endpoints in your instance.
Developers can define the routes and implement the code that will handle incoming HTTP requests.

This feature allows developers to create endpoints that can receive webhook events from other
services. An endpoint receiving a request can invoke Effects in a Canvas instance, send another
request to a different service, or simply return a response back to the requester.

## Quickstart

Follow the instructions in
[Your First Plugin](https://docs.canvasmedical.com/guides/your-first-plugin/) to create a plugins
project. For this exercise, use `my_api` as your project (i.e. plugin) name.

Open `CANVAS_MANIFEST.json` in your editor. You can modify filenames, directory structures, and
class names as you see fit in your project, but for this exercise, we are just going to set the
value at `components -> protocols -> 0 -> class` to be `my_api.protocols.my_protocol:MyAPI`.

We're going to need a secret value for authentication. The instructions for declaring secrets is
outlined on the [Your First Plugin](https://docs.canvasmedical.com/guides/your-first-plugin/) page.
Declare a secret in `CANVAS_MANIFEST.json` named `my-api-key`.

Open `my_api/protocols/my_protocol.py` and replace the contents of the file with this code:

```python
from secrets import compare_digest

from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/routes/hello-world"

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

The next step is to deploy your plugin; the instructions for doing so are on the
[Your First Plugin](https://docs.canvasmedical.com/guides/your-first-plugin/) page.

You can see in the code above that the `authenticate` method is going to authenticate using API key
authentication. We've already declared the secret, so now we need to generate a value and set it on
your instance. You can generate an API key like this:

```shell
python -c "import secrets; print(secrets.token_hex(16))"
```

Copy the value that it prints out and set the value for `my-api-key` in your plugin secrets on your
instance.

Now that your plugin is deployed and your secret is set, you can send requests to your endpoint with
`curl`. The `curl` command would look like the following (note that you will need to supply your
instance name and API key):

```shell
curl --location 'https://<instance-name>.canvasmedical.com/plugin-io/api/my_api/routes/hello-world' \
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

The plugin name and the `PATH` value together will form the unique part of the full URL for your
endpoint. The format of the full URL will be:

`https://<instance-name>.canvasmedical.com/plugin-io/api/<plugin-name>/<PATH>`

We can adapt the previous example to add a POST endpoint for the same route on the same handler:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/routes/hello-world"

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

The handler can now respond to both GET and POST requests at `/routes/hello-world`.

### SimpleAPI

For handlers that inherit from **SimpleAPI**, the syntax is a little different. You can include any
number of endpoints in your handler class, and you can name your route handling methods anything you
wish. Here is an example:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPI, api


class MyAPI(SimpleAPI):
    PREFIX = "/routes"

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
the `/routes` portion of the URL path.

### Request objects

When a handler is invoked to handle an incoming HTTP request, the request object is available as an
attribute on the handler. The request method, path, query parameters, content type, and body are all
available as attributes on the request object:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/routes/hello-world"

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

        # Query parameters as a key-value mapping
        query_params = request.query_params

        # Request headers
        headers = request.headers

        # Request body content type
        content_type = request.content_type

        # Raw body
        body = request.body

        # JSON body as a Python dictionary (for requests with application/json content types)
        json_body = request.json()

        # Body as plain text
        text_body = request.text()

        # Body parsed as form data
        form_data = request.form_data()
        
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```

#### Key-value mappings

Attributes on the request object like headers, query parameters, and form data can in most cases be
represented by mappings containing key-value pairs (e.g. Python dictionaries) with a small caveat:
keys are not required to be unique. Because of this, there can be more than one value per key.

These attributes are represented by a data structure that most of the time will behave like a Python
dictionary, unless you want to access the addition values for a key. If you do request the value for
a key using standard dictionary syntax, you will get the first value that was encountered for that
key. If you want the other values, you will need to use different methods to access them.

Here is an example showing how to access the additional values:

```python
# Request sent to /route?value1=a&value1=b&value2=c
query_params = request.query_params

# Get the first value for value1
value1: str = query_params["value1"]

# Get all values for value1 with get_list
value1_all: list[str] = query_params.get_list("value1")

# Iterate over all query parameters (repeating keys if necessary) with multi_items
for key, value in query_params.multi_items():
    log.info(f"key:   {key}")
    log.info(f"value: {value}")
```

#### Forms

If your endpoint is set up to accept `application/x-www-form-urlencoded` or `multipart/form-data`
data, there is method named `form_data` on the request object that will parse the request body. This
method will return a key-value mapping containing `FormPart` objects, each of which represents a
subpart of the form.

Every subpart in a form has a name, and these names are the keys in the mapping that is returned by
the method. A `FormPart` can represent either a simple string value or a file. A `FormPart` that
represents a string will have attributes for `name` and `value`. A `FormPart` that represents a file
will have attributes for `name`, `filename`, `content`, `content_type`.

If the content type of a request is `application/x-www-form-urlencoded`, then all `FormPart` objects
will represent simple string values. If the content type of a request is `multipart/form-data`, then
each `FormPart` object may represent either a simple string value or a file.

Here is an example of how to use the `form_data` method to iterate over the subparts of a request
body with form data:

```python
form_data = request.form_data()

# To iterate over all parts, we have to use the multi_items method because there may be more than
# one part with the same name
for name, part in form_data.multi_items():
    log.info(f"part name:    {name}")

    if part.is_file():
        # It's a file
        log.info(f"content:      {part.content}")
        log.info(f"filename:     {part.filename}")
        log.info(f"content type: {part.content_type}")
    else:
        # It's a simple string
        log.info(f"value:        {part.value")
```

If you know the name of the subparts you are looking for, you can also access the subparts directly
by looking up the name in the mapping returned by `form_data`:

```python
form_data = request.form_data()

# Get the first part named "my-part-name"
part = form_data["my-part-name"]

# Get all parts named "my-part-name"
parts_all = form_data.get_list("my-part-name")
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
    PATH = "/routes/hello-world"

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

Please keep in mind that while setting plugins secrets on your instance is out of scope for this
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
    PATH = "/routes/hello-world"

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
    PATH = "/routes/hello-world"

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
    PATH = "/routes/hello-world"

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
    PATH = "/routes/hello-world"

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
    PATH = "/routes/hello-world"

    def authenticate(self, credentials: MyCredentials) -> bool:
        provided_api_key = credentials.api_key
        provided_app_key = credentials.app_key

        # Validate provided credentials against the credentials in self.secrets
        ...

    def get(self) -> list[Response | Effect]:
        ...
```

#### Authentication mixins

The Canvas SDK offers several "batteries included" authentication mixins that you can use to
implement your authentication method. If you choose to use these, then the only action you must take
is to ensure that you set the appropriate secrets for your plugin on your instance.

Make sure you always list the mixin class to the left of the base class, which is **SimpleAPIRoute**
in the examples below.

##### Basic

If you want an implementation of Basic authentication, you can use the `BasicAuthMixin`. You will
need to declare the `simpleapi-basic-username` and `simpleapi-basic-password` secrets in your
manifest file, and then set the secrets on your instance after you deploy your plugin.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import BasicAuthMixin, SimpleAPIRoute


class MyAPI(BasicAuthMixin, SimpleAPIRoute):
    PATH = "/routes/hello-world"

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```

##### API key

If you want an implementation of API key authentication, you can use the `APIKeyAuthMixin`. You will
need to declare the `simpleapi-api-key` secret in your manifest file, and then set the secret on
your instance after you deploy your plugin.

You can generate a secure, random API key like this:

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
    PATH = "/routes/hello-world"

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```
