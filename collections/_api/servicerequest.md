---
title: ServiceRequest
sections:
  - type: section
    blocks:
      - type: apidoc
        name: ServiceRequest
        article: "a"
        description: >-
          ServiceRequest description
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the ServiceRequest.
            type: string
          - name: status
            description: A code specifying the state of the ServiceRequest.
            type: string
            enum_options:
              - value: active
              - value: draft
              - value: active
              - value: on-hold
              - value: revoked
              - value: completed
              - value: entered-in-error
              - value: unknown
          - name: intent
            description: ...
          - name: category
            description: ...
          - name: code
            description: ...
          - name: subject
            description: ...
          - name: occurrencePeriod
            description: ...
          - name: authoredOn
            description: ...
          - name: requester
            description: ...
        search_parameters:
          - name: _id
            description: The identifier of the ServiceRequest.
            type: string
          - name: patient
            description: The patient reference associated to the Service Request in the format `Patient/c4ff2ee2e41b4636b7d37ac7f9297d95`.
            type: string
          - name: authored
            description: Filter by **authoredOn**. See [Date Filtering](/api/date-filtering) for more information.
            type: date
          - name: status
            description: ...
            type: string
          - name: intent
            description: ...
            type: string
          - name: category
            description: ...
            type: string
          - name: code
            description: ...
            type: string
        endpoints: [read, search]
        read:
          description: Read a ServiceRequest resource.
          responses: [200, 401, 403, 404]
          example_request: ServiceRequest-read-request
          example_response: ServiceRequest-read-response
        search:
          description: Search for ServiceRequest resources.
          responses: [200, 400, 401, 403]
          example_request: ServiceRequest-search-request
          example_response: ServiceRequest-search-response
---

<div id="ServiceRequest-read-request">
{%  include read-request.html resource_type="ServiceRequest" %}
</div>

<div id="ServiceRequest-read-response">

  {% tabs ServiceRequest-read-response %}

    {% tab ServiceRequest-read-response 200 %}
```json
{
    "resourceType": "ServiceRequest",
    "id": "a47c7b0e-bbb4-42cd-bc4a-df259d148ea1",
    "status": "active",
    "intent": "order",
    "category": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "363679005",
                    "display": "Imaging"
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "24627-2",
                "display": "CT Chest"
            }
        ]
    },
    "subject": {
        "reference": "Patient/c4ff2ee2e41b4636b7d37ac7f9297d95",
        "type": "Patient"
    },
    "occurrencePeriod": {
        "start": "2025-10-01T09:00:00+00:00",
        "end": "2025-10-01T09:30:00+00:00"
    },
    "authoredOn": "2025-09-30T19:12:25.073749+00:00",
    "requester": {
        "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
        "type": "Practitioner"
    }
}
```
    {% endtab %}

    {% tab ServiceRequest-read-response 401 %}
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

    {% tab ServiceRequest-read-response 403 %}
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

    {% tab ServiceRequest-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown ServiceRequest resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="ServiceRequest-search-request">
{% include search-request.html resource_type="ServiceRequest" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="ServiceRequest-search-response">

  {% tabs ServiceRequest-search-response %}

    {% tab ServiceRequest-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/ServiceRequest?_count=10&_offset=0"
        },

            "relation": "first",
            "url": "/ServiceRequest?_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/ServiceRequest?_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "ServiceRequest",
                "id": "a47c7b0e-bbb4-42cd-bc4a-df259d148ea1",
                "status": "active",
                "intent": "order",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "363679005",
                                "display": "Imaging"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "24627-2",
                            "display": "CT Chest"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/c4ff2ee2e41b4636b7d37ac7f9297d95",
                    "type": "Patient"
                },
                "occurrencePeriod": {
                    "start": "2025-10-01T09:00:00+00:00",
                    "end": "2025-10-01T09:30:00+00:00"
                },
                "authoredOn": "2025-09-30T19:12:25.073749+00:00",
                "requester": {
                    "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
                    "type": "Practitioner"
                }
            }
        }
    ]
}
```
    {% endtab %}

    {% tab ServiceRequest-search-response 400 %}
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

    {% tab ServiceRequest-search-response 401 %}
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

    {% tab ServiceRequest-search-response 403 %}
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