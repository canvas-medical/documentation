---
title: "Building Custom Plugin UI with Action Buttons and SimpleAPI"
guide_for:
- /sdk/handlers-action-button/
- /sdk/effect-launch-modal/
- /sdk/handlers-simple-api-http/
- /sdk/effects/
---

<!-- sources: discussions #1363, #1503, #610 -->

A common need is to add your own button to the Canvas UI that opens a custom screen — a printable visit summary, a data-entry form, a dashboard — and then act on what the user does there. The building blocks are always the same three pieces:

1. An [`ActionButton`](/sdk/handlers-action-button/) (or [`Application`](/sdk/handlers-application/)) places a button in the UI and, when clicked, returns a [`LaunchModalEffect`](/sdk/effect-launch-modal/).
2. The modal shows HTML/JavaScript, either inlined with `content=` or loaded from a URL served by your own [`SimpleAPI`](/sdk/handlers-simple-api-http/).
3. The `SimpleAPI` endpoint queries data, renders HTML, and/or receives requests from the modal's JavaScript and returns [effects](/sdk/effects/) (such as [commands](/sdk/commands/)) that change the note.

This guide shows two variations of the pattern: a read-only custom print template, and an interactive form that adds a command to a note.

## Two ways to populate the modal

`LaunchModalEffect` accepts either:

- `content=` — an HTML string you render inline. Best for small, self-contained screens.
- `url=` — a path served by your plugin's `SimpleAPI`, in the form `/plugin-io/api/<plugin_name>/...`. Best when you need to query several data models server-side, serve CSS or images as separate files, reuse the endpoint for external integrations (fax, PDF generation), or you would otherwise hit size limits on inline content.

## Pattern 1: A custom printable visit summary

The default "Print note" button gives you no control over layout. By serving your own HTML template from a `SimpleAPI` endpoint, you fully control the printed output. The plugin registers two components: an `ActionButton` in the note header and a `SimpleAPI` that renders the page.

### Manifest

Register both components in `CANVAS_MANIFEST.json`:

```json
{
    "sdk_version": "0.75.0",
    "plugin_version": "1.0.0",
    "name": "patient_visit_summary",
    "components": {
        "protocols": [
            {
                "class": "patient_visit_summary.protocols.patient_visit_summary:CustomHTMLActionButton",
                "description": "Note header button that opens the visit summary."
            },
            {
                "class": "patient_visit_summary.protocols.patient_visit_summary:CustomerHTMLApi",
                "description": "API endpoint serving the visit summary HTML."
            }
        ]
    },
    "secrets": ["simple-api-key"]
}
```

### Action button

The button opens the modal by pointing it at the plugin's own API endpoint:

```python
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.action_button import ActionButton


class CustomHTMLActionButton(ActionButton):
    BUTTON_TITLE = "Patient Visit Summary"
    BUTTON_KEY = "PATIENT_VISIT_SUMMARY"
    BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_HEADER

    def visible(self) -> bool:
        # Add logic here if the button should only show on specific notes.
        return True

    def handle(self):
        return [
            LaunchModalEffect(
                url=f"/plugin-io/api/patient_visit_summary/?patient_id={self.target}&note_id={self.event.context['note_id']}"
            ).apply()
        ]
```

Key details:

- `self.target` gives the patient ID.
- `self.event.context['note_id']` gives the current note.
- The URL pattern `/plugin-io/api/<plugin_name>/` routes to your `SimpleAPI`.

### SimpleAPI that renders the HTML

The endpoint authenticates the caller, queries the data you want on the page, and returns rendered HTML. Authenticating via the session first lets staff click straight through from the Canvas UI; the optional API-key fallback lets you fetch the same page from outside Canvas.

```python
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import HTMLResponse, Response
from canvas_sdk.handlers.simple_api import Credentials, SimpleAPI, api
from canvas_sdk.handlers.simple_api.security import SessionCredentials
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data.note import Note
from canvas_sdk.v1.data.patient import Patient


class CustomerHTMLApi(SimpleAPI):
    def authenticate(self, credentials: Credentials) -> bool:
        # First try session auth (a staff user clicking from the Canvas UI).
        try:
            logged_in_user = SessionCredentials(self.request).logged_in_user
            if logged_in_user["type"] == "Staff":
                return True
        except InvalidCredentialsError:
            pass

        # Fallback to an API key for external access.
        api_key_secret = self.secrets.get("simple-api-key")
        request_auth_key = self.request.headers.get("Authorization")
        if api_key_secret and request_auth_key and api_key_secret.encode() == request_auth_key.encode():
            return True
        return False

    @api.get("/")
    def index(self) -> list[Response | Effect]:
        patient_id = self.request.query_params.get("patient_id")
        note_id = self.request.query_params.get("note_id")

        patient = Patient.objects.get(id=patient_id)
        note = Note.objects.get(dbid=note_id)

        # Fetch any data you want on the page (vitals, assessments, prescriptions, etc.).

        return [
            HTMLResponse(
                render_to_string(
                    "templates/patient_visit_summary.html",
                    context={"patient": patient, "note": note},
                ),
                status_code=HTTPStatus.OK,
            )
        ]

    @api.get("/style.css")
    def get_css(self) -> list[Response | Effect]:
        return [
            Response(
                render_to_string("templates/style.css").encode(),
                status_code=HTTPStatus.OK,
                content_type="text/css",
            )
        ]
```

### HTML template

The template is where you craft your print layout. Reference the CSS through the plugin's own API endpoint and add a print button:

```html
<link rel="stylesheet" type="text/css"
      href="/plugin-io/api/patient_visit_summary/style.css">

<button class="print-button" onclick="window.print()">Print</button>
```

A `@media print` query keeps the page clean when printed — hide the button and control page breaks:

