---
title: Provenance
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Provenance
        article: "a"
        description: >-
          Provenance of a resource is a record that describes entities and processes involved in producing and delivering or otherwise influencing that resource. Provenance provides a critical foundation for assessing authenticity, enabling trust, and allowing reproducibility. Provenance assertions are a form of contextual metadata and can themselves become important records with their own provenance. Provenance statement indicates clinical significance in terms of confidence in authenticity, reliability, and trustworthiness, integrity, and stage in lifecycle (e.g. Document Completion - has the artifact been legally authenticated), all of which may impact security, privacy, and trust policies.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-provenance.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-provenance.html)
        attributes:
          - name: id
            description: The identifier of the Provenance
            type: string
          - name: target
            description: Target Reference(s)
            type: array[json]
          - name: recorded
            description: When the activity was recorded / updated
            type: datetime
          - name: activity
            description: Activity that occurred
            type: json
          - name: agent
            description: Actor involved
            type: array[json]
        search_parameters:
          - name: _id
            description: The identifier of the Provenance
            type: string
          - name: agent
            description: Who participated
            type: string
          - name: patient
            description: Where the activity involved patient data
            type: string
          - name: target
            description: Target Reference(s)
            type: string
        endpoints: [read, search]
        read:
          description: Read a Provenance resource.
          responses: [200, 401, 403, 404]
          example_request: provenance-read-request
          example_response: provenance-read-response
        search:
          description: Search for Provenance resources.
          responses: [200, 400, 401, 403]
          example_request: provenance-search-request
          example_response: provenance-search-response
---

<div id="provenance-read-request">
{%  include read-request.html resource_type="Provenance" %}
</div>

<div id="provenance-read-response">

  {% tabs provenance-read-response %}

    {% tab provenance-read-response 200 %}
```json
{
    "resourceType": "Provenance",
    "id": "db1631ed-bcd3-4e43-84a1-7e507e8aa44c",
    "target": [
        {
            "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
            "type": "Patient"
        }
    ],
    "recorded": "2023-09-18T14:42:14.981528+00:00",
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
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type",
                        "code": "composer",
                        "display": "Composer"
                    }
                ]
            },
            "who": {
                "reference": "Organization/00000000-0000-0000-0002-000000000000",
                "type": "Organization",
                "display": "Canvas Medical"
            },
            "onBehalfOf": {
                "reference": "Organization/00000000-0000-0000-0002-000000000000",
                "type": "Organization"
            }
        }
    ]
}
```
    {% endtab %}

    {% tab provenance-read-response 401 %}
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

    {% tab provenance-read-response 403 %}
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

    {% tab provenance-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Provenance resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="provenance-search-request">
{% include search-request.html resource_type="Provenance" search_string="target=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="provenance-search-response">

  {% tabs provenance-search-response %}

    {% tab provenance-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Provenance?target=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Provenance?target=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Provenance?target=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "db1631ed-bcd3-4e43-84a1-7e507e8aa44c",
                "target": [
                    {
                        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
                        "type": "Patient"
                    }
                ],
                "recorded": "2023-09-18T14:42:14.981528+00:00",
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
                        "type": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type",
                                    "code": "composer",
                                    "display": "Composer"
                                }
                            ]
                        },
                        "who": {
                            "reference": "Organization/00000000-0000-0000-0002-000000000000",
                            "type": "Organization",
                            "display": "Canvas Medical"
                        },
                        "onBehalfOf": {
                            "reference": "Organization/00000000-0000-0000-0002-000000000000",
                            "type": "Organization"
                        }
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab provenance-search-response 400 %}
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

    {% tab provenance-search-response 401 %}
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

    {% tab provenance-search-response 403 %}
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
