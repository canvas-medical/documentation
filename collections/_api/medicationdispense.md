---
title: MedicationDispense
sections:
  - type: section
    blocks:
      - type: apidoc
        name: MedicationDispense
        article: "a"
        description: >-
          Indicates that a medication product is to be or has been dispensed for a named person/patient. This includes a description of the medication product (supply) provided and the instructions for administering the medication. The medication dispense is the result of a pharmacy system responding to a medication order.<br><br>
          [https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-medicationdispense.html](https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-medicationdispense.html)<br><br>
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the MedicationDispense.
            type: string
          - name: status
            description: A code specifying the state of the dispense event. When status is "completed", whenHandedOver SHALL be present.
            type: enum [ preparation | in-progress | on-hold | completed | entered-in-error | stopped | declined | unknown ]
          - name: medicationCodeableConcept
            description: Identifies the medication that was dispensed. This is either a link to a resource representing the details of the medication or a simple attribute carrying a code that identifies the medication from a known list of medications.
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
            description: A link to the resource representing the patient to whom the medication will be given.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: performer
            description: Indicates who or what performed the dispense.
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
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    type: string
                  - name: code
                    description: The code of the dispense type.
                    type: string
                  - name: display
                    description: The display name of the coding.
                    type: string
          - name: quantity
            description: The amount of medication that has been dispensed. Includes unit of measure.
            type: json
            attributes:
              - name: value
                type: decimal
                description: Numerical value of the quantity.
              - name: unit
                type: string
                description: Unit representation (e.g., "Tablet", "ml", "mg").
              - name: system
                type: string
                description: System that defines the coded form of the unit.
              - name: code
                type: string
                description: Coded form of the unit.
          - name: daysSupply
            description: The amount of medication expressed as a timing amount.
            type: json
            attributes:
              - name: value
                type: integer
                description: Numerical value of the days supply.
              - name: unit
                type: string
                description: Unit representation (typically "days").
          - name: whenHandedOver
            description: When the medication was handed over to the patient or their representative. SHALL be present if the status is "completed".
            type: datetime
          - name: dosageInstruction
            description: Indicates how the medication is to be used by the patient.
            type: array[json]
            attributes:
                - name: text
                  type: string
                  description: Free text dosage instructions.
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
        search_parameters:
          - name: _id
            description: The identifier of the MedicationDispense.
            type: string
          - name: patient
            description: The patient reference associated to the Medication Dispense in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
          - name: performer
            description: The Practitioner reference associated to the MedicationDispense.performer attribute in the format `Practitioner/6c20b7152cf7421791c5ab4113060b3f`.
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
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "RFP",
                "display": "Refill - Part Fill"
            }
        ]
    },
    "quantity": {
        "value": 30,
        "unit": "Tablet",
        "system": "http://unitsofmeasure.org",
        "code": "mL"
    },
    "daysSupply": {
        "value": 30,
        "unit": "days"
    },
    "whenHandedOver": "2023-09-21T18:35:00.000+00:00",
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
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                            "code": "RFP",
                            "display": "Refill - Part Fill"
                        }
                    ]
                },
                "quantity": {
                    "value": 30,
                    "unit": "Tablet",
                    "system": "http://unitsofmeasure.org",
                    "code": "mL"
                },
                "daysSupply": {
                    "value": 30,
                    "unit": "days"
                },
                "whenHandedOver": "2023-09-21T18:35:00.000+00:00",
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
