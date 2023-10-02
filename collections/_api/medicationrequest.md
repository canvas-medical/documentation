---
title: MedicationRequest
sections:
  - type: section
    blocks:
      - type: apidoc
        name: MedicationRequest
        article: "a"
        description: >-
          An order or request for both supply of the medication and the instructions for administration of the medication to a patient. The resource is called "MedicationRequest" rather than "MedicationPrescription" or "MedicationOrder" to generalize the use across inpatient and outpatient settings, including care plans, etc., and to harmonize with workflow patterns.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-medicationrequest.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-medicationrequest.html)<br><br>
          FHIR MedicationRequests maps to the [Prescribe](https://canvas-medical.zendesk.com/hc/en-us/articles/360063523313-Prescribing-a-Medication) and [Refill](https://canvas-medical.zendesk.com/hc/en-us/articles/360057482354-Refill-Medications) commands in Canvas. Any adjustments made with the [Adjust Prescription](https://canvas-medical.zendesk.com/hc/en-us/articles/360061706154-Adjust-an-Existing-Medication) command will appear in MedicationRequest API responses.
        attributes:
          - name: id
            description: The identifier of the MedicationRequest
            type: string
          - name: status
            description: A code specifying the current state of the order. Generally, this will be active or completed state
            type: string
          - name: intent
            description: Whether the request is a proposal, plan, or an original order
            type: string
          - name: reportedBoolean
            description: Indicates if this record was captured as a secondary 'reported' record rather than as an original primary source-of-truth record
            type: boolean
          - name: medicationCodeableConcept
            description: Identifies the medication being requested. This is simply an attribute carrying a code that identifies the medication from a known list of medications.
            type: json
          - name: subject
            description: Who or group medication request is for
            type: json
          - name: encounter
            description: Encounter created as part of encounter/admission/stay
            type: json
          - name: authoredOn
            description: When request was initially authored
            type: datetime
          - name: requester
            description: Who/What requested the Request
            type: json
          - name: performer [deprecated]
            description: >-
              Intended performer of administration<br><br>
              This attribute is deprecated and will be removed in a future release. It currently (and incorrectly) contains information about the dispenser of the medication. Canvas recommends disregarding this attribute. Information about the dispenser can be obtained from the `performer` attribute under `dispenseRequest`.
            type: json
          - name: reasonCode
            description: Reason or indication for ordering or not ordering the medication
            type: array[json]
          - name: note
            description: Information about the prescription
            type: array[json]
          - name: dosageInstruction
            description: How the medication should be taken
            type: array[json]
          - name: dispenseRequest
            description: Medication supply authorization
            type: json
          - name: substitution
            description: Any restrictions on medication substitution
            type: json
        search_parameters:
          - name: _id
            description: The identifier of the MedicationRequest
            type: string
          - name: intent
            description: >-
              Returns prescriptions with different intents<br><br>Supported codes for search interactions: **order**, **filler-order**
            type: string
          - name: patient
            description: Returns prescriptions for a specific patient	
            type: string
          - name: status
            description: >-
              Status of the prescription<br><br>Supported codes for search interactions: **active**, **cancelled**, **entered-in-error**, **stopped** 
            type: string
        endpoints: [read, search]
        read:
          description: Read a MedicationRequest resource.
          responses: [200, 401, 403, 404]
          example_request: medicationrequest-read-request
          example_response: medicationrequest-read-response
        search:
          description: Search for MedicationRequest resources.
          responses: [200, 400, 401, 403]
          example_request: medicationrequest-search-request
          example_response: medicationrequest-search-response
---

<div id="medicationrequest-read-request">
{%  include read-request.html resource_type="MedicationRequest" %}
</div>

<div id="medicationrequest-read-response">

  {% tabs medicationrequest-read-response %}

    {% tab medicationrequest-read-response 200 %}
```json
{
    "resourceType": "MedicationRequest",
    "id": "3423a69c-618d-4cbe-861a-54c60f48744e",
    "status": "active",
    "intent": "order",
    "reportedBoolean": false,
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "244899",
                "display": "lisinopril 10 mg tablet"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "314076",
                "display": "lisinopril 10 mg tablet"
            }
        ]
    },
    "subject": {
        "reference": "Patient/6cb2a409334943c2b48f1686dc739f11",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/bdadce18-098b-40dc-8bdd-ef8481bd999a",
        "type": "Encounter"
    },
    "authoredOn": "2023-09-21T18:19:36.106449+00:00",
    "requester": {
        "reference": "Practitioner/6c20b7152cf7421791c5ab4113060b3f",
        "type": "Practitioner"
    },
    "reasonCode": [
        {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/sid/icd-10-cm",
                    "code": "I10",
                    "display": "Essential (primary) hypertension"
                }
            ]
        }
    ],
    "dosageInstruction": [
        {
            "text": "take 1 daily",
            "doseAndRate": [
                {
                    "doseQuantity": {
                        "unit": "Tablet"
                    }
                }
            ]
        }
    ],
    "dispenseRequest": {
        "numberOfRepeatsAllowed": 3,
        "quantity": {
            "value": 30.0
        },
        "expectedSupplyDuration": {
            "value": 30,
            "unit": "days"
        },
        "performer": {
            "display": "Name: CVS Health #68534|NCPDP ID: 0068534|Address: 1 Cvs Dr, Woonsocket, RI, 028956146|Phone: 4017702500|Fax: 4017704486"
        }
    },
    "substitution": {
        "allowedBoolean": true
    }
}
```
    {% endtab %}

    {% tab medicationrequest-read-response 401 %}
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

    {% tab medicationrequest-read-response 403 %}
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

    {% tab medicationrequest-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown MedicationRequest resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="medicationrequest-search-request">
{% include search-request.html resource_type="MedicationRequest" search_string="patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="medicationrequest-search-response">

  {% tabs medicationrequest-search-response %}

    {% tab medicationrequest-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/MedicationRequest?patient=Patient%2F6cb2a409334943c2b48f1686dc739f11&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/MedicationRequest?patient=Patient%2F6cb2a409334943c2b48f1686dc739f11&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/MedicationRequest?patient=Patient%2F6cb2a409334943c2b48f1686dc739f11&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "MedicationRequest",
                "id": "3423a69c-618d-4cbe-861a-54c60f48744e",
                "status": "active",
                "intent": "order",
                "reportedBoolean": false,
                "medicationCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://www.fdbhealth.com/",
                            "code": "244899",
                            "display": "lisinopril 10 mg tablet"
                        },
                        {
                            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                            "code": "314076",
                            "display": "lisinopril 10 mg tablet"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/6cb2a409334943c2b48f1686dc739f11",
                    "type": "Patient"
                },
                "encounter": {
                    "reference": "Encounter/bdadce18-098b-40dc-8bdd-ef8481bd999a",
                    "type": "Encounter"
                },
                "authoredOn": "2023-09-21T18:19:36.106449+00:00",
                "requester": {
                    "reference": "Practitioner/6c20b7152cf7421791c5ab4113060b3f",
                    "type": "Practitioner"
                },
                "reasonCode": [
                    {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                                "code": "I10",
                                "display": "Essential (primary) hypertension"
                            }
                        ]
                    }
                ],
                "dosageInstruction": [
                    {
                        "text": "take 1 daily",
                        "doseAndRate": [
                            {
                                "doseQuantity": {
                                    "unit": "Tablet"
                                }
                            }
                        ]
                    }
                ],
                "dispenseRequest": {
                    "numberOfRepeatsAllowed": 3,
                    "quantity": {
                        "value": 30.0
                    },
                    "expectedSupplyDuration": {
                        "value": 30,
                        "unit": "days"
                    },
                    "performer": {
                        "display": "Name: CVS Health #68534|NCPDP ID: 0068534|Address: 1 Cvs Dr, Woonsocket, RI, 028956146|Phone: 4017702500|Fax: 4017704486"
                    }
                },
                "substitution": {
                    "allowedBoolean": true
                }
            }
        }
    ]
}
```
    {% endtab %}

    {% tab medicationrequest-search-response 400 %}
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

    {% tab medicationrequest-search-response 401 %}
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

    {% tab medicationrequest-search-response 403 %}
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
