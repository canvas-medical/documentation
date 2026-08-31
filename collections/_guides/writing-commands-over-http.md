---
title: "Writing Commands Over HTTP"
last_modified_at: "2026-08-13"
guide_for:
- /sdk/commands/
- /sdk/handlers-simple-api/
- /sdk/data/
---

Writing to a patient's chart from outside Canvas — from a custom charting surface, a scribe, an intake
form, a back-office tool — used to mean building the API yourself: a
[SimpleAPI](/sdk/handlers-simple-api/) route per command, reading a JSON body, mapping keys onto
command fields, deciding what a bad value returns, building the effect. Every team that needed it
built the same one.

**Canvas has now built it for you.** `CommandAPI` is that endpoint, templated: it reads the body onto
a command, validates it against that command, and emits the effects. All you add is the part that
should be yours — who may call it, and what they are allowed to write.

That remainder is most of this guide, because it is the part no template can decide: authentication
tells you *who* is calling, not whether that person may write to *this note*.

## What you'll learn

- How to expose one command as an HTTP endpoint with [`CommandAPI`](/sdk/handlers-simple-api-commands/)
- The request and response shape every operation shares
- How to check that the caller may actually write to *this note*, which authentication alone does
  not tell you
- How to serve every command from a single endpoint

## Your first command endpoint

`CommandAPI` is a `SimpleAPI`, so it brings the request handling. What it will not do is **choose your
authentication**: the schemes ship with the SDK, but which one guards your endpoint is your decision,
not the base's. You declare it alongside a prefix and your routes:

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

    @api.patch("/hpi/<command_id>")
    def update(self) -> list[Response | Effect]:
        return self.edit(HistoryOfPresentIllnessCommand, self.request.path_params["command_id"])

    @api.delete("/hpi/<command_id>")
    def remove(self) -> list[Response | Effect]:
        return self.action(
            HistoryOfPresentIllnessCommand, self.request.path_params["command_id"], "delete"
        )
```

That is the whole endpoint. Posting to it:

```sh
curl -X POST "https://example.canvasmedical.com/plugin-io/api/my_plugin/v1/hpi" \
  -H "Content-Type: application/json" \
  -d '{
        "note_id": "fd05f99a-7abe-4bcd-be94-adf09937af2a",
        "values": {"narrative": "Patient reports a headache for three days."}
      }'
