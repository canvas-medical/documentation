---
title: "Questionnaire"
slug: "data-questionnaire"
excerpt: "Canvas SDK Questionnaire"
hidden: false
---

## Introduction

The `Questionnaire` model represents a structured set of questions intended to guide the collection of answers from end-users.

The `Interview` model represents answers to a structured set of questions represented by a `Questionnaire`.

## Basic usage

To get a questionnaire or interview by identifier, use the `get` method on the `Questionnaire` or `Interview` model managers:

```python
from canvas_sdk.v1.data.questionnaire import Questionnaire
from canvas_sdk.v1.data.interview import Interview

questionnaire = Questionnaire.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
interview = Interview.objects.get(id="75df6d7f-d58d-443b-9fa0-ce43b4d7b2a0")
```

If you have a patient object, the interviews for a patient can be accessed with the `interviews` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
interviews = patient.interviews.all()
```

If you have a patient ID, you can get the interviews for the patient with the `for_patient` method on the `Interview` model manager:

```python
from canvas_sdk.v1.data.interview import Interview

patient_id = "1eed3ea2a8d546a1b681a2a45de1d790"
interviews = Interview.objects.for_patient(patient_id)
```

## Questionnaire questions

The questions for a questionnaire can be accessed with the `questions` attribute on an `Questionnaire` object:

```python
from canvas_sdk.v1.data.questionnaire import Questionnaire
from logger import log

questionnaire = Questionnaire.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for question in questionnaire.questions.all():
    log.info(f"system: {question.code_system}")
    log.info(f"code: {question.code}")
    log.info(f"name: {question.name}")
```

## Interview responses

The interview responses for an interview can be accessed with the `interview_responses` attribute on an `Interview` object:

```python
from canvas_sdk.v1.data.interview import Interview
from logger import log

interview = Interview.objects.get(id="75df6d7f-d58d-443b-9fa0-ce43b4d7b2a0")

for interview_response in interview.interview_responses.all():
    log.info(f"response option: {interview_response.response_option_value}")
```

## Filtering

Questionnaires and interviews can be filtered by any attribute that exists on the models.

Filtering for questionnaires and interviews is done with the `filter` method on the `Questionnaire` and `Interview` model managers.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.questionnaire import Questionnaire
from canvas_sdk.v1.data.interview import Interview

questionnaires = Questionnaire.objects.filter(name="Tobacco")
interviews = Interview.objects.filter(progress_status="F")
```

### By ValueSet

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering:

```python
from canvas_sdk.v1.data.questionnaire import Questionnaire
from canvas_sdk.value_set.v2022.assessment import TobaccoUseScreening

questionnaires = Questionnaire.objects.find(TobaccoUseScreening)
```

## Attributes

### ResponseOptionSet
| Field Name  | Type     |
|-------------|----------|
| dbid        | Integer  |
| created     | DateTime |
| modified    | DateTime |
| status      | String   |
| name        | String   |
| code_system | String   |
| code        | String   |
| type        | String   |
| use_in_shx  | Boolean  |

### ResponseOption
| Field Name          | Type                                    |
|---------------------|-----------------------------------------|
| dbid                | Integer                                 |
| created             | DateTime                                |
| modified            | DateTime                                |
| status              | String                                  |
| name                | String                                  |
| code                | String                                  |
| code_description    | String                                  |
| value               | String                                  |
| response_option_set | [ResponseOptionSet](#responseoptionset) |
| ordering            | Integer                                 |

### Question
| Field Name          | Type                                    |
|---------------------|-----------------------------------------|
| id                  | UUID                                    |
| dbid                | Integer                                 |
| created             | DateTime                                |
| modified            | DateTime                                |
| status              | String                                  |
| name                | String                                  |
| response_option_set | [ResponseOptionSet](#responseoptionset) |
| acknowledge_only    | Boolean                                 |
| show_prologue       | Boolean                                 |
| code_system         | String                                  |
| code                | String                                  |

### Questionnaire
| Field Name                | Type     |
|---------------------------|----------|
| id                        | UUID     |
| dbid                      | Integer  |
| created                   | DateTime |
| modified                  | DateTime |
| status                    | String   |
| name                      | String   |
| expected_completion_time  | Float    |
| can_originate_in_charting | Boolean  |
| use_case_in_charting      | String   |
| scoring_function_name     | Text     |
| scoring_code_system       | String   |
| scoring_code              | String   |
| code_system               | String   |
| code                      | String   |
| search_tags               | String   |
| questions                 | Question |
| use_in_shx                | Boolean  |
| carry_forward             | Text     |

### QuestionnaireQuestionMap
| Field Name    | Type                            |
|---------------|---------------------------------|
| dbid          | Integer                         |
| created       | DateTime                        |
| modified      | DateTime                        |
| status        | String                          |
| questionnaire | [Questionnaire](#questionnaire) |
| question      | [Question](#question)           |

### Interview
| Field Name           | Type                                  |
|----------------------|---------------------------------------|
| id                   | UUID                                  |
| dbid                 | Integer                               |
| deleted              | Boolean                               |
| committer            | CanvasUser                            |
| entered_in_error     | CanvasUser                            |
| status               | String                                |
| name                 | String                                |
| language_id          | Integer                               |
| use_case_in_charting | String                                |
| patient              | [Patient](/sdk/data-patient/#patient) |
| note_id              | Integer                               |
| appointment_id       | Integer                               |
| questionnaires       | Questionnaire                         |
| progress_status      | String                                |
| created              | DateTime                              |
| modified             | DateTime                              |

### InterviewQuestionResponse
| Field Name            | Type                              |
|-----------------------|-----------------------------------|
| dbid                  | Integer                           |
| created               | DateTime                          |
| modified              | DateTime                          |
| status                | String                            |
| interview             | [Interview](#interview)           |
| questionnaire         | [Questionnaire](#questionnaire)   |
| question              | [Question](#question)             |
| response_option       | [ResponseOption](#responseoption) |
| response_option_value | Text                              |
| questionnaire_state   | Text                              |
| interview_state       | Text                              |
| comment               | String                            |
