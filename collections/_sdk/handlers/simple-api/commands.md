---
title: "SimpleAPI Commands"
slug: "handlers-simple-api-commands"
excerpt: "Expose Canvas commands as HTTP endpoints with the Canvas SDK."
---

**Any time you want to write a [command](/sdk/commands/) to a patient's chart over HTTP, this is
already built for you.** `CommandAPI` is a [SimpleAPI](/sdk/handlers-simple-api-http/) that reads a
request body onto a command, validates it against that command, and emits the effects. You declare the
routes and who may reach them; it does the rest.

Reach for it whenever something outside Canvas needs to write to a chart — a patient-facing intake
form, a device reporting readings, an internal tool your staff already work in, or a service that
turns its own records into chart entries. Written by hand, each of those means parsing a body, mapping
it onto a command, deciding how to report every way it can be wrong, and keeping your own record of
which command you wrote. None of that is yours to write anymore.

For a walkthrough — including how to check that the caller may write to a particular note — see
[Writing Commands Over HTTP](/guides/writing-commands-over-http/).

## Quickstart

```python
from canvas_sdk.commands import HistoryOfPresentIllnessCommand
from canvas_sdk.commands.api import CommandAPI
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response
from canvas_sdk.handlers.simple_api import StaffSessionAuthMixin, api


class HistoryOfPresentIllnessAPI(StaffSessionAuthMixin, CommandAPI):
    PREFIX = "/v1"

    @api.post("/hpi")
    def insert(self) -> list[Response | Effect]:
        return self.originate(HistoryOfPresentIllnessCommand)
```

That class is five lines, and both of its base classes are load-bearing.

### What it inherits from SimpleAPI

`CommandAPI` is a full [SimpleAPI](/sdk/handlers-simple-api-http/). The Quickstart shows one shape —
a single `POST` under a `PREFIX` — but that is just this example. Anything you can build with a
SimpleAPI you can build here:

- **As many routes as you like**, declared with `@api.get`, `@api.post`, `@api.put`, `@api.patch` and
  `@api.delete`. `PREFIX` is optional and prefixes them all.
- **Path parameters.** A segment written `<name>` in a route path is a placeholder — `@api.put("/hpi/<command_id>")`
  matches a request to `/hpi/2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10`, and what it matched is available as
  `self.request.path_params["command_id"]`. That is how the routes below say *which* command to edit or
  act on: the id comes from the URL rather than the body. A value is always a string, is never empty,
  and covers one path segment only — it cannot contain a `/`.
- **The whole request.** `self.request` carries the method, path, headers, query parameters, the raw
  body, parsed JSON, text, and `multipart/form-data` parts including file uploads.
- **Any response you want to send.** A handler always returns the ordinary SimpleAPI list of
  responses and effects. `originate`, `edit` and `action` each return that list already built — which
  is why the handlers here read `return self.originate(...)` with no brackets of their own. When you
  want your own response, you build the list yourself, as the `act` route does below with
  `[JSONResponse(...)]`, or splice onto theirs: `return [*self.originate(...), my_effect]`.
