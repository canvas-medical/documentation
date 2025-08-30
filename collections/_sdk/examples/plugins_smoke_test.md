---
title: 'plugins_smoke_test'
slug: 'example-plugins_smoke_test'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/plugins_smoke_test' target='_blank'>View the source</a> for this plugin on GitHub." %}

plugins_smoke_test
==================

Make this plugin do lots of stuff so we can smoke test plugins

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "plugins_smoke_test",
    "description": "Used to test various canvas plugins functionality",
    "url_permissions": [
        {
            "url": "https://www.canvasmedical.com/extensions",
            "permissions": []
        }
    ],
    "components": {
        "protocols": [
            {
                "class": "plugins_smoke_test.applications.my_application:SmokeTestApi",
                "description": "Provides api for the application",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
        ],
        "applications": [
            {
                "class": "plugins_smoke_test.applications.my_application:MyGlobalApplication",
                "name": "Smoke Test",
                "description": "Test various canvas plugins functionality",
                "scope": "global",
                "icon": "assets/test-pattern.png"
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

## templates/

### global-smoke-test.html

## applications/

### my_application.py

**Purpose**

The code defines an example plugin for the Canvas Medical application platform. It demonstrates basic integration via the Canvas SDK, including launching a modal window, rendering HTML in response to API requests, authenticating staff users, and creating tasks via an API endpoint.

**Classes and Functionality**

**MyGlobalApplication**

- Subclass of Application.
- Overrides on_open to immediately launch a modal window containing content served from the "/plugin-io/api/plugins_smoke_test/global" endpoint. This modal uses the default modal interface as specified by the Canvas SDK.

**SmokeTestApi**

- Subclass of StaffSessionAuthMixin and SimpleAPI, meaning all endpoints require authenticated staff context.
- Contains two endpoints:
  
  1. **GET /global**
     - Retrieves the currently logged-in staff user (using their ID from request headers).
     - Renders an HTML template ("templates/global-smoke-test.html") with the staff user's info passed in the context.
     - Returns the rendered HTML as an HTTP 200 response.

  2. **POST /add-task**
     - Creates a new task (title: "This came from the smoke test", status: OPEN, due in 5 days).
     - Uses the SDK's AddTask effect to schedule creation of the task.
     - Returns the effect to trigger task creation and additionally returns a JSON response indicating that the task will be created, with HTTP 202 Accepted status.

**Summary of Integration with Canvas SDK**

- Uses SDK "Effect" classes to trigger UI changes (modal launch) and backend actions (task creation).
- Uses HTTP and JSON/HTML responses according to API best practices.
- Employs template rendering and staff-user context for personalized interface.
- Demonstrates safe, authenticated access for staff users.

**Intended Usage**

The plugin is a "smoke test" — it is intended to be a simple demonstration or test of core SDK capabilities (auth, UI modals, staff context, API endpoints, and task creation). It can serve as a starting point or example for building more complex integrations with the Canvas Medical platform.

```python
import arrow

from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.effects.simple_api import Response, JSONResponse, HTMLResponse
from canvas_sdk.effects.task import AddTask, TaskStatus

from canvas_sdk.handlers.application import Application
from canvas_sdk.handlers.simple_api import StaffSessionAuthMixin, SimpleAPI, api

from canvas_sdk.templates import render_to_string

from canvas_sdk.v1.data.staff import Staff


class MyGlobalApplication(Application):
    def on_open(self) -> Effect:
        return LaunchModalEffect(
            url="/plugin-io/api/plugins_smoke_test/global",
            target=LaunchModalEffect.TargetType.DEFAULT_MODAL,
        ).apply()


class SmokeTestApi(StaffSessionAuthMixin, SimpleAPI):
    @api.get("/global")
    def ical_links(self) -> list[Response | Effect]:
        logged_in_staff = Staff.objects.get(id=self.request.headers["canvas-logged-in-user-id"])

        context = {
            "logged_in_staff": logged_in_staff,
        }
        return [
            HTMLResponse(
                render_to_string("templates/global-smoke-test.html", context),
                status_code=HTTPStatus.OK,
            )
        ]

    @api.post("/add-task")
    def add_task(self) -> list[Response | Effect]:
        add_task = AddTask(
            title="This came from the smoke test.",
            due=arrow.utcnow().shift(days=5).datetime,
            status=TaskStatus.OPEN,
        )
        return [
            add_task.apply(),
            JSONResponse(
                {"message": "Task will be created"},
                status_code=HTTPStatus.ACCEPTED
            )
        ]
```

### __init__.py

This file is empty.
## assets/

### test-pattern.png

<br/>
<br/>
<br/>
