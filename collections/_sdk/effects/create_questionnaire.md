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

While questionnaires can be created using YAML templates in the plugin manifest, the `CreateQuestionnaire` effect provides a way to create questionnaires programmatically. This is particularly useful when:

- Questionnaires need to be generated dynamically based on patient data or clinical context
- External systems need to create questionnaires via API integrations
- Questionnaire content needs to be customized per practice or provider
- Questionnaires are generated in response to specific clinical events

## Attributes

| Attribute                                  | Type                          | Description                                                                                                                                                    | Required |
|--------------------------------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| `name`                                     | `str`                         | Name of the questionnaire                                                                                                                                      | Yes      |
| `form_type`                                | `str`                         | Specifies the use case: `QUES` (Questionnaire), `SA` (Structured Assessment), `EXAM` (Physical Exam), or `ROS` (Review of Systems)                             | Yes      |
| `code_system`                              | `str`                         | The coding system used for the questionnaire (e.g., `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`, `CANVAS`)                                                  | Yes      |
| `code`                                     | `str`                         | The assigned code for the questionnaire                                                                                                                        | Yes      |
| `can_originate_in_charting`                | `bool`                        | Specifies if the questionnaire can be initiated from charting                                                                                                  | Yes      |
| `questions`                                | `list[QuestionnaireQuestion]` | List of questions in the questionnaire                                                                                                                         | Yes      |
| `prologue`                                 | `str` or `None`               | Text displayed at the beginning of the questionnaire to provide context to the user                                                                            | No       |
| `display_results_in_social_history_section`| `bool` or `None`              | Determines if completion information should be displayed in the Social History (SHX) section. Defaults to `False`                                              | No       |
| `expected_completion_time`                 | `float` or `None`             | Expected time in minutes to complete the questionnaire                                                                                                         | No       |
| `search_tags`                              | `str` or `None`               | Comma-separated tags for search functionality                                                                                                                  | No       |

## QuestionnaireQuestion

The `QuestionnaireQuestion` dataclass represents an individual question within a questionnaire.

### Attributes

| Attribute                                  | Type                             | Description                                                                                                      | Required |
|--------------------------------------------|----------------------------------|------------------------------------------------------------------------------------------------------------------|----------|
| `code_system`                              | `str`                            | The coding system for the question (e.g., `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`, `CANVAS`)              | Yes      |
| `code`                                     | `str`                            | The assigned code for the question. Must be unique within the questionnaire                                      | Yes      |
| `content`                                  | `str`                            | The question text displayed to the user                                                                          | Yes      |
| `responses_code_system`                    | `str`                            | The coding system for responses (e.g., `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`)                           | Yes      |
| `responses_type`                           | `str`                            | Response type: `SING` (Single Select), `MULT` (Multi Select), `TXT` (Free Text)                                  | Yes      |
| `responses`                                | `list[QuestionnaireResponse]`    | List of possible responses for the question                                                                      | Yes      |
| `display_result_in_social_history_section` | `bool` or `None`                 | Determines if the response should be shown in the Social History (SHX) section. Defaults to `False`              | No       |

## QuestionnaireResponse

The `QuestionnaireResponse` dataclass represents a possible response option for a question.

### Attributes

| Attribute | Type            | Description                                                                                                                | Required |
|-----------|-----------------|-----------------------------------------------------------------------------------------------------------------------------|----------|
| `name`    | `str`           | For `SING`/`MULT`, the text displayed for the response option. For `TXT` type questions, should be set to "TXT"            | Yes      |
| `code`    | `str`           | The assigned code for the response. Must be unique within the question                                                     | Yes      |
| `value`   | `str` or `None` | For `SING`/`MULT`, optional numerical value for scoring. Leave blank or omit if no scoring is desired                     | No       |

## Implementation Details

- **Validation**: Validates that all required fields are provided and conform to expected formats
- **Code Uniqueness**: Ensures question codes are unique within the questionnaire and response codes are unique within each question
- **Form Type Validation**: Ensures `form_type` is one of: `QUES`, `SA`, `EXAM`, or `ROS`
- **Response Type Validation**: Ensures `responses_type` is one of: `SING`, `MULT`, or `TXT`
- **Code System Validation**: Validates that code systems are recognized (e.g., `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`, `CANVAS`)

