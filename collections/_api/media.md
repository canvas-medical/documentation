---
title: Media
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Media
        article: "a"
        description: >-
          A photo, video, or audio recording acquired or used in healthcare.<br><br>
          [https://hl7.org/fhir/R4/media.html](https://hl7.org/fhir/R4/media.html)<br><br>
          FHIR Media maps to a [Visual Exam Finding Command](https://canvas-medical.help.usepylon.com/articles/4119751144-command-visual-exam-finding) in Canvas.
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the Media.
            type: string
            exclude_in: create
          - name: extension
            type: array[json]
            description_for_all_endpoints: Canvas supports a note identifier extension on this resource. The note identifier can be used with the [Canvas Note API](/api/note).
            create_description: Canvas recommends sending the note identifier extension or the Encounter reference, but not both. If both are supplied, they must both refer to the same note. If neither is specified, it will insert into a Data Import note where the DOS is the current time of ingestion.
            attributes:
                - name: url
                  type: string
                  description: Source that defines the content of this object.
                  enum_options:
                    - value: http://schemas.canvasmedical.com/fhir/extensions/note-id
                - name: valueId
                  type: string
                  description: The valueId field is used for the Note extension and will be the note's unique identifier.
          - name: status
            required_in: create
            description: The current state of the media.
            enum_options:
              - value: completed
              - value: entered-in-error
            type: string
          - name: subject
            required_in: create
            description: Who/What this Media is a record of.
            type: json
            attributes:
              - name: reference
                type: string
                required_in: create
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: encounter
            description_for_all_endpoints: Encounter associated with media.
            create_description: >-
                Supply an encounter reference to be able to insert the allergy command into a specific note on the patient's timeline. If no encounter is specified, it will insert into a Data Import note where the DOS is the current time of ingestion.
                <br><br>
                **Canvas does not currently support concurrent creation of resources on the same encounter.** Please avoid issuing concurrent requests that reference the same encounter to this endpoint, or to any other endpoints that reference encounters. It is OK to issue concurrent requests to these endpoints as long as the requests reference different encounters.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the encounter in the format of `"Encounter/086cd6fe-2c94-455d-a53e-6ff1c2652cae"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Encounter").
          - name: operator
            description: >-
              The person who generated the image.<br><br>
              The operator attribute contains a reference to the practitioner or patient that generated the media. This will show up in the Canvas UI as the value for Originator when you click the command in the tooltip that pops up. If omitted, it will default to Canvas Bot.
            type: json
            attributes:
              - name: reference
                type: string
                required_in: create
                description: The reference string of the operator in the format of `"Practitioner/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
          - name: content
            required_in: create
            description_for_all_endpoints: Actual Media.
            read_and_search_description: >-
              **Note: There is a temporary extension that will contain the presigned URL for the Attachment; this will be provided while we migrate to static URLs that will require bearer authentication to retrieve attachment files. Use this extension for backward-compatible URLs until the migration is completed.**
            type: json
            attributes:
              - name: contentType
                type: string
                required_in: create
                description: Mime type of the content, with charset etc.
                enum_options:
                  - value: image/heic
                  - value: image/jpeg
                  - value: image/png
              - name: data
                type: string
                exclude_in: read, search
                required_in: create
                description: Inline data in Base64 format.
              - name: title
                type: string
                description: Label to display in place of the data. This will appear on the Visual Exam Finding Command in the patient's chart.
              - name: url
                type: string
                exclude_in: create
                description: Uri where the data can be found.
          - name: note
            description: >-
              Comments made about the media<br><br>
              The note attribute is an array of JSON objects, each of which contains a text attribute that contains the text of a comment that will be attached to the inserted media on the UI.
            type: array[json]
            attributes:
              - name: text
                type: string
                required_in: create
                description: The annotation - text content.
        endpoints: [create, read, search]
        create:
          description: Create a Media resource.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: media-create-request
          example_response: media-create-response
        read:
          description: Read a Media resource.
          responses: [200, 401, 403, 404]
          example_request: media-read-request
          example_response: media-read-response
        update:
          description: Update an Media resource.
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: media-update-request
          example_response: media-update-response
        search:
          description: Search for Media resources.
          responses: [200, 400, 401, 403]
          example_request: media-search-request
          example_response: media-search-response
        search_parameters:
          - name: _id
            description: The identifier of the Media.
            type: string
          - name: patient
            description: The patient the media is associated with in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
---

<div id="media-create-request">

  {% tabs media-create-request %}

    {% tab media-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Media' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Media",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "status": "completed",
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "operator": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "content": {
        "contentType": "image/jpeg",
        "data": "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",
        "title": "Image title"
    },
    "note": [
        {
            "text": "Note #1"
        },
        {
            "text": "Note #2"
        }
    ]
}'
```
    {% endtab %}

    {% tab media-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Media"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Media",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "status": "completed",
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "operator": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "content": {
        "contentType": "image/jpeg",
        "data": "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",
        "title": "Image title"
    },
    "note": [
        {
            "text": "Note #1"
        },
        {
            "text": "Note #2"
        }
    ]
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="media-create-response">
{% include create-response.html %}
</div>

<div id="media-read-request">
{%  include read-request.html resource_type="Media" %}
</div>

<div id="media-read-response">

  {% tabs media-read-response %}

    {% tab media-read-response 200 %}
```json
{
    "resourceType": "Media",
    "id": "729e5242-bad6-4bd7-905d-9716ae262971",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "status": "completed",
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "operator": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "content": {
        "extension": [
              {
                  "url": "http://schemas.canvasmedical.com/fhir/extensions/deprecated-url",
                  "valueUri": "https://canvas-client-media.s3.amazonaws.com/local/20240412_124150_e8443b40ac434173a45e649b40b6a9f4.png?AWSAccessKeyId=AKIAQB7SIDR7C2IYANB6&Signature=cTm%2BodgYbW8WSgnjUld8GBmmRXo%3D&Expires=1714137543"
              }
        ],
        "contentType": "image/jpeg",
        "url": "https://fumage-example.canvasmedical.com/Media/729e5242-bad6-4bd7-905d-9716ae262971/files/content",
        "title": "Image title"
    },
    "note": [
        {
            "text": "Note #1"
        },
        {
            "text": "Note #2"
        }
    ]
}
```
    {% endtab %}

    {% tab media-read-response 401 %}
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

    {% tab media-read-response 403 %}
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

    {% tab media-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Media resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="media-search-request">
{% include search-request.html resource_type="Media" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="media-search-response">

  {% tabs media-search-response %}

    {% tab media-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Media?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Media?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Media?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Media",
                "id": "729e5242-bad6-4bd7-905d-9716ae262971",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
                        "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
                    }
                ],
                "status": "completed",
                "subject": {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
                    "type": "Patient"
                },
                "encounter": {
                    "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
                },
                "operator": {
                    "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
                },
                "content": {
                    "extension": [
                        {
                            "url": "http://schemas.canvasmedical.com/fhir/extensions/deprecated-url",
                            "valueUri": "https://canvas-client-media.s3.amazonaws.com/local/20240412_124150_e8443b40ac434173a45e649b40b6a9f4.png?AWSAccessKeyId=AKIAQB7SIDR7C2IYANB6&Signature=cTm%2BodgYbW8WSgnjUld8GBmmRXo%3D&Expires=1714137543"
                        }
                    ],
                    "contentType": "image/jpeg",
                    "url": "https://fumage-example.canvasmedical.com/Media/729e5242-bad6-4bd7-905d-9716ae262971/files/content",
                    "title": "Image title"
                },
                "note": [
                    {
                        "text": "Note #1"
                    },
                    {
                        "text": "Note #2"
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab media-search-response 400 %}
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

    {% tab media-search-response 401 %}
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

    {% tab media-search-response 403 %}
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
