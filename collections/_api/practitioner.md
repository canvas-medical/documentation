---
title: Practitioner 
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Practitioner
        article: "a"
        attributes:
          - name: id
            description: >-
              The identifier of the practitioner
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: identifier
            type: json
            required: false
          - name: name
            type: json
            required: true
          - name: family
            type: string
            description: Last name
          - name: given
            type: string
            description: First Name
          - name: prefix
            type: string
          - name: suffix
            type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: name
            type: string
            description: Look up practitioner by name. Partial search is supported. If the practitioner you are looking for is inactive, you still need to use the include-non-scheduleable-practitioners = True
          - name: include-non-scheduleable-practitioners
            type: boolean
            description: By default we only display schedule-able staff, marking this as True will return all active staff
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_request: practitioner-read-request
          example_response: practitioner-read-response
        search:
          responses: [200, 400]
          example_request: practitioner-search-request
          example_response: practitioner-search-response
  
---

<div id="practitioner-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Practitioner/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)

```
{% endtab %}
{% tab read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Patient/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}

{% endtabs %}
</div>

<div id="practitioner-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
{
    "resourceType": "Practitioner",
    "id": "e766816672f34a5b866771c773e38f3c",
    "identifier": [
        {
            "system": "http://hl7.org/fumage/sid/us-npi",
            "value": "3554694505"
        }
    ],
    "name": [
        {
            "use": "usual",
            "text": "Youta Priti MD",
            "family": "Priti",
            "given": [
                "Youta"
            ]
        }
    ]
}
```
{% endtab %}
{% tab read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown Practitioner resource 'abc'"
            }
        }
    ]
}

```
{% endtab %}
{% endtabs %}
</div>

<div id="practitioner-search-request">
{% tabs search-request %}
{% tab search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Practitioner"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)

```
{% endtab %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Patient \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}

{% endtabs %}
</div>

<div id="practitioner-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
  {
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 4,
    "link": [
        {
            "relation": "self",
            "url": "/Practitioner?_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Practitioner?_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Practitioner?_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Practitioner",
                "id": "e766816672f34a5b866771c773e38f3c",
                "identifier": [
                    {
                        "system": "http://hl7.org/fumage/sid/us-npi",
                        "value": "3554694505"
                    }
                ],
                "name": [
                    {
                        "use": "usual",
                        "text": "Youta Priti MD",
                        "family": "Priti",
                        "given": [
                            "Youta"
                        ]
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Practitioner",
                "id": "3a182f42885645e0bc3d608e7c02aad8",
                "identifier": [
                    {
                        "system": "http://hl7.org/fumage/sid/us-npi",
                        "value": "123456789"
                    }
                ],
                "name": [
                    {
                        "use": "usual",
                        "text": "Nikhil Krishnan MD",
                        "family": "Krishnan",
                        "given": [
                            "Nikhil"
                        ]
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Practitioner",
                "id": "77bd177f81b14c9f943e1e30ed3dd989",
                "identifier": [
                    {
                        "system": "http://hl7.org/fumage/sid/us-npi",
                        "value": "123456789"
                    }
                ],
                "name": [
                    {
                        "use": "usual",
                        "text": "Breanna Heller LMFT",
                        "family": "Heller",
                        "given": [
                            "Breanna"
                        ]
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Practitioner",
                "id": "f65c2bed0d8643cc808e25d5cfcf5070",
                "identifier": [
                    {
                        "system": "http://hl7.org/fuamge/sid/us-npi",
                        "value": "1366978173"
                    }
                ],
                "name": [
                    {
                        "use": "usual",
                        "text": "Patrick van Nieuwenhuizen MD",
                        "family": "van Nieuwenhuizen",
                        "given": [
                            "Patrick"
                        ]
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab search-response 400 %}
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

