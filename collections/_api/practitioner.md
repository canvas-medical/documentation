---
title: Practitioner
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Practitioner
        article: "a"
        description: >-
         A person who is directly or indirectly involved in the provisioning of healthcare.<br><br>[https://hl7.org/fhir/R4/practitioner.html](https://hl7.org/fhir/R4/practitioner.html)<br><br>To create a new staff member in Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360058232193-Add-a-new-staff-member).
        attributes:
          - name: id
            description: >-
              The identifier of the practitioner
            type: string
          - name: identifier
            type: array[json]
            description: An identifier for the person as this agent
          - name: name
            type: array[json]
            description: The name(s) associated with the practitioner
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: include-non-scheduleable-practitioners
            type: boolean
            description: By default, only scheduleable staff are displayed. Passing this parameter as True will return all active staff.
          - name: name
            type: string
            description: A search that may match any of the string fields in the name, including family, given, prefix, suffix, and/or text. Partial search is supported. If the practitioner you are looking for is inactive, you will still need to pass <i>include-non-scheduleable-practitioners=True</i>.
        endpoints: [read, search]
        read:
          responses: [200, 401, 403, 404]
          example_request: practitioner-read-request
          example_response: practitioner-read-response
          description: Read a Practitioner resource
        search:
          responses: [200, 400, 401, 403]
          example_request: practitioner-search-request
          example_response: practitioner-search-response
          description: Search for Practitioner resources
---

<div id="practitioner-read-request">
{% tabs practitioner-read-request %}
{% tab practitioner-read-request python %}
```python
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
{% tab practitioner-read-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/Practitioner/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="practitioner-read-response">
{% tabs practitioner-read-response %}
{% tab practitioner-read-response 200 %}
```json
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
}
```
{% endtab %}
{% tab practitioner-read-response 401 %}
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
{% tab practitioner-read-response 403 %}
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
{% tab practitioner-read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown Practitioner resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}

```
{% endtab %}
{% endtabs %}
</div>

<div id="practitioner-search-request">
{% tabs practitioner-search-request %}
{% tab practitioner-search-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Practitioner?name=Magee"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)

```
{% endtab %}
{% tab practitioner-search-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/Practitioner?name=Magee' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="practitioner-search-response">
{% tabs practitioner-search-response %}
{% tab practitioner-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Practitioner?name=Magee&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Practitioner?name=Magee&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Practitioner?name=Magee&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Practitioner",
                "id": "3640cd20de8a470aa570a852859ac87e",
                "identifier": [
                    {
                        "system": "http://hl7.org/fhir/sid/us-npi",
                        "value": "2967110133"
                    }
                ],
                "name": [
                    {
                        "use": "usual",
                        "text": "Steven Magee MD",
                        "family": "Magee",
                        "given": [
                            "Steven"
                        ]
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab practitioner-search-response 400 %}
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
{% tab practitioner-search-response 401 %}
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
{% tab practitioner-search-response 403 %}
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
