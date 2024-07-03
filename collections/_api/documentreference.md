---
title: DocumentReference
sections:
  - type: section
    blocks:
      - type: apidoc
        name: DocumentReference
        article: "a"
        description: >-
          A reference to a document of any kind for any purpose. Provides metadata about the document so that the document can be discovered and managed. The scope of a document is any seralized object with a mime-type, so includes formal patient centric documents (CDA), clinical notes, scanned paper, and non-patient specific documents like policy text.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-documentreference.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-documentreference.html)<br><br>
          A Document Reference can represent many different PDFs generated in Canvas:
          

          - A [Letter](https://canvas-medical.zendesk.com/hc/en-us/articles/360057339634-Letters) that has been faxed or printed from the patient's chart.
          
          - All documents uploaded via [Data Integration](https://canvas-medical.zendesk.com/hc/en-us/articles/360056078034-Data-Integration-Overview) and linked to a Patient. This includes Lab Reports, Imaging Reports, Referral Reports, Clinical, and Administrative Documents.
          
          - [POC Lab Command's](https://canvas-medical.zendesk.com/hc/en-us/articles/360055629214-Point-of-Care-POC-Tests) committed on the Patient's chart
          
          - [Clinical Notes](https://canvas-medical.zendesk.com/hc/en-us/articles/360057949073-Printing-a-Chart-Note) representing a PDF of each locked note. This also includes superseded versions on notes.
          
          - Any [Educational Material](https://canvas-medical.zendesk.com/hc/en-us/articles/4999882305939-Educational-Material-Command) committed on a patient's chart.
          
          - Any [Invoices](https://canvas-medical.zendesk.com/hc/en-us/articles/4406239284499-Statements-and-Invoicing) generated for a patient.
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
            exclude_in: create
          - name: id
            description: The identifier of the document reference.
            type: string
          - name: identifier
            type: array[json]
            description: Other identifiers for the document.
            attributes:
              - name: system
                type: string
                description:  The namespace for the identifier value.
                enum_options: 
                  - value: http://schemas.canvasmedical.com/fhir/document-reference-identifier
              - name: value
                type: string
                description: The identifier value that is unique.
          - name: extension
            type: array[json]
            description_for_all_endpoints: Specific FHIR extensions on this resource are supported to be able to map some Canvas specific attributes for a comment, clinical date, review mode, reviewer, priority, and if it requires a signature. 
            create_and_update_description: In order to identify which extension maps to specific fields in Canvas, the url field is used as an exact string match.
            attributes:
              - name: url
                type: string
                required_in: create
                description: Identifies the meaning of the extension
                enum_options:
                  - value: http://schemas.canvasmedical.com/fhir/document-reference-comment
                  - value: http://schemas.canvasmedical.com/fhir/document-reference-clinical-date
                  - value: http://schemas.canvasmedical.com/fhir/document-reference-review-mode
                  - value: http://schemas.canvasmedical.com/fhir/document-reference-reviewer
                  - value: http://schemas.canvasmedical.com/fhir/document-reference-priority
                  - value: http://schemas.canvasmedical.com/fhir/document-reference-requires-signature
              - name: valueString
                type: string
                description: Value of extensions for Comment and Review Mode.<br><br> The `valueString` attribute is needed for the Comment's extension where the `url` is `http://schemas.canvasmedical.com/fhir/document-reference-comment` and for the Review Mode extension where the `url` is `http://schemas.canvasmedical.com/fhir/document-reference-review-mode`. <br><br> Comment is a comment on the underlying Canvas document that is related to this DocumentReference resource, while the Review Mode is also a field on the underlying Canvas document record which determines the review mode values (`RR` for Review Required, `AR` for Already Reviewed and `RN` for Review Not Required).
              - name: valueDate
                type: date
                description: Value of extension.<br><br> The `valueDate` attribute is needed for the Clinical Date extension where the `url` is `http://schemas.canvasmedical.com/fhir/document-reference-clinical-date`. This attribute determines the Clinical Date on the underlying document record related to this DocumentReference resource. It's the `original_date` field on the related Canvas document record. Expected date value format for this field is `YYYY-MM-DD`.
                required_in: create
              - name: valueReference
                type: json
                required_in: create
                description: Value of extension.<br><br> The `valueReference` attribute is needed for expressing the Reviewer of the document where the `url` is `http://schemas.canvasmedical.com/fhir/document-reference-reviewer`. This attribute will be the reference to the Practitioner (Canvas Staff) that's assigned as the reviewer of this document.
                attributes:
                  - name: reference
                    type: string
                    required_in: create
                    description: The reference string of the Practitioner in the format of `"Practitioner/95b9ac2d-e963-4d7a-b165-7901870f1663"`.
                  - name: type
                    type: string
                    required_in: create
                    description: Type the reference refers to (e.g. "Practitioner").
              - name: valueBoolean
                type: string
                description: Value of extensions for Priority and Requires Signature.<br><br> The `valueBoolean` attribute is needed for the Priority extension where the `url` is `http://schemas.canvasmedical.com/fhir/document-reference-priority` and for the Requires Signature where the `url` is `http://schemas.canvasmedical.com/fhir/document-reference-requires-signature`. <br><br> Priority is a field on the underlying Canvas document that is related to this DocumentReference resource and determines if the document should be prioritized, while Requires Signature is also a field on the underlying Canva document that determines where the related document requires Practitioner's signature.
          - name: status
            description: >-
              The status of the document reference. <br><br>

              - Letters and POC Lab Reports will always have a status of `current`.
              
              - Documents uploaded in Data Integration will have a status of `current` when created. If a document is removed from the patient's chart, it will have a status of `entered-in-error`.
              
              - For Clinical Note documents, the status will be `current` if it is the latest PDF of the locked note. If it is an older version due to a practitioner unlocking/ammending the note, the status will be `superseded`. If the note is deleted on the patient's chart, the status will be `entered-in-error`.

              - For Educational Material, the status will be `current` if the command is committed. If the command was entered-in-error in the chart, the status will also be `entered-in-error`.

              - For Invoices, the status will be `current` if it is a latest version or an adhoc invoice. The status will be `entered-in-error` if there was a problem generating or sending out the invoice to the patient. The status will be `superseded` if an automated invoice gets archived as it is older than the invoice interval defined Constance Config in Settings.
            type: enum [ current | superseded | entered-in-error]
          - name: type
            description: A coding for the type of document.
            type: json
            required_in: create
            attributes:
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                required_in: create
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    enum_options: 
                      - value: http://loinc.org
                    type: string
                    required_in: create
                  - name: code
                    description: The code value.
                    type: string
                    required_in: create
                    enum_options: 
                      - value: codes supported in Data Integration (see link at top of page).
                      - value: 51852-2 (Letters)
                      - value: 34895-3 (Educational Material)
                      - value: 94093-2 (Invoices/Itemized Bill)
                  - name: display
                    description: >-
                      The display name of the coding.
                    type: string
                    exclude_in: create
              - name: text
                type: string
                description: Plain text representation of the type of document.
                exclude_in: create
          - name: category
            type: array[json]
            required_in: create
            description: The categorization of the document.
            attributes:
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                required_in: create
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    enum_options: 
                      - value: http://schemas.canvasmedical.com/fhir/document-reference-category
                    type: string
                    required_in: create
                  - name: code
                    description: The code value.
                    type: string
                    required_in: create
                    enum_options: 
                      - value: clinical-note
                        exclude_in: create
                      - value: correspondence
                        exclude_in: create
                      - value: educationalmaterial
                        exclude_in: create
                      - value: imagingreport
                        exclude_in: create
                      - value: invoicefull
                        exclude_in: create
                      - value: labreport
                        exclude_in: create
                      - value: patientadministrativedocument
                      - value: referralreport
                        exclude_in: create
                      - value: uncategorizedclinicaldocument
            type: array[json]
          - name: subject
            description: Who/what is the subject of the document.
            type: json
            required_in: create
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: date
            description: When this document reference was created.
            type: date
            exclude_in: create
          - name: author
            description: >-
              Who and/or what authored the document. 

              - For letters, it is the practitioner who signed the letter determined by the practitioner dropdown in the UI when creating the letter.

              - For Lab Reports the author will be the practitioner who linked the report to the patient in Data Integration or if it the report has been reviewed, it will be the practitioner who committed a Lab Review. If the lab report that came through Health Gorilla was automtically linked to a Patient, there will be no author. 

              - For POC Lab Reports, the author will be the practitioner who committed the command in the patient's chart.

              - For Clinical and Administrative submitted through Data Integration, the author will be the practitioner who linked the doc to the patient in Data Integration.

              - For Educational Material docs, the author will be the practitioner who originated the command on the patient's chart

              - For Invoices, the author will either be the practitioner who asked for the invoice when invoice was created adhoc or it will be Canvas Bot if the invoice was automtically generated.

              - There are no authors on Imaging Reports or Clinical Notes.
            type: array[json]
            attributes:
              - name: reference
                type: string
                description: The reference string of the author in the format of `"Practitioner/0e46396e-9cbc-48c6-94cc-f75f08b66c80"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
          - name: custodian
            description: >-
              Organization which maintains the document.
            type: json
            exclude_in: create
            attributes:
              - name: reference
                type: string
                description: The reference string of the custodian in the format of `"Organization/00000000-0000-0000-0002-000000000000"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Organization").
          - name: description
            type: string
            required_in: create
            description_for_all_endpoints: The title of the underlying Canvas Document related to this DocumentReference resource. 
            create_and_update_description: It requires standard Document titles that must be matched to the Document provided in the coding type attribute.
          - name: content
            type: array[json]
            required_in: create
            description: Document referenced
            attributes:
              - name: attachment
                description: Where to access the document
                type: json
                required_in: create
                attributes: 
                  - name: contentType
                    description: Mime type of the content, with charset etc.
                    type: string
                    required_in: create
                    exclude_in: create
                  - name: url
                    description: URI where the data can be found. Please note that urls may have an AWSAccessKeyId and an Expires attribute. By default documents stored in AWS S3 will expire 10 minutes after the response payload is returned.
                    exclude_in: create
                    type: string
                  - name: data
                    type: string
                    required_in: create
                    description: Base64 encoded document file as a string.
                    exclude_in: read, search
              - name: format
                type: json
                description: Format/content rules for the document
                exclude_in: create
                attributes:
                  - name: system
                    description: The system url of the coding.
                    enum_options: 
                      - value: http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem
                    type: string
                  - name: code
                    description: The code value.
                    type: string
                    enum_options: 
                      - value: urn:ihe:iti:xds:2017:mimeTypeSufficient
                  - name: display
                    description: >-
                      The display name of the coding.
                    type: string
                    enum_options:
                      - value: mimeType Sufficient
          - name: context
            type: json
            exclude_in: create
            description: >-
              Clinical context of document. <br><br>

              - For clinical note documents, the context will contain information about the encounter associated with the note if applicable.

              - For POC Lab Reports or Educational Material documents, the context will contain information about the encounter of the note the commands were committed with if applicable. 

              - For Lab Reports that have a Lab Review committed in a note, the context will have information about any encounter associated with that note.
            attributes: 
              - name: encounter
                type: array[json]
                description: Context of the document content
                attributes: 
                  - name: reference
                    type: string
                    description: The reference string of the encounter in the format of `"Encounter/879b35fd-3bc2-4ccd-98d7-954dd9b6d0a9"`.
                  - name: type
                    type: string
                    description: Type the reference refers to (e.g. "Encounter").
              - name: period
                type: json
                description: Time of service that is being documented
                attributes: 
                  - name: start
                    type: datetime
                    description: Starting time with inclusive boundary of the encounter
                  - name: end
                    type: datetime
                    description: End time with inclusive boundary, if not ongoing of the encounter
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: category
            type: string
            description: >-
              Categorization of document. Filters by the code and/or system under `category.coding` attribute. You can search by just the code value or you can search by the system and code in the format `system|code` (e.g  `http://schemas.canvasmedical.com/fhir/document-reference-category|labreport`).
          - name: date
            type: date
            description: Filter by the date the document was created. See [Date Filtering](/api/date-filtering) for more information.
          - name: patient
            type: string
            description: The patient reference associated to the document in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
          - name: status
            type: string
            description: The status of the document reference
            create_description: The "status" field is required by FHIR to indicate the current state of the document. This ensures consistent and accurate document tracking across Canvas healthcare systems.
            enum_options: 
              - value: current
              - value: superseded
                exclude_in: create
              - value: entered-in-error
                exclude_in: create
            search_options: 
              - value: current
              - value: superseded
              - value: entered-in-error
            create_description: 
          - name: subject
            description: The patient reference associated to the document in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`. Can be used interchangeably with the patient parameter.
            type: string
          - name: type
            type: string
            description: Kind of document (LOINC if possible). Filters by the code and/or system under `type.coding` attribute. You can search by just the code value or you can search by the system and code in the format `system|code` (e.g `http://loinc.org|11502-2`).
        endpoints: [create, read, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: documentreference-create-request
          example_response: documentreference-create-response
          description: Create DocumentReference with provided fields and values.
        read:
          responses: [200, 401, 403, 404]
          example_request: documentreference-read-request
          example_response: documentreference-read-response
          description: Read DocumentReference resource.
        search:
          responses: [200, 400, 401, 403]
          example_request: documentreference-search-request
          example_response: documentreference-search-response
          description: Search for DocumentReference resources.
---

<div id="documentreference-create-request">

  {% tabs documentreference-create-request %}

    {% tab documentreference-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/DocumentReference' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
  {
    "resourceType": "DocumentReference",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
            "valueString": "Some comment on Document"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
            "valueDate": "2024-04-01"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
            "valueString": "RN"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
            "valueReference": {
                "reference": "Practitioner/5843991a8c934118ab4f424c839b340f",
                "type": "Practitioner"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-priority",
            "valueBoolean": true
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-requires-signature",
            "valueBoolean": true
        }
    ],
    "status": "current",
    "type": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "34105-7"
            }
        ]
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                    "code": "uncategorizedclinicaldocument"
                }
            ]
        }
    ],
    "subject": {
        "reference": "Patient/aabcf98215eb4356ad773a0ec9cd3369",
        "type": "Patient"
    },
    "author": [
        {
            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
            "type": "Practitioner"
        }
    ],
    "description": "Hospital Discharge Summary",
    "content": [
        {
            "attachment": {
                "contentType": "application/pdf",
                "data": "JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
            }
        }
    ]
  }
}'
```
    {% endtab %}
    {% tab documentreference-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/DocumentReference"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json",
}

payload = {
    "resourceType": "DocumentReference",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
            "valueString": "Some comment on Document",
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
            "valueDate": "2024-04-01",
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
            "valueString": "RN",
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
            "valueReference": {
                "reference": "Practitioner/5843991a8c934118ab4f424c839b340f",
                "type": "Practitioner",
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-priority",
            "valueBoolean": true,
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-requires-signature",
            "valueBoolean": true,
        }
    ],
    "status": "current",
    "type": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "34105-7",
            }
        ]
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                    "code": "uncategorizedclinicaldocument",
                }
            ]
        }
    ],
    "subject": {
        "reference": "Patient/aabcf98215eb4356ad773a0ec9cd3369",
        "type": "Patient",
    },
    "author": [
        {
            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
            "type": "Practitioner",
        }
    ],
    "description": "Hospital Discharge Summary",
    "content": [
        {
            "attachment": {
                "contentType": "application/pdf",
                "data": "JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G",
            }
        }
    ]
}
```
    {% endtab %}

  {% endtabs %}
