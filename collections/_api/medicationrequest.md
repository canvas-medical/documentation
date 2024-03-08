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
          FHIR MedicationRequest maps to the [Prescribe](https://canvas-medical.zendesk.com/hc/en-us/articles/360063523313-Prescribing-a-Medication), [Refill](https://canvas-medical.zendesk.com/hc/en-us/articles/360057482354-Refill-Medications), [Adjust Prescription](https://canvas-medical.zendesk.com/hc/en-us/articles/360061706154-Adjust-an-Existing-Medication), [Deny Refill](https://canvas-medical.zendesk.com/hc/en-us/articles/360059826994-Denying-an-electronic-refill-request) or [Approve Refill](https://canvas-medical.zendesk.com/hc/en-us/articles/360063524493-Approve-an-electronic-refill-request) commands in Canvas.
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the MedicationRequest.
            type: string
          - name: status
            description: A code specifying the current state of the order.
            type: enum [ active | entered-in-error | cancelled ]
          - name: intent
            description: Whether the request is a proposal, plan, or an original order. <br><br>A Medication Request that corresponds to a refill in the patient's chart will have an intent of `filler-order` while all other Medication Requests will be `order`.
            type: enum [ order | filler-order ]
          - name: reportedBoolean
            description: Indicates if this record was captured as a secondary 'reported' record rather than as an original primary source-of-truth record.<br><br> Currently this will always be False from Canvas.
            type: boolean
          - name: medicationCodeableConcept
            description: Identifies the medication being requested. This is simply an attribute carrying a code that identifies the medication from a known list of medications.
            type: json
            attributes:
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      enum_options: 
                        - value: http://www.nlm.nih.gov/research/umls/rxnorm
                        - value: http://www.fdbhealth.com/
                      type: string
                    - name: code
                      description: The code of the medication.
                      type: string
                    - name: display
                      description: The display name of the coding.
                      type: string
          - name: subject
            description: Who or group medication request is for.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: encounter
            description: Encounter created as part of encounter/admission/stay. 
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the encounter in the format of `"Encounter/f7663d7b-13bd-4236-843e-086306aea125"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Encounter").
          - name: authoredOn
            description: When request was initially authored. In Canvas this corresponds to the time the command was created. 
            type: datetime
          - name: requester
            description: Who/What requested the Request.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Practitioner/ed1e304acdb847148338c6b0596d93fd"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
          - name: performer [deprecated]
            description: >-
              Intended performer of administration<br><br>
              This attribute is deprecated and will be removed in a future release. It currently (and incorrectly) contains information about the dispenser of the medication. Canvas recommends disregarding this attribute. Information about the dispenser can be obtained from the `performer` attribute under `dispenseRequest`.
            type: json
          - name: reasonCode
            description: Reason or indication for ordering or not ordering the medication.<br><br> In Canvas this represents the indications on a Prescribe/Refill Command.
            type: array[json]
            attributes:
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      type: string
                      enum_options:
                        - value: http://hl7.org/fhir/sid/icd-10-cm
                    - name: code
                      description: The code of the indication.
                      type: string
                    - name: display
                      description: The display name of the coding.
                      type: string
          - name: note
            description: Information about the prescription.
            type: array[json]
            attributes:
                - name: text
                  type: string
                  description: The annotation - text content.
          - name: dosageInstruction
            description: How the medication should be taken.
            type: array[json]
            attributes:
                - name: text
                  type: string
                  description: Free text dosage instructions. In Canvas this text comes from the `SIG` or  `DIRECTIONS` field on the associated command.
                - name: doseAndRate
                  type: array[json]
                  description: Amount of medication administered.
                  attributes:
                    - name: doseQuantity
                      type: json
                      description: Amount of medication per dose.
                      attributes:
                        - name: unit
                          description: Unit representation. 
                          type: string
          - name: dispenseRequest
            description: Medication supply authorization.
            type: json
            attributes: 
                - name: numberOfRepeatsAllowed
                  type: integer
                  description: Number of refills authorized.
                - name: quantity
                  type: json
                  description: Amount of medication to supply per dispense.
                  attributes: 
                    - name: value
                      type: decimal
                      description: Numerical value.
                - name: expectedSupplyDuration
                  type: json
                  description: Number of days supply per dispense.
                  attributes:
                    - name: value
                      type: integer
                      description: Numerical value.
                    - name: unit
                      description: Unit representation. 
                      type: string
                      enum_options:
                        - value: days
                - name: performer
                  type: json
                  description: Intended dispenser. In Canvas this represents the pharmacy the medication request was sent to. 
                  attributes:
                    - name: display
                      type: string
                      description: "Text alternative for the resource. <br><br>This display name concatenates the following information about the pharmacy: Name, NCPDP ID, Address, Phone, and Fax"
          - name: substitution
            description: Any restrictions on medication substitution.
            type: json
            attributes:
                - name: allowedBoolean
                  type: boolean
                  description: Whether substitution is allowed or not.
        search_parameters:
          - name: _id
            description: The identifier of the MedicationRequest.
            type: string
          - name: intent
            description: Search Medication Requests by specific intents.
            search_options:
                - value: order
                - value: filler-order
            type: string
          - name: patient
            description: The patient reference associated to the Medication Request in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
          - name: status
            description: Search Medication Requests by a specific status.
            type: string
            search_options:
                - value: active
                - value: entered-in-error
                - value: cancelled
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
{% include search-request.html resource_type="MedicationRequest" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
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
