---
title: FHIR Organization
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Organization
        article: "a"
        description: >-
         A formally or informally recognized grouping of people or organizations formed for the purpose of achieving some form of collective action. Includes companies, institutions, corporations, departments, community groups, healthcare practice groups, payer/insurer, etc.
        attributes:
          - name: id
            description: >-
              The identifier of the patient
            type: string
            required: true
          - name: resourceType
            description: >-
              The type of resource
            type: string
            required: true
          - name: identifier
            description: >-
              Identifies this organization  across multiple systems
            type: array
          - name: active
            description: >-
              Whether the organization's record is still in active use
            type: boolean
          - name: name
            description: >-
              Name used for the organization
            type: string
          - name: telecom
            description: >-
              A contact detail for the organization
            type: array
          - name: address
            description: >-
              An address for the organization
            type: array          
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: name
            type: string
            description: A name of the organization
          - name: address
            type: string
            description: An address of the organization
        endpoints: [read, search]
        read:
          responses: [200, 400]
          example_response: organization-read-response
          example_request: organization-read-request
        search:
          responses: [200, 400]
          example_response: organization-search-response
          example_request: organization-search-request
---
<div id="organization-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Organization/<id>"

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
     --url https://fumage-example.canvasmedical.com/Organization/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="organization-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
{
    "resourceType": "Organization",
    "id": "7c7761c7-2bd9-4321-abab-450b9be44941",
    "active": true,
    "name": "Alternative Service Concepts (ASC)"
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
                "text": "Unknown Organization resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="organization-search-request">
{% tabs search-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Organization?name=Austin Resolutions"

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
     --url https://fumage-example.canvasmedical.com/Organization?name=Austin Resolutions \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="organization-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Organization?name=Austin+Resolutions&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Organization?name=Austin+Resolutions&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Organization?name=Austin+Resolutions&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Organization",
                "id": "ca6b73d1-6374-45c9-9ac9-7bd4303cb9a0",
                "active": true,
                "name": "Austin Resolutions"
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

