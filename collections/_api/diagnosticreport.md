---
title: DiagnosticReport
sections:
  - type: section
    blocks:
      - type: apidoc
        name: DiagnosticReport
        article: "a"
        description: >-
          The findings and interpretation of diagnostic tests performed on patients, groups of patients, devices, and locations, and/or specimens derived from these. The report includes clinical context such as requesting and provider information, and some mix of atomic results, images, textual and coded interpretations, and formatted representation of diagnostic reports. [https://hl7.org/fhir/R4/diagnosticreport.html](https://hl7.org/fhir/R4/diagnosticreport.html)<br><br>
          This endpoint implements the US Core DiagnosticReport Profile for Report. The following USCDI data elements are retrievable from this endpoint:<br><br>Clinical Notes:<br>- Imaging Narrative<br>- Laboratory Report Narrative<br>- Pathology Report Narrative<br>- Procedure Note<br><br>Laboratory:<br>- Tests<br>- Values/Results
        attributes:
          - name: id
            type: string
            description: A Canvas-issued unique identifier
            required: true
          - name: status
            type: string
            description: DiagnosticReportStatus [https://hl7.org/fhir/R4/valueset-diagnostic-report-status.html](https://hl7.org/fhir/R4/valueset-diagnostic-report-status.html)
          - name: category
            type: array[json]
            description: Service category [https://hl7.org/fhir/R4/valueset-diagnostic-service-sections.html](https://hl7.org/fhir/R4/valueset-diagnostic-service-sections.html)
          - name: code
            type: json
            description: Name/Code for this diagnostic report
          - name: subject
            type: json
            description: The subject of the report - usually, but not always, the patient
          - name: encounter
            type: json
            description: Health care event when test ordered
          - name: effectiveDateTime
            type: datetime | date
            description: Clinically relevant date/time for report
          - name: issued
            type: datetime
            description: 	DateTime this version was made
          - name: performer
            type: array[json]
            description: Responsible Diagnostic Service
          - name: result
            type: array[json]
            description: Observations
          - name: presentedForm
            type: array[json]
            description: Entire report as issued
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: category
            type: string
            description: The DiagnosticReport category. Filters by the code value under category.coding.
          - name: code
            type: string
            description: The DiagnosticReport code. Filters by the code value under code.coding.
          - name: date
            type: date
            description: Filter by date
          - name: patient
            type: string
            description: The patient associated with the report
        endpoints: [read, search]
        read:
          description: Read a DiagnosticReport resource
          responses: [200, 401, 403, 404]
          example_request: diagnostic-report-read-request
          example_response: diagnostic-report-read-response
        search:
          description: Search for DiagnosticReport resources
          responses: [200, 400, 401, 403]
          example_request: diagnostic-report-search-request
          example_response: diagnostic-report-search-response
---

<div id="diagnostic-report-read-request">
{% include read-request.html resource_type="DiagnosticReport" %}
</div>

<div id="diagnostic-report-read-response">
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
            "url": "https://canvas-client-media.s3.amazonaws.com/instance/Imaging_Report.pdf?AWSAccessKeyId=xxxx&Signature=xxxx&Expires=1675179226"
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


<div id="diagnostic-report-search-request">
{% tabs diagnostic-report-search-request %}
{% tab diagnostic-report-search-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/DiagnosticReport?patient=Patient%2Fca52f2b76011429d8a0e4aa2b56b18bc&code=73562&date=ge2023-09-12"

headers = {
  "accept": "application/json",
  "Authorization": "Bearer "
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab diagnostic-report-search-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/DiagnosticReport?patient=Patient%2Fca52f2b76011429d8a0e4aa2b56b18bc&code=73562&date=ge2023-09-12' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="diagnostic-report-search-response">
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
            "url": "/DiagnosticReport?patient=Patient%2Fca52f2b76011429d8a0e4aa2b56b18bc&code=73562&date=ge2023-09-12&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/DiagnosticReport?patient=Patient%2Fca52f2b76011429d8a0e4aa2b56b18bc&code=73562&date=ge2023-09-12&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/DiagnosticReport?patient=Patient%2Fca52f2b76011429d8a0e4aa2b56b18bc&code=73562&date=ge2023-09-12&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "DiagnosticReport",
                "id": "822a7292-7489-4f0d-8432-4715bc060ce7",
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
                        },
                        {
                            "system": "http://snomed.info/sct",
                            "code": "281296001",
                            "display": "Comment"
                        },
                        {
                            "system": "http://snomed.info/sct",
                            "code": "282290005",
                            "display": "Interpretation"
                        }
                    ]
                },
                "subject":
                {
                    "reference": "Patient/ca52f2b76011429d8a0e4aa2b56b18bc",
                    "type": "Patient"
                },
                "effectiveDateTime": "2023-09-15",
                "issued": "2023-09-15T19:46:15.747800+00:00",
                "performer":
                [
                    {
                        "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e",
                        "type": "Practitioner"
                    }
                ],
                "presentedForm":
                [
                    {
                        "url": "https://canvas-client-media.s3.amazonaws.com/local/PDF_VLHGufm.pdf?AWSAccessKeyId=xxxx&Signature=xxxx&Expires=1694807775"
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
                ],
                "presentedForm":
                [
                    {
                        "url": "https://canvas-client-media.s3.amazonaws.com/local/PDF_kS8w1sl.pdf?AWSAccessKeyId=xxxx&Signature=xxxx&Expires=1694808176"
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
