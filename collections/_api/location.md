---
title: Location
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Location
        article: "a"
        description: >-
          Details and position information for a physical place where services are provided and resources and participants may be stored, found, contained, or accommodated.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-location.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-location.html)<br><br>
          The FHIR Location resource corresponds to Canvas Practice Location.
        attributes:
          - name: id
            description: The identifier of the AllergyIntolerance
            type: string
          - name: status
            description: The status property covers the general availability of the resource, not the current value which may be covered by the operationStatus, or by a schedule/slots if they are configured for the location
            type: string
          - name: name
            description: Name of the location as used by humans
            type: string
          - name: alias
            description: A list of alternate names that the location is known as, or was known as, in the past
            type: array[string]
          - name: description
            description: Additional details about the location that could be displayed as further information to identify the location beyond its name
            type: string
        endpoints: [read, search]
        read:
          description: Read a Location resource.
          responses: [200, 401, 403, 404]
          example_request: location-read-request
          example_response: location-read-response
        search:
          description: Search for Location resources.
          responses: [200, 400, 401, 403]
          example_request: location-search-request
          example_response: location-search-response
---

<div id="location-read-request">
{%  include read-request.html resource_type="Location" %}
</div>

<div id="location-read-response">

  {% tabs location-read-response %}

    {% tab location-read-response 200 %}
```json
{
    "resourceType": "Location",
    "id": "a04b44ec-c7df-4808-9043-e9c4b1d352a9",
    "status": "active",
    "name": "Canvas Medical",
    "alias":
    [
        "Canvas Medical HQ"
    ],
    "description": "Canvas Medical, San Francisco, CA"
}
```
    {% endtab %}

    {% tab location-read-response 401 %}
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

    {% tab location-read-response 403 %}
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

    {% tab location-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Location resource 'a04b44ec-c7df-4808-9043-e9c4b1d352a9'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="location-search-request">
{% include search-request-no-parameters.html resource_type="Location" %}
</div>

<div id="location-search-response">

  {% tabs location-search-response %}

    {% tab location-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
        {
            "relation": "self",
            "url": "/Location?_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Location?_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Location?_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Location",
                "id": "a04b44ec-c7df-4808-9043-e9c4b1d352a9",
                "status": "active",
                "name": "Canvas Medical",
                "alias":
                [
                    "Canvas Medical HQ"
                ],
                "description": "Canvas Medical, San Francisco, CA"
            }
        }
    ]
}
```
    {% endtab %}

    {% tab location-search-response 400 %}
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

    {% tab location-search-response 401 %}
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

    {% tab location-search-response 403 %}
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
