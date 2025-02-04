---
title: "Questionnaires"
slug: "questionnaires"
excerpt: "Build and install a Questionnaire."
hidden: false
---

Questionnaires are a structured set of questions intended to guide the collection of answers from end-users.

## How to build and install a Questionnaire

To include a questionnaire in your plugin, add a reference to its YAML template inside the `questionnaires` section of the `CANVAS_MANIFEST.json` file.

### Example Manifest Configuration

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "example_questionnaire",
    "description": "Edit the description in CANVAS_MANIFEST.json",
    "components": {
        "protocols": [],
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
    "secrets": [],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

### Key Properties
- **`template`**: The relative path to the YAML file defining the questionnaire.


The questionnaire YAML file should adhere to the JSON schema found [here](https://raw.githubusercontent.com/canvas-medical/canvas-plugins/main/schemas/questionnaire.json) that is also listed below.

## JSON Schema Reference

### Questionnaire Settings

| Property                                    | Description                                                                                                                                | Required |
|---------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|----------|
| `name`                                      | Name of the Questionnaire.                                                                                                                 | Yes      |
| `form_type`                                 | Specifies the use case: `QUES` (Questionnaire), `SA` (Structured Assessment), `EXAM` (Physical Exam), or `ROS` (Review of Systems).        | Yes      |
| `code_system`                               | The coding system used for the questionnaire, e.g., `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`, `CANVAS`.                              | Yes      |
| `code`                                      | The assigned code for the questionnaire (e.g., `72109-2`).                                                                                 | Yes      |
| `can_originate_in_charting`                 | Specifies if the questionnaire can be initiated from charting. Values: `TRUE` or `FALSE`.                                                  | Yes      |
| `prologue`                                  | Text displayed at the beginning of the questionnaire to provide context to the user.                                                       | No       |
| `display_results_in_social_history_section` | Determines if completion information should be displayed in the Social History (SHX) section. Values: `TRUE` or `FALSE`. Default: `FALSE`. | No       |
| `questions`                                 | List of questions in the questionnaire. See below.                                                                                         | Yes      |

### Question Settings

| Property                                   | Description                                                                                                                  | Required |
|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|----------|
| `code_system`                              | The coding system for the question. Options: `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`, `CANVAS`.                       | Yes      |
| `code`                                     | The assigned code for the question. Example: `44250-9`. Codes should be unique within the same questionnaire.                | Yes      |
| `code_description`                         | A description of the assigned code.                                                                                          | No       |
| `content`                                  | The text displayed when the command is printed.                                                                              | Yes      |
| `responses_code_system`                    | The coding system for responses. Options: `SNOMED`, `LOINC`, `INTERNAL`, `ICD-10`, `CPT`.                                    | Yes      |
| `responses_type`                           | Response type: `SING` (Single Select), `MULT` (Multi Select), `TXT` (Free Text).                                             | Yes      |
| `display_result_in_social_history_section` | Determines if the response should be shown in the Social History (SHX) section. Values: `TRUE` or `FALSE`. Default: `FALSE`. | No       |
| `responses`                                | List of responses for the question. See below.                                                                               | Yes      |

### Response Settings

| Property           | Description                                                                                                          | Required |
|--------------------|----------------------------------------------------------------------------------------------------------------------|----------|
| `name`             | For `SING`/`MULT`, this is the text that will be displayed for each response. For `TXT`, enter "TXT".                | Yes      |
| `code`             | The assigned code for the response. Example: `Z759`. No response codes should be reused within the same question.    | Yes      |
| `code_description` | A description of the assigned code.                                                                                  | No       |
| `value`            | For `SING`/`MULT`, leave blank if no scoring is desired. If scoring is desired, insert the numerical value assigned. | No       |


### Example Questionnaire Definition

```yaml
name: Example Name
form_type: QUES
code_system: LOINC
code: QUES_EXAMPLE_NAME
can_originate_in_charting: true
prologue: This is an example of a structured assessment with single select, multiselect, and free text responses.
questions:
  - content: "This is question #1"
    code_system: CPT
    code: H0005
    code_description: ""
    responses_code_system: INTERNAL
    responses_type: SING
    display_result_in_social_history_section: true
    responses:
      - name: "Single select response #1"
        code: QUES_EXAMPLE_NAME_Q1_A1
        code_description: ''
        value: "1"
      - name: "Single select response #2"
        code: QUES_EXAMPLE_NAME_Q1_A2
        code_description: ''
        value: "0"
      - name: "Single select response #3"
        code: QUES_EXAMPLE_NAME_Q1_A3
        code_description: ''
        value: "0"
  - content: "This is question #2"
    code_system: INTERNAL
    code: QUES_EXAMPLE_NAME_Q2
    code_description: ""
    responses_code_system: ICD-10
    responses_type: MULT
    display_result_in_social_history_section: true
    responses:
      - name: "Multi select response #1"
        code: F1910
        code_description: ''
        value: "0"
      - name: "Multi select response #2"
        code: QUES_EXAMPLE_NAME_Q1_A1
        code_description: ''
        value: "2"
      - name: "Multi select response #3"
        code: QUES_EXAMPLE_NAME_Q1_A2
        code_description: ''
        value: "0"
  - content: "This is question #3"
    code_system: INTERNAL
    code: QUES_EXAMPLE_NAME_Q3
    code_description: ""
    responses_code_system: INTERNAL
    responses_type: TXT
    display_result_in_social_history_section: true
    responses:
      - name: "Free text response"
        code: QUES_EXAMPLE_NAME_Q3_A1
        code_description: ''
        value: "This is a default pre-populated free text response."
```

## Load Questionnaire definition from YAML file

You can use the `questionnaire_from_yaml` function from `canvas_sdk.questionnaires` within your plugin to load a questionnaire definition from a YAML file. 
The function takes the path to the YAML file as an argument and returns a dictionary containing the questionnaire definition.

```python
def questionnaire_from_yaml(questionnaire_name: str, **kwargs: Any) -> QuestionnaireConfig | None:
    """Load a Questionnaire configuration from a YAML file.

    Args:
        questionnaire_name (str): The path to the questionnaire file, relative to the plugin package.
            If the path starts with a forward slash ("/"), it will be stripped during resolution.
        kwargs (Any): Additional keyword arguments.

    Returns:
        QuestionnaireConfig: The loaded Questionnaire configuration.

    Raises:
        FileNotFoundError: If the questionnaire file does not exist within the plugin's directory
            or if the resolved path is invalid.
        PermissionError: If the resolved path is outside the plugin's directory.
        ValidationError: If the questionnaire file does not conform to the JSON schema.
    """
````
