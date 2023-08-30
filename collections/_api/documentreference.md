---
title: DocumentReference
sections:
  - type: section
    blocks:
      - type: apidoc
        name: DocumentReference
        article: "a"
        description: >-
          A reference to a document of any kind for any purpose. Provides metadata about the document so that the document can be discovered and managed. The scope of a document is any seralized object with a mime-type, so includes formal patient centric documents (CDA), cliical notes, scanned paper, and non-patient specific documents like policy text.
        attributes:
          - name: id
            description: >-
              The identifier of the document reference
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: status
            description: >-
              The status of the document reference
            type: string
            required: true
          - name: type
            description: >-
              The kind of document
            type: json
            required: true
            attribute:
              - name: coding
                type: json
                required: true
          - name: category
            description: >-
              Categorization of document
            type: array
            required: true
            attribute:
              - name: coding
                type: json
                required: true
          - name: subject
            description: >-
              Who/what is the subject of the document
            type: string
          - name: identifier
            type: json
            description: >-
              Other identifiers for the document
            attribute:
              - name: system
                type: string
              - name: value
                type: string
          - name: date
            description: >-
              The date the document was created
            type: date
          - name: author
            description: >-
              Who and/or what authored the document
            type: string
          - name: custodian
            description: >-
              Organization which maintains the document
            type: string
          - name: content
            type: array
            description: >-
              Document referenced
            attributes:
              - name: attachment
                type: json
                attributes:
                  - name: contentType
                    type: string
                  - name: url
                    type: string
              - name: format
                type: json
                attributes:
                  - name: system
                    type: string
                  - name: code
                    type: string
                  - name: display
                    type: string
          - name: context
            type: json
            description: >-
              Clinical context of document
            attributes:
              - name: encounter
                type: string
              - name: period
                type: json
                attributes:
                  - name: start
                    type: date
                  - name: end
                    type: date
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
          - name: subject
            type: string
          - name: category
            type: string
          - name: status
            type: string
          - name: date
            type: date
          - name: type
            type: string
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_request: document-reference-read-request
          example_response: document-reference-read-response
        search:
          responses: [200, 400]
          example_request: document-reference-search-request
          example_response: document-reference-search-response
---
<div id="document-reference-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/DocumentReference/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/DocumentReference/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="document-reference-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "DocumentReference",
    "id": "6f60ed1c-a6b3-4791-99f0-f618704e33d1",
    "status": "current",
    "type": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "94093-2",
                "display": "Itemized bill"
            }
        ]
    },
    "category": [
        {
            "coding": [
                {
                    "code": "invoicefull"
                }
            ]
        }
    ],
    "subject": {
        "reference": "Patient/f3d750f5d77d403c96baef6a6055c6e7",
        "type": "Patient"
    },
    "date": "2021-10-27T00:00:00+00:00",
    "author": [
        {
            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
            "type": "Practitioner"
        }
    ],
    "custodian": {
        "reference": "Organization/00000000-0000-0000-0002-000000000000",
        "type": "Organization"
    },
    "content": [
        {
            "attachment": {
                "contentType": "application/pdf",
                "url": "https://canvas-client-media.s3.amazonaws.com/training/invoices/f3d750f5d77d403c96baef6a6055c6e7_20211027_193132.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=KuerA1REbZw9d%2BhLL0yZgEumjek%3D&Expires=1693418727"
            },
            "format": {
                "system": "http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem",
                "code": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
                "display": "mimeType Sufficient"
            }
        }
    ]
}
```
{% endtab %}
{% tab search-response 404 %}
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


<div id="document-reference-search-request">
{% tabs search-request %}
{% tab search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/DocumentReference"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/DocumentReference \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="document-reference-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
   "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link": [
        {
            "relation": "self",
            "url": "/DocumentReference?status=current&type=http%3A%2F%2Floinc.org%7C94093-2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/DocumentReference?status=current&type=http%3A%2F%2Floinc.org%7C94093-2&_count=10&_offset=0"
        },
        {
            "relation": "next",
            "url": "/DocumentReference?status=current&type=http%3A%2F%2Floinc.org%7C94093-2&_count=10&_offset=10"
        },
        {
            "relation": "last",
            "url": "/DocumentReference?status=current&type=http%3A%2F%2Floinc.org%7C94093-2&_count=10&_offset=1490"
        }
    ],
"entry": [
        {
            "resource": {
                "resourceType": "DocumentReference",
                "id": "6f60ed1c-a6b3-4791-99f0-f618704e33d1",
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "94093-2",
                            "display": "Itemized bill"
                        }
                    ]
                },
                "category": [
                    {
                        "coding": [
                            {
                                "code": "invoicefull"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/f3d750f5d77d403c96baef6a6055c6e7",
                    "type": "Patient"
                },
                "date": "2021-10-27T00:00:00+00:00",
                "author": [
                    {
                        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                        "type": "Practitioner"
                    }
                ],
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/invoices/f3d750f5d77d403c96baef6a6055c6e7_20211027_193132.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=5rQHzcXayn5z89bsptnrHSa7IEQ%3D&Expires=1693418670"
                        },
                        "format": {
                            "system": "http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem",
                            "code": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
                            "display": "mimeType Sufficient"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "DocumentReference",
                "id": "df175bb0-7087-4ffa-8a1b-461035b8867f",
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "94093-2",
                            "display": "Itemized bill"
                        }
                    ]
                },
                "category": [
                    {
                        "coding": [
                            {
                                "code": "invoicefull"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/a9c9602ae62f4e03bb3262382915fd74",
                    "type": "Patient"
                },
                "date": "2021-12-29T00:00:00+00:00",
                "author": [
                    {
                        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                        "type": "Practitioner"
                    }
                ],
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/invoices/a9c9602ae62f4e03bb3262382915fd74_20211229_131850.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=LMx9qAKxrd5HzQggJf7o%2FMGzyQQ%3D&Expires=1693418670"
                        },
                        "format": {
                            "system": "http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem",
                            "code": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
                            "display": "mimeType Sufficient"
                        }
                    }
                ]
            }
        }
    ]
```
{% endtab %}
{% tab search-response 400 %}
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
