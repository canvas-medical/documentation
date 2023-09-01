---
title: Questionnaire
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Questionnaire
        article: "a"
        description: >-
          A structured set of questions intended to guide the collection of answers from end-users. Questionnaires provide detailed control over order, presentation, phraseology and grouping to allow coherent, consistent data collection.
        attributes:
          - name: id
            description: >-
              The identifier of the questionnaire
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: name
            description: >-
              Name for this questionnaire (computer friendly)
            type: string
            required: true
          - name: status
            type: string
            required: true
          - name: description
            description: >-
              Natural language description of the questionnaire
            type: string
            required: true
          - name: code
            description: >-
              Concept that represents the overall questionnaire
            type: json
            required: true
            attributes:
              - name: system
                type: string
                required: true
              - name: code
                description: >-
                  The code
                type: string
                required: true
          - name: item
            type: json
            required: true
            description: >-
              Questions and sections within the Questionnaire
            attributes:
              - name: linkId
                description: >-
                  Unique id for item in questionnaire
                type: string
                required: true
              - name: code
                type: json
                required: true
                attributes:
                  - name: system
                    type: string
                    required: true
                  - name: code
                    description: >-
                      The code
                    type: string
                    required: true
              - name: text
                description: >-
                  The primary text of the item
                type: string
                required: true
              - name: type
                type: string
                required: true
              - name: repeats
                type: boolean
                required: true
                description: >-
                  Whether the item may repeat
              - name: answerOption
                description: >-
                  The answerOption of the item
                type: json
                required: true
                attributes:
                  - name: valueCoding
                    description: >-
                      The valueCoding of the answerOption
                    type: json
                    required: true
                    attributes:
                      - name: system
                        type: string
                      - name: code
                        type: string
                      - name: display
                        type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: identifier
            type: string
            description: The Canvas-issued MRN or a saved identifier from an external system
          - name: name
            type: string
            description: Part of a first or last name
          - name: status
            type: string
            description: The status of the questionnaire
          - name: code
            type: string
            description: The code of the questionnaire
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_request: questionnaire-read-request
          example_response: questionnaire-read-response
        search:
          responses: [200, 400]
          example_request: questionnaire-search-request
          example_response: questionnaire-search-response
