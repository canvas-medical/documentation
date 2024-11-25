---
title: "Chart Summary Configuration"
slug: "effect-chart-summary-configuration"
excerpt: "Rearrange or hide summary sections in a patient's chart."
hidden: false
---

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

| Constant | Description |
| -------- | ----------- |
| SOCIAL_DETERMINANTS | social_determinants |
| GOALS | goals |
| CONDITIONS | conditions |
| MEDICATIONS | medications |
| ALLERGIES | allergies |
| CARE_TEAMS | care_teams |
| VITALS | vitals |
| IMMUNIZATIONS | immunizations |
| SURGICAL_HISTORY | surgical_history |
| FAMILY_HISTORY | family_history |
| CODING_GAPS | coding_gaps |

<br/>
<br/>
<br/>