</div>

<div id="documentreference-create-response">
{% include create-response.html %}
</div>

<div id="documentreference-read-request">
{% include read-request.html resource_type="DocumentReference" %}
</div>

<div id="documentreference-read-response">
{% tabs document-reference-read-response %}
{% tab document-reference-read-response 200 %}
```json
{
    "resourceType": "DocumentReference",
    "id": "6f60ed1c-a6b3-4791-99f0-f618704e33d1",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
            "valueString": "Some comment on Document"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
            "valueDate": "2024-04-01"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
            "valueString": "RN"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
            "valueReference": {
                "reference": "Practitioner/5843991a8c934118ab4f424c839b340f",
                "type": "Practitioner"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-priority",
            "valueBoolean": true
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/document-reference-requires-signature",
            "valueBoolean": true
        }
    ],
    "status": "current",
    "type": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "34105-7",
                "display": "Hospital Discharge summary"
            }
        ]
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                    "code": "uncategorizedclinicaldocument"
                }
            ]
        }
    ],
    "subject": {
        "reference": "Patient/aabcf98215eb4356ad773a0ec9cd3369",
        "type": "Patient"
    },
    "date": "2024-04-22T00:00:00+00:00",
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
    "description": "Hospital Discharge Summary",
    "content": [
        {
            "attachment": {
                "contentType": "application/pdf",
                "url": "https://canvas-client-media.s3.amazonaws.com/training/invoices//Hospital_Discharge_Summary_2024-04-22_18-27-45_7aeadd4496b34f86a78c26223cdabbf4_YQiesv8.pdf?AWSAccessKeyId=xxxx&Signature=xxxx&Expires=xxxx"
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
{% include search-request.html resource_type="DocumentReference" search_string="subject=Patient/cfd91cd3bd9046db81199aa8ee4afd7f&status=current&type=http://loinc.org|11502-2" %}
</div>

<div id="documentreference-search-response">
{% tabs document-reference-search-response %}
{% tab document-reference-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 12,
    "link": [
        {
            "relation": "self",
            "url": "/DocumentReference?patient=Patient/c0df2c04a0e64b46ba7fe3f836068e49&_count=50&_offset=0"
        },
        {
            "relation": "first",
            "url": "/DocumentReference?patient=Patient/c0df2c04a0e64b46ba7fe3f836068e49&_count=50&_offset=0"
        },
        {
            "relation": "last",
            "url": "/DocumentReference?patient=Patient/c0df2c04a0e64b46ba7fe3f836068e49&_count=50&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "DocumentReference",
                "id": "4b640065-ae64-4775-b5a8-8264314cf5fc",
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "94093-2",
                            "display": "Itemized bill"
                        }
                    ],
                    "text": "Itemized bill"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "invoicefull"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-24T00:00:00+00:00",
                "author": [
                    {
                        "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
                        "type": "Practitioner"
                    }
                ],
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "description": "Itemized bill",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/invoices/c0df2c04a0e64b46ba7fe3f836068e49_20240224_124702.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=WtfvJWbBgc50VgekeqrUDTPsyHk%3D&Expires=1709072108"
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
                "id": "5a0cf7ae-bd88-4f04-bd7e-60a33e5e2824",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
                        "valueString": "Some comment on LabReport Document"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
                        "valueDate": "2024-04-02"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
                        "valueString": "AR"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
                        "valueReference": {
                            "reference": "Practitioner/5843991a8c934118ab4f424c839b340f",
                            "type": "Practitioner"
                        }
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-requires-signature",
                        "valueBoolean": true
                    }
                ],
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "11502-2",
                            "display": "Laboratory report"
                        }
                    ],
                    "text": "Laboratory report"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "labreport"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-04-22T00:00:00+00:00",
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
                "description": "Lab Report",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/dummy_BLseNPP.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=uBuEZpbxcCg4w9hZ6hAXLJxMGe8%3D&Expires=1709072108"
                        },
                        "format": {
                            "system": "http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem",
                            "code": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
                            "display": "mimeType Sufficient"
                        }
                    }
                ],
                "context": {
                    "encounter": [
                        {
                            "reference": "Encounter/879b35fd-3bc2-4ccd-98d7-954dd9b6d0a9",
                            "type": "Encounter"
                        }
                    ],
                    "period": {
                        "start": "2024-02-22T23:10:12.409838+00:00"
                    }
                }
            }
        },
        {
            "resource": {
                "resourceType": "DocumentReference",
                "id": "b9f82cd0-6644-4b3f-a9d1-7585c3e71498",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
                        "valueString": "Some comment on ImagingReport Document"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
                        "valueDate": "2024-04-03"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
                        "valueString": "RN"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
                        "valueReference": {
                            "reference": "Practitioner/5843991a8c934118ab4f424c839b340f",
                            "type": "Practitioner"
                        }
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-requires-signature",
                        "valueBoolean": true
                    }
                ],
                "status": "entered-in-error",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "18748-4",
                            "display": "Diagnostic imaging study"
                        }
                    ],
                    "text": "Diagnostic imaging study"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "imagingreport"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-04-21T00:00:00+00:00",
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "description": "Imaging Report",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/document_annotations/blob_FeMcbYv?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=7V8KwSeZlPCCJiiarAHK55IW4pI%3D&Expires=1709072108"
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
        {
            "resource": {
                "resourceType": "DocumentReference",
                "id": "51a49fef-eb67-4b8d-a992-b3dd9e754dea",
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "51852-2",
                            "display": "Letter"
                        }
                    ],
                    "text": "Letter"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "correspondence"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-21T00:00:00+00:00",
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
                "description": "Letter",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/generic_documents/letter_494.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=K4d67C%2FNj9PtLIjY9by5qLwYiK4%3D&Expires=1709072108"
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
                "id": "713394da-f250-4c59-8b47-96458155f687",
                "status": "entered-in-error",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "clinical-note"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-22T00:00:00+00:00",
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/note_history/training_note_state_document_232604_1708628478?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=yangPOcYiWvr48s6VhvQIBSw0fs%3D&Expires=1709072108"
                        },
                        "format": {
                            "system": "http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem",
                            "code": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
                            "display": "mimeType Sufficient"
                        }
                    }
                ],
                "description": "Lab visit",
                "context": {
                    "encounter": [
                        {
                            "reference": "Encounter/aaefb326-8601-4c03-84d4-d6151b3a96bf",
                            "type": "Encounter"
                        }
                    ],
                    "period": {
                        "start": "2024-02-21T21:52:42.777590+00:00",
                        "end": "2024-02-22T19:37:10.850120+00:00"
                    }
                }
            }
        },
        {
            "resource": {
                "resourceType": "DocumentReference",
                "id": "6ebf590d-ff90-412e-a5e7-9be30d6e4c35",
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "11488-4",
                            "display": "Consult note"
                        }
                    ],
                    "text": "Consult note"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "referralreport"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-22T00:00:00+00:00",
                "author": [
                    {
                        "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
                        "type": "Practitioner"
                    }
                ],
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "description": "Consultancy Report",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/dummy_BLseNPP.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=uBuEZpbxcCg4w9hZ6hAXLJxMGe8%3D&Expires=1709072108"
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
                "id": "d9a1304d-159d-4518-be88-3f9a1ea93cd1",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
                        "valueString": "Disability form comment"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
                        "valueDate": "2023-12-12"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
                        "valueString": "RN"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
                        "valueReference": {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner"
                        }
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-priority",
                        "valueBoolean": false
                    }
                ],
                "status": "current",
                "type": {
                    "text": "Disability Form"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "patientadministrativedocument"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-22T00:00:00+00:00",
                "author": [
                    {
                        "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
                        "type": "Practitioner"
                    }
                ],
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "description": "Disability Form",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/dummy_BLseNPP.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=uBuEZpbxcCg4w9hZ6hAXLJxMGe8%3D&Expires=1709072108"
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
                "id": "bce56cc4-268a-4562-a699-16e8869415ad",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
                        "valueString": "Hospital discharge summary comment"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
                        "valueDate": "2024-01-14"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
                        "valueString": "AR"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
                        "valueReference": {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner"
                        }
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-priority",
                        "valueBoolean": true
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-requires-signature",
                        "valueBoolean": false
                    }
                ],
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "34105-7",
                            "display": "Hospital Discharge summary"
                        }
                    ],
                    "text": "Hospital Discharge summary"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "uncategorizedclinicaldocument"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-22T00:00:00+00:00",
                "author": [
                    {
                        "reference": "Practitioner/fdb06c59cecd43d095884222fcd93717",
                        "type": "Practitioner"
                    }
                ],
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "description": "Hospital Discharge Summary",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/dummy_BLseNPP.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=uBuEZpbxcCg4w9hZ6hAXLJxMGe8%3D&Expires=1709072108"
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
                "id": "d220fa24-2b2f-44cf-9843-5a1b681f0805",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
                        "valueString": "Advance beneficiary comment"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
                        "valueDate": "2024-02-13"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
                        "valueString": "RN"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
                        "valueReference": {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner"
                        }
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-priority",
                        "valueBoolean": true
                    }
                ],
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "53243-2",
                            "display": "Advanced beneficiary notice"
                        }
                    ],
                    "text": "Advanced beneficiary notice"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "patientadministrativedocument"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-22T00:00:00+00:00",
                "author": [
                    {
                        "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
                        "type": "Practitioner"
                    }
                ],
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "description": "Advanced Beneficiary Notice",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/dummy_BLseNPP.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=uBuEZpbxcCg4w9hZ6hAXLJxMGe8%3D&Expires=1709072108"
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
                "id": "04a71b54-89b0-49bf-96be-60b5bdfa6450",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
                        "valueString": "Handicap Parking Permit comment"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
                        "valueDate": "2024-04-01"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
                        "valueString": "RN"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
                        "valueReference": {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner"
                        }
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-priority",
                        "valueBoolean": true
                    }
                ],
                "status": "current",
                "type": {
                    "text": "Handicap Parking Permit"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "patientadministrativedocument"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-22T00:00:00+00:00",
                "author": [
                    {
                        "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
                        "type": "Practitioner"
                    }
                ],
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "description": "Handicap Parking Permit",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/dummy_BLseNPP.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=uBuEZpbxcCg4w9hZ6hAXLJxMGe8%3D&Expires=1709072108"
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
                "id": "efe6c0d6-97c0-42a6-91ba-926a2dc3c66f",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-comment",
                        "valueString": "Disability form comment"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-clinical-date",
                        "valueDate": "2024-01-15"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-review-mode",
                        "valueString": "RN"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-reviewer",
                        "valueReference": {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner"
                        }
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/document-reference-priority",
                        "valueBoolean": false
                    }
                ],
                "status": "current",
                "type": {
                    "text": "Disability Form"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "patientadministrativedocument"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-22T00:00:00+00:00",
                "author": [
                    {
                        "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
                        "type": "Practitioner"
                    }
                ],
                "custodian": {
                    "reference": "Organization/00000000-0000-0000-0002-000000000000",
                    "type": "Organization"
                },
                "description": "Disability Form",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/dummy_BLseNPP.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=uBuEZpbxcCg4w9hZ6hAXLJxMGe8%3D&Expires=1709072108"
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
                "id": "380ad499-ec8f-4f1f-b1f0-5f25b04fd574",
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "34895-3",
                            "display": "Education note"
                        }
                    ],
                    "text": "Education note"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/document-reference-category",
                                "code": "educationalmaterial"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/c0df2c04a0e64b46ba7fe3f836068e49",
                    "type": "Patient"
                },
                "date": "2024-02-22T00:00:00+00:00",
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
                "description": "Making a birth plan",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "url": "https://canvas-client-media.s3.amazonaws.com/training/generic_documents/Glaucoma_Screening_lFimBWS.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=2IfdGPA%2FOMFdRf3p75oYhY6QJ%2Bs%3D&Expires=1709072109"
                        },
                        "format": {
                            "system": "http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem",
                            "code": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
                            "display": "mimeType Sufficient"
                        }
                    }
                ],
                "context": {
                    "encounter": [
                        {
                            "reference": "Encounter/879b35fd-3bc2-4ccd-98d7-954dd9b6d0a9",
                            "type": "Encounter"
                        }
                    ],
                    "period": {
                        "start": "2024-02-22T23:10:12.409838+00:00"
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
