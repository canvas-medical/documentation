---
title: Provenance
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Provenance
        article: "a"
        description: >-
         Provenance of a resource is a record that describes entities and processes involved in producing and delivering or otherwise influencing that resource. Provenance provides a critical foundation for assessing authenticity, enabling trust, and allowing reproducibility. Provenance assertions are a form of contextual metadata and can themselves become important records with their own provenance. Provenance statement indicates clinical significance in terms of confidence in authenticity, reliability, and trustworthiness, integrity, and stage in lifecycle (e.g. Document Completion - has the artifact been legally authenticated), all of which may impact security, privacy, and trust policies.
        attributes:
          - name: id
            description: >-
              The identifier of the patient
            type: string
            required: true
          - name: resourceType
            description: >-
              The type of resource
            type: string
            required: true
          - name: recorded
            description: >-
              When the activity occurred
            type: string
          - name: target
            description: >-
              The target resource that was created
            type: array
          - name: location
            description: >-
              Where the activity occurred, if relevant
            type: string
            attributes:
              - name: extension
                type: array
                attributes:
                  - name: url
                    type: string
                  - name: valueCode
                    type: string
          - name: activity
            description: >-
              The activity that occurred
            type: string
            attributes:
              - name: coding
                type: array
                attributes:
                  - name: system
                    type: string
                  - name: code
                    type: string
          - name: agent
            description: >-
              The agent that created the provenance
            type: array
            attributes:
              - name: type
                type: json
                attributes:
                  - name: coding
                    type: array
                    attributes:
                      - name: system
                        type: string
                      - name: code
                        type: string
                      - name: display
                        type: string
              - name: who
                type: string
              - name: onBehalfOf
                type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
            description: The patient associated with the provenance
          - name: target
            type: string
            description: The target resource that was created
          - name: agent
            type: string
            description: The agent that created the provenance
        endpoints: [read, search]
        read:
          responses: [200, 400]
          example_response: provenance-read-response
          example_request: provenance-read-request
        search:
          responses: [200, 400]
          example_response: provenance-search-response
          example_request: provenance-search-request
---
<div id="provenance-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fhir-example.canvasmedical.com/Provenance/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Provenance/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="provenance-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
{
    "resourceType": "Provenance",
    "id": "1df85d92-05ae-4965-bed3-9f2d6418e53b",
    "target": [
        {
            "reference": "Observation/1267a082-f12e-4c84-b715-5839e2cec392",
            "type": "Observation"
        }
    ],
    "recorded": "2022-01-10T03:46:59.312603+00:00",
    "location": {
        "extension": [
            {
                "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                "valueCode": "unsupported"
            }
        ]
    },
    "activity": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                "code": "CREATE"
            }
        ]
    },
    "agent": [
        {
            "who": {
                "display": "Not available"
            },
            "onBehalfOf": {
                "display": "Not available"
            }
        }
    ]
}
```
{% endtab %}
{% tab read-response 404 %}
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

<div id="provenance-search-request">
{% tabs search-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fhir-example.canvasmedical.com/Provenance/"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Provenance \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="provenance-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 97722,
    "link": [
        {
            "relation": "self",
            "url": "/Provenance?_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Provenance?_count=10&_offset=0"
        },
        {
            "relation": "next",
            "url": "/Provenance?_count=10&_offset=10"
        },
        {
            "relation": "last",
            "url": "/Provenance?_count=10&_offset=97720"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "e2c6ff9b-6a04-4a73-81e2-5fa4bc605a15",
                "target": [
                    {
                        "reference": "Observation/eb38c5f7-09fd-4cc1-8e7b-73b0bc87dd0b",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.036676+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "596bffc9-fda6-4503-8e08-9bdf4045a31f",
                "target": [
                    {
                        "reference": "Observation/c903ee1c-a3b1-424a-b3bc-469354316e34",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.083833+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "023ae5a7-8949-4422-a39b-8118f0d51a39",
                "target": [
                    {
                        "reference": "Observation/1cb9be26-f43b-4556-ac97-564a6b7f5654",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.291160+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "1df85d92-05ae-4965-bed3-9f2d6418e53b",
                "target": [
                    {
                        "reference": "Observation/1267a082-f12e-4c84-b715-5839e2cec392",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.312603+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "5839cf69-855d-4277-bb63-961d6c74f826",
                "target": [
                    {
                        "reference": "Observation/28349f01-9820-42a0-9b39-7730877dbc6c",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.362657+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "b503e886-6d36-41a9-a5e7-8486db304293",
                "target": [
                    {
                        "reference": "Observation/d6193b4a-11cb-4560-9dc0-3ffa1f03c94a",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.386909+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "ed2db4c0-6dde-4fb3-9934-b4a07b45338f",
                "target": [
                    {
                        "reference": "Observation/5e27a8d6-9f06-4d79-b6f5-2aaaccb4966c",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.434493+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "3a137a73-66aa-45ad-ad97-c6537c9283dc",
                "target": [
                    {
                        "reference": "Observation/87020167-7bcb-4e30-a534-ea9b1325f6f6",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.602605+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "2ad5933f-2d49-4ca7-aed0-401d73cdd269",
                "target": [
                    {
                        "reference": "Observation/53138e50-8eaf-48b5-9351-b9084a2c0bdb",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.619071+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "c5684741-5110-408b-9e7a-1d60df4f11c6",
                "target": [
                    {
                        "reference": "Observation/0a5142b7-7195-4e1c-8b36-595f4637340a",
                        "type": "Observation"
                    }
                ],
                "recorded": "2022-01-10T03:46:59.636894+00:00",
                "location": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "who": {
                            "display": "Not available"
                        },
                        "onBehalfOf": {
                            "display": "Not available"
                        }
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab search-response 400 %}
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