```

```json
{ "command_uuid": "2588aa22-f5b4-4335-b4fe-aea69cdfb3f3", "committed": false }
```

{% include alert.html type="warning" content="A route handler cannot be named `originate`, `edit` or `action` — those are the methods you are calling. Name handlers for the HTTP verb they serve, as above." %}

## The three operations

| Method | Body | Success |
|---|---|---|
| `self.originate(model)` | `note_id` **required**; optional `command_id`, `commit`, `metadata`, `values` | `201` `{"command_uuid", "committed"}` |
| `self.edit(model, command_id)` | optional `metadata`, `values` | `200` `{"command_uuid", "mode": "edit"}` |
| `self.action(model, command_id, action)` | none | `200` `{"command_uuid", "mode": <action>}` |

**`values`** carries the command's own fields, named exactly as the command declares them. Commands
parse leniently, so JSON's strings are fine — a date arrives as `"2026-08-04"`, an enum as its value
(`"mild"`), a number as `"12"` if that is what your caller sends.

**`commit`** decides whether the command is committed or left staged for a human to finish in the
note. It defaults to `false`, which is usually what you want: your endpoint proposes, the provider
completes.

**`command_id`** on originate lets *you* choose the command's id instead of taking the one the
response returns. That is worth doing when the thing you are writing already has an identity on your
side — you can then tell whether it reached the chart by asking for that id, rather than storing a
mapping. It also makes a retry safe: a second post of the same id is refused with a `409` rather
than writing the command twice.

**`metadata`** is a flat `{"key": "value"}` map attached to the command after it is created. The API
stores whatever you send and interprets none of it.

**`action`** names a method on the command class: `delete`, `commit`, `enter_in_error`, and
`review` / `send` on the commands whose classes support them. Some operations only apply to a
command in a particular state:

| Operation | Required state |
|---|---|
| `edit` | staged |
| `delete` | staged |
| `commit` | staged |
| `enter_in_error` | committed |
| `review`, `send` | none — the command decides |

A refusal says which state the command is in and which it needed, so the caller can tell "not yet"
from "not ever":

```json
{
  "error": "a committed command cannot be edited",
  "state": "committed",
  "required_state": "staged",
  "validation_errors": []
}
```

## When something is wrong

Every rejection has the same shape, so a caller can render them uniformly:

```json
{
  "error": "Validation failed",
  "validation_errors": [
    { "field": "values.narrative", "message": "Input should be a valid string" }
  ]
}
```

- **`400`** — the body is not a JSON object, a value is wrong for its field, or the command's own
  rules refuse it. A key under `values` that is not a field on the command is refused too, rather
  than dropped: silently ignoring a typo would write a blank command.
- **`404`** — no command *of this type* has that id. The lookup is scoped by command type, so an id
  belonging to a different command is a miss rather than a cross-type edit.
- **`409`** — the `command_id` you chose already belongs to a command. Nothing is written, so
  posting the same id twice cannot create a second command:

  ```json
  { "error": "a command already has that id", "command_uuid": "2588aa22-…", "validation_errors": [] }
  ```

## Checking that the caller may write to this note

This is the part worth thinking about, because the two questions look alike and are not:

- **Authentication** — *who is calling?* `StaffSessionAuthMixin` answers "a logged-in staff member",
  and nothing more. See [authentication schemes](/sdk/handlers-simple-api/) for the rest.
- **Authorization** — *may this caller do this to this note?* The mixin cannot answer that, because
  it never sees the note.

An endpoint gated only on "is staff" lets any staff member write any command to any note. That may
be exactly right — it is roughly what the chart itself allows — but decide it rather than inherit it.

### Who the caller is

Canvas sets the logged-in user on the request. A client cannot forge it: plugin-io strips these
headers if they arrive from the caller and sets them only from a real session.

```python?partial=true
from canvas_sdk.v1.data.staff import Staff


def caller(self) -> Staff | None:
    """The staff member behind this request, or None when there is no staff session."""
    if self.request.headers.get("canvas-logged-in-user-type") != "Staff":
        return None
    return Staff.objects.filter(id=self.request.headers.get("canvas-logged-in-user-id")).first()
```

### Only the note's author, and only while the note is open

The common rule for a charting surface: the caller must be the note's provider, and the note must
still accept documentation. Check it before you write, and return the refusal yourself:

```python
from http import HTTPStatus

from canvas_sdk.commands import PlanCommand
from canvas_sdk.commands.api import CommandAPI
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import StaffSessionAuthMixin, api
from canvas_sdk.v1.data.note import Note, NoteStateChangeEvent, NoteStates

# The states in which a note still accepts documentation.
OPEN_STATES = (
    NoteStates.NEW,
    NoteStates.PUSHED,
    NoteStates.UNLOCKED,
    NoteStates.RESTORED,
    NoteStates.UNDELETED,
    NoteStates.CONVERTED,
)


