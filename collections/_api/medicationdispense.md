---
title: MedicationDispense
sections:
  - type: section
    blocks:
      - type: apidoc
        name: MedicationDispense
        article: "a"
        description: >-
          Indicates that a medication product is to be or has been dispensed for a named person/patient. This includes a description of the medication product (supply) provided and the instructions for administering the medication.<br><br>
          [https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-medicationdispense.html](https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-medicationdispense.html)<br><br>
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the MedicationDispense.
            type: string
          - name: status
            description: A code specifying the state of the dispense event.
            type: string
            enum_options:
              - value: completed
              - value: entered-in-error
              - value: stopped
          - name: medicationCodeableConcept
            description: Identifies the medication being requested. This is simply an attribute carrying a code that identifies the medication from a known list of medications.
            type: json
            attributes:
                - name: coding
                  description: Code defined by a terminology system.
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
            description: Who the dispense is for.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: performer
            description: Indicates who performed the dispense.
            type: array[json]
            attributes:
              - name: actor
                type: json
                description: The individual who performed the dispense.
                attributes:
                  - name: reference
                    type: string
                    description: The reference string of the performer in the format of `"Practitioner/ed1e304acdb847148338c6b0596d93fd"`.
                  - name: type
                    type: string
                    description: Type the reference refers to (e.g. "Practitioner").
          - name: authorizingPrescription
            description: Indicates the medication order that is being dispensed against.
            type: array[json]
            attributes:
              - name: reference
                type: string
                description: The reference string of the MedicationRequest in the format of `"MedicationRequest/3423a69c-618d-4cbe-861a-54c60f48744e"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "MedicationRequest").
          - name: type
            description: Indicates the type of dispensing event that is being performed.
            type: json
            attributes:
              - name: text
                description: Plain text representation of the concept
                type: string
          - name: quantity
            description: The amount of medication that has been dispensed.
            type: json
            attributes:
              - name: value
                type: decimal
                description: Numerical value of the quantity.
          - name: whenHandedOver
            description: When the medication was handed over to the patient.
            type: datetime
          - name: dosageInstruction
            description: Indicates how the medication is to be used by the patient.
            type: array[json]
            attributes:
                - name: text
                  type: string
                  description: Free text dosage instructions. In Canvas this text comes from the `SIG` or  `DIRECTIONS` field on the associated command.
                - name: timing
                  type: json
                  description: When medication should be administered.
                  attributes:
                    - name: event
                      type: array[string]
                      description: Identifies the specific times when the medication should be administered.
                - name: doseAndRate
                  type: array[json]
                  description: Amount of medication administered.
                  attributes:
                    - name: doseQuantity
                      type: json
                      description: Amount of medication per dose.
                      attributes:
                        - name: value
                          description: Numerical value
                          type: decimal
                        - name: unit
                          description: Unit representation. 
                          type: string
        search_parameters:
          - name: _id
            description: The identifier of the MedicationDispense.
            type: string
          - name: patient
            description: The patient reference associated with the MedicationDispense in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
        endpoints: [read, search]
        read:
          description: Read a MedicationDispense resource.
          responses: [200, 401, 403, 404]
          example_request: medicationdispense-read-request
          example_response: medicationdispense-read-response
        search:
          description: Search for MedicationDispense resources.
          responses: [200, 400, 401, 403]
          example_request: medicationdispense-search-request
          example_response: medicationdispense-search-response
---

<div id="medicationdispense-read-request">
{%  include read-request.html resource_type="MedicationDispense" %}
</div>

<div id="medicationdispense-read-response">

  {% tabs medicationdispense-read-response %}

    {% tab medicationdispense-read-response 200 %}
```json
{
    "resourceType": "MedicationDispense",
    "id": "a47c7b0e-bbb4-42cd-bc4a-df259d148ea1",
    "status": "completed",
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
    "performer": [
        {
            "actor": {
                "reference": "Practitioner/6c20b7152cf7421791c5ab4113060b3f",
                "type": "Practitioner"
            }
        }
    ],
    "authorizingPrescription": [
        {
            "reference": "MedicationRequest/3423a69c-618d-4cbe-861a-54c60f48744e",
            "type": "MedicationRequest"
        }
    ],
    "type": {
        "text": "Office-supplied"
    },
    "quantity": {
        "value": 30
    },
    "whenHandedOver": "2023-09-21T18:35:00.000+00:00",
    "dosageInstruction": [
        {
            "text": "take 1 daily",
            "timing": {
              "event": [
                "2023-09-21T18:35:00.000+00:00"
              ]
            },
            "doseAndRate": [
                {
                    "doseQuantity": {
                        "value": 5,
                        "unit": "Tablet"
                    }
                }
            ]
        }
    ]
}
```
    {% endtab %}

    {% tab medicationdispense-read-response 401 %}
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

    {% tab medicationdispense-read-response 403 %}
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

    {% tab medicationdispense-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown MedicationDispense resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="medicationdispense-search-request">
{% include search-request.html resource_type="MedicationDispense" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="medicationdispense-search-response">

  {% tabs medicationdispense-search-response %}

    {% tab medicationdispense-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/MedicationDispense?patient=Patient%2F6cb2a409334943c2b48f1686dc739f11&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/MedicationDispense?patient=Patient%2F6cb2a409334943c2b48f1686dc739f11&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/MedicationDispense?patient=Patient%2F6cb2a409334943c2b48f1686dc739f11&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "MedicationDispense",
                "id": "a47c7b0e-bbb4-42cd-bc4a-df259d148ea1",
                "status": "completed",
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
                "performer": [
                    {
                        "actor": {
                            "reference": "Practitioner/6c20b7152cf7421791c5ab4113060b3f",
                            "type": "Practitioner"
                        }
                    }
                ],
                "authorizingPrescription": [
                    {
                        "reference": "MedicationRequest/3423a69c-618d-4cbe-861a-54c60f48744e",
                        "type": "MedicationRequest"
                    }
                ],
                "type": {
                    "text": "Office-supplied"
                },
                "quantity": {
                    "value": 30
                },
                "whenHandedOver": "2023-09-21T18:35:00.000+00:00",
                "dosageInstruction": [
                    {
                        "text": "take 1 daily",
                        "timing": {
                            "event": [
                                "2023-09-21T18:35:00.000+00:00"
                            ]
                        },
                        "doseAndRate": [
                            {
                                "doseQuantity": {
                                    "value": 5,
                                    "unit": "Tablet"
                                }
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab medicationdispense-search-response 400 %}
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

    {% tab medicationdispense-search-response 401 %}
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

    {% tab medicationdispense-search-response 403 %}
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
