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

`CommandAPI` is a `SimpleAPI`, so it brings the request handling. You declare a scheme, a prefix and
your routes — here a staff session guards the endpoint, and one `POST` writes a History of Present
Illness. Which scheme to use is [a decision of its own](#checking-that-the-caller-may-write-to-this-note):

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

Everything `CommandAPI` does is one of three calls, and between them they cover the life of a command:
`originate` puts a new one in a note, `edit` revises it while it is still staged, and `action` runs
whatever finishes it — committing it, sending it, or entering it in error. Each returns the effects and
the response together, so a route handler stays a single `return`.

The body each call accepts, the status it answers with, and every error shape are documented in
[Commands API](/sdk/handlers-simple-api-commands/#methods). What is left to you is a handful of
decisions no reference can make:

**Staged, or committed in the same request.** `originate` leaves the command staged unless you ask
otherwise. Staged is usually right — your endpoint proposes and the provider completes, which is also
how the chart behaves. Commit in the same request when nobody needs to check the entry, such as a
reading from a device, and not when a clinician should see it before it counts. Bear in mind that
[several commands cannot be committed at all](/sdk/effects/#commands) and are finished by sending or
signing instead.

**Whose id the command has.** By default Canvas names it and hands the id back. Pass `command_id` and
you name it, which earns its keep when the thing you are writing already has an identity on your side:
you can ask whether it reached the chart by that id instead of keeping a mapping, and a retry becomes
safe, because posting the same id twice is refused rather than writing a second command. It has to be
a genuine UUID —
[Choosing the command's id](/sdk/handlers-simple-api-commands/#choosing-the-commands-id) covers how to
produce one, including when your own identifier is not a UUID.

**What you want to remember about the entry.** `metadata` attaches a flat map that Canvas stores and
never interprets. Use it for what the entry meant on your side — the submission it came from, the
version of your mapping — so that months later a chart entry can be traced back to its origin.

**How much a caller learns from a rejection.** Every refusal has the same shape, and every field at
fault is reported at once rather than one per round trip. Build against that and a form can mark all
its bad fields from a single response, rather than walking its user through them one at a time.

## Checking that the caller may write to this note

This is the part worth thinking about, because three questions look alike and are not:

- **Authentication** — *who is calling?* `CommandAPI` does not pick this for you, but the schemes are
  provided: `StaffSessionAuthMixin`, `PatientSessionAuthMixin`, `APIKeyAuthMixin` and
  `BasicAuthMixin`, each declared by listing it before `CommandAPI` in the bases. Declare none and the
  endpoint refuses every request rather than admitting anyone. `StaffSessionAuthMixin` answers "a
  logged-in staff member", and nothing more — see
  [authentication mixins](/sdk/handlers-simple-api-http/#authentication-mixins) for what each needs.
- **Authorization** — *may this caller do this to this note?* The mixin cannot answer that, because
  it never sees the note.
- **Attribution** — *who will the chart say wrote it?* This follows from how the caller authenticated,
  which makes the scheme you pick a clinical decision and not only a security one. A session-backed
  request is attributed to the logged-in user, and so is one carrying an access token from the
  [Authorization Code flow](/api/customer-authentication#authorization-code). A shared secret
  identifies nobody, so `APIKeyAuthMixin` and `BasicAuthMixin` requests are recorded as **Canvas Bot**
  — fine for a device feed, wrong for anything a clinician should be seen to have written. See
  [Acting as a Canvas user](/sdk/handlers-simple-api-http/#acting-as-a-canvas-user).

An endpoint gated only on "is staff" lets any staff member write any command to any note. That may
be exactly right — it is roughly what the chart itself allows — but decide it rather than inherit it.

### Reading who the caller is

Canvas does the identifying; turning it into something you can check is yours.

When a request arrives with a real session behind it, Canvas sets two headers on it —
`canvas-logged-in-user-type` and `canvas-logged-in-user-id`. Neither can be forged: plugin-io strips
both if they arrive from the client and sets them only from a session it has verified itself.

Nothing in the SDK turns them into a record, so write the one line that does. There is no built-in
`caller()` — this is a helper on your own handler:

```python?partial=true
from canvas_sdk.v1.data.staff import Staff


def caller(self) -> Staff | None:
    """The staff member behind this request, or None when there is no staff session."""
    if self.request.headers.get("canvas-logged-in-user-type") != "Staff":
        return None
    return Staff.objects.filter(id=self.request.headers.get("canvas-logged-in-user-id")).first()
```

The header carries the staff **key**, which is what `Staff.id` holds — a 32-character UUID with no
dashes — so it matches on `id` rather than `dbid`.

Whether those headers are there at all depends on the scheme you chose, and so does who the chart
credits for the write:

| Scheme | Identifies a person | The command is attributed to |
|:-------|:--------------------|:-----------------------------|
| `StaffSessionAuthMixin` | yes — a staff member | that staff member |
| `PatientSessionAuthMixin` | yes — a patient | that patient |
| An [Authorization Code](/api/customer-authentication#authorization-code) access token | yes | the staff member who authorized it |
| `APIKeyAuthMixin` | no — a shared key | Canvas Bot |
| `BasicAuthMixin` | no — a shared secret | Canvas Bot |

The bottom two authenticate a *system*, not a person, so there is no logged-in user to read and
nothing for the chart to credit. If your endpoint needs a named clinician on the entry, that rules
them out.

### Only the note's author, and only while the note is open

Canvas already refuses a command bound for a note that has been deleted or cancelled, or that is
signed and no longer writable — `canvas_core` validates the note as the effect is applied, inside the
transaction, so nothing lands.

What it cannot do is tell your caller.

{% include alert.html type="danger" content="Nothing in canvas-plugins reads the note's state, and command effects are applied after your response has already gone back. A closed note therefore answers <code>201</code> with a <code>command_uuid</code> and then writes no command. Checking before you write is the only way the caller ever finds out." %}

The check is also where you add the rule Canvas has no opinion on: any staff member may write to any
note. If your surface is meant for the note's own provider, that is yours to enforce.

So make both decisions before you write, and return the refusal yourself:

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

`OPEN_STATES` is deliberately stricter than Canvas's own rule, which refuses only deleted, cancelled
and signed notes. Listing the states you accept, rather than the ones you reject, means a state added
to Canvas later is refused until you have decided what it should mean for your endpoint.

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
