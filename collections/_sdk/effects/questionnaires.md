---
title: "Questionnaires"
slug: "effect-questionnaires"
excerpt: "Author, create and score questionnaires from a plugin"
hidden: false
redirect_from:
  - /sdk/questionnaires/
---

Questionnaires are a structured set of questions that guide collecting answers from end users. A plugin can ship one with its manifest, create one while it runs, and score a completed one.

## Creating a Questionnaire

There are two ways to create a questionnaire, and both describe it with the same [field reference](#field-reference):

- **[A manifest YAML template](#manifest-yaml-template)** — the simplest path when the questionnaire's shape is fixed as you build the plugin. Define the template and reference it in your `CANVAS_MANIFEST.json` file.
- **[The `CreateQuestionnaire` effect](#createquestionnaire-effect)** — for a shape that is not fixed at build time, such as one assembled from external data, user input, or per-instance configuration. Also the path to take when the questions change often enough that a plugin release per change is impractical.
  - This is the route to pair with a [SimpleAPI](/sdk/handlers-simple-api-http/) route to stand up your own create-questionnaire endpoint, where a caller posts the questionnaire it wants and your plugin publishes it. See [Publishing from a SimpleAPI route](#publishing-from-a-simpleapi-route).

### Field reference

Both paths describe the same questionnaire and the same JSON schema validates both. In a manifest template these keys are YAML; in Python they are the `QuestionnaireConfig` dictionary the effect takes.

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

Two rules hold at every level, on both paths:

- **Unknown keys are rejected**, rather than dropped. A misspelled key fails validation instead of silently losing the setting it was meant to carry.
- **Types are matched strictly.** A score is the string `"0"` rather than the integer `0`, which is why the YAML examples below quote their values.

#### Top level

| Key                                         | Required | Type | Description                                                                                                                                |
|---------------------------------------------|----------|------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `name`                                      | Yes      | str  | Name of the questionnaire, up to 241 characters. The limit leaves room for the `<name> (v<id>)` rename a [supersede](#versioning) applies. |
| `form_type`                                 | Yes      | str  | One of the [form types](#form-types).                                                                                                      |
| `code_system`                               | Yes      | str  | One of the [code systems](#code-systems).                                                                                                  |
| `code`                                      | Yes      | str  | The code for the questionnaire, up to 100 characters, for example `72109-2`.                                                               |
| `can_originate_in_charting`                 | Yes      | bool | Whether a user can start this questionnaire from charting.                                                                                 |
| `questions`                                 | Yes      | list | At least one [question](#questions).                                                                                                       |
| `prologue`                                  | No       | str  | Text shown at the start of the questionnaire, for context.                                                                                 |
| `display_results_in_social_history_section` | No       | bool | Whether completion shows in the Social History section. Defaults to `False`.                                                               |

#### questions[]

| Key                                        | Required | Type | Description                                                                                                                                             |
|--------------------------------------------|----------|------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `code_system`                              | Yes      | str  | One of the [code systems](#code-systems).                                                                                                               |
| `code`                                     | Yes      | str  | The code for the question, up to 100 characters and non-empty. A question's coding, `code_system` plus `code`, must be unique within the questionnaire. |
| `content`                                  | Yes      | str  | The question text, up to 1024 characters.                                                                                                               |
| `responses_code_system`                    | Yes      | str  | One of the [code systems](#code-systems).                                                                                                               |
| `responses_type`                           | Yes      | str  | One of the [response types](#response-types).                                                                                                           |
| `responses`                                | Yes      | list | At least one [response](#responses).                                                                                                                    |
| `code_description`                         | No       | str  | A description of the code, up to 255 characters.                                                                                                        |
| `display_result_in_social_history_section` | No       | bool | Whether this answer shows in the Social History section. Defaults to `False`.                                                                           |
| `enabled_behavior`                         | No       | str  | One of the [enablement behaviors](#enablement-behaviors), when the question carries more than one condition.                                            |
| `enabled_conditions`                       | No       | list | [Conditions](#enabled_conditions) that enable this question.                                                                                            |

#### responses[]

| Key                | Required | Type | Description                                                                                                                         |
|--------------------|----------|------|-------------------------------------------------------------------------------------------------------------------------------------|
| `name`             | Yes      | str  | Up to 1024 characters. The displayed text for `SING` and `MULT`. Use `"TXT"` on a `TXT` question and `"DATE"` on a `DATE` question. |
| `code`             | Yes      | str  | Up to 100 characters. Must be non-empty and unique within the question, except on `TXT` and `DATE`.                                 |
| `code_description` | No       | str  | A description of the code, up to 255 characters.                                                                                    |
| `value`            | No       | str  | Up to 1000 characters. The score for `SING` and `MULT`, or default text for `TXT`. Not used for `DATE`.                             |

A `TXT` or `DATE` question still needs exactly one entry in `responses`, carrying a placeholder: `{"name": "TXT", "code": "<code>"}` or `{"name": "DATE", "code": "<code>"}`. A placeholder response is exempt from the response-code rules, both the non-empty check and the uniqueness check.

`value` is the score for a single answer, not a total. Canvas stores it against the response and does not add anything up, so turning a completed questionnaire into a score on the chart means summing the answers yourself and emitting [CreateQuestionnaireResult](#creating-a-questionnaire-result).

On a `TXT` question, `value` carries default text for the answer rather than a score, so it is how you prompt the person answering. A Review of Systems or Physical Exam note then lists that answer only once it differs from the default. Give the placeholder response a `value` to use this:

```python?partial=true
{
    "content": "Describe anything else you would like us to know",
    "code_system": "INTERNAL",
    "code": "other-notes",
    "responses_code_system": "INTERNAL",
    "responses_type": "TXT",
    "responses": [
        {"name": "TXT", "code": "other-notes-text", "value": "No additional concerns"},
    ],
}
```

#### enabled_conditions[]

| Key             | Required | Type        | Description                                                                                                  |
|-----------------|----------|-------------|--------------------------------------------------------------------------------------------------------------|
| `question_code` | Yes      | str         | The `code` of the question whose answer is tested. It must match exactly one question in this questionnaire. |
| `operator`      | Yes      | str         | One of the [enablement operators](#enablement-operators).                                                    |
| `value_code`    | No       | str or None | The response `code` to match, for a `SING` or `MULT` question.                                               |
| `value_string`  | No       | str or None | A free text value to match, up to 255 characters.                                                            |

A condition names its question by bare `code`, with no code system, so two questions sharing a code under different code systems make the reference ambiguous and validation rejects it.

Pair `=` and `!=` with `value_code` on a `SING` or `MULT` question, or with `value_string` on a `TXT` one. `exists` and `not_exists` take neither, since they test only whether the question was answered:

```python?partial=true
# Enable when an earlier question was answered "Yes".
{"question_code": "travel-recent", "operator": "=", "value_code": "travel-recent-yes"}

# Enable for every answer except "None".
{"question_code": "symptoms", "operator": "!=", "value_code": "symptoms-none"}

# Enable once the earlier question has an answer, whatever it is.
{"question_code": "current-medications", "operator": "exists"}

# Enable only while the earlier question is unanswered.
{"question_code": "pharmacy-preference", "operator": "not_exists"}

# Enable when a free text answer matches exactly.
{"question_code": "employment-status", "operator": "=", "value_string": "Retired"}
```

A question carrying more than one condition needs `enabled_behavior` to pick between them. Here a `MULT` symptoms question feeds two conditions, and either one is enough:

```python?partial=true
{
    "content": "How long have you had these symptoms?",
    "code_system": "INTERNAL",
    "code": "symptom-duration",
    "responses_code_system": "INTERNAL",
    "responses_type": "SING",
    "responses": [
        {"name": "Under a week", "code": "symptom-duration-short", "value": "0"},
        {"name": "A week or more", "code": "symptom-duration-long", "value": "1"},
    ],
    # "all" would require the patient to have reported both a cough and a fever.
    "enabled_behavior": "any",
    "enabled_conditions": [
        {"question_code": "symptoms", "operator": "=", "value_code": "symptoms-cough"},
        {"question_code": "symptoms", "operator": "=", "value_code": "symptoms-fever"},
    ],
}
```

Every `question_code` and `value_code` above has to resolve inside the same questionnaire. A `value_code` that is not a response of the question it names is rejected when the effect is applied, rather than quietly dropping the branching.

#### Value sets

The tables above reference these by name. They are enforced by the JSON schema, so an unlisted value is rejected when the effect is applied.

##### Code systems

Taken by `code_system` at both the questionnaire and question level, and by `responses_code_system`.

| Value      | Meaning                                                                           |
|------------|-----------------------------------------------------------------------------------|
| `SNOMED`   | SNOMED CT codes.                                                                  |
| `LOINC`    | LOINC codes.                                                                      |
| `ICD-10`   | ICD-10 codes.                                                                     |
| `CPT`      | CPT codes.                                                                        |
| `INTERNAL` | A coding of your own, when the questionnaire has no code from a published system. |

##### Form types

| Value  | Meaning                |
|--------|------------------------|
| `QUES` | Questionnaire.         |
| `SA`   | Structured assessment. |
| `EXAM` | Physical exam.         |
| `ROS`  | Review of systems.     |

##### Response types

| Value  | Answer                                                |
|--------|-------------------------------------------------------|
| `SING` | Single select. One response from `responses`.         |
| `MULT` | Multi select. One or more responses from `responses`. |
| `TXT`  | Free text. Takes a single placeholder response.       |
| `DATE` | A calendar date, entered as `YYYY-MM-DD`. Takes a single placeholder response. |

The [question types](/sdk/data-questionnaire/#question-types) a saved question can carry also include `INT` and `DEC`. Neither is in this value set, so a questionnaire created through the effect cannot use them.

##### Enablement operators

| Value        | Condition is met when                                     |
|--------------|-----------------------------------------------------------|
| `=`          | the answer matches `value_code` or `value_string`.        |
| `!=`         | the answer does not match `value_code` or `value_string`. |
| `exists`     | the question has any answer.                              |
| `not_exists` | the question has no answer.                               |

##### Enablement behaviors

| Value | Meaning                      |
|-------|------------------------------|
| `all` | Every condition must be met. |
| `any` | One condition is enough.     |

### Manifest YAML template

Shipping a questionnaire with your plugin takes two files: the YAML template that defines it, and the manifest entry that points at it.

```text
example_questionnaire/
├── CANVAS_MANIFEST.json
└── templates/
    └── example_questionnaire.yml
```

#### The template file

`templates/example_questionnaire.yml` holds the questionnaire itself, written with the keys in the [field reference](#field-reference). This one has a single select, a multi select, a free text and a date question:

```yaml
name: Example Name
form_type: QUES
code_system: LOINC
code: QUES_EXAMPLE_NAME
can_originate_in_charting: true
prologue: This is an example of a structured assessment with single select, multiselect, free text, and date responses.
questions:
  - content: "This is question #1"
    code_system: CPT
    code: H0005
    responses_code_system: INTERNAL
    responses_type: SING
    display_result_in_social_history_section: true
    responses:
      - name: "Single select response #1"
        code: QUES_EXAMPLE_NAME_Q1_A1
        value: "1"
      - name: "Single select response #2"
        code: QUES_EXAMPLE_NAME_Q1_A2
        value: "0"
      - name: "Single select response #3"
        code: QUES_EXAMPLE_NAME_Q1_A3
        value: "0"
  - content: "This is question #2"
    code_system: INTERNAL
    code: QUES_EXAMPLE_NAME_Q2
    responses_code_system: ICD-10
    responses_type: MULT
    display_result_in_social_history_section: true
    responses:
      - name: "Multi select response #1"
        code: F1910
        value: "0"
      - name: "Multi select response #2"
        code: QUES_EXAMPLE_NAME_Q1_A1
        value: "2"
      - name: "Multi select response #3"
        code: QUES_EXAMPLE_NAME_Q1_A2
        value: "0"
  - content: "This is question #3"
    code_system: INTERNAL
    code: QUES_EXAMPLE_NAME_Q3
    responses_code_system: INTERNAL
    responses_type: TXT
    display_result_in_social_history_section: true
    responses:
      - name: "Free text response"
        code: QUES_EXAMPLE_NAME_Q3_A1
        value: "This is a default pre-populated free text response."
  - content: "This is question #4"
    code_system: INTERNAL
    code: QUES_EXAMPLE_NAME_Q4
    responses_code_system: INTERNAL
    responses_type: DATE
    display_result_in_social_history_section: true
    responses:
      - name: "DATE"
        code: QUES_EXAMPLE_NAME_Q4_A1
```

The [JSON schema](https://raw.githubusercontent.com/canvas-medical/canvas-plugins/main/schemas/questionnaire.json) is the authority on these keys.

#### Referencing it from the manifest

Add the template's path to the `questionnaires` section of `CANVAS_MANIFEST.json`. `template` is relative to the plugin package:

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "example_questionnaire",
    "description": "Ships a structured assessment questionnaire.",
    "components": {
        "handlers": [],
        "commands": [],
        "content": [],
        "effects": [],
        "views": [],
        "questionnaires": [
            {
                "template": "templates/example_questionnaire.yml"
            }
        ]
    },
    "variables": [],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

#### Example with branching

A template using `enabled_conditions` to show questions only once an earlier answer calls for them:

```yaml
name: Branching Example
form_type: QUES
code_system: INTERNAL
code: QUES_BRANCHING_EXAMPLE
can_originate_in_charting: true
prologue: This questionnaire demonstrates conditional logic with enabled_conditions and enabled_behavior.
questions:
  - content: "Do you have any allergies?"
    code_system: INTERNAL
    code: QUES_BRANCH_Q1
    responses_code_system: INTERNAL
    responses_type: SING
    responses:
      - name: "Yes"
        code: QUES_BRANCH_Q1_YES
      - name: "No"
        code: QUES_BRANCH_Q1_NO
  - content: "Please describe your allergies"
    code_system: INTERNAL
    code: QUES_BRANCH_Q2
    responses_code_system: INTERNAL
    responses_type: TXT
    enabled_conditions:
      - question_code: QUES_BRANCH_Q1
        operator: "="
        value_code: QUES_BRANCH_Q1_YES
    responses:
      - name: "TXT"
        code: QUES_BRANCH_Q2_A1
  - content: "How severe are your allergies?"
    code_system: INTERNAL
    code: QUES_BRANCH_Q3
    responses_code_system: INTERNAL
    responses_type: SING
    enabled_behavior: all
    enabled_conditions:
      - question_code: QUES_BRANCH_Q1
        operator: "="
        value_code: QUES_BRANCH_Q1_YES
      - question_code: QUES_BRANCH_Q2
        operator: exists
    responses:
      - name: "Mild"
        code: QUES_BRANCH_Q3_MILD
      - name: "Moderate"
        code: QUES_BRANCH_Q3_MODERATE
      - name: "Severe"
        code: QUES_BRANCH_Q3_SEVERE
```

In this example:

- **Q1** is always visible.
- **Q2** only appears if Q1 is answered "Yes" (using `=` with `value_code`).
- **Q3** only appears if Q1 is "Yes" **and** Q2 has been answered (using `enabled_behavior: all` with two conditions).

#### Loading a definition from YAML

`questionnaire_from_yaml` reads a template out of your plugin package and returns it as a `QuestionnaireConfig`, validated against the schema on the way:

```python?partial=true
from canvas_sdk.questionnaires import questionnaire_from_yaml

config = questionnaire_from_yaml("templates/example_questionnaire.yml")
```

A leading `/` on the path is stripped during resolution. It raises `FileNotFoundError` when the file is not in the plugin, `PermissionError` when the path resolves outside the plugin directory, and a `ValidationError` when the template does not match the schema.

Because it returns the shape the effect takes, a template can seed a questionnaire built at runtime: load it, adjust it in Python, and hand it to the [CreateQuestionnaire effect](#createquestionnaire-effect).

### CreateQuestionnaire Effect

Creates a questionnaire while your plugin runs.

```python?partial=true
from canvas_sdk.effects.questionnaire import CreateQuestionnaire
```

#### Attributes

| Attribute     | Required | Type                                        | Description                             |
|---------------|----------|---------------------------------------------|-----------------------------------------|
| questionnaire | Yes      | [QuestionnaireConfig](#field-reference) | The questionnaire definition to create. |

`.apply()` takes no arguments and returns an `Effect` for your handler to return:

```python?partial=true
CreateQuestionnaire(questionnaire=config).apply()
```

#### Validation

Call `.apply()` to emit the effect. Validation runs at that point and raises one pydantic `ValidationError` listing every problem it found, rather than stopping at the first.

Beyond the JSON schema, it checks that:

- Each question's coding (`code_system` plus `code`) is unique within the questionnaire, and each response `code` is unique within its question. Question and response codes are also non-empty, since branching logic attaches to them. `TXT` and `DATE` responses carry a placeholder code and are exempt from the response-code rules.
- Every `enabled_conditions` entry resolves within the same questionnaire: its `question_code` matches exactly one question, and its `value_code`, when present, is a response of that question.
- `name` is at most 241 characters, leaving room to rename a superseded questionnaire `<name> (v<id>)` within the 255-character column.

Validation runs plugin-side because a failure raised on the Canvas server goes to Sentry rather than back to your plugin. For the same reason, a clean `.apply()` is not confirmation that the questionnaire was created.

There is also no event to wait on: no [event type](/sdk/events/) fires when a questionnaire is created or updated. `INTERVIEW_CREATED` and `INTERVIEW_UPDATED` cover a questionnaire being filled out rather than the questionnaire itself, and the `QUESTIONNAIRE_COMMAND__*` events cover the command in a note. To confirm a questionnaire was created, read `canvas logs`, or query it back through the [Questionnaire](/sdk/data-questionnaire/) data model with `Questionnaire.objects.filter(name=...)`.

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

See [enabled_conditions[]](#enabled_conditions) for the other operators and for a question gated on more than one condition.

##### Publishing from a SimpleAPI route

A [SimpleAPI](/sdk/handlers-simple-api-http/) route gives you a create-questionnaire endpoint of your own: the caller posts a shape you define, and the route translates it. Canvas's schema stays on your side of the boundary, and changing the questions becomes a different request body rather than a plugin release.

This route takes a title, a code, and a list of questions:

```json
{
  "title": "Daily Wellness Check",
  "code": "daily-wellness-check",
  "questions": [
    {
      "prompt": "How are you feeling today?",
      "choices": ["Good", "Not good"]
    },
    {
      "prompt": "Anything else you would like us to know?",
      "type": "text"
    }
  ]
}
```

Each question in the body becomes a question in the config, with its choices scored by position and codes generated as it goes. [`APIKeyAuthMixin`](/sdk/handlers-simple-api-http/#api-key) handles authentication, which needs a `simpleapi-api-key` secret declared in the manifest and set on the instance:

```python?partial=true
from typing import Any

from canvas_sdk.effects import Effect
from canvas_sdk.effects.questionnaire import CreateQuestionnaire
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPIRoute
from canvas_sdk.questionnaires.utils import Question, QuestionnaireConfig


class PublishQuestionnaire(APIKeyAuthMixin, SimpleAPIRoute):
    PATH = "/publish-questionnaire"

    def post(self) -> list[Response | Effect]:
        try:
            config = self._build_config(self.request.json())
            # A pydantic ValidationError subclasses ValueError, so the except below returns the
            # caller a 400 naming the problem instead of letting it fail out of sight on the
            # Canvas side.
            effect = CreateQuestionnaire(questionnaire=config).apply()
        except KeyError as error:
            return [JSONResponse({"error": f"Missing field {error}"}, status_code=400)]
        except ValueError as error:
            return [JSONResponse({"error": str(error)}, status_code=400)]

        return [
            JSONResponse({"created": config["name"], "questions": len(config["questions"])}),
            effect,
        ]

    def _build_config(self, body: dict[str, Any]) -> QuestionnaireConfig:
        return {
            "name": body["title"],
            "form_type": "QUES",
            "code_system": "INTERNAL",
            "code": body["code"],
            "can_originate_in_charting": True,
            "questions": [
                self._build_question(index, item)
                for index, item in enumerate(body["questions"], start=1)
            ],
        }

    def _build_question(self, index: int, item: dict[str, Any]) -> Question:
        code = f"Q{index}"

        if item.get("type") == "text":
            return {
                "content": item["prompt"],
                "code_system": "INTERNAL",
                "code": code,
                "responses_code_system": "INTERNAL",
                "responses_type": "TXT",
                # A typed answer still needs one option to hang the response on.
                "responses": [{"name": "TXT", "code": f"{code}A1"}],
            }

        return {
            "content": item["prompt"],
            "code_system": "INTERNAL",
            "code": code,
            "responses_code_system": "INTERNAL",
            "responses_type": "SING",
            "responses": [
                {"name": choice, "code": f"{code}A{position + 1}", "value": str(position)}
                for position, choice in enumerate(item["choices"])
            ],
        }
```

Scoring each choice by its position is the kind of thing that is tedious to maintain in a static template and trivial to compute here, which is the case for building the questionnaire in Python rather than declaring it.

The [`example_sdk_effect_create_questionnaire`](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/example_sdk_effect_create_questionnaire) reference plugin goes further: it maps a caller's own question types onto `SING`, `MULT`, `TXT`, and `DATE`, wires a follow-up question to an earlier answer through `enabled_conditions`, and reads the questionnaire back with its branching.

## Creating a Questionnaire Result

`CreateQuestionnaireResult` applies your own scoring to a questionnaire. The result:

- adds a narrative to the command in the UI.
- appears in the Social Determinants section on the left of the chart, when the questionnaire is configured to show there. [Questionnaires](#field-reference) covers the `display_result_in_social_history_section` setting.

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

### Examples

#### Summing the answers

The simplest scoring is a total of every answer's `value`. This handler runs when a questionnaire command is committed, checks the questionnaire is the one it scores, and adds the answers up:

```python?partial=true
from canvas_sdk.effects import Effect
from canvas_sdk.effects.questionnaire_result import CreateQuestionnaireResult
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.command import Command

# A TXT or DATE answer is typed rather than chosen from a list, so it carries no score.
UNSCORED_TYPES = ["TXT", "DATE"]


class QuestionnaireScore(BaseHandler):
    """Score a committed questionnaire by totalling its answers."""

    RESPONDS_TO = [EventType.Name(EventType.QUESTIONNAIRE_COMMAND__POST_COMMIT)]

    QUESTIONNAIRE_CODE_SYSTEM = "LOINC"
    QUESTIONNAIRE_CODE = "93025-5"
    SCORE_CODE_SYSTEM = "INTERNAL"
    SCORE_CODE = "questionnaire-score"

    def compute(self) -> list[Effect]:
        # The interview is the anchor object on the questionnaire command.
        command = Command.objects.get(id=self.event.target.id)
        interview = command.anchor_object

        # The event fires for every questionnaire, so ignore the ones this handler does not score.
        questionnaire = interview.questionnaires.first()
        if (
            questionnaire.code != self.QUESTIONNAIRE_CODE
            or questionnaire.code_system != self.QUESTIONNAIRE_CODE_SYSTEM
        ):
            return []

        scorable = questionnaire.questions.exclude(
            response_option_set__type__in=UNSCORED_TYPES
        ).count()
        answers = interview.interview_responses.exclude(
            response_option__response_option_set__type__in=UNSCORED_TYPES
        )

        # A part-answered questionnaire totals lower than a complete one, so publishing a score
        # for it would understate the result.
        if answers.count() != scorable:
            return []

        # An option left unscored has an empty value and contributes nothing.
        score = sum(int(answer.response_option.value or 0) for answer in answers)

        effect = CreateQuestionnaireResult(
            interview_id=str(interview.id),
            score=score,
            narrative=f"Score of {score}.",
            code_system=self.SCORE_CODE_SYSTEM,
            code=self.SCORE_CODE,
        )

        return [effect.apply()]
```

Set `QUESTIONNAIRE_CODE_SYSTEM` and `QUESTIONNAIRE_CODE` to the questionnaire you are scoring, and `SCORE_CODE_SYSTEM` and `SCORE_CODE` to the coding you want the result's [Observation](/sdk/data-observation/) to carry.

#### Banding the score into a narrative

A total on its own tells a reader little. This M-CHAT example sums the answers the same way, then turns the total into a risk band with the follow-up it calls for, and marks the result abnormal.

**Note:** This example assumes an M-CHAT questionnaire is already created and loaded into the Canvas instance.

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
