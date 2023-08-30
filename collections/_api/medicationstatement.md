---
title: MedicationStatement
sections:
  - type: section
    blocks:
      - type: apidoc
        name: MedicationStatement
        article: "a"
        description: >-
         A record of a medication that is being consumed by a patient. A MedicationStatement may indicate that the patient may be taking the medication now or has taken the medication in the past or will be taking the medication in the future. The source of this information can be the patient, significant other (such as a family member or spouse), or a clinician. A common scenario where this information is captured is during the history taking process during a patient visit or stay. The medication information may come from sources such as the patient's memory, from a prescription bottle, or from a list of medications the patient, clinician or other party maintains.
        attributes:
          - name: id
            description: >-
              The identifier of the medication statement
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: status
            description: >-
              active | entered-in-error | intended | stopped | unknown
            type: string
          - name: medicationCodeableConcept
            type: string
          - name: medicationReference
            type: string
          - name: subject
            description: >-
              Who is/was taking the medication
            type: string
          - name: effectivePeriod
            description: >-
              The date/time or interval when the medication is/was/will be taken
            type: string
          - name: dateAsserted
            description: >-
              The date and time the medication statement was asserted
            type: date
          - name: derivedFrom
            description: >-
              Additional supporting information
            type: date
          - name: dosage
            description: >-
              Details of how medication is/was taken or should be taken
            type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            description: >-
              The patient who is consuming the medication
            type: string
        endpoints: [search]
        search:
          responses: [200, 400]
          example_response: medication-statement-search-response
          example_request: medication-statement-search-request
---
<div id="medication-statement-search-request">
{% tabs search-request %}
{% tab search-request python %}
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
     --url https://fumage-example.canvasmedical.com/MedicationStatement/?patient=Patient/<patient_id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="medication-statement-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 5,
    "link": [
        {
            "relation": "self",
            "url": "/MedicationStatement?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/MedicationStatement?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/MedicationStatement?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "MedicationStatement",
                "status": "stopped",
                "medicationReference": {
                    "reference": "Medication/fdb-297274",
                    "type": "Medication",
                    "display": "Adderall 10 mg tablet"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "effectivePeriod": {
                    "start": "2022-04-04T05:26:34.711718+00:00",
                    "end": "2022-12-06T17:14:42.751120+00:00"
                },
                "dateAsserted": "2022-04-04T05:28:08.521828+00:00",
                "dosage": [
                    {
                        "text": "take as directed"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "MedicationStatement",
                "status": "entered-in-error",
                "medicationReference": {
                    "reference": "Medication/fdb-587530",
                    "type": "Medication",
                    "display": "Metamucil 3.4 gram/5.4 gram oral powder"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "dateAsserted": "2022-07-20T14:35:01.648218+00:00"
            }
        },
        {
            "resource": {
                "resourceType": "MedicationStatement",
                "status": "active",
                "medicationReference": {
                    "reference": "Medication/fdb-177730",
                    "type": "Medication",
                    "display": "sumatriptan 100 mg tablet"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "effectivePeriod": {
                    "start": "2022-11-22T16:17:38.553742+00:00"
                },
                "dateAsserted": "2022-11-22T16:18:09.314648+00:00",
                "derivedFrom": [
                    {
                        "reference": "MedicationRequest/9723dfa3-cf8e-4d6d-800f-4479c5b29927",
                        "type": "MedicationRequest"
                    },
                    {
                        "reference": "MedicationRequest/c9f8949d-81f5-4d04-a743-ed7d185cc22b",
                        "type": "MedicationRequest"
                    }
                ],
                "dosage": [
                    {
                        "text": "twice daily"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "MedicationStatement",
                "status": "active",
                "medicationReference": {
                    "reference": "Medication/fdb-275877",
                    "type": "Medication",
                    "display": "ibuprofen 600 mg tablet"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "effectivePeriod": {
                    "start": "2022-12-05T16:30:42+00:00"
                },
                "dateAsserted": "2022-12-06T17:07:22.630013+00:00",
                "dosage": [
                    {
                        "text": "once daily"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "MedicationStatement",
                "status": "stopped",
                "medicationReference": {
                    "reference": "Medication/fdb-270143",
                    "type": "Medication",
                    "display": "furosemide 20 mg tablet"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "effectivePeriod": {
                    "start": "2022-12-06T17:11:36.839849+00:00",
                    "end": "2022-12-06T17:12:49.492753+00:00"
                },
                "dateAsserted": "2022-12-06T17:12:09.892765+00:00",
                "dosage": [
                    {
                        "text": "once daily"
                    }
                ]
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