class PlanAPI(StaffSessionAuthMixin, CommandAPI):
    PREFIX = "/v1"

    @api.post("/plan")
    def insert(self) -> list[Response | Effect]:
        # A body that will not parse is not authorized against — `originate` refuses it with a
        # 400 of its own, and nothing is written in the meantime.
        try:
            body = self.request.json()
        except ValueError:
            return self.originate(PlanCommand)

        note_id = body.get("note_id", "") if isinstance(body, dict) else ""
        if denial := self.refuse(str(note_id)):
            return [denial]
        return self.originate(PlanCommand)

    def refuse(self, note_id: str) -> JSONResponse | None:
        """A response to send instead of writing, or None when the caller may proceed."""
        # One query for the two scalars the decision needs.
        note = Note.objects.filter(id=note_id).values("dbid", "provider__id").first()
        if note is None:
            return JSONResponse({"error": "unknown note"}, status_code=HTTPStatus.NOT_FOUND)

        staff_id = self.request.headers.get("canvas-logged-in-user-id") or ""
        if not staff_id or str(note["provider__id"]) != staff_id:
            return JSONResponse(
                {"error": "only the note's author can write to it"},
                status_code=HTTPStatus.FORBIDDEN,
            )

        state = (
            NoteStateChangeEvent.objects.filter(note_id=note["dbid"])
            .order_by("created")
            .values_list("state", flat=True)
            .last()
        )
        if state not in OPEN_STATES:
            return JSONResponse(
                {"error": "this note no longer accepts documentation"},
                status_code=HTTPStatus.CONFLICT,
            )

        return None
```

Two things worth copying from that shape. It reads the note **once**, with `.values()`, because the
check runs on every write. And it answers different refusals differently — `404` for a note that is
not there, `403` for the wrong caller, `409` for a closed note — so the caller can tell "you may
not" from "not any more".

{% include alert.html type="warning" content="Do not read `note_id` from the body and then trust a *different* note id further down. The value you authorize against and the value you write to have to be the same one." %}

### Narrowing who reaches the endpoint at all

When the rule is about the person rather than the note, put it in `authenticate` — the request never
reaches your handler:

```python?partial=true
from canvas_sdk.handlers.simple_api import SessionCredentials
from canvas_sdk.v1.data.staff import Staff


def authenticate(self, credentials: SessionCredentials) -> bool:
    """Only active staff who are providers may write commands here."""
    if credentials.logged_in_user["type"] != "Staff":
        return False
    return Staff.objects.filter(
        id=credentials.logged_in_user["id"], active=True, primary_practice_location__isnull=False
    ).exists()
```

Which of the two you use is a real choice. `authenticate` is cheaper and applies to every route, but
it cannot see the note. A per-request check can, and it can explain itself in the response. Rules
about the *caller* belong in the first; rules about the *note* belong in the second.

## Serving every command from one endpoint

Nothing ties an endpoint to a single command — the command is an argument. Put the command in the path
and look it up, and one endpoint serves the lot.

Two things are worth getting right before you write it.

**Key the lookup on each command's own `Meta.key`.** That is the value `CommandAPI` uses when it looks
a command up by id, so deriving the path segment from it keeps the URL and the lookup naming the same
schema. It also saves you transcribing keys that are not guessable from the class name — `hpi`,
`reasonForVisit`, `structuredAssessment`, `chartSectionReview`, `exam`, `ros`.

**Allow actions per command, not from one shared set.** [Not every command accepts every
action](/sdk/effects/#commands): Prescribe and Refill are finished by sending rather than committing,
Lab Order takes `send`, Imaging Order and Refer take `delegate` and `sign`, and Reason for Visit takes
none of them. This matters more than it looks — see the warning below.

```python
from http import HTTPStatus

from canvas_sdk.commands import (
    AllergyCommand,
    AssessCommand,
    DiagnoseCommand,
    HistoryOfPresentIllnessCommand,
    LabOrderCommand,
    PlanCommand,
    PrescribeCommand,
)
from canvas_sdk.commands.api import CommandAPI
from canvas_sdk.commands.base import _BaseCommand
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import StaffSessionAuthMixin, api

# Keyed on Meta.key, so the path segment always matches the schema CommandAPI looks up.
COMMANDS: dict[str, type[_BaseCommand]] = {
    command.Meta.key: command
    for command in (
        AllergyCommand,
        AssessCommand,
        DiagnoseCommand,
        HistoryOfPresentIllnessCommand,
        LabOrderCommand,
        PlanCommand,
        PrescribeCommand,
    )
}

