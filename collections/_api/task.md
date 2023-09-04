---
title: Task
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Task
        article: "a"
        description: >-
          A task to be performed.
        attributes:
          - name: id
            description: >-
              The identifier of the task
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: status
            type: string
            required: true
          - name: description
            type: string
            required: true
          - name: for
            type: string
            required: true
          - name: authoredOn
            type: datetime
            required: true
          - name: requester
            type: string
            required: true
          - name: owner
            type: string
            required: true
          - name: intent
            type: string
            required: true
          - name: restriction
            type: json
            required: true
            attributes:
              - name: period
                type: json
                required: true
                attributes:
                  - name: end
                    type: datetime
                    required: true
          - name: note
            type: json
            required: true
            attributes:
              - name: text
                type: string
                required: true
              - name: authorReference
                type: string
                required: true
              - name: time
                type: datetime
                required: true
          - name: input
            type: string
            required: true
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: label
            type: string
            description: A human-readable label for the task
          - name: owner
            type: string
            description: The owner of the task
          - name: description
            type: string
            description: A description of the task
          - name: patient
            type: string
            description: The patient associated with the task
          - name: requester
            type: string
            description: The requester of the task
        endpoints: [search, create, update]
        search:
          responses: [200, 400]
          example_request: task-search-request
          example_response: task-search-response
        create:
          responses: [201, 400]
          example_request: task-create-request
          example_response: task-create-response
        update:
          responses: [200, 400]
          example_request: task-update-request
          example_response: task-update-response
---
<div id="task-search-request">
{% tabs task-search-request %}
{% tab task-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Task?_id=<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab task-search-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/Task?_id=<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="task-search-response">
{% tabs task-search-response %}
{% tab task-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Task?_id=3ff6b4a0-e172-490c-b8cd-45bedf156bd8&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Task?_id=3ff6b4a0-e172-490c-b8cd-45bedf156bd8&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Task?_id=3ff6b4a0-e172-490c-b8cd-45bedf156bd8&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Task",
                "id": "3ff6b4a0-e172-490c-b8cd-45bedf156bd8",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/task-permalink",
                        "valueString": "https://training.canvasmedical.com/permalinks/v1/VGFzazoxMTY6MzU0OQ=="
                    }
                ],
                "status": "requested",
                "intent": "unknown",
                "description": "call bob (juan test)  <patient:26566:4675f8a6f65944c7b0e2b8abf8e196ea|Juan Zapata (Sebastian)>",
                "for": {
                    "reference": "Patient/4675f8a6f65944c7b0e2b8abf8e196ea",
                    "type": "Patient"
                },
                "authoredOn": "2023-08-31T14:31:42.363988+00:00",
                "requester": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                },
                "owner": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
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

<div id="task-create-request">
{% tabs task-create-request %}
{% tab task-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Task"

payload = {
    "resourceType": "Task",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
            "valueReference": {
                "reference": "Group/9bf1d726-8c04-4aed-8b0e-e066f4d54b13",
                "display": "All Responsibilities"
            }
        }
    ],
    "status": "requested",
    "requester": { "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14" },
    "description": "Ask patient for new insurance information.",
    "for": { "reference": "Patient/5350cd20de8a470aa570a852859ac87e" },
    "owner": { "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e" },
    "authoredOn": "2022-03-20T14:00:00.000Z",
    "restriction": { "period": { "end": "2022-08-01T04:00:00+00:00" } },
    "note": [
        {
            "text": "Please be sure to scan them in at their next visit.",
            "time": "2022-03-20T14:00:00.000Z",
            "authorReference": { "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14" }
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
{% tab task-create-request curl %}
```sh
curl --request POST \
     --url https://fumage-example.canvasmedical.com/Task \
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
        "reference": "Group/9bf1d726-8c04-4aed-8b0e-e066f4d54b13",
        "display": "All Responsibilities"
      }
    }
  ],
  "status": "requested",
  "requester": {
    "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14"
  },
  "description": "Ask patient for new insurance information.",
  "for": {
    "reference": "Patient/5350cd20de8a470aa570a852859ac87e"
  },
  "owner": {
    "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e"
  },
  "authoredOn": "2022-03-20T14:00:00.000Z",
  "restriction": {
    "period": {
      "end": "2022-08-01T04:00:00+00:00"
    }
  },
  "note": [
    {
      "text": "Please be sure to scan them in at their next visit.",
      "time": "2022-03-20T14:00:00.000Z",
      "authorReference": {
        "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14"
      }
    }
  ],
  "input": [
    {
      "type": {
        "text": "label"
      },
      "valueString": "Urgent"
    }
  ]
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="task-create-response">
{% tabs task-create-response %}
{% tab task-create-response 201 %}
```json
null
```
{% endtab %}
{% tab task-create-response 400 %}
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

<div id="task-update-request">
{% tabs task-update-request %}
{% tab task-update-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Task/_id"

payload = {
    "resourceType": "Task",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
            "valueReference": {
                "reference": "Group/9bf1d726-8c04-4aed-8b0e-e066f4d54b13",
                "display": "All Responsibilities"
            }
        }
    ],
    "for": { "reference": "Patient/5350cd20de8a470aa570a852859ac87e" },
    "status": "requested",
    "requester": { "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14" },
    "description": "Ask patient for new insurance information.",
    "owner": { "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e" },
    "authoredOn": "2022-03-20T14:00:00.000Z",
    "restriction": "{         \"period\": {             \"end\": \"2022-08-01T04:00:00+00:00\"         }     }",
    "note": "[         {             \"text\": \"Please be sure to scan them in at their next visit.\",             \"time\": \"2022-03-20T14:00:00.000Z\"             \"authorReference\": {               \"reference\": \"Practitioner/5eede137ecfe4124b8b773040e33be14\"             }         }     ]",
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
{% tab task-update-request curl %}
```sh
curl --request PUT \
     --url https://fumage-example.canvasmedical.com/Task/_id \
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
        "reference": "Group/9bf1d726-8c04-4aed-8b0e-e066f4d54b13",
        "display": "All Responsibilities"
      }
    }
  ],
  "for": {
    "reference": "Patient/5350cd20de8a470aa570a852859ac87e"
  },
  "status": "requested",
  "requester": {
    "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14"
  },
  "description": "Ask patient for new insurance information.",
  "owner": {
    "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e"
  },
  "authoredOn": "2022-03-20T14:00:00.000Z",
  "restriction": "{         \"period\": {             \"end\": \"2022-08-01T04:00:00+00:00\"         }     }",
  "note": "[         {             \"text\": \"Please be sure to scan them in at their next visit.\",             \"time\": \"2022-03-20T14:00:00.000Z\"             \"authorReference\": {               \"reference\": \"Practitioner/5eede137ecfe4124b8b773040e33be14\"             }         }     ]",
  "input": [
    {
      "type": {
        "text": "label"
      },
      "valueString": "Urgent"
    }
  ]
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="task-update-response">
{% tabs task-update-response %}
{% tab task-update-response 200 %}
```json
null
```
{% endtab %}
{% tab task-update-response 400 %}
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