- **Authentication.** You decide which method to use — see [Authentication](/sdk/handlers-simple-api-http/#authentication) for the schemes available.

One difference worth knowing: `CommandAPI` extends `SimpleAPI`, not
[`SimpleAPIRoute`](/sdk/handlers-simple-api-http/#simpleapiroute). A class declares `PREFIX` and
decorated route handlers rather than a single `PATH` with `get` and `post` methods.

What `CommandAPI` adds on top is the three methods below — `originate`, `edit` and `action` — and
nothing else. Those three names are reserved: a route handler may not reuse one, and SimpleAPI raises
at class-definition time if you try.

### Where authentication comes from

`CommandAPI` brings **no authentication of its own** — who may write commands is your plugin's
decision. Authentication comes from a mixin you list *before* it in the bases, and the SDK ships four
to choose from: `StaffSessionAuthMixin`, `PatientSessionAuthMixin`, `APIKeyAuthMixin` and
`BasicAuthMixin`. See [Authentication mixins](/sdk/handlers-simple-api-http/#authentication-mixins)
for what each one needs. You can also skip the mixins and write `authenticate` yourself.

**The order of the base classes matters, and getting it wrong fails quietly.** SimpleAPI's own
`authenticate` returns `False`, so whichever class Python reaches first decides:

| Base classes | Result |
|:-------------|:-------|
| `(StaffSessionAuthMixin, CommandAPI)` | The mixin answers first. Authentication works as you expect. |
| `(CommandAPI, StaffSessionAuthMixin)` | SimpleAPI answers first, and it refuses everything. **Every request is rejected**, with no error to tell you why. |

{% include alert.html type="warning" content="An authentication mixin establishes <em>who</em> the caller is, not <em>what</em> they may write. <code>StaffSessionAuthMixin</code> only checks that the session belongs to a staff member — it does not consider roles, and it says nothing about whether that person may write to the note in the request body. For that check, see <a href='/guides/writing-commands-over-http/'>Writing Commands Over HTTP</a>." %}

## A complete endpoint

The Quickstart creates a command. Most endpoints also need to change one afterwards, which means three
routes — create, update, and apply an action such as committing it. All three live on one class, and
each is a single call:

```python
from http import HTTPStatus

from canvas_sdk.commands import HistoryOfPresentIllnessCommand
from canvas_sdk.commands.api import CommandAPI
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import StaffSessionAuthMixin, api

# The actions this endpoint will pass on. Checked against the request so a caller
# cannot name an arbitrary attribute of the command class.
ALLOWED_ACTIONS = {"commit", "delete", "enter_in_error"}


class HistoryOfPresentIllnessAPI(StaffSessionAuthMixin, CommandAPI):
    PREFIX = "/v1"

    @api.post("/hpi")
    def create(self) -> list[Response | Effect]:
        return self.originate(HistoryOfPresentIllnessCommand)

    @api.put("/hpi/<command_id>")
    def update(self) -> list[Response | Effect]:
        return self.edit(HistoryOfPresentIllnessCommand, self.request.path_params["command_id"])

    @api.post("/hpi/<command_id>/<action>")
    def act(self) -> list[Response | Effect]:
        action = self.request.path_params["action"]

        if action not in ALLOWED_ACTIONS:
            return [
                JSONResponse(
                    {"error": "unsupported action", "allowed": sorted(ALLOWED_ACTIONS)},
                    status_code=HTTPStatus.BAD_REQUEST,
                )
            ]

        return self.action(
            HistoryOfPresentIllnessCommand,
            self.request.path_params["command_id"],
            action,
        )
```

Staging a note entry, committing it, and retracting it, against that endpoint:

```shell
# Create it, staged for a human to finish.
curl -X POST https://example.canvasmedical.com/plugin-io/api/my_plugin/v1/hpi \
  -H 'Content-Type: application/json' \
  -d '{
        "note_id": "d2194110-5c9a-4842-8733-ef09ea5ead11",
        "values": {"narrative": "Patient reports a cough for three days."}
      }'
# 201 {"command_uuid": "2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10", "committed": false}

# Revise it.
curl -X PUT https://example.canvasmedical.com/plugin-io/api/my_plugin/v1/hpi/2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10 \
  -H 'Content-Type: application/json' \
  -d '{"values": {"narrative": "Patient reports a dry cough for three days."}}'
# 200 {"command_uuid": "2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10", "mode": "edit"}

# Commit it.
curl -X POST https://example.canvasmedical.com/plugin-io/api/my_plugin/v1/hpi/2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10/commit
# 200 {"command_uuid": "2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10", "mode": "commit"}

# Retract it. A committed command cannot be edited, so entering it in error is
# how you take it back - then originate its replacement.
curl -X POST https://example.canvasmedical.com/plugin-io/api/my_plugin/v1/hpi/2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10/enter_in_error
# 200 {"command_uuid": "2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10", "mode": "enter_in_error"}
```

The order matters: `enter_in_error` needs a **committed** command, so it only works after the commit
above. Sent against the staged command it would have been refused — see [State](#state).

To serve every command from one endpoint instead of one class per command, see
[Serving every command from one endpoint](/guides/writing-commands-over-http/#serving-every-command-from-one-endpoint) in the guide — the
command is an argument, so a dict of them and a path parameter is all it takes.

## Methods

Each returns the effects and the response for you to return from the route handler. You return the
list as-is; nothing else is required of the handler.

### originate

`originate(model)` creates a command from the request body.

| Body field | Type | Required | Description |
|---|---|---|---|
| `note_id` | _string_ | `true` | The id of the [Note](/sdk/data-note/#note) to write the command into. |
| `values` | _object_ | `false` | The command's own fields, named as the command declares them. See [Commands](/sdk/commands/) for the fields each command takes. |
| `command_id` | _string_ | `false` | An id of your choosing for the new command, instead of the one the response returns. |
| `commit` | _boolean_ | `false` | Commit the command as well as creating it. Defaults to `false`, leaving it staged for a human to finish. |
| `metadata` | _object_ | `false` | A flat `{"key": "value"}` map attached to the command. See [Command metadata](/sdk/effect-command-metadata/). |

Responds `201` with the id of the command it wrote and whether it was committed:

```json
{ "command_uuid": "2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10", "committed": false }
```

A body using every field:

```json
{
  "note_id": "d2194110-5c9a-4842-8733-ef09ea5ead11",
  "command_id": "2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10",
  "commit": true,
  "values": { "narrative": "Patient reports a dry cough for three days." },
  "metadata": { "source": "intake-form", "submission": "8871" }
}
```

If anything is wrong with the request, nothing is written and you get a `400` instead. A value that
the command refuses is reported against the field it came from:

```json
{
  "error": "Validation failed",
  "validation_errors": [
    { "field": "values.narrative", "message": "String should have at most 512 characters" }
  ]
}
```

A problem with the envelope rather than the values reads the same way, without the `values.` prefix —
here a body that left `note_id` out:

```json
{
  "error": "Validation failed",
  "validation_errors": [
    { "field": "note_id", "message": "Field required" }
  ]
}
```

Every field at fault is reported at once, so a caller sees the whole list rather than fixing one
problem per round trip. The other statuses this route can answer with are in
[Responses](#responses).

### edit

`edit(model, command_id)` updates a **staged** command. The command is addressed by id in your route,
and the body carries `values` and `metadata`:

```json
{ "values": { "narrative": "Patient reports a dry cough for three days." } }
```

Responds `200`:

```json
{ "command_uuid": "2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10", "mode": "edit" }
```

{% include alert.html type="warning" content="<code>values</code> replaces the command's fields as a whole and is re-validated in full — it is not a patch. A field you leave out is not left alone; send the complete set of values you want the command to end up with." %}

Three things can go wrong, and each is checked before anything is written.

**The id matches no command of this type** — a `404`:

```json
{ "error": "No hpi command with that id" }
```

**The command is not staged** — a `400` naming the state it is in and the one the operation needed. A
committed command cannot be edited; enter it in error and originate its replacement instead:

```json
{
  "error": "a committed command cannot be edited",
  "state": "committed",
  "required_state": "staged",
  "validation_errors": []
}
```

**A value is wrong for its field** — a `400` in the same shape
[`originate` returns](#originate), reported against `values.<field>`. A body that is not a JSON object
at all is a `400` too, carrying `"Request body must be a JSON object"`.

See [State](#state) for which operations each state allows, and [Responses](#responses) for the full
list of statuses.

### action

`action(model, command_id, action)` runs one of the command's own methods. It takes no request body,
and responds `200` naming what it did:

```json
{ "command_uuid": "2588aa22-9d0e-4f1f-9b28-6f0e6a1c9a10", "mode": "commit" }
```

`action` names a method on the command class. Each one builds the corresponding [command effect](/sdk/effects/#commands), which is also where you can see which commands support which actions:

| Action | What it does | Required state |
|:-------|:-------------|:---------------|
| `commit` | Signs the staged command into the note. | staged |
| `delete` | Removes the staged command from the note. | staged |
| `enter_in_error` | Marks a committed command as entered in error. | committed |
| `review`, `send` | Only on the commands that support them — see [Commands](/sdk/effects/#commands). | none — the command decides |

An action the command class does not have is a `400`:

```json
{ "error": "HistoryOfPresentIllnessCommand does not support the 'review' action", "validation_errors": [] }
```

{% include alert.html type="danger" content="The action usually arrives from the request, and it is passed to <code>getattr</code> on the command. Check it against a set you control first — as <code>ALLOWED_ACTIONS</code> does above — or a caller can name any attribute of the command class." %}

## Field values

`values` carries the command's own fields, named exactly as the command declares them. Each command's
fields are listed under [Commands](/sdk/commands/) — `values` accepts the same set, so that page is
the reference for what may go in here.

Commands parse leniently, so JSON's own types are enough. Posting to an
[Allergy](/sdk/commands/#allergy) endpoint:

```json
{
  "note_id": "d2194110-5c9a-4842-8733-ef09ea5ead11",
  "values": {
    "narrative": "Hives within an hour of eating shellfish.",
    "severity": "mild",
    "approximate_date": "2026-08-04"
  }
}
```

- `narrative` is a plain string, capped at 512 characters by the command.
- `severity` is an enum, given as its value — `"mild"`, not `AllergyCommand.Severity.MILD`.
- `approximate_date` is a date, given as an ISO string.
- A number may arrive as a number or as a string: `12` and `"12"` are both read as `12`.

A key that is not a field on the command is **refused**, not dropped — silently ignoring a typo would
write a blank command over it. Every unknown key is reported at once, against `values.<field>`:

```json
{
  "error": "Validation failed",
  "validation_errors": [
    { "field": "values.narative", "message": "Unexpected field" }
  ]
}
```

`note_id`, `command_id`, `commit` and `metadata` are the envelope, not fields — they sit alongside
`values`, not inside it, and they are kept out of what the command writes.

## Metadata

`metadata` attaches a flat `{"key": "value"}` map to the command. It is stored as sent and nothing in
Canvas interprets it, which makes it the place to record what the entry meant on your side:

```json
{
  "note_id": "d2194110-5c9a-4842-8733-ef09ea5ead11",
  "values": { "narrative": "Patient reports a dry cough for three days." },
  "metadata": { "source": "intake-form", "submission": "8871", "version": "2" }
}
```

Both `originate` and `edit` accept it. Values must be strings — send `"8871"`, not `8871`.

## Responses

| Status | When |
|---|---|
| `201` | The command was created. |
| `200` | An edit or an action was applied. |
| `400` | The body is not a JSON object, a value is wrong for its field, or the command's state does not allow the operation. |
| `404` | No command **of this type** has that id. The lookup is scoped by command type, so an id belonging to a different command is a miss rather than a cross-type edit. |
| `409` | The `command_id` you chose already belongs to a command. |

**Every rejection has the same shape** — an `error` summarising it and a `validation_errors` list,
empty when nothing field-specific was at fault. A caller can render all of them the same way.

A value that is wrong for its field:

```json
{
  "error": "Validation failed",
  "validation_errors": [
    { "field": "values.narrative", "message": "Input should be a valid string" }
  ]
}
```

A body that is not a JSON object at all:

```json
{ "error": "Request body must be a JSON object", "validation_errors": [] }
```

An id matching no command of this endpoint's type:

```json
{ "error": "No hpi command with that id" }
```

That `404` covers three cases at once, deliberately: no command has the id, a command has it but is of
a different type, or the id is not a well-formed UUID. The lookup is scoped to the command type this
endpoint serves, so an id belonging to a Plan command reaching a History of Present Illness endpoint is
a miss rather than a cross-type edit.

### Choosing the command's id

Passing `command_id` is worth doing when the thing you are writing already has an identity on your
side: you can then ask whether it reached the chart by that id rather than storing a mapping. Posting
the same id twice answers `409` rather than writing a second command, which makes a retry safe:

```json
{ "error": "a command already has that id", "command_uuid": "2588aa22-…", "validation_errors": [] }
```

### State

Some operations only apply to a command in a particular state.

| Operation | Required state |
|---|---|
| `edit` | staged |
| `delete` | staged |
| `commit` | staged |
| `enter_in_error` | committed |
| `review`, `send` | none — the command decides |

A refusal says which state the command is in and which it needed:

```json
{
  "error": "a committed command cannot be edited",
  "state": "committed",
  "required_state": "staged",
  "validation_errors": []
}
```

## Naming route handlers

A route handler cannot be called `originate`, `edit` or `action` — those are the methods you are
calling. Name handlers for the HTTP verb they serve.
