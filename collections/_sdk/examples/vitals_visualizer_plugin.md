---
title: 'Vitals Visualizer'
slug: 'example-vitals_visualizer_plugin'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/vitals_visualizer_plugin' target='_blank'>View the source</a> for this plugin on GitHub." %}


A Canvas plugin that displays a "Visualize" button in the vitals section of the chart summary and shows interactive vital signs visualizations.

## Structure

```
vitals_visualizer_plugin/
├── handlers/
│   ├── __init__.py
│   ├── vitals_button.py      # Action button handler
│   └── vitals_api.py         # API endpoint with visualization
├── templates/
│   └── vitals_visualization.html # HTML template for visualization UI
├── CANVAS_MANIFEST.json      # Plugin configuration
└── README.md                 # Documentation
```

## Features

- Adds a "Visualize" button to the vitals section of the chart summary
- When clicked, opens a modal in the right chart pane displaying:
  - Dropdown selector for vital signs (weight, body temperature, o2sat)
  - Interactive line graph with modern styling and tooltips
  - Tabular display of the same data below the chart
  - Shows all historical vital signs data

## Vital Signs Supported

- **Weight**: Patient weight measurements over time
- **Body Temperature**: Temperature readings with different measurement sites
- **Oxygen Saturation (O2Sat)**: Oxygen saturation percentage readings

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.1.0",
    "name": "vitals_visualizer_plugin",
    "description": "A plugin that adds visualization capabilities to patient vital signs in the chart summary",
    "components": {
        "protocols": [
            {
                "class": "vitals_visualizer_plugin.handlers.vitals_button:VitalsVisualizerButton",
                "description": "A button that opens vitals visualization modal",
                "data_access": {
                    "event": "SHOW_CHART_SUMMARY_VITALS_SECTION_BUTTON",
                    "read": ["v1.Observation"],
                    "write": []
                }
            },
            {
                "class": "vitals_visualizer_plugin.handlers.vitals_api:VitalsVisualizerAPI",
                "description": "API endpoint that serves vitals visualization data and UI",
                "data_access": {
                    "event": "",
                    "read": ["v1.Observation"],
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
    "tags": [],
    "license": "NONE",
    "readme": "./README.md"
}
```

## templates/

### vitals_visualization.html

## handlers/

### vitals_api.py

**Summary of What the Code Does**

The `vitals_api.py` file defines a class-based API endpoint called `VitalsVisualizerAPI` for a Canvas Medical plugin. This endpoint provides both a user interface (HTML) and data (as JSON) for visualizing patient vitals—specifically weight, body temperature, and oxygen saturation.

**Key Functionalities**

- **API Endpoint**:  
  The endpoint is accessed at `/visualize`, and requires staff authentication via `StaffSessionAuthMixin`.
  
- **Request Handling**:  
  The main entry point is the `get()` method, which expects a `patient_id` as a query parameter.
    - If `patient_id` is missing, it returns a 400 JSON error response.
    - If present, it fetches and compiles the patient's vital sign data, then generates and returns an HTML interface for visualization.

- **Vitals Data Extraction**:  
  The `_get_vitals_data(patient_id)` method:
    - Queries Canvas Medical's `Observation` resource for the specified patient.
    - Filters for observations in the "vital-signs" category that are not deleted, not entered in error, and are not “Vital Signs Panel” summary records.
    - Extracts individual observations for:
        - **Weight** (converting from ounces to pounds),
        - **Body Temperature** (with default units °F if missing),
        - **Oxygen Saturation** (with default units % if missing).
    - Organizes the data into a dictionary keyed by vital sign name, each containing a list of timestamped values.
        
- **HTML Visualization Rendering**:  
  The `_generate_visualization_html(vitals_data)` method:
    - Serializes the vitals data as JSON.
    - Passes it as context to a template called `vitals_visualization.html` for rendering the UI.
  
- **Error Handling and Logging**:  
  All major steps have try/except blocks, logging errors and returning JSON error responses if needed.

**How the Components Work Together**

- The endpoint provides a combined UI/data interface for staff to review prescribed vitals over time for a selected patient.
- The code is built for integration into the Canvas Medical system utilizing their SDK, data models, and permission system.
- All HTML and logic for visualization are rendered server-side using a templating mechanism.

**Dependencies and Assumptions**

- Depends on `Observation` model/data from Canvas Medical's API SDK.
- Uses Canvas SDK facilities for routing, API responses, session authentication, and template rendering.
- Relies on templates being in the `templates/` folder, specifically one for vitals visualization.
- Expects a structured logging setup.

**Returned Data Types**

- Templated HTML (for visualization) or JSON (for errors), wrapped in Canvas SDK response objects (`HTMLResponse`, `JSONResponse`).

```python
import json
from typing import Any, Dict, List

from canvas_sdk.effects.simple_api import HTMLResponse, JSONResponse
from canvas_sdk.handlers.simple_api import SimpleAPIRoute, StaffSessionAuthMixin
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data import Observation
from logger import log


class VitalsVisualizerAPI(StaffSessionAuthMixin, SimpleAPIRoute):
    """API endpoint that serves vitals visualization data and UI."""

    PATH = "/visualize"

    def get(self) -> list[HTMLResponse | JSONResponse]:
        """Return the vitals visualization UI and data."""
        patient_id = self.request.query_params.get("patient_id")

        if not patient_id:
            return [JSONResponse({"error": "Patient ID is required"}, status_code=400)]

        try:
            vitals_data = self._get_vitals_data(patient_id)
            html_content = self._generate_visualization_html(vitals_data)
            return [HTMLResponse(content=html_content)]

        except Exception as e:
            log.error(f"Error in VitalsVisualizerAPI: {str(e)}")
            return [JSONResponse({"error": str(e)}, status_code=500)]

    def _get_vitals_data(self, patient_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get vitals data for the patient using Canvas vitals structure."""

        try:
            # Get individual vital observations from vital signs panels
            vital_observations = (
                Observation.objects.for_patient(patient_id)
                .filter(
                    category="vital-signs",
                    effective_datetime__isnull=False,
                    deleted=False,
                )
                .exclude(name="Vital Signs Panel")
                .exclude(entered_in_error__isnull=False)
                .select_related("is_member_of")
                .order_by("effective_datetime")
            )

            vitals_data = {
                "weight": [],
                "body_temperature": [],
                "oxygen_saturation": [],
            }

            for obs in vital_observations:
                if not obs.value or obs.name in ["note", "pulse_rhythm"]:
                    continue

                if obs.name == "weight":
                    try:
                        value_oz = float(obs.value)
                        value_lbs = value_oz / 16
                        vitals_data["weight"].append(
                            {
                                "date": obs.effective_datetime.isoformat(),
                                "value": round(value_lbs, 1),
                                "units": "lbs",
                            }
                        )
                    except (ValueError, TypeError):
                        continue

                elif obs.name == "body_temperature":
                    try:
                        value = float(obs.value)
                        vitals_data["body_temperature"].append(
                            {
                                "date": obs.effective_datetime.isoformat(),
                                "value": value,
                                "units": obs.units or "°F",
                            }
                        )
                    except (ValueError, TypeError):
                        continue

                elif obs.name == "oxygen_saturation":
                    try:
                        value = float(obs.value)
                        vitals_data["oxygen_saturation"].append(
                            {
                                "date": obs.effective_datetime.isoformat(),
                                "value": value,
                                "units": obs.units or "%",
                            }
                        )
                    except (ValueError, TypeError):
                        continue

            return vitals_data

        except Exception as e:
            log.error(f"Error collecting vitals data: {str(e)}")
            return {"weight": [], "body_temperature": [], "oxygen_saturation": []}

    def _generate_visualization_html(
        self, vitals_data: Dict[str, List[Dict[str, Any]]]
    ) -> str:
        """Generate the HTML for the vitals visualization using template."""
        context = {"vitals_data": json.dumps(vitals_data)}
        return render_to_string("templates/vitals_visualization.html", context)
```

### vitals_button.py

**Purpose**

The code defines a custom action button for the Canvas Medical application. The button, labeled "Visualize," appears in the chart summary's vitals section for a patient.

**Class Details**

- The class `VitalsVisualizerButton` inherits from `ActionButton`.
- It specifies metadata such as title ("Visualize"), a unique key (`vitals_visualizer_button`), the section of the UI where it appears (vitals summary), and its priority (1).

**Functionality**

- When a user clicks the button, the `handle` method is triggered.
- This method constructs a URL to an API endpoint for visualizing vitals: `/plugin-io/api/vitals_visualizer_plugin/visualize?patient_id=<id>`, where `<id>` is the current patient ID.
- The button initiates a `LaunchModalEffect`, opening a large modal on the right side of the chart pane with the title "Vitals Visualization".
- The modal displays the contents served by the constructed URL (likely a vitals graph or dashboard).

**Integration with Canvas SDK**

- Uses SDK classes:
    - `ActionButton` for button behaviors and placement.
    - `LaunchModalEffect` to open a modal window within the Canvas UI.
    - The effect is returned in a list, as required by the SDK’s handler pattern.

**Summary**

This file adds a "Visualize" button to the patient chart's vitals section, which, when clicked, opens a modal with a visual representation of the patient’s vitals data, using the Canvas plugin and effect framework.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.action_button import ActionButton


class VitalsVisualizerButton(ActionButton):
    """A button that opens the vitals visualization modal."""
    
    BUTTON_TITLE = "Visualize"
    BUTTON_KEY = "vitals_visualizer_button"
    BUTTON_LOCATION = ActionButton.ButtonLocation.CHART_SUMMARY_VITALS_SECTION
    PRIORITY = 1
    
    def handle(self) -> list[Effect]:
        """Handle button click by opening vitals visualization modal."""
        # The API endpoint will be at /plugin-io/api/vitals_visualizer_plugin/visualize
        # We need to pass the patient ID in the URL
        patient_id = self.target
        
        return [
            LaunchModalEffect(
                url=f"/plugin-io/api/vitals_visualizer_plugin/visualize?patient_id={patient_id}",
                target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE_LARGE,
                title="Vitals Visualization"
            ).apply()
        ]
```

### \___init__.py

This file is blank.

<br/>
<br/>
<br/>
