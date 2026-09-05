---
title: "Create Questionnaire"
slug: "effect-create-questionnaire"
excerpt: "Effect for creating questionnaires programmatically"
hidden: false
---

# Create Questionnaire Effect

The `CreateQuestionnaire` effect enables the programmatic creation of questionnaires within the Canvas system. This effect allows developers to dynamically generate structured sets of questions intended to guide the collection of answers from end-users.

{% include alert.html type="info" content="For creating questionnaires via YAML templates, see the <a href='/sdk/questionnaires/'>Questionnaires</a> documentation. Use this effect when you need to create questionnaires dynamically at runtime based on business logic or external data sources." %}

## Overview

The `CreateQuestionnaire` effect creates questionnaires programmatically within Canvas plugins. Here's how it works:

1. **Define the questionnaire config**: Create a `QuestionnaireConfig` dictionary with your questionnaire structure (name, questions, responses, etc.)
2. **Create the effect**: Instantiate `CreateQuestionnaire` with your config as the `questionnaire_config` parameter
3. **Apply the effect**: Call `.apply()` on the effect instance
4. **Return from your handler**: Include the effect in the list returned from your `compute()` method
5. **Canvas processes the effect**: The Canvas interpreter validates the config against the JSON schema, converts it to YAML internally, and persists the questionnaire to the database

This approach is particularly useful when:

- Questionnaires need to be generated dynamically based on patient data or clinical context
- External systems need to create questionnaires via API integrations
- Questionnaire content needs to be customized per practice or provider
- Questionnaires are generated in response to specific clinical events

## Usage

The `CreateQuestionnaire` effect accepts a single `questionnaire_config` parameter that follows the same structure as the questionnaire YAML format. The config is validated against the questionnaire JSON schema when the effect is applied.

```python?partial=true
from canvas_sdk.effects.questionnaire import CreateQuestionnaire
from canvas_sdk.questionnaires.utils import QuestionnaireConfig

config: QuestionnaireConfig = {
    "name": "PHQ-9",
    "form_type": "QUES",
    "code_system": "LOINC",
    "code": "44249-1",
    "can_originate_in_charting": True,
    "questions": [...]
}

effect = CreateQuestionnaire(questionnaire_config=config)
```

## QuestionnaireConfig Structure

### Top-Level Fields

| Attribute                                  | Type                 | Description                                                                                                                                                    | Required |
|--------------------------------------------|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| `name`                                     | `str`                | Name of the questionnaire                                                                                                                                      | Yes      |
| `form_type`                                | `str`                | Specifies the use case: `QUES` (Questionnaire), `SA` (Structured Assessment), `EXAM` (Physical Exam), or `ROS` (Review of Systems)                             | Yes      |
| `code_system`                              | `str`                | The coding system used for the questionnaire (e.g., `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`, `CANVAS`)                                                  | Yes      |
| `code`                                     | `str`       | The assigned code for the questionnaire (will be converted to string)                                                                                         | Yes      |
| `can_originate_in_charting`                | `bool`               | Specifies if the questionnaire can be initiated from charting                                                                                                  | Yes      |
| `questions`                                | `list[dict]`         | List of questions in the questionnaire                                                                                                                         | Yes      |
| `prologue`                                 | `str`                | Text displayed at the beginning of the questionnaire to provide context to the user                                                                            | No       |
| `display_results_in_social_history_section`| `bool`               | Determines if completion information should be displayed in the Social History (SHX) section. Defaults to `False`                                              | No       |

### Question Fields

Each question in the `questions` list should have the following structure:

