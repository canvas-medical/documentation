---
title: "Questionnaires"
slug: "effect-questionnaires"
excerpt: "Effects for questionnaires"
hidden: false
---

The Canvas SDK provides two effects for questionnaires: `CreateQuestionnaire` builds a questionnaire, and `CreateQuestionnaireResult` records a custom score against a completed one.

## Creating a Questionnaire

There are two ways to create a questionnaire, and both share the same field contract:

- **A manifest YAML template** — the simplest path when the questionnaire's shape is fixed as you build the plugin. Define the template and reference it in your `CANVAS_MANIFEST.json` file.
- **The `CreateQuestionnaire` effect** — for a shape that is not fixed at build time, such as one assembled from external data, user input, or per-instance configuration. Also the path to take when the questions change often enough that a plugin release per change is impractical.

[Questionnaires](/sdk/questionnaires/) holds the schema and the full field reference for both.

### CreateQuestionnaire Effect

Creates a questionnaire while your plugin runs.

```python?partial=true
from canvas_sdk.effects.questionnaire import CreateQuestionnaire
```

`CreateQuestionnaire` is not re-exported at the `canvas_sdk.effects` top level.

#### Attributes

| Attribute     | Required | Type                  | Description                             |
|---------------|----------|-----------------------|-----------------------------------------|
| questionnaire | Yes      | `QuestionnaireConfig` | The questionnaire definition to create. |

`.apply()` takes no arguments and returns an `Effect` for your handler to return:

```python?partial=true
CreateQuestionnaire(questionnaire=config).apply()
```

#### QuestionnaireConfig

`QuestionnaireConfig` is a `TypedDict`, so a plain dictionary satisfies it and the import is only needed to annotate the definition you build. `Question`, `Response`, and `EnabledCondition` annotate the nested levels:

```python?partial=true
from canvas_sdk.questionnaires.utils import (
    EnabledCondition,
    Question,
    QuestionnaireConfig,
    Response,
)
```

