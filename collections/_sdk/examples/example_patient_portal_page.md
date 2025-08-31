---
title: 'Customize Patient Portal Page'
slug: 'example-customize_patient_portal_page'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/example_patient_portal_page' target='_blank'>View the source</a> for this plugin on GitHub." %}

This plugin demonstrates how to embed custom patient facing content and tools to the Canvas patient portal. It provides an example of how to expose new patient-facing content or features via the portal, such as educational materials, forms, or interactive tools. On open, the plugin can launch an application and return effects to update the portal UI or patient data as needed.

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "example_patient_portal_page",
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
                "class": "example_patient_portal_page.applications.my_application:MyApplication",
                "name": "My Cool Tool",
                "description": "Defines the menu item and what it should launch.",
                "scope": "portal_menu_item",
                "icon": "assets/icon.png"
            }
        ],
        "protocols": [
            {
                "class": "example_patient_portal_page.handlers.my_web_app:MyWebApp",
                "description": "Serves the application"
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

## handlers/

### my_web_app.py

This file defines a simple web application, MyWebApp, that serves HTML, JavaScript, and CSS content.

**Authentication**

The app uses session credentials to check if a user is logged in before providing access to its endpoints. This is done in the authenticate method, which returns True only if a logged-in user exists.

**Endpoints**

- **/app/patient-portal-application**:  
  - Retrieves the current logged-in Patient using an ID supplied in the request headers.
  - Renders an HTML template ("static/index.html") and supplies the patient's first and last name as context variables.
  - Returns a rendered HTML page as the response.

- **/app/main.js**:  
  - Serves the contents of "static/main.js" as JavaScript.

- **/app/styles.css**:  
  - Serves the contents of "static/styles.css" as CSS.

**Template Rendering**

All files (HTML, JS, CSS) are rendered using the Canvas SDK's render_to_string function, allowing the inclusion of dynamic server-side data, especially for the HTML response.

**Security**

Only authenticated (logged-in) users can access any endpoint. The app enforces this globally by overriding the authenticate method.


```python
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import HTMLResponse, Response
from canvas_sdk.handlers.simple_api import SessionCredentials, SimpleAPI, api
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data.patient import Patient

#
# Check out https://docs.canvasmedical.com/sdk/handlers-simple-api-http


class MyWebApp(SimpleAPI):
    PREFIX = "/app"

    # Using session credentials allows us to ensure only logged in users can
    # access this.
    def authenticate(self, credentials: SessionCredentials) -> bool:
        return credentials.logged_in_user != None

    # Serve templated HTML
    @api.get("/patient-portal-application")
    def index(self) -> list[Response | Effect]:
        logged_in_user = Patient.objects.get(id=self.request.headers["canvas-logged-in-user-id"])

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

## assets/

### icon.png

This icon is displayed in the portal menu.

## applications/

### my_application.py

The code defines a custom application called `MyApplication`, which is the mechanism for registering the application in the portal menu..

**Key Functionality**

- The core implementation is within the `on_open` method, which handles the application's "open" event.
- When the application is opened, it triggers a launch effect (`LaunchModalEffect`) that opens an iframe modal.
- The iframe modal displays the content found at the URL `/plugin-io/api/example_patient_portal_page/app/patient-portal-application`.
- The effect specifically targets the main page area (`target=LaunchModalEffect.TargetType.PAGE`) for embedding.
- The `on_open` method is a customization point where additional logic could be inserted—for example, dynamic URL selection based on application state or data.


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
            url="/plugin-io/api/example_patient_portal_page/app/patient-portal-application",
            target=LaunchModalEffect.TargetType.PAGE,
        ).apply()
```

### \__init__.py

This file is empty.

## static/

### main.js

Static javascript referenced by the html template.

### styles.css

Stylesheets referenced by the html template.

### index.html

Templated HTML to render when the menu item is clicked.

<br/>
<br/>
<br/>
