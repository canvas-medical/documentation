---
title: Goal
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Goal
        article: "a"
        description: >-
         Describes the intended objective(s) for a patient, group or organization care, for example, weight loss, restoring an activity of daily living, obtaining herd immunity via immunization, meeting a process improvement objective, etc.
        attributes:
          - name: id
            description: >-
              The identifier of the goal
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: lifecycleStatus
            type: string
            required: true
          - name: achievementStatus
            type: json
            attributes:
              - name: coding
                type: array
                attributes:
                  - name: system
                    type: string
                    required: true
                  - name: code
                    type: string
                    required: true
                  - name: display
                    type: string
                    required: true
          - name: priority
            type: json
            attributes:
              - name: coding
                type: array
                attributes:
                  - name: system
                    type: string
                    required: true
                  - name: code
                    type: string
                    required: true
                  - name: display
                    type: string
                    required: true
          - name: description
            type: json
            attributes:
              - name: text
                type: string
                required: true
          - name: subject
            type: string
          - name: statusDate
            type: date
          - name: target
            type: string
          - name: expressedBy
            type: string
          - name: note
            type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_request: goal-read-request
          example_response: goal-read-response
        search:
          responses: [200, 400]
          example_request: goal-search-request
          example_response: goal-search-response
---

<div id="goal-read-request">
{% tabs goal-read-request %}
{% tab goal-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Goal/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab goal-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Goal/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="goal-read-response">
{% tabs goal-read-response %}
{% tab goal-read-response 200 %}
```json
{
    "resourceType": "Goal",
    "id": "d942b2b6-5c87-4f95-b7d6-51e2355aabf5",
    "lifecycleStatus": "completed",
    "priority": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/goal-priority",
                "code": "medium-priority",
                "display": "Medium Priority"
            }
        ]
    },
    "description": {
        "text": "Eat one veggie a day"
    },
    "subject": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "startDate": "2022-12-06",
    "expressedBy": {
        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
        "type": "Practitioner"
    },
    "note": [
        {
            "id": "fe2365c7-1a87-43c3-8846-fc26349a8797",
            "authorReference": {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                "type": "Practitioner"
            },
            "time": "2022-12-06T17:21:25.172196+00:00",
            "text": "Not going well only eat skittles"
        }
    ]
}
```
{% endtab %}
{% tab goal-read-response 404 %}
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

<div id="goal-search-request">
{% tabs goal-search-request %}
{% tab goal-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Goal"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab goal-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Goal \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="goal-search-response">
{% tabs goal-search-response %}
{% tab goal-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link": [
        {
            "relation": "self",
            "url": "/Goal?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Goal?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Goal?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Goal",
                "id": "d942b2b6-5c87-4f95-b7d6-51e2355aabf5",
                "lifecycleStatus": "completed",
                "priority": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/goal-priority",
                            "code": "medium-priority",
                            "display": "Medium Priority"
                        }
                    ]
                },
                "description": {
                    "text": "Eat one veggie a day"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "startDate": "2022-12-06",
                "expressedBy": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                },
                "note": [
                    {
                        "id": "fe2365c7-1a87-43c3-8846-fc26349a8797",
                        "authorReference": {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner"
                        },
                        "time": "2022-12-06T17:21:25.172196+00:00",
                        "text": "Not going well only eat skittles"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Goal",
                "id": "730e38b4-afaf-476c-914c-5eb0b2de405d",
                "lifecycleStatus": "active",
                "description": {
                    "text": "Walk 3 steps each day"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "startDate": "2023-03-03",
                "expressedBy": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        }
    ]
}
```
{% endtab %}
{% tab goal-search-response 400 %}
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

