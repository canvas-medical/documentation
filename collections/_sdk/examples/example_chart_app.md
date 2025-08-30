---
title: 'example_chart_app'
slug: 'example-example_chart_app'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/example_chart_app' target='_blank'>View the source</a> for this plugin on GitHub." %}

example_chart_app
==================

An example custom UI for the patient chart

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "example_chart_app",
    "description": "Used to test various canvas plugins functionality",
    "url_permissions": [],
    "components": {
        "protocols": [
            {
                "class": "example_chart_app.applications.my_application:MyApi",
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
                "class": "example_chart_app.applications.my_application:MyChartApplication",
                "name": "Example Chart App",
                "description": "Show a custom, interactive UI in the chart",
                "scope": "patient_specific",
                "icon": "assets/rx.png"
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

### custom-ui.html

## applications/

### my_application.py

**Overview**

This file defines an application plugin for Canvas Medical using the Canvas SDK. It includes a custom application (`MyChartApplication`) and an API (`MyApi`) for rendering a modal user interface pane and handling related actions, such as adding tasks.

**MyChartApplication Class**

- Subclasses the `Application` class from the Canvas SDK.
- The `on_open` method is triggered when the application is opened. It retrieves the current patient's ID from `self.context`.
- It returns a `LaunchModalEffect`, which opens a custom modal UI in the right chart pane. The URL for this modal includes the patient ID as a query parameter.

**MyApi Class**

- Subclasses both `StaffSessionAuthMixin` and `SimpleAPI`, enabling API definition with authentication.
- Defines two endpoints using the `@api` decorator: a GET and a POST.

**GET /custom-ui**

- Endpoint: `/custom-ui`
- Retrieves the logged-in staff user via the header `"canvas-logged-in-user-id"`.
- Renders a template (`templates/custom-ui.html`) with context including the logged-in staff and the selected patient ID.
- Returns the rendered HTML as an `HTMLResponse` with HTTP 200 (OK) status.

**POST /add-task**

- Endpoint: `/add-task`
- Creates a new task for the specified patient (using `patient_id` from the posted JSON payload).
- Sets the task to be due in 5 days from the current UTC time and sets its status to open.
- Returns two responses:
  - The effect to add a task (which also triggers any related UI updates).
  - A JSON response with a success message and HTTP 202 (Accepted) status.

**Miscellaneous**

- Imports various components and utilities from the Canvas SDK, such as effects for UI actions, response types, authentication mixins, and template rendering.
- Uses the `arrow` library for time/date handling.

**Summary**

The code provides a Canvas plugin that opens a modal UI displaying custom content for a selected patient. It can also create a new patient-related task when a specific endpoint is called, handling user authentication and returning appropriate UI and API responses. The flow is tailored to staff users interacting with patient charts.

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


class MyChartApplication(Application):
    def on_open(self) -> Effect:
        patient_id = self.context['patient']['id']
        return LaunchModalEffect(
            url=f"/plugin-io/api/example_chart_app/custom-ui?patient={patient_id}",
            target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
        ).apply()


class MyApi(StaffSessionAuthMixin, SimpleAPI):
    @api.get("/custom-ui")
    def ical_links(self) -> list[Response | Effect]:
        logged_in_staff = Staff.objects.get(id=self.request.headers["canvas-logged-in-user-id"])

        context = {
            "logged_in_staff": logged_in_staff,
            "patient_id": self.request.query_params["patient"],
        }
        return [
            HTMLResponse(
                render_to_string("templates/custom-ui.html", context),
                status_code=HTTPStatus.OK,
            )
        ]

    @api.post("/add-task")
    def add_task(self) -> list[Response | Effect]:
        add_task = AddTask(
            title="This came from the custom patient ui.",
            patient_id=self.request.json()["patient_id"],
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

### rx.png

<br/>
<br/>
<br/>
