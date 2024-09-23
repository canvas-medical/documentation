---
title: Task
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Task
        article: "a"
        description: >-
          A task to be performed.<br><br>[http://hl7.org/fhir/R4/task.html](http://hl7.org/fhir/R4/task.html)
        attributes:
          - name: id
            description: >-
              The identifier of the task
            type: string
          - name: extension
            type: array[json]
            description: >-
              An extension that optionally includes the following:<br><br>
              - The team that the task is assigned to. This optional field requires a reference to the team from the [Group](/api/group) endpoint. In the Canvas UI, this will display under the field **team** in the task card.
              <br><br>
              - A [permalink](https://canvas-medical.zendesk.com/hc/en-us/articles/13341828094227-Linking-Resources-to-Tasks) URL to the task.
          - name: status
            type: string
            description: >- # TODO - enter status mapping table from README. Having rendering issues with the table
              The current status of the task. Supported values are **requested**, **cancelled** and **completed**.
            required_in: create,update
          - name: description
            type: string
            required_in: create,update
            description: Human-readable explanation of task
          - name: for
            type: json
            description: Beneficiary of the Task. This must be a [Patient](/api/patient) reference.
          - name: authoredOn
            type: datetime
            description: Task Creation Date. If omitted from the message, it will default to the current timestamp at the time of ingestion.
          - name: lastModified
            type: datetime
            exclude_in: create, update
            description: Task Update Date. Whenever the task receieves any updates, including comments, this field will be updated accordingly.
          - name: requester
            type: json
            required_in: create,update
            description: Who is asking for task to be done. This must be a [Practitioner](/api/practitioner) reference.
          - name: owner
            type: json
            description: Responsible individual. This must be a [Practitioner](/api/practitioner) reference.
          - name: intent
            type: string
            required_in: create,update
            description: Distinguishes whether the task is a proposal, plan or full order. Canvas does not have a mapping for this field, so it should always be set to **unknown**.
          - name: restriction
            type: json
            description: Constraints on fulfillment tasks. In Canvas, this field is used to represent the due date for a task.
          - name: note
            type: array[json]
            description: >-
              Comments made about the task. For each comment, the following values can be specified:<br>
              - The comment's text<br>
              - Timestamp the comment was left. If omitted, this will default to current timestamp at data ingestion.<br>
              - Reference to the practitioner that left the specific comment<br>
          - name: input
            type: array[json]
            description: >-
              Information used to perform the task. This field will add labels to the task in the Canvas UI. If the label doesn't exist in Canvas already, it will be created.
        search_parameters:
          - name: _id
            type: string
            description: Search by a task id
          - name: _sort
            type: string
            description: Triggers sorting of the results by a specific criteria. Accepted values are **_id** and **due-date**. Use **-_id** or **-due-date** to sort in descending order.
          - name: description
            type: string
            description: Search by description
          - name: due
            type: string
            description: Filter by the task's due date and time. See [Date Filtering](/api/date-filtering) for more information.
          - name: label
            type: string
            description: Search for a task with an associated label
          - name: modified
            type: string
            description: Filter by the tasks' modified date and time. See [Date Filtering](/api/date-filtering) for more information.
          - name: owner
            type: string
            description: Search by task owner
          - name: patient
            type: string
            description: Search by patient
          - name: requester
            type: string
            description: Search by task requester
          - name: status
            type: string
            description: Search by task status
        endpoints: [create, read, update, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: task-create-request
          example_response: task-create-response
          description: >-
            Create a task.<br><br>
            Tasks created through this FHIR Endpoint will display in the [patient chart via the tasks icon](https://canvas-medical.zendesk.com/hc/en-us/articles/360057545873-Tasks). Open tasks will also display in the [Task Panel](https://canvas-medical.zendesk.com/hc/en-us/articles/360059339433-Task-List).
        read:
          description: Read a Task resource.
          responses: [200, 401, 403, 404]
          example_request: task-read-request
          example_response: task-read-response
        update:
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: task-update-request
          example_response: task-update-response
          description: Update a task.<br><br>Any `note` comments included in the update message body will not be checked if they already exist in Canvas. Canvas will always assume each Note is an addition to the Task Comments.<br><br>Omitting the group `extension` and `authoredOn` fields in an update body does not delete the contents of that field. They will remain set to the last value they were assigned.<br><br>Omitting the `description`, `owner`, `restriction` and `input` attributes will delete the contents of the field in the Canvas database. In order to have a Task keep the values in these fields after an update, they must be included.
        search:
          responses: [200, 400, 401, 403]
          example_request: task-search-request
          example_response: task-search-response
          description: Search for a task
---

<div id="task-create-request">

  {% tabs task-create-request %}

    {% tab task-create-request curl %}
```sh
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Task' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Task",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
            "valueReference": {
                "reference": "Group/0c59ba86-dd40-4fde-8179-6e0b91dc617b"
            }
        }
    ],
    "status": "requested",
    "description": "Ask patient for new insurance information.",
    "for": { "reference": "Patient/cfd91cd3bd9046db81199aa8ee4afd7f" },
    "authoredOn": "2023-09-22T14:00:00.000Z",
    "requester": { "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e" },
    "owner": { "reference": "Practitioner/a02cbf2403e140f7bc9a355c6ed420f3" },
    "intent": "unknown",
    "restriction": { "period": { "end": "2023-09-23T14:00:00.000Z" } },
    "note": [
        {
            "text": "Please call patient to update insurance information.",
            "time": "2023-09-22T14:00:00.000Z",
            "authorReference": { "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e" }
        }
    ],
    "input": [
        {
            "type": { "text": "label" },
            "valueString": "Urgent"
        }
    ]
}
'
```
    {% endtab %}

    {% tab task-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Task"

payload = {
    "resourceType": "Task",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
            "valueReference": {
                "reference": "Group/0c59ba86-dd40-4fde-8179-6e0b91dc617b"
            }
        }
    ],
    "status": "requested",
    "description": "Ask patient for new insurance information.",
    "for": { "reference": "Patient/cfd91cd3bd9046db81199aa8ee4afd7f" },
    "authoredOn": "2023-09-22T14:00:00.000Z",
    "requester": { "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e" },
    "owner": { "reference": "Practitioner/a02cbf2403e140f7bc9a355c6ed420f3" },
    "intent": "unknown",
    "restriction": { "period": { "end": "2023-09-23T14:00:00.000Z" } },
    "note": [
        {
            "text": "Please call patient to update insurance information.",
            "time": "2023-09-22T14:00:00.000Z",
            "authorReference": { "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e" }
        }
    ],
    "input": [
        {
            "type": { "text": "label" },
            "valueString": "Urgent"
        }
    ]
}

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="task-create-response">
{% include create-response.html %}
</div>

<div id="task-read-request">
{% include read-request.html resource_type="Task" %}
</div>

<div id="task-read-response">

  {% tabs task-read-response %}

    {% tab task-read-response 200 %}
```json
 {
    "resourceType": "Task",
    "id": "5f72fbcc-10ac-48ff-a2d2-02b229c38ce9",
    "extension":
    [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
            "valueReference":
            {
                "reference": "Group/0c59ba86-dd40-4fde-8179-6e0b91dc617b",
                "type": "Group",
                "display": "Payment Collection"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-permalink",
            "valueString": "http://example.canvasmedical.com/permalinks/v1/VGFzazo4OTo3MA=="
        }
    ],
    "status": "completed",
    "description": "Ask patient for new insurance information.",
    "for":
    {
        "reference": "Patient/cfd91cd3bd9046db81199aa8ee4afd7f",
        "type": "Patient"
    },
    "authoredOn": "2023-09-22T14:00:00+00:00",
    "lastModified": "2023-10-22T21:06:27.893521+00:00",
    "requester":
    {
        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
        "type": "Practitioner"
    },
    "owner":
    {
        "reference": "Practitioner/a02cbf2403e140f7bc9a355c6ed420f3",
        "type": "Practitioner"
    },
    "intent": "unknown",
    "restriction":
    {
        "period":
        {
            "end": "2023-09-23T14:00:00+00:00"
        }
    },
    "note":
    [
        {
            "authorReference":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                "type": "Practitioner"
            },
            "time": "2023-09-22T14:00:00+00:00",
            "text": "Please call patient to update insurance information."
        }
    ],
    "input":
    [
        {
            "type":
            {
                "text": "label"
            },
            "valueString": "Urgent"
        }
    ]
}
```
    {% endtab %}

    {% tab task-read-response 401 %}
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

    {% tab task-read-response 403 %}
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

    {% tab task-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Task resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="task-update-request">

  {% tabs task-update-request %}

    {% tab task-update-request curl %}
```sh
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/Task/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Task",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
            "valueReference": {
                "reference": "Group/0c59ba86-dd40-4fde-8179-6e0b91dc617b"
            }
        }
    ],
    "status": "completed",
    "description": "Ask patient for new insurance information.",
    "for": { "reference": "Patient/cfd91cd3bd9046db81199aa8ee4afd7f" },
    "authoredOn": "2023-09-22T14:00:00.000Z",
    "requester": { "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e" },
    "owner": { "reference": "Practitioner/a02cbf2403e140f7bc9a355c6ed420f3" },
    "intent": "unknown",
    "restriction": { "period": { "end": "2023-09-23T14:00:00.000Z" } },
    "note": [
        {
            "text": "Please call patient to update insurance information.",
            "time": "2023-09-22T14:00:00.000Z",
            "authorReference": { "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e" }
        }
    ],
    "input": [
        {
            "type": { "text": "label" },
            "valueString": "Urgent"
        }
    ]
}
'
```
    {% endtab %}

    {% tab task-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Task/<id>"

payload = {
    "resourceType": "Task",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
            "valueReference": {
                "reference": "Group/0c59ba86-dd40-4fde-8179-6e0b91dc617b"
            }
        }
    ],
    "status": "completed",
    "description": "Ask patient for new insurance information.",
    "for": { "reference": "Patient/cfd91cd3bd9046db81199aa8ee4afd7f" },
    "authoredOn": "2023-09-22T14:00:00.000Z",
    "requester": { "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e" },
    "owner": { "reference": "Practitioner/a02cbf2403e140f7bc9a355c6ed420f3" },
    "intent": "unknown",
    "restriction": { "period": { "end": "2023-09-23T14:00:00.000Z" } },
    "note": [
        {
            "text": "Please call patient to update insurance information.",
            "time": "2023-09-22T14:00:00.000Z",
            "authorReference": { "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e" }
        }
    ],
    "input": [
        {
            "type": { "text": "label" },
            "valueString": "Urgent"
        }
    ]
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

  {% endtabs %}

</div>

<div id="task-update-response">
{% include update-response.html resource_type="Task" %}
</div>

<div id="task-search-request">
{% include search-request.html resource_type="Task" search_string="owner=Practitioner%2Fa02cbf2403e140f7bc9a355c6ed420f3&label=Urgent" %}
</div>

<div id="task-search-response">
{% tabs task-search-response %}
{% tab task-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
        {
            "relation": "self",
            "url": "/Task?owner=Practitioner%2Fa02cbf2403e140f7bc9a355c6ed420f3&label=Urgent&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Task?owner=Practitioner%2Fa02cbf2403e140f7bc9a355c6ed420f3&label=Urgent&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Task?owner=Practitioner%2Fa02cbf2403e140f7bc9a355c6ed420f3&label=Urgent&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Task",
                "id": "5f72fbcc-10ac-48ff-a2d2-02b229c38ce9",
                "extension":
                [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
                        "valueReference":
                        {
                            "reference": "Group/0c59ba86-dd40-4fde-8179-6e0b91dc617b",
                            "type": "Group",
                            "display": "Payment Collection"
                        }
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/task-permalink",
                        "valueString": "http://example.canvasmedical.com/permalinks/v1/VGFzazo4OTo3MA=="
                    }
                ],
                "status": "completed",
                "description": "Ask patient for new insurance information.",
                "for":
                {
                    "reference": "Patient/cfd91cd3bd9046db81199aa8ee4afd7f",
                    "type": "Patient"
                },
                "authoredOn": "2023-09-22T14:00:00+00:00",
                "lastModified": "2023-10-22T21:06:27.893521+00:00",
                "requester":
                {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                },
                "owner":
                {
                    "reference": "Practitioner/a02cbf2403e140f7bc9a355c6ed420f3",
                    "type": "Practitioner"
                },
                "intent": "unknown",
                "restriction":
                {
                    "period":
                    {
                        "end": "2023-09-23T14:00:00+00:00"
                    }
                },
                "note":
                [
                    {
                        "authorReference":
                        {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner"
                        },
                        "time": "2023-09-22T14:00:00+00:00",
                        "text": "Please call patient to update insurance information."
                    }
                ],
                "input":
                [
                    {
                        "type":
                        {
                            "text": "label"
                        },
                        "valueString": "Urgent"
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab task-search-response 400 %}
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
{% tab task-search-response 401 %}
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
{% tab task-search-response 403 %}
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
