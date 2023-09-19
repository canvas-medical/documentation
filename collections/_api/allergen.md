---
title: Allergen
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Allergen
        article: "an"
        description: >-
          Get information about a particular Allergen record
        attributes:
          - name: id
            description: >-
              The identifier of the Allergen
            type: string
            required: true
          - name: resourceType
            description: >-
              The type of resource
            type: string
            required: true
          - name: code
            description: >-
              Code that identifies the allergen
            type: json
        search_parameters:
          - name: code
            type: string
            description: Code that identifies the allergen
          - name: _text
            type: string
            description: Search on the narrative of the Allergen
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_response: allergen-read-response
          example_request: allergen-read-request
        search:
          responses: [200, 400]
          example_response: allergen-search-response
          example_request: allergen-search-request
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
{% tab allergen-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Allergen resource 'a04b44ec-c7df-4808-9043-e9c4b1d352a9'"
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
            "url": "/Allergen?code=http://www.nlm.nih.gov/research/umls/rxnorm|6979&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Allergen?code=http://www.nlm.nih.gov/research/umls/rxnorm|6979&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Allergen?code=http://www.nlm.nih.gov/research/umls/rxnorm|6979&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                {
                    "resourceType": "Allergen",
                    "id": "fdb-6-2754",
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
        }
    ]
}
```
{% endtab %}
{% tab allergen-search-response 400 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
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
{% endtabs %}
</div>
