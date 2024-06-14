---
title: Allergen
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Allergen
        article: "an"
        description: >-
          A substance that, upon exposure to an individual, may cause a harmful or undesirable physiological response.
          <br><br>
          Best practices is to utilize this endpoint to find codings to feed the [Allergy Intolerance Create/Update](/api/allergyintolerance/#create). These substances come directly from our integration with FDB.
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the Allergen.
            type: string
          - name: text
            description: Text summary of the Allergen, for human interpretation.
            type: json
            attributes:
              - name: status
                description: All allergens returned from this endpoint will show a status of `generated` since this resource is generated from FDB.
              - name: div
                description: Limited xhtml content that contains the human readable text of the Allergen.
          - name: code
            description: "Code that identifies the allergen <br><br> In Canvas we will return two different codings: one from FDB and one RxNorm"
            type: json
            attributes: 
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes: 
                  - name: system
                    description: >-
                      The system url of the coding.
                    enum_options: 
                      - value: http://www.nlm.nih.gov/research/umls/rxnorm
                      - value: http://snomed.info/sct
                      - value: http://www.fdbhealth.com/
                    type: string
                  - name: code
                    description: >-
                      The code of the allergen
                    type: string
                  - name: display
                    description: >-
                      The display name of the coding
                    type: string
        search_requirements_description: An Allergen Search requires either a code or _text search parameter to perform. 
        search_parameters:
          - name: _text
            description: Performs a case insensitive partial search on the narrative of the Allergen.
            type: string
          - name: code
            description: System url and code that identifies the allergen formatted like <br> `system_url|code`.
            search_options:
              - value: http://www.nlm.nih.gov/research/umls/rxnorm|code
              - value: http://snomed.info/sct|code
            type: string
        endpoints: [read, search]
        read:
          description: Read an Allergen resource.
          responses: [200, 401, 403, 404]
          example_request: allergen-read-request
          example_response: allergen-read-response
        search:
          description: Search for Allergyen resources.
          responses: [200, 400, 401, 403]
          example_request: allergen-search-request
          example_response: allergen-search-response
---

<div id="allergen-read-request">
{%  include read-request.html resource_type="Allergen" %}
</div>

<div id="allergen-read-response">

  {% tabs allergen-read-response %}

    {% tab allergen-read-response 200 %}
```json
{
    "resourceType": "Allergen",
    "id": "fdb-6-2754",
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>minocycline HCl</p><p>6979</p>\"</div>"
    },
    "code": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "6-2754",
                "display": "minocycline HCl"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "6979"
            }
        ]
    }
}
```
    {% endtab %}

    {% tab allergen-read-response 401 %}
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

    {% tab allergen-read-response 403 %}
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

    {% tab allergen-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Allergen resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="allergen-search-request">
{% include search-request.html resource_type="Allergen" search_string="code=http://www.nlm.nih.gov/research/umls/rxnorm|6979" %}
</div>

<div id="allergen-search-response">

  {% tabs allergen-search-response %}

    {% tab allergen-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Allergen?code=http%3A%2F%2Fwww.nlm.nih.gov%2Fresearch%2Fumls%2Frxnorm%7C6979&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Allergen?code=http%3A%2F%2Fwww.nlm.nih.gov%2Fresearch%2Fumls%2Frxnorm%7C6979&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Allergen?code=http%3A%2F%2Fwww.nlm.nih.gov%2Fresearch%2Fumls%2Frxnorm%7C6979&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Allergen",
                "id": "fdb-6-2754",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>minocycline HCl</p><p>6979</p>\"</div>"
                },
                "code": {
                    "coding": [
                        {
                            "system": "http://www.fdbhealth.com/",
                            "code": "6-2754",
                            "display": "minocycline HCl"
                        },
                        {
                            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                            "code": "6979"
                        }
                    ]
                }
            }
        }
    ]
}
```
    {% endtab %}

    {% tab allergen-search-response 400 %}
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

    {% tab allergen-search-response 401 %}
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

    {% tab allergen-search-response 403 %}
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
