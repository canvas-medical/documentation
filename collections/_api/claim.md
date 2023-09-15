---
title: Claim
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Claim
        article: "a"
        description: |-
          A provider issued list of professional services and products which have been provided, or are to be provided, to a patient which is sent to an insurer for reimbursement.<br><br>
          [http://hl7.org/fhir/R4/claim.html](http://hl7.org/fhir/R4/claim.html)
        attributes:
          - name: status
            description: >-
              The status of the resource instance.<br><br>Supported codes for create interactions are: **active**
            type: string
            required: true
          - name: type
            description: >-
              The category of claim.<br><br>Supported codes for create interactions are: **professional** with a `system` of **http://hl7.org/fhir/ValueSet/claim-type**
            type: json
            required: true
          - name: use
            description: >-
              A code to indicate the nature of the request<br><br>Supported codes for create interactions are: **claim**
            type: string
            required: true
          - name: patient
            description: >-
              The Canvas patient resource for the claim
            type: json
            required: true
          - name: created
            description: |-
              The date this resource was created.<br>
              Canvas will use this as the date of service for the claims in this message.<br><br>
              Expected format is : **YYYY-MM-DD**
            type: date
            required: true
          - name: provider
            description: >-
              The Canvas provider resource for the staff responsible for the claim.
            type: json
            required: true
          - name: priority
            description: >-
              The provider-required urgency of processing the request.<br><br>Supported codes for create interactions are: **normal** with a system of **http://hl7.org/fhir/ValueSet/process-priority**
            type: json
            required: true
          - name: supportingInfo
            description: >-
              Additional information about the Claim<br><br>Canvas supports a single iteration for a reason for visit - the text in the `valueString` will be used.
            type: array[json]
          - name: diagnosis
            description: >-
              Information about diagnoses relevant to the claim items.<br><br>These diagnoses will create Assessments in Canvas.<br><br>The `sequence` should be unique within the Claim message, usually starting at 1 and incrementing as needed.<br><br>Must be a `diagnosisCodeableConcept`<br><br>Codes are supported from the following systems: **http://hl7.org/fhir/ValueSet/icd-10**
            type: array[json]
            required: true
          - name: insurance
            description: >-
              FHIR resource for the coverage(s) to use when adjudicating the claim<br><br>
              `sequence` should be unique for each insurance in the claim message.<br><br>
              `focal` indicates whether this insurance should be used to adjudicate the claim in this message. We will ignore any elements that are False.<br><br>
              `coverage` is a Canvas coverage resource identifying the coverage for this iteration of insurance<br><br>Additional information on a Coverage can be obtained from the Coverage search endpoint
            type: array[json]
            required: true
          - name: item
            description: >-
              List of service charges to be used in the claim.<br><br>
              `sequence` should be unique for each item in the message.<br><br>
              `diagnosisSequence` should have one or more `sequence` values from the `diagnosis` section.<br><br>
              `productOrService` is an object that specifies the coding of the service. We use the first coding where system is **http://hl7.org/fhir/us/core/ValueSet/us-core-procedure-code**.<br><br>
              `modifier` specifies the list of charge modifier codings. Canvas accepts the first element where the coding's system is **http://hl7.org/fhir/us/carin-bb/ValueSet/AMACPTCMSHCPCSModifiers**. Canvas uses the 2 character modifiers from this ValueSet.<br><br>
            type: array[json]
            required: true
        endpoints: [create]
        create:
          description: Create a Claim resource.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: claim-create-request
          example_response: claim-create-response
          
---
<div id="claim-create-request">
  {% tabs claim-create-request %}
    {% tab claim-create-request curl %}
```shell
curl --request POST \
    --url 'https://fumage-example.canvasmedical.com/Claim' \
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
  "patient": {
    "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd",
    "type": "Patient"
  },
  "created": "2021-08-16",
  "provider": {
    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
    "type": "Practitioner"
  },
  "priority": {
    "coding": [
      {
        "code": "normal",
        "system": "http://hl7.org/fhir/ValueSet/process-priority"
      }
    ]
  },
  "supportingInfo": [
    {
      "sequence": 1,
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
        "reference": "Coverage/02d4f77a-ebaf-47d5-b162-6313244aed5f"
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
      "quantity": {
        "value": 1
      },
      "unitPrice": {
        "value": 75
      }
    }
  ]
}'
```
    {% endtab %}

    {% tab claim-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Claim"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}
payload = {
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
  "patient": {
    "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd",
    "type": "Patient"
  },
  "created": "2021-08-16",
  "provider": {
    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
    "type": "Practitioner"
  },
  "priority": {
    "coding": [
      {
        "code": "normal",
        "system": "http://hl7.org/fhir/ValueSet/process-priority"
      }
    ]
  },
  "supportingInfo": [
    {
      "sequence": 1,
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
      "focal": True,
      "coverage": {
        "reference": "Coverage/02d4f77a-ebaf-47d5-b162-6313244aed5f"
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
      "quantity": {
        "value": 1
      },
      "unitPrice": {
        "value": 75
      }
    }
  ]
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}
  {% endtabs %}
</div>

<div id="claim-create-response">
  {% tabs claim-create-response %}
    {% tab claim-create-response 201 %}
```json
null
```
    {% endtab %}
    {% tab claim-create-response 400 %}
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
    {% tab claim-create-response 401 %}
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
    {% tab claim-create-response 403 %}
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
    {% tab claim-create-response 405 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-supported",
      "details": {
        "text": "Operation is not supported"
      }
    }
  ]
}
```
    {% endtab %}
    {% tab claim-create-response 412 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "conflict",
      "details": {
        "text": "Resource updated since If-Unmodified-Since date"
      }
    }
  ]
}
```
    {% endtab %}
    {% tab claim-create-response 422 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "business-rule",
      "details": {
        "text": "Unprocessable entity"
      }
    }
  ]
}
```
    {% endtab %}
  {% endtabs %}
</div>