## Example Usage

### Basic Questionnaire Creation

```python?partial=true
from canvas_sdk.effects.questionnaire import CreateQuestionnaire, QuestionnaireQuestion, QuestionnaireResponse
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType


class DynamicQuestionnaireCreator(BaseHandler):
    """
    Create a questionnaire programmatically in response to a patient creation event.
    """
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_CREATED)]

    def compute(self):
        # Create a simple pain assessment questionnaire
        questionnaire = CreateQuestionnaire(
            name="Pain Assessment",
            form_type="QUES",
            code_system="LOINC",
            code="72514-3",
            can_originate_in_charting=True,
            prologue="Please answer the following questions about your pain level.",
            display_results_in_social_history_section=True,
            questions=[
                QuestionnaireQuestion(
                    code_system="LOINC",
                    code="72514-3",
                    content="What is your current pain level?",
                    responses_code_system="LOINC",
                    responses_type="SING",
                    display_result_in_social_history_section=True,
                    responses=[
                        QuestionnaireResponse(
                            name="No pain",
                            code="LA6568-5",
                            value="0"
                        ),
                        QuestionnaireResponse(
                            name="Mild pain",
                            code="LA6569-3",
                            value="3"
                        ),
                        QuestionnaireResponse(
                            name="Moderate pain",
                            code="LA6570-1",
                            value="5"
                        ),
                        QuestionnaireResponse(
                            name="Severe pain",
                            code="LA6571-9",
                            value="8"
                        ),
                    ]
                )
            ]
        )

        return [questionnaire.create()]
```

### Multi-Question Questionnaire with Different Response Types

```python?partial=true
from canvas_sdk.effects.questionnaire import CreateQuestionnaire, QuestionnaireQuestion, QuestionnaireResponse
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType


class ComprehensiveQuestionnaireCreator(BaseHandler):
    """
    Create a comprehensive questionnaire with multiple question types.
    """
    RESPONDS_TO = [EventType.Name(EventType.PLUGIN_INSTALLED)]

    def compute(self):
        questionnaire = CreateQuestionnaire(
            name="Patient Health Screening",
            form_type="SA",
            code_system="INTERNAL",
            code="PATIENT_HEALTH_SCREEN_V1",
            can_originate_in_charting=True,
            prologue="This screening will help us understand your current health status.",
            expected_completion_time=5.0,
            search_tags="health,screening,intake",
            questions=[
                # Single select question
                QuestionnaireQuestion(
                    code_system="INTERNAL",
                    code="EXERCISE_FREQ",
                    content="How often do you exercise per week?",
                    responses_code_system="INTERNAL",
                    responses_type="SING",
                    responses=[
                        QuestionnaireResponse(name="Never", code="EX_NEVER", value="0"),
                        QuestionnaireResponse(name="1-2 times", code="EX_1_2", value="1"),
                        QuestionnaireResponse(name="3-4 times", code="EX_3_4", value="2"),
                        QuestionnaireResponse(name="5+ times", code="EX_5_PLUS", value="3"),
                    ]
                ),
                # Multi select question
                QuestionnaireQuestion(
                    code_system="INTERNAL",
                    code="CHRONIC_CONDITIONS",
                    content="Do you have any of the following conditions? (Select all that apply)",
                    responses_code_system="INTERNAL",
                    responses_type="MULT",
                    display_result_in_social_history_section=True,
                    responses=[
                        QuestionnaireResponse(name="Diabetes", code="COND_DIABETES"),
                        QuestionnaireResponse(name="Hypertension", code="COND_HYPERTENSION"),
                        QuestionnaireResponse(name="Asthma", code="COND_ASTHMA"),
                        QuestionnaireResponse(name="Heart Disease", code="COND_HEART"),
                        QuestionnaireResponse(name="None", code="COND_NONE"),
                    ]
                ),
                # Free text question
                QuestionnaireQuestion(
                    code_system="INTERNAL",
                    code="ADDITIONAL_NOTES",
                    content="Please provide any additional information about your health:",
                    responses_code_system="INTERNAL",
                    responses_type="TXT",
                    responses=[
                        QuestionnaireResponse(
                            name="TXT",
                            code="ADDITIONAL_NOTES_TEXT"
                        )
                    ]
                ),
            ]
        )

        return [questionnaire.create()]
```