# What each command is actually finished with. Nothing infers this for you.
STAGED_ACTIONS = {"commit", "delete", "enter_in_error"}
ACTIONS: dict[str, set[str]] = {
    AllergyCommand.Meta.key: STAGED_ACTIONS,
    AssessCommand.Meta.key: STAGED_ACTIONS,
    DiagnoseCommand.Meta.key: STAGED_ACTIONS,
    HistoryOfPresentIllnessCommand.Meta.key: STAGED_ACTIONS,
    PlanCommand.Meta.key: STAGED_ACTIONS,
    LabOrderCommand.Meta.key: {"delete", "send", "enter_in_error"},
    PrescribeCommand.Meta.key: {"delete", "review", "send", "enter_in_error"},
}


def unknown_command() -> Response:
    """The one response every route shares, so a bad path reads the same way throughout."""
    return JSONResponse(
        {"error": "no such command", "commands": sorted(COMMANDS)},
        status_code=HTTPStatus.NOT_FOUND,
    )


class ChartingAPI(StaffSessionAuthMixin, CommandAPI):
    PREFIX = "/commands"

    @api.post("/<schema>")
    def create(self) -> list[Response | Effect]:
        command = COMMANDS.get(self.request.path_params["schema"])

        if command is None:
            return [unknown_command()]

        return self.originate(command)

    @api.put("/<schema>/<command_id>")
    def update(self) -> list[Response | Effect]:
        command = COMMANDS.get(self.request.path_params["schema"])

        if command is None:
            return [unknown_command()]

        return self.edit(command, self.request.path_params["command_id"])

    @api.post("/<schema>/<command_id>/<action>")
    def act(self) -> list[Response | Effect]:
        schema = self.request.path_params["schema"]
        command = COMMANDS.get(schema)

        if command is None:
            return [unknown_command()]

        action = self.request.path_params["action"]
        allowed = ACTIONS.get(schema, set())

        if action not in allowed:
            return [
                JSONResponse(
                    {"error": f"{schema} does not accept that action", "allowed": sorted(allowed)},
                    status_code=HTTPStatus.BAD_REQUEST,
                )
            ]

        return self.action(command, self.request.path_params["command_id"], action)
```

That is the whole surface: `POST /commands/hpi` creates, `PUT /commands/hpi/<id>` revises,
`POST /commands/hpi/<id>/commit` finishes. Adding a command is two lines — one in `COMMANDS`, one in
`ACTIONS`.

{% include alert.html type="warning" content="Gating the actions is not defensive tidiness, it is the difference between a write landing and silently not landing. Every command class inherits <code>commit()</code>, so <code>POST /commands/prescribe/&lt;id&gt;/commit</code> would build a valid effect and answer <code>200</code> — and Canvas would then refuse to apply it, because Prescribe has no COMMIT. The caller is told the write succeeded when it did not. An action absent from <code>ACTIONS</code> is refused before any effect is built." %}

Two smaller things the shape buys you:

- **One `404` for an unknown command, everywhere.** `unknown_command()` is a plain function rather
  than a method, because `CommandAPI` reserves `originate`, `edit` and `action`, and SimpleAPI raises
  at class-definition time if a subclass shadows a base method.
- **The `<schema>` segment is also your allow-list.** A command absent from `COMMANDS` is unreachable,
  so adding `CommandAPI` to a plugin does not expose every command in the SDK — only the ones you
  named.

## Where to go next

- [Commands](/sdk/commands/) — every command and its fields
- [Populating Command Fields](/guides/populating-command-fields/) — where a field's *value* comes
  from when there is no autocomplete to pick it for you
- [Commands API](/sdk/handlers-simple-api-commands/) — the reference for `CommandAPI`
- [SimpleAPI](/sdk/handlers-simple-api/) — routing, authentication schemes, and responses
