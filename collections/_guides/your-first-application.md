---
title: "Your First Application"
guide_for:
- /sdk/handlers-applications/
---

This guide will walk you through the process of installing, initializing, and customizing embeddable applications in Canvas.

## What Are Applications in Canvas?

Applications in Canvas are embeddable plugins that enhance the functionality of the Canvas platform. They allow developers to create custom features accessible directly from within the Canvas interface, such as interactive tools, data visualizations, or workflow integrations. These applications can be configured to appear globally or within specific contexts, such as the patient chart page.

## Step 1: Install and Configure the Canvas CLI

Follow the instructions in the [Canvas documentation](https://docs.canvasmedical.com/guides/your-first-plugin/#1-install-the-canvas-cli) to install and configure the Canvas CLI. Once complete, ensure that you can successfully run `canvas` commands from your terminal.

## Step 2: Initialize an Application

To create a new application, run the following command:

```bash
canvas init application
```

This will generate a boilerplate application along with a `CANVAS_MANIFEST.json` file.

## Step 3: Understanding the `CANVAS_MANIFEST.json` File

The `CANVAS_MANIFEST.json` file describes your application and its components. Below is an example of a manifest and a description of the customizable properties:

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "my_cool_application",
    "description": "Edit the description in CANVAS_MANIFEST.json",
    "url_permissions": [
        {
            "url": "https://my-application.com",
            "permissions": []
        }
    ],
    "components": {
        "applications": [
            {
                "class": "my_cool_application.applications.my_application:MyApplication",
                "name": "My Application",
                "description": "An Application that does xyz...",
                "scope": "global",
                "icon": "assets/python-logo.png",
                "menu_position": "top",
                "menu_order": "100"
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

### Customizable Properties

1. **name**: The display name of the application.
2. **description**: A brief description of the application.
3. **icon**: The icon for the application. This can be a URL to an image or a path inside the plugin package.
4. **scope**:
   - `global`: The app will appear across all contexts.
   - `patient_specific`: The app will appear only in the patient chart page.
   - `provider_menu_item`: The app button will be displayed on the provider's menu.
   - `portal_menu_item`: The app button will be displayed on the patient portal menu.
5. **url_permissions**: The allowed urls and permissions for the application. This is used for security purposes. For more info check the [Application Handler](/sdk/handlers-applications).
6. **menu_position**: Determines where the menu item will be placed within the menu (this configuration applies only to the providers menu) 
   - `top`: The item will be placed on the top section.
   - `bottom`: The item will be placed in the bottom section - this section should display items that open in a new window.
7. **menu_order**: How the items will be ordered in the menu. e.g 100, 200

## Step 4: Overriding the Application Behavior

Developers must extend the `Application` class and override the `on_open` method to define the behavior when the app icon is clicked. Below is an example implementation:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application

class MyApplication(Application):
    """An embeddable application that can be registered to Canvas."""

    def on_open(self) -> Effect:
        """Handle the on_open event."""
        # Implement this method to handle the application on_open event.
        return LaunchModalEffect(
            url="http://localhost:8000",
            target=LaunchModalEffect.TargetType.DEFAULT_MODAL
        ).apply()
```

### Key Details

- **`on_open` Method**:
  - Called when the user clicks on the app icon.
  - Should return a `LaunchModalEffect` that specifies:
    - **url**: The URL to open.
    - **target**: The display target.

### Target Options

- `DEFAULT_MODAL`: Opens the URL in a modal centered on the screen.
- `NEW_WINDOW`: Opens the URL in a new browser window.
- `PAGE`: Opens the URL as a page in the app
- `RIGHT_CHART_PANE`: Opens the URL in the right-hand pane of the patient chart.
- `RIGHT_CHART_PANE_LARGE`: Opens the URL in an enlarged right-hand pane of the patient chart.

## Step 5: Installing the Application

To install your application, run:

```bash
canvas install <path/to/application>
```

<br/>
<br/>
<br/>
<br/>