---
<div id="example-read-request">
{% tabs questionnaire-read-request %}
{% tab questionnaire-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Questionnaire/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab questionnaire-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Questionnaire/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-read-response">
{% tabs questionnaire-read-response %}
{% tab questionnaire-read-response 200 %}
```json
{
    "resourceType": "Questionnaire",
    "id": "2e278b81-3bfe-4ffd-a0fc-27ac9c5344cc",
    "name": "Osteopenia/Osteoporosis",
    "status": "active",
    "description": "No Description Provided",
    "code": [
        {
            "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
            "code": "MEDI_"
        }
    ],
    "item": [
        {
            "linkId": "d3b1b76d-dead-4a9f-afcb-159bb0c4ce96",
            "code": [
                {
                    "system": "http://hl7.org/fhir/sid/icd-10",
                    "code": "711013002"
                }
            ],
            "text": "Type",
            "type": "choice",
            "repeats": true,
            "answerOption": [
                {
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/sid/icd-10",
                        "code": "M8580",
                        "display": "Osteopenia"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/sid/icd-10",
                        "code": "M800",
                        "display": "Osteoporosis with current pathological fractures"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/sid/icd-10",
                        "code": "M810",
                        "display": "Osteoporosis without current pathological fractures"
                    }
                }
            ]
        },
        {
            "linkId": "a76e6947-a3a8-4e09-ace2-a9b16f420df3",
            "code": [
                {
                    "system": "http://www.ama-assn.org/go/cpt",
                    "code": "1003F"
                }
            ],
            "text": "Assessment of Physical Activity",
            "type": "choice",
            "repeats": true,
            "answerOption": [
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "398636004_r001",
                        "display": "rarely / never"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "398636004_r002",
                        "display": "once a week"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "398636004_r003",
                        "display": "multiple times a week"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "398636004_r004",
                        "display": "once a month"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "398636004_r005",
                        "display": "multiple times a month"
                    }
                }
            ]
        },
        {
            "linkId": "01935995-4534-4674-853e-36078fda8992",
            "code": [
                {
                    "system": "http://www.ama-assn.org/go/cpt",
                    "code": "99213"
                }
            ],
            "text": "Assessment - Pharmacologic Therapy",
            "type": "choice",
            "repeats": true,
            "answerOption": [
                {
                    "valueCoding": {
                        "system": "http://www.ama-assn.org/go/cpt",
                        "code": "VkvX8DKgURdJbW28",
                        "display": "Calcium supplementation"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://www.ama-assn.org/go/cpt",
                        "code": "VkvX8DKgURdJbW29",
                        "display": "Vitamin D supplementation"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://www.ama-assn.org/go/cpt",
                        "code": "4005F",
                        "display": "Disease modifying medication other than vitamins/minerals"
                    }
                }
            ]
        },
        {
            "linkId": "d13c56ed-a68e-412d-8ee6-0dd26f05071b",
            "code": [
                {
                    "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                    "code": "VkvX8DKgURdJbW27"
                }
            ],
            "text": "Recommendation",
            "type": "choice",
            "repeats": true,
            "answerOption": [
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "VkvX8DKgURdJbW28",
                        "display": "Continue calcium supplementation"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "VkvX8DKgURdJbW29",
                        "display": "consider initiating Vitamin D supplementation"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "VkvX8DKgURcJbW30",
                        "display": "Continue vitamin D supplementation"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "VkvX8DKgURdJbW30",
                        "display": "Referral for densitometry placed"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "jvw9cfwwHCgrxN36",
                        "display": "Recommend Repeat DEXA in 3-5 years"
                    }
                }
            ]
        },
        {
            "linkId": "8af7ab00-ebc3-4261-b0e7-f6d95fc64a3b",
            "code": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "406216001"
                }
            ],
            "text": "Other Recommendations",
            "type": "text",
            "repeats": false,
            "answerOption": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "406216001",
                        "display": "other"
                    }
                }
            ]
        },
        {
            "linkId": "cf622d15-a047-4607-bcb5-ca715eedb8bd",
            "code": [
                {
                    "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                    "code": "311401005"
                }
            ],
            "text": "Patient Instructions",
            "type": "choice",
            "repeats": true,
            "answerOption": [
                {
                    "valueCoding": {
                        "system": "http://schemas.training.canvasmedical.com/fhir/systems/internal",
                        "code": "pt_311401005",
                        "display": "Encouraged lifestyle habits to support good bone mineral density (walk daily; do weight bearing exercises; eat a healthy, varied diet with plenty of fresh vegetables)"
                    }
                }
            ]
        }
    ]
}
```
{% endtab %}
{% tab questionnaire-read-response 404 %}
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
</div>

<div id="example-search-request">
{% tabs questionnaire-search-request %}
{% tab questionnaire-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Questionnaire??code=711013002&name=Alcohol, tobacco and other substances"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab questionnaire-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Questionnaire??code=711013002&name=Alcohol, tobacco and other substances\
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-search-response">
{% tabs questionnaire-search-response %}
{% tab questionnaire-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Questionnaire?code=711013002&name=Alcohol%2C+tobacco+and+other+substances&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Questionnaire?code=711013002&name=Alcohol%2C+tobacco+and+other+substances&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Questionnaire?code=711013002&name=Alcohol%2C+tobacco+and+other+substances&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Questionnaire",
                "id": "0dfc714f-fe85-4dbc-819a-545246c78368",
                "name": "Alcohol, tobacco and other substances",
                "status": "active",
                "description": "No Description Provided",
                "code": [
                    {
                        "system": "http://loinc.org",
                        "code": "62541-8"
                    }
                ],
                "item": [
                    {
                        "linkId": "ccc92372-b333-4692-9e32-6c1196f64632",
                        "code": [
                            {
                                "system": "http://loinc.org",
                                "code": "68518-0"
                            }
                        ],
                        "text": "Drink frequency (AUDIT-C)",
                        "type": "choice",
                        "repeats": false,
                        "answerOption": [
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA6270-8",
                                    "display": "Never"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18926-8",
                                    "display": "Monthly or less"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18927-6",
                                    "display": "2-4 times a month"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18928-4",
                                    "display": "2-3 times a week"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18929-2",
                                    "display": "4 or more times a week"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "6b558d72-b964-4b40-9216-d89084504ef6",
                        "code": [
                            {
                                "system": "http://loinc.org",
                                "code": "68519-8"
                            }
                        ],
                        "text": "Drink intensity (AUDIT-C)",
                        "type": "choice",
                        "repeats": false,
                        "answerOption": [
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA15694-5",
                                    "display": "None"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA15694-5",
                                    "display": "1 or 2"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA15695-2",
                                    "display": "3 or 4"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18930-0",
                                    "display": "5 or 6"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18931-8",
                                    "display": "7 to 9"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18932-6",
                                    "display": "10 or more"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "27c9464e-5038-4026-a3cf-0e44bdead8fd",
                        "code": [
                            {
                                "system": "http://loinc.org",
                                "code": "68520-6"
                            }
                        ],
                        "text": "Binge frequency (AUDIT-C)",
                        "type": "choice",
                        "repeats": false,
                        "answerOption": [
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA6270-8",
                                    "display": "Never"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18933-4",
                                    "display": "Less than monthly"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18876-5",
                                    "display": "Monthly"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18891-4",
                                    "display": "Weekly"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LA18934-2",
                                    "display": "Daily or almost daily"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "d4269ed2-f899-4631-86b2-571b1b1ac4af",
                        "code": [
                            {
                                "system": "http://loinc.org",
                                "code": "39240-7"
                            }
                        ],
                        "text": "Tobacco status",
                        "type": "choice",
                        "repeats": false,
                        "answerOption": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "266919005",
                                    "display": "Never smoker"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "8517006",
                                    "display": "Former smoker"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "449868002",
                                    "display": "Current everyday smoker"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "428041000124106",
                                    "display": "Current some day smoker"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "428071000124103",
                                    "display": "Current Heavy tobacco smoker"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "428061000124105",
                                    "display": "Current Light tobacco smoker"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "77176002",
                                    "display": "Smoker, current status unknown"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "266927001",
                                    "display": "Unknown if ever smoked"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "04835739-2a6d-43ae-bafa-af195906a622",
                        "code": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "711013002"
                            }
                        ],
                        "text": "Tobacco comment",
                        "type": "text",
                        "repeats": false,
                        "answerOption": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "711013002",
                                    "display": "Tobacco comment"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "840a25c9-8812-41e1-9ef5-af6ee3c8bf77",
                        "code": [
                            {
                                "system": "http://loinc.org",
                                "code": "63689-4"
                            }
                        ],
                        "text": "Other substances",
                        "type": "text",
                        "repeats": false,
                        "answerOption": [
                            {
                                "valueCoding": {
                                    "system": "http://loinc.org",
                                    "code": "LL1446-5",
                                    "display": "Other substances"
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