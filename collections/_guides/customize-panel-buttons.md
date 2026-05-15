---
title: "Customize your panel buttons"
guide_for:
- /sdk/layout-effect/
---

This guide is intended to help you customize which buttons are shown on the main page and the patient page.
It allows you to add, order, or hide specific buttons as needed.

## Getting Started

To achieve this, you’ll use the [PANEL_SECTIONS_CONFIGURATION](/sdk/events) event, which sends both the patient and the user attributes.

If you need to identify where the event is coming from, you can check if the patient attributes are present — on the global (main) page, the patient will be empty.


## Defining the Sections

In the SDK, you’ll use the [PanelConfiguration](/sdk/layout-effect/#panel-configuration) effect. This effect takes in the sections you want to display and specifies the page where they should appear.

You’ll use:
- PanelPatientSection – for sections shown on the patient page
- PanelGlobalSection – for sections shown on the main (global) page

The SDK has built-in safeguards to prevent you from mixing them up or placing a section on the wrong page.

That’s It!

Once you apply the effect, your panel is configured — go check your page to see the changes in action!


## The Complete Example

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.panel_configuration import PanelConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler

class CustomizePatientSection(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PANEL_SECTIONS_CONFIGURATION)

    def compute(self) -> list[Effect]:
        patient = self.target
        # user = self.context["user"]

        if patient:
            return [PanelConfiguration(sections=[
                PanelConfiguration.PanelPatientSection.REFILL_REQUEST,
                PanelConfiguration.PanelPatientSection.LAB_REPORT,
                PanelConfiguration.PanelPatientSection.CHANGE_REQUEST,
                PanelConfiguration.PanelPatientSection.TASK,
            ], page=PanelConfiguration.Page.PATIENT if patient else PanelConfiguration.Page.GLOBAL).apply()]
        else:
            return []


class CustomizeGlobalSection(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PANEL_SECTIONS_CONFIGURATION)

    def compute(self) -> list[Effect]:
        patient = self.target
        # user = self.context["user"]

        if not patient:
            return [PanelConfiguration(sections=[
                PanelConfiguration.PanelGlobalSection.LAB_REPORT,
                PanelConfiguration.PanelGlobalSection.TASK,
                PanelConfiguration.PanelGlobalSection.CHANGE_REQUEST,
            ], page=PanelConfiguration.Page.PATIENT if patient else PanelConfiguration.Page.GLOBAL).apply()]
        else:
            return []
```