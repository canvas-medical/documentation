---
title: Questionnaire
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Questionnaire
        article: "a"
        description: >-
          A structured set of questions intended to guide the collection of answers from end-users. Questionnaires provide detailed control over order, presentation, phraseology and grouping to allow coherent, consistent data collection.<br><br>
          [https://hl7.org/fhir/R4/questionnaire.html](https://hl7.org/fhir/R4/questionnaire.html)<br><br>
          See our [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4403561447827-Creating-a-New-Questionnaire) for information about how to create and upload a questionnaire in Canvas.<br><br>
          **Understanding Canvas Questionnaires**<br><br>
          *Codings*<br><br>
          All questionnaires must have coding, and all response options within a question on a questionnaire must have codings.<br><br>
          *Question Types*<br><br>
          Canvas supports 3 different type of questions:<br><br>
          1. Multi select responses allowed questions are denoted with<br><br>
          `"type": "choice", "repeats": true`<br><br>
          2. Single select response questions are denoted with<br><br>
          `"type": "choice", "repeats": false`<br><br>
          3. Free text responses questions are denoted with<br><br>
          `"type": "text", "repeats": false`<br><br>
        attributes:
          - name: id
            description: The identifier of the Questionnaire
            type: string
          - name: name
            description: Name for this questionnaire (computer friendly)
            type: 
          - name: status
            description: The status of this questionnaire. Enables tracking the life-cycle of the content.
            type: string
          - name: description
            description: Natural language description of the questionnaire. May contain markdown syntax.
            type: string
          - name: code
            description: Concept that represents the overall questionnaire
            type: array[json]
          - name: item
            description: Questions and sections within the Questionnaire
            type: array[json]
        search_parameters:
          - name: _id
            description: The identifier of the Questionnaire
            type: string
          - name: code
            description: >-
              A code that corresponds to one of its items in the questionnaire<br><br>
              A Questionnaire search of the form `/Questionnaire?code=456789` will return Questionnaire resources uploaded to Canvas that have a question with the code **456789**. Questions can be reused in multiple questionnaires, but any given question code should only appear once within a particular questionnaire.
            type: string
          - name: name
            description: Computationally friendly name of the questionnaire
            type: string
          - name: questionnaire-code
            description: >-
              The questionnaire the answers are provided for<br><br>
              A Questionnaire search of of the form `/Questionnaire?questionnaire-code=711013002` will return Questionnaire resources uploaded to Canvas that have the code **711013002**.
            type: string
          - name: status
            description: The current status of the questionnaire
            type: string
        endpoints: [read, search]
        read:
          description: Read an Questionnaire resource.
          responses: [200, 401, 403, 404]
          example_request: questionnaire-read-request
          example_response: questionnaire-read-response
        search:
          description: Search for Questionnaire resources.
          responses: [200, 400, 401, 403]
          example_request: questionnaire-search-request
          example_response: questionnaire-search-response
---

<div id="questionnaire-read-request">
{%  include read-request.html resource_type="Questionnaire" %}
</div>

<div id="questionnaire-read-response">

  {% tabs questionnaire-read-response %}

    {% tab questionnaire-read-response 200 %}
```json
{
    "resourceType": "Questionnaire",
    "id": "47a408d7-9f1d-4cfd-97c7-aa810df9ed39",
    "name": "Exercise",
    "status": "active",
    "description": "No Description Provided",
    "code":
    [
        {
            "system": "http://snomed.info/sct",
            "code": "404684003"
        }
    ],
    "item":
    [
        {
            "linkId": "d82e29db-0cac-4b97-a5aa-9e81749686e2",
            "code":
            [
                {
                    "system": "http://snomed.info/sct",
                    "code": "228448000"
                }
            ],
            "text": "Do you exercise on a regular basis?",
            "type": "choice",
            "repeats": false,
            "answerOption":
            [
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "LA33-6",
                        "display": "Yes"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "LA32-8",
                        "display": "No"
                    }
                }
            ]
        },
        {
            "linkId": "f2419de1-a208-4a3f-9d55-ba9bd5ed4ec2",
            "code":
            [
                {
                    "system": "http://snomed.info/sct",
                    "code": "228449008"
                }
            ],
            "text": "In an average week, how many days do you exercise?",
            "type": "choice",
            "repeats": false,
            "answerOption":
            [
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "228449008-0",
                        "display": "0"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "38112003",
                        "display": "1"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "19338005",
                        "display": "2"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "79605009",
                        "display": "3"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "9362000",
                        "display": "4"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "34001005",
                        "display": "5"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "68244004",
                        "display": "6"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "65607009",
                        "display": "7"
                    }
                }
            ]
        },
        {
            "linkId": "93137723-295f-4b28-9f97-fb58825b2cda",
            "code":
            [
                {
                    "system": "http://snomed.info/sct",
                    "code": "255257008"
                }
            ],
            "text": "On the days when you exercised, for how long did you exercise?",
            "type": "choice",
            "repeats": false,
            "answerOption":
            [
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "QUES_FINACIAL_STRESS_CODE_Q3_A1",
                        "display": "10-20 min"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "QUES_FINACIAL_STRESS_CODE_Q3_A2",
                        "display": "20-40 min"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "QUES_FINACIAL_STRESS_CODE_Q3_A3",
                        "display": "40-60 min"
                    }
                },
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "QUES_FINACIAL_STRESS_CODE_Q3_A4",
                        "display": "> 1 hr"
                    }
                }
            ]
        },
        {
            "linkId": "7eb053cd-cb2d-435f-8f55-f154645b55c4",
            "code":
            [
                {
                    "system": "http://snomed.info/sct",
                    "code": "QUES_FINACIAL_STRESS_CODE_Q4"
                }
            ],
            "text": "What type of exercise do you do?",
            "type": "text",
            "repeats": false,
            "answerOption":
            [
                {
                    "valueCoding":
                    {
                        "system": "http://snomed.info/sct",
                        "code": "QUES_FINACIAL_STRESS_CODE_Q4_A1",
                        "display": "What type of exercise do you do?"
                    }
                }
            ]
        }
    ]
}
```
    {% endtab %}

    {% tab questionnaire-read-response 401 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
      "details": {
        "text": "Authentication failed"
      }
    }
  ]
}
```
    {% endtab %}

    {% tab questionnaire-read-response 403 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "forbidden",
      "details": {
        "text": "Authorization failed"
      }
    }
  ]
}
```
    {% endtab %}

    {% tab questionnaire-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Questionnaire resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="questionnaire-search-request">
{% include search-request.html resource_type="Questionnaire" search_string="name=exercise" %}
</div>

<div id="questionnaire-search-response">

  {% tabs questionnaire-search-response %}

    {% tab questionnaire-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
        {
            "relation": "self",
            "url": "/Questionnaire?name=exercise&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Questionnaire?name=exercise&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Questionnaire?name=exercise&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Questionnaire",
                "id": "47a408d7-9f1d-4cfd-97c7-aa810df9ed39",
                "name": "Exercise",
                "status": "active",
                "description": "No Description Provided",
                "code":
                [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "404684003"
                    }
                ],
                "item":
                [
                    {
                        "linkId": "d82e29db-0cac-4b97-a5aa-9e81749686e2",
                        "code":
                        [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "228448000"
                            }
                        ],
                        "text": "Do you exercise on a regular basis?",
                        "type": "choice",
                        "repeats": false,
                        "answerOption":
                        [
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "LA33-6",
                                    "display": "Yes"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "LA32-8",
                                    "display": "No"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "f2419de1-a208-4a3f-9d55-ba9bd5ed4ec2",
                        "code":
                        [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "228449008"
                            }
                        ],
                        "text": "In an average week, how many days do you exercise?",
                        "type": "choice",
                        "repeats": false,
                        "answerOption":
                        [
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "228449008-0",
                                    "display": "0"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "38112003",
                                    "display": "1"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "19338005",
                                    "display": "2"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "79605009",
                                    "display": "3"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "9362000",
                                    "display": "4"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "34001005",
                                    "display": "5"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "68244004",
                                    "display": "6"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "65607009",
                                    "display": "7"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "93137723-295f-4b28-9f97-fb58825b2cda",
                        "code":
                        [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "255257008"
                            }
                        ],
                        "text": "On the days when you exercised, for how long did you exercise?",
                        "type": "choice",
                        "repeats": false,
                        "answerOption":
                        [
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "QUES_FINACIAL_STRESS_CODE_Q3_A1",
                                    "display": "10-20 min"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "QUES_FINACIAL_STRESS_CODE_Q3_A2",
                                    "display": "20-40 min"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "QUES_FINACIAL_STRESS_CODE_Q3_A3",
                                    "display": "40-60 min"
                                }
                            },
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "QUES_FINACIAL_STRESS_CODE_Q3_A4",
                                    "display": "> 1 hr"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "7eb053cd-cb2d-435f-8f55-f154645b55c4",
                        "code":
                        [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "QUES_FINACIAL_STRESS_CODE_Q4"
                            }
                        ],
                        "text": "What type of exercise do you do?",
                        "type": "text",
                        "repeats": false,
                        "answerOption":
                        [
                            {
                                "valueCoding":
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "QUES_FINACIAL_STRESS_CODE_Q4_A1",
                                    "display": "What type of exercise do you do?"
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

    {% tab questionnaire-search-response 400 %}
```json
{
  "resourceType": "OperationOutcome",
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

    {% tab questionnaire-search-response 401 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
      "details": {
        "text": "Authentication failed"
      }
    }
  ]
}
```
    {% endtab %}

    {% tab questionnaire-search-response 403 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "forbidden",
      "details": {
        "text": "Authorization failed"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>
