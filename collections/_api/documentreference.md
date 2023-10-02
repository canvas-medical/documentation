---
title: DocumentReference
sections:
  - type: section
    blocks:
      - type: apidoc
        name: DocumentReference
        article: "a"
        description: >-
          A reference to a document of any kind for any purpose. Provides metadata about the document so that the document can be discovered and managed. The scope of a document is any seralized object with a mime-type, so includes formal patient centric documents (CDA), cliical notes, scanned paper, and non-patient specific documents like policy text.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-documentreference.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-documentreference.html)<br><br>
          PDFs are generated for lab reports, imaging reports and invoicing associated with a patient.
        attributes:
          - name: id
            description: >-
              The identifier of the document reference
            type: string
            required: true
          - name: identifier
            type: array[json]
            description: Other identifiers for the document
            type: string
          - name: status
            description: >-
              The status of the document reference. Supported values are: **current**, **superseded** and **entered-in-error**.
            type: string
          - name: type
            description: >-
              A coding for the type of document
            type: json
          - name: category
            description: >-
              The categorization of the document. Supported category codes are: **labreport**, **imagingreport**, **educationalmaterial** and **invoicefull**.
            type: array[json]
          - name: subject
            description: >-
              Who/what is the subject of the document
            type: json
          - name: date
            description: >-
              When this document reference was created
            type: date
          - name: author
            description: >-
              Who and/or what authored the document
            type: array[json]
          - name: custodian
            description: >-
              Organization which maintains the document
            type: json
          - name: content
            type: array[json]
            description: >-
              Document referenced
          - name: context
            type: json
            description: >-
              Clinical context of document
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: category
            type: string
            description: >-
              Categorization of document
          - name: date
            type: date
            description: The date the document was created
          - name: patient
            type: string
            description: The patient associated with the document
          - name: status
            type: string
            description: The status of the document reference
          - name: subject
            description: The patient associated with the document. Can be used interchangeably with the patient parameter.
            type: string
          - name: type
            type: string
            description: Kind of document (LOINC if possible)
        endpoints: [read, search]
        read:
          responses: [200, 401, 403, 404]
          example_request: document-reference-read-request
          example_response: document-reference-read-response
        search:
          responses: [200, 400, 401, 403]
          example_request: document-reference-search-request
          example_response: document-reference-search-response
---

<div id="document-reference-read-request">
{% tabs document-reference-read-request %}
{% tab document-reference-read-request python %}
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
{% tab document-reference-read-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/DocumentReference/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="document-reference-read-response">
{% tabs document-reference-read-response %}
{% tab document-reference-read-response 200 %}
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
                "url": "https://canvas-client-media.s3.amazonaws.com/training/invoices/f3d750f5d77d403c96baef6a6055c6e7_20211027_193132.pdf?AWSAccessKeyId=xxxx&Signature=xxxx&Expires=xxxx"
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
{% tab document-reference-read-response 401 %}
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
{% tab document-reference-read-response 403 %}
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
{% tab document-reference-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown DocumentReference resource '9b814d81-fb56-456b-a46d-c67fdaaec2ac'"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="documentreference-search-request">
{% include search-request.html resource_type="DocumentReference" search_string="subject=Patient%2Fcfd91cd3bd9046db81199aa8ee4afd7f&status=current&type=http%3A%2F%2Floinc.org%7C11502-2" %}
</div>

<div id="document-reference-search-response">
{% tabs document-reference-search-response %}
{% tab document-reference-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
        {
            "relation": "self",
            "url": "/DocumentReference?subject=Patient%2Fcfd91cd3bd9046db81199aa8ee4afd7f&status=current&type=http%3A%2F%2Floinc.org%7C11502-2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/DocumentReference?subject=Patient%2Fcfd91cd3bd9046db81199aa8ee4afd7f&status=current&type=http%3A%2F%2Floinc.org%7C11502-2&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/DocumentReference?subject=Patient%2Fcfd91cd3bd9046db81199aa8ee4afd7f&status=current&type=http%3A%2F%2Floinc.org%7C11502-2&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "DocumentReference",
                "id": "1cd418c3-3d7b-4b6e-a5d5-75efc9eae27e",
                "status": "current",
                "type":
                {
                    "coding":
                    [
                        {
                            "system": "http://loinc.org",
                            "code": "11502-2",
                            "display": "Laboratory report"
                        }
                    ]
                },
                "category":
                [
                    {
                        "coding":
                        [
                            {
                                "code": "labreport"
                            }
                        ]
                    }
                ],
                "subject":
                {
                    "reference": "Patient/cfd91cd3bd9046db81199aa8ee4afd7f",
                    "type": "Patient"
                },
                "date": "2023-09-18T00:00:00+00:00",
                "author":
                [
                    {
                        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                        "type": "Practitioner"
                    }
                ],
                "custodian":
                {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "content":
                [
                    {
                        "attachment":
                        {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/instance/documents/5-Hiaa_Plasma_WgIqY6E.pdf?AWSAccessKeyId=xxx&Signature=xxxx&Expires=xxxx"
                        },
                        "format":
                        {
                            "system": "http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem",
                            "code": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
                            "display": "mimeType Sufficient"
                        }
                    }
                ],
                "context":
                {
                    "encounter":
                    [
                        {
                            "reference": "Encounter/ca757171-c26c-4a83-ad02-d9d44024e01e",
                            "type": "Encounter"
                        }
                    ],
                    "period":
                    {
                        "start": "2023-09-18T23:38:43.252179+00:00"
                    }
                }
            }
        }
    ]
}
```
{% endtab %}
{% tab document-reference-search-response 400 %}
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
{% tab document-reference-search-response 401 %}
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
{% tab document-reference-search-response 403 %}
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
