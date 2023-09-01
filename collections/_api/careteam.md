---
title: CareTeam
sections:
  - type: section
    blocks:
      - type: apidoc
        name: CareTeam
        article: "a"
        description: >-
         The Care Team includes all the people and organizations who plan to participate in the coordination and delivery of care for a patient.
        attributes:
          - name: id
            description: >-
              The identifier of the care team
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: status
            type: string
          - name: name
            type: string
          - name: subject
            type: string
          - name: participant
            type: array
            attributes:
              - name: role
                type: array
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
              - name: member
                type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
          - name: practitioner
            type: string
          - name: status
            type: string
        endpoints: [read, search, update]
        read:
          responses: [200, 404]
          example_request: care-team-read-request
          example_response: care-team-read-response
        search:
          responses: [200, 400]
          example_request: care-team-search-request
          example_response: care-team-search-response
        update:
          responses: [200, 400]
          example_request: care-team-update-request
          example_response: care-team-update-response
---
<div id="care-team-read-request">
{% tabs care-team-read-request %}
{% tab care-team-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/CareTeam/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% tab care-team-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/CareTeam/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% endtabs %}
</div>

<div id="care-team-read-response">
{% tabs care-team-read-response %}
{% tab care-team-read-response 200 %}
```json
{
    "resourceType": "CareTeam",
    "id": "8ab7cc3c86f54723ba267baf1f906ec7",
    "status": "active",
    "name": "Care Team for Testing, Regression",
    "subject": {
        "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
        "type": "Patient",
        "display": "Testing, Regression"
    },
    "participant": [
        {
            "role": [
                {
                    "coding": [
                        {
                            "system": "INTERNAL",
                            "code": "123",
                            "display": "BFF"
                        }
                    ]
                }
            ],
            "member": {
                "reference": "Practitioner/0f0d694324914fb2ad5a1c03428a43ec",
                "type": "Practitioner",
                "display": "Cecilia Orta DO"
            }
        }
    ]
}
```
{% endtab %}
{% tab care-team-read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown CareTeam resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="care-team-search-request">
{% tabs care-team-search-request %}
{% tab care-team-search-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/CareTeam?patient=Patient%<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% tab care-team-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/CareTeam?patient=Patient%<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% endtabs %}
</div>

<div id="care-team-search-response">
{% tabs care-team-search-response %}
{% tab care-team-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/CareTeam?id=8ab7cc3c86f54723ba267baf1f906ec7&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/CareTeam?id=8ab7cc3c86f54723ba267baf1f906ec7&_count=10&_offset=0"
        },
        {
            "relation": "next",
            "url": "/CareTeam?id=8ab7cc3c86f54723ba267baf1f906ec7&_count=10&_offset=10"
        },
        {
            "relation": "last",
            "url": "/CareTeam?id=8ab7cc3c86f54723ba267baf1f906ec7&_count=10&_offset=1210"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "CareTeam",
                "id": "8ab7cc3c86f54723ba267baf1f906ec7",
                "status": "active",
                "name": "Care Team for Testing, Regression",
                "subject": {
                    "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
                    "type": "Patient",
                    "display": "Testing, Regression"
                },
                "participant": [
                    {
                        "role": [
                            {
                                "coding": [
                                    {
                                        "system": "INTERNAL",
                                        "code": "123",
                                        "display": "BFF"
                                    }
                                ]
                            }
                        ],
                        "member": {
                            "reference": "Practitioner/0f0d694324914fb2ad5a1c03428a43ec",
                            "type": "Practitioner",
                            "display": "Cecilia Orta DO"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "CareTeam",
                "id": "999f6fd203d24e26ba95b77ffa7827b6",
                "status": "active",
                "name": "Care Team for Koepp, Sandrine E. (Montana)",
                "subject": {
                    "reference": "Patient/999f6fd203d24e26ba95b77ffa7827b6",
                    "type": "Patient",
                    "display": "Koepp, Sandrine E. (Montana)"
                },
                "participant": [
                    {
                        "role": [
                            {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "17561000",
                                        "display": "Cardiologist"
                                    }
                                ]
                            }
                        ],
                        "member": {
                            "reference": "Practitioner/c2ff4546548e46ab8959af887b563eab",
                            "type": "Practitioner",
                            "display": "Saharsh Patel"
                        }
                    },
                    {
                        "role": [
                            {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "453231000124104",
                                        "display": "Primary care provider"
                                    }
                                ]
                            }
                        ],
                        "member": {
                            "reference": "Practitioner/fc87cbb2525f4c5eb50294f620c7a15e",
                            "type": "Practitioner",
                            "display": "Michael Zimmerman DO"
                        }
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab care-team-search-response 400 %}
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


<div id="care-team-update-request">
{% tabs care-team-update-request %}
{% tab care-team-update-request curl %}
```sh
curl --request PUT \
     --url https://fhir-example.canvasmedical.com/CareTeam/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "CareTeam",
  "participant": [
    {
      "role": [
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "17561000",
              "display": "Cardiologist"
            }
          ]
        }
      ],
      "member": {
        "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e"
      }
    },
    {
      "role": [
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "453231000124104",
              "display": "Primary care provider"
            }
          ]
        }
      ],
      "member": {
        "reference": "Practitioner/2a6cfdb145c8469b9d935fe91f6b0172"
      }
    }
  ],
  "subject": {
    "reference": "Patient/3e72c07b5aac4dc5929948f82c9afdfd"
  }
}
'
```
{% endtab %}
{% tab care-team-update-request python %}
```sh
import requests

url = "https://fhir-example.canvasmedical.com/CareTeam/<id>"

payload = {
    "resourceType": "CareTeam",
    "participant": [
        {
            "role": [{ "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "17561000",
                            "display": "Cardiologist"
                        }
                    ] }],
            "member": { "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e" }
        },
        {
            "role": [{ "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "453231000124104",
                            "display": "Primary care provider"
                        }
                    ] }],
            "member": { "reference": "Practitioner/2a6cfdb145c8469b9d935fe91f6b0172" }
        }
    ],
    "subject": { "reference": "Patient/3e72c07b5aac4dc5929948f82c9afdfd" }
}
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
{% endtabs %}
</div>

<div id="care-team-update-response">
{% tabs care-team-update-response %}
{% tab care-team-update-response 200 %}
```json
null
```
{% endtab %}
{% tab care-team-update-response 400 %}
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

