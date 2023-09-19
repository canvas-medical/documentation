---
title: Group
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Group
        article: "a"
        description: >-
          Represents a defined collection of entities that may be discussed or acted upon collectively but which are not expected to act collectively, and are not formally or legally recognized; i.e. a collection of entities that isn't an Organization.<br><br>
          https://hl7.org/fhir/R4/group.html
        attributes:
          - name: id
            description: The identifier of the Group
            type: string
          - name: type
            description: Identifies the broad classification of the kind of resources the group includes
            type: string
          - name: actual
            description: If true, indicates that the resource refers to a specific group of real individuals. If false, the group defines a set of intended individuals
            type: boolean
          - name: name
            description: Label for Group
            type: string
          - name: quantity
            description: Number of members
            type: integer
          - name: characteristic
            description: Identifies traits whose presence or absence is shared by members of the group
            type: array[json]
          - name: member
            description: Who or what is in group
            type: array[json]
        search_parameters:
          - name: _id
            description: The identifier of the Group
            type: string
          - name: type
            description: The type of resources the group contains
            type: string
        endpoints: [create, read, update, search]
        create:
          description: Create a Group resource.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: group-create-request
          example_response: group-create-response
        read:
          description: Read a Group resource.
          responses: [200, 401, 403, 404]
          example_request: group-read-request
          example_response: group-read-response
        update:
          description: Update a Group resource.
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: group-update-request
          example_response: group-update-response
        search:
          description: Search for Group resources.
          responses: [200, 400, 401, 403]
          example_request: group-search-request
          example_response: group-search-response
---

<div id="group-create-request">

  {% tabs group-create-request %}

    {% tab group-create-request curl %}
```shell
curl --request POST \
     --url https://fumage-example.canvasmedical.com/Group \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Group",
    "type": "person",
    "actual": true,
    "name": "A Test Team",
    "characteristic":
    [
        {
            "exclude": false,
            "code":
            {
                "text": "responsibility"
            },
            "valueCodeableConcept":
            {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            }
        }
    ],
    "member":
    [
        {
            "entity":
            {
                "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39",
                "type": "Practitioner"
            }
        }
    ]
}'
```
    {% endtab %}

    {% tab group-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Group"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Group",
    "type": "person",
    "actual": True,
    "name": "A Test Team",
    "characteristic":
    [
        {
            "exclude": False,
            "code":
            {
                "text": "responsibility"
            },
            "valueCodeableConcept":
            {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            }
        }
    ],
    "member":
    [
        {
            "entity":
            {
                "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39",
                "type": "Practitioner"
            }
        }
    ]
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="group-create-response">
{% include create_response.html %}
</div>

<div id="group-read-request">
{%  include read_request.html resource_type="Group" %}
</div>

<div id="group-read-response">

  {% tabs group-read-response %}

    {% tab group-read-response 200 %}
```json
{
    "resourceType": "Group",
    "id": "3340c331-d446-4700-9c23-7959bd393f26",
    "type": "person",
    "actual": true,
    "name": "A Test Team",
    "characteristic":
    [
        {
            "exclude": false,
            "code":
            {
                "text": "responsibility"
            },
            "valueCodeableConcept":
            {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            }
        }
    ],
    "member":
    [
        {
            "entity":
            {
                "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39",
                "type": "Practitioner"
            }
        }
    ]
}
```
    {% endtab %}

    {% tab group-read-response 401 %}
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

    {% tab group-read-response 403 %}
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

    {% tab group-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Group resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
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

    {% tab group-update-request curl %}
```shell
curl --request PUT \
     --url https://fumage-example.canvasmedical.com/Group/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Group",
    "id": "3340c331-d446-4700-9c23-7959bd393f26",
    "type": "person",
    "actual": true,
    "name": "A Test Team",
    "characteristic":
    [
        {
            "exclude": false,
            "code":
            {
                "text": "responsibility"
            },
            "valueCodeableConcept":
            {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            }
        }
    ],
    "member":
    [
        {
            "entity":
            {
                "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39",
                "type": "Practitioner"
            }
        }
    ]
}'
```
    {% endtab %}

    {% tab group-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Group/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Group",
    "id": "3340c331-d446-4700-9c23-7959bd393f26",
    "type": "person",
    "actual": True,
    "name": "A Test Team",
    "characteristic":
    [
        {
            "exclude": False,
            "code":
            {
                "text": "responsibility"
            },
            "valueCodeableConcept":
            {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            }
        }
    ],
    "member":
    [
        {
            "entity":
            {
                "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39",
                "type": "Practitioner"
            }
        }
    ]
}
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="group-update-response">
{% include update_response.html resource_type="Group" %}
</div>

<div id="group-search-request">

  {% tabs group-search-request %}

    {% tab group-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Group?type=person \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
    {% endtab %}

    {% tab group-search-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Group?type=person"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
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
    "total": 1,
    "link":
    [
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
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Group",
                "id": "3340c331-d446-4700-9c23-7959bd393f26",
                "type": "person",
                "actual": true,
                "name": "A Test Team",
                "characteristic":
                [
                    {
                        "exclude": false,
                        "code":
                        {
                            "text": "responsibility"
                        },
                        "valueCodeableConcept":
                        {
                            "text": "COLLECT_SPECIMENS_FROM_PATIENT"
                        }
                    }
                ],
                "member":
                [
                    {
                        "entity":
                        {
                            "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39",
                            "type": "Practitioner"
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

    {% tab group-search-response 401 %}
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

    {% tab group-search-response 403 %}
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
