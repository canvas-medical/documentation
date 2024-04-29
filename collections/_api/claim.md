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
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the Claim.
            required_in: update
            exclude_in: create
            type: string
          - name: extension
            type: array[json]
            description_for_all_endpoints: >-
              Canvas supports a single extension iteration on a claim to represent the current queue the given claim is in on the Canvas instance. Learn more about navigating claim queues [here](https://canvas-medical.zendesk.com/hc/en-us/articles/1500000932761-Navigating-the-Queues-in-Revenue).<br><br>

              **Canvas Claim Queues**

                | display     | code                   |
                | :-----------| :----------------------|
                | Adjudicated | AdjudicatedOpenBalance |
                | Appointment | Appointment            |
                | Clinician   | NeedsClinicianReview   |
                | Coding      | NeedsCodingReview      |
                | Filed       | FiledAwaitingResponse  |
                | History     | ZeroBalance            |
                | Patient     | PatientBalance         |
                | Rejected    | RejectedNeedsReview    |
                | Submission  | QueuedForSubmission    | 
                | Trash       | Trash                  |
            create_and_update_description: >-
              By default, a claim is created in the **NeedsCodingReview** queue in Canvas.<br>Sending a different value in this extension updates the claim to be in that queue.
            attributes:
              - name: url
                type: string
                required_in: create,update
                description: Reference that defines the content of this object.
                enum_options:
                  - value: http://schemas.canvasmedical.com/fhir/extensions/claim-queue
              - name: valueCoding
                type: json
                required_in: create,update
                description: Value of extension.
                attributes: 
                  - name: system
                    required_in: create,update
                    description: The system url of the coding.
                    enum_options: 
                      - value: http://canvasmedical.com
                    type: string
                  - name: code
                    required_in: create,update
                    description: 
                    type: string
                    enum_options:
                      - value: NeedsClinicianReview
                      - value: NeedsCodingReview
                      - value: QueuedForSubmission
                      - value: FiledAwaitingResponse
                      - value: RejectedNeedsReview
                      - value: AdjudicatedOpenBalance
                      - value: PatientBalance
                      - value: ZeroBalance
                      - value: Trash
                      - value: Appointment
                  - name: display
                    description: The display name of the coding.
                    type: string
                    enum_options:
                      - value: Adjudicated
                      - value: Appointment
                      - value: Clinician
                      - value: Coding
                      - value: Filed
                      - value: History
                      - value: Patient
                      - value: Rejected
                      - value: Submission
                      - value: Trash
          - name: status
            description: The status of the resource instance.
            type: enum [ active ]
            required_in: create,update
          - name: type
            description: The category of claim.
            type: json
            required_in: create,update
            attributes:
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                required_in: create,update
                attributes: 
                  - name: system
                    required_in: create,update
                    description: The system url of the coding.
                    enum_options: 
                      - value: http://terminology.hl7.org/CodeSystem/claim-type
                      - value: http://hl7.org/fhir/ValueSet/claim-type
                    type: string
                  - name: code
                    required_in: create,update
                    description: The code.
                    type: string
                    enum_options: 
                      - value: professional
                  - name: display
                    description: The display name of the coding.
                    type: string
                    enum_options: 
                      - value: Professional
          - name: use
            description: A code to indicate the nature of the request.
            type: enum [ claim ]
            required_in: create,update
          - name: patient
            description: >-
              The Canvas patient resource for the claim.
            type: json
            required_in: create,update
            attributes:
              - name: reference
                type: string
                required_in: create,update
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: created
            description: |-
              The date this resource was created.<br>
              This maps to the date of service for note in Canvas the claims is associated with.
            type: date [ YYYY-MM-DD ]
            required_in: create,update
          - name: provider
            description: Party responsible for the claim. This will be a reference to a Practitioner.
            type: json
            required_in: create,update
            attributes:
              - name: reference
                type: string
                required_in: create,update
                description: The reference string of the subject in the format of `"Practitioner/bb24f084e1fa46c7931663259540266d"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
          - name: priority
            description: The provider-required urgency of processing the request.
            type: json
            required_in: create,update
            attributes:
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                required_in: create,update
                attributes: 
                  - name: system
                    required_in: create,update
                    description: The system url of the coding.
                    enum_options: 
                      - value: http://hl7.org/fhir/ValueSet/process-priority
                      - value: http://terminology.hl7.org/CodeSystem/processpriority
                    type: string
                  - name: code
                    required_in: create,update
                    description: The code.
                    type: string
                    enum_options: 
                      - value: normal
                  - name: display
                    description: The display name of the coding.
                    type: string
                    enum_options: 
                      - value: Normal
          - name: supportingInfo
            description: >-
              Additional information about the Claim.<br><br>Canvas supports a single iteration for a reason for visit - the text in the `valueString` will be the note's RFV the claim is associated with.
            type: array[json]
            attributes:
              - name: sequence
                type: positive integer
                description: Information instance identifier. Most likely will be `1` since Canvas currently only accepts one SupportingInfo object.
                required_in: create, update
              - name: category
                type: json
                required_in: create, update
                description: Classification of the supplied information.
                attributes: 
                  - name: system
                    required_in: create,update
                    description: The system url of the coding.
                    enum_options: 
                      - value: http://hl7.org/fhir/ValueSet/claim-informationcategory
                      - value: http://terminology.hl7.org/CodeSystem/claiminformationcategory
                    type: string
                  - name: code
                    required_in: create,update
                    description: The code.
                    type: string
                    enum_options: 
                      - value: patientreasonforvisit
                  - name: display
                    description: The display name of the coding.
                    type: string
                    enum_options: 
                      - value: Patient Reason for Visit
              - name: valueString
                type: string
                description: Data to be provided.<br><br>Canvas supports free text to be passed as the reason for visit associated with the claim.
          - name: diagnosis
            description_for_all_endpoints: >-
              Information about diagnoses relevant to the claim items.
            create_and_update_description: These diagnoses will create Assessments in Canvas. At least one diagnosis element is required. 
            type: array[json]
            required_in: create,update
            attributes:
              - name: sequence
                required_in: create,update
                type: positive integer
                description: Diagnosis instance identifier.<br><br>The `sequence` should be unique within the Claim message, usually starting at 1 and incrementing as needed.
              - name: diagnosisCodeableConcept
                description: Nature of illness or problem.
                type: array[json]
                required_in: create,update
                attributes: 
                  - name: system
                    required_in: create,update
                    description: The system url of the coding.
                    enum_options: 
                      - value: http://hl7.org/fhir/ValueSet/icd-10
                      - value: http://hl7.org/fhir/sid/icd-10-cm
                    type: string
                  - name: code
                    required_in: create,update
                    description: The ICD10 code. Canvas will automatically add the `.` when displaying in the UI (e.g the code 'H9190' is for the ICD10 H91.90 for unspecified hearing loss in an unspecified ear)
                    type: string
                  - name: display
                    description: The display name of the coding.
                    type: string
          - name: insurance
            description_for_all_endpoints: >-
              Patient insurance information. Contains the list of coverage's associated with the claim in Canvas.
            create_and_update_description: >-
              If the claim should be a self paying claim, pass the insurance list as 
              
              ```
                "insurance": [
                    {
                        "sequence": 1,
                        "focal": false,
                        "coverage": {
                            "display": "No Coverage"
                        }
                    }
                ]
              ```
            type: array[json]
            required_in: create,update
            attributes:
              - name: focal
                type: boolean
                required_in: create,update
                description_for_all_endpoints: Coverage to be used for adjudication. 
                read_and_search_description: Only insurance objects with `focal` as True will be returned in a Search/Read. 
                create_and_update_description: Canvas will ignore any elements that are set to False. 
              - name: sequence
                required_in: create,update
                type: positive integer
                description: Insurance instance identifier.<br><br>The `sequence` should be unique within the Claim message, usually starting at 1 and incrementing as needed.
              - name: coverage
                required_in: create, update
                type: json
                description: Insurance Information
                attributes: 
                  - name: reference
                    type: string
                    description: The reference string of the coverage in the format of `"Coverage/05274c93-341c-4d23-9e46-718f6743609f"`.
                  - name: display
                    type: string
                    enum_options:
                      - value: "No Coverage"
                    description: A display of `"No Coverage"` are for claims that are self pay.
          - name: item
            description: >-
              List of service charges to be used in the claim.
            type: array[json]
            required_in: create,update
            attributes:
              - name: sequence
                required_in: create,update
                type: positive integer
                description: Item instance identifier.<br><br>The `sequence` should be unique within the Claim message, usually starting at 1 and incrementing as needed.
              - name: diagnosisSequence
                type: array[positive integer]
                required_in: create, update
                description: Applicable diagnoses. This list of integers corresponds one or more diagnoses in the `Claim.diagnosis` list that this service charge is associated with. 
              - name: productOrService
                type: json
                required_in: create, update
                description: Billing, service, product, or drug code.
                attributes:
                  - name: coding
                    description: Identifies where the definition of the code comes from.
                    type: array[json]
                    required_in: create,update
                    attributes: 
                      - name: system
                        required_in: create,update
                        description: The system url of the coding.
                        enum_options: 
                          - value: http://hl7.org/fhir/us/core/ValueSet/us-core-procedure-code
                          - value: http://www.ama-assn.org/go/cpt
                        type: string
                      - name: code
                        required_in: create,update
                        description: The code.
                        type: string
                      - name: display
                        required_in: create,update
                        description: The display name of the coding.
                        type: string
              - name: quantity
                type: json
                required_in: create, update
                description: Count of products or services.
                attributes:
                 - name: value
                   type: integer
                   description:  Numerical value.
              - name: unitPrice
                type: json
                required_in: create, update
                description: Fee, charge or cost per item.
                attributes:
                 - name: value
                   type: integer
                   description:  Numerical value (with implicit precision)
              - name: modifier
                type: array[json]
                description: Product or service billing modifiers. 
                attributes:
                  - name: coding
                    description: Identifies where the definition of the code comes from.
                    type: array[json]
                    required_in: create,update
                    attributes: 
                      - name: system
                        required_in: create,update
                        description: The system url of the coding.
                        enum_options: 
                          - value: hhttp://hl7.org/fhir/us/carin-bb/ValueSet/AMACPTCMSHCPCSModifiers
                          - value: https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets
                        type: string
                      - name: code
                        required_in: create,update
                        description: The code.
                        type: string
                      - name: display
                        required_in: create,update
                        description: The display name of the coding.
                        type: string
        search_parameters:
          - name: _id
            type: string
            description: The Canvas resource identifier of the Claim
          - name: patient
            description: The patient reference associated to the Claim in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
        endpoints: [create, read, update, search]
        create:
          description: Create a Claim resource.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: claim-create-request
          example_response: claim-create-response
        read:
          description: Read a Claim resource.
          responses: [200, 401, 403, 404]
          example_request: claim-read-request
          example_response: claim-read-response
        update:
          description: >-
           Update a Claim resource.<br><br>**The only Claim update supported by Canvas is to change an existing Claim's queue. Changes to other fields will be ignored, but required fields must still be valued.**
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: claim-update-request
          example_response: claim-update-response
        search:
          description: Search for Claim resources.
          responses: [200, 400, 401, 403]
          example_request: claim-search-request
          example_response: claim-search-response
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
  "extension": [
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/claim-queue",
      "valueCoding": {
          "system": "http://canvasmedical.com",
          "code": "NeedsClinicianReview",
          "display": "Clinician"
      }
    }
  ],
  "status": "active",
  "type": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/claim-type",
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
        "system": "http://terminology.hl7.org/CodeSystem/processpriority"
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
            "system": "http://terminology.hl7.org/CodeSystem/claiminformationcategory",
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
            "system": "http://hl7.org/fhir/sid/icd-10-cm",
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
            "system": "http://www.ama-assn.org/go/cpt",
            "code": "exam",
            "display": "Office visit"
          }
        ]
      },
      "modifier": [
        {
          "coding": [
            {
              "system": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
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
  "extension": [
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/claim-queue",
      "valueCoding": {
          "system": "http://canvasmedical.com",
          "code": "NeedsClinicianReview",
          "display": "Clinician"
      }
    }
  ],
  "status": "active",
  "type": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/claim-type",
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
        "system": "http://terminology.hl7.org/CodeSystem/processpriority"
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
            "system": "http://terminology.hl7.org/CodeSystem/claiminformationcategory",
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
            "system": "http://hl7.org/fhir/sid/icd-10-cm",
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
            "system": "http://www.ama-assn.org/go/cpt",
            "code": "exam",
            "display": "Office visit"
          }
        ]
      },
      "modifier": [
        {
          "coding": [
            {
              "system": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
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
{% include create-response.html %}
</div>

<div id="claim-read-request">
{% include read-request.html resource_type="Claim" %}
</div>

<div id="claim-read-response">
{% tabs claim-read-response %}

{% tab claim-read-response 200 %}
```json
{
    "resourceType": "Claim",
    "id": "e4df0a15-d98c-400e-ad46-54eeb13f2753",
    "extension": [
      {
        "url": "http://schemas.canvasmedical.com/fhir/extensions/claim-queue",
        "valueCoding": {
            "system": "http://canvasmedical.com",
            "code": "NeedsClinicianReview",
            "display": "Clinician"
        }
      }
    ],
    "status": "active",
    "type": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/claim-type",
                "code": "professional"
            }
        ]
    },
    "use": "claim",
    "patient": {
        "reference": "Patient/4dc9d97b71924de58b54a9a91a8250dd",
        "type": "Patient"
    },
    "created": "2023-11-16",
    "provider": {
        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
        "type": "Practitioner"
    },
    "priority": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/processpriority",
                "code": "normal"
            }
        ]
    },
    "diagnosis": [
        {
            "sequence": 1,
            "diagnosisCodeableConcept": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/sid/icd-10-cm",
                        "code": "J940",
                        "display": "Chylous effusion"
                    }
                ]
            }
        },
        {
            "sequence": 2,
            "diagnosisCodeableConcept": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/sid/icd-10-cm",
                        "code": "L639",
                        "display": "Alopecia areata, unspecified"
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
                "reference": "Coverage/39f37e33-bb0b-4e6b-88ca-56ea94629974",
                "type": "Coverage"
            }
        }
    ],
    "item": [
        {
            "sequence": 1,
            "diagnosisSequence": [
                1,
                2
            ],
            "productOrService": {
                "coding": [
                    {
                        "system": "http://www.ama-assn.org/go/cpt",
                        "code": "99211",
                        "display": "Office outpatient visit 5 minutes"
                    }
                ]
            },
            "quantity": {
                "value": 1
            },
            "unitPrice": {
                "value": 50.0
            },
            "net": {
                "value": 50.0
            }
        },
        {
            "sequence": 2,
            "diagnosisSequence": [
                1
            ],
            "productOrService": {
                "coding": [
                    {
                        "system": "http://www.ama-assn.org/go/cpt",
                        "code": "77012",
                        "display": "Ct guidance needle placement"
                    }
                ]
            },
            "quantity": {
                "value": 1
            },
            "unitPrice": {
                "value": 200.0
            },
            "net": {
                "value": 200.0
            }
        }
    ]
}
```
{% endtab %}

{% tab claim-read-response 401 %}
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

{% tab claim-read-response 403 %}
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

{% tab claim-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Claim resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
{% endtab %}

{% endtabs %}

</div>

<div id="claim-update-request">

  {% tabs claim-update-request %}

    {% tab claim-update-request curl %}
```shell
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/Claim/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Claim",
  "extension": [
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/claim-queue",
      "valueCoding": {
          "system": "http://canvasmedical.com",
          "code": "AdjudicatedOpenBalance",
          "display": "Adjudicated"
      }
    }
  ],
  "status": "active",
  "type": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/claim-type",
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
        "system": "http://terminology.hl7.org/CodeSystem/processpriority"
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
            "system": "http://terminology.hl7.org/CodeSystem/claiminformationcategory",
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
            "system": "http://hl7.org/fhir/sid/icd-10-cm",
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
            "system": "http://www.ama-assn.org/go/cpt",
            "code": "exam",
            "display": "Office visit"
          }
        ]
      },
      "modifier": [
        {
          "coding": [
            {
              "system": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
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

    {% tab claim-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Claim/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
  "resourceType": "Claim",
  "extension": [
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/claim-queue",
      "valueCoding": {
          "system": "http://canvasmedical.com",
          "code": "AdjudicatedOpenBalance",
          "display": "Adjudicated"
      }
    }
  ],
  "status": "active",
  "type": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/claim-type",
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
        "system": "http://terminology.hl7.org/CodeSystem/processpriority"
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
            "system": "http://terminology.hl7.org/CodeSystem/claiminformationcategory",
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
            "system": "http://hl7.org/fhir/sid/icd-10-cm",
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
            "system": "http://www.ama-assn.org/go/cpt",
            "code": "exam",
            "display": "Office visit"
          }
        ]
      },
      "modifier": [
        {
          "coding": [
            {
              "system": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
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
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="claim-update-response">
{% include update-response.html resource_type="Claim" %}
</div>

<div id="claim-search-request">
{% include search-request.html resource_type="Claim" search_string="patient=Patient/4dc9d97b71924de58b54a9a91a8250dd" %}
</div>

<div id="claim-search-response">
{% tabs claim-search-response %}
{% tab claim-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Claim?patient=4dc9d97b71924de58b54a9a91a8250dd&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Claim?patient=4dc9d97b71924de58b54a9a91a8250dd&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Claim?patient=4dc9d97b71924de58b54a9a91a8250dd&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Claim",
                "id": "e4df0a15-d98c-400e-ad46-54eeb13f2753",
                "extension": [
                  {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/claim-queue",
                    "valueCoding": {
                        "system": "http://canvasmedical.com",
                        "code": "AdjudicatedOpenBalance",
                        "display": "Adjudicated"
                    }
                  }
                ],
                "status": "active",
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/claim-type",
                            "code": "professional"
                        }
                    ]
                },
                "use": "claim",
                "patient": {
                    "reference": "Patient/4dc9d97b71924de58b54a9a91a8250dd",
                    "type": "Patient"
                },
                "created": "2023-11-16",
                "provider": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                },
                "priority": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/processpriority",
                            "code": "normal"
                        }
                    ]
                },
                "diagnosis": [
                    {
                        "sequence": 1,
                        "diagnosisCodeableConcept": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/sid/icd-10-cm",
                                    "code": "J940",
                                    "display": "Chylous effusion"
                                }
                            ]
                        }
                    },
                    {
                        "sequence": 2,
                        "diagnosisCodeableConcept": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/sid/icd-10-cm",
                                    "code": "L639",
                                    "display": "Alopecia areata, unspecified"
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
                            "reference": "Coverage/39f37e33-bb0b-4e6b-88ca-56ea94629974",
                            "type": "Coverage"
                        }
                    }
                ],
                "item": [
                    {
                        "sequence": 1,
                        "diagnosisSequence": [
                            1,
                            2
                        ],
                        "productOrService": {
                            "coding": [
                                {
                                    "system": "http://www.ama-assn.org/go/cpt",
                                    "code": "99211",
                                    "display": "Office outpatient visit 5 minutes"
                                }
                            ]
                        },
                        "quantity": {
                            "value": 1
                        },
                        "unitPrice": {
                            "value": 50.0
                        },
                        "net": {
                            "value": 50.0
                        }
                    },
                    {
                        "sequence": 2,
                        "diagnosisSequence": [
                            1
                        ],
                        "productOrService": {
                            "coding": [
                                {
                                    "system": "http://www.ama-assn.org/go/cpt",
                                    "code": "77012",
                                    "display": "Ct guidance needle placement"
                                }
                            ]
                        },
                        "quantity": {
                            "value": 1
                        },
                        "unitPrice": {
                            "value": 200.0
                        },
                        "net": {
                            "value": 200.0
                        }
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab claim-search-response 401 %}
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

    {% tab claim-search-response 403 %}
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