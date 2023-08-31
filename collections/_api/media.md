---
title: Media
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Media
        article: "a"
        description: >-
          A photo, video, or audio recording acquired or used in healthcare. The actual content may be inline or provided by direct reference.
        attributes:
          - name: integration_type
            type: string
            required: true
          - name: integration_source
            type: string
            required: true
            description: >-
              The source of integration. This will be hardcoded to `fumage` for this endpoint
          - name: patient_identifier
            type: json
            required: true
            attributes:
              - name: identifier_type
                type: string
                required: true
                description: >-
                  The type of integration. This will be hardcoded to `fumage` for this endpoint
              - name: identifier
                type: string
                required: true
                description: >-
                  The identifier for the image
          - name: integration_payload
            type: json
            required: true
            attributes:
              - name: status
                type: string
                required: true
              - name: encounter_id
                type: string
                required: true
              - name: media
                type: json
                required: true
                attributes:
                  - name: content_type
                    type: string
                    required: true
                  - name: content
                    type: string
                    required: true
              - name: originator
                type: string
              - name: title
                type: string
              - name: narrative
                type: string
        endpoints: [create]
        create:
          responses: [201, 400]
          example_request: media-create-request
          example_response: media-create-response
---
<div id="media-create-request">
{% tabs media-create-request %}
{% tab media-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Media"

payload = {
    "resourceType": "Media",
    "status": "completed",
    "subject": { "reference": "Patient/610066552b0a42c5a0095a047cf1bff1" },
    "encounter": { "reference": "Encounter/302fca5c-9231-4eca-83e7-c62b6ab93ba7" },
    "operator": { "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e" },
    "content": {
        "contentType": "image/jpeg",
        "data": "QWxsIHlvdXIgYmFzZSBhcmUgYmVsb25nIHRvIHVzCg==",
        "title": "Image title"
    },
    "note": [{ "text": "First note" }, { "text": "Second note" }]
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
{% tab media-create-request curl %}
```sh
curl --request POST \
     --url https://fumage-example.canvasmedical.com/Media \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Media",
  "status": "completed",
  "subject": {
    "reference": "Patient/610066552b0a42c5a0095a047cf1bff1"
  },
  "encounter": {
    "reference": "Encounter/302fca5c-9231-4eca-83e7-c62b6ab93ba7"
  },
  "operator": {
    "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e"
  },
  "content": {
    "contentType": "image/jpeg",
    "data": "QWxsIHlvdXIgYmFzZSBhcmUgYmVsb25nIHRvIHVzCg==",
    "title": "Image title"
  },
  "note": [
    {
      "text": "First note"
    },
    {
      "text": "Second note"
    }
  ]
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="media-create-response">
{% tabs media-create-response %}
{% tab media-create-response 200 %}
```json
null
```
{% endtab %}
{% tab media-create-response 400 %}
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