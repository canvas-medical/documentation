---
title: "Customize your panel buttons"
guide_for:
- /sdk/layout-effect/
---

This guide is intended to help you customize which buttons are shown on the main page and the patient page.
It allows you to add, order, or hide specific buttons as needed.

## Getting Started

To achieve this, you’ll use the [PANEL_SECTIONS_CONFIGURATION](/sdk/events) event, which sends both the patient and the user attributes.

The event fires for both pages, and Canvas applies the sections you return to whichever page sent it. Check `self.target` to tell the pages apart: it holds the patient on the patient page and is empty on the global (main) page. Return a configuration only for the page you want to change. If a handler returns a global list for every event, the patient page shows only those buttons, which hides Protocols and Commands.


## Defining the Sections

In the SDK, you’ll use the [PanelConfiguration](/sdk/layout-effect/#panel-configuration) effect. This effect takes in the sections you want to display and specifies the page where they should appear.

You’ll use:
- PanelPatientSection – for sections shown on the patient page
- PanelGlobalSection – for sections shown on the main (global) page

The SDK checks that every section you list belongs to the `page` you set. That check doesn't choose where the buttons appear; the event does.

Any button you leave out of `sections` is hidden. On the patient page, this includes the Protocols button, so add `PanelPatientSection.PROTOCOL` to your list if your users need it.

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