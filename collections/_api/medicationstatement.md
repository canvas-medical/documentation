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
          MedicationStatement resources can be created in two ways in the Canvas UI:

          - [Prescribe commands](https://canvas-medical.zendesk.com/hc/en-us/articles/360063523313-Prescribing-a-Medication) create [MedicationRequest](/api/medicationrequest/) resources, but these `Prescribe` commands are also represented as MedicationStatement resources. MedicationStatement resources that were created with a `Prescribe` command will contain a reference to the related MedicationRequest resource in the `derivedFrom` attribute.

          - MedicationStatement resources can also be created with the [Medication Statement command](https://canvas-medical.zendesk.com/hc/en-us/articles/1500004007942-Documenting-a-Historical-Medication)
        attributes:
          - name: id
            description: The identifier of the MedicationStatement.
            type: string
            exclude_in: create
            required_in: update
          - name: extension
            type: array[json]
            description_for_all_endpoints: Canvas supports a note identifier extension on this resource. The note identifier can be used with the [Canvas Note API](/api/note).
            create_description: Canvas recommends sending the note identifier extension or the Encounter reference, but not both. If both are supplied, they must both refer to the same note. If neither is specified, it will insert into a Data Import note where the DOS is the current time of ingestion.
            attributes:
              - name: url
                type: string
                description: Identifies the meaning of the extension
                enum_options:
                  - value: http://schemas.canvasmedical.com/fhir/extensions/note-id
                required_in: create, update
              - name: valueId
                type: string
                description: The valueId field is used for the Note extension and will be the note's unique identifier.
                required_in: create, update
          - name: status
            required_in: create,update
            description: >-
              A code representing the patient or other source's judgment about the state of the medication used that this statement is about.
            enum_options: 
              - value: active
                exclude_in: update
              - value: entered-in-error
              - value: stopped
                exclude_in: update
              - value: intented
                exclude_in: create, update
                description: Medications where the effectivePeriod.start date is in the future
            type: string
          - name: medicationReference
            create_and_update_description: What medication was taken. <br><br>
                Canvas recommends using a medicationReference on create/update to ensure a proper medication lookup is done on validation similar to our commands framework on the Canvas UI. Use the [Medication search endpoint](/api/medication/#search) to help find the correct FDB ID. <br><br>A create/update requires either a medicationReference or medicationCodeableConcept when making a request
            type: json
            exclude_in: read,search
            attributes:
                - name: reference
                  type: string
                  required_in: create,update
                  description: The reference string of the medication in the format of `"Medication/fdb-449732"`
                - name: display
                  type: string
                  required_in: create,update
                  description: The display name of the medication
          - name: medicationCodeableConcept
            description_for_all_endpoints: What medication was taken. <br><br>
                Canvas recommends using a medicationReference on create/update; however on a Read/Search the medicationCodeableConcept will be returned to allow visibility into all the coding associated with the medication (e.g RxNorm, FDB)  <br><br>
            create_and_update_description: A create/update requires either a medicationReference or medicationCodeableConcept when making a request.
            type: json
            attributes:
                - name: system
                  type: string
                  required_in: create,update
                  description: The url of the medication coding. 
                  enum_options:
                    - value: http://www.nlm.nih.gov/research/umls/rxnorm
                    - value: http://www.fdbhealth.com/
                - name: code
                  type: string
                  required_in: create,update
                  description: The code value of the medication coding
                - name: display
                  type: string
                  required_in: create,update
                  description: The display name of the medication
          - name: subject
            description: Who is/was taking the medication.
            type: json
            required_in: create,update
            attributes:
                - name: reference
                  type: string
                  required_in: create,update
                  description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Patient")
          - name: context
            create_and_update_description: >-
              Encounter / Episode associated with MedicationStatement.<br><br>
              Supply an encounter reference to be able to insert the command into a specific note on the patient's timeline. If no encounter or note via the extension is specified, it will insert into a Data Import note where the DOS is the current time of ingestion.
              <br><br>
              **Canvas does not currently support concurrent creation of resources on the same encounter.** Please avoid issuing concurrent requests that reference the same encounter to this endpoint, or to any other endpoints that reference encounters. It is OK to issue concurrent requests to these endpoints as long as the requests reference different encounters.
            type: json
            exclude_in: read,search
            attributes:
                - name: reference
                  type: string
                  required_in: create,update
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
                  description_for_all_endpoints: The datetime string represented the start time of the medication in ISO 8601 format like `"2022-03-19T14:54:12.194952+00:00"`.
                  create_description: If omitted this will default to the current timestamp.
                - name: end
                  type: datetime
                  description_for_all_endpoints: The datetime string represented the end time of the medication in ISO 8601 format like `"2022-03-19T14:54:12.194952+00:00"`.
                  create_description: If omitted, this field will be left empty.
          - name: dateAsserted
            description: When the statement was asserted. This is autogenerated on a create request as the timestamp of ingestion. 
            type: datetime
            exclude_in: create, update
          - name: derivedFrom
            read_and_search_description: This will display if the medication was added to the Patient's chart via a MedicationRequest (prescribe or refill command).
            type: array[json]
            exclude_in: create, update
            attributes:
                - name: reference
                  type: string
                  description: The reference string of the MedicationRequest in the format of `"medicationReference/948b54e2-40b7-4648-bfce-e2373f9802af"`
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "MedicationRequest")
          - name: dosage
            description_for_all_endpoints: >-
              Details of how medication is/was taken or should be taken.<br><br>
              The `text` attribute for the Dosage object contains the SIG. 
            create_description: Canvas will only ingest the first item in the dosage array. 
            type: array[json]
            attributes:
                - name: text
                  type: string
                  description: The SIG of the medication
        search_parameters:
          - name: _id
            description: The identifier of the MedicationStatement.
            type: string
          - name: patient
            description: The patient reference associated to the Medication Statement in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
        endpoints: [create, read, update, search]
        create:
          description: Create a MedicationStatement resource.<br><br>If `context` or `extension` is provided, the MedicationStatement will be added to the existing encounter (note). If it is not provided, a new data import note will be created.<br><br>Create requests support either `medicationReference` or `medicationCodeableConcept` in the request body; Canvas recommends using `medicationReference`. Medication identifiers for `medicationReference` can be obtained from the [Medication search endpoint](/api/medication/#search).
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
    "medicationReference": {
        "reference": "Medication/fdb-259181",
        "display": "Advil 200 mg tablet"
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
    "medicationReference": {
        "reference": "Medication/fdb-259181",
        "display": "Advil 200 mg tablet"
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
    "medicationReference": {
        "reference": "Medication/fdb-259181",
        "display": "Advil 200 mg tablet"
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
    "medicationReference": {
        "reference": "Medication/fdb-259181",
        "display": "Advil 200 mg tablet"
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
