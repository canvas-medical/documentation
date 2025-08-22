---
title: RelatedPerson
layout: api
sections:
  - type: section
    blocks:
      - type: apidoc
        name: RelatedPerson
        article: "a"
        description: >-
          Information about a person that is involved in the care for a patient, but who is not the target of healthcare, nor has a formal responsibility in the care process.<br><br>
          [https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-relatedperson.html](https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-relatedperson.html)
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the RelatedPerson.
            type: string
          - name: active
            description: Whether this related person's record is in active use.
            type: boolean
          - name: patient
            description: The patient this person is related to.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the patient in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: relationship
            description: The nature of the relationship.
            type: array[json]
            attributes:
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    enum_options: 
                      - value: <blank>
                      - value: http://terminology.hl7.org/CodeSystem/v3-RoleCode
                    type: string
                  - name: code
                    description: >-
                      The code of the relationship.<br><br>
                      Values are nominally from the [PatientRelationshipType ValueSet](https://hl7.org/fhir/R4/valueset-relatedperson-relationshiptype.html), but custom contact categories can be used as well.
                    type: string
                  - name: display
                    description: >-
                      The display name of the coding.<br><br>
                      Values are nominally from the [PatientRelationshipType ValueSet](https://hl7.org/fhir/R4/valueset-relatedperson-relationshiptype.html), but custom contact categories can be used as well.
                    type: string
          - name: name
            description: A name associated with the person.
            type: array[json]
            attributes:
              - name: text
                type: string
                description: >-
                  Text representation of the full name.<br><br>
                  If the RelatedPerson is a patient contact but not a Patient on Canvas, this attribute will be populated.<br><br> 
                  If the RelatedPerson is a Patient on Canvas, this attribute will not be populated; instead the `family`, `given`, `prefix`, and `suffix` attributes will be provided.
              - name: family
                type: string
                description: Family name (often called 'Surname').
              - name: given
                type: array[string]
                description: >-
                  Given names (not always 'first'). Includes middle names.<br><br>
                  This repeating element order: Given Names appear in the correct order for presenting the name.
              - name: prefix
                type: array[string]
                description: Parts that come before the name.
              - name: suffix
                type: array[string]
                description: Parts that come after the name.
          - name: telecom
            type: array[json]
            description: Contact details for the individual.
            attributes:
              - name: system
                type: string
                description: Supported values are **phone**, **fax**, **email**, **pager**, **url**, **sms**, and **other**.
              - name: value
                type: string
                description: Free text string of the value for this contact point.
              - name: use
                type: string
                description: Supported values are  **home**, **work**, **temp**, **old** and **mobile**.
              - name: rank
                type: integer
                description: An integer representing the preferred order of contact points per system.
          - name: address
            description: Address where the related person can be contacted or visited
            type: array[json]
            attributes:
              - name: use
                type: string
                description: Supported values are **home**, **work**, **temp** and **old**.
              - name: type
                type: string
                description: Supported values are **both**, **physical** and **postal**.
              - name: line
                type: array[string]
                description:  List of strings. The first item in the list will be address line 1 in Canvas. The rest of the items in the list will be concatenated to be address line 2.
              - name: city
                type: string
                description: String representing the city of the address.
              - name: state
                type: string
                description: 2 letter state abbreviation of the address.
              - name: postalCode
                type: string
                description: The 5 digit postal code of the address.
              - name: country
                type: string
                description: The ISO 3166 2 letter country code.
              - name: period
                type: json
                attributes:
                  - name: start
                    type: date
                    description: Starting date with inclusive boundary
                  - name: end
                    type: date
                    description: End date with inclusive boundary, if not ongoing
        search_parameters:
          - name: _id
            description: The identifier of the RelatedPerson.
            type: string
          - name: patient
            description: The patient reference associated with the RelatedPerson in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
        endpoints: [read, search]
        read:
          description: Read a RelatedPerson resource.
          responses: [200, 401, 403, 404]
          example_request: relatedperson-read-request
          example_response: relatedperson-read-response
        search:
          description: Search for RelatedPerson resources.
          responses: [200, 400, 401, 403]
          example_request: relatedperson-search-request
          example_response: relatedperson-search-response
---

<div id="relatedperson-read-request">
{% include read-request.html resource_type="RelatedPerson" %}
</div>

<div id="relatedperson-read-response">

  {% tabs relatedperson-read-response %}

    {% tab relatedperson-read-response 200 %}
```json
{
  "resourceType": "RelatedPerson",
  "id": "3fcea5ee-8961-43b4-9d47-3e8a2a625e95",
  "active": true,
  "patient": {
    "reference": "Patient/7982b53c2c35427fbb70afceb83145f8",
    "type": "Patient"
  },
  "relationship": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
          "code": "ITWINSIS",
          "display": "identical twin sister"
        }
      ]
    }
  ],
  "name": [
    {
      "family": "Solis",
      "given": [
        "Terry"
      ]
    }
  ],
  "telecom": [
    {
      "system": "phone",
      "value": "5555555555",
      "use": "home",
      "rank": 1
    },
    {
      "system": "email",
      "value": "solisterry@example.net",
      "use": "home",
      "rank": 1
    }
  ],
  "address": [
    {
      "use": "home",
      "type": "both",
      "line": [
        "498 Frank Fields Suite 770"
      ],
      "city": "Taylorbury",
      "state": "RI",
      "postalCode": "90298",
      "country": "us"
    }
  ]
}
```
    {% endtab %}

    {% tab relatedperson-read-response 401 %}
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

    {% tab relatedperson-read-response 403 %}
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

    {% tab relatedperson-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown RelatedPerson resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="relatedperson-search-request">
{% include search-request.html resource_type="RelatedPerson" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="relatedperson-search-response">

  {% tabs relatedperson-search-response %}

    {% tab relatedperson-search-response 200 %}
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 1,
  "link": [
    {
      "relation": "self",
      "url": "/RelatedPerson?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
    },
    {
      "relation": "first",
      "url": "/RelatedPerson?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
    },
    {
      "relation": "last",
      "url": "/RelatedPerson?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
    }
  ],
  "entry": [
    {
      "resource": {
        "resourceType": "RelatedPerson",
        "id": "3fcea5ee-8961-43b4-9d47-3e8a2a625e95",
        "active": true,
        "patient": {
          "reference": "Patient/7982b53c2c35427fbb70afceb83145f8",
          "type": "Patient"
        },
        "relationship": [
          {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                "code": "ITWINSIS",
                "display": "identical twin sister"
              }
            ]
          }
        ],
        "name": [
          {
            "family": "Solis",
            "given": [
              "Terry"
            ]
          }
        ],
        "telecom": [
          {
            "system": "phone",
            "value": "5555555555",
            "use": "home",
            "rank": 1
          },
          {
            "system": "email",
            "value": "solisterry@example.net",
            "use": "home",
            "rank": 1
          }
        ],
        "address": [
          {
            "use": "home",
            "type": "both",
            "line": [
              "498 Frank Fields Suite 770"
            ],
            "city": "Taylorbury",
            "state": "RI",
            "postalCode": "90298",
            "country": "us"
          }
        ]
      }
    }
  ]
}
```
    {% endtab %}

    {% tab relatedperson-search-response 400 %}
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

    {% tab relatedperson-search-response 401 %}
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

    {% tab relatedperson-search-response 403 %}
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
