---
title: FHIR MedicationRequest
sections:
  - type: section
    blocks:
      - type: apidoc
        name: MedicationRequest
        article: "a"
        description: >-
         An order or request for both supply of the medication and the instructions for administration of the medication to a patient. The resource is called "MedicationRequest" rather than "MedicationPrescription" or "MedicationOrder" to generalize the use across inpatient and outpatient settings, including care plans, etc., and to harmonize with workflow patterns.
        attributes:
          - name: id
            description: >-
              The identifier of the medication request
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: status
            description: >-
              The status of the medication request
            type: string
          - name: intent
            description: >-
              The intent of the medication request (e.g. isFiller, order, etc.)
            type: string
          - name: reportedBoolean
            type: boolean
          - name: medicationCodeableConcept
            description: >-
              Medication to be taken
            type: string
          - name: medicationReference
            description: >-
              Medication to be taken
            type: string
          - name: subject
            description: >-
              The patient who is the subject of the medication request
            type: string
          - name: encounter
            description: >-
              The encounter associated with the medication request
            type: string
          - name: authoredOn
            description: >-
              The date and time the medication request was authored
            type: date
          - name: requester
            description: >-
              The practitioner who authored the medication request
            type: string
          - name: performer
            description: >-
              The practitioner who will perform the medication request
            type: string
          - name: reasonCode
            description: >-
              The reason for the medication request
            type: string
            attributes:
              - name: coding
                type: string
                attributes:
                  - name: system
                    type: string
                  - name: code
                    type: string
                  - name: display
                    type: string
          - name: note
            description: >-
              Additional notes about the medication request
            type: string
          - name: dosageInstruction
            description: >-
              Details of how medication is/was taken or should be taken
            type: string
            attributes:
              - name: text
                type: string
              - name: doseAndRate
                type: string
                attributes:
                  - name: doseQuantity
                    type: string
                    attributes:
                      - name: value
                        type: number
                      - name: unit
                        type: string
          - name: dispenseRequest
            description: >-
              Medication supply authorization
            type: string
            attributes:
              - name: numberOfRepeatsAllowed
                type: number
              - name: quantity
                type: string
                attributes:
                  - name: value
                    type: number
              - name: expectedSupplyDuration
                type: string
                attributes:
                  - name: value
                    type: number
                  - name: unit
                    type: string
          - name: substitution
            description: >-
              Whether substitution is allowed or not
            type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            description: >-
              The patient who is the subject of the medication request
            type: string
        endpoints: [read, search]
        read:
          responses: [200, 400]
          example_response: medication-request-read-response
          example_request: medication-request-read-request
        search:
          responses: [200, 400]
          example_response: medication-request-search-response
          example_request: medication-request-search-request
---
<div id="medication-request-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/MedicationRequest/<id>"

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
     --url https://fumage-example.canvasmedical.com/MedicationRequest/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="medication-request-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
{
    "resourceType": "MedicationRequest",
    "id": "c9f8949d-81f5-4d04-a743-ed7d185cc22b",
    "status": "active",
    "intent": "order",
    "reportedBoolean": false,
    "medicationReference": {
        "reference": "Medication/fdb-177730",
        "type": "Medication",
        "display": "sumatriptan 100 mg tablet"
    },
    "subject": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "authoredOn": "2022-11-22T16:17:38.553742+00:00",
    "requester": {
        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
        "type": "Practitioner"
    },
    "performer": {
        "display": "Name: |NCPDP ID: |Address: |Phone: |Fax: "
    },
    "reasonCode": [
        {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/sid/icd-10-cm",
                    "code": "R519",
                    "display": "Headache, unspecified"
                }
            ]
        }
    ],
    "dosageInstruction": [
        {
            "text": "once daily",
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
        "numberOfRepeatsAllowed": 0,
        "quantity": {
            "value": 1.0
        },
        "expectedSupplyDuration": {
            "value": 1,
            "unit": "days"
        }
    },
    "substitution": {
        "allowedBoolean": true
    }
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
                "text": "Unknown MedicationRequest resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="medication-request-search-request">
{% tabs search-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Medication/?patient=Patient/<patient_id>"

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
     --url https://fumage-example.canvasmedical.com/MedicationRequest/?patient=Patient/<patient_id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="medication-request-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link": [
        {
            "relation": "self",
            "url": "/MedicationRequest?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/MedicationRequest?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/MedicationRequest?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "MedicationRequest",
                "id": "c9f8949d-81f5-4d04-a743-ed7d185cc22b",
                "status": "active",
                "intent": "order",
                "reportedBoolean": false,
                "medicationReference": {
                    "reference": "Medication/fdb-177730",
                    "type": "Medication",
                    "display": "sumatriptan 100 mg tablet"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "authoredOn": "2022-11-22T16:17:38.553742+00:00",
                "requester": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                },
                "performer": {
                    "display": "Name: |NCPDP ID: |Address: |Phone: |Fax: "
                },
                "reasonCode": [
                    {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                                "code": "R519",
                                "display": "Headache, unspecified"
                            }
                        ]
                    }
                ],
                "dosageInstruction": [
                    {
                        "text": "once daily",
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
                    "numberOfRepeatsAllowed": 0,
                    "quantity": {
                        "value": 1.0
                    },
                    "expectedSupplyDuration": {
                        "value": 1,
                        "unit": "days"
                    }
                },
                "substitution": {
                    "allowedBoolean": true
                }
            }
        },
        {
            "resource": {
                "resourceType": "MedicationRequest",
                "id": "9723dfa3-cf8e-4d6d-800f-4479c5b29927",
                "status": "active",
                "intent": "order",
                "reportedBoolean": false,
                "medicationReference": {
                    "reference": "Medication/fdb-177730",
                    "type": "Medication",
                    "display": "sumatriptan 100 mg tablet"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "encounter": {
                    "reference": "Encounter/5dd9213b-4b0e-46d2-a476-53d65d8d31af",
                    "type": "Encounter"
                },
                "authoredOn": "2022-12-06T17:14:52.173419+00:00",
                "requester": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                },
                "performer": {
                    "display": "Name: |NCPDP ID: |Address: |Phone: |Fax: "
                },
                "reasonCode": [
                    {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                                "code": "R519",
                                "display": "Headache, unspecified"
                            }
                        ]
                    }
                ],
                "dosageInstruction": [
                    {
                        "text": "twice daily",
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
                    "numberOfRepeatsAllowed": 0,
                    "quantity": {
                        "value": 1.0
                    },
                    "expectedSupplyDuration": {
                        "value": 1,
                        "unit": "days"
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

