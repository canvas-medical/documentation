---
title: "Your First Plugin"
guide_for:
- /sdk/quickstart/
- /sdk/canvas_cli/
- /sdk/events/
- /sdk/effects/
---

Plugins are your tool for customizing the Canvas experience. By using the
modules of the Canvas SDK, you can react to [events](/sdk/events/) emitted from the EHR,
request additional [data](/sdk/data/) if needed, and respond with [effects](/sdk/effects/) that alter workflows and add or change data in Canvas. You can also use [utils](/sdk/utils/) to do things like call out to web services with our provided HTTP client.

## Video

The video below showcases a Canvas engineer working through this guide
step-by-step.

<iframe width="560" height="315"
src="https://www.youtube.com/embed/X2JOEElq2ck?si=V6oA6eolpyq_kYGE&amp;controls=0"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## 1. Install the Canvas CLI

To install the Canvas CLI, simply `pip install canvas`. Python 3.11 or 3.12 is required. You can find
additional detail on the features of the Canvas CLI [here](/sdk/canvas_cli/).

## 2. Configure the Canvas CLI for your instances

The Canvas CLI uses OAuth credentials to connect to your Canvas instance. If
you've used our FHIR API, you'll be very familiar with the process for
[registering credentials](/api/customer-authentication/). Register a separate
OAuth application, choosing `confidential` for the Client type, and `client-credentials`
for the Authorization grant type. Redirect URIs can be left blank, and the
Algorithm should be `No OIDC support`. Note the client_id and client_secret
for the next step.

Create a file at the path `~/.canvas/credentials.ini`.
Here is what its contents should look like:

```ini
[buttered-popcorn]
client_id=butter
client_secret=salt

[buttered-popcorn-dev]
client_id=devbutter
client_secret=devsalt
is_default=true
```

Each section represents credentials for a different Canvas instance. Replace
the section headers with your Canvas subdomains. The example configuration
provided would be valid for instances with URLs
`https://buttered-popcorn.canvasmedical.com` and `https://buttered-popcorn-dev.canvasmedical.com`.

You can optionally set the `is_default` flag for the instance you wish to be
implied when using the CLI. If no section is set as default, the first one
will be considered default.


## 3. Initialize a new plugin

The Canvas CLI gives you a great head start when creating a plugin. Simply
run `canvas init`, and answer the prompt to name your plugin.

```sh
$ canvas init
  [1/1] project_name (My Cool Plugin): Paperwork Eviscerator
Project created in /Users/andrew/src/canvas-plugins/paperwork-eviscerator
```

This output shows the location of our freshly generated plugin project.

## 4. Navigate the structure of a plugin

Let's take a look at what was generated for us.

```sh
$ tree paperwork-eviscerator/
paperwork-eviscerator
├── paperwork_eviscerator
│   ├── __init__.py
│   ├── CANVAS_MANIFEST.json
│   ├── handlers
│   │   ├── __init__.py
│   │   └── event_handlers.py
│   └── README.md
├── pyproject.toml
└── tests
    ├── __init__.py
    └── test_event_handlers.py

4 directories, 8 files
```

### CANVAS_MANIFEST.json

The CANVAS_MANIFEST.json is particularly important. It is used during the
installation of the plugin.

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "paperwork_eviscerator",
    "description": "Edit the description in CANVAS_MANIFEST.json",
    "components": {
        "handlers": [
            {
                "class": "paperwork_eviscerator.handlers.event_handlers:NewOfficeVisitNoteHandler",
                "description": "A handler that listens for an event and sets an inspirational goal."
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": ["my_secret_code"],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

The name, plugin version, and description are all surfaced in your Canvas
instance when viewing installed plugins.

Only handlers declared here are invoked by the plugin runner. If they are
not declared, they will be ignored.

Secrets can be declared (though not defined) here. Any secrets declared here
will be initialized on plugin install, and can be set in the plugin listing in the Settings section of your Canvas instance.

### README.md

Share details about the purpose of your plugins and how it works in this
README file.

### handlers/event_handlers.py

This file contains the handler class declared in the manifest file. We've included
some sample content and comments for inspiration.

```python
from canvas_sdk.commands import GoalCommand
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.note import Note
from canvas_sdk.v1.data.patient import Patient
from logger import log


# Inherit from BaseHandler to properly get registered for events
class NewOfficeVisitNoteHandler(BaseHandler):
    """Originates goal command when a new office visit note is created."""

    # Name the event type you wish to run in response to
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def compute(self) -> list[Effect]:
        """This method gets called when an event of the type RESPONDS_TO is fired."""
        # This class is initialized with several pieces of information you can
        # access.
        #
        # `self.event` is the event object that caused this method to be
        # called.
        #
        # `self.event.target.id` is an identifier for the object that is the subject of
        # the event. In this case, it would be the identifier of the note state.
        #
        # `self.event.context` is a python dictionary of additional data that was
        # given with the event. The information given here depends on the
        # event type.
        #
        # `self.secrets` is a python dictionary of the secrets you defined in
        # your CANVAS_MANIFEST.json and set values for in the uploaded
        # plugin's configuration page: <emr_base_url>/admin/plugin_io/plugin/<plugin_id>/change/
        # Example: self.secrets['WEBHOOK_URL']

        # You can log things and see them using the Canvas CLI's log streaming
        # function.
        log.info(f"[NewOfficeVisitNoteHandler] Context: {self.event.context}")

        # Get the note state from context
        note_state = self.event.context.get("state")

        # Check if the note state is NEW
        if note_state != "NEW":
            return []

        # Get the note ID from context and fetch the Note object
        note_id = self.event.context.get("note_id")
        note = Note.objects.get(id=note_id)

        # Check if note type is OFFICE VISIT
        note_type_name = note.note_type_version.name

        if note_type_name != "Office visit":
            return []

        # Get the note UUID from context (it's already a UUID string)
        note_uuid = note_id

        # Get the patient to create a personalized goal statement
        patient_id = self.event.context.get("patient_id")
        patient = Patient.objects.get(id=patient_id)
        patient_name = patient.first_name
        goal_statement = f"{patient_name} will build plugins with the Canvas SDK to improve their clinical workflow"

        # Create and originate Goal command with personalized statement
        goal_command = GoalCommand(note_uuid=note_uuid, goal_statement=goal_statement)

        return [goal_command.originate()]
```

## 5. Listen for an Event

Set the `RESPONDS_TO` value to the [Event Type](/sdk/events/#event-types) you're interested in.

## 6. Return an Effect

Form an [Effect](/sdk/effects/#effect-types) to return to your Canvas
instance.

## 7. Deploy and use your plugin

When your plugin is just the way you'd like it, deploying is simple. Navigate to the root of your plugin project (i.e. `paperwork-eviscerator/`) and
run `canvas install <path/to/plugin_package>` (i.e. `canvas install paperwork_eviscerator`) and your plugin will be packaged,
uploaded, installed, and enabled. As you make changes to your plugin, run the
same command to update the code of the installed plugin.

## 8. Tail the logs

To view logs and to surface any errors with your plugin, run `canvas logs --host buttered-popcorn-dev` (replace with your Canvas instance name). This will tail the logs for all plugins installed on that instance.

<br/>
<br/>
<br/>