```css
.print-button {
    position: fixed;
    top: 10px;
    right: 10px;
}

@media print {
    body { background-color: white; padding: 0; }
    #container { box-shadow: none; }
    .print-button { display: none; }
    h2 { page-break-after: avoid; }
    .section-container { page-break-inside: avoid; }
}
```

### Recommended structure

A clean layout for this kind of plugin is:

- `protocols/` — the `ActionButton` handler and the `SimpleAPI` handler (in one file, or split across two).
- `templates/` — the Django HTML templates rendered by `render_to_string()`.
- `images/` — logos stored as base64-encoded strings (for example in an `images_b64.py`) and embedded directly into the HTML via template variables, which avoids serving image files separately.

### Flow summary

```
User clicks "Patient Visit Summary" in the note header
  → ActionButton.handle() fires
  → LaunchModalEffect opens /plugin-io/api/patient_visit_summary/?patient_id=X&note_id=Y
  → SimpleAPI authenticates via session cookie (staff user)
  → SimpleAPI queries patient data, commands, vitals, assessments, etc.
  → render_to_string() renders the HTML template with all context
  → HTMLResponse returns the fully rendered page
  → User sees the summary in a modal and clicks "Print" → window.print()
```

## Pattern 2: A form that adds a command to the note

The same architecture works in reverse: instead of only displaying data, the modal's JavaScript can POST back to a `SimpleAPI` endpoint that originates a command on the note. Here the modal content is inlined with `content=` and a `SimpleAPI` route handles the submission.

### Action button rendering an inline form

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.action_button import ActionButton
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data.note import Note


class AddDiagnosisButton(ActionButton):
    """ActionButton in the note header that lets users add diagnoses to the note."""

    BUTTON_TITLE = "Add Diagnosis"
    BUTTON_KEY = "ADD_DIAGNOSIS"
    BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_HEADER

    def handle(self) -> list[Effect]:
        note_dbid = self.context.get("note_id", "")
        note_id = Note.objects.filter(dbid=note_dbid).values_list("id", flat=True).first()
        patient_id = self.context.get("patient", {}).get("id", "")

        context = {
            "note_id": note_id,
            "patient_id": patient_id,
            "api_endpoint": "/plugin-io/api/diagnosis_modal/diagnoses",
        }

        html_content = render_to_string("templates/add_diagnosis.html", context)

        return [
            LaunchModalEffect(
                content=html_content,
                target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
                title="Add Diagnosis",
            ).apply()
        ]
```

### Frontend JavaScript

The template embeds the note ID and API endpoint, captures form input, and calls the endpoint with `fetch()`. Include the session cookie with `credentials: 'include'`:

{% raw %}
```html
<script>
    const noteId = "{{ note_id }}";
    const apiEndpoint = "{{ api_endpoint }}";

    document.getElementById('diagnosisForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            note_id: noteId,
            icd10_code: document.getElementById('icd10Code').value,
            background: document.getElementById('background').value,
            assessment: document.getElementById('assessment').value
        };

        const response = await fetch(apiEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',  // include session cookies
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        // ... handle success/error in the UI
    });
</script>
```
{% endraw %}

### SimpleAPI endpoint that originates a command

Use `StaffSessionAuthMixin` so only logged-in staff can call the endpoint. Parse the request, build the command, and return its `.originate()` effect alongside a JSON response:

```python
from http import HTTPStatus

from canvas_sdk.commands import DiagnoseCommand
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import SimpleAPIRoute, StaffSessionAuthMixin
from logger import log


class AddDiagnosisAPI(StaffSessionAuthMixin, SimpleAPIRoute):
    """Adds a diagnosis command to a note. Only logged-in staff can call it."""

    PATH = "/diagnoses"

    def post(self) -> list[Response | Effect]:
        body = self.request.json()
        note_id = body.get("note_id")
        icd10_code = body.get("icd10_code")
        background = body.get("background", "")
        assessment = body.get("assessment", "")

        diagnose = DiagnoseCommand(
            note_uuid=note_id,
            icd10_code=icd10_code,
            background=background,
            today_assessment=assessment,
        )

        log.info(f"Adding diagnosis {icd10_code} to note {note_id}")

        return [
            diagnose.originate(),
            JSONResponse(
                {
                    "success": True,
                    "message": "Diagnosis added to note",
                    "command_id": diagnose.command_uuid,
                },
                status_code=HTTPStatus.CREATED,
            ),
        ]
```

### Flow summary

```
User clicks "Add Diagnosis" in the note header
  → ActionButton.handle() returns a LaunchModalEffect with HTML/JS (note_id embedded)
  → The modal form captures input and POSTs to the SimpleAPI endpoint
  → AddDiagnosisAPI authenticates (StaffSessionAuthMixin), builds a DiagnoseCommand
  → It calls .originate() and returns a JSON response
  → The diagnosis command appears in the note body
```

## One plugin or several? Grouping components

Both patterns above register more than one component in a single plugin. When deciding whether to ship related components together or split them across plugins, keep these tradeoffs in mind:

- **Deploy and update together.** Components in one plugin are installed, updated, and removed as a unit, so components that depend on one another are guaranteed to be deployed and updated together.
- **They do not crash together.** If a handler errors on installation, only that affected handler fails to load — the others in the plugin still run. (Interdependent components can still misbehave if one is missing, so account for that.)
- **Cache and pub/sub are scoped per plugin.** A plugin can only read and write its own [cache](/sdk/caching/) (keys are namespaced by plugin), and can only publish to its own [pub/sub](/sdk/websockets/) channel (channels are namespaced too). If two components must share cached state or a channel, they need to live in the same plugin.

There are no known performance benefits or penalties to grouping itself.
