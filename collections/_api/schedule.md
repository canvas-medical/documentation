---
title: Schedule
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Schedule
        article: "a"
        description: >-
          A container for slots of time that may be available for booking appointments<br><br>
          [http://hl7.org/fhir/R4/schedule.html](http://hl7.org/fhir/R4/schedule.html)<br><br>
          Staff availability is denoted separately at each practice location associated with the organization record. The schedule **id** obtained from a Schedule search is used to search for bookable time slots for appointments.
        attributes:
          - name: id
            description: >-
              The identifier of the schedule
            type: string
          - name: text
            type: json
            description: Descriptive and status information about the schedule
          - name: actor
            type: array[json]
            description: >-
              Resource(s) (practitioner or location) that availability information is being provided for
          - name: comment
            type: string
            description: >-
              Comments on availability
        endpoints: [search]
        search:
          responses: [200, 400, 401, 403]
          example_request: schedule-search-request
          example_response: schedule-search-response
          description: Returns a list of location/practitioner combinations that is necessary for identifying open slots when booking appointments. This endpoint does not include any parameters.
---

<div id="schedule-search-request">
{% include search-request-no-parameters.html resource_type="Schedule" %}
</div>

<div id="schedule-search-response">
{% tabs schedule-search-response %}
{% tab schedule-search-response 200 %}
```json
  {
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 8,
    "entry": [
        {
            "resource": {
                "resourceType": "Schedule",
                "id": "Location.1-Staff.e766816672f34a5b866771c773e38f3c",
                "text": {
                    "status": "generated",
                    "div": "<div>Schedule for Youta Priti MD at California</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/e766816672f34a5b866771c773e38f3c",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Schedule for Youta Priti MD at California"
            }
        },
        {
            "resource": {
                "resourceType": "Schedule",
                "id": "Location.1-Staff.77bd177f81b14c9f943e1e30ed3dd989",
                "text": {
                    "status": "generated",
                    "div": "<div>Schedule for Breanna Heller LMFT at California</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/77bd177f81b14c9f943e1e30ed3dd989",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Schedule for Breanna Heller LMFT at California"
            }
        },
        {
            "resource": {
                "resourceType": "Schedule",
                "id": "Location.1-Staff.f65c2bed0d8643cc808e25d5cfcf5070",
                "text": {
                    "status": "generated",
                    "div": "<div>Schedule for Patrick van Nieuwenhuizen MD at California</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/f65c2bed0d8643cc808e25d5cfcf5070",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Schedule for Patrick van Nieuwenhuizen MD at California"
            }
        },
        {
            "resource": {
                "resourceType": "Schedule",
                "id": "Location.2-Staff.e766816672f34a5b866771c773e38f3c",
                "text": {
                    "status": "generated",
                    "div": "<div>Schedule for Youta Priti MD at Tennessee</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/e766816672f34a5b866771c773e38f3c",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Schedule for Youta Priti MD at Tennessee"
            }
        },
        {
            "resource": {
                "resourceType": "Schedule",
                "id": "Location.2-Staff.3a182f42885645e0bc3d608e7c02aad8",
                "text": {
                    "status": "generated",
                    "div": "<div>Schedule for Nikhil Krishnan MD at Tennessee</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/3a182f42885645e0bc3d608e7c02aad8",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Schedule for Nikhil Krishnan MD at Tennessee"
            }
        },
        {
            "resource": {
                "resourceType": "Schedule",
                "id": "Location.2-Staff.77bd177f81b14c9f943e1e30ed3dd989",
                "text": {
                    "status": "generated",
                    "div": "<div>Schedule for Breanna Heller LMFT at Tennessee</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/77bd177f81b14c9f943e1e30ed3dd989",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Schedule for Breanna Heller LMFT at Tennessee"
            }
        },
        {
            "resource": {
                "resourceType": "Schedule",
                "id": "Location.2-Staff.f65c2bed0d8643cc808e25d5cfcf5070",
                "text": {
                    "status": "generated",
                    "div": "<div>Schedule for Patrick van Nieuwenhuizen MD at Tennessee</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/f65c2bed0d8643cc808e25d5cfcf5070",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Schedule for Patrick van Nieuwenhuizen MD at Tennessee"
            }
        }
    ]
}
```
{% endtab %}
{% tab schedule-search-response 400 %}
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
{% tab schedule-search-response 401 %}
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
{% tab schedule-search-response 403 %}
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
