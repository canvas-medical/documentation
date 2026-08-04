---
title: "Patient Chart Summary Custom Section"
slug: "patient-chart-summary-custom-section-effect"
excerpt: "Effect for rendering a custom section in the patient chart summary."
hidden: false
---

## Overview

The `PatientChartSummaryCustomSection` effect allows plugin developers to supply the content for a custom section in the patient chart summary. It is returned by a [`PatientChartSummaryCustomSectionHandler`](/sdk/patient-chart-summary-custom-section-handler/) in response to a request for the section's content.

Content can be provided as an inline HTML string or as a URL to a hosted page. An icon must always be supplied — it is shown in the chart summary header when the section is collapsed.

```python
from canvas_sdk.effects.patient_chart_summary_custom_section import PatientChartSummaryCustomSection
from canvas_sdk.templates import render_to_string


# Serve content as an inline HTML string
PatientChartSummaryCustomSection(
    content=render_to_string("templates/my_section.html"),
    icon="📋",
)

# Serve content from a hosted URL
PatientChartSummaryCustomSection(
    url="/plugin-io/api/my_plugin/my-section",
    icon_url="/plugin-io/api/my_plugin/icon.png",
)
```

## Structure

### Attributes

| Attribute  | Required                                 | Type            | Description                                                                                     |
|------------|------------------------------------------|-----------------|-------------------------------------------------------------------------------------------------|
| `content`  | required (if `url` is not provided)      | `str` \| `None` | Inline HTML content to render in the section. Mutually exclusive with `url`.                    |
| `url`      | required (if `content` is not provided)  | `str` \| `None` | URL of the page to load in the section iframe. Mutually exclusive with `content`.               |
| `icon`     | required (if `icon_url` is not provided) | `str` \| `None` | Text or emoji displayed as the section icon when collapsed. Mutually exclusive with `icon_url`. |
| `icon_url` | required (if `icon` is not provided)     | `str` \| `None` | URL of an image to use as the section icon when collapsed. Mutually exclusive with `icon`.      |

### Validation

Exactly one of `content` / `url` must be provided, and exactly one of `icon` / `icon_url` must be provided. Providing both fields in a pair or neither will raise a `ValidationError` when `.apply()` is called.

## Examples

### Inline HTML content

Return a rendered HTML template as the section content.

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

### URL-based content

Load the section content from a hosted endpoint. This is useful when the section is a standalone page served by a [Simple API](/sdk/simple-api/) handler.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_chart_summary_custom_section import PatientChartSummaryCustomSection
from canvas_sdk.handlers.patient_chart_summary_custom_section_handler import PatientChartSummaryCustomSectionHandler


class MySectionHandler(PatientChartSummaryCustomSectionHandler):
    SECTION_KEY = "my_section"

    def handle(self) -> list[Effect]:
        return [
            PatientChartSummaryCustomSection(
                url="/plugin-io/api/my_plugin/my-section",
                icon_url="/plugin-io/api/my_plugin/icon.png",
            ).apply()
        ]
```

### Passing data to the template

Use `render_to_string` with a context dictionary to inject dynamic data into the HTML template.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_chart_summary_custom_section import PatientChartSummaryCustomSection
from canvas_sdk.handlers.patient_chart_summary_custom_section_handler import PatientChartSummaryCustomSectionHandler
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data.patient import Patient


class MySectionHandler(PatientChartSummaryCustomSectionHandler):
    SECTION_KEY = "my_section"

    def handle(self) -> list[Effect]:
        patient = Patient.objects.get(id=self.target)

        return [
            PatientChartSummaryCustomSection(
                content=render_to_string(
                    "templates/my_section.html",
                    {"patient_name": patient.first_name},
                ),
                icon="📋",
            ).apply()
        ]
```
