---
title: "SimpleAPI HTTP"
slug: "handlers-simple-api-http"
excerpt: "Framework for defining HTTP APIs with the Canvas SDK."
---

The Canvas SDK provides a way to define an HTTP API with any number of endpoints in your instance.
Developers can define the routes and implement the code that will handle incoming HTTP requests.

This feature allows developers to create endpoints that can receive webhook events from other
services. An endpoint receiving a request can invoke Effects in a Canvas instance, send another
request to a different service, or simply return a response back to the requester.

## Quickstart

Follow the instructions in
[Your First Plugin (with Claude Code)](https://docs.canvasmedical.com/guides/your-first-plugin-with-claude-code/) to create a plugins
project. For this exercise, use `my_api` as your project (i.e. plugin) name.

Open `CANVAS_MANIFEST.json` in your editor. You can modify filenames, directory structures, and
class names as you see fit in your project, but for this exercise, we are just going to set the
value at `components -> handlers -> 0 -> class` to be `my_api.handlers.my_handler:MyAPI`.

We're going to need a secret value for authentication. The instructions for declaring secrets are
outlined on the [Your First Plugin (Manual)](https://docs.canvasmedical.com/guides/your-first-plugin/) page.
Declare a secret in `CANVAS_MANIFEST.json` named `my-api-key`.

Open `my_api/handlers/my_handler.py` and replace the contents of the file with this code:

```python
from hmac import compare_digest

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
[Your First Plugin (Manual)](https://docs.canvasmedical.com/guides/your-first-plugin/) page.

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

### Path patterns

If you want to set up an endpoint that will respond to requests where the path matches a pattern
rather than an exact string, you can use a path pattern. This is common in cases where the path of
an endpoint contains a resource identifier.

You can specify a path pattern by by denoting any number of the path parameters in the path using
`<>` syntax, with the name of the path parameters in between the angle brackets. Path parameter
names must be be unique within the path. They can also be specified in the path prefix (for
**SimpleAPI** handlers).

Path parameters will be extracted from the path and will be available on the
[request object](#request-objects) in the `path_params` attribute.

In the example below, the value `id` is specified as part of the path, and can be accessed by the
handler:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/routes/hello-world/<id>"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        ...

    def get(self) -> list[Response | Effect]:
        id_ = self.request.path_params["id"]

        return [
            JSONResponse(
                {
                    "message": "Hello world from my GET endpoint!",
                    "id": id_
                }
            )
        ]
```

#### Path matching

When you specify routes using path patterns, it is possible that multiple endpoints may match with a
request. This has a few implications that need to be considered, because only one endpoint can
provide a response.

If the endpoints that match are all part of the same handler class, then the request will be handled
by the endpoint that appears highest up in the class definition, i.e. the one that is defined first.
Consider two endpoints specified to match the following patterns:

```generic
/routes/hello-world/current-user
/routes/hello-world/<id>
```

The first uses an exact match, and the second uses a pattern. The path
`/routes/hello-world/current-user` matches both of those patterns. However, if you register the
second endpoint first it would never be possible for a request with the path of
`/routes/hello-world/current-user` to match with the endpoint for
`/routes/hello-world/current-user`. If you need to define endpoints that use exact matching that may
overlap with endpoints defined with path patterns, order must be carefully considered.

If, however, you have defined multiple **SimpleAPIRoute** or **SimpleAPI** handlers, and a request
matches with multiple endpoints across these handlers, an error condition will result. There is not
a way to specify priority across handlers, so if you need fine-grained control over request routing
for endpoints that use path patterns, make sure they are contained within the same handler class.

### Request objects

When a handler is invoked to handle an incoming HTTP request, the request object is available as an
attribute on the handler. The request method, path, query parameters, content type, and body are all
available as attributes on the request object:

```python

from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute

from logger import log


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
dictionary, unless you want to access the additional values for a key. If you do request the value for
a key using standard dictionary syntax, you will get the first value that was encountered for that
key. If you want the other values, you will need to use different methods to access them.

Here is an example showing how to access the additional values:

```python?partial=true
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

```python?partial=true
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
        log.info(f"value:        {part.value}")
```

If you know the name of the subparts you are looking for, you can also access the subparts directly
by looking up the name in the mapping returned by `form_data`:

```python?partial=true
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
                "Hello world from my PUT endpoint!",
                status_code=HTTPStatus.ACCEPTED,
                headers={"My-Header", "my header value"}
            )
        ]

    def patch(self) -> list[Response | Effect]:
        return [
            Response(
                b'{"message": "Hello world from my PATCH endpoint!"}',
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

### Asynchronous requests

By default, **SimpleAPI** requests are processed synchronously—the caller waits for the plugin to
finish executing before receiving a response. If you prefer an immediate acknowledgement instead,
include the `Prefer: respond-async` header in your request:

```bash
curl --location 'https://<instance-name>.canvasmedical.com/plugin-io/api/<plugin-name>/<route>' \
     --header 'Authorization: <api-key>' \
     --header 'Prefer: respond-async'
```

When this header is present, Canvas will return a **202 Accepted** response right away and continue
executing the plugin in the background. Any effects returned by the handler will still be processed
by your Canvas instance; however, no response body from the handler will be delivered to the caller.

Note that authentication failures and plugin-not-found errors are always returned synchronously,
regardless of this header.

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

##### Session

To authenticate using a logged-in user's session, use `SessionCredentials`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import SessionCredentials, SimpleAPIRoute


class MyAPI(SimpleAPIRoute):
    PATH = "/routes/hello-world"

    def authenticate(self, credentials: SessionCredentials) -> bool:
        logged_in_user = credentials.logged_in_user

        # Structure looks like:
        # {
        #     "id": "abc123",
        #     "type": "Staff"
        # }
        # Where "type" is "Staff" or "Patient"
        # You could authenticate based on type or check to see if the
        # individual is in a particular group or team.
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
from canvas_sdk.handlers.simple_api.api import Request


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
from canvas_sdk.effects.simple_api import JSONResponse, Response
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
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPIRoute


class MyAPI(APIKeyAuthMixin, SimpleAPIRoute):
    PATH = "/routes/hello-world"

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```

##### Staff Session

If you want to ensure the visiting user is a logged in staff user, you can use
the `StaffSessionAuthMixin`. This makes no assertions about the particular
staff member, just that they are staff, and that they are logged in.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import StaffSessionAuthMixin, SimpleAPIRoute


class MyAPI(StaffSessionAuthMixin, SimpleAPIRoute):
    PATH = "/routes/hello-world"

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```

##### Patient Session

If you want to ensure the visiting user is a logged in patient user, you can use
the `PatientSessionAuthMixin`. This makes no assertions about the particular
patient, just that they are a patient, and that they are logged in.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import PatientSessionAuthMixin, SimpleAPIRoute


class MyAPI(PatientSessionAuthMixin, SimpleAPIRoute):
    PATH = "/routes/hello-world"

    def get(self) -> list[Response | Effect]:
        return [
            JSONResponse({"message": "Hello world!"})
        ]
```

## Acting as a Canvas user

By default, a SimpleAPI request isn't tied to a specific person, so any effects it
returns — such as creating, locking, or signing a note — are recorded as Canvas Bot
rather than a clinician.

To have a request run **as a specific Canvas staff member** — for example, so a note
is signed under the treating provider's name — call the endpoint with an access token
obtained through the
[Authorization Code flow](/api/customer-authentication#authorization-code). That flow
issues a token that represents the staff member who signed in and approved it. Send it
as a Bearer token in the `Authorization` header, and Canvas identifies the user from
the token and treats the request as coming from them, so any effects the handler
returns are attributed to that staff member.

```bash
curl --request POST \
  --url 'https://example.canvasmedical.com/plugin-io/api/my_plugin/note/<note-id>/sign' \
  --header 'Authorization: Bearer <access-token>'
```

In this example the note is signed and recorded in Canvas as signed by the staff
member who authorized the access token, not by Canvas Bot.

## Common use cases

SimpleAPI is the supported way to react to external (non-Canvas) events and to
expose functionality that the FHIR API does not cover. A few recurring patterns:

<!-- source: discussion #536 -->
### Reacting to external events

Effects such as Protocol Cards can normally only be created in response to
internal Canvas events. To create one from an outside trigger, expose a
SimpleAPI endpoint that accepts the external request and returns the
corresponding effect. This makes SimpleAPI the supported entry point for any
workflow that needs to be initiated from outside of Canvas.

<!-- source: discussion #1164 -->
### Originating commands that have no FHIR resource

There are no FHIR API endpoints for HPI, Assessment, Plan, or Reason for Visit —
these levels of granularity have no standard FHIR resource, and a custom FHIR
extension would defeat the purpose of the standard. Instead, expose a SimpleAPI
endpoint and originate the corresponding commands from your handler using the
classes in the [command module](/sdk/commands/). You may also use
`Command.objects` from the data module to check for uniqueness or to edit
existing commands. This SDK-based approach gives you maximal control and
correctness.

<!-- source: discussion #708 -->
### Calling SimpleAPI from an external application

External applications (for example a Node.js service) integrate with Canvas by
making POST/GET calls to the SimpleAPI endpoints you define in your plugin,
which in turn trigger effects. Note that not every workflow has a dedicated
effect — there is, for example, an effect for creating a [note](/sdk/effect-notes/),
but Care Plan and Next Steps creation may not be directly supported. Task and
Protocol Card creation are available and can often accomplish the same goal.

<!-- source: discussion #735 -->
### Creating or updating patients from a third-party webhook

To process a third-party webhook (for example a form-submission webhook), point
the webhook at a SimpleAPI `POST` endpoint rather than at the FHIR API. This is
the recommended approach when you need to set custom patient metadata, which is
not settable via FHIR. In your handler:

1. Construct a [Patient effect](/sdk/effect-patient/) from the request body.
2. Listen for the resulting [`PatientCreated` or `PatientUpdated` event](/sdk/events/#patients)
   to obtain the new patient's ID.
3. Call a [Patient Metadata effect](/sdk/effect-patient-metadata/) to set your
   custom metadata.

To carry the metadata across from the POST request to the event handler, use the
[cache](/sdk/caching/): set the value when handling the POST and retrieve it when
the event fires.

<!-- source: discussion #1242 -->
### Serving plugin frontends without leaking secrets

If your plugin serves an HTML/JS UI (for example a vitals chart), do **not**
embed secrets or credentials in client-side JavaScript to call third-party APIs
directly. Instead, have your JavaScript call a SimpleAPI endpoint provided by the
same plugin and protected with the [staff session authentication mixin](#staff-session).
The plugin's Python code holds the secrets and makes the authenticated outbound
request. This works as long as the HTML/JS is served from the plugin. See the
[vitals visualizer example plugin](/sdk/example-vitals_visualizer_plugin/#vitals_visualizationhtml)
for a working implementation.

<!-- source: discussion #1547 -->
### Grouping custom patient metadata fields

A flat list of `PatientMetadataCreateFormEffect` fields cannot be divided into
sections or headers. To present custom-grouped metadata UIs, build an
[Application](/sdk/handlers-applications/) with the
[`full_chart` scope](/sdk/handlers-applications/#full-chart-scope) — it appears
as a tab alongside Chart and Profile. Build your own HTML forms, group them as
you like, and write the values back as `PatientMetadata` through a SimpleAPI
endpoint so they are stored the same way in the backend.

## Building custom UIs

<!-- source: discussion #1408 -->
The recommended way to build a custom-styled UI — for either the provider UI or
the patient portal — is to use `LaunchModalEffect` within a plugin. These are
surfaced as either [action buttons](/sdk/handlers-action-buttons/) or
[applications](/sdk/handlers-applications/). A `LaunchModalEffect` can be passed a
URL, HTML directly, or be paired with a SimpleAPI request to back a custom
frontend. For applications, the `scope` in `CANVAS_MANIFEST.json` controls where
the app appears:

- `global` — appears across all contexts in the provider UI except the patient chart.
- `patient_specific` — appears only on the patient chart page in the provider UI.
- `provider_menu_item` — appears in the provider UI hamburger menu.
- `portal_menu_item` — appears in the patient portal sidebar.

<!-- source: discussion #1204 -->
> **Note:** Patient portal application URLs use the base64-encoded app identifier
> (for example `.../app/application/cGF0aWVudF9wb3J0YWxfY29uc2VudF9mb3Jtcy4uLg==`,
> which decodes to `plugin_name.module.path:ClassName`). The browser address bar
> does not change as the user navigates between apps. Because the identifier is
> the plugin name, module path, and class name, renaming any of those files or
> classes invalidates the link. If you need a direct, stable link, consider a URL
> shortener and update it when those names change.

<!-- source: discussion #556 -->
> **Note:** Today all installed applications are visible to all users. Per-user
> visibility control exists for [action buttons](/sdk/handlers-action-buttons/#optional-implement-the-visible-method)
> via the `visible()` method, but not yet for applications.

<!-- source: discussion #1310 -->
> **Note:** There is no way to add a custom button to the panel-button list at
> the top of the patient profile. You can only [reorder the existing panel buttons](/guides/customize-panel-buttons/).
> The equivalent UX is a custom [Application](/sdk/handlers-applications/), which
> is accessed from that same panel-button list.

<!-- source: discussion #1411 -->
> **Note:** Custom visual indicators on calendar/schedule appointments are not
> currently supported. As a workaround, a `global`-scope Application can be shown
> as a right-hand modal side by side with the schedule view to display
> appointment groups, labels, tables, or links into the chart.

<!-- source: discussion #1429 -->
> **Note:** Action buttons do not currently show a loading or spinner state while
> processing. For actions that take a few seconds (for example committing all
> commands in a note), the button gives no visual feedback that work is in
> progress, so users may click it repeatedly.

<!-- source: discussion #1724 -->
## Iframe sandbox and top-frame navigation

There is no environment-specific iframe sandbox configuration in Canvas — dev and
prod run identical code paths. Whether the application iframe gets a `sandbox`
attribute is decided by matching the loaded URL against your manifest's
`url_permissions` entries:

- Matching is a **case-insensitive prefix match** of the loaded URL against each
  `url_permissions[].url`. Every character counts, including scheme, port, and
  trailing slash. The most common silent mismatch is a trailing-slash difference
  (`https://example.com/` will not match a runtime URL of `https://example.com`).
- If a matching entry grants `ALLOW_SAME_ORIGIN`, the iframe is rendered as
  `sandbox="allow-same-origin allow-forms allow-popups allow-scripts"`. This does
  **not** include `allow-top-navigation` or `allow-top-navigation-by-user-activation`,
  so navigating the top frame from inside the iframe is blocked.
- If no entry matches, no `sandbox` attribute is rendered and top-frame
  navigation works normally.

If you see top-navigation work in one environment but not another, the URLs are
matching `url_permissions` differently between them (usually a character-level
difference such as a missing trailing slash). To navigate while keeping
`ALLOW_SAME_ORIGIN`, use `window.open(url, '_blank')` — the sandbox already
includes `allow-popups`. Alternatively, remove `ALLOW_SAME_ORIGIN` from the
manifest entry if your app does not need same-origin access from inside the
iframe.

## Troubleshooting

<!-- source: discussion #858 -->
### A SimpleAPI endpoint returns 404

A 404 from an endpoint you believe is deployed usually means the plugin failed to
load at reload time even though the deploy appeared to succeed — a runtime error
when the plugins reload on the server. Keep two shells open: deploy in one and run
`canvas logs` in the other to catch the load failure (and the line number) as it
happens. Note also that the **plugin name cannot contain a hyphen** (`-`); use
underscores in both the plugin name and the class path, or routing will 404.

<!-- source: discussion #551 -->
### 503 responses when originating many commands

If you receive intermittent **503 No server is available** responses while issuing
many command requests, have your client retry with
[exponential backoff](https://en.wikipedia.org/wiki/Exponential_backoff#Rate_limiting).
To reduce the number of round trips, expose a SimpleAPI endpoint that batches
originate-and-commit in a single call. Normally a command's UUID is generated for
you on originate, but to commit in the same call you must self-assign it first so
both operations reference the same command:

```python
import uuid

command = PlanCommand()
command.command_uuid = str(uuid.uuid4())

return [command.originate(), command.commit()]
```

<!-- source: discussion #498 -->
### Action button "commit all commands" payload key

In a commit-all-commands action button, the effect payload key must be `command`,
not `command_uuid`:

```python
payload=json.dumps({"command": str(command.id)}),
```

Only commands enabled on your instance (non-beta) appear in a note and are
therefore available to commit. Some commands are still in
[beta](/product-updates/commands-module/); support can confirm which are enabled
or turn beta commands on. In the UI, an enabled command shows the three-dot action
menu before it is committed.

<!-- source: discussion #458 -->
### `note_id` in action button context is a numeric dbid

The `note_id` provided in an action button's event context is a numeric database
ID, not a UUID. Look the note up with `Note.objects.get(dbid=note_id)` — using
`get(id=...)` will raise `Note matching query does not exist`.

## Plugin sandbox

Plugin code runs in a `RestrictedPython` sandbox with an allowlist of imports and
language features.

<!-- source: discussion #844 -->
- `match` statements are now allowed in plugin code (they were previously blocked
  with a `Match statements are not allowed` error).

<!-- source: discussion #796 -->
- The `cryptography` package is available, so the `jwt` package can sign tokens
  using RS256. This is required to sign JWTs for external APIs that mandate RS256
  (for example, Google APIs).
