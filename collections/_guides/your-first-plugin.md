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
request additional [data](/sdk/data/) if needed, and respond with [effects](/sdk/effects/) that
mutate state in Canvas. You can also use [utils](/sdk/utils/) to do things like call out to web
services with our provided HTTP client.

## Video

The video below showcases a Canvas engineer working through this guide
step-by-step.

<iframe width="560" height="315"
src="https://www.youtube.com/embed/X2JOEElq2ck?si=V6oA6eolpyq_kYGE&amp;controls=0"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## 1. Install the Canvas CLI

To install the Canvas CLI, simply `pip install canvas`. You can find
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

```
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

```
$ canvas init
  [1/1] project_name (My Cool Plugin): Paperwork Eviscerator
{"success": true, "message": "Project created in /Users/andrew/src/canvas-plugins/paperwork_eviscerator",
"project_dir": "/Users/andrew/src/canvas-plugins/paperwork_eviscerator"}
```

This output shows the location of our freshly generated plugin.

## 4. Navigate the structure of a plugin

Let's take a look at what was generated for us.

```
$ tree paperwork_eviscerator/
paperwork_eviscerator/
|-- CANVAS_MANIFEST.json
|-- README.md
`-- protocols
    |-- __init__.py
    `-- my_protocol.py

2 directories, 4 files
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
        "protocols": [
            {
                "class": "paperwork_eviscerator.protocols.my_protocol.Protocol",
                "description": "A protocol that does xyz...",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": [],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

The name, plugin version, and description are all surfaced in your Canvas
instance when viewing installed plugins.

Only protocols declared here are invoked by the plugin runner. If they are
not declared, they will be ignored.

Secrets can be declared (though not defined) here. Any secrets declared here
will be initialized on plugin install, and can be set in the plugin listing on
your Canvas instance.

### README.md

Share details about the purpose of your plugins and how it works in this
README file.

### protocols/my_protocol.py

This file contains the protocol class declared in the manifest file. We've included
some sample content and copious comments for inspiration.

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log


# Inherit from BaseProtocol to properly get registered for events
class Protocol(BaseProtocol):
    """
    You should put a helpful description of this protocol's behavior here.
    """

    # Name the event type you wish to run in response to
    RESPONDS_TO = EventType.Name(EventType.ASSESS_COMMAND__CONDITION_SELECTED)

    NARRATIVE_STRING = "I was inserted from my plugin's protocol."

    def compute(self):
        """
        This method gets called when an event of the type RESPONDS_TO is fired.
        """
        # This class is initialized with several pieces of information you can
        # access.
        #
        # `self.event` is the event object that caused this method to be
        # called.
        #
        # `self.target` is an identifier for the object that is the subject of
        # the event. In this case, it would be the identifier of the assess
        # command. If this was a patient create event, it would be the
        # identifier of the patient. If this was a task update event, it would
        # be the identifier of the task. Etc, etc.
        #
        # `self.context` is a python dictionary of additional data that was
        # given with the event. The information given here depends on the
        # event type.
        #
        # `self.secrets` is a python dictionary of the secrets you defined in
        # your CANVAS_MANIFEST.json and set values for in the uploaded
        # plugin's configuration page: <emr_base_url>/admin/plugin_io/plugin/<plugin_id>/change/
        # Example: self.secrets['WEBHOOK_URL']

        # You can log things and see them using the Canvas CLI's log streaming
        # function.
        log.info(self.NARRATIVE_STRING)

        # Craft a payload to be returned with the effect(s).
        payload = {
            "note": {"uuid": self.context["note"]["uuid"]},
            "data": {"narrative": self.NARRATIVE_STRING},
        }

        # Return zero, one, or many effects.
        # Example:
        # return [Effect(type=EffectType.ADD_PLAN_COMMAND, payload=json.dumps(payload))]
        return []
```

## 5. Listen for an Event

Set the `RESPONDS_TO` value to the [Event Type](/sdk/events/#event-types) you're interested in.

## 6. Return an Effect

Form an [Effect](/sdk/effects/#effect-types) to return to your Canvas
instance.

## 7. Deploy and use your plugin

When your plugin is just the way you'd like it, deploying is simple. Simply
run `canvas install <path/to/plugin_root>` and your plugin will be packaged,
uploaded, installed, and enabled. As you make changes to your plugin, run the
same command to update the code of the installed plugin.


