---
title: "How to group items on a patient chart section"
guide_for:
- /sdk/events/
- /sdk/effects/
---

This guide explains how to group items on a patient chart section. With this, you can define custom groups to organize medications, conditions, or detected issues.

Currently, this is supported for the Conditions, Medications, and Detected Issues sections.

## What you'll learn:

- Use the [`PatientChartGroup`](/sdk/patient-chart-group-effect) effect to group items in a section by priority.
- Group conditions based on ICD-10 code ranges
- Group detected issues (such as coding gaps) by custom criteria

## Patient Chart Group

The `PatientChartGroup` effect allows you to group items in a patient chart section. You can define multiple groups with a name, priority, and the items that belong to each group.

#### 3. The plugin

Here’s an example of a plugin that groups conditions based on their codes - here we are creating a "Psychiatry" group for ICD-10 codes F01-F99 and R45.x and placing all matching conditions in that group.

```python

from canvas_sdk.effects.patient_chart_group import PatientChartGroup
from canvas_sdk.effects import Effect
from canvas_sdk.effects.group import Group
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.commands.constants import CodeSystems

class Protocol(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART__CONDITIONS)

    def compute(self) -> list[Effect]:
        groups: dict[str, Group] = {}
        groups.setdefault("Psychiatry", Group(priority=100, items=[], name="Psychiatry"))

        for condition in self.event.context:
           for coding in condition["codings"]:
               if coding["system"] == CodeSystems.ICD10 and ("F01" <= coding["code"] <= "F99" or coding["code"].startswith("R45.")):
                   groups["Psychiatry"].items.append(condition)
                   break

        return [PatientChartGroup(items=groups).apply()]

```

#### 4. The Output

Below, you can see how it will appear in the app.

<div style="max-width: 100%"><img style="max-width: 100%" src="/assets/images/patient-chart-group.png" alt="patient chart group" /></div>

## Grouping Detected Issues

You can also group detected issues, such as coding gaps, using the same approach. Here's an example that groups detected issues by their status or other criteria:

```python
from canvas_sdk.effects.patient_chart_group import PatientChartGroup
from canvas_sdk.effects import Effect
from canvas_sdk.effects.group import Group
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler

class GroupDetectedIssues(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART__DETECTED_ISSUES)

    def compute(self) -> list[Effect]:
        groups: dict[str, Group] = {}
        groups.setdefault("High Priority", Group(priority=200, items=[], name="High Priority"))
        groups.setdefault("Standard", Group(priority=100, items=[], name="Standard"))

        for detected_issue in self.event.context:
            # Group by custom logic - for example, based on evidence or other attributes
            # Note: The context for detected issues contains only the "id" field
            # You may need to query additional data using the SDK if needed

            # Example: place first 5 in high priority, rest in standard
            if len(groups["High Priority"].items) < 5:
                groups["High Priority"].items.append(detected_issue)
            else:
                groups["Standard"].items.append(detected_issue)

        return [PatientChartGroup(items=groups).apply()]
```

**Note:** The context structure for detected issues differs from conditions and medications. The `PATIENT_CHART__DETECTED_ISSUES` event context includes only the `id` field for each detected issue. If you need additional information (such as evidence, status, or code) to determine grouping logic, you'll need to query the detected issue data using the Canvas SDK's data models.
