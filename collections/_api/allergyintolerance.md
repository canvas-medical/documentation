---
title: AllergyIntolerance
sections:
  - type: section
    blocks:
      - type: apidoc
        name: AllergyIntolerance
        article: "a"
        description: >-
          Get information about a particular AllergyIntolerance record
        attributes:
          - name: id
            description: >-
              The identifier of the allergyintolerance
            type: string
            required: true
          - name: patient
            description: >-
              The patient
            type: string
            required: true
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_response: allergyintolerance-read-response
          example_request: allergyintolerance-read-request
        search:
          responses: [200, 400]
          example_response: allergyintolerance-search-response
          example_request: allergyintolerance-search-request
---
<div id="allergyintolerance-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/AllergyIntolerance/<id>"

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
     --url https://fumage-example.canvasmedical.com/AllergyIntolerance/<id>\
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="allergyintolerance-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
{
    "resourceType": "AllergyIntolerance",
    "id": "5882be6e-9f7a-4fed-8d78-bf6eb00025e8",
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                "code": "active",
                "display": "Active"
            }
        ]
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                "code": "unconfirmed",
                "display": "Unconfirmed"
            }
        ]
    },
    "code": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "476",
                "display": "Penicillins"
            }
        ]
    },
    "patient": {
        "reference": "Patient/a29eaebb284143ba97c76b01fdb46964",
        "type": "Patient"
    },
    "onsetDateTime": "1950-01-01",
    "note": [
        {
            "text": "Hives"
        }
    ],
    "reaction": [
        {
            "manifestation": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                            "code": "unknown",
                            "display": "Unknown"
                        }
                    ]
                }
            ],
            "severity": "moderate"
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

<div id="allergyintolerance-search-request">
{% tabs search-request %}
{% tab search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/AllergyIntolerance?patient=Patient%2F9420c5f6c44e47ec82d7e48f78d5723a"

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
     --url https://fumage-example.canvasmedical.com/AllergyIntolerance \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="allergyintolerance-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/AllergyIntolerance?patient=Patient%2Fa29eaebb284143ba97c76b01fdb46964&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/AllergyIntolerance?patient=Patient%2Fa29eaebb284143ba97c76b01fdb46964&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/AllergyIntolerance?patient=Patient%2Fa29eaebb284143ba97c76b01fdb46964&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "AllergyIntolerance",
                "id": "5882be6e-9f7a-4fed-8d78-bf6eb00025e8",
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ]
                },
                "verificationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                            "code": "unconfirmed",
                            "display": "Unconfirmed"
                        }
                    ]
                },
                "code": {
                    "coding": [
                        {
                            "system": "http://www.fdbhealth.com/",
                            "code": "476",
                            "display": "Penicillins"
                        }
                    ]
                },
                "patient": {
                    "reference": "Patient/a29eaebb284143ba97c76b01fdb46964",
                    "type": "Patient"
                },
                "onsetDateTime": "1950-01-01",
                "note": [
                    {
                        "text": "Hives"
                    }
                ],
                "reaction": [
                    {
                        "manifestation": [
                            {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                                        "code": "unknown",
                                        "display": "Unknown"
                                    }
                                ]
                            }
                        ],
                        "severity": "moderate"
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


