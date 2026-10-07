---
title: "Your First Plugin (Manual)"
guide_for:
- /sdk/quickstart/
- /sdk/canvas_cli/
- /sdk/events/
- /sdk/effects/
---

Plugins are your tool for customizing the Canvas experience. By using the
modules of the Canvas SDK, you can react to [events](/sdk/events/) emitted from the EHR,
request additional [data](/sdk/data/) if needed, and respond with [effects](/sdk/effects/) that alter workflows and add or change data in Canvas. You can also use [utils](/sdk/utils/) to do things like call out to web services with our provided HTTP client.

{% include alert.html type="warning" content="This guide is for manual coding. Want a faster, AI-assisted approach? Check out <a href='/guides/your-first-plugin-with-claude-code/'>Your First Plugin (with Claude Code)</a>, which uses an AI assistant to guide you through building and deploying your plugin." %}

## Video

The video below showcases a Canvas engineer working through this guide
step-by-step.

<iframe width="560" height="315"
src="https://www.youtube.com/embed/X2JOEElq2ck?si=V6oA6eolpyq_kYGE&amp;controls=0"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## 1. Install the Canvas CLI

To install the Canvas CLI, simply `pip install canvas`. Python 3.11–3.14 (`>=3.11, <3.15`) is required. You can find
additional detail on the features of the Canvas CLI [here](/sdk/canvas_cli/).

## 2. Sign in to Canvas Platform

The Canvas CLI deploys plugins through [Canvas Platform](https://platform.canvasmedical.com).
Sign in once on your machine:

```sh
$ canvas login
Signed in to https://platform.canvasmedical.com as you@example.com.
  Acme Health (acme): plugin prefix acme__
```

`canvas login` opens your browser and lists each organization you belong to with
its plugin prefix. Every plugin you publish is named with that prefix, such as
`acme__paperwork_eviscerator`. Publishing a plugin needs the Plugin developer role
in the organization, and deploying it needs Deploy manager.

{% include alert.html type="info" content="Configuring the CLI with OAuth client credentials in <code>~/.canvas/credentials.ini</code> is deprecated, and support ends on December 14, 2026. See <a href='/guides/moving-to-canvas-platform/'>Moving to Canvas Platform</a>." %}


## 3. Initialize a new plugin

The Canvas CLI gives you a great head start when creating a plugin. Simply
run `canvas init`, and answer the prompt to name your plugin.

```sh
$ canvas init
  [1/1] project_name (My Cool Plugin): Paperwork Eviscerator
Project created in /Users/andrew/src/canvas-plugins/paperwork-eviscerator
Registered acme__paperwork_eviscerator with Canvas Platform.
```

This output shows the location of our freshly generated plugin project. `canvas init`
names the package with your organization's prefix, registers it with Canvas Platform,
and makes the project folder a git repository that `canvas deploy` pushes to. If you
belong to several organizations, it asks which one publishes the plugin.

## 4. Navigate the structure of a plugin

Let's take a look at what was generated for us.

```sh
$ tree paperwork-eviscerator/
paperwork-eviscerator/
├── acme__paperwork_eviscerator
│    ├── CANVAS_MANIFEST.json
│    ├── README.md
│    └── handlers
│         ├── __init__.py
│         └── event_handlers.py
├── pyproject.toml
└── tests
    ├── __init__.py
    └── test_models.py

5 directories, 9 files
```

### CANVAS_MANIFEST.json

The CANVAS_MANIFEST.json is particularly important. It is used during the
installation of the plugin. See the [Canvas Manifest](/sdk/canvas_manifest/)
reference for every field it can contain.

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "acme__paperwork_eviscerator",
    "description": "Edit the description in CANVAS_MANIFEST.json",
    "components": {
        "handlers": [
            {
                "class": "acme__paperwork_eviscerator.handlers.event_handlers:Handler",
                "description": "A handler that does xyz...",
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
    "variables": [
        {"name": "my_secret_code", "sensitive": true}
    ],
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
will be initialized on plugin install, and can be set with [`canvas config set`](/sdk/canvas_cli/#canvas-config-set).

### README.md

Share details about the purpose of your plugins and how it works in this
README file.

### handlers/event_handlers.py

This file contains the handler class declared in the manifest file. We've included
some sample content and copious comments for inspiration.

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from logger import log


# Inherit from BaseHandler to properly get registered for events
class Handler(BaseHandler):
    """
    You should put a helpful description of this handler's behavior here.
    """

    # Name the event type you wish to run in response to
    RESPONDS_TO = EventType.Name(EventType.ASSESS_COMMAND__CONDITION_SELECTED)

    NARRATIVE_STRING = "I was inserted from my plugin's handler."

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
        # return [Effect(type=EffectType.LOG, payload=json.dumps(payload))]
        return []
```

## 5. Listen for an Event

Set the `RESPONDS_TO` value to the [Event Type](/sdk/events/#event-types-and-context) you're interested in.

## 6. Return an Effect

Form an [Effect](/sdk/effects/#effect-types) to return to your Canvas
instance.

## 7. Deploy and use your plugin

When your plugin is just the way you'd like it, validate it and deploy it. Navigate to the root of your plugin project (i.e. `paperwork-eviscerator/`) and run:

```sh
$ canvas validate acme__paperwork_eviscerator
$ canvas deploy acme__paperwork_eviscerator --instance buttered-popcorn-dev
```

`canvas deploy` commits your changes after you confirm, pushes them to Canvas Platform, and
deploys that commit to the instance, where the plugin is installed and enabled. Replace
`buttered-popcorn-dev` with your instance; without `--instance`, `deploy` targets the only
instance you can deploy to, or lists the choices. As you make changes to your plugin, run the
same command to deploy the new code.

## 8. Tail the logs

To view logs and to surface any errors with your plugin, run `canvas logs --host buttered-popcorn-dev` (replace with your Canvas instance name). This will tail the logs for all plugins installed on that instance.

`canvas logs` connects to the instance with the [instance API credentials](/sdk/canvas_cli/#instance-api-credentials-credentialsini-deprecated) in `~/.canvas/credentials.ini` until it moves to your Canvas Platform sign-in, before December 14, 2026.

<br/>
<br/>
<br/>
