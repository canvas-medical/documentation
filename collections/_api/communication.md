---
title: Communication
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Communication
        article: "a"
        description: >-
          An occurrence of information being transmitted; e.g. a message that was sent to a responsible provider<br><br>
          [https://hl7.org/fhir/R4/communication.html](https://hl7.org/fhir/R4/communication.html)<br><br>
          The Communication resource maps to messages in Canvas. Click [here](https://canvas-medical.zendesk.com/hc/en-us/articles/1500001593221-Patient-Message-Inbox-) to learn more.<br><br>
          **Additional HTML formatting**<br> With the release of Advanced Letter Templates, Messages are now saved in the database in HTML format. Customers using the Communication endpoint for their own patient applications will need to take this into account either by embedding the html directly using a library like Interweave or extracting the text. **Messages sent before this update (10/26/2022 @ 17:00 PST) will remain in plain text format.**<br><br>
        attributes:
          - name: id
            type: string
            description: The identifier of the communication
          - name: status
            type: string
            required: true
            description: >-
              The status of the transmission<br><br>Supported codes for create interactions are: **unknown**
          - name: sent
            type: datetime
            description: When sent<br><br>**ISO 8601 format**
          - name: received
            type: datetime
            description: When received<br><br>**ISO 8601 format**
          - name: recipient
            type: array[json]
            required: true
            description: >-
              Message recipient<br><br>Supported reference types for create interactions: a single **Patient** or **Practitioner**
          - name: sender
            type: json
            required: true
            description: >-
              Message sender<br><br>Supported reference types for create interactions: **Patient**, **Practitioner**
          - name: payload
            type: array[json]
            description: >-
              Message payload<br><br>Supported payload content types: **contentString**
            required: true
        search_parameters:
          - name: _id
            type: string
            description: The unique Canvas identifier of the Communication
          - name: recipient
            type: array[json]
            description: FHIR resource for the recipient, either a Patient or Practitioner
          - name: sender
            type: string
            description: FHIR resource for the sender, either a Patient or Practitioner
        endpoints: [create, search]
        create:
          description: >-
            Messages created through this endpoint will be added to the patient's timeline based on the created date.<br><br>
            If the sender of the message is a `Practitioner`, the message will be displayed as a draft in the timeline, drafter by Canvas Bot. There is no way to mark it as sent via the API today.<br><br>
            If the sender of the message is a patient, the message will show in the recipient's message inbox for review, as well as on the timeline. 
          responses: [201, 400, 401, 403, 405, 422]
          example_request: communication-create-request
          example_response: communication-create-response
        search:
          description: >-
            Communication search will only return messages between a practitioner and patient, not between two practitioners.<br><br>
          responses: [200, 400, 401, 403]
          example_request: communication-search-request
          example_response: communication-search-response
        
---
<div id="communication-create-request">
  {% tabs communication-create-request %}
    {% tab communication-create-request curl %}
```shell
curl --request POST \
     --url https://fumage-example.canvasmedical.com/Communication \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Communication",
  "status": "unknown",
  "sent": "2022-04-29T13:30:00.000Z",
  "received": "2022-04-29T13:30:00.000Z",
  "recipient": [
    {
      "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd"
    }
  ],
  "sender": {
    "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14"
  },
  "payload": [
    {
      "contentString": "Upcoming appointment"
    }
  ]
}'
```
    {% endtab %}

    {% tab communication-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Communication"

payload = {
    "resourceType": "Communication",
    "sent": "2022-04-29T13:30:00.000Z",
    "received": "2022-04-29T13:30:00.000Z",
    "recipient": [{ "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd" }],
    "sender": { "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14" },
    "payload": [{ "contentString": "Upcoming appointment" }]
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

<div id="communication-create-response">
  {% tabs communication-create-response %}
    {% tab communication-create-response 201 %}
```json
null
```
    {% endtab %}
    {% tab communication-create-response 400 %}
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
    {% tab communication-create-response 401 %}
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
    {% tab communication-create-response 403 %}
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
    {% tab communication-create-response 405 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-supported",
      "details": {
        "text": "Operation is not supported"
      }
    }
  ]
}
```
    {% endtab %}
    {% tab communication-create-response 412 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "conflict",
      "details": {
        "text": "Resource updated since If-Unmodified-Since date"
      }
    }
  ]
}
```
    {% endtab %}
    {% tab communication-create-response 422 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "business-rule",
      "details": {
        "text": "Unprocessable entity"
      }
    }
  ]
}
```
    {% endtab %}
  {% endtabs %}
</div>

<div id="communication-search-request">
  {% tabs communication-search-request %}
    {% tab communication-search-request curl %}
```shell
curl --request GET \
    --url 'https://fumage-example.canvasmedical.com/Communication?recipient=Patient%2Fb3084f7e884e4af2b7e23b1dca494abd'\
    --header 'Authorization: Bearer <token>' \
    --header 'accept: application/json'
```
    {% endtab %}

    {% tab communication-search-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Communication?recipient=Patient%2Fb3084f7e884e4af2b7e23b1dca494abd"

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

<div id="communication-search-response">
{% tabs communication-search-response %}
{% tab communication-search-response 200 %}
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 1,
  "link": [
    {
      "relation": "self",
      "url": "/Communication?_id=7433b4b2-0d18-45ca-bb12-71105c80386b&_count=10&_offset=0"
    },
    {
      "relation": "first",
      "url": "/Communication?_id=7433b4b2-0d18-45ca-bb12-71105c80386b&_count=10&_offset=0"
    },
    {
      "relation": "last",
      "url": "/Communication?_id=7433b4b2-0d18-45ca-bb12-71105c80386b&_count=10&_offset=0"
    }
  ],
  "entry": [
    {
      "resource": {
        "resourceType": "Communication",
        "id": "7433b4b2-0d18-45ca-bb12-71105c80386b",
        "status": "unknown",
        "sent": "2021-03-21T10:46:17+00:00",
        "received": "2022-03-14T12:03:58.958000+00:00",
        "recipient": [
          {
            "reference": "Patient/4c21512185184e579b09bfac16dfdd2f",
            "type": "Patient"
          }
        ],
        "sender": {
            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
            "type": "Practitioner"
        },
        "payload": [
          {
            "contentString": "Similique amet at est necessitatibus repellendus eius." 
          }
        ]
      }
    }
  ]
}
```
    {% endtab %}
    {% tab communication-search-response 400 %}
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
    {% tab communication-search-response 401 %}
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
    {% tab communication-search-response 403 %}
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


