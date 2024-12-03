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
          [https://hl7.org/fhir/R4/group.html](https://hl7.org/fhir/R4/group.html)<br><br>
          In Canvas Teams and Patient Groups are mapped to the FHIR Group resource. <br>
          See this [Zendesk article](https://canvas-medical.help.usepylon.com/articles/5123845479-teams) for information about creating teams in Canvas.<br>
          See this [Zendesk article](https://canvas-medical.help.usepylon.com/articles/9728314628-patient-groups) for information about patient groups in Canvas.
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            required_in: update
            exclude_in: create
            description: The identifier of the Group.
            type: string
          - name: type
            description: Identifies the broad classification of the kind of resources the group includes. <br><br> A group with type `person` refers to a Patient Group in canvas, while a group of type `practitioner` refers to a Team in Canvas. 
            type: string
            required_in: create,update
            enum_options: 
                - value: person
                - value: practitioner
          - name: actual
            required_in: create,update
            description: If true, indicates that the resource refers to a specific group of real individuals. If false, the group defines a set of intended individuals. <br><br>
                While this is a required field in FHIR, Canvas assumes all groups are made up of real individuals, so this will be assumed True for all interactions.
            type: boolean
          - name: name
            description: Label for Group.
            type: string
            required_in: create,update
          - name: quantity
            description: Number of members.
            type: integer
            exclude_in: create,update
          - name: characteristic
            description_for_all_endpoints: >-
              Identifies traits whose presence or absence is shared by members of the group<br><br>
              The `text` attribute on the `valueCodeableConcept` for each `characteristic` represents responsibilities held by the Group (in Canvas a Team). Responsibilities may not be shared by more than one team. 
            create_and_update_description: If a group of practitioners is created/updated with a responsibility that another group is assigned, the endpoint will return an error dictating the responsibilities have already been assigned.
            type: array[json]
            attributes:
                - name: code
                  type: json
                  required_in: create, update
                  description: Kind of characteristic
                  attributes:
                    - name: text
                      type: string
                      required_in: create, update
                      description: Plain text representation of the concept.
                      enum_options: 
                        - value: responsibility
                - name: exclude
                  type: boolean
                  exclude_in: create,update
                  description: Group includes or excludes
                  enum_options: 
                    - value: False
                - name: valueCodeableConcept
                  type: json
                  required_in: create, update
                  description: Value held by characteristic.
                  attributes: 
                    - name: text
                      description: Plain text representation of the concept. <br><br>These responsibilities represent the responsibilities of a Canvas Team. They are not applicable for a Patient Group.
                      type: string
                      enum_options:
                        - value: COLLECT_SPECIMENS_FROM_PATIENT
                        - value: COMMUNICATE_DIAGNOSTIC_RESULTS_TO_PATIENT
                        - value: COORDINATE_REFERRALS_FOR_PATIENT
                        - value: PROCESS_REFILL_REQUESTS
                        - value: PROCESS_CHANGE_REQUESTS
                        - value: SCHEDULE_LAB_VISITS_FOR_PATIENT
                        - value: POPULATION_HEALTH_CAMPAIGN_OUTREACH
                        - value: COLLECT_PATIENT_PAYMENTS
                        - value: COMPLETE_OPEN_LAB_ORDERS
                        - value: REVIEW_ERA_POSTING_EXCEPTIONS
                        - value: REVIEW_COVERAGES
          - name: member
            description: Who or what is in group.
            type: array[json]
            attributes:
                - name: entity
                  type: json
                  required_in: create, update
                  description: Reference to the group member.
                  attributes:
                    - name: reference
                      type: string
                      required_in: create,update
                      description: The reference string of the member in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"` or `"Practitioner/a09946c97cb04f44bc36f1c08f6d1b76"`.
                    - name: type
                      type: string
                      description: Type the reference refers to (e.g. "Patient", "Practitioner").
                    - name: display
                      type: string
                      exclude_in: create,update
                      description: Text alternative for the resource.
        search_parameters:
          - name: _id
            description: The identifier of the Group.
            type: string
          - name: type
            description: The type of resources the group contains.
            type: string
            search_options:
                - value: person
                - value: practitioner
        endpoints: [create, read, update, search]
        create:
          description: >-
            Create a Group resource.<br><br>
            **Note:** The Canvas implementation of Group create/update assigns responsibilities to practitioner Groups using the `characteristic` attribute, rather than using the `characteristic` attribute to establish membership.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: group-create-request
          example_response: group-create-response
        read:
          description: Read a Group resource.
          responses: [200, 401, 403, 404]
          example_request: group-read-request
          example_response: group-read-response
        update:
          description: >-
            Update a Group resource.<br><br>
            **Note:** The Canvas implementation of Group create/update assigns responsibilities to practitioner Groups using the `characteristic` attribute, rather than using the `characteristic` attribute to establish membership.
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
     --url 'https://fumage-example.canvasmedical.com/Group' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Group",
    "type": "practitioner",
    "actual": true,
    "name": "A Test Team",
    "characteristic": [
        {
            "code": {
                "text": "responsibility"
            },
            "valueCodeableConcept": {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            },
            "exclude": false
        }
    ],
    "member": [
        {
            "entity": {
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
    "type": "practitioner",
    "actual": True,
    "name": "A Test Team",
    "characteristic": [
        {
            "code": {
                "text": "responsibility"
            },
            "valueCodeableConcept": {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            },
            "exclude": False
        }
    ],
    "member": [
        {
            "entity": {
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
{% include create-response.html %}
</div>

<div id="group-read-request">
{%  include read-request.html resource_type="Group" %}
</div>

<div id="group-read-response">

  {% tabs group-read-response %}

    {% tab group-read-response 200 %}
```json
{
    "resourceType": "Group",
    "id": "3340c331-d446-4700-9c23-7959bd393f26",
    "type": "practitioner",
    "actual": true,
    "name": "A Test Team",
    "characteristic": [
        {
            "code": {
                "text": "responsibility"
            },
            "valueCodeableConcept": {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            },
            "exclude": false
        }
    ],
    "member": [
        {
            "entity": {
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
        "text": "Unknown Group resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
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
     --url 'https://fumage-example.canvasmedical.com/Group/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Group",
    "id": "3340c331-d446-4700-9c23-7959bd393f26",
    "type": "practitioner",
    "actual": true,
    "name": "A Test Team",
    "characteristic": [
        {
            "code": {
                "text": "responsibility"
            },
            "valueCodeableConcept": {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            },
            "exclude": false
        }
    ],
    "member": [
        {
            "entity": {
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
    "type": "practitioner",
    "actual": True,
    "name": "A Test Team",
    "characteristic": [
        {
            "code": {
                "text": "responsibility"
            },
            "valueCodeableConcept": {
                "text": "COLLECT_SPECIMENS_FROM_PATIENT"
            },
            "exclude": False
        }
    ],
    "member": [
        {
            "entity": {
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
{% include update-response.html resource_type="Group" %}
</div>

<div id="group-search-request">
{% include search-request.html resource_type="Group" search_string="type=practitioner" %}
</div>

<div id="group-search-response">

  {% tabs group-search-response %}

    {% tab group-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Group?type=practitioner&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Group?type=practitioner&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Group?type=practitioner&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Group",
                "id": "3340c331-d446-4700-9c23-7959bd393f26",
                "type": "practitioner",
                "actual": true,
                "name": "A Test Team",
                "characteristic": [
                    {
                        "code": {
                            "text": "responsibility"
                        },
                        "valueCodeableConcept": {
                            "text": "COLLECT_SPECIMENS_FROM_PATIENT"
                        },
                        "exclude": false
                    }
                ],
                "member": [
                    {
                        "entity": {
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