These are the config shapes, not the data models. `Question` here is the question you are about to write, while [Question](/sdk/data-questionnaire/#question) in `canvas_sdk.v1.data` is a question already saved, so importing both in one file needs an alias.

Three rules hold at every level of the config:

- **Unknown keys are rejected**, rather than dropped. A misspelled key fails validation instead of silently losing the setting it was meant to carry.
- **Types are matched strictly.** A score is the string `"0"`, and passing the integer `0` fails.
- **The accepted values are the manifest template's values**, because both paths validate against the same schema. [Questionnaires](/sdk/questionnaires/) shows the same fields authored as YAML.

##### Top level

| Key                                         | Required | Type | Description                                                                                                                 |
|---------------------------------------------|----------|------|-----------------------------------------------------------------------------------------------------------------------------|
| `name`                                      | Yes      | str  | Name of the questionnaire, up to 241 characters. The limit leaves room for the `<name> (v<id>)` rename a supersede applies. |
| `form_type`                                 | Yes      | str  | `QUES` (questionnaire), `SA` (structured assessment), `EXAM` (physical exam), or `ROS` (review of systems).                 |
| `code_system`                               | Yes      | str  | `SNOMED`, `LOINC`, `ICD-10`, `INTERNAL`, or `CPT`.                                                                          |
| `code`                                      | Yes      | str  | The code for the questionnaire, up to 100 characters, for example `72109-2`.                                                |
| `can_originate_in_charting`                 | Yes      | bool | Whether a user can start this questionnaire from charting.                                                                  |
| `questions`                                 | Yes      | list | At least one question, each shaped as below.                                                                                |
| `prologue`                                  | No       | str  | Text shown at the start of the questionnaire, for context.                                                                  |
| `display_results_in_social_history_section` | No       | bool | Whether completion shows in the Social History section. Defaults to `False`.                                                |

##### questions[]

| Key                                        | Required | Type | Description                                                                                                  |
|--------------------------------------------|----------|------|--------------------------------------------------------------------------------------------------------------|
| `code_system`                              | Yes      | str  | `SNOMED`, `LOINC`, `ICD-10`, `INTERNAL`, or `CPT`.                                                           |
| `code`                                     | Yes      | str  | Up to 100 characters. Must be non-empty and unique within the questionnaire, since branching attaches to it. |
| `content`                                  | Yes      | str  | The question text, up to 1024 characters.                                                                    |
| `responses_code_system`                    | Yes      | str  | `SNOMED`, `LOINC`, `ICD-10`, `INTERNAL`, or `CPT`.                                                           |
| `responses_type`                           | Yes      | str  | `SING` (single select), `MULT` (multi select), `TXT` (free text), or `DATE`.                                 |
| `responses`                                | Yes      | list | At least one response, each shaped as below.                                                                 |
| `code_description`                         | No       | str  | A description of the code, up to 255 characters.                                                             |
| `display_result_in_social_history_section` | No       | bool | Whether this answer shows in the Social History section. Defaults to `False`.                                |
| `enabled_behavior`                         | No       | str  | `all` or `any`: whether all or one of `enabled_conditions` must be met.                                      |
| `enabled_conditions`                       | No       | list | Conditions that enable this question, each shaped as below.                                                  |

##### responses[]

| Key                | Required | Type | Description                                                                                                                         |
|--------------------|----------|------|-------------------------------------------------------------------------------------------------------------------------------------|
| `name`             | Yes      | str  | Up to 1024 characters. The displayed text for `SING` and `MULT`. Use `"TXT"` on a `TXT` question and `"DATE"` on a `DATE` question. |
| `code`             | Yes      | str  | Up to 100 characters. Must be non-empty and unique within the question, except on `TXT` and `DATE`.                                 |
| `code_description` | No       | str  | A description of the code, up to 255 characters.                                                                                    |
| `value`            | No       | str  | The score for `SING` and `MULT`, up to 1000 characters. Omit it for no scoring. Not used for `DATE`.                                |

A `TXT` or `DATE` question still needs exactly one entry in `responses`, carrying a placeholder: `{"name": "TXT", "code": "<code>"}` or `{"name": "DATE", "code": "<code>"}`. A placeholder response is exempt from the response-code rules, both the non-empty check and the uniqueness check.

##### enabled_conditions[]

| Key             | Required | Type        | Description                                                                                                  |
|-----------------|----------|-------------|--------------------------------------------------------------------------------------------------------------|
| `question_code` | Yes      | str         | The `code` of the question whose answer is tested. It must match exactly one question in this questionnaire. |
| `operator`      | Yes      | str         | `=`, `!=`, `exists`, or `not_exists`.                                                                        |
| `value_code`    | No       | str or None | The response `code` to match, for a `SING` or `MULT` question.                                               |
| `value_string`  | No       | str or None | A free text value to match, up to 255 characters.                                                            |

A condition names its question by bare `code`, with no code system, so two questions sharing a code under different code systems make the reference ambiguous and validation rejects it.

#### Validation

Call `.apply()` to emit the effect. Validation runs at that point and raises one pydantic `ValidationError` listing every problem it found, rather than stopping at the first.

Beyond the JSON schema, it checks that:

- Each question's coding (`code_system` plus `code`) is unique within the questionnaire, and each response `code` is unique within its question. Question and response codes are also non-empty, since branching logic attaches to them. `TXT` and `DATE` responses carry a placeholder code and are exempt from the response-code rules.
- Every `enabled_conditions` entry resolves within the same questionnaire: its `question_code` matches exactly one question, and its `value_code`, when present, is a response of that question.
- `name` is at most 241 characters, leaving room to rename a superseded questionnaire `<name> (v<id>)` within the 255-character column.

Validation runs plugin-side because a failure raised on the Canvas server goes to Sentry rather than back to your plugin. For the same reason, a clean `.apply()` is not confirmation that the questionnaire was created. To check, read `canvas logs`, or query it back through the [Questionnaire](/sdk/data-questionnaire/) data model with `Questionnaire.objects.filter(name=...)`.

#### Versioning

Questionnaire names are globally unique, so emitting the effect with a name already in use:

- archives the existing questionnaire and renames it `<name> (v<id>)`,
- then creates a new questionnaire in its place.

Each emission publishes a new version rather than editing the current one, so repeated emissions leave a chain of superseded versions.

{% include alert.html type="warning" content="Drive this effect from an explicit trigger, such as a SimpleAPI route. A handler on a recurring event supersedes the questionnaire every time it fires." %}

To read the branching logic back after publishing, see the [Question](/sdk/data-questionnaire/#question) and [QuestionEnablementCondition](/sdk/data-questionnaire/#questionenablementcondition) data models.

#### Examples

##### Branching on an earlier answer

`enabled_conditions` wires a question to an answer given earlier in the same questionnaire. Here the second question appears only once the first is answered "Yes":

```python?partial=true
questions = [
    {
        "content": "Have you traveled outside the country in the last 30 days?",
        "code_system": "INTERNAL",
        "code": "travel-recent",
        "responses_code_system": "INTERNAL",
        "responses_type": "SING",
        "responses": [
            {"name": "Yes", "code": "travel-recent-yes"},
            {"name": "No", "code": "travel-recent-no"},
        ],
    },
    {
        "content": "Which countries did you visit?",
        "code_system": "INTERNAL",
        "code": "travel-countries",
        "responses_code_system": "INTERNAL",
        "responses_type": "TXT",
        "responses": [{"name": "TXT", "code": "travel-countries-text"}],
        "enabled_conditions": [
            {
                "question_code": "travel-recent",
                "operator": "=",
                "value_code": "travel-recent-yes",
            },
        ],
    },
]
```

A question carrying more than one condition needs `enabled_behavior` to say whether all of them or any one of them enables it.

##### Publishing from a SimpleAPI route

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

`CreateQuestionnaireResult` applies your own scoring to a questionnaire. The result:

- adds a narrative to the command in the UI.
- appears in the Social Determinants section on the left of the chart, when the questionnaire is configured to show there. [Questionnaires](/sdk/questionnaires/) covers the `display_result_in_social_history_section` setting.

### Attributes

| Attribute    | Required | Type   | Description                                                                                          |
|--------------|----------|--------|------------------------------------------------------------------------------------------------------|
| interview_id | Yes      | string | The id of the interview to associate the result with.                                                |
| score        | Yes      | float  | The numerical score of the questionnaire result.                                                     |
| abnormal     | No       | bool   | Whether the result is considered abnormal. Defaults to `False`.                                      |
| narrative    | No       | string | A text description of the result and any recommended follow-up actions. Defaults to an empty string. |
| code_system  | Yes*     | string | The code system used to identify the questionnaire, for example `"INTERNAL"`.                        |
| code         | Yes*     | string | The code identifying the questionnaire within the code system, for example `"mchat_scoring"`.        |

\* `code_system` and `code` are required because a questionnaire result also creates an [Observation](/sdk/data-observation/) record, and they are what tell one result's observations from another's.

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