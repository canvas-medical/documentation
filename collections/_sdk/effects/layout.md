---
title: "Layout Effects"
slug: "layout-effect"
excerpt: "Modify or interact with the layout in Canvas."
hidden: false
---

## Patient Summary
There are many summary sections in a patient's chart, organized by data type.
While there is a default ordering, you can use an Effect to reorder them or
hide some of them entirely. The `PatientChartSummaryConfiguration` class helps
you craft the effect to do so.

![Before and after](/assets/images/sdk/summary-section-modified.png)

The example below shows reordering and hiding or omitting some of the
sections:

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.effects.patient_chart_summary_configuration import PatientChartSummaryConfiguration


class SummarySectionLayout(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION)

    def compute(self):
        layout = PatientChartSummaryConfiguration(sections=[
          PatientChartSummaryConfiguration.Section.CARE_TEAMS,
          PatientChartSummaryConfiguration.Section.SOCIAL_DETERMINANTS,
          PatientChartSummaryConfiguration.Section.ALLERGIES,
          PatientChartSummaryConfiguration.Section.CONDITIONS,
          PatientChartSummaryConfiguration.Section.MEDICATIONS,
          PatientChartSummaryConfiguration.Section.VITALS,
        ])

        return [layout.apply()]
```

The `PatientChartSummaryConfiguration` takes a single argument, `sections`,
which is expected to be a list at least one element long, filled with choices
from the `PatientChartSummaryConfiguration.Section` enum. The `.apply()`
method returns a well-formed `Effect` object.

This effect is only used in response to the
`PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION` event. It does nothing in any
other context.

Values in the `PatientChartSummaryConfiguration.Section` enum are:

| Constant            | Description         |
|---------------------|---------------------|
| SOCIAL_DETERMINANTS | social_determinants |
| GOALS               | goals               |
| CONDITIONS          | conditions          |
| MEDICATIONS         | medications         |
| ALLERGIES           | allergies           |
| CARE_TEAMS          | care_teams          |
| VITALS              | vitals              |
| IMMUNIZATIONS       | immunizations       |
| SURGICAL_HISTORY    | surgical_history    |
| FAMILY_HISTORY      | family_history      |
| CODING_GAPS         | coding_gaps         |

### Action Buttons
Each section of the patient chart can also be customized with action buttons. Please refer to the [Action Buttons](/sdk/handlers-action-buttons/) documentation for more information.


## Patient Profile


The ``PatientProfileConfiguration`` class allows you to reorder, hide, and/or specificy whether sections load expanded or collapsed. 

``` python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.effects.patient_profile_configuration import PatientProfileConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log


class Protocol(BaseProtocol):
    """This protocol is used to configure which sections appear in the Patient Profile section.

    The SHOW_PATIENT_PROFILE_SECTIONS payload expects a list of sections where each section is a dict like { "type": str, "start_expanded": bool }
    The accepted values for the "type" are:
    "demographics", "preferences", "preferred_pharmacies", "patient_consents", 
    "care_team", "parent_guardian", "addresses", "phone_numbers", "emails", "contacts"
    """

    # Name the event type you wish to run in response to
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PROFILE__SECTION_CONFIGURATION)

    def compute(self) -> list[Effect]:
        """This method gets called when an event of the type RESPONDS_TO is fired."""

        sections = [
            PatientProfileConfiguration.Payload(type=PatientProfileConfiguration.Section.PREFERENCES,
                                                             start_expanded=False),
            PatientProfileConfiguration.Payload(type=PatientProfileConfiguration.Section.DEMOGRAPHICS,
                                                             start_expanded=False),
            PatientProfileConfiguration.Payload(
                type=PatientProfileConfiguration.Section.PREFERRED_PHARMACIES, start_expanded=True),
            PatientProfileConfiguration.Payload(type=PatientProfileConfiguration.Section.PARENT_GUARDIAN,
                                                             start_expanded=False),
            PatientProfileConfiguration.Payload(type=PatientProfileConfiguration.Section.CONTACTS,
                                                start_expanded=True),
            PatientProfileConfiguration.Payload(type=PatientProfileConfiguration.Section.CARE_TEAM,
                                                             start_expanded=False),
            PatientProfileConfiguration.Payload(type=PatientProfileConfiguration.Section.TELECOM,
                                                             start_expanded=False),
            PatientProfileConfiguration.Payload(type=PatientProfileConfiguration.Section.ADDRESSES,
                                                             start_expanded=False),
            PatientProfileConfiguration.Payload(type=PatientProfileConfiguration.Section.PATIENT_CONSENTS,
                                                start_expanded=False),
        ]

        effect = PatientProfileConfiguration(sections=sections).apply()

        return [effect]
