---
title: FHIR Practitioner 
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Practitioner
        article: "a"
        attributes:
          - name: _id
            description: >-
              The identifier of the practitioner
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: extension
            type: json
            required: true
          - name: identifier
            type: json
            required: false
          - name: active
            type: boolean
            required: false
          - name: name
            type: json
            required: true
          - name: telecom
            type: json
            required: false
          - name: gender
            description: >-
              Default: male
            type: string
            required: false
          - name: deceased
            type: boolean
            required: false
          - name: address
            type: json
            required: false
          - name: photo
            type: json
            required: false
          - name: contact
            type: json
            required: false
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: identifier
            type: string
            description: The Canvas-issued MRN or a saved identifier from an external system  
          - name: name
            type: string
            description: Part of a first or last name
          - name: family
            type: string
            description: Last name
          - name: given
            type: string
            description: First Name
          - name: birthdate
            type: date
            description: The practitioner's birthdate
          - name: gender
            type: string
          - name: nickname
            type: string
            description: Preferred or alternate name
          - name: email
            type: string
            description: Practitioner email address
          - name: phone
            type: string
            description: Practitioner phone number, expected to be 10 digits
          - name: active
            type: boolean
            description: By default, both active and inactive practitioners are returned. Use this parameter to only return active (true) or inactive (false)
        endpoints: [read, search]
        # example_payload: example-payload-code
        read:
          responses: [200, 400]
          example_request: example-read-request
          example_response: example-read-response
        search:
          responses: [200, 400]
          example_request: example-search-request
          example_response: example-search-response
  
---
<div id="example-payload-code">
{% tabs payload %}
{% tab payload json %}
```json
some data here
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-read-request">
{% tabs read-request %}
{% tab read-request curl %}
```sh
curl --request GET \
     --url https://fhir-example.canvasmedical.com/Patient/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% tab read-request python %}
```sh
import requests

url = "{{base_url}}/Practitioner/"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```
{% endtab %}
{% endtabs %}
</div>

<div id="example-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
200 {
  {
      "resourceType": "Practitioner",
      "id": "e766816672f34a5b866771c773e38f3c",
      "identifier": [
          {
              "system": "http://hl7.org/fhir/sid/us-npi",
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
  }}
```
{% endtab %}
{% tab read-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-search-request">
{% tabs search-request %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fhir-example.canvasmedical.com/Patient \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% tab search-request python %}
```sh
import requests
import json

url = "{{base_url}}/Practitioner"

payload={}
headers = {
  'Content-Type': 'application/fhir+json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```
{% endtab %}
{% endtabs %}
</div>

<div id="example-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
200 {
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
                        "system": "http://hl7.org/fhir/sid/us-npi",
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
                        "system": "http://hl7.org/fhir/sid/us-npi",
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
                        "system": "http://hl7.org/fhir/sid/us-npi",
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
                        "system": "http://hl7.org/fhir/sid/us-npi",
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
}
```
{% endtab %}
{% tab search-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

