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
          The Communication resource maps to messages in Canvas between a patient and practitioner. Click [here](https://canvas-medical.zendesk.com/hc/en-us/articles/1500001593221-Patient-Message-Inbox-) to learn more.<br><br>
          **Additional HTML formatting**<br> With the release of Advanced Letter Templates, Messages are now saved in the database in HTML format. Customers using the Communication endpoint for their own patient applications will need to take this into account either by embedding the html directly using a library like Interweave or extracting the text. **Messages sent before this update (10/26/2022 @ 17:00 PST) will remain in plain text format.**<br><br>
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            type: string
            description: The identifier of the communication.
            exclude_in: create, update
            required_in: update
          - name: status
            type: string
            required_in: create,update
            description_for_all_endpoints: The status of the transmission.
            create_description: >-
             While status is a required attribute, all communication messages will be created with a `completed` status regardless of what is supplied in the payload.
            read_and_search_description: A communication message in Canvas that was sent, received, delivered, or relayed will all appear in FHIR as `completed`. For draft messages in Canvas, they will appear in FHIR as `preparation`. While a FHIR status of `in-progress` are Canvas messages that are scheduled to be delivered at a later time.
            enum_options:
              - value: completed
              - value: in-progress
              - value: preparation
              - value: unknown
          - name: subject
            type: json
            exclude_in: create, update
            description: >-
              Focus of the message.  Always a **Patient** reference.
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: sent
            type: datetime
            description_for_all_endpoints: When sent<br><br>**ISO 8601 format**
            create_description: If not supplied on creation, it will default to the current timestamp.
          - name: received
            type: datetime
            description_for_all_endpoints: When received<br><br>**ISO 8601 format**
            create_description: If no `received` datetime is supplied when the recipient of the message is a Practitioner, the message will appear on the subject's timeline as unread, indicated by a blue circle on the message icon. The practitioner will have the ability to mark the communication message as read in the Canvas UI which will update this attribute.
            read_and_search_description: Messages sent via Canvas UI to a patient will not have a `received` timestamp. <br><br>If the received timestamp is not added via API to messages sent to practitioners, it can still be updated if the practitioner manually marks the message as read in the UI. 
          - name: recipient
            type: array[json]
            required_in: create,update
            description_for_all_endpoints: >-
              Message recipient.<br><br>Supported reference types are a single **Patient** or **Practitioner**. 
            create_description: Between the sender and recipient, one must be a practitioner while the other must be a patient.
            attributes:
              - name: reference
                type: string
                required_in: create,update
                description: The reference string of the sender in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"` or `"Practitioner/ed1e304acdb847148338c6b0596d93fd"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient" or "Practitioner").
          - name: sender
            type: json
            required_in: create,update
            description_for_all_endpoints: >-
              Message sender.<br><br>Supported reference types are a single **Patient** or **Practitioner**. 
            create_description: Between the sender and recipient, one must be a practitioner while the other must be a patient.
            attributes:
              - name: reference
                type: string
                required_in: create,update
                description: The reference string of the sender in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"` or `"Practitioner/ed1e304acdb847148338c6b0596d93fd"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient" or "Practitioner").
          - name: payload
            type: array[json]
            description: Message payload.<br><br>Messages are now saved in the Canvas database in HTML format. Customers using the Communication endpoint for their own patient applications will need to take this into account either by embedding the html directly using a library like Interweave or extracting the text. Messages sent before 10/26/2022 @ 17:00 PST will remain in plain text format.
            required_in: create,update
            attributes:
              - name: contentString
                type: string
                required_in: create,update
                description: Message part content.
        search_parameters:
          - name: _id
            type: string
            description: The unique Canvas identifier of the Communication.
          - name: patient
            type: string
            description: The patient reference that is the subject of the communication in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
          - name: recipient
            type: string
            description: >-
              Message recipient in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"` or `"Practitioner/ed1e304acdb847148338c6b0596d93fd"`.
          - name: sender
            type: string
            description: >-
              Message sender in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"` or `"Practitioner/ed1e304acdb847148338c6b0596d93fd"`.
        endpoints: [create, read, search]
        create:
          description: >-
            Messages created through this endpoint will be added to the patient's timeline and in the patient app based on the ingestion date into Canvas.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: communication-create-request
          example_response: communication-create-response
        read:
          description: Read a Communication resource.
          responses: [200, 401, 403, 404]
          example_request: communication-read-request
          example_response: communication-read-response
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
     --url 'https://fumage-example.canvasmedical.com/Communication' \
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
{% include create-response.html %}
</div>

<div id="communication-search-request">
{% include search-request.html resource_type="Communication" search_string="recipient=Patient/b3084f7e884e4af2b7e23b1dca494abd" %}
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

<div id="communication-read-request">
{%  include read-request.html resource_type="Communication" %}
</div>

<div id="communication-read-response">
{% tabs communication-read-response %}
{% tab communication-read-response 200 %}
```json
{
    "resourceType": "Communication",
    "id": "17b7d61e-4b0e-4940-bd37-b64f5c2ae29d",
    "status": "unknown",
    "sent": "2023-10-23T21:19:22.865089+00:00",
    "recipient": [
        {
            "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e",
            "type": "Practitioner"
        }
    ],
    "sender": {
        "reference": "Patient/43f1418bae9c41919203e0006761067c",
        "type": "Patient"
    },
    "payload": [
        {
            "contentString": "What's up doc?"
        }
    ]
}

```
    {% endtab %}
    {% tab communication-read-response 400 %}
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
    {% tab communication-read-response 401 %}
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
    {% tab communication-read-response 403 %}
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
