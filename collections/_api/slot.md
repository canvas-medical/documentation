---
title: Slot
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Slot
        article: "a"
        description: >-
          A slot of time on a schedule that may be available for booking appointments.<br><br>[http://hl7.org/fhir/R4/slot.html](http://hl7.org/fhir/R4/slot.html)
        attributes:
          - name: schedule
            type: json
            description: The [Schedule](/api/schedule) resource that this slot belongs to
          - name: status
            type: string
            description: The status of the available slot. Canvas only returns slots that are available for booking, so this field will always be returned as **free**.
          - name: start
            type: datetime
            description: Date/Time that the slot is to begin
          - name: end
            type: datetime
            description: Date/Time that the slot is to conclude
        search_parameters:
          - name: duration
            type: integer
            description: >-
              If included, the request will search for available appointment slots with the given duration value in minutes. If not provided, a duration of 20 minutes will be used.
          - name: end
            type: date
            description: >-
              If included, the request will search for available appointment slots up until this date. If not included, a week will be used as default (7 days from the start date).
          - name: schedule
            type: string
            description: The Schedule Resource that we are seeking a slot within. The [Schedule](/api/schedule) resource can be used to retrieve a list of Schedule ids.
            required: true
          - name: start
            type: date
            description: >-
              If included, the request will search for available appointment slots on or after this date. If not included, the current UTC date will be used.
        endpoints: [search]
        search:
          responses: [200, 400, 401, 403]
          example_request: slot-search-request
          example_response: slot-search-response
          description: Search for available appointment slots
---

<div id="slot-search-request">
{% include search-request.html resource_type="Slot" search_string="schedule=Location.2-Staff.3640cd20de8a470aa570a852859ac87e&start=2023-09-21&end=2023-09-23&duration=20" %}
</div>

<div id="slot-search-response">
{% tabs slot-search-response %}
{% tab slot-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 3,
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Slot",
                "schedule":
                {
                    "reference": "Schedule/Location.2-Staff.3640cd20de8a470aa570a852859ac87e",
                    "type": "Schedule"
                },
                "status": "free",
                "start": "2023-09-21T08:45:00-07:00",
                "end": "2023-09-21T09:05:00-07:00"
            }
        },
        {
            "resource":
            {
                "resourceType": "Slot",
                "schedule":
                {
                    "reference": "Schedule/Location.2-Staff.3640cd20de8a470aa570a852859ac87e",
                    "type": "Schedule"
                },
                "status": "free",
                "start": "2023-09-21T13:45:00-07:00",
                "end": "2023-09-21T14:05:00-07:00"
            }
        },
        {
            "resource":
            {
                "resourceType": "Slot",
                "schedule":
                {
                    "reference": "Schedule/Location.2-Staff.3640cd20de8a470aa570a852859ac87e",
                    "type": "Schedule"
                },
                "status": "free",
                "start": "2023-09-22T09:15:00-07:00",
                "end": "2023-09-22T09:35:00-07:00"
            }
        }
    ]
}
```
{% endtab %}
{% tab slot-search-response 400 %}
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
{% tab slot-search-response 401 %}
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
{% tab slot-search-response 403 %}
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
