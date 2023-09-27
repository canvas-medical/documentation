---
title: Procedure
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Procedure
        article: "a"
        description: >-
          An action that is or was performed on or for a patient. This can be a physical intervention like an operation, or less invasive like long term services, counseling, or hypnotherapy.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-procedure.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-procedure.html)<br><br>
          See this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360055626874-Perform-Command-for-In-Office-Procedures) for information on creating procedures with the `Perform` command.
        attributes:
          - name: id
            description: The identifier of the Procedure
            type: string
          - name: status
            description: A code specifying the state of the procedure
            type: string
          - name: code
            description: Identification of the procedure
            type: json
          - name: subject
            description: Who the procedure was performed on
            type: json
          - name: performedDateTime
            description: When the procedure was performed
            type: datetime
        search_parameters:
          - name: _id
            description: The identifier of the Procedure
            type: string
          - name: patient
            description: Who the procedure was performed on
            type: string
        endpoints: [read, search]
        read:
          description: Read an Procedure resource.
          responses: [200, 401, 403, 404]
          example_request: procedure-read-request
          example_response: procedure-read-response
        search:
          description: Search for Procedure resources.
          responses: [200, 400, 401, 403]
          example_request: procedure-search-request
          example_response: procedure-search-response
---

<div id="procedure-read-request">
{%  include read-request.html resource_type="Procedure" %}
</div>

<div id="procedure-read-response">

  {% tabs procedure-read-response %}

    {% tab procedure-read-response 200 %}
```json
{
    "resourceType": "Procedure",
    "id": "2dd9a3bc-a3bb-472b-aaef-c57be394de39",
    "status": "unknown",
    "code": {
        "coding": [
            {
                "system": "http://www.ama-assn.org/go/cpt",
                "code": "23066",
                "display": "Biopsy soft tissue shoulder deep"
            }
        ]
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
        "type": "Patient"
    },
    "performedDateTime": "2023-09-20T21:18:54.263690+00:00"
}
```
    {% endtab %}

    {% tab procedure-read-response 401 %}
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

    {% tab procedure-read-response 403 %}
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

    {% tab procedure-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Procedure resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="procedure-search-request">
{% include search-request.html resource_type="Procedure" search_string="patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="procedure-search-response">

  {% tabs procedure-search-response %}

    {% tab procedure-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Procedure?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Procedure?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Procedure?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Procedure",
                "id": "2dd9a3bc-a3bb-472b-aaef-c57be394de39",
                "status": "unknown",
                "code": {
                    "coding": [
                        {
                            "system": "http://www.ama-assn.org/go/cpt",
                            "code": "23066",
                            "display": "Biopsy soft tissue shoulder deep"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
                    "type": "Patient"
                },
                "performedDateTime": "2023-09-20T21:18:54.263690+00:00"
            }
        }
    ]
}
```
    {% endtab %}

    {% tab procedure-search-response 400 %}
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

    {% tab procedure-search-response 401 %}
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

    {% tab procedure-search-response 403 %}
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
