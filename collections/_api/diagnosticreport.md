---
title: DiagnosticReport
sections:
  - type: section
    blocks:
      - type: apidoc
        name: DiagnosticReport
        article: "a"
        description: >-
          Implantable diagnostic-reports
        attributes:
          - name: id
            type: string
            description: A Canvas-issued unique identifier
            required: true
          - name: resourceType
            type: string
            required: true
          - name: category
            type: string
          - name: code
            type: string
          - name: effectiveDateTime
            type: date
          - name: encounter
            type: string
          - name: issued
            type: date
          - name: performer
            type: string
          - name: presentedForm
            type: string
          - name: result
            type: string
          - name: status
            type: string
          - name: subject
            type: string
         search_parameters:
          - name: id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
            description: >-
              The patient
          - name: category
            type: string
          - name: code
            type: string
          - name: date
            type: date
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_response: diagnostic-report-read-response
          example_request: diagnostic-report-read-request
        search:
          responses: [200, 400]
          example_response: diagnostic-report-search-response
          example_request: diagnostic-report-search-request

---
<div id="diagnostic-report-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/DiagnosticReport/<id>"

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
     --url https://fumage-example.canvasmedical.com/DiagnosticReport/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="diagnostic-report-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
{
    "resourceType": "DiagnosticReport",
    "id": "9b90621b-059f-4f6e-9ef5-58171098e424",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "LP29684-5",
                    "display": "Radiology"
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://www.ama-assn.org/go/cpt",
                "code": "71010",
                "display": "XRAY, chest; single view, frontal"
            }
        ]
    },
    "subject": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "effectiveDateTime": "2023-01-01",
    "issued": "2023-01-31T15:23:46.900813+00:00",
    "performer": [
        {
            "reference": "Practitioner/883f7147517e444fb746cdac3860b0dc",
            "type": "Practitioner"
        }
    ],
    "presentedForm": [
        {
            "url": "https://canvas-client-media.s3.amazonaws.com/training/Test_-_Imaging_Report.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=IYUaecGWpgUzZ8FGgH7yUxFC2Ck%3D&Expires=1675179226"
        }
    ]
}
```
{% endtab %}
{% tab read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown DiagnosticReport resource 'abc'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="diagnostic-report-search-request">
{% tabs search-request %}
{% tab search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/DiagnosticReport"

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
     --url https://fumage-example.canvasmedical.com/DiagnosticReport \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="diagnostic-report-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/DiagnosticReport?patient=a1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/DiagnosticReport?patient=a1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/DiagnosticReport?patient=a1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "DiagnosticReport",
                "id": "9b90621b-059f-4f6e-9ef5-58171098e424",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "LP29684-5",
                                "display": "Radiology"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://www.ama-assn.org/go/cpt",
                            "code": "71010",
                            "display": "XRAY, chest; single view, frontal"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "effectiveDateTime": "2023-01-01",
                "issued": "2023-01-31T15:23:46.900813+00:00",
                "performer": [
                    {
                        "reference": "Practitioner/883f7147517e444fb746cdac3860b0dc",
                        "type": "Practitioner"
                    }
                ],
                "presentedForm": [
                    {
                        "url": "https://canvas-client-media.s3.amazonaws.com/training/Test_-_Imaging_Report.pdf?AWSAccessKeyId=AKIAQB7SIDR7EI2V32FZ&Signature=IYUaecGWpgUzZ8FGgH7yUxFC2Ck%3D&Expires=1675179226"
                    }
                ]
            }
        }
    ]
}
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