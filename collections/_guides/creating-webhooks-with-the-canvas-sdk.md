---
title: "Creating Webhooks With the Canvas SDK"
---

Webhooks are user-defined callbacks that make a request to an API. You may
want to create a webhook to notify a system you control that some event has
occurred in Canvas. This guide shows how to create a webhook that sends an API
request containing the ID of a Task upon its creation.

{% include alert.html type="info" content="This guide assumes pre-existing
knowledge of the Canvas SDK. If you're starting from scratch, you may want to
read and implement <a href='/guides/your-first-plugin/'>Your First Plugin</a> before
working through this exercise." %}


## Initialize a new plugin

The Canvas CLI gives you a great head start when creating a plugin. Simply
run `canvas init`, and answer the prompt to name your plugin.

```
$ canvas init
  [1/1] project_name (My Cool Plugin): Task Webhook
Project created in /Users/andrew/src/canvas-plugins/task_webhook
```

This output shows the location of our freshly generated plugin.

## Edit the plugin code

The default content of this file shows you the information you have available
to you in the comments. I've stripped it down to almost nothing so we can
layer in the functionality step by step.

### Log a message when a task is created.

The code below listens for the `TASK_CREATED` event and logs the string "A
Task was created!".

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log


class Protocol(BaseProtocol):
    """
    When a task is created, log a message
    """

    RESPONDS_TO = EventType.Name(EventType.TASK_CREATED)

    def compute(self):
        """
        Log a message as tasks are created.
        """
        log.info("A Task was created!")

        return []
```

You can see this log output by first streaming logs with `canvas logs` and
then creating a task. You can create this task with Canvas Chat, a Task
Command, or our [FHIR Task Create endpoint](/api/task/#create).

After you've [installed your plugin](/sdk/canvas_cli/#canvas-install) and
created a task, you should see this in your log stream:

```
INFO 2024-09-26 17:04:08,396 Starting server, listening on port 50051
INFO 2024-09-26 17:04:08,396 Loading custom-plugins/task_webhook
INFO 2024-09-26 17:04:08,396 Loading plugin 'task_webhook:task_webhook.protocols.my_protocol:Protocol'
INFO 2024-09-26 17:04:24,410 A Task was created!
INFO 2024-09-26 17:04:24,410 task_webhook:task_webhook.protocols.my_protocol:Protocol.compute() completed (0 ms)
INFO 2024-09-26 17:04:24,411 Responded to Event TASK_CREATED (1 ms)
```

Awesome! But we're not here to log, we need to make an API request. To do
that, we need to use the HTTP client found in the Canvas SDK's [Utils
module](/sdk/utils/)

### Make an HTTP request when a Task is created

We can use [https://webhook.site/](https://webhook.site/) for a quick way to test our webhook and see
the requests it receives. Here is the updated code that uses the HTTP client
to make the request:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.utils import Http
from logger import log


class Protocol(BaseProtocol):
    """
    When a task is created, hit a webhook
    """

    RESPONDS_TO = EventType.Name(EventType.TASK_CREATED)

    def compute(self):
        """
        Notify our server of tasks as they are created.
        """

        url = "https://webhook.site/ee7aed78-b652-4d9e-b858-04465c409d15"
        payload = {
            "message": "A Task was created!"
        }

        http = Http()
        response = http.post(url, json=payload)

        if response.ok:
            log.info("Successfully notified API of task creation!")
        else:
            log.info("Notification unsuccessful. =[")

        return []
```

After you've [installed your updated plugin](/sdk/canvas_cli/#canvas-install) and
created a task, you should see this in your log stream:

```
INFO 2024-09-26 17:18:23,206 Loading custom-plugins/task_webhook
INFO 2024-09-26 17:18:23,207 Reloading plugin 'task_webhook:task_webhook.protocols.my_protocol:Protocol'
INFO 2024-09-26 17:18:33,850 Successfully notified API of task creation!
INFO 2024-09-26 17:18:33,851 task_webhook:task_webhook.protocols.my_protocol:Protocol.compute() completed (693 ms)
INFO 2024-09-26 17:18:33,851 Responded to Event TASK_CREATED (696 ms)
```

This log output is a great reminder for me to mention that making HTTP
requests to external servers will slow plugin execution while it waits on the
external server to respond. It's a good idea to make sure the servers you're
hitting have a sufficiently quick response time.

Checking in on our webhook.site logs shows it received our request!
![Log of web
request](/assets/images/webhook-guide/webhook-guide-first-request.png)


Awesome, but you aren't sending these requests to a server that allows
unauthenticated requests! And this request doesn't even tell you anything
about the task it's notifying you about. This isn't useful at all!

Let's do another iteration, this time using the information provided along
with the event so that we can send a usable message, securely. We're
specifically going to incorporate the event's `target` and `secrets`.

### Make an authenticated HTTP request that includes the newly created Task's ID

Within your `Protocol` class, you have access to `self.target`, which
represents the ID of the subject of the event. In our case, it will be the
Task's ID. This is the same ID used in the [FHIR Task endpoints](/api/task/),
so you can use it to make FHIR API requests.

You also have access to `self.secrets`, which is a python dictionary
containing the key-value pairs from your plugins configuration page. You
declare the keys in your `CANVAS_MANIFEST.json`, and can then set the values
after the plugin is installed.

We'll set two secrets, one for the unique id of the webhook, and one for an
auth token. Here's what the manifest file looks like with secrets declared:

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "task_webhook",
    "description": "Webhooks for task creation",
    "components": {
        "protocols": [
            {
                "class": "task_webhook.protocols.my_protocol:Protocol",
                "description": "Hit an API when a task is created",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
       ]
    },
    "secrets": ["WEBHOOK_ID", "AUTH_TOKEN"],
    "tags": {},
    "license": "",
    "readme": "./README.md"
}
```

The line `"secrets": ["WEBHOOK_ID", "AUTH_TOKEN"],` declares two secrets,
`WEBHOOK_ID` and `AUTH_TOKEN`. After we update the plugin, we can set values
for these in the plugin configuration page. This allows for different values
to be used across different installations.

Here's how that configuration looks:

![Plugin secrets
configuration](/assets/images/webhook-guide/webhook-guide-secrets.png)

With those values set, we can use them in our code:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.utils import Http
from logger import log


class Protocol(BaseProtocol):
    """
    When a task is created, hit a webhook
    """

    RESPONDS_TO = EventType.Name(EventType.TASK_CREATED)

    def compute(self):
        """
        Notify our server of tasks as they are created.
        """

        url = f"https://webhook.site/{self.secrets['WEBHOOK_ID']}"
        headers = {
            "Authorization": f"Bearer {self.secrets['AUTH_TOKEN']}"
        }
        payload = {
            "message": "A Task was created!",
            "resource_id": self.target
        }

        http = Http()
        response = http.post(url, json=payload, headers=headers)

        if response.ok:
            log.info("Successfully notified API of task creation!")
        else:
            log.info("Notification unsuccessful. =[")

        return []
```

And checking once more on our webhook.site logs shows it received our updated
request, including our `AUTH_TOKEN` value and the created task's ID.

![Log of web
request](/assets/images/webhook-guide/webhook-guide-second-request.png)


## Listening for multiple events

A single plugin class can listen for multiple event types. The event type will
be available in `self.event.type`, which will contain a member of the `EventType`
enum. The [full list of events is available](/sdk/events/#event-types).
Here is a short example that listens for two different events:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.utils import Http
from logger import log


class Protocol(BaseProtocol):
    """
    When a task is created or updated, hit a webhook
    """

    RESPONDS_TO = [
        EventType.Name(EventType.TASK_CREATED),
        EventType.Name(EventType.TASK_UPDATED),
    ]

    def compute(self):
        """
        Notify our server of tasks as they are created.
        """
        url = f"https://webhook.site/{self.secrets['WEBHOOK_ID']}"
        headers = {"Authorization": f"Bearer {self.secrets['AUTH_TOKEN']}"}

        # self.event.type is a member of the EventType enum corresponding to
        # one of the event types in the plugin's RESPONDS_TO attribute
        verb = 'created' if self.event.type == EventType.TASK_CREATED else 'updated'

        payload = {
            "message": f"A Task was {verb}!",
            "resource_id": self.target,
        }

        http = Http()
        response = http.post(url, json=payload, headers=headers)

        # You can also get the name of the event as as sting using EventType.Name()
        event_name = EventType.Name(self.event.type)

        if response.ok:
            log.info(f"Successfully notified API of {event_name}")
        else:
            log.info(f"Notification of {event_name} unsuccessful. =[")

        return []


Alternatively, you could include several classes, each resposible for some
specific request type. When including several classes in one plugin, they all
have access to the same secrets dictionary, you just need to declare each class
in the manifest file.

## Conclusion

I hope you found this helpful. Happy coding, we can't wait to see what you build!

<br/>
<br/>
<br/>
