---
title: Communication
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Communication
        article: "a"
        description: >-
          An occurrence of information being transmitted; e.g. an alert that was sent to a responsible provider, a public health agency that was notified about a reportable condition.<br><br> The communication resource maps to messages in Canvas. Click [here](https://canvas-medical.zendesk.com/hc/en-us/articles/1500001593221-Patient-Message-Inbox-) to learn more. 
        attributes:
          - name: id
            description: >-
              The identifier of the communication
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: status
            type: string
          - name: sent
            type: string
          - name: received
            type: string
          - name: recipient
            type: string
          - name: sender
            type: string
          - name: payload
            type: json
            attributes:
              - name: contentString
                type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
          - name: recipient
            type: string
          - name: sender
            type: string
        endpoints: [search, create]
        search:
          description: Communication search will only return messages between a practitioner and patient, not between two practitioners.<br><br>**Additional HTML formatting**<br> With the release of Advanced Letter Templates, Messages are now saved in the database in HTML format. Customers using the Communication endpoint for their own patient applications will need to take this into account either by embedding the html directly using a library like Interweave or extracting the text. **Messages sent before this update (10/26/2022 @ 17:00 PST) will remain in plain text format.**
          responses: [200, 400]
          example_request: communication-search-request
          example_response: communication-search-response
        create:
          description: Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the Location header.<br><br>Messages created through this endpoint will be added to the patient's timeline based on the created date. <br><br>If the sender of the message is a `Practitioner`, the message will be displayed as a draft in the timeline, drafter by Canvas Bot. There is no way to mark it as sent via the API today. <br><br>If the sender of the message is a patient, the message will show in the recipient's message inbox for review, as well as on the timeline. 

          responses: [201, 400]
          example_request: communication-create-request
          example_response: communication-create-response
---
<div id="communication-search-request">
{% tabs communication-search-request %}
{% tab communication-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Communication<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab communication-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Communication<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
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
                        "contentString": "Similique amet at est necessitatibus repellendus eius. Voluptas quis ducimus qui dolorum magni harum odio. Atque qui nihil. Dolorum dolores commodi hic eaque rerum. Excepturi cupiditate doloribus. Modi ea deleniti."
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
{% endtabs %}
</div>

<div id="communication-create-request">
{% tabs communication-create-request %}
{% tab communication-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Communication"

payload = {
    "resourceType": "Communication",
    "sent": "2022-04-29T13:30:00.000Z",
    "received": "2022-04-29T13:30:00.000Z",
    "recipient": [{ "reference": "Patient/5350cd20de8a470aa570a852859ac87e" }],
    "sender": "{             \"reference\": \"Practitioner/5eede137ecfe4124b8b773040e33be14\"         },",
    "payload": [{ "content": "Upcoming appointment hi" }]
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
{% tab communication-create-request curl %}
```sh
curl --request POST \
     --url https://fuamge-example.canvasmedical.com/Communication \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Communication",
  "sent": "2022-04-29T13:30:00.000Z",
  "received": "2022-04-29T13:30:00.000Z",
  "recipient": [
    {
      "reference": "Patient/5350cd20de8a470aa570a852859ac87e"
    }
  ],
  "sender": "{             \"reference\": \"Practitioner/5eede137ecfe4124b8b773040e33be14\"         },",
  "payload": [
    {
      "content": "Upcoming appointment hi"
    }
  ]
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="communication-create-response">
{% tabs communication-create-response %}
{% tab communication-create-response 200 %}
```json
null
```
{% endtab %}
{% tab communication-create-response 400 %}
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

