---
title: Organization
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Organization
        article: "a"
        description: >-
          A formally or informally recognized grouping of people or organizations formed for the purpose of achieving some form of collective action. Includes companies, institutions, corporations, departments, community groups, healthcare practice groups, payer/insurer, etc.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-organization.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-organization.html)
        attributes:
          - name: id
            description: The identifier of the Organization
            type: string
          - name: identifier
            description: >-
               Identifies this organization across multiple systems.<br><br>
               When relevant, group NPI values will be found here.  Other identifiers, such as
               insurance payor values, are not yet supported.<br><br>
            type: array[json]
          - name: active
            description: Whether the organization's record is still in active use
            type: boolean
          - name: name
            description: Name used for the organization
            type: string
          - name: telecom
            description: A contact detail for the organization
            type: array[json]
          - name: address
            description: An address for the organization
            type: array[json]
        search_parameters:
          - name: _id
            description: The identifier of the Organization
            type: string
          - name: address
            description: A server defined search that may match any of the string fields in the Address, including line, city, district, state, country, postalCode, and/or text
            type: string
          - name: name
            description: A portion of the organization's name or alias
            type: string
        endpoints: [read, search]
        read:
          description: Read an Organization resource.
          responses: [200, 401, 403, 404]
          example_request: organization-read-request
          example_response: organization-read-response
        search:
          description: Search for Organization resources.
          responses: [200, 400, 401, 403]
          example_request: organization-search-request
          example_response: organization-search-response
---

<div id="organization-read-request">
{%  include read-request.html resource_type="Organization" %}
</div>

<div id="organization-read-response">

  {% tabs organization-read-response %}

    {% tab organization-read-response 200 %}
```json
{
    "resourceType": "Organization",
    "id": "bcf685dd-f71e-49da-b471-1ee322a8d9f4",
    "identifier": [
        {
            "system": "http://hl7.org.fhir/sid/us-npi",
            "value": "1144221847"
        }
    ],
    "active": true,
    "name": "Acme Labs",
    "telecom": [
        {
            "system": "fax",
            "value": "5558675310",
            "use": "work"
        },
        {
            "system": "phone",
            "value": "5558675309",
            "use": "work"
        },
        {
            "system": "email",
            "value": "hq@acme.org",
            "use": "work"
        }
    ],
    "address": [
        {
            "use": "work",
            "type": "both",
            "line": [
                "3300 Washtenaw Avenue, Suite 227"
            ],
            "city": "Amherst",
            "state": "MA",
            "postalCode": "01002",
            "country": "USA"
        }
    ]
}
```
    {% endtab %}

    {% tab organization-read-response 401 %}
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

    {% tab organization-read-response 403 %}
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

    {% tab organization-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Organization resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="organization-search-request">
{% include search-request.html resource_type="Organization" search_string="name=acme" %}
</div>

<div id="organization-search-response">

  {% tabs organization-search-response %}

    {% tab organization-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Organization?name=acme&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Organization?name=acme&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Organization?name=acme&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Organization",
                "id": "bcf685dd-f71e-49da-b471-1ee322a8d9f4",
                "identifier": [
                    {
                        "system": "http://hl7.org.fhir/sid/us-npi",
                        "value": "1144221847"
                    }
                ],
                "active": true,
                "name": "Acme Labs",
                "telecom": [
                    {
                        "system": "fax",
                        "value": "5558675310",
                        "use": "work"
                    },
                    {
                        "system": "phone",
                        "value": "5558675309",
                        "use": "work"
                    },
                    {
                        "system": "email",
                        "value": "hq@acme.org",
                        "use": "work"
                    }
                ],
                "address": [
                    {
                        "use": "work",
                        "type": "both",
                        "line": [
                            "3300 Washtenaw Avenue, Suite 227"
                        ],
                        "city": "Amherst",
                        "state": "MA",
                        "postalCode": "01002",
                        "country": "USA"
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab organization-search-response 400 %}
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

    {% tab organization-search-response 401 %}
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

    {% tab organization-search-response 403 %}
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
