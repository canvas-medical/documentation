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

{% include alert.html type="danger" content="<strong>With great power comes great responsibility.</strong> Your <code>compute()</code> method runs <strong>synchronously</strong> inside a worker. A slow <code>compute()</code> &mdash; especially one that makes a blocking network call to an external service (an LLM API, a third-party HTTP endpoint) &mdash; holds that worker for its entire duration. If the external service slows down or goes offline, every event that triggers your handler piles up until the worker pool is exhausted, and your <strong>entire Canvas instance can grind to a halt and stop responding to requests</strong>. Long timeouts and retries multiply the damage: a 300&nbsp;second timeout retried three times pins a single worker for over ten minutes. Keep <code>compute()</code> fast, and move long-running or failure-prone work off the synchronous path &mdash; see <a href='#keep-compute-fast'>Keep compute() fast</a> below." %}

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

```python?partial=true
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
your plugin with `self.secrets` and for the running instance with `self.environment`. You can use
our [Data Module](/sdk/data/) to retrieve additional information at runtime.

## Keep `compute()` fast

`compute()` runs synchronously on a bounded pool of plugin workers that is
shared across your whole Canvas instance. Whatever you do inside `compute()`
occupies one of those workers until it returns. Fast handlers free their worker
in milliseconds; slow handlers hold it, and a handler that blocks on a slow or
unavailable external dependency holds it for a long time. When enough handlers
are blocked at once, the pool is exhausted and the instance can no longer
respond to requests — providers experience this as the entire application
becoming inaccessible, not just your plugin.

This matters most when your handler responds to a high-frequency event (for
example, a note-state-change or task event that fires throughout the day) and
does work that can hang:

- **Calls to external HTTP APIs**, including LLM providers. These are the most
  common cause of instance-wide slowdowns, because a single provider-side
  outage turns every one of your handler invocations into a multi-second (or
  multi-minute) hang at the same time.
- **Long timeouts combined with retries.** A 300&nbsp;second timeout retried a
  few times can pin one worker for over ten minutes per event.
- **Heavy synchronous computation** that doesn't yield.

### Move slow work off the synchronous path

The platform can run effects asynchronously so they don't block the event that
produced them:

- Chain [`.set_async()`](/sdk/effects/#async-execution) on any effect to have
  the platform run it as a deferred task, with optional delay and retries. This
  is the right tool for **fire-and-forget side effects** (kick off a webhook,
  schedule a downstream write).
- Use the [`HttpRequestEffect`](/sdk/effect-http-request/) to have the platform
  make an HTTP call on your behalf — chained with `.set_async()` so the
  platform's async runner manages the delay, retries, and backoff instead of
  your handler blocking on the network.

Note that `set_async()` defers *effects*, not `compute()` itself — `compute()`
always runs synchronously. A raw blocking call made *inside* `compute()` (for
example, a `requests.post(...)` directly to a third-party API) still pins the
worker, regardless of whether the effects you return are async. If your handler
needs to "call an external service, read the result, then decide what to do,"
decompose it: a thin synchronous handler that emits an async effect to a
[SimpleAPI](/sdk/handlers-simple-api/) callback route, and let that route do the
slow work off the event path and apply its effects when it finishes.

If you genuinely cannot move the work off the synchronous path, at minimum cut
the reach of a failure: use a short timeout, limit retries, and gate the handler
so it only runs for the cases that truly need it.

<br/>
<br/>
<br/>
