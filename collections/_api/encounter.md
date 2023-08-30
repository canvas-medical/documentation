---
title: Encounter
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Encounter
        article: "a"
        description: >-
         An interaction between a patient and healthcare provider(s) for the purpose of providing healthcare service(s) or assessing the health status of a patient.
        attributes:
          - name: id
            description: >-
              The identifier of the encounter
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: identifier
            type: string
            description: >-
              Identifier(s) by which this encounter is known
            attributes:
             - name: id
               type: string
             - name: system
               type: string
             - name: value
               type: string
          - name: status
            type: string
            description: >-
              planned | in-progress | finished | cancelled
          - name: class
            type: json
            description: >-
              Classification of patient encounter
            attributes:
             - name: system
               type: string
             - name: code
               type: string
             - name: display
               type: string
          - name: type
            type: json
            description: >-
              Specific type of encounter
            attributes:
             - name: coding
               type: string
               attributes:
                 - name: system
                   type: string
                 - name: code
                   type: string
                 - name: display
                   type: string
          - name: subject
            type: string
            description: >-
              The patient or group present at the encounter
          - name: participant
            type: json
            description: >-
              List of participants involved in the encounter
            attributes:
              - name: type
                type: string
                attributes:
                  - name: coding
                    type: string
                    attributes:
                      - name: system
                        type: string
                      - name: code
                        type: string
                      - name: display
                        type: string
              - name: period
                type: json
                attributes:
                  - name: start
                    type: datetime
                  - name: end
                    type: datetime
              - name: individual
                type: string
          - name: appointment
            type: string
            description: >-
              The appointment that scheduled this encounter
          - name: period
            type: json
            description: >-
              The start and end time of the encounter
            attributes:
              - name: start
                type: datetime
              - name: end
                type: datetime
          - name: reasonCode
            type: string
            description: >-
              Coded reason the encounter takes place
          - name: reasonReference
            type: string
            description: >-
              Reason the encounter takes place (reference)
          - name: hospitalization
            type: json
            description: >-
              Details about the admission to a healthcare service
            attributes:
              - name: dischargeDisposition
                type: json
                attributes:
                 - name: coding
                   type: string
                   attributes:
                    - name: system
                      type: string
                    - name: code
                      type: string
                    - name: display
                      type: string
          - name: location
            type: string
            description: >-
              List of locations where the patient has been during the encounter
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: appointment
            type: string
            description: >-
              The appointment that scheduled this encounter
          - name: patient
            type: string
            description: >-
              The patient or group present at the encounter
          - name: subject
            type: string
            description: >-
              Encounter subject
          - name: date
            type: array
            description: >-
              The date the encounter was created
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_response: encounter-read-response
          example_request: encounter-read-request
        search:
          responses: [200, 400]
          example_response: encounter-search-response
          example_request: encounter-search-request
---
<div id="encounter-read-request">
{% tabs encounter-read-request %}
{% tab encounter-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Encounter/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab encounter-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Encounter/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="encounter-read-response">
{% tabs encounter-read-response %}
{% tab encounter-read-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Encounter?_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Encounter?_count=10&_offset=0"
        },
        {
            "relation": "next",
            "url": "/Encounter?_count=10&_offset=10"
        },
        {
            "relation": "last",
            "url": "/Encounter?_count=10&_offset=3090"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Encounter",
                "id": "ac4bff6e-a32d-49c4-884d-dad2ea7230b7",
                "identifier": [
                    {
                        "id": "ac4bff6e-a32d-49c4-884d-dad2ea7230b7",
                        "system": "http://canvasmedical.com",
                        "value": "ac4bff6e-a32d-49c4-884d-dad2ea7230b7"
                    }
                ],
                "status": "finished",
                "class": {
                    "system": "https://www.hl7.org/fhir/v3/ActEncounterCode/vs.html"
                },
                "type": [
                    {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "308335008",
                                "display": "Office Visit"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c645ed9c31b1430f82e5e371eb1657cb",
                    "type": "Patient"
                },
                "participant": [
                    {
                        "type": [
                            {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                                        "code": "PART",
                                        "display": "Participation"
                                    }
                                ]
                            }
                        ],
                        "period": {
                            "start": "2021-06-15T20:56:01.419149+00:00"
                        },
                        "individual": {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner",
                            "display": "Canvas Support MD"
                        }
                    }
                ],
                "period": {
                    "start": "2021-06-15T20:56:01.419149+00:00"
                },
                "reasonCode": [
                    {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "308335008",
                                "display": "Patient encounter procedure (procedure)"
                            }
                        ]
                    }
                ],
                "hospitalization": {
                    "dischargeDisposition": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/discharge-disposition",
                                "code": "oth",
                                "display": "Other"
                            }
                        ]
                    }
                },
                "location": [
                    {
                        "location": {
                            "reference": "Location/50ea08f9-f4a5-4315-90e3-10d38922daa8",
                            "type": "Location"
              }
                    }
                ]
            }
        }
    ]
}


```
{% endtab %}
{% tab encounter-read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown Encounter resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="encounter-search-request">
{% tabs encounter-search-request %}
{% tab encounter-search-request python %}
```sh
import requests

url = "https://fhir-example.canvasmedical.com/Encounter"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab encounter-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Encounter \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="encounter-search-response">
{% tabs encounter-search-response %}
{% tab encounter-search-response 200 %}
```json
{
    "resourceType": "Encounter",
    "id": "7720a218-c0bd-4cee-82a2-729bd9c101f3",
    "identifier": [
        {
            "id": "7720a218-c0bd-4cee-82a2-729bd9c101f3",
            "system": "http://canvasmedical.com",
            "value": "7720a218-c0bd-4cee-82a2-729bd9c101f3"
        }
    ],
    "status": "in-progress",
    "class": {
        "system": "https://www.hl7.org/fhir/v3/ActEncounterCode/vs.html"
    },
    "type": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "308335008",
                    "display": "Office Visit"
                }
            ]
        }
    ],
    "subject": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "participant": [
        {
            "type": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                            "code": "PART",
                            "display": "Participation"
                        }
                    ]
                }
            ],
            "period": {
                "start": "2022-04-04T05:26:34.711718+00:00"
            },
            "individual": {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                "type": "Practitioner",
                "display": "Canvas Support MD"
            }
        }
    ],
    "period": {
        "start": "2022-04-04T05:26:34.711718+00:00"
    },
    "reasonCode": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "308335008",
                    "display": "Patient encounter procedure (procedure)"
                }
            ]
        }
    ],
    "hospitalization": {
        "dischargeDisposition": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/discharge-disposition",
                    "code": "oth",
                    "display": "Other"
                }
            ]
        }
    },
    "location": [
        {
            "location": {
                "reference": "Location/50ea08f9-f4a5-4315-90e3-10d38922daa8",
                "type": "Location"
            }
        }
    ]
}
```
{% endtab %}
{% tab encounter-search-response 400 %}
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

