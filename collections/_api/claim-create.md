---
title: Claim
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Claim
        article: "a"
        description: >-
          A provider issued list of professional services and products which have been provided, or are to be provided, to a patient which is sent to an insurer for reimbursement.
        attributes:
          - name: integration_type
            type: string
            required: true
          - name: integration_source
            type: string
            required: true
          - name: patient_identifier
            type: string
            required: true
            attributes:
              - name: identifier_type
                type: string
                required: true
              - name: identifier
                type: string
                required: true
          - name: integration_payload
            type: json
            required: true
            attributes:
              - name: created
                type: string
              - name: provider_identifier
                attributes:
                  - name: identifier_type
                    type: string
                    required: true
                  - name: identifier
                    type: string
                    required: true
              - name: originator_identifier
                type: string
                attributes:
                  - name: identifier_type
                    type: string
                    required: true
                  - name: identifier
                    type: string
                    required: true
              - name: charges
                type: json
              - name: diagnosis
                type: json
              - name: coverages
                type: json
              - name: reason_for_visit
                type: string
        endpoints: create
        create:
          example_request: claim-create-request
          example_response: claim-create-response
          responses: [201, 400]
---
<div id="claim-create-request">
{% tabs create-request %}
{% tab create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Claim"

payload = {
    "resourceType": "Claim",
    "status": "active",
    "type": { "coding": [
            {
                "system": "http://hl7.org/fhir/ValueSet/claim-type",
                "code": "professional"
            }
        ] },
    "use": "claim",
    "patient": "Patient/865058f6654149bd921264d91519af9e",
    "created": "2021-08-16",
    "provider": {
        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
        "type": "http://canvasmedical.com"
    },
    "supportingInfo": [
        {
            "sequence": 0,
            "category": { "coding": [
                    {
                        "code": "patientreasonforvisit",
                        "system": "http://hl7.org/fhir/ValueSet/claim-informationcategory",
                        "display": "Patient Reason for Visit"
                    }
                ] },
            "valueString": "This is only...a test"
        }
    ],
    "diagnosis": [
        {
            "sequence": 1,
            "diagnosisCodeableConcept": { "coding": [
                    {
                        "code": "F41.1",
                        "system": "http://hl7.org/fhir/ValueSet/icd-10",
                        "display": "Generalized anxiety"
                    }
                ] }
        }
    ],
    "insurance": [
        {
            "sequence": 1,
            "focal": True,
            "coverage": { "reference": "Coverage/7afeaa26-48e1-43c2-b414-fd8aa9780af1" }
        }
    ],
    "item": [
        {
            "sequence": 1,
            "diagnosisSequence": [1],
            "productOrService": { "coding": [
                    {
                        "system": "http://hl7.org/fhir/us/core/ValueSet/us-core-procedure-code",
                        "code": "exam",
                        "display": "Office visit"
                    }
                ] },
            "modifier": [{ "coding": [
                        {
                            "system": "http://hl7.org/fhir/us/carin-bb/ValueSet/AMACPTCMSHCPCSModifiers",
                            "code": "21"
                        }
                    ] }],
            "quantity": 1,
            "unitPrice": { "value": 75 }
        }
    ]
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
{% tab create-request curl %}
```sh
curl --request POST \
     --url https://fumage-example.canvasmedical.com/Claim \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Claim",
  "status": "active",
  "type": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/ValueSet/claim-type",
        "code": "professional"
      }
    ]
  },
  "use": "claim",
  "patient": "Patient/865058f6654149bd921264d91519af9e",
  "created": "2021-08-16",
  "provider": {
    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
    "type": "http://canvasmedical.com"
  },
  "supportingInfo": [
    {
      "sequence": 0,
      "category": {
        "coding": [
          {
            "code": "patientreasonforvisit",
            "system": "http://hl7.org/fhir/ValueSet/claim-informationcategory",
            "display": "Patient Reason for Visit"
          }
        ]
      },
      "valueString": "This is only...a test"
    }
  ],
  "diagnosis": [
    {
      "sequence": 1,
      "diagnosisCodeableConcept": {
        "coding": [
          {
            "code": "F41.1",
            "system": "http://hl7.org/fhir/ValueSet/icd-10",
            "display": "Generalized anxiety"
          }
        ]
      }
    }
  ],
  "insurance": [
    {
      "sequence": 1,
      "focal": true,
      "coverage": {
        "reference": "Coverage/7afeaa26-48e1-43c2-b414-fd8aa9780af1"
      }
    }
  ],
  "item": [
    {
      "sequence": 1,
      "diagnosisSequence": [
        1
      ],
      "productOrService": {
        "coding": [
          {
            "system": "http://hl7.org/fhir/us/core/ValueSet/us-core-procedure-code",
            "code": "exam",
            "display": "Office visit"
          }
        ]
      },
      "modifier": [
        {
          "coding": [
            {
              "system": "http://hl7.org/fhir/us/carin-bb/ValueSet/AMACPTCMSHCPCSModifiers",
              "code": "21"
            }
          ]
        }
      ],
      "quantity": 1,
      "unitPrice": {
        "value": 75
      }
    }
  ]
}
'

```
{% endtab %}
{% endtabs %}
</div>

<div id="claim-create-response">
{% tabs create-response %}
{% tab create-response 201 %}
```json
null
```
{% endtab %}
{% tab create-response 400 %}
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

