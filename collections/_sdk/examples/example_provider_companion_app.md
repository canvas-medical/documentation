---
title: 'example_provider_companion_app'
slug: 'example-example_provider_companion_app'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/example_provider_companion_app' target='_blank'>View the source</a> for this plugin on GitHub." %}

example_provider_companion_app
=====================

## Description

This plugin demonstrates how to Extend provider workflows to on-the-go capabilities through custom mobile web applications for use with Canvas. It provides an example of how to add provider-facing features or workflows, such as custom notifications, workflow shortcuts, or integrations with external tools. On open, the plugin can launch an application to update the provider UI or trigger provider-specific actions as needed.

### Important Note!

The CANVAS_MANIFEST.json is used when installing your plugin. Please ensure it
gets updated if you add, remove, or rename protocols.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "example_provider_companion_app",
    "description": "Edit the description in CANVAS_MANIFEST.json",
    "url_permissions": [
        {
            "url": "https://www.canvasmedical.com/extensions",
            "permissions": ["ALLOW_SAME_ORIGIN", "SCRIPTS", "MICROPHONE", "CAMERA"]
        }
    ],
    "components": {
        "applications": [
            {
                "class": "example_provider_companion_app.applications.my_application:MyApplication",
                "name": "My Cool Tool",
                "description": "Defines the app icon what it should launch.",
                "scope": "provider_companion",
                "icon": "assets/doctor.png"
            }
        ],
        "protocols": [
            {
                "class": "example_provider_companion_app.handlers.my_web_app:MyWebApp",
                "description": "Serves the application",
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

## applications/

### my_application.py

**Overview**

This file defines a class called `MyApplication`, which is a custom embeddable application plugin for the Canvas platform. It uses the Canvas SDK to integrate with the Canvas Medical EHR environment.

**Key Functionality**

- The class inherits from `Application`, making it a valid embeddable app that can be registered to Canvas.
- It implements the `on_open` method, which is a Canvas application lifecycle event handler that executes when the app is opened.

**on_open Method**

- The `on_open` method is responsible for responding to the application's "open" event.
- When triggered, it launches a modal window in the Canvas UI.
- The modal displays content from the URL `/plugin-io/api/example_provider_companion_app/app/provider-app`, which could be hosted by the plugin or externally (with the appropriate permissions in the plugin's manifest).
- The effect is applied and returned using Canvas SDK's `LaunchModalEffect`, specifically setting the modal's target type to the platform's default modal.

**Summary of Purpose**

The code enables the plugin to show a modal dialog with custom content whenever the application is opened in Canvas, making it easy to embed additional user interfaces, widgets, or workflows from a specified URL inside Canvas Medical.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application


class MyApplication(Application):
    """An embeddable application that can be registered to Canvas."""

    def on_open(self) -> Effect:
        """Handle the on_open event."""
        # Implement this method to handle the application on_open event.
        # You can look up data here to be used in knowing what to launch, if
        # what you're launching depends on some dynamic criteria.

        return LaunchModalEffect(
            # This URL is what will get iframed. It can be hosted elsewhere,
            # or it could be hosted by your plugin! Canvas plugins can serve
            # html, css, js, or json.
            #
            # If embedding a remote URL, be sure to declare it in the URL
            # permissions section of your plugin's CANVAS_MANIFEST.json
            url="/plugin-io/api/example_provider_companion_app/app/provider-app",
            target=LaunchModalEffect.TargetType.DEFAULT_MODAL,
        ).apply()
```

### __init__.py

This file is empty.
## assets/

### doctor.png

## static/

### index.html

### main.js

### styles.css

## handlers/

### my_web_app.py

**Purpose of the File**

The code defines a web application class MyWebApp, using the Canvas SDK's SimpleAPI system. It configures several HTTP GET routes under the "/app" prefix and ensures user authentication for access.

**Authentication**

- The authenticate method confirms that only logged-in Canvas users (those for whom credentials.logged_in_user is not None) can access the app's routes.

**HTTP Endpoints**

- **/app/provider-app**:  
  - Serves a templated HTML page.
  - Fetches the currently logged-in user (a Staff object) based on the "canvas-logged-in-user-id" passed in request headers.
  - renders static/index.html with the provider's first and last name passed into the template context as context variables.
  - Returns the generated HTML with HTTP 200 OK.

- **/app/main.js**:  
  - Serves the static/main.js file as raw JavaScript with the appropriate Content-Type header.
  - Returns the file's contents as a response with HTTP 200 OK.

- **/app/styles.css**:  
  - Serves the static/styles.css file as raw CSS with the appropriate Content-Type header.
  - Returns the file's contents as a response with HTTP 200 OK.

**Summary of Operation**

- The app's routes are only accessible to authenticated users.
- The app provides essential UI resources: an HTML page, a JavaScript file, and a CSS file.
- It uses Canvas-specific session/bearer authentication and standard Canvas SDK response and rendering utilities.
- The app is structured following Canvas SDK best practices for simple web plugins.

```python
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import HTMLResponse, Response
from canvas_sdk.handlers.simple_api import SessionCredentials, SimpleAPI, api
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data.staff import Staff

#
# Check out https://docs.canvasmedical.com/sdk/handlers-simple-api-http


class MyWebApp(SimpleAPI):
    PREFIX = "/app"

    # Using session credentials allows us to ensure only logged in users can
    # access this.
    def authenticate(self, credentials: SessionCredentials) -> bool:
        return credentials.logged_in_user != None

    # Serve templated HTML
    @api.get("/provider-app")
    def index(self) -> list[Response | Effect]:
        logged_in_user = Staff.objects.get(id=self.request.headers["canvas-logged-in-user-id"])

        context = {
            "first_name": logged_in_user.first_name,
            "last_name": logged_in_user.last_name,
        }

        return [
            HTMLResponse(
                render_to_string("static/index.html", context),
                status_code=HTTPStatus.OK,
            )
        ]

    # Serve the contents of a js file
    @api.get("/main.js")
    def get_main_js(self) -> list[Response | Effect]:
        return [
            Response(
                render_to_string("static/main.js").encode(),
                status_code=HTTPStatus.OK,
                content_type="text/javascript",
            )
        ]

    # Serve the contents of a css file
    @api.get("/styles.css")
    def get_css(self) -> list[Response | Effect]:
        return [
            Response(
                render_to_string("static/styles.css").encode(),
                status_code=HTTPStatus.OK,
                content_type="text/css",
            )
        ]
```

<br/>
<br/>
<br/>
