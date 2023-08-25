---
title: Slot 
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Slot
        article: "a"
        description: >-
            A bookable time-slot from a specific schedule, used when creating or updating an appointment
        attributes:
          - name: _id
            description: >-
              The identifier of the slot
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: schedule
            type: string
            description: This is a FHIR Schedule reference. GET /Schedule for a list of schedule ids.
          - name: start
            type: date
            description: If provided, we will search for available appointment slots on or after this date. NOTE- If not provided, we will use the current UTC date.
          - name: duration
            type: int32
            description: If provided, we will search for available appointment slots with the given duration in minutes. NOTE- If not provided, we will search for 20 minute slots.
          - name: end
            type: date
            description: If provided, we will search for available appointment slots up until this date. NOTE- If not provided, we will show a week as default (7 days from the start date)
        search_parameters:
          - name: schedule
            type: string
            description: This is a FHIR Schedule reference. GET /Schedule for a list of schedule ids.
            required: true
          - name: start
            type: date
            description: If provided, we will search for available appointment slots on or after this date. NOTE- If not provided, we will use the current UTC date.
          - name: duration
            type: int32
            description: If provided, we will search for available appointment slots with the given duration in minutes. NOTE- If not provided, we will search for 20 minute slots.
          - name: end
            type: date
            description: If provided, we will search for available appointment slots up until this date. NOTE- If not provided, we will show a week as default (7 days from the start date)
            

        endpoints: [search]
        search:
          responses: [200, 400]
          example_request: slot-search-request
          example_response: slot-search-response
---

<div id="slot-search-request">
{% tabs search-request %}
{% tab search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Slot?schedule=Schedule%2FLocation.1-Staff.c2ff4546548e46ab8959af887b563eab&start=2022-03-10&duration=20&end=2022-03-30"

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
     --url https://fumage-example.canvasmedical.com/Slot \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="slot-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
  {
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 3,
    "entry": [
        {
                 {
            "resource": {
                "resourceType": "Slot",
                "schedule": {
                    "reference": "Schedule/Location.1-Staff.4150cd20de8a470aa570a852859ac87e",
                    "type": "Schedule"
                },
                "status": "free",
                "start": "2023-08-25T06:15:00-07:00",
                "end": "2023-08-25T06:35:00-07:00"
            }
        },
        {
            "resource": {
                "resourceType": "Slot",
                "schedule": {
                    "reference": "Schedule/Location.1-Staff.4150cd20de8a470aa570a852859ac87e",
                    "type": "Schedule"
                },
                "status": "free",
                "start": "2023-08-25T06:30:00-07:00",
                "end": "2023-08-25T06:50:00-07:00"
            }
        },
        {
            "resource": {
                "resourceType": "Slot",
                "schedule": {
                    "reference": "Schedule/Location.1-Staff.4150cd20de8a470aa570a852859ac87e",
                    "type": "Schedule"
                },
                "status": "free",
                "start": "2023-08-25T06:35:00-07:00",
                "end": "2023-08-25T06:55:00-07:00"
            }
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

