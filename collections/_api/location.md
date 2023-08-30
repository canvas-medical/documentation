---
title: Location
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Location
        article: "a"
        description: >-
          Get information about a location (via Canvas's practice location)
        attributes:
          - name: id
            description: >-
              The identifier of the patient
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: status
            type: string
          - name: name
            type: string
            description: >-
              The full name of the location
          - name: alias
            type: string
            description: >-
              The short name of the location
          - name: description
            type: string
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_response: location-read-response
          example_request: location-read-request
        search:
          responses: [200, 400]
          example_response: location-search-response
          example_request: location-search-request

---
<div id="location-read-request">
{% tabs location-read-request %}
{% tab location-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Location/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab location-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Location/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="location-read-response">
{% tabs location-read-response %}
{% tab location-read-response 200 %}
```json
{
    "resourceType": "Location",
    "id": "50ea08f9-f4a5-4315-90e3-10d38922daa8",
    "status": "active",
    "name": "Canvas Training Clinic",
    "alias": [
        "Canvas ABC Location"
    ],
    "description": "Canvas Training Organization: Canvas Training Clinic"
}
```
{% endtab %}
{% tab location-read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown Location resource 'abc'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="location-search-request">
{% tabs location-search-request %}
{% tab location-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/LocationSearch"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab location-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Patient \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="location-search-response">
{% tabs location-search-response %}
{% tab location-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 3,
    "link": [
        {
            "relation": "self",
            "url": "/Location?_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Location?_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Location?_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Location",
                "id": "50ea08f9-f4a5-4315-90e3-10d38922daa8",
                "status": "active",
                "name": "Canvas Training Clinic",
                "alias": [
                    "Canvas ABC Location"
                ],
                "description": "Canvas Training Organization: Canvas Training Clinic"
            }
        },
        {
            "resource": {
                "resourceType": "Location",
                "id": "b3476a18-3f63-422d-87e7-b3dc0cd55060",
                "status": "active",
                "name": "Training - Florida full",
                "alias": [
                    "Training - Florida short"
                ],
                "description": "Canvas Training Organization: Training - Florida full"
            }
        },
        {
            "resource": {
                "resourceType": "Location",
                "id": "3c01c6ea-b7dc-4109-9d1c-1cf4ba7c211e",
                "status": "inactive",
                "name": "Canvas Los Angeles Office",
                "alias": [
                    "LA Office"
                ],
                "description": "Canvas Training Organization: Canvas Los Angeles Office"
            }
        }
    ]
}
```
{% endtab %}
{% tab location-search-response 400 %}
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


