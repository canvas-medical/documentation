---
title: "Base Handler"
slug: "handlers-basehandler"
excerpt: "Respond to system events with a list of effects."
hidden: false
---

The `BaseHandler` is the simplest of all handlers. Specify which events you
are interested in, then provide the code to execute when one of those events
is emitted. All the [handlers](/sdk/handlers/) inherit from `BaseHandler`, and
many of yours will too.

## Handling Events With `BaseHandler`

To create a class that responds to one or more events, inherit from
`BaseHandler`, set the `RESPONDS_TO` constant, and implement the `compute()`
method.

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler

class MyEventHandler(BaseHandler):

    RESPONDS_TO = EventType.Name(EventType.TASK_CREATED)

    def compute(self):
        # Your code goes here!
        return []
```

You can respond to one event, or several. To respond to multiple events, set
`RESPONDS_TO` to a list of [event types](/sdk/events/).

```python
# Respond when tasks are created:
RESPONDS_TO = EventType.Name(EventType.TASK_CREATED)

# Respond when tasks are created OR updated:
RESPONDS_TO = [
    EventType.Name(EventType.TASK_CREATED),
    EventType.Name(EventType.TASK_UPDATED),
]
```

The `compute()` method must return a list of [Effects](/sdk/effects/). That list can be empty,
of course. You have access to event information with `self.event`,
`self.target`, and`self.context`, as well as configuration information for
your plugin with `self.secrets`. You can use our [Data Module](/sdk/data/) to
retrieve additional information at runtime.

<br/>
<br/>
<br/>
<br/>
