---
title: "SimpleAPI Commands"
slug: "handlers-simple-api-commands"
excerpt: "Expose Canvas commands as HTTP endpoints with the Canvas SDK."
---

`CommandAPI` is a [SimpleAPI](/sdk/handlers-simple-api-http/) that reads a request body onto a
[command](/sdk/commands/), validates it against that command, and emits the effects. You declare the
routes and who may reach them; it does the rest.

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

`CommandAPI` is a [SimpleAPI](/sdk/handlers-simple-api-http/), so everything you already know about
SimpleAPI applies unchanged: `PREFIX` prefixes every route on the class, `@api.post` and its siblings
declare the routes, `self.request` is the incoming request, and a handler returns a list of responses
and effects.

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

## Methods

Each returns the effects and the response for you to return from the route handler.

### originate

`originate(model)` creates a command from the request body.

| Body field | Type | Required | Description |
|---|---|---|---|
| `note_id` | _string_ | `true` | The [Note](/sdk/data-note/#note) to write the command into. |
| `values` | _object_ | `false` | The command's own fields, named as the command declares them. |
| `command_id` | _string_ | `false` | An id of your choosing for the new command, instead of the one the response returns. |
| `commit` | _boolean_ | `false` | Commit the command as well as creating it. Defaults to `false`, leaving it staged for a human to finish. |
| `metadata` | _object_ | `false` | A flat `{"key": "value"}` map attached to the command. Stored as sent; nothing interprets it. |

Responds `201` with `{"command_uuid": ..., "committed": ...}`.

### edit

`edit(model, command_id)` updates a **staged** command. Takes `values` and `metadata`; responds
`200` with `{"command_uuid": ..., "mode": "edit"}`.

### action

`action(model, command_id, action)` runs one of the command's own methods. Takes no body; responds
`200` with `{"command_uuid": ..., "mode": <action>}`.

`action` names a method on the command class — `delete`, `commit`, `enter_in_error`, and
`review` / `send` on the commands that support them. Because it usually arrives from the request,
check it against a set you control before passing it on; otherwise a caller can name any attribute
of the command.

## Field values

`values` carries the command's own fields. Commands parse leniently, so JSON's strings are fine: a
date arrives as `"2026-08-04"`, an enum as its value (`"mild"`), a number as `"12"`.

A key that is not a field on the command is **refused**, not dropped — silently ignoring a typo
would write a blank command.

## Responses

| Status | When |
|---|---|
| `201` | The command was created. |
| `200` | An edit or an action was applied. |
| `400` | The body is not a JSON object, a value is wrong for its field, or the command's state does not allow the operation. |
| `404` | No command **of this type** has that id. The lookup is scoped by command type, so an id belonging to a different command is a miss rather than a cross-type edit. |
| `409` | The `command_id` you chose already belongs to a command. |

A refused value is reported per field, so a caller can render the errors uniformly:

```json
{
  "error": "Validation failed",
  "validation_errors": [
    { "field": "values.narrative", "message": "Input should be a valid string" }
  ]
}
```

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
