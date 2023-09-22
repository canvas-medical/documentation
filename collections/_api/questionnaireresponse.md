---
title: QuestionnaireResponse
sections:
  - type: section
    blocks:
      - type: apidoc
        name: QuestionnaireResponse
        article: "a"
        description: >-
           [FHIR:](https://hl7.org/fhir/R4/questionnaireresponse.html) A structured set of questions and their answers. The questions are ordered and grouped into coherent subsets, corresponding to the structure of the grouping of the questionnaire being responded to.<br><br> Questionnaires in Canvas are used to capture structured data. They are fully customizable and support many use cases. Learn how to configure questionnaires in your instance [here](/documentation/questionnaires). Once loaded to Canvas, you will need the Questionnaire ID to interact with this resource. You can leverage our Questionnaire Search to do so.<br><br>When building your questionnaires, make sure to follow our best practices around codes and code systems. The tool to load your questionnaires now has validation to ensure unique pairings where necessary. 
        attributes:
          - name: id
            description: >-
              The identifier of the questionnaire response
            type: string
            required: true
          - name: resourceType
            type: string
            description:
                This should be hardcoded to QuestionnaireResponse
            required: true
          - name: questionnaire
            type: string
            required: true
            description:
                Canvas questionnaire resource that the responses are for, formatted like "Questionnaire/ac1da1a4-ccc4-492e-a9e0-7f70a58c2129".
            create_description:
                Canvas questionnaire resource that the responses are for, formatted like "Questionnaire/ac1da1a4-ccc4-492e-a9e0-7f70a58c2129". You can obtain this id by using our [Questionnaire Search](/api/questionnaire/#search)
          - name: status
            type: string
            required: true
            create_description: Canvas only acknowledges a ‘completed’ status. All QuestionnaireResponse messages should contain status ‘completed’.
          - name: subject
            type: string
            required: true
            description: The subject of the questions. Supports a patient reference. 
          - name: encounter
            type: string
            description: Encounter created as part of.
            Create_description: Adding an encounter reference will import the QuestionnaireResponse into an existing note. Without one, a Data Import note will be added to the timeline in a locked state 
          - name: authored
            type: string
            required: true
            description: The UTC datetime string for when the questionnaire responses were provided, iso8601 format. 
            create_description: The UTC datetime string for when the questionnaire responses were provided, iso8601 format. If omitted from the body, the current timestamp at data ingestion will be used
          - name: author
            type: string
            required: true
            description:
                A reference to the person that filled out the questionnaire.
            create_description:
                Canvas notes are intended to be multi-author. You can reference either the patient or practitioner. The audit tooltip on the command will display the author as the patient or staff member. If not included, the built in automation user, "Canvas Bot" will be used instead. ## Is this acurate if required is true ## 
          - name: item
            type: string
            required: true
            description: >-
                A list of one or more questions and how they were answered. Each item object in the list should contain:<br><br>**`linkId`:** [Required] A Canvas assigned identifier that uniquely identifies this question in Canvas. This linkId must only occur at most once in the payload.<br>**`text`:** Human readable text of the question. Not stored but can be helpful to include for troubleshooting.<br> **`answer`:** [Required] A list of one or more answers to this question. Canvas supports three question types: Free text, Single Response, and Multi Response.<br><br> **Free text** answers (Questionnaire item type = "text") will contain a single object containing a valueString field with the response text.<br><br> For **single** & **multiselect** answers (Questionnaire item `type` = "choice" and `repeats` is "false for single and "true" for multi), the list will have one or more objects containing:<br><br>**`code`:** [required] Value that can uniquely identify this answer within the associated <br>**`display`:** [required] Text of answer that was selected<br>**`system`:** [required] Coding system where the `code` comes from. Currently we only support specific system's in Canvas through our FHIR endpoints. Here is the mapping of system uri in FHIR to systems in Canvas:<br><br>**SNOMED:** http://snomed.info/sct<br>**LOINC:** http://loinc.org<br>**Canvas:** http://canvasmedical.com<br>**CPT:** http://www.ama-assn.org/go/cpt<br>**ICD-10:** http://hl7.org/fhir/sid/icd-10<br>**Internal:** http://schemas.[instance_name].canvasmedical.com/fhir/systems/internal<br><br>
            create_description: >-
                A list of one or more questions and how they were answered. If a question is omitted it will be left unanswered in Canvas. However, if it is a questionnaire tied to a scoring function, Canvas requires all questions to be answered in order to accurately score the questionnaire. <br> <br> Perform a [QuestionnaireSearch](/api/Questionnaire/#search) in order to know each question's attributes to fill in below. Each item object in the list should contain:<br><br>**`linkId`:** [Required] A Canvas assigned identifier that uniquely identifies this question in Canvas. This linkId must only occur at most once in the payload.<br>**`text`:** Human readable text of the question. Not stored but can be helpful to include for troubleshooting.<br> **`answer`:** [Required] A list of one or more answers to this question. Canvas supports three question types: Free text, Single Response, and Multi Response.<br><br> **Free text** answers (Questionnaire item type = "text") will contain a single object containing a valueString field with the response text.<br><br> For **single** & **multiselect** answers (Questionnaire item `type` = "choice" and `repeats` is "false for single and "true" for multi), the list will have one or more objects containing:<br><br>**`code`:** [required] Value that can uniquely identify this answer within the associated <br>**`display`:** [required] Text of answer that was selected<br>**`system`:** [required] Coding system where the `code` comes from. Currently we only support specific system's in Canvas through our FHIR endpoints. Here is the mapping of system uri in FHIR to systems in Canvas:<br><br>**SNOMED:** http://snomed.info/sct<br>**LOINC:** http://loinc.org<br>**Canvas:** http://canvasmedical.com<br>**CPT:** http://www.ama-assn.org/go/cpt<br>**ICD-10:** http://hl7.org/fhir/sid/icd-10<br>**Internal:** http://schemas.[instance_name].canvasmedical.com/fhir/systems/internal<br><br><b>⚠ Validation</b><br><br> The system in the ValueCoding answer needs to match the system that the question specified in the Questionnaire Search Response. If it does not you will see the message: `Question expects answer of code system {system} but {coding['code_system']} was given`<br><br>If a code is passed that does not exist for that question in Canvas, you will see the following message: `Question received an invalid response option code: {coding['code']}` <br><br> For single or free text questions, if the length of answer is greater than one, you will see the message `Question of type {_type} is expecting at most one answer` <br><br> For free text questions, the answer object needs to include ValueString or you will see this message: `Question of type TXT expects a valueString answer`<br><br> For single or multi select questions, the answer object(s) need to include ValueCoding or you will see: `Question of type {_type} expects a valueCoding answer`
          - name: extension
            type: array
            required: true
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: authored
            type: string
            description: An operand and a date field in the format YYYY-MM-DD. eq, gt, ge, lt, and le are currently supported operands. Can be sent more than once to search within a range. example - "/QuestionnaireResponse?authored=ge2021-09-16&authored=le2021-10-01"
          - name: patient
            type: string
            description: The patient that is the subject of the questionnaire response
          - name: questionnaire
            type: string
            description: The questionnaire that was used to generate the questionnaire response
        endpoints: [create, read, search]
        read:
          responses: [200, 404]
          example_request: questionnaire-response-read-request
          example_response: questionnaire-response-read-response
        search:
          responses: [200, 400]
          description: >-
            <b> Authored Search Param </b> <br><br> We support ways to search by date:<br><br>Search for QuestionnaireResponses anytime during this day: **eq2021-09-01**  <br>Search for QuestionnaireResponses on or after this day: **ge2021-09-16**<br>Search for QuestionnaireResponses after this day: **gt2021-09-16**<br>Search for QuestionnaireResponses on or before this day: **le2021-10-01** <br>Search for QuestionaireResponses before this day: **lt2021-10-01**<br><br>


          example_request: questionnaire-response-search-request
          example_response: questionnaire-response-search-response
        create:
          description: >-
          Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location: header`. You will use this for subsequent requests that reference this questionnaire response.
          responses: [201, 400]
          example_request: questionnaire-response-create-request
          example_response: questionnaire-response-create-response
          
---
<div id="questionnaire-response-read-request">
{% tabs questionnaire-response-read-request %}
{% tab questionnaire-response-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/QuestionnaireResponse/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab questionnaire-response-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/QuestionnaireResponse/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="questionnaire-response-read-response">
{% tabs questionnaire-response-read-response %}
{% tab questionnaire-response-read-response 200 %}
```json
{
    "resourceType": "QuestionnaireResponse",
    "id": "9a884b0a-ed2c-448f-b186-56a7813f01d4",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/questionnaire-permalink",
            "valueString": "https://training.canvasmedical.com/permalinks/v1/SW50ZXJ2aWV3OjUxOjcwOA=="
        }
    ],
    "questionnaire": "Questionnaire/e26d16dd-c54b-4909-a016-a508c73a3448",
    "status": "completed",
    "subject": {
        "reference": "Patient/51af861606aa4fb1b2cf8f2716008267",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/4759f784-e9d2-4ebb-b73f-968c435d620a",
        "type": "Encounter"
    },
    "authored": "2021-09-16T17:15:00.709137+00:00",
    "author": {
        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
        "type": "Practitioner"
    },
    "item": [
        {
            "linkId": "d9fc7bbe-ddca-4bf3-ae32-c85e2c95cd8e",
            "text": "Feeling nervous, anxious or on edge?",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "404684003",
                        "display": "Several days"
                    }
                }
            ]
        },
        {
            "linkId": "d07f2e92-d6c1-469c-9d8a-9a3dfc0a00bf",
            "text": "Not being able to control or stop worrying?",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "404684003",
                        "display": "Several days"
                    }
                }
            ]
        },
        {
            "linkId": "7e391e73-d4e5-496d-b3c7-611880aa3dc7",
            "text": "Worrying too much about different things?",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "404684003",
                        "display": "More than half the days"
                    }
                }
            ]
        },
        {
            "linkId": "4dd15d5d-2b77-4f69-bd99-2d36e2b20267",
            "text": "Trouble relaxing?",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "404684003",
                        "display": "Several days"
                    }
                }
            ]
        },
        {
            "linkId": "7b69f499-ed9e-4c02-b309-cebc1a56fc59",
            "text": "Being so restless that it is hard to sit still?",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "404684003",
                        "display": "Several days"
                    }
                }
            ]
        },
        {
            "linkId": "55526753-4540-4320-9643-9e25ccba64d2",
            "text": "Becoming easily annoyed or irritable?",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "404684003",
                        "display": "Several days"
                    }
                }
            ]
        },
        {
            "linkId": "4edd55c1-a80b-4a03-a52a-fd975248aebc",
            "text": "Being afraid as if something awful might happen?",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "404684003",
                        "display": "Several days"
                    }
                }
            ]
        },
        {
            "linkId": "44848247-57a2-463a-a4a7-60b3e3a95463",
            "text": "How difficult have these problems made it for you to do you work, take care of things at home or get along with other people?",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "404684003",
                        "display": "Somewhat difficult"
                    }
                }
            ]
        }
    ]
}
```
{% endtab %}
{% tab questionnaire-response-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Resource not found"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div

<div id="questionnaire-response-search-request">
{% tabs questionnaire-response-search-request %}
{% tab questionnaire-response-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/QuestionnaireResponse?questionnaire=Questionnaire/e26d16dd-c54b-4909-a016-a508c73a3448&authored=ge2021-09-16&authored=le2021-10-01"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab questionnaire-response-search-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/QuestionnaireResponse?questionnaire=Questionnaire/e26d16dd-c54b-4909-a016-a508c73a3448&authored=ge2021-09-16&authored=le2021-10-01' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="questionnaire-response-search-response">
{% tabs questionnaire-response-search-response %}
{% tab questionnaire-response-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/QuestionnaireResponse?questionnaire=Questionnaire%2Fe26d16dd-c54b-4909-a016-a508c73a3448&authored=ge2021-09-16&authored=le2021-10-01&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/QuestionnaireResponse?questionnaire=Questionnaire%2Fe26d16dd-c54b-4909-a016-a508c73a3448&authored=ge2021-09-16&authored=le2021-10-01&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/QuestionnaireResponse?questionnaire=Questionnaire%2Fe26d16dd-c54b-4909-a016-a508c73a3448&authored=ge2021-09-16&authored=le2021-10-01&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "QuestionnaireResponse",
                "id": "9a884b0a-ed2c-448f-b186-56a7813f01d4",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/questionnaire-permalink",
                        "valueString": "https://training.canvasmedical.com/permalinks/v1/SW50ZXJ2aWV3OjUxOjcwOA=="
                    }
                ],
                "questionnaire": "Questionnaire/e26d16dd-c54b-4909-a016-a508c73a3448",
                "status": "completed",
                "subject": {
                    "reference": "Patient/51af861606aa4fb1b2cf8f2716008267",
                    "type": "Patient"
                },
                "encounter": {
                    "reference": "Encounter/4759f784-e9d2-4ebb-b73f-968c435d620a",
                    "type": "Encounter"
                },
                "authored": "2021-09-16T17:15:00.709137+00:00",
                "author": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                },
                "item": [
                    {
                        "linkId": "d9fc7bbe-ddca-4bf3-ae32-c85e2c95cd8e",
                        "text": "Feeling nervous, anxious or on edge?",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "404684003",
                                    "display": "Several days"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "d07f2e92-d6c1-469c-9d8a-9a3dfc0a00bf",
                        "text": "Not being able to control or stop worrying?",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "404684003",
                                    "display": "Several days"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "7e391e73-d4e5-496d-b3c7-611880aa3dc7",
                        "text": "Worrying too much about different things?",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "404684003",
                                    "display": "More than half the days"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "4dd15d5d-2b77-4f69-bd99-2d36e2b20267",
                        "text": "Trouble relaxing?",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "404684003",
                                    "display": "Several days"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "7b69f499-ed9e-4c02-b309-cebc1a56fc59",
                        "text": "Being so restless that it is hard to sit still?",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "404684003",
                                    "display": "Several days"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "55526753-4540-4320-9643-9e25ccba64d2",
                        "text": "Becoming easily annoyed or irritable?",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "404684003",
                                    "display": "Several days"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "4edd55c1-a80b-4a03-a52a-fd975248aebc",
                        "text": "Being afraid as if something awful might happen?",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "404684003",
                                    "display": "Several days"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "44848247-57a2-463a-a4a7-60b3e3a95463",
                        "text": "How difficult have these problems made it for you to do you work, take care of things at home or get along with other people?",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "404684003",
                                    "display": "Somewhat difficult"
                                }
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab questionnaire-response-search-response 400 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "invalid",
      "details": {
        "text": "Bad request"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="questionnaire-response-create-request">
{% tabs questionnaire-response-create-request %}
{% tab questionnaire-response-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/QuestionnaireResponse"

payload = {
    "resourceType": "QuestionnaireResponse",
    "questionnaire": "Questionnaire/7291013b-81c6-41b6-9212-6c96b8b44f94",
    "subject": { "reference": "Patient/a39cafb9d1b445be95a2e2548e12a787" },
    "authored": "2022-03-19T14:54:12.194952+00:00",
    "author": { "reference": "Practitioner/fc87cbb2525f4c5eb50294f620c7a15e" },
    "item": [
        {
            "linkId": "c79da8bd-d20e-4f56-909f-f3dabae7f64f",
            "text": "This is question #1",
            "answer": [{ "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "10101-1",
                        "display": "Single select response #1"
                    } }]
        },
        {
            "linkId": "f25af10f-5d26-42a8-90a1-d86c2b363600",
            "text": "This is question #2",
            "answer": [{ "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "10102-1",
                        "display": "Multi select response #1"
                    } }, { "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "10102-2",
                        "display": "Multi select response #2"
                    } }]
        },
        {
            "linkId": "24178e3c-c67c-4524-bcb1-522aef068795",
            "text": "This is question #3",
            "answer": [{ "valueString": "This is a free text response" }]
        }
    ]
}
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
{% tab questionnaire-response-create-request curl %}
```sh
curl --request POST \
     --url https://fumage-example.canvasmedical.com/QuestionnaireResponse \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "QuestionnaireResponse",
  "questionnaire": "Questionnaire/7291013b-81c6-41b6-9212-6c96b8b44f94",
  "subject": {
    "reference": "Patient/a39cafb9d1b445be95a2e2548e12a787"
  },
  "authored": "2022-03-19T14:54:12.194952+00:00",
  "author": {
    "reference": "Practitioner/fc87cbb2525f4c5eb50294f620c7a15e"
  },
  "item": [
    {
      "linkId": "c79da8bd-d20e-4f56-909f-f3dabae7f64f",
      "text": "This is question #1",
      "answer": [
        {
          "valueCoding": {
            "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
            "code": "10101-1",
            "display": "Single select response #1"
          }
        }
      ]
    },
    {
      "linkId": "f25af10f-5d26-42a8-90a1-d86c2b363600",
      "text": "This is question #2",
      "answer": [
        {
          "valueCoding": {
            "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
            "code": "10102-1",
            "display": "Multi select response #1"
          }
        },
        {
          "valueCoding": {
            "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
            "code": "10102-2",
            "display": "Multi select response #2"
          }
        }
      ]
    },
    {
      "linkId": "24178e3c-c67c-4524-bcb1-522aef068795",
      "text": "This is question #3",
      "answer": [
        {
          "valueString": "This is a free text response"
        }
      ]
    }
  ]
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="questionnaire-response-create-response">
{% tabs questionnaire-response-create-response %}
{% tab questionnaire-response-create-response 201 %}
```json
null
```
{% endtab %}
{% tab questionnaire-response-create-response 400 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "invalid",
      "details": {
        "text": "Bad request"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div>
