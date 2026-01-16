---
title: "Protocol Card"
slug: "effect-protocol-cards"
excerpt: "Calls to action in a patient's chart, commonly used for decision support intervention."
hidden: false
---

Protocol cards appear on the right-hand-side of a patient's chart, and can be accessed by clicking on the Protocols filter button in the filter menu.

{:refdef: style="text-align: center;"}
![protocol card](/assets/images/protocol-card.png){:width="95%"}
{: refdef}

A Protocol card consists of three main parts:

- A title, which appears at the top in bold
- A narrative, which appears just below the title to add any additional clarifying information
- A list of recommendations, which each have a title and optionally a button that can either:
  - open a new tab and navigate to another site
  - insert commands into a note

| Name               | Type                                    | Required                                     | Description                                                                                                                                        |
| :----------------- | :-------------------------------------- | :------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| `patient_id`       | _string_                                | `true` (if `patient_filter` is not included) | The id of the [patient](/sdk/data-patient/)                                                                                                        |
| `patient_filter`   | _dict_                                  | `true` (if `patient_id` is not included)     | Patient queryset filters to apply the effect to multiple patients. For example, `{"active": True}` will apply to the effect to all active patients |
| `key`              | _string_                                | `true`                                       | A unique identifier for the protocol card                                                                                                          |
| `title`            | _string_                                | `true`                                       | The title for the protocol card, which appears at the top in bold                                                                                  |
| `narrative`        | _string_                                | `false`                                      | The narrative for the protocol card, which appears just below the title                                                                            |
| `can_be_snoozed`   | _boolean_                               | `false`                                      | Whether the protocol card can be snoozed, defaults to `false`                                                                                      |
| `status`           | [Status](#status)                       | `false`                                      | The status of the protocol card, defaults to `Status.DUE`                                                                                          |
| `recommendations`  | list[[Recommendation](#recommendation)] | `false`                                      | The recommendations to appear in the protocol card                                                                                                 |
| `feedback_enabled` | _boolean_                               | `false`                                      | Whether users can provide feedback for the protocol card in Settings, defaults to `false`                                                          |
| `due_in`           | _integer_                               | `false`                                      | The number of days until the protocol card will be considered due for the patient, defaults to `-1` for already due                                |
|                    |                                         |                                              |                                                                                                                                                    |

### Recommendation

| Attribute  | Type                             | Required | Description                           |
|:-----------|:---------------------------------|:---------|:--------------------------------------|
| `title`    | _string_                         | `true`   | The description of the recommendation |
| `button`   | _string_                         | `false`  | The text to appear on the button      |
| `href`     | _string_                         | `false`  | The url for the button to navigate to |
| `commands` | list[[Command](#/sdk/commands/)] | `false`  | The commands to be inserted           |

### Status

| Enum             | Value          |
| :--------------- | :------------- |
| `DUE`            | due            |
| `SATISFIED`      | satisfied      |
| `NOT_APPLICABLE` | not_applicable |
| `PENDING`        | pending        |
| `NOT_RELEVANT`   | not_relevant   |
|                  |                |

To include a command recommendation you can:
- import the command from the [commands module](/sdk/commands/), instantiate the command with all the values you wish to populate, and then call `.recommend(title: str = "", button: str | None)` on the command to generate the recommendation that you can append to the protocol card's recommendations. Keep in mind that, at the moment, not all commands are supported for command insertion. See [below](#supported-commands) for the list of supported commands.
- instantiate the command as above, and then pass it in a list to the `commands` attribute of a recommendation.

</br>
</br>

For non-command recommendations, you can either use the `Recommendation` class, or the `.add_recommendation(title: str = "", button: str = "", href: str | None)` method on the protocol card.

**Example**:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from datetime import date
from canvas_sdk.effects.protocol_card import ProtocolCard, Recommendation
from canvas_sdk.commands import DiagnoseCommand, PlanCommand


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self):
        diagnose = DiagnoseCommand(
            icd10_code="I10",
            background="feeling bad for many years",
            approximate_date_of_onset=date(2020, 1, 1),
            today_assessment="still not great",
        )
        
        plan = PlanCommand(
            narrative="Follow up in 2 weeks",
        )
        
        p = ProtocolCard(
            patient_id=self.target,
            key="testing-protocol-cards",
            title="This is a ProtocolCard title",
            narrative="this is the narrative",
            status=ProtocolCard.Status.DUE,
            recommendations=[
              Recommendation(title="this recommendation has no action, just words!"),
              Recommendation(title="this recommendation inserts multiple commands", button="add commands", commands=[diagnose, plan])
            ],
        )

        p.add_recommendation(
            title="this is a recommendation", button="go here", href="https://canvasmedical.com/"
        )

        p.recommendations.append(diagnose.recommend(title="this inserts a diagnose command"))
        p.recommendations.append(title="new recommendation", button="start", commands=[diagnose])

        return [p.apply()]

```

To apply the effect to all active patients on plugin create and plugin update, you would include the plugin create and update events in `RESPONDS_TO`. And when responding to one of the plugin events you would use `patient_filter` instead of `patient_id` for the ProtocolCard.

```python
from canvas_sdk.effects.protocol_card import ProtocolCard, Recommendation
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from datetime import date
from canvas_sdk.effects.protocol_card import ProtocolCard, Recommendation
from canvas_sdk.commands import DiagnoseCommand


class Protocol(BaseProtocol):
    RESPONDS_TO = [
        EventType.Name(EventType.PATIENT_UPDATED),
        EventType.Name(EventType.PLUGIN_CREATED),
        EventType.Name(EventType.PLUGIN_UPDATED),
    ]

    def compute(self):
        p = ProtocolCard(
            key="testing-protocol-cards",
            title="This is a ProtocolCard title",
            narrative="this is the narrative",
            can_be_snoozed=True,
            recommendations=[
                Recommendation(title="this recommendation has no action, just words!")
            ],
        )
        p.add_recommendation(
            title="this is a recommendation", button="go here", href="https://canvasmedical.com/"
        )

        diagnose = DiagnoseCommand(
            icd10_code="I10",
            background="feeling bad for many years",
            approximate_date_of_onset=date(2020, 1, 1),
            today_assessment="still not great",
        )
        p.recommendations.append(diagnose.recommend(title="this inserts a diagnose command"))

        if self.event.type in [EventType.PLUGIN_CREATED, EventType.PLUGIN_UPDATED]:
            p.patient_filter = {"active": True}
        else:
            p.patient_id = self.target

        return [p.apply()]

```

### Supported Commands

The following commands from the [commands module](/sdk/commands/) are currently supported for insertion from Protocol Cards:

- Allergy
- Assess
- Diagnose
- FollowUp
- Goal
- HistoryOfPresentIllness
- Image
- Immunize
- Instruct
- LabOrder
- MedicationStatement
- Perform
- Plan
- Prescribe
- Questionnaire
- ReasonForVisit
- Refer
- StructuredAssessment
- Task
- ValidateCodingGap
- Vitals
