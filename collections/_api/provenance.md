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
              The identifier of the provenance
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
{% tabs provenance-read-request %}
{% tab provenance-read-request python %}
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
{% tab provenance-read-request curl %}
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
{% tabs provenance-read-response %}
{% tab provenance-read-response 200 %}
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
{% tab provenance-read-response 404 %}
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
{% tabs provenance-search-request %}
{% tab provenance-search-request python %}
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
{% tab provenance-search-request curl %}
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
{% tabs provenance-search-response %}
{% tab provenance-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link": [
        {
            "relation": "self",
            "url": "/Provenance?_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Provenance?_count=10&_offset=0"
        },
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
    ]
}
```
{% endtab %}
{% tab provenance-search-response 400 %}
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

