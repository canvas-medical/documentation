---
title: "Patient Chart Summary Custom Section Handler"
slug: "patient-chart-summary-custom-section-handler"
excerpt: "Handler for serving content to custom patient chart summary sections."
hidden: false
---

The `PatientChartSummaryCustomSectionHandler` is the base class for implementing custom sections in the patient chart summary. When Canvas needs to render a custom section, it fires an event that this handler intercepts, and the handler returns a [`PatientChartSummaryCustomSection`](/sdk/patient-chart-summary-custom-section-effect/) effect with the content to display.

## Overview

Custom chart summary sections are registered through [`PatientChartSummaryConfiguration`](/sdk/patient-chart-summary-configuration-effect/) and served by a `PatientChartSummaryCustomSectionHandler` subclass. Each handler is responsible for exactly one section, identified by its `SECTION_KEY`.

To implement a custom section you need two things:

1. A `PatientChartSummaryConfiguration` handler that includes the section in the layout.
2. A `PatientChartSummaryCustomSectionHandler` subclass that returns the section content.

## Creating a Custom Section Handler

Subclass `PatientChartSummaryCustomSectionHandler` and:

1. Set `SECTION_KEY` to the unique identifier of your section. This must match the key used in `PatientChartSummaryConfiguration.CustomSection`.
2. Implement `handle()` to return a `PatientChartSummaryCustomSection` effect.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_chart_summary_custom_section import PatientChartSummaryCustomSection
from canvas_sdk.handlers.patient_chart_summary_custom_section_handler import PatientChartSummaryCustomSectionHandler
from canvas_sdk.templates import render_to_string


class MySectionHandler(PatientChartSummaryCustomSectionHandler):
    SECTION_KEY = "my_section"

    def handle(self) -> list[Effect]:
        return [
            PatientChartSummaryCustomSection(
                content=render_to_string("templates/my_section.html"),
                icon="📋",
            ).apply()
        ]
```

### Required

- **`SECTION_KEY`**
  A unique string identifier for the section. Must match the key passed to `PatientChartSummaryConfiguration.CustomSection`. Omitting or leaving it empty will raise an `ImproperlyConfigured` error when the plugin loads.

- **`handle()`**
  Called when Canvas requests the content for this section. Must return a list containing a single `PatientChartSummaryCustomSection` effect.

## Registering the Section

A custom section handler alone is not enough — the section must also be included in the chart summary layout. Use `PatientChartSummaryConfiguration` to declare which sections appear in the chart summary and in what order.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_chart_summary_configuration import PatientChartSummaryConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MySummaryConfiguration(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION)]

    def compute(self) -> list[Effect]:
        return [
            PatientChartSummaryConfiguration(
                sections=[
                    PatientChartSummaryConfiguration.CustomSection(name="my_section"),
                    PatientChartSummaryConfiguration.Section.MEDICATIONS,
                    PatientChartSummaryConfiguration.Section.CONDITIONS,
                ]
            ).apply()
        ]
```

Both handlers must be registered in `CANVAS_MANIFEST.json`.

## Full Example

The following example shows a complete plugin with a custom section that displays a list of items fetched from command metadata.

### `handlers/my_section.py`

```python
import json

from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_chart_summary_custom_section import PatientChartSummaryCustomSection
from canvas_sdk.effects.patient_chart_summary_configuration import PatientChartSummaryConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.handlers.patient_chart_summary_custom_section_handler import PatientChartSummaryCustomSectionHandler
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data.command import CommandMetadata


class MySectionHandler(PatientChartSummaryCustomSectionHandler):
    SECTION_KEY = "my_section"

    def handle(self) -> list[Effect]:
        entries = (
            CommandMetadata.objects.filter(
                key="my_section",
                command__patient__id=self.target,
            )
            .order_by("created")
        )

        items = []
        for entry in entries:
            try:
                items.append(json.loads(entry.value))
            except (json.JSONDecodeError, TypeError):
                items.append({"title": entry.value})

        return [
            PatientChartSummaryCustomSection(
                content=render_to_string("templates/my_section.html", {"items": items}),
                icon="📋",
            ).apply()
        ]


class MySummaryConfiguration(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION)]

    def compute(self) -> list[Effect]:
        return [
            PatientChartSummaryConfiguration(
                sections=[
                    PatientChartSummaryConfiguration.CustomSection(name="my_section"),
                    PatientChartSummaryConfiguration.Section.MEDICATIONS,
                    PatientChartSummaryConfiguration.Section.CONDITIONS,
                ]
            ).apply()
        ]
```

### `templates/my_section.html`

```html
<ul>
  {% for item in items %}
    <li>{{ item.title }}</li>
  {% empty %}
    <li>No items on record.</li>
  {% endfor %}
</ul>
```

### `CANVAS_MANIFEST.json`

```json
{
  "components": {
    "handlers": [
      {
        "class": "my_plugin.handlers.my_section:MySectionHandler",
        "description": "Serves content for the My Section custom chart section"
      },
      {
        "class": "my_plugin.handlers.my_section:MySummaryConfiguration",
        "description": "Configures the chart summary layout to include My Section"
      }
    ]
  }
}
```

## Accessing Patient Data

The patient key is available via `self.target`. Use it to scope database queries to the current patient.

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id=self.target)
```