| Attribute                                  | Type                 | Description                                                                                                      | Required |
|--------------------------------------------|----------------------|------------------------------------------------------------------------------------------------------------------|----------|
| `content`                                  | `str`                | The question text displayed to the user                                                                          | Yes      |
| `code_system`                              | `str`                | The coding system for the question (e.g., `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`, `CANVAS`)              | Yes      |
| `code`                                     | `str`                | The assigned code for the question. Must be unique within the questionnaire                                      | Yes      |
| `responses_code_system`                    | `str`                | The coding system for responses (e.g., `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`)                           | Yes      |
| `responses_type`                           | `str`                | Response type: `SING` (Single Select), `MULT` (Multi Select), `TXT` (Free Text)                                  | Yes      |
| `responses`                                | `list[dict]`         | List of possible responses for the question                                                                      | Yes      |
| `code_description`                         | `str`                | Description of the question code                                                                                 | No       |
| `display_result_in_social_history_section` | `bool`               | Determines if the response should be shown in the Social History (SHX) section. Defaults to `False`              | No       |
| `enabled_behavior`                         | `str`                | Branching logic behavior: `all` (all conditions must be met) or `any` (any condition can be met)                 | No       |
| `enabled_conditions`                       | `list[dict]`         | List of conditions that determine when this question is shown. See [Enabled Conditions](#enabled-conditions)     | No       |

### Enabled Conditions

When using branching logic, each condition in the `enabled_conditions` list should have:

| Attribute       | Type            | Description                                                                    | Required |
|-----------------|-----------------|--------------------------------------------------------------------------------|----------|
| `question_code` | `str`           | The code of the question whose answer determines if this question is shown    | Yes      |
| `operator`      | `str`           | Comparison operator (e.g., `=`, `!=`, `>`, `<`)                                | Yes      |
| `value_code`    | `str` or `None` | The response code value to compare against                                     | No*      |
| `value_string`  | `str` or `None` | The string value to compare against (for text responses)                       | No*      |

*Either `value_code` or `value_string` should be provided depending on the type of comparison.

### Response Fields

Each response in the `responses` list should have the following structure:

| Attribute         | Type            | Description                                                                                                                | Required |
|-------------------|-----------------|----------------------------------------------------------------------------------------------------------------------------|----------|
| `name`            | `str`           | For `SING`/`MULT`, the text displayed for the response option. For `TXT` type questions, should be set to "TXT"           | Yes      |
| `code`            | `str`           | The assigned code for the response. Must be unique within the question                                                     | Yes      |
| `code_description`| `str`           | Description of the response code                                                                                           | No       |
| `value`           | `str` or `int`  | For `SING`/`MULT`, optional numerical value for scoring. Leave blank or omit if no scoring is desired                     | No       |

## Implementation Details

- **Validation**: The questionnaire config is validated against the JSON schema defined in the canvas-plugins repository
- **YAML Conversion**: The config is automatically converted to YAML format internally
- **Default Values**: Optional fields are handled appropriately with defaults when not provided

## Example Usage

### Basic Questionnaire Creation

```python?partial=true
from canvas_sdk.effects.questionnaire import CreateQuestionnaire
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType
from canvas_sdk.questionnaires.utils import QuestionnaireConfig


class DynamicQuestionnaireCreator(BaseHandler):
    """
    Create a questionnaire programmatically in response to a patient creation event.
    """
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_CREATED)]

    def compute(self):
        # Create a simple pain assessment questionnaire
        config: QuestionnaireConfig = {
            "name": "Pain Assessment",
            "form_type": "QUES",
            "code_system": "LOINC",
            "code": "72514-3",
            "can_originate_in_charting": True,
            "prologue": "Please answer the following questions about your pain level.",
            "display_results_in_social_history_section": True,
            "questions": [
                {
                    "code_system": "LOINC",
                    "code": "72514-3",
                    "content": "What is your current pain level?",
                    "responses_code_system": "LOINC",
                    "responses_type": "SING",
                    "display_result_in_social_history_section": True,
                    "responses": [
                        {"name": "No pain", "code": "LA6568-5", "value": "0"},
                        {"name": "Mild pain", "code": "LA6569-3", "value": "3"},
                        {"name": "Moderate pain", "code": "LA6570-1", "value": "5"},
                        {"name": "Severe pain", "code": "LA6571-9", "value": "8"},
                    ],
                }
            ],
        }

        questionnaire = CreateQuestionnaire(questionnaire_config=config)
        return [questionnaire.apply()]
```

### Multi-Question Questionnaire with Different Response Types

```python?partial=true
from canvas_sdk.effects.questionnaire import CreateQuestionnaire
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType
from canvas_sdk.questionnaires.utils import QuestionnaireConfig


class ComprehensiveQuestionnaireCreator(BaseHandler):
    """
    Create a comprehensive questionnaire with multiple question types.
    """
    RESPONDS_TO = [EventType.Name(EventType.PLUGIN_INSTALLED)]

    def compute(self):
        config: QuestionnaireConfig = {
            "name": "Patient Health Screening",
            "form_type": "SA",
            "code_system": "INTERNAL",
            "code": "PATIENT_HEALTH_SCREEN_V1",
            "can_originate_in_charting": True,
            "prologue": "This screening will help us understand your current health status.",
            "display_results_in_social_history_section": True,
            "questions": [
                # Single select question
                {
                    "code_system": "INTERNAL",
                    "code": "EXERCISE_FREQ",
                    "content": "How often do you exercise per week?",
                    "responses_code_system": "INTERNAL",
                    "responses_type": "SING",
                    "responses": [
                        {"name": "Never", "code": "EX_NEVER", "value": "0"},
                        {"name": "1-2 times", "code": "EX_1_2", "value": "1"},
                        {"name": "3-4 times", "code": "EX_3_4", "value": "2"},
                        {"name": "5+ times", "code": "EX_5_PLUS", "value": "3"},
                    ],
                },
                # Multi select question
                {
                    "code_system": "INTERNAL",
                    "code": "CHRONIC_CONDITIONS",
                    "content": "Do you have any of the following conditions? (Select all that apply)",
                    "responses_code_system": "INTERNAL",
                    "responses_type": "MULT",
                    "display_result_in_social_history_section": True,
                    "responses": [
                        {"name": "Diabetes", "code": "COND_DIABETES"},
                        {"name": "Hypertension", "code": "COND_HYPERTENSION"},
                        {"name": "Asthma", "code": "COND_ASTHMA"},
                        {"name": "Heart Disease", "code": "COND_HEART"},
                        {"name": "None", "code": "COND_NONE"},
                    ],
                },
                # Free text question
                {
                    "code_system": "INTERNAL",
                    "code": "ADDITIONAL_NOTES",
                    "content": "Please provide any additional information about your health:",
                    "responses_code_system": "INTERNAL",
                    "responses_type": "TXT",
                    "responses": [{"name": "TXT", "code": "ADDITIONAL_NOTES_TEXT"}],
                },
            ],
        }

        questionnaire = CreateQuestionnaire(questionnaire_config=config)
        return [questionnaire.apply()]
```

### Questionnaire with Branching Logic

```python?partial=true
from canvas_sdk.effects.questionnaire import CreateQuestionnaire
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType
from canvas_sdk.questionnaires.utils import QuestionnaireConfig


class BranchingQuestionnaireCreator(BaseHandler):
    """
    Create a questionnaire with conditional branching logic.
    Questions appear based on previous answers using enabled_behavior and enabled_conditions.
    """
    RESPONDS_TO = [EventType.Name(EventType.PLUGIN_INSTALLED)]

    def compute(self):
        config: QuestionnaireConfig = {
            "name": "Patient Health Screening with Branching",
            "form_type": "QUES",
            "code_system": "LOINC",
            "code": "75626-2",
            "can_originate_in_charting": True,
            "prologue": "This questionnaire will help us understand your current health status. Some questions will appear based on your previous answers.",
            "display_results_in_social_history_section": True,
            "questions": [
                {
                    "content": "Do you currently smoke cigarettes?",
                    "code_system": "LOINC",
                    "code": "72166-2",
                    "code_description": "Tobacco smoking status",
                    "responses_code_system": "SNOMED",
                    "responses_type": "SING",
                    "display_result_in_social_history_section": True,
                    "responses": [
                        {
                            "name": "Yes",
                            "code": "373066001",
                            "code_description": "Yes (qualifier value)",
                            "value": "1",
                        },
                        {
                            "name": "No",
                            "code": "373067005",
                            "code_description": "No (qualifier value)",
                            "value": "0",
                        },
                    ],
                },
                {
                    "content": "How many cigarettes do you smoke per day?",
                    "code_system": "LOINC",
                    "code": "68520-2",
                    "code_description": "Number of cigarettes smoked per day",
                    "responses_code_system": "INTERNAL",
                    "responses_type": "SING",
                    "enabled_behavior": "all",  # All conditions must be met
                    "enabled_conditions": [
                        {
                            "question_code": "72166-2",  # References smoking question
                            "operator": "=",
                            "value_code": "373066001",  # "Yes" response code
                            "value_string": None,
                        }
                    ],
                    "responses": [
                        {
                            "name": "Less than 10",
                            "code": "SMOKE_LIGHT",
                            "code_description": "Light smoker",
                            "value": "1",
                        },
                        {
                            "name": "10-20",
                            "code": "SMOKE_MODERATE",
                            "code_description": "Moderate smoker",
                            "value": "2",
                        },
                        {
                            "name": "More than 20",
                            "code": "SMOKE_HEAVY",
                            "code_description": "Heavy smoker",
                            "value": "3",
                        },
                    ],
                },
                {
                    "content": "Would you like information about smoking cessation programs?",
                    "code_system": "INTERNAL",
                    "code": "CESSATION_INFO",
                    "code_description": "Interest in smoking cessation",
                    "responses_code_system": "SNOMED",
                    "responses_type": "SING",
                    "enabled_behavior": "all",
                    "enabled_conditions": [
                        {
                            "question_code": "72166-2",
                            "operator": "=",
                            "value_code": "373066001",
                            "value_string": None,
                        }
                    ],
                    "responses": [
                        {
                            "name": "Yes, please",
                            "code": "373066001",
                            "code_description": "Yes (qualifier value)",
                            "value": "1",
                        },
                        {
                            "name": "No, thank you",
                            "code": "373067005",
                            "code_description": "No (qualifier value)",
                            "value": "0",
                        },
                    ],
                },
                {
                    "content": "Do you consume alcohol?",
                    "code_system": "LOINC",
                    "code": "74013-4",
                    "code_description": "Alcoholic drinks per day",
                    "responses_code_system": "SNOMED",
                    "responses_type": "SING",
                    "display_result_in_social_history_section": True,
                    "responses": [
                        {
                            "name": "Never",
                            "code": "228274009",
                            "code_description": "Never drank alcohol",
                            "value": "0",
                        },
                        {
                            "name": "Occasionally",
                            "code": "228276006",
                            "code_description": "Occasional drinker",
                            "value": "1",
                        },
                        {
                            "name": "Regularly",
                            "code": "228273003",
                            "code_description": "Regular drinker",
                            "value": "2",
                        },
                    ],
                },
                {
                    "content": "How many alcoholic drinks do you have per week?",
                    "code_system": "LOINC",
                    "code": "11287-0",
                    "code_description": "Alcohol intake per week",
                    "responses_code_system": "INTERNAL",
                    "responses_type": "SING",
                    "enabled_behavior": "any",  # Any condition can be met
                    "enabled_conditions": [
                        {
                            "question_code": "74013-4",
                            "operator": "=",
                            "value_code": "228276006",  # "Occasionally"
                            "value_string": None,
                        },
                        {
                            "question_code": "74013-4",
                            "operator": "=",
                            "value_code": "228273003",  # "Regularly"
                            "value_string": None,
                        },
                    ],
                    "responses": [
                        {
                            "name": "1-3 drinks",
                            "code": "ALCOHOL_LOW",
                            "code_description": "Low alcohol consumption",
                            "value": "1",
                        },
                        {
                            "name": "4-7 drinks",
                            "code": "ALCOHOL_MODERATE",
                            "code_description": "Moderate alcohol consumption",
                            "value": "2",
                        },
                        {
                            "name": "8-14 drinks",
                            "code": "ALCOHOL_HIGH",
                            "code_description": "High alcohol consumption",
                            "value": "3",
                        },
                        {
                            "name": "More than 14 drinks",
                            "code": "ALCOHOL_VERY_HIGH",
                            "code_description": "Very high alcohol consumption",
                            "value": "4",
                        },
                    ],
                },
                {
                    "content": "Do you exercise regularly?",
                    "code_system": "LOINC",
                    "code": "89574-8",
                    "code_description": "Physical activity level",
                    "responses_code_system": "SNOMED",
                    "responses_type": "SING",
                    "responses": [
                        {
                            "name": "Yes, 3+ times per week",
                            "code": "256235009",
                            "code_description": "Exercises regularly",
                            "value": "2",
                        },
                        {
                            "name": "Sometimes, 1-2 times per week",
                            "code": "256236005",
                            "code_description": "Exercises occasionally",
                            "value": "1",
                        },
                        {
                            "name": "No",
                            "code": "256237001",
                            "code_description": "Does not exercise",
                            "value": "0",
                        },
                    ],
                },
                {
                    "content": "Any additional health concerns you'd like to discuss?",
                    "code_system": "INTERNAL",
                    "code": "FREE_TEXT_CONCERNS",
                    "code_description": "Additional health concerns",
                    "responses_code_system": "INTERNAL",
                    "responses_type": "TXT",
                    "responses": [
                        {
                            "name": "TXT",
                            "code": "FREE_TEXT_CONCERNS_RESPONSE",
                            "code_description": "Free text response for health concerns",
                            "value": "",
                        }
                    ],
                },
            ],
        }

        questionnaire = CreateQuestionnaire(questionnaire_config=config)
        return [questionnaire.apply()]
```

### API Endpoint for Creating Questionnaires

```python?partial=true
from typing import cast
from jsonschema import ValidationError

from canvas_sdk.effects import Effect
from canvas_sdk.effects.questionnaire import CreateQuestionnaire
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPIRoute
from canvas_sdk.questionnaires.utils import QuestionnaireConfig


class CreateQuestionnaireAPI(SimpleAPIRoute):
    """API endpoint that creates a questionnaire from JSON input."""

    PATH = "/create-questionnaire"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        """Simple API key authentication."""
        return credentials.key == self.secrets["api-key"]

    def post(self) -> list[Response | Effect]:
        """Create a questionnaire from JSON input."""
        try:
            questionnaire_data = cast(QuestionnaireConfig, self.request.json())
            effect = CreateQuestionnaire(questionnaire_config=questionnaire_data)

            return [
                effect.apply(),
                JSONResponse(
                    {
                        "message": "Questionnaire created successfully",
                        "questionnaire_name": questionnaire_data.get("name"),
                    }
                ),
            ]

        except ValidationError as e:
            return [
                JSONResponse(
                    {"error": "Invalid questionnaire configuration", "details": str(e)},
                    status_code=400,
                )
            ]

        except Exception as e:
            return [
                JSONResponse(
                    {"error": f"Failed to create questionnaire: {str(e)}"}, status_code=500
                )
            ]
```

## Validation

The `CreateQuestionnaire` effect performs comprehensive validation before execution:

1. **Schema Validation**: The questionnaire config is validated against the questionnaire JSON schema
2. **Required Fields**: Validates that all mandatory fields are provided for the questionnaire, questions, and responses
3. **Code Uniqueness**:
   - Ensures question codes are unique within the questionnaire
   - Ensures response codes are unique within each question
4. **Enumeration Validation**:
   - `form_type` must be one of: `QUES`, `SA`, `EXAM`, `ROS`
   - `responses_type` must be one of: `SING`, `MULT`, `TXT`
   - `code_system` and `responses_code_system` must be recognized coding systems
5. **Response Validation**:
   - For `TXT` type questions, validates that there is exactly one response
   - For `SING` and `MULT` types, validates that there is at least one response option
6. **Branching Logic Validation**:
   - Validates that `enabled_behavior` is either `all` or `any` when provided
   - Ensures referenced `question_code` values in conditions exist in the questionnaire
   - Validates that operators and value types are compatible
7. **Structural Validation**:
   - Ensures at least one question is provided
   - Validates proper nesting of questions and responses

## Error Handling

If validation fails, a `ValidationError` is raised with detailed error messages indicating which fields failed validation and why. The error messages follow the JSON schema validation format.

Common validation errors include:
- Missing required fields (e.g., `name`, `code`, `questions`)
- Invalid enumeration values (e.g., invalid `form_type`)
- Duplicate codes within the same scope
- Improperly structured free text questions
- Empty question or response lists
- Invalid code system values

## Complete Example JSON

Here's a complete example of a questionnaire configuration in JSON format (useful for API endpoints):

```json
{
  "name": "Test questionnaire",
  "form_type": "QUES",
  "code_system": "INTERNAL",
  "code": "TEST_QUES_001",
  "can_originate_in_charting": true,
  "prologue": "This is a sample questionnaire for testing purposes.",
  "display_results_in_social_history_section": true,
  "questions": [
    {
      "content": "This is a single select question",
      "code_system": "INTERNAL",
      "code": "QUESTIONNAIRE_Q1",
      "responses_code_system": "INTERNAL",
      "responses_type": "SING",
      "display_result_in_social_history_section": true,
      "responses": [
        {
          "name": "Single select Option 1",
          "code": "QUESTIONNAIRE_Q1_A1"
        },
        {
          "name": "Single select Option 2",
          "code": "QUESTIONNAIRE_Q1_A2"
        }
      ]
    },
    {
      "content": "This is a text question",
      "code_system": "INTERNAL",
      "code": "QUESTIONNAIRE_Q2",
      "responses_code_system": "INTERNAL",
      "responses_type": "TXT",
      "responses": [
        {
          "name": "TXT",
          "code": "QUESTIONNAIRE_Q2_A1"
        }
      ]
    },
    {
      "content": "This is a multiselect question",
      "code_system": "INTERNAL",
      "code": "QUESTIONNAIRE_Q3",
      "responses_code_system": "INTERNAL",
      "responses_type": "MULT",
      "responses": [
        {
          "name": "Multiselect Option 1",
          "code": "QUESTIONNAIRE_Q3_A1"
        },
        {
          "name": "Multiselect Option 2",
          "code": "QUESTIONNAIRE_Q3_A2"
        },
        {
          "name": "Multiselect Option 3",
          "code": "QUESTIONNAIRE_Q3_A3"
        }
      ]
    }
  ]
}
```

### Branching Logic Note

For questionnaires with conditional branching (where questions appear based on previous answers), add `enabled_behavior` and `enabled_conditions` to individual questions. See the [Questionnaire with Branching Logic](#questionnaire-with-branching-logic) example above for a complete implementation.

## Related Documentation

- [Questionnaires](/sdk/questionnaires/) - Creating questionnaires via YAML templates
- [Questionnaire Data Model](/sdk/data-questionnaire/) - Working with questionnaire data
- [Questionnaire Results](/sdk/effect-questionnaires/) - Creating questionnaire results and scoring
- [SimpleAPI](/sdk/handlers-simple-api-http/) - Creating HTTP API endpoints in plugins

<br/>
<br/>
<br/>
