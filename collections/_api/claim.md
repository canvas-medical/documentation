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
          - name: extension
            type: array[json]
            description: >-
              Canvas supports a single extension iteration on a claim.<br><br>
              By default, a claim is created in the **NeedsCodingReview** queue in Canvas.<br><br>Sending a different value in this extension creates or updates a claim to be in that queue.<br><br>The `url` must be **http://schemas.canvasmedical.com/fhir/extensions/claim-queue** and the `system` must be **http://canvasmedical.com**<br><br>
              
              **Supported claim queues**

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
          - name: status
            description: >-
              The status of the resource instance.<br><br>Supported codes for create interactions are: **active**
            type: string
            required_in: create,update
          - name: type
            description: >-
              The category of claim.<br><br>Supported codes for create interactions are: **professional** with a `system` of **http://terminology.hl7.org/CodeSystem/claim-type**
            type: json
            required_in: create,update
          - name: use
            description: >-
              A code to indicate the nature of the request<br><br>Supported codes for create interactions are: **claim**
            type: string
            required_in: create,update
          - name: patient
            description: >-
              The Canvas patient resource for the claim
            type: json
            required_in: create,update
          - name: created
            description: |-
              The date this resource was created.<br>
              Canvas will use this as the date of service for the claims in this message.<br><br>
              Expected format is : **YYYY-MM-DD**
            type: date
            required_in: create,update
          - name: provider
            description: >-
              The Canvas provider resource for the staff responsible for the claim.
            type: json
            required_in: create,update
          - name: priority
            description: >-
              The provider-required urgency of processing the request.<br><br>Supported codes for create interactions are: **normal** with a system of **http://terminology.hl7.org/CodeSystem/processpriority**
            type: json
            required_in: create,update
          - name: supportingInfo
            description: >-
              Additional information about the Claim<br><br>Canvas supports a single iteration for a reason for visit - the text in the `valueString` will be used.
            type: array[json]
          - name: diagnosis
            description: >-
              Information about diagnoses relevant to the claim items.<br><br>These diagnoses will create Assessments in Canvas.<br><br>The `sequence` should be unique within the Claim message, usually starting at 1 and incrementing as needed.<br><br>Must be a `diagnosisCodeableConcept`<br><br>Codes are supported from the following systems: **http://hl7.org/fhir/sid/icd-10-cm**
            type: array[json]
            required_in: create,update
          - name: insurance
            description: >-
              FHIR resource for the coverage(s) to use when adjudicating the claim<br><br>
              `sequence` should be unique for each insurance in the claim message.<br><br>
              `focal` indicates whether this insurance should be used to adjudicate the claim in this message. Canvas will ignore any elements that are False.<br><br>
              `coverage` is a Canvas coverage resource identifying the coverage for this iteration of insurance<br><br>Additional information on a Coverage can be obtained from the Coverage search endpoint
            type: array[json]
            required_in: create,update
          - name: item
            description: >-
              List of service charges to be used in the claim.<br><br>
              `sequence` should be unique for each item in the message.<br><br>
              `diagnosisSequence` should have one or more `sequence` values from the `diagnosis` section.<br><br>
              `productOrService` is an object that specifies the coding of the service. Canvas uses the first coding where system is **http://www.ama-assn.org/go/cpt**.<br><br>
              `modifier` specifies the list of charge modifier codings. Canvas accepts the first element where the coding's system is **https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets**. Canvas uses the 2 character modifiers from this CodeSet.<br><br>
            type: array[json]
            required_in: create,update
        search_parameters:
          - name: _id
            type: string
            description: The Canvas resource identifier of the Claim
          - name: patient
            type: string
            description: Patient receiving the products or services
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