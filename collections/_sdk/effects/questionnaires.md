---
title: "Questionnaires"
slug: "effect-questionnaires"
excerpt: "Effects for questionnaires"
hidden: false
---

The Canvas SDK includes functionality for handling questionnaire-related events.

## Creating a Questionnaire

You can create a questionnaire in one of two ways. A manifest YAML template is the simplest path when the questionnaire's shape is fixed and known when you build the plugin: you define the template and reference it in your `CANVAS_MANIFEST.json` file. Use the `CreateQuestionnaire` effect instead when the questionnaire's shape is not fixed at build time — for example, when it is assembled from external data, user input, or per-tenant configuration. Also use it when the questions change often and you do not want to ship a plugin release for each change. Both paths share the same field contract. See [Questionnaires](/sdk/questionnaires/) for the manifest schema and full field reference.

### CreateQuestionnaire Effect

The `CreateQuestionnaire` effect creates a questionnaire while your plugin runs. Import it as `from canvas_sdk.effects.questionnaire import CreateQuestionnaire`. It is not re-exported at the `canvas_sdk.effects` top level.

The effect takes a single `questionnaire` attribute: a `QuestionnaireConfig` dictionary that mirrors the manifest YAML template. It carries the questionnaire's `name`, `form_type`, `code_system`, and `code`, and a list of `questions`, each with its `responses` and optional `enabled_conditions`. See [Questionnaires](/sdk/questionnaires/) for the full field reference and the accepted value for each field. Those values are enforced by the JSON schema when the effect is applied.

#### Attributes

| Attribute     | Required | Type                       | Description                                                                                                                                          |
|---------------|----------|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| questionnaire | Yes      | QuestionnaireConfig (dict) | The questionnaire definition to create. Mirrors the manifest YAML template; see [Questionnaires](/sdk/questionnaires/) for the full field reference. |

#### Validation

Call `.apply()` to emit the effect. Validation runs at that point, so applying the effect with an invalid config raises a single pydantic `ValidationError` in the plugin — one error that lists every problem it found rather than stopping at the first — where you can see it. Effect failures raised on the Canvas server go to Sentry rather than back to the plugin, which is why the config is validated plugin-side. That also means the effect's return value alone cannot confirm the questionnaire was created; query it back through the [Questionnaire](/sdk/data-questionnaire/) data model — for example, `Questionnaire.objects.filter(name=...)` or by its `code_system` and `code` — or check `canvas logs`. Beyond the JSON schema, applying the effect checks that:

- Each question's coding (`code_system` plus `code`) is unique within the questionnaire, and each response `code` is unique within its question. Question and response codes are also non-empty, since branching logic attaches to them. `TXT` and `DATE` responses carry a placeholder code and are exempt from the response-code rules.
- Every `enabled_conditions` entry resolves within the same questionnaire: its `question_code` matches exactly one question, and its `value_code`, when present, is a response of that question.
- `name` is at most 241 characters, leaving room to rename a superseded questionnaire `<name> (v<id>)` within the 255-character column.

#### Versioning

Questionnaire names are globally unique. Emitting the effect with a name that is already in use archives the existing questionnaire, renames it `<name> (v<id>)`, and creates a new questionnaire in its place. Each emission publishes a new version rather than editing the current one, so repeated emissions leave a chain of superseded versions. Drive the effect from an explicit trigger, such as a [SimpleAPI](/sdk/handlers-simple-api-http/) route, rather than a handler on a recurring event, which would supersede the questionnaire every time it fires. To read the branching logic back after publishing, see the [Question](/sdk/data-questionnaire/#question) and [QuestionEnablementCondition](/sdk/data-questionnaire/#questionenablementcondition) data models.

#### Example

This [SimpleAPI](/sdk/handlers-simple-api-http/) route builds a small questionnaire from a request and publishes it:

```python?partial=true
from canvas_sdk.effects import Effect
from canvas_sdk.effects.questionnaire import CreateQuestionnaire
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute


class PublishWellnessQuestionnaire(SimpleAPIRoute):
    PATH = "/publish-wellness-questionnaire"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        # Replace with your own authentication logic.
        return True

    def post(self) -> list[Response | Effect]:
        config = {
            "name": "Daily Wellness Check",
            "form_type": "QUES",
            "code_system": "INTERNAL",
            "code": "daily-wellness-check",
            "can_originate_in_charting": True,
            "questions": [
                {
                    "content": "How are you feeling today?",
                    "code_system": "INTERNAL",
                    "code": "wellness-mood",
                    "responses_code_system": "INTERNAL",
                    "responses_type": "SING",
                    "responses": [
                        {"name": "Good", "code": "wellness-mood-good", "value": "0"},
                        {"name": "Not good", "code": "wellness-mood-bad", "value": "1"},
                    ],
                },
            ],
        }

        return [
            CreateQuestionnaire(questionnaire=config).apply(),
            JSONResponse({"status": "published"}),
        ]
```

The [`example_sdk_effect_create_questionnaire`](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/example_sdk_effect_create_questionnaire) reference plugin shows a fuller version: it translates an external screening definition into a `QuestionnaireConfig`, wires a follow-up question to an earlier answer through `enabled_conditions`, and reads the questionnaire back with its branching.

## Creating a Questionnaire Result

The `CreateQuestionnaireResult` effect allows you to create custom scoring of questionnaires in Canvas. It adds a narrative to the command in the UI and can appear in the Social Determinants section of the left side of the chart if the questionnaire is configured to show in that section (see [here](/sdk/questionnaires) for how to control setting `display_result_in_social_history_section` for questionnaires).


### Attributes

| Attribute    | Required | Type             | Description                                                                                                  |
|--------------|----------|------------------|--------------------------------------------------------------------------------------------------------------|
| interview_id | Yes      | string           | The id of the interview to associate the result with.           |
| score        | Yes      | float            | The numerical score of the questionnaire result.                                                             |
| abnormal     | No       | bool             | Whether the result is considered abnormal. Defaults to `False`.                                              |
| narrative    | No       | string           | A text description of the result and any recommended follow-up actions. Defaults to an empty string.         |
| code_system  | Yes*     | string           | The code system used to identify the questionnaire (e.g., `"INTERNAL"`).                                     |
| code         | Yes*     | string           | The code identifying the questionnaire within the code system (e.g., `"mchat_scoring"`).                             |

*Note: Questionnaire Results create an associated Observation record. The `code` and `code_system` fields are required in order to distinguish the Observation results. 

### Example

**Note:** This example assumes that an M-CHAT questionnaire created and loaded into the Canvas instance.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.questionnaire_result import CreateQuestionnaireResult
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.command import Command


class MChatQuestionnaireResult(BaseHandler):
    """
    Return a CreateQuestionnaireResult effect in response to a committed Questionnaire Command that
    contains questions coded for the M-CHAT questionnaire.
    """

    RESPONDS_TO = [EventType.Name(EventType.QUESTIONNAIRE_COMMAND__POST_COMMIT)]

    MCHAT_CODE_SYSTEM = "INTERNAL"
    MCHAT_CODE = "mchat_scoring"

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

<br/>
<br/>
<br/>