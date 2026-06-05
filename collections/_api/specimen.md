---
title: Specimen
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Specimen
        article: "a"
        description: >-
          A sample to be used for analysis.<br><br>
          [https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-specimen.html](https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-specimen.html)
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: Unique Canvas identifier for this resource.
            type: string
          - name: type
            description: Kind of material that forms the specimen.
            type: json
            attributes:
              - name: text
                description: Free-text description of the specimen type (e.g. "Serum").
                type: string
          - name: subject
            description: The patient from whom the specimen was collected.
            type: json
            attributes:
              - name: reference
                type: string
                description: The patient reference in the format `Patient/<patient_id>`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. `Patient`).
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier for a specific Specimen.
          - name: patient
            type: string
            description: The patient reference associated to the Specimen using the format `Patient/<patient_id>`.
        endpoints: [read, search]
        read:
          description: Read a Specimen resource.
          responses: [200, 401, 403, 404]
          example_request: specimen-read-request
          example_response: specimen-read-response
        search:
          description: Search for Specimen resources.
          responses: [200, 400, 401, 403]
          example_request: specimen-search-request
          example_response: specimen-search-response
---

<div id="specimen-read-request">
{% include read-request.html resource_type="Specimen" %}
</div>

<div id="specimen-read-response">
  {% tabs specimen-read-response %}

    {% tab specimen-read-response 200 %}

```json
{
  "resourceType": "Specimen",
  "id": "0a5d9e1f-1c64-4d04-a2bb-2a58e34f9f6d",
  "type": {
    "text": "Serum"
  },
  "subject": {
    "reference": "Patient/1c8c6f27551d4d01aa3bf2477a4d5259",
    "type": "Patient",
  }
}
```

    {% endtab %}

    {% tab specimen-read-response 401 %}

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

    {% tab specimen-read-response 403 %}

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

    {% tab specimen-read-response 404 %}

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Specimen resource 'SPM-unknown'"
      }
    }
  ]
}
```

    {% endtab %}

  {% endtabs %}
</div>

<div id="specimen-search-request">
{% include search-request.html resource_type="Specimen" search_string="_id=0a5d9e1f-1c64-4d04-a2bb-2a58e34f9f6d&patient=Patient/1c8c6f27-55d-4d01-aa3b-f2477a4d5259" %}
</div>

<div id="specimen-search-response">
  {% tabs specimen-search-response %}

    {% tab specimen-search-response 200 %}

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 1,
  "link": [
    {
      "relation": "self",
      "url": "/Specimen?_id=0a5d9e1f-1c64-4d04-a2bb-2a58e34f9f6d&patient=Patient/1c8c6f27551d4d01aa3bf2477a4d5259&_count=10&_offset=0"
    },
    {
      "relation": "first",
      "url": "/Specimen?_id=0a5d9e1f-1c64-4d04-a2bb-2a58e34f9f6d&patient=Patient/1c8c6f27551d4d01aa3bf2477a4d5259&_count=10&_offset=0"
    },
    {
      "relation": "last",
      "url": "/Specimen?_id=0a5d9e1f-1c64-4d04-a2bb-2a58e34f9f6d&patient=Patient/1c8c6f27551d4d01aa3bf2477a4d5259&_count=10&_offset=0"
    }
  ],
  "entry": [
    {
      "resource": {
        "resourceType": "Specimen",
        "id": "0a5d9e1f-1c64-4d04-a2bb-2a58e34f9f6d",
        "type": {
          "text": "Serum"
        },
        "subject": {
          "reference": "Patient/1c8c6f27-551d4d01aa3bf2477a4d5259",
          "type": "Patient",
        }
      }
    }
  ]
}
```

    {% endtab %}

    {% tab specimen-search-response 400 %}

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

    {% tab specimen-search-response 401 %}

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

    {% tab specimen-search-response 403 %}

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
