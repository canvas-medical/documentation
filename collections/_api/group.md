---
title: Group
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Group
        article: "a"
        description: >-
          Represents a defined collection of entities that may be discussed or acted upon collectively but which are not expected to act collectively, and are not formally or legally recognized; i.e. a collection of entities that isn't an Organization.
        attributes:
          - name: id
            description: >-
              The identifier of the group
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: actual
            type: boolean
            required: true
          - name: type
            type: string
          - name: name
            type: string
          - name: quantity
            type: integer
          - name: member
            type: json
            attributes:
              - name: entity
                type: string
                required: true
          - name: characteristic
            type: array
            attributes:
              - name: valueCodeableConcept
                type: string
              - name: exclude
                type: boolean
              - name: code
                type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
        endpoints: [read, search, create, update]
        read:
          responses: [200, 404]
          example_request: group-read-request
          example_response: group-read-response
        search:
          responses: [200, 400]
          example_request: group-search-request
          example_response: group-search-response
        create:
          responses: [201, 400]
          example_request: group-create-request
          example_response: group-create-response
        update:
          responses: [200, 400]
          example_request: group-update-request
          example_response: group-update-response
---
<div id="group-read-request">
{% tabs group-read-request %}
{% tab group-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Group/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab group-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Group/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="group-read-response">
{% tabs group-read-response %}
{% tab group-read-response 200 %}
```json
{
    "resourceType": "Group",
    "id": "33104aa7-e3ae-4650-bdac-04bfae8365bc",
    "type": "person",
    "actual": true,
    "name": "Test Group",
    "quantity": 3,
    "member": [
        {
            "entity": {
                "reference": "Patient/cf10ff9d14d0429cb5bb7040611d1a24",
                "type": "Patient"
            }
        },
        {
            "entity": {
                "reference": "Patient/d7370b4c04f142abb594b634a8126a91",
                "type": "Patient"
            }
        },
        {
            "entity": {
                "reference": "Patient/bbfc07f009cb403882cd9d3661f1613b",
                "type": "Patient"
            }
        }
    ]
}
```
{% endtab %}
{% tab group-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Resource not found"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="group-search-request">
{% tabs group-search-request %}
{% tab group-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Group"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab group-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Group \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="group-search-response">
{% tabs group-search-response %}
{% tab group-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 6,
    "link": [
        {
            "relation": "self",
            "url": "/Group?type=person&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Group?type=person&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Group?type=person&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Group",
                "id": "33104aa7-e3ae-4650-bdac-04bfae8365bc",
                "type": "person",
                "actual": true,
                "name": "Test Group",
                "quantity": 3,
                "member": [
                    {
                        "entity": {
                            "reference": "Patient/cf10ff9d14d0429cb5bb7040611d1a24",
                            "type": "Patient"
                        }
                    },
                    {
                        "entity": {
                            "reference": "Patient/d7370b4c04f142abb594b634a8126a91",
                            "type": "Patient"
                        }
                    },
                    {
                        "entity": {
                            "reference": "Patient/bbfc07f009cb403882cd9d3661f1613b",
                            "type": "Patient"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Group",
                "id": "47ae3df8-9204-4790-a4ac-f05b14d7b56f",
                "type": "person",
                "actual": true,
                "name": "Test Group",
                "quantity": 3,
                "member": [
                    {
                        "entity": {
                            "reference": "Patient/cf10ff9d14d0429cb5bb7040611d1a24",
                            "type": "Patient"
                        }
                    },
                    {
                        "entity": {
                            "reference": "Patient/d7370b4c04f142abb594b634a8126a91",
                            "type": "Patient"
                        }
                    },
                    {
                        "entity": {
                            "reference": "Patient/bbfc07f009cb403882cd9d3661f1613b",
                            "type": "Patient"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Group",
                "id": "03811b90-5c2c-4490-9ac8-8ffd7f25fcf4",
                "type": "person",
                "actual": true,
                "name": "Gold Kidney Arizona",
                "quantity": 1,
                "member": [
                    {
                        "entity": {
                            "reference": "Patient/16a0895781ed4b15add239d4d1331524",
                            "type": "Patient"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Group",
                "id": "fb89388f-2d82-4f8f-8abb-66162cf6d504",
                "type": "person",
                "actual": true,
                "name": "Jess",
                "quantity": 1,
                "member": [
                    {
                        "entity": {
                            "reference": "Patient/9578102aa5be415dae8133de22eff713",
                            "type": "Patient"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Group",
                "id": "728b07ce-4199-46c0-8766-f5bbc1566f9b",
                "type": "person",
                "actual": true,
                "name": "Reba Test",
                "quantity": 0
            }
        },
        {
            "resource": {
                "resourceType": "Group",
                "id": "e8b1840b-b3c6-42ae-a118-c66aad5197f8",
                "type": "person",
                "actual": true,
                "name": "Kevin Carey's Favorites",
                "quantity": 5,
                "member": [
                    {
                        "entity": {
                            "reference": "Patient/a373ec4c17014d089a855dae552e7d88",
                            "type": "Patient"
                        }
                    },
                    {
                        "entity": {
                            "reference": "Patient/0c0ed63303624320be9cecd30e19897e",
                            "type": "Patient"
                        }
                    },
                    {
                        "entity": {
                            "reference": "Patient/31dfdc4e0f134ca49dfb9c4f40afe4c3",
                            "type": "Patient"
                        }
                    },
                    {
                        "entity": {
                            "reference": "Patient/4de53e023c02498294d5e0bb4890c876",
                            "type": "Patient"
                        }
                    },
                    {
                        "entity": {
                            "reference": "Patient/9076311ef40f4458af7209b9aaa4bcd3",
                            "type": "Patient"
                        }
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab group-search-response 400 %}
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

<div id="group-create-request">
{% tabs group-create-request %}
{% tab group-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Group?group_type=practitioner&group_name=A Test Group"

payload = {
  {
    "resourceType": "Group",
    "type": "practitioner",
    "name": "A Test Patient Group",
    "active": true,
    "actual": true,
    "member": [
        {
            "entity": {
                "reference": "Patient/<patient_id>",
                "type": "Patient"
            }
        }
    ]
}
}
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab group-create-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Group \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --data '
{
    "resourceType": "Group",
    "type": "practitioner",
    "name": "A Test Patient Group",
    "active": true,
    "actual": true,
    "member": [
        {
            "entity": {
                "reference": "Patient/<patient_id>",
                "type": "Patient"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="group-create-response">
{% tabs group-create-response %}
{% tab group-create-response 201 %}
```json
null
```
{% endtab %}
{% tab group-create-response 400 %}
```json
{
    "resourceType": "Group",
    "type": "practitioner",
    "name": "A Test Patient Group",
    "active": true,
    "actual": true,
    "member": [
        {
            "entity": {
                "reference": "Patient/<patient_id>",
                "type": "Patient"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="group-update-request">
{% tabs group-update-request %}
{% tab group-update-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Appointment/<id>"

payload = {
  {
    "resourceType": "Group",
    "type": "person",
    "actual": true,
    "name": "A different Patient Group",
    "member": [
        {
            "entity": {
                "reference": "Patient/<patient_id>",
                "type": "Patient"
            },
            "inactive": false
        }
    ]
}
}
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)

```
{% endtab %}
{% tab group-update-request curl %}
```sh
curl --request PUT \
     --url https://fumage-example.canvasmedical.com/Group/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Group",
    "type": "person",
    "actual": true,
    "name": "A different Patient Group",
    "member": [
        {
            "entity": {
                "reference": "Patient/<patient_id>",
                "type": "Patient"
            },
            "inactive": false
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="group-update-response">
{% tabs group-update-response %}
{% tab group-update-response 200 %}
```json
null
```
{% endtab %}
{% tab group-update-response 400 %}
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

