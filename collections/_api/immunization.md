---
title: FHIR Immunization
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Immunization
        article: "a"
        description: >-
         Describes the event of a patient being administered a vaccine or a record of an immunization as reported by a patient, a clinician or another party.
        attributes:
          - name: id
            description: >-
              The identifier of the immunization
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: occurrenceDateTime
            description: >-
              The date and time the immunization was administered
            type: string
          - name: patient
            description: >-
              The patient who received the immunization
            type: string
          - name: primarySource
            description: >-
              Whether the immunization was administered by a primary source
            type: string
          - name: status
            description: >-
              The status of the immunization
            type: string
          - name: statusReason
            type: string
          - name: vaccineCode
            description: >-
              The vaccine administered
            type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            description: >-
              The patient who received the immunization
            type: string
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_response: immunization-read-response
          example_request: immunization-read-request
        search:
          responses: [200, 400]
          example_response: immunization-search-response
          example_request: immunization-search-request
---
<div id="immunization-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Immunization/<id>"

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
     --url https://fumage-example.canvasmedical.com/Immunization/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="immunization-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
{
    "resourceType": "Immunization",
    "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
    "status": "completed",
    "vaccineCode": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/cvx",
                "code": "207",
                "display": "Moderna Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) (coronavirus disease [COVID-19]) vaccine, mRNA-LNP, spike protein, preservative free, 50 mcg/0.25 mL dosage, for intramuscular use"
            }
        ]
    },
    "patient": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "occurrenceDateTime": "2021-12-01",
    "primarySource": false
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
                "text": "Unknown Immunization resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="immunization-search-request">
{% tabs search-request %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Immunization \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="immunization-search-response">
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
            "url": "/Immunization?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Immunization?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Immunization?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Immunization",
                "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
                "status": "completed",
                "vaccineCode": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "code": "207",
                            "display": "Moderna Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) (coronavirus disease [COVID-19]) vaccine, mRNA-LNP, spike protein, preservative free, 50 mcg/0.25 mL dosage, for intramuscular use"
                        }
                    ]
                },
                "patient": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "occurrenceDateTime": "2021-12-01",
                "primarySource": false
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

