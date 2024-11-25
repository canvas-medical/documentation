---
title: "Staying on Top of Tasks"
---

Many Canvas users work in multiple systems. If you have a system that deals
with tasks that are ultimately completed in Canvas, you'll want to manage the
full task lifecycle from that external system. Using Canvas' [FHIR API](/api/) and the
[Canvas SDK](/sdk/), you can have your system create tasks in Canvas, and get notified
when your users complete them.

<br/>
<div style="text-align: center;">
  <img src="/assets/images/guides/staying-on-top-of-tasks/flow.png" width="80%">
</div>

## Creating Tasks with the FHIR API

Your system can originate Tasks in Canvas using our FHIR [Task Create endpoint](/api/task/#create).
The id of the task you create can be found in the `location` response header.
It comes back as the FHIR Task Read URL, but you can parse the id from it. See
the example below. Remember, this code is hitting the Canvas API from _your_
system, not from within Canvas.

```python
import requests
import json

payload = json.dumps({
  "resourceType": "Task",
  "status": "requested",
  "intent": "unknown",
  "description": "Send a thank you card to the office admin team.",
  "requester": {
    "reference": "Practitioner/abc123"
  }
})

url = "https://fumage-api-test-clinic.canvasmedical.com/Task"

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'not-a-real-token'
}

response = requests.request("POST", url, headers=headers, data=payload)

# find the id of the task we just created
task_location = response.headers['location']  # http://fumage-api-test-clinic.canvasmedical.com/Task/b6426693-eb5b-4702-9f90-4728972c7f16
task_id = task_location.split("/Task/")[1]  # b6426693-eb5b-4702-9f90-4728972c7f16
```

You can then take that task id and persist it in your application for tracking
its status. While some choose to poll for status changes, a better way to keep
track of the state of a task is by creating a webhook. We can do that with the
Canvas SDK.

## Creating a Task completion webhook with the Canvas SDK

{% include alert.html type="info" content="Webhook plugins are discussed in
more detail in <a href='/guides/creating-webhooks-with-the-canvas-sdk/'>Creating Webhooks with the Canvas SDK</a>." %}

Implementing webhooks in a plugin gives you ultimate control over the payload
and headers in your request. We use the python
[requests](https://requests.readthedocs.io/en/latest/) library under the hood,
so there's an extremely good chance anything you require for your request is
supported. 

In this example, we listen for either the `TASK_COMPLETED` or the
`TASK_CLOSED` events, and send an HTTP POST with the id of the task that was
either completed or closed, along with whether it was completed or closed. The
target of the event is the id of the task, so the event comes with all the
information we need here. You can substitute any of the Canvas SDK's supported
[events](/sdk/events/) to extend this example to other record types.


```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.utils import Http

from logger import log


class TaskResolutionWebhook(BaseHandler):

    RESPONDS_TO = [
        EventType.Name(EventType.TASK_COMPLETED),
        EventType.Name(EventType.TASK_CLOSED),
    ]

    def compute(self):
        task_disposition = 'closed'
        if self.event.type == EventType.TASK_COMPLETED:
            task_disposition = 'completed'

        url = "https://webhook.site/ee7aed78-b652-4d9e-b858-04465c409d15"
        payload = {
            "task_id": self.target,
            "disposition": task_disposition,
        }

        http = Http()
        response = http.post(url, json=payload)
        
        if response.ok:
            log.info("Successfully notified API of task update!")
        else:
            log.info("Notification unsuccessful. =[")

        return []
```

Once installed, the url you specified in the code will receive an HTTP POST
request whenever a user marks a task as completed or closed. Your application
can listen for those requests and update your internal status of that task.

<br/>
<br/>
<br/>
