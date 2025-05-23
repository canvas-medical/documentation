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
          <br><br>Organizations come from three different Canvas data types: Organizations, Vendors, and Insurers. You can manage these resources in Canvas Settings. FHIR Organizations created by Insurers in Canvas are useful in the [FHIR Coverage](/api/coverage) payor attribute.
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the Organization.
            type: string
          - name: identifier
            description: >-
               Identifies this organization across multiple systems.<br><br>
               When relevant, group NPI values, taxonomy ids, and tax ids will be found for relevant organizations.  Identifiers for vendors and transactors, such as insurance payor values, are not yet supported.
            type: array[json]
            attributes:
                - name: type
                  type: array
                  description: Description of identifier. <br><br>Currently only type will appear for Organizations with a Tax ID.
                  attributes:
                    - name: coding
                      type: array[json]
                      description:  Code defined by a terminology system.
                      attributes: 
                        - name: system
                          description: The system url of the coding.
                          enum_options: 
                            - value: http://terminology.hl7.org/CodeSystem/v2-0203
                          type: string
                        - name: code
                          description: The code of the clinical status.
                          type: string
                          enum_options: 
                            - value: TAX
                        - name: display
                          description: The display name of the coding.
                          type: string
                          enum_options: 
                            - value: Tax ID number
                - name: system
                  type: string
                  description:  The namespace for the identifier value.
                  enum_options: 
                    - value: urn:oid:2.16.840.1.113883.4.4 (for Tax ID)
                    - value: http://hl7.org/fhir/sid/us-npi (for NPI)
                - name: value
                  type: string
                  description: The value that is unique.
          - name: active
            description: Whether the organization's record is still in active use. 
            type: boolean
          - name: name
            description: Name used for the organization.
            type: string
          - name: telecom
            description: A contact detail for the organization (phone / email / fax).
            type: array[json]
            attributes:
              - name: system
                type: enum [ phone | fax | email | pager | other ]
                description: Telecommunications form for contact point - what communications system is required to make use of the contact.
              - name: value
                type: string
                description: The actual contact point details, in a form that is meaningful to the designated communication system (i.e. phone number or email address).
              - name: use
                type: enum [ work | temp | old | mobile ]
                description: Identifies the purpose for the contact point.
          - name: address
            description: An address for the organization.  This will include both physical and billing addresses, when available.
            type: array[json]
            attributes:
                - name: use
                  type: enum [ work | temp | old | billing ]
                  description: Defines the purpose of this address.
                - name: type
                  type: enum [ both | physical | postal ] 
                  description: Distinguishes between physical addresses (those you can visit) and mailing addresses (e.g. PO Boxes and care-of addresses).
                - name: line
                  type: array[string]
                  description: This component contains the house number, apartment number, street name, street direction, P.O. Box number, delivery hints, and similar address information.<br><br> The first item in the list will be address line 1 in Canvas. The rest of the items in the list will be concatenated to be address line 2.
                - name: city
                  type: string
                  description: The name of the city, town, suburb, village or other community or delivery center.
                - name: state
                  type: string
                  description: Two-letter state abbreviation of the address.
                - name: postalCode
                  type: string
                  description: The 5-digit postal code of the address.
                - name: country
                  type: string
                  description: Specifies the country in which the organization's address is located.
        search_parameters:
          - name: _id
            description: The identifier of the Organization
            type: string
          - name: address
            description: A server defined search that may match any of the string fields in the Address, including line, city, state, and/or postalCode
            type: string
          - name: name
            description: A portion of the organization's name
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
    "id": "192cf534-fc40-4c68-a233-062807338635",
    "identifier": [
        {
            "system": "http://hl7.org/fhir/sid/us-npi",
            "value": "1111111112"
        },
        {
            "system": "http://nucc.org/provider-taxonomy",
            "value": "207Q00000X"
        },
        {
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                        "code": "TAX",
                        "display": "Tax ID number"
                    }
                ]
            },
            "system": "urn:oid:2.16.840.1.113883.4.4",
            "value": "123456789"
        }
    ],
    "active": true,
    "name": "Canvas Training Organization",
    "telecom": [
        {
            "system": "fax",
            "value": "2314217892",
            "use": "work"
        },
        {
            "system": "email",
            "value": "example@example.com",
            "use": "work"
        },
        {
            "system": "phone",
            "value": "9567768088",
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
            "country": "United States"
        },
        {
            "use": "billing",
            "type": "both",
            "line": [
                "1 Billing Lane"
            ],
            "city": "NY",
            "state": "NY",
            "postalCode": "11111",
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
{% include search-request.html resource_type="Organization" search_string="name=Canvas" %}
</div>

<div id="organization-search-response">

  {% tabs organization-search-response %}

    {% tab organization-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link": [
        {
            "relation": "self",
            "url": "/Organization?name=Canvas&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Organization?name=Canvas&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Organization?name=Canvas&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Organization",
                "id": "00000000-0000-0000-0002-000000000000",
                "active": true,
                "name": "Canvas Medical",
                "telecom": [
                    {
                        "system": "phone",
                        "value": "8003701416",
                        "use": "work"
                    },
                    {
                        "system": "email",
                        "value": "example@canvasmedical.com",
                        "use": "work"
                    }
                ],
                "address": [
                    {
                        "use": "work",
                        "type": "both",
                        "line": [
                            "2037 Irving Street",
                            "Suite 228"
                        ],
                        "city": "San Francisco",
                        "state": "CA",
                        "postalCode": "94122"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Organization",
                "id": "192cf534-fc40-4c68-a233-062807338635",
                "identifier": [
                    {
                        "system": "http://hl7.org/fhir/sid/us-npi",
                        "value": "1111111112"
                    },
                    {
                        "system": "http://nucc.org/provider-taxonomy",
                        "value": "207Q00000X"
                    },
                    {
                        "type": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                    "code": "TAX",
                                    "display": "Tax ID number"
                                }
                            ]
                        },
                        "system": "urn:oid:2.16.840.1.113883.4.4",
                        "value": "123456789"
                    }
                ],
                "active": true,
                "name": "Canvas Training Organization",
                "telecom": [
                    {
                        "system": "fax",
                        "value": "2314217892",
                        "use": "work"
                    },
                    {
                        "system": "email",
                        "value": "example@example.com",
                        "use": "work"
                    },
                    {
                        "system": "phone",
                        "value": "9567768088",
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
                        "country": "United States"
                    },
                    {
                        "use": "billing",
                        "type": "both",
                        "line": [
                            "1 Billing Lane"
                        ],
                        "city": "NY",
                        "state": "NY",
                        "postalCode": "11111",
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
