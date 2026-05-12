---
title: 'Customize Patient Portal with Widgets'
slug: 'example-portal-customization-widgets'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_portal_plugin' target='_blank'>View the source</a> for this plugin on GitHub." %}

## Description

The Patient Portal Widgets Plugin provides various widgets for the patient portal.
The plugin listens to the `PATIENT_PORTAL__WIDGET_CONFIGURATION` event.


## Widgets

### Header Widget

The Header Widget displays the patient's preferred name and has quick links for messaging and scheduling.

For more, visit the [Canvas SDK documentation](https://docs.canvasmedical.com/sdk/data-patient/)


### Care Team Widget

It is used to display a compact widget in the Patient Portal that lists the
active care team members for a patient.

It renders a scrollable list in a compact plugin format of all active members.

For more information, visit the [Canvas SDK documentation](https://docs.canvasmedical.com/sdk/data-care-team/).


### Footer Widget

The Footer Widget displays the support contact information for the patient.


## Secrets

The Patient Portal Plugin uses the following secrets:

- `BACKGROUND_COLOR`: The background color for the widgets. Defaults to `#17634d`.
- `EMERGENCY_CONTACT`: The emergency contact information. Defaults to `1-888-555-5555`.


In order to deal with `SECRETS` take a look at the
[SDK documentation](https://docs.canvasmedical.com/sdk/secrets/).


## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "patient_portal_plugin",
    "description": "Patient Portal Plugin for Canvas",
    "components": {
        "handlers": [
            {
                "class": "patient_portal_plugin.handlers.patient_portal_handler:PatientPortalHandler",
                "description": "The handler that listens for the patient portal `PATIENT_PORTAL__WIDGET_CONFIGURATION` and responds with the patient portal widgets"
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "variables": [
        {"name": "BACKGROUND_COLOR", "sensitive": false},
        {"name": "EMERGENCY_CONTACT", "sensitive": false}
    ],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## templates/

### care_team_widget.html

### header_widget.html

### footer_widget.html

## handlers/

### patient_portal_handler.py

**Purpose**

The code defines a handler, PatientPortalHandler, for the Canvas Medical SDK that renders custom widgets on the patient portal within Canvas. It listens for a specific widget configuration event and responds by displaying a set of widgets (header, care team, and footer) with certain configurable properties.

**Event Handling**

The handler is triggered (via RESPONDS_TO) when the event type PATIENT_PORTAL__WIDGET_CONFIGURATION occurs. When Canvas requests portal widget configuration for a patient, this handler gets called.

**Widgets Produced**

- **Header Widget**:
  Collects basic patient information (first name, last name, etc.), constructs a "preferred full name," and passes it to an HTML template along with a configurable background color (using either a secret or a default).
- **Care Team Widget**:
  Fetches the patient's active care team members. For each member, gathers name components, professional role, profile photo URL, and composes formatted display strings. This list is rendered in a compact widget, styled with the background color as a title color.
- **Footer Widget**:
  Renders a footer using a background color and an emergency contact number, both customizable via secrets, falling back to sensible defaults if not specified.

**Widget Rendering**

For each widget, an appropriate HTML template is rendered with the relevant payload/context, and the widget is then wrapped as a PortalWidget with defined size and priority. These effects are returned as a list which the Canvas platform uses to display each widget on the patient portal.

**Customization and Defaults**

Two elements are customizable via the plugin’s secrets dictionary:
- BACKGROUND_COLOR: Sets the color for visual elements (widgets, titles).
- EMERGENCY_CONTACT: Sets the emergency contact number in the footer.

If these are not provided, default values are used:
- DEFAULT_BACKGROUND_COLOR = "#17634d"
- DEFAULT_EMERGENCY_CONTACT = "1-888-555-5555"

**Summary**

This file enables a Canvas plugin to inject and style custom patient-facing widgets: a personalized header, a care team overview, and an emergency contact panel, all triggered when the platform requests configuration for the patient portal widgets. It leverages data models and template rendering of the Canvas SDK, with runtime customization via plugin secrets.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.widgets import PortalWidget
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data import Patient
from canvas_sdk.v1.data.care_team import CareTeamMembership, CareTeamMembershipStatus


# Inherit from BaseHandler to properly get registered for events
class PatientPortalHandler(BaseHandler):
    """Handler responsible for rendering a patient portal widgets."""

    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__WIDGET_CONFIGURATION)

    # Default background and title color for the portal's widgets if not provided in secrets
    DEFAULT_BACKGROUND_COLOR = "#17634d"

    # Default emergency contact number if not provided in secrets
    DEFAULT_EMERGENCY_CONTACT = "1-888-555-5555"

    def compute(self) -> list[Effect]:
        """This method gets called when an event of the type RESPONDS_TO is fired."""
        return [
            self.header_widget,
            self.care_team_widget,
            self.footer_widget,
        ]

    @property
    def header_widget(self) -> Effect:
        """Constructs the header widget for the patient portal."""
        # Get the patient needed fields to generate the preferred full name
        patient = Patient.objects.only("first_name", "last_name", "suffix", "nickname").get(id=self.target)

        payload = {
            "preferred_full_name": patient.preferred_full_name,
            "background_color": self.background_color,
        }

        header_widget = PortalWidget(
            content=render_to_string("templates/header_widget.html", payload),
            size=PortalWidget.Size.EXPANDED,
            priority=10,
        )

        return header_widget.apply()

    @property
    def care_team_widget(self) -> Effect:
        """Constructs the care team widget for the patient portal."""
        patient_care_team = CareTeamMembership.objects.values(
            "staff__first_name",
            "staff__last_name",
            "staff__prefix",
            "staff__suffix",
            "staff__photos__url",
            "role_display",
        ).filter(
            patient__id=self.target,
            status=CareTeamMembershipStatus.ACTIVE,
        )

        care_team = []
        for member in patient_care_team:
            # Aliasing the member's name components for clarity
            name = f"{member['staff__first_name']} {member['staff__last_name']}"
            prefixed_name = f"{member['staff__prefix']} " if member['staff__prefix'] else name
            professional_name = f"{prefixed_name}, {member['staff__suffix']}" if member['staff__suffix'] else prefixed_name
            photo_url = member['staff__photos__url']
            role = member['role_display']

            care_team.append(
                {
                    "name": name,
                    "prefixed_name": prefixed_name,
                    "professional_name": professional_name,
                    "photo_url": photo_url,
                    "role": role,
                }
            )

        payload = {
            "care_team": care_team,
            "title_color": self.background_color,
        }

        care_team_widget = PortalWidget(
            content=render_to_string("templates/care_team_widget.html", payload),
            size=PortalWidget.Size.COMPACT,
            priority=11,
        )

        return care_team_widget.apply()

    @property
    def footer_widget(self) -> Effect:
        """This method gets called when an event of the type RESPONDS_TO is fired."""
        return PortalWidget(
            content=render_to_string("templates/footer_widget.html", {
                "background_color": self.background_color,
                "emergency_contact": self.emergency_contact,
            }),
            size=PortalWidget.Size.EXPANDED,
            priority=12,
        ).apply()

    @property
    def background_color(self) -> str:
        """Get the background color from secrets, defaulting to a specific color if not set."""
        return self.secrets.get("BACKGROUND_COLOR") or self.DEFAULT_BACKGROUND_COLOR

    @property
    def emergency_contact(self) -> str:
        """Get the emergency contact from secrets, defaulting to a specific contact if not set."""
        return self.secrets.get("EMERGENCY_CONTACT") or self.DEFAULT_EMERGENCY_CONTACT
```

<br/>
<br/>
<br/>
