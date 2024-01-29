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
        attributes:
          - name: id
            description: The identifier of the Allergen
            type: string
          - name: text
            description: Text summary of the Allergen, for human interpretation
            type: json
          - name: code
            description: Code that identifies the allergen
            type: json
        search_parameters:
          - name: _text
            description: Search on the narrative of the Allergen
            type: string
          - name: code
            description: Code that identifies the allergen
            type: string
        endpoints: [read, search]
        read:
          description: Read an Allergen resource.
          responses: [200, 401, 403, 404]
          example_request: allergen-read-request
          example_response: allergen-read-response
        search:
          description: Search for Allergen resources.
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
