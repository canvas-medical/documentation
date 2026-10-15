---
title: "Patient Chart Summary Custom Section"
slug: "patient-chart-summary-custom-section-effect"
excerpt: "Effect for rendering a custom section in the patient chart summary."
hidden: false
---

The `PatientChartSummaryCustomSection` effect allows plugin developers to supply the content for a custom section in the patient chart summary. It is returned by a [`PatientChartSummaryCustomSectionHandler`](/sdk/patient-chart-summary-custom-section-handler/) in response to a request for the section's content.

Content can be provided as an inline HTML string or as a URL to a hosted page. An icon must always be supplied; it is shown in the chart summary header when the section is collapsed.

Build a `PatientChartSummaryCustomSection` with the [attributes](#attributes) you want to set, then return its `apply()` from your handler.

## Methods

### apply() → Effect

Supplies the section's content.

- Exactly one of `content` or `url` is required.
- Exactly one of `icon` or `icon_url` is required.

Providing both fields in a pair, or neither, raises a `ValidationError`.

## Attributes

| Attribute  | Type            | Description                                                                                     | Required                         |
|------------|-----------------|-------------------------------------------------------------------------------------------------|----------------------------------|
| `content`  | `str` \| `None` | Inline HTML content to render in the section. Mutually exclusive with `url`.                    | Exactly one of `content` or `url` |
| `url`      | `str` \| `None` | URL of the page to load in the section iframe. Mutually exclusive with `content`.               | Exactly one of `content` or `url` |
| `icon`     | `str` \| `None` | Text or emoji displayed as the section icon when collapsed. Mutually exclusive with `icon_url`. | Exactly one of `icon` or `icon_url` |
| `icon_url` | `str` \| `None` | URL of an image to use as the section icon when collapsed. Mutually exclusive with `icon`.      | Exactly one of `icon` or `icon_url` |

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

Load the section content from a hosted endpoint. This is useful when the section is a standalone page served by a [Simple API](/sdk/handlers-simple-api/) handler.

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
