---
title: MedicationStatement
sections:
  - type: section
    blocks:
      - type: apidoc
        name: MedicationStatement
        article: "a"
        description: >-
         A record of a medication that is being consumed by a patient. A MedicationStatement may indicate that the patient may be taking the medication now or has taken the medication in the past or will be taking the medication in the future. The source of this information can be the patient, significant other (such as a family member or spouse), or a clinician. A common scenario where this information is captured is during the history taking process during a patient visit or stay. The medication information may come from sources such as the patient's memory, from a prescription bottle, or from a list of medications the patient, clinician or other party maintains.<br><br>
          [https://hl7.org/fhir/R4/medicationstatement.html](https://hl7.org/fhir/R4/medicationstatement.html)<br><br>
          MedicationStatement resources can be created in several ways. Canvas [Prescribe](https://canvas-medical.zendesk.com/hc/en-us/articles/360063523313-Prescribing-a-Medication) commands create [MedicationRequest](http://localhost:3000/api/medicationrequest/) resources, but these `Prescribe` commands are also represented as MedicationStatement resources. MedicationStatement resources that were created with a `Prescribe` command will contain a reference to the related MedicationRequest resource in the `derivedFrom` attribute.<br><br>
          MedicationStatement resources can also be created with the `Medication Statement` command. See our [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/1500004007942-Documenting-a-Historical-Medication) for more information.
        attributes:
          - name: id
            description: The identifier of the MedicationStatement
            type: string
          - name: extension
            type: array[json]
            description: >-
              Canvas supports a note identifier extension on this resource for create interactions. The note identifier can be used with the [Canvas Note API](/api/note).<br>
              <br>
              **Important:** For create interactions, Canvas recommends sending the note identifier extension or the Encounter reference, but not both. If both are supplied, they must both refer to the same note.<br>
              <br>
              See the request and response examples for more information.
            attributes:
                - name: url
                  type: string
                  required: true
                  description: >-
                    Reference that defines the content of this object. Currently we only support extensions for note identifier we have a url of `http://schemas.canvasmedical.com/fhir/extensions/note-id`
                - name: valueId
                  type: string
                  required: false
                  description: The valueId field is used for the Note extension and will be the note's unique identifier
          - name: status
            required: true
            description: >-
              A code representing the patient or other source's judgment about the state of the medication used that this statement is about<br><br>Supported codes for create interactions are: **active**, **entered-in-error**, **stopped**
            type: string
          - name: medicationCodeableConcept
            description: What medication was taken
            required: true
            type: json
            attributes:
                - name: system
                  type: string
                  required: true
                  description: The url of the medication coding. Currently Canvas supports `"http://www.nlm.nih.gov/research/umls/rxnorm"` or `"http://www.fdbhealth.com/"`
                - name: code
                  type: string
                  required: true
                  description: The code value of the medication coding
                - name: display
                  type: string
                  required: true
                  description: The display name of the medication
          - name: subject
            description: Who is/was taking the medication
            type: json
            required: true
            attributes:
                - name: reference
                  type: string
                  required: true
                  description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Patient")
          - name: context
            description: >-
              Encounter / Episode associated with MedicationStatement<br><br>
              The `context` attribute is accepted by create and update interactions, but is not returned by read or search interactions. If ommitted in the create request, a Data Import note will be added to the timeline based on the timestamp of creation of the create request<br><br>
              **Canvas does not currently support concurrent creation of resources on the same encounter.** Please avoid issuing concurrent requests that reference the same encounter to this endpoint, or to any other endpoints that reference encounters. It is OK to issue concurrent requests to these endpoints as long as the requests reference different encounters.
            type: json
            attributes:
                - name: reference
                  type: string
                  required: true
                  description: The reference string of the encounter in the format of `"Encounter/948b54e2-40b7-4648-bfce-e2373f9802af"`
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Encounter")
          - name: effectivePeriod
            description: The interval when the medication is/was/will be taken.
            type: json
            attributes:
                - name: start
                  type: datetime
                  required: true
                  description: The datetime string represented the start time of the medication in ISO 8601 format like `"2022-03-19T14:54:12.194952+00:00"`. If omitted this will default to the current timestamp.
                - name: end
                  type: datetime
                  required: true
                  description: The datetime string represented the end time of the medication in ISO 8601 format like `"2022-03-19T14:54:12.194952+00:00"`. If omitted, this field will be left empty.
          - name: dateAsserted
            description: When the statement was asserted. This is autogenerated on a create request. 
            type: datetime
          - name: derivedFrom
            description: Additional supporting information that will display in a Read/Search only and ignored in a Create/Update. Currently this will display if the medication was added to the Patient's chart via a MedicationRequest (prescribe or refill command).
            type: array[json]
            attributes:
                - name: reference
                  type: string
                  required: true
                  description: The reference string of the MedicationRequest in the format of `"medicationReference/948b54e2-40b7-4648-bfce-e2373f9802af"`
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "MedicationRequest")
          - name: dosage
            description: >-
              Details of how medication is/was taken or should be taken<br><br>
              The `text` attribute for the Dosage object contains the SIG.
            type: array[json]
            attributes:
                - name: text
                  type: string
                  description: The SIG of the medication
        search_parameters:
          - name: _id
            description: The identifier of the MedicationStatement
            type: string
          - name: patient
            description: Returns statements for a specific patient
            type: string
        endpoints: [create, read, update, search]
        create:
          description: Create a MedicationStatement resource.<br><br>If `context` is provided, the MedicationStatement will be added to the existing encounter (note). If it is not provided, a new data import note will be created.<br><br>Create requests support either `medicationReference` or `medicationCodeableConcept` in the request body; Canvas recommends using `medicationReference`. Medication identifiers for `medicationReference` can be obtained from the [Medication search endpoint](/api/medication/#search).
          responses: [201, 400, 401, 403, 405, 422]
          example_request: medicationstatement-create-request
          example_response: medicationstatement-create-response
        read:
          description: Read an MedicationStatement resource.<br><br>Read responses will always contain a `medicationCodeableConcept` regardless of what was used to create the MedicationStatement.
          responses: [200, 401, 403, 404]
          example_request: medicationstatement-read-request
          example_response: medicationstatement-read-response
        update:
          description: Update an MedicationStatement resource.<br><br>The only type of MedicationStatement update interaction that is supported by Canvas is to mark an existing MedicationStatement as **entered-in-error**. No changes to other fields will be processed.
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: medicationstatement-update-request
          example_response: medicationstatement-update-response
        search:
          description: Search for MedicationStatement resources.<br><br>Search bundle entries will always contain values for `medicationCodeableConcept` regardless of what was used to create the MedicationStatement.
          responses: [200, 400, 401, 403]
          example_request: medicationstatement-search-request
          example_response: medicationstatement-search-response
---

<div id="medicationstatement-create-request">

  {% tabs medicationstatement-create-request %}

    {% tab medicationstatement-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/MedicationStatement' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "MedicationStatement",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "status": "active",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "259181",
                "display": "Advil 200 mg tablet"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "310965",
                "display": "Advil 200 mg tablet"
            }
        ]
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "context": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "effectivePeriod": {
        "start": "2023-06-15T15:00:00-04:00",
        "end": "2023-06-25T15:00:00-04:00"
    },
    "dosage": [
        {
            "text": "1-2 tablets once daily at bedtime as needed for restless legs"
        }
    ]
}'
```
    {% endtab %}

    {% tab medicationstatement-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/MedicationStatement"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "MedicationStatement",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "status": "active",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "259181",
                "display": "Advil 200 mg tablet"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "310965",
                "display": "Advil 200 mg tablet"
            }
        ]
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "context": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "effectivePeriod": {
        "start": "2023-06-15T15:00:00-04:00",
        "end": "2023-06-25T15:00:00-04:00"
    },
    "dosage": [
        {
            "text": "1-2 tablets once daily at bedtime as needed for restless legs"
        }
    ]
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="medicationstatement-create-response">
{% include create-response.html %}
</div>

<div id="medicationstatement-read-request">
{%  include read-request.html resource_type="MedicationStatement" %}
</div>

<div id="medicationstatement-read-response">

  {% tabs medicationstatement-read-response %}

    {% tab medicationstatement-read-response 200 %}
```json
{
    "resourceType": "MedicationStatement",
    "id": "e76e44b4-4e68-4f72-b1c3-1de528a3bb2a",
    "status": "active",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "259181",
                "display": "Advil 200 mg tablet"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "310965",
                "display": "Advil 200 mg tablet"
            }
        ]
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "context": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "effectivePeriod": {
        "start": "2023-06-15T15:00:00-04:00",
        "end": "2023-06-25T15:00:00-04:00"
    },
    "dosage": [
        {
            "text": "1-2 tablets once daily at bedtime as needed for restless legs"
        }
    ]
}
```
    {% endtab %}

    {% tab medicationstatement-read-response 401 %}
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

    {% tab medicationstatement-read-response 403 %}
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

    {% tab medicationstatement-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown MedicationStatement resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="medicationstatement-update-request">

  {% tabs medicationstatement-update-request %}

    {% tab medicationstatement-update-request curl %}
```shell
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/MedicationStatement/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "MedicationStatement",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "status": "entered-in-error",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "259181",
                "display": "Advil 200 mg tablet"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "310965",
                "display": "Advil 200 mg tablet"
            }
        ]
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "context": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "effectivePeriod": {
        "start": "2023-06-15T15:00:00-04:00",
        "end": "2023-06-25T15:00:00-04:00"
    },
    "dosage": [
        {
            "text": "1-2 tablets once daily at bedtime as needed for restless legs"
        }
    ]
}'
```
    {% endtab %}

    {% tab medicationstatement-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/MedicationStatement/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "MedicationStatement",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "status": "entered-in-error",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "259181",
                "display": "Advil 200 mg tablet"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "310965",
                "display": "Advil 200 mg tablet"
            }
        ]
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "context": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "effectivePeriod": {
        "start": "2023-06-15T15:00:00-04:00",
        "end": "2023-06-25T15:00:00-04:00"
    },
    "dosage": [
        {
            "text": "1-2 tablets once daily at bedtime as needed for restless legs"
        }
    ]
}
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="medicationstatement-update-response">
{% include update-response.html resource_type="MedicationStatement" %}
</div>

<div id="medicationstatement-search-request">
{% include search-request.html resource_type="MedicationStatement" search_string="patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="medicationstatement-search-response">

  {% tabs medicationstatement-search-response %}

    {% tab medicationstatement-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/MedicationStatement?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/MedicationStatement?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/MedicationStatement?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "MedicationStatement",
                "id": "e76e44b4-4e68-4f72-b1c3-1de528a3bb2a",
                "status": "active",
                "medicationCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://www.fdbhealth.com/",
                            "code": "259181",
                            "display": "Advil 200 mg tablet"
                        },
                        {
                            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                            "code": "310965",
                            "display": "Advil 200 mg tablet"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
                },
                "context": {
                    "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
                },
                "effectivePeriod": {
                    "start": "2023-06-15T15:00:00-04:00",
                    "end": "2023-06-25T15:00:00-04:00"
                },
                "dosage": [
                    {
                        "text": "1-2 tablets once daily at bedtime as needed for restless legs"
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab medicationstatement-search-response 400 %}
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

    {% tab medicationstatement-search-response 401 %}
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

    {% tab medicationstatement-search-response 403 %}
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