```

The `PatientProfileConfiguration` takes a single argument, `sections`,
which is expected to be a list at least one element long, filled with `PatientProfileConfiguration.Payload` objects. These are python typed dictionaries that expect a `PatientProfileConfiguration.Section` choice, which describes a section of the patient profile, and a `start_expanded` boolean, which determines if the fields in that section should be exposed by default. The `.apply()`
method returns a well-formed `Effect` object.

This effect is only used in response to the
`PATIENT_PROFILE__SECTION_CONFIGURATION` event. It does nothing in any
other context.

Values in the `PatientProfileConfiguration.Section` enum are:

| Constant | Description |
| -------- | ----------- |
| DEMOGRAPHICS | demographics |
| PREFERENCES | preferences |
| PREFERRED_PHARMACIES | preferred_pharmacies |
| PATIENT_CONSENTS | patient_consents |
| CARE_TEAM | care_team |
| PARENT_GUARDIAN | parent_guardian |
| ADDRESSES | addresses |
| TELECOM | telecom |
| CONTACTS | contacts |





<br/>
<br/>
<br/>

## Modals

The `LaunchModalEffect` class allows you to launch modals in Canvas, providing a flexible way to display content or navigate to external resources.

### Example Usage

```python
from canvas_sdk.effects import LaunchModalEffect, EffectType

class ModalEffectHandler:
    def compute(self):
        modal_effect = LaunchModalEffect(
            url="https://example.com/info",
            content=None,
            target=LaunchModalEffect.TargetType.DEFAULT_MODAL
        )
        return [modal_effect.apply()]
```

The `LaunchModalEffect` class has the following properties:

- **url**: A string containing the URL to load within the modal. If `content` is also specified, an error will be raised.
- **content**: A string containing the content to be displayed directly within the modal. If `url` is also provided, an error will be raised.
- **target**: Defines where the modal should be launched. Options include:
  - `DEFAULT_MODAL`: Opens the URL in a modal centered on the screen.
  - `NEW_WINDOW`: Opens the content in a new browser window.
  - `RIGHT_CHART_PANE`: Opens the URL in the right-hand pane of the patient chart.
  - `RIGHT_CHART_PANE_LARGE`: Like above, but a bit wider.


## Portal Landing Page Widgets

The `PortalWidget` class allows you to add widgets of various sizes to the patient portal landing page. You can fully customize your widgets or leverage ready-made widgets provided by Canvas, such as Appointments and Messaging.

### Example Usage

```python
from canvas_sdk.effects.widgets import PortalWidget

class PortalWidgetHandler:
    def compute(self):
        portal_widget = PortalWidget(
            url="https://example.com/info",
            size=PortalWidget.Size.COMPACT, 
            priority=25
        )
        return [portal_widget.apply()]
