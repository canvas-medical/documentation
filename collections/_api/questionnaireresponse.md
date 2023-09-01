---
title: QuestionnaireResponse
sections:
  - type: section
    blocks:
      - type: apidoc
        name: QuestionnaireResponse
        article: "a"
        description: >-
          A structured set of questions and their answers. The questions are ordered and grouped into coherent subsets, corresponding to the structure of the grouping of the questionnaire being responded to.
        attributes:
          - name: id
            description: >-
              The identifier of the questionnaire response
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: questionnaire
            type: string
            required: true
          - name: status
            type: string
            required: true
          - name: subject
            type: string
            required: true
          - name: authored
            type: string
            required: true
          - name: author
            type: string
            required: true
          - name: item
            type: string
            required: true
          - name: extension
            type: array
            required: true
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: authored
            type: string
          - name: patient
            type: string
            description: The patient that is the subject of the questionnaire response
          - name: questionnaire
            type: string
            description: The questionnaire that was used to generate the questionnaire response
        endpoints: [read, search, create]
        read:
          responses: [200, 404]
          example_request: questionnaire-response-read-request
          example_response: questionnaire-response-read-response
        search:
          responses: [200, 400]
          example_request: questionnaire-response-search-request
          example_response: questionnaire-response-search-response
        create:
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

url = "https://fhir-example.canvasmedical.com/QuestionnaireResponse"

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
     --url https://fhir-example.canvasmedical.com/QuestionnaireResponse \
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