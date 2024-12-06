---
title: DiagnosticReport
sections:
  - type: section
    blocks:
      - type: apidoc
        name: DiagnosticReport
        article: "a"
        description: >-
          The findings and interpretation of diagnostic tests performed on patients, groups of patients, devices, and locations, and/or specimens derived from these. The report includes clinical context such as requesting and provider information, and some mix of atomic results, images, textual and coded interpretations, and formatted representation of diagnostic reports.
          <br><br>
          [https://hl7.org/fhir/R4/diagnosticreport.html](https://hl7.org/fhir/R4/diagnosticreport.html)<br><br>
          This endpoint implements the US Core DiagnosticReport Profile for Report. The following USCDI data elements are retrievable from this endpoint:<br><br>Clinical Notes:<br>- Imaging Narrative<br>- Laboratory Report Narrative<br>- Pathology Report Narrative<br>- Procedure Note<br><br>Laboratory:<br>- Tests<br>- Values/Results
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the Diagnostic Report.
            type: string
          - name: text
            description: Text summary of the Diagnostic Report, for human interpretation.
            type: json
            attributes:
              - name: status
                description: All reports returned from this endpoint will show a status of `generated`.
              - name: div
                description: Limited xhtml content that contains the human readable text of the Diagnostic Report.
          - name: identifier
            description: Business identifier for report.
            type: array[json]
            attributes:
                - name: id 
                  description: The identifier of the Diagnostic Report.
                  type: string
          - name: status
            type: enum [ final | entered-in-error ]
            description: >-
                Status of the Diagnostic Report see [https://hl7.org/fhir/R4/valueset-diagnostic-report-status.html](https://hl7.org/fhir/R4/valueset-diagnostic-report-status.html). Currently Canvas only supports two types of statuses. 
          - name: category
            type: array[json]
            description: Service category [https://hl7.org/fhir/R4/valueset-diagnostic-service-sections.html](https://hl7.org/fhir/R4/valueset-diagnostic-service-sections.html). Use this attribute to help distinguish the type of report in Canvas.
            attributes: 
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes: 
                  - name: system
                    description: >-
                      The system url of the coding.
                    enum_options: 
                      - value: http://terminology.hl7.org/CodeSystem/v2-0074
                      - value: http://loinc.org
                    type: string
                  - name: code
                    description: >-
                      The code of the category.
                    type: string
                    enum_options: 
                      - value: LAB
                      - value: LP29684-5
                      - value: LP7839-6
                      - value: LP29708-2
                  - name: display
                    description: >-
                      The display name of the coding.
                    type: string
                    enum_options: 
                      - value: Laboratory
                      - value: Radiology
                      - value: Cardiology
                      - value: Pathology
          - name: code
            type: json
            description: Name/Code for this diagnostic report.
            attributes: 
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes: 
                  - name: system
                    description: >-
                      The system url of the coding.
                    type: string
                  - name: code
                    description: >-
                      The code of the category.
                    type: string
                  - name: display
                    description: >-
                      The display name of the coding.
                    type: string
              - name: text
                type: string
                description: Plain text representation of the Lab or Imaging Report.
          - name: subject
            type: json
            description: The subject of the report.
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: encounter
            type: json
            description: >-
                Health care event when test ordered or reviewed. <br><br>
                Lab and Imaging Reports in Canvas will have an Encounter associated with the payload if there has been a Lab Results Review, Imaging Report Review, or a POC Lab Test command committed in a note on the patient's chart. 
            attributes:
              - name: reference
                type: string
                description: The reference string of the Encounter in the format of `"Encounter/912542cf-3bfb-4609-99f6-26ce94feb70d"`.
              - name: id
                type: string
                description: Unique identifier of the Encounter.
          - name: effectiveDateTime
            type: datetime | date
            description: Clinically relevant date/time for report.
          - name: issued
            type: datetime
            description: DateTime this version was made.
          - name: performer
            type: array[json]
            description: Responsible Diagnostic Service. In Canvas this will be the Practitioner who is assigned to the Report.
            attributes:
              - name: reference
                type: string
                description: The reference string of the practitioner in the format of `"Practitioner/4150cd20de8a470aa570a852859ac87e"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
          - name: result
            type: array[json]
            description: Observations associated with the Diagnostic Report.
            attributes:
              - name: reference
                type: string
                description: The reference string of the observation in the format of `"Observation/dcc3239b-ffc9-4d02-9cb6-a486bb9d406e"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Observation").
          - name: presentedForm
            type: array[json]
            description: >-
              Entire report as issued. There is also a [DocumentReference](/api/documentreference) resource specifically for this Report PDF being created. <br><br>
              **Note: There is a temporary extension that will contain the presigned URL for the Attachment; this will be provided while we migrate to static URLs that will require bearer authentication to retrieve attachment files. Use this extension for backward-compatible URLs until the migration is completed.**
            attributes:
                - name: url
                  type: string
                  description: Uri where the data can be found.
                - name: extension
                  type: json
                  description: Extension for backward-compatible URLs 
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier for a specific diagnostic report.
          - name: category
            type: string
            description: The DiagnosticReport category. Filters by the code and/or system  under `category.coding` attribute. You can search by just the code value or you can search by the system and code in the format `system|code`.
            search_options:
              - value: http://terminology.hl7.org/CodeSystem/v2-0074
              - value: http://loinc.org
          - name: code
            type: string
            description: The DiagnosticReport code. Filters by the code and/or system under `code.coding` attribute. You can search by just the code value or you can search by the system and code in the format `system|code`.
          - name: date
            type: date
            description: Filter by effectiveDateTime. See [Date Filtering](/api/date-filtering) for more information.
          - name: patient
            type: string
            description: The patient reference associated to the Diagnostic Report in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
        endpoints: [read, search]
        read:
          description: Read a DiagnosticReport resource
          responses: [200, 401, 403, 404]
          example_request: diagnosticreport-read-request
          example_response: diagnosticreport-read-response
        search:
          description: Search for DiagnosticReport resources
          responses: [200, 400, 401, 403]
          example_request: diagnosticreport-search-request
          example_response: diagnosticreport-search-response
---

<div id="diagnosticreport-read-request">
{% include read-request.html resource_type="DiagnosticReport" %}
</div>

<div id="diagnosticreport-read-response">
{% tabs diagnostic-report-read-response %}
{% tab diagnostic-report-read-response 200 %}
```json
{
    "resourceType": "DiagnosticReport",
    "id": "9b90621b-059f-4f6e-9ef5-58171098e424",
    "status": "final",
    "category":
    [
        {
            "coding":
            [
                {
                    "system": "http://loinc.org",
                    "code": "LP29684-5",
                    "display": "Radiology"
                }
            ]
        }
    ],
    "code":
    {
        "coding":
        [
            {
                "system": "http://www.ama-assn.org/go/cpt",
                "code": "73562",
                "display": "XRAY, knee; 3 views"
            }
        ]
    },
    "subject":
    {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "encounter":
    {
        "reference": "Encounter/6a077e6f-ead2-4af7-803d-0a203bedfb1c",
        "type": "Encounter"
    },
    "effectiveDateTime": "2023-08-22",
    "issued": "2023-08-22T21:35:01.909441+00:00",
    "performer":
    [
        {
            "reference": "Practitioner/883f7147517e444fb746cdac3860b0dc",
            "type": "Practitioner"
        }
    ],
    "presentedForm":
    [
        {
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/deprecated-url",
                    "valueUri": "https://canvas-client-media.s3.amazonaws.com/local/Screenshot_2024-02-21_at_15.26.42.pdf?AWSAccessKeyId=AKIAQB7SIDR7C2IYANB6&Signature=Ns%2BLQ5z5XXWH4WMOXWczuMQ7s0A%3D&Expires=1714138104"
                }
            ],
            "url": "http://schemas.canvasmedical.com/DiagnosticReport/resource_key/files/presentedForm"
        }
    ]
}
```
{% endtab %}
{% tab diagnostic-report-read-response 401 %}
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

{% tab diagnostic-report-read-response 403 %}
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

{% tab diagnostic-report-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown DiagnosticReport resource '9b814d81-fb56-456b-a46d-c67fdaaec2ac'"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="diagnosticreport-search-request">
{% include search-request.html resource_type="DiagnosticReport" search_string="patient=Patient/ca52f2b76011429d8a0e4aa2b56b18bc&code=73562&date=ge2023-09-12" %}
</div>

<div id="diagnosticreport-search-response">
{% tabs diagnostic-report-search-response %}
{% tab diagnostic-report-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link":
    [
        {
            "relation": "self",
            "url": "/DiagnosticReport?patient=Patient/ca52f2b76011429d8a0e4aa2b56b18bc&code=73562&date=ge2023-09-12&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/DiagnosticReport?patient=Patient/ca52f2b76011429d8a0e4aa2b56b18bc&code=73562&date=ge2023-09-12&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/DiagnosticReport?patient=Patient/ca52f2b76011429d8a0e4aa2b56b18bc&code=73562&date=ge2023-09-12&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "DiagnosticReport",
                "id": "197d1b7a-374e-4aa8-82b2-6960a62ecf7a",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                                "code": "LAB",
                                "display": "Laboratory"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "6690-2",
                            "display": "WBC"
                        },
                        {
                            "system": "http://loinc.org",
                            "code": "785-6",
                            "display": "MCH"
                        },
                        {
                            "system": "http://loinc.org",
                            "code": "5905-5",
                            "display": "Monocytes"
                        }
                    ],
                    "text": "Complete Blood Count (Cbc) With Differential"
                },
                "subject": {
                    "reference": "Patient/ca52f2b76011429d8a0e4aa2b56b18bc",
                    "type": "Patient"
                },
                "effectiveDateTime": "2022-04-01T07:00:00+00:00",
                "issued": "2022-04-15T15:24:22.522951+00:00",
                "performer": [
                    {
                        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                        "type": "Practitioner"
                    }
                ],
                "result": [
                    {
                        "reference": "Observation/422f9f0f-151a-4488-bcad-ab4b0c3967da",
                        "type": "Observation"
                    }
                ],
                "presentedForm": [
                    {
                        "extension": [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/deprecated-url",
                                "valueUri": "https://canvas-client-media.s3.amazonaws.com/local/Screenshot_2024-02-21_at_15.26.42.pdf?AWSAccessKeyId=AKIAQB7SIDR7C2IYANB6&Signature=Ns%2BLQ5z5XXWH4WMOXWczuMQ7s0A%3D&Expires=1714138104"
                            }
                        ],
                        "url": "http://schemas.canvasmedical.com/DiagnosticReport/resource_key/files/presentedForm"
                    }
                ]
            }
        },
        {
            "resource":
            {
                "resourceType": "DiagnosticReport",
                "id": "9b814d81-fb56-456b-a46d-c67fdaaec2ad",
                "status": "final",
                "category":
                [
                    {
                        "coding":
                        [
                            {
                                "system": "http://loinc.org",
                                "code": "LP29684-5",
                                "display": "Radiology"
                            }
                        ]
                    }
                ],
                "code":
                {
                    "coding":
                    [
                        {
                            "system": "http://www.ama-assn.org/go/cpt",
                            "code": "73562",
                            "display": "XRAY, knee; 3 views"
                        }
                    ]
                },
                "subject":
                {
                    "reference": "Patient/ca52f2b76011429d8a0e4aa2b56b18bc",
                    "type": "Patient"
                },
                "effectiveDateTime": "2023-09-15",
                "issued": "2023-09-15T19:52:56.711871+00:00",
                "performer":
                [
                    {
                        "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e",
                        "type": "Practitioner"
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab diagnostic-report-search-response 400 %}
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
{% tab diagnostic-report-search-response 401 %}
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
{% tab diagnostic-report-search-response 403 %}
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
