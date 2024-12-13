---
title: "Layout Effects"
slug: "layout-effect"
excerpt: "Rearrange or hide sections in a patient's profile o chart."
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