### Dynamic Questionnaire Based on Patient Data

```python?partial=true
from canvas_sdk.effects.questionnaire import CreateQuestionnaire, QuestionnaireQuestion, QuestionnaireResponse
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.condition import Condition


class PatientSpecificQuestionnaire(BaseHandler):
    """
    Create a questionnaire dynamically based on patient's existing conditions.
    """
    RESPONDS_TO = [EventType.Name(EventType.APPOINTMENT_CREATED)]

    def compute(self):
        # Get patient information
        patient_id = self.event.context.get("patient_id")
        if not patient_id:
            return []

        patient = Patient.objects.get(id=patient_id)
        conditions = Condition.objects.filter(patient=patient, clinicalStatus="active")

        # Build questions based on active conditions
        questions = []
        
        if conditions.filter(coding__code="E11").exists():  # Diabetes
            questions.append(
                QuestionnaireQuestion(
                    code_system="INTERNAL",
                    code="DIABETES_CHECK",
                    content="Have you been checking your blood sugar regularly?",
                    responses_code_system="INTERNAL",
                    responses_type="SING",
                    responses=[
                        QuestionnaireResponse(name="Yes, daily", code="DIABETES_YES_DAILY", value="3"),
                        QuestionnaireResponse(name="Yes, weekly", code="DIABETES_YES_WEEKLY", value="2"),
                        QuestionnaireResponse(name="Occasionally", code="DIABETES_OCCASIONALLY", value="1"),
                        QuestionnaireResponse(name="No", code="DIABETES_NO", value="0"),
                    ]
                )
            )

        if conditions.filter(coding__code="I10").exists():  # Hypertension
            questions.append(
                QuestionnaireQuestion(
                    code_system="INTERNAL",
                    code="BP_CHECK",
                    content="Have you been monitoring your blood pressure at home?",
                    responses_code_system="INTERNAL",
                    responses_type="SING",
                    responses=[
                        QuestionnaireResponse(name="Yes, regularly", code="BP_YES", value="1"),
                        QuestionnaireResponse(name="No", code="BP_NO", value="0"),
                    ]
                )
            )

        # Only create questionnaire if there are relevant questions
        if not questions:
            return []

        questionnaire = CreateQuestionnaire(
            name=f"Pre-Visit Assessment for {patient.first_name} {patient.last_name}",
            form_type="QUES",
            code_system="INTERNAL",
            code=f"PREVST_ASSESS_{patient.id}",
            can_originate_in_charting=True,
            prologue="Please complete this brief assessment before your appointment.",
            questions=questions
        )

        return [questionnaire.create()]
```

## Validation

The `CreateQuestionnaire` effect performs comprehensive validation before execution:

1. **Required Fields**: Validates that all mandatory fields are provided for the questionnaire, questions, and responses
2. **Code Uniqueness**:
   - Ensures question codes are unique within the questionnaire
   - Ensures response codes are unique within each question
3. **Enumeration Validation**:
   - `form_type` must be one of: `QUES`, `SA`, `EXAM`, `ROS`
   - `responses_type` must be one of: `SING`, `MULT`, `TXT`
   - `code_system` and `responses_code_system` must be recognized coding systems
4. **Response Validation**:
   - For `TXT` type questions, validates that there is exactly one response with name "TXT"
   - For `SING` and `MULT` types, validates that there is at least one response option
5. **Structural Validation**:
   - Ensures at least one question is provided
   - Validates proper nesting of questions and responses

## Error Handling

If validation fails, a `ValidationError` is raised with detailed error messages indicating which fields failed validation and why. Error messages are aggregated to provide comprehensive feedback about all validation failures at once.

Common validation errors include:
- Missing required fields
- Invalid enumeration values
- Duplicate codes within the same scope
- Improperly structured free text questions
- Empty question or response lists

## Related Documentation

- [Questionnaires](/sdk/questionnaires/) - Creating questionnaires via YAML templates
- [Questionnaire Data Model](/sdk/data-questionnaire/) - Working with questionnaire data
- [Questionnaire Results](/sdk/effect-questionnaires/) - Creating questionnaire results and scoring

<br/>
<br/>
<br/>

