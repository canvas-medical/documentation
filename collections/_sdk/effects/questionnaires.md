---
title: "Questionnaires"
slug: "effect-questionnaires"
excerpt: "Effects for questionnaires"
hidden: false
---

The Canvas SDK includes functionality for handling questionnaire-related events.

## Creating a questionnaire result

When a questionnaire is committed, a questionnaire result can be created using the `CreateQuestionnaireResult` effect.

This effect will cause a new entry to appear in the Social Determinants section of the left side of the chart.

The `CreateQuestionnairResult` effect enables custom scoring of questionnaires in Canvas.

### Example

**Note:** This example assumes that an M-CHAT questionnaire created and loaded into the Canvas instance.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.questionnaire_result import CreateQuestionnaireResult
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data.command import Command


class MChatQuestionnaireResult(BaseProtocol):
    """
    Return a CreateQuestionnaireResult effect in response to a committed Questionnaire Command that
    contains questions coded for the M-CHAT questionnaire.
    """

    RESPONDS_TO = [EventType.Name(EventType.QUESTIONNAIRE_COMMAND__POST_COMMIT)]

    MCHAT_CODE_SYSTEM = "INTERNAL"
    MCHAT_CODE = "mchat"

    def compute(self) -> list[Effect]:
        # Get the interview object, which will be the anchor object on the Questionnaire command.
        command = Command.objects.get(id=self.event.target.id)
        interview = command.anchor_object
        if not interview.committer:
            return []

        # Return no effects if the interview has no questions that are coded as M-CHAT questions
        if not any(
            q.code == self.MCHAT_CODE and q.code_system == self.MCHAT_CODE_SYSTEM
            for q in interview.questionnaires.all()
        ):
            return []

        # sum up the numerical value of each answered questionnaire
        score = 0
        for response in interview.interview_responses.all():
            score = score + int(response.response_option.value)

        # Determine the narrative and whether the result is abnormal
        if score >= 0 and score <= 2:
            abnormal = False
            narrative = (
                "The score is LOW risk. Child has screened negative. No immediate follow-up is "
                "needed. However, the child should be rescreened at 24 months or after 3 months "
                "have passed if they are younger than 2 years. Monitoring the child's "
                "development remains important."
            )
        elif score >= 3 and score <= 7:
            abnormal = True
            narrative = (
                "The score is MODERATE risk. Administer the M-CHAT-R Follow-Up items that "
                "correspond to the at-risk responses. Only those items which were scored at risk "
                "need to be completed. If 2 or more items continue to be at-risk, refer the "
                "child immediately for (a) early intervention and (b) diagnostic evaluation."
            )
        elif score >= 8 and score <= 20:
            abnormal = True
            narrative = (
                "The score is HIGH risk. It is not necessary to complete the M-CHAT-R Follow-Up "
                "at this time. Bypass Follow-Up, and refer immediately for (a) early "
                "intervention and (b) diagnostic evaluation."
            )
        else:
            abnormal = True
            narrative = "Error occurred trying to score questionnaire."

        # Create and return the effect
        effect = CreateQuestionnaireResult(
            interview_id=str(interview.id),
            score=score,
            abnormal=abnormal,
            narrative=narrative,
            code_system=self.MCHAT_CODE_SYSTEM,
            code=self.MCHAT_CODE,
        )

        return [effect.apply()]
```
