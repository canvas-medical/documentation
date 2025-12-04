---
title: "Protocol Cards"
slug: "effect-protocol-cards"
excerpt: "Calls to action in a patient's chart, commonly used for decision support intervention."
hidden: false
---

## Protocol Card

Protocol cards appear on the right-hand-side of a patient's chart, and can be accessed by clicking on the Protocols filter button in the filter menu.

{:refdef: style="text-align: center;"}
![protocol card](/assets/images/protocol-card.png){:width="95%"}
{: refdef}

A Protocol card consists of three main parts:

- A title, which appears at the top in bold
- A narrative, which appears just below the title to add any additional clarifying information
- A list of recommendations, which each have a title and optionally a button that can either:
  - open a new tab and navigate to another site
  - insert a command into a note

| Name              | Type                   | Required                                     | Description                                                                                                                                        |
| :---------------- | :--------------------- | :------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| `patient_id`      | _string_               | `true` (if `patient_filter` is not included) | The id of the [patient](/sdk/data-patient/)                                                                                                        |
| `patient_filter`  | _dict_                 | `true` (if `patient_id` is not included)     | Patient queryset filters to apply the effect to multiple patients. For example, `{"active": True}` will apply to the effect to all active patients |
| `key`             | _string_               | `true`                                       | A unique identifier for the protocol card                                                                                                          |
| `title`           | _string_               | `true`                                       | The title for the protocol card, which appears at the top in bold                                                                                  |
| `narrative`       | _string_               | `false`                                      | The narrative for the protocol card, which appears just below the title                                                                            |
| `recommendations` | list[_Recommendation_] | `false`                                      | The recommendations to appear in the protocol card                                                                                                 |
|                   |                        |                                              |                                                                                                                                                    |

| `Recommendation` |          |         |                                       |
| :--------------- | :------- | :------ | :------------------------------------ |
| `title`          | _string_ | `true`  | The description of the recommendation |
| `button`         | _string_ | `false` | The text to appear on the button      |
| `href`           | _string_ | `false` | The url for the button to navigate to |
|                  |          |         |                                       |

To include a command recommendation, we recommend you import the command from the [commands module](/sdk/commands/), instantiate the command with all the values you wish to populate, and then call `.recommend(title: str = "", button: str | None)` on the command to generate the recommendation that you can append to the protocol card's recommendations. Keep in mind that, at the moment, not all commands are supported for command insertion. See [below](#supported-commands) for the list of supported commands.
</br>
</br>
For non-command recommendations, you can either use the `Recommendation` class, or the `.add_recommendation(title: str = "", button: str = "", href: str | None)` method on the protocol card.

**Example**:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from datetime import date
from canvas_sdk.effects.protocol_card import ProtocolCard, Recommendation
from canvas_sdk.commands import DiagnoseCommand


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self):
        p = ProtocolCard(
            patient_id=self.target,
            key="testing-protocol-cards",
            title="This is a ProtocolCard title",
            narrative="this is the narrative",
            recommendations=[Recommendation(title="this recommendation has no action, just words!")]
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

<br/>

### Supported Commands

Only the following commands from the [commands module](/sdk/commands/) are currently supported for insertion from Protocol Cards:

- Assess
- Diagnose
- Goal
- HistoryOfPresentIllness
- Instruct
- MedicationStatement
- Perform
- Plan
- Prescribe
- Questionnaire
- ReasonForVisit
