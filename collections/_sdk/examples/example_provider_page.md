---
title: 'example_provider_page'
slug: 'example-example_provider_page'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/example_provider_page' target='_blank'>View the source</a> for this plugin on GitHub." %}

example_provider_page
=====================

## Description

Embed custom tools directly into clinical interface

### Important Note!

The CANVAS_MANIFEST.json is used when installing your plugin. Please ensure it
gets updated if you add, remove, or rename protocols.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "example_provider_page",
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
                "class": "example_provider_page.applications.my_application:MyApplication",
                "name": "My Cool Tool",
                "description": "Defines the menu item and what it should launch.",
                "scope": "provider_menu_item",
                "icon": "assets/python-logo.png"
            }
        ],
        "protocols": [
            {
                "class": "example_provider_page.handlers.my_web_app:MyWebApp",
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

**Purpose of the File**

This file defines a custom application class called `MyApplication` intended to be embedded as a plugin within the Canvas Medical platform, by extending the Canvas SDK's `Application` base class.

**Main Functionality**

- The primary purpose of this class is to handle the `on_open` event, which is triggered when the application is launched within Canvas.
- When `on_open` is triggered, the method returns a `LaunchModalEffect`, which instructs Canvas to open a modal window.
- The modal displays the content of the URL: `/plugin-io/api/example_provider_page/app/provider-application`. This URL can either be hosted as part of the plugin itself or point to an external page (which must be added to the plugin's manifest permissions if so).
- The modal is targeted to a "PAGE" context, which means it will open as a full-page modal within the Canvas interface.

**Integration with Canvas SDK**

- The code utilizes the Canvas SDK's Effects system, specifically `LaunchModalEffect`, to declaratively notify Canvas how the app should respond during launch.
- By subclassing `Application`, the code ensures that the component can be registered and recognized as an embeddable app inside Canvas.

**Customization Notes**

- The comments suggest this method could be customized to look up dynamic data before deciding which URL to launch. As currently written, it launches a static modal.
- To embed remote URLs, proper permissions must be declared in the `CANVAS_MANIFEST.json` file of the plugin.

**Summary**

This code enables the creation of an embeddable plugin application in Canvas Medical that, when opened, automatically launches a modal displaying a specified (and configurable) web page.

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
            url="/plugin-io/api/example_provider_page/app/provider-application",
            target=LaunchModalEffect.TargetType.PAGE,
        ).apply()
```

### __init__.py

This file is empty.
## assets/

### python-logo.png

## static/

### index.html

### main.js

### styles.css

## handlers/

### my_web_app.py

**Overview**

This code defines a subclass of SimpleAPI called MyWebApp for serving a simple web application through a Canvas plugin, using the Canvas SDK. It sets up API endpoints for authenticated users to access an HTML page and associated static resources (JavaScript and CSS).

**Authentication**

The authenticate() method ensures that only logged-in users (determined by the presence of credentials.logged_in_user) are allowed to use the endpoints. This ties in with Canvas session logic.

**Endpoints**

- /app/provider-application (GET):  
  Renders a templated HTML page (static/index.html) with the first and last name of the logged-in staff user injected into the template context. User info is looked up via Staff.objects.get using an id from the request headers (canvas-logged-in-user-id).
- /app/main.js (GET):  
  Serves the contents of static/main.js as JavaScript with an appropriate content-type header ("text/javascript").
- /app/styles.css (GET):  
  Serves the contents of static/styles.css as CSS with the content-type header set to "text/css".

**Template Rendering and Static Assets**

The render_to_string function is used throughout to retrieve and render files from the static/ directory, with HTMLResponse used for HTML and Response for other content types.

**Summary of Purpose**

This file provides a basic, authenticated web interface for a plugin—including user-specific HTML via a Jinja-like template, and static JS/CSS assets—intended for embedding or serving within the Canvas Medical environment. It demonstrates authenticating users via Canvas, injecting user data, and simple static asset routing.

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
    @api.get("/provider-application")
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