```

The `PortalWidget` class has the following properties:

- **url**: A string containing the URL to load within the widget. If either `content` or `component` is specified, an error will be raised.
- **content**: A string containing the content to be displayed directly within the widget. If either `url` or  `component` is provided, an error will be raised.
- **component**: Choose one of ready-made widgets made by Canvas. If either `url` or  `content` is provided, an error will be raised. The available ready-made widgets include:
  - `APPOINTMENTS`: Displays upcoming appointments.
  - `MESSAGING`: Enables quick messaging.
- **Size**: Determines the widget's layout on the frontend grid:
  - `EXPANDED`: Fills an entire row (12 columns).
  - `MEDIUM`: Occupies 8 columns.
  - `COMPACT`: Occupies 4 columns
- **priority**: This value is used to order the widgets within the patient portal. A lower number indicates a higher priority.

## Custom HTML and Django Templates

To facilitate the use of custom HTML, you can utilize the `render_to_string` utility from `canvas_sdk.templates` to render Django templates with a specified context. This allows for dynamic rendering of HTML that can be passed to a `LaunchModalEffect` or `PortalWidget`.

```python
def render_to_string(template_name: str, context: dict[str, Any] | None = None) -> str | None:
    """Load a template and render it with the given context.

    Args:
        template_name (str): The path to the template file, relative to the plugin package.
            If the path starts with a forward slash ("/"), it will be stripped during resolution.
        context (dict[str, Any] | None): A dictionary of variables to pass to the template
            for rendering. Defaults to None, which uses an empty context.

    Returns:
        str: The rendered template as a string.

    Raises:
        FileNotFoundError: If the template file does not exist within the plugin's directory
            or if the resolved path is invalid.
    """
```

#### Example Template

Consider a simple HTML file named `templates/custom_content.html`:
{% raw %}
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ heading }}</h1>
    <p>{{ message }}</p>
</body>
</html>
```
{% endraw %}

This template uses Django template placeholders like {% raw %} `{{ title }}`, `{{ heading }}`, and `{{ message }}` {% endraw %} to dynamically render content based on the provided context.

#### Rendering the Template in Python

Here’s how you can use the `render_to_string` utility to render the template and pass the resulting HTML to a `LaunchModalEffect` or `PortalWidget`:

```python
from canvas_sdk.effects import LaunchModalEffect
from canvas_sdk.effects.widgets import PortalWidget
from canvas_sdk.templates import render_to_string 

class ModalEffectHandler:
    def compute(self):
        # Define the context for the template
        context = {
            "title": "Welcome Modal",
            "heading": "Hello, User!",
            "message": "This is a dynamically rendered modal using Django templates."
        }

        # Render the HTML content using the template and context
        rendered_html = render_to_string("templates/custom_content.html", context)

        # Create a LaunchModalEffect with the rendered content
        modal_effect = LaunchModalEffect(
            content=rendered_html,
            target=LaunchModalEffect.TargetType.DEFAULT_MODAL
        )

        return [modal_effect.apply()]

class PortalWidgetHandler:
    def compute(self):
        # Define the context for the template
        context = {
            "title": "Welcome Modal",
            "heading": "Hello, User!",
            "message": "This is a dynamically rendered modal using Django templates."
        }

        # Render the HTML content using the template and context
        rendered_html = render_to_string("templates/custom_content.html", context)

        # Create a PortalWidget with the rendered content
        portal_widget = PortalWidget(
            content=rendered_html,
            size=PortalWidget.Size.COMPACT, 
            priority=25
        )

        return [portal_widget.apply()]
```

## Additional Configuration
To use URLs or custom scripts within the `LaunchModalEffect` or `PortalWidget`, additional security configurations must be specified in the `CANVAS_MANIFEST.json` file of your plugin.

- **Allowing URLs**: URLs specified in the **url** property must be added to the `url_permissions` section of the `CANVAS_MANIFEST.json` in order for the URL to load properly.
- **Allowing custom scripts**: If you need to load scripts from an external source, the URL for the script must be added to the `url_permissions` section of the `CANVAS_MANIFEST.json` and `'SCRIPTS'` must be in the permissions list.
- **Requesting microphone access**: If the site in your modal or widget needs microphone access, `'MICROPHONE'` must be in the URL's permissions list.
- **Allowing browser access to cookies from the iframe's origin**: If you want the loaded URL to access cookies for its domain, `'ALLOW_SAME_ORIGIN'` must be in the URL's permissions list. If the URL you're loading requires authentication, this will prevent your user from having to log in each time the modal is launched.

The URLs must match the format available [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy#host-source).

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "custom_html",
    "description": "...",
    "url_permissions": [
        {
            "url": "https://example.com/info",
            "permissions": ["ALLOW_SAME_ORIGIN", "MICROPHONE"]
        },
        {
            "url": "https://d3js.org/d3.v4.js",
            "permissions": ["SCRIPTS"]
        }
    ]
}
```
