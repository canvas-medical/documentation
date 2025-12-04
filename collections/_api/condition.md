---
title: Condition
layout: api
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Condition
        article: "a"
        description: >-
          A clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-condition.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-condition.html)
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the Condition.
            type: string
            exclude_in: create
            required_in: update
          - name: text
            description: Text summary of the Condition, for human interpretation.
            type: json
            exclude_in: create,update
            attributes:
              - name: status
                type: enum [ generated ]
                description: The status of the narrative.
              - name: div
                type: string
                description: Limited xhtml content that contains the human readable text of the Condition.
          - name: extension
            type: array[json]
            exclude_in: update
            description_for_all_endpoints: Canvas supports a note identifier extension on this resource. The note identifier can be used with the [Canvas Note API](/api/note).
            create_description: Canvas recommends sending the note identifier extension or the Encounter reference, but not both. If both are supplied, they must both refer to the same note. If neither is specified, it will insert into a Data Import note where the DOS is the current time of ingestion.
            attributes:
                - name: url
                  type: string
                  description: Reference that defines the content of this object.
                  enum_options:
                    - value: http://schemas.canvasmedical.com/fhir/extensions/note-id
                - name: valueId
                  type: string
                  description: The valueId field is used for the Note extension and will be the note's unique identifier.
          - name: clinicalStatus
            description_for_all_endpoints: The clinical status of the condition.
            create_description: If clinicalStatus is active, the Condition will be added as a Diagnose command. If it is not active, the Condition will be added as a Past Medical History command.
            required_in: create, update
            type: json
            attributes:
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  required_in: create, update
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      required_in: create, update
                      enum_options: 
                        - value: http://terminology.hl7.org/CodeSystem/condition-clinical
                      type: string
                    - name: code
                      description: The code of the clinical status.
                      required_in: create, update
                      type: string
                      enum_options: 
                        - value: active
                        - value: resolved
                        - value: relapsed
                          exclude_in: create,update
                        - value: remission
                          exclude_in: create,update
                    - name: display
                      description: The display name of the coding.
                      exclude_in: create, update
                      type: string
                      enum_options: 
                        - value: Active
                        - value: Resolved
                        - value: Relapsed
                          exclude_in: create,update
                        - value: Remission
                          exclude_in: create,update
                - name: text
                  description: Plain text representation of the concept.
                  exclude_in: create, update
                  type: string
                  enum_options: 
                        - value: Active
                        - value: Resolved
                        - value: Relapsed
                          exclude_in: create,update
                        - value: Remission
                          exclude_in: create,update
          - name: verificationStatus
            description_for_all_endpoints: The verification status to support the clinical status of the condition.
            read_and_search_description: A `confirmed` status corresponds to committed conditions from a Diagnose or Past Medical History command. An `entered-in-error` status means the Diagnose or Past Medical History command was entered-in-error. A `provisional` condition means it was added as an `indication` to either Image, Refer, POC Lab Test, or a Lab Order command.  
            exclude_in: create, update
            type: json
            attributes:
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  required_in: create, update
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      required_in: create, update
                      enum_options: 
                        - value: http://terminology.hl7.org/CodeSystem/condition-ver-status
                      type: string
                    - name: code
                      description: The code of the clinical status.
                      required_in: create, update
                      type: string
                      enum_options: 
                        - value: confirmed
                        - value: entered-in-error
                        - value: provisional
                    - name: display
                      description: The display name of the coding.
                      exclude_in: create, update
                      type: string
                      enum_options: 
                        - value: Confirmed
                        - value: Entered in Error
                        - value: Provisional
                - name: text
                  description: Plain text representation of the concept.
                  exclude_in: create, update
                  type: string
                  enum_options: 
                        - value: Confirmed
                        - value: Entered in Error
                        - value: Provisional
          - name: category
            description: A category assigned to the condition.
            required_in: create,update
            type: array[json]
            attributes:
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  required_in: create, update
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      required_in: create, update
                      enum_options: 
                        - value: http://terminology.hl7.org/CodeSystem/condition-category
                      type: string
                    - name: code
                      description: The code of the clinical status.
                      required_in: create, update
                      type: string
                      enum_options: 
                        - value: encounter-diagnosis
                    - name: display
                      description: The display name of the coding.
                      exclude_in: create, update
                      type: string
                      enum_options: 
                        - value: Encounter Diagnosis
                - name: text
                  description: Plain text representation of the concept.
                  exclude_in: create, update
                  type: string
                  enum_options: 
                        - value: Encounter Diagnosis
          - name: code
            description_for_all_endpoints: Identification of the condition, problem or diagnosis.
            create_description: Canvas will not validate the coding supplied in the payload, instead Canvas will just save the system, code, and display as provided. We highly recommend supplying a coding with the `system` of `http://hl7.org/fhir/sid/icd-10-cm`.
            type: json
            required_in: create,update
            attributes:
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  required_in: create, update
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      required_in: create, update
                      type: string
                    - name: code
                      description: The code of the clinical status.
                      required_in: create, update
                      type: string
                    - name: display
                      description: The display name of the coding.
                      exclude_in: create, update
                      type: string
          - name: subject
            description: Who has the condition.
            required_in: create,update
            type: json
            attributes:
              - name: reference
                type: string
                required_in: create,update
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: encounter
            exclude_in: update
            description_for_all_endpoints: Encounter created as part of
            create_description: >-
              **Canvas does not currently support concurrent creation of resources on the same encounter.** Please avoid issuing concurrent requests that reference the same encounter to this endpoint, or to any other endpoints that reference encounters. It is OK to issue concurrent requests to these endpoints as long as the requests reference different encounters.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the encounter in the format of `"Encounter/f7663d7b-13bd-4236-843e-086306aea125"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Encounter").
          - name: onsetDateTime
            description: Estimated or actual date.
            type: date
            exclude_in: update
          - name: abatementDateTime
            description: When in resolution/remission.
            type: date
            exclude_in: update
          - name: recordedDate
            description_for_all_endpoints: Date-time record was first recorded.
            create_description: If ommitted it will default to the timestamp of ingestion into Canvas.
            type: datetime
            exclude_in: update
          - name: recorder
            description: Who recorded the condition.
            create_description: If ommitted, this will default to Canvas Bot.
            update_description: On an Update this Practitioner will become the user in Canvas who marked the Condition as entered-in-error. If ommitted, it will default to Canvas Bot.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Practitioner/ed1e304acdb847148338c6b0596d93fd"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
          - name: note
            exclude_in: update
            description: Additional information about the Condition. This note only appears in the Canvas UI for resolved conditions.
            type: array[json]
            attributes:
                - name: text
                  type: string
                  description: The annotation - text content.
        search_parameters:
          - name: _id
            description: The identifier of the Condition.
            type: string
          - name: clinical-status
            description: The clinical status of the condition.
            type: string
            search_options:
                - value: active
                - value: resolved
          - name: patient
            description: The patient reference associated to the Condition in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
          - name: verification-status
            description: The verification status to support the clinical status of the condition.
            type: string
            search_options: 
              - value: entered-in-error
              - value: provisional
        endpoints: [create, read, update, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          description: >-
            Create a Condition resource.<br><br>
            This endpoint does not prevent duplicates in the record. **Canvas recommends performing a search prior to adding a new condition** to confirm whether the condition has already been created for the patient.<br><br>
            If `clinicalStatus` is **active**, the Condition will be added as a `Diagnose` command. If it is not **active**, the Condition will be added as a `Past Medical History` command.<br><br>
            If an `encounter` or a note ID in the `extension` is provided, the Condition will be added to the existing encounter (note). If it is not provided, a new data import note will be created.
          example_request: condition-create-request
          example_response: condition-create-response
        read:
          description: Read a Condition resource.
          responses: [200, 401, 403, 404]
          example_request: condition-read-request
          example_response: condition-read-response
        update:
          description: >-
            Update a Condition resource.<br><br>
            The only type of Condition update interaction that is supported by Canvas is to mark an existing Condition as **entered-in-error**. No changes to other fields will be processed. All required fields must still be provided, but out FHIR Update will assume a call to the FHIR Condition Update is an intention to mark the condition as entered-in-error.
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: condition-update-request
          example_response: condition-update-response
        search:
          description: Search for Condition resources.
          responses: [200, 400, 401, 403]
          example_request: condition-search-request
          example_response: condition-search-response
---

<div id="condition-create-request">

  {% tabs condition-create-request %}

    {% tab condition-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Condition' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Condition",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "resolved",
                "display": "Resolved"
            }
        ],
        "text": "Resolved"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed",
                "display": "Confirmed"
            }
        ],
        "text": "Confirmed"
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                }
            ],
            "text": "Encounter Diagnosis"
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                "code": "V97.21XS",
                "display": "Parachutist entangled in object, sequela"
            }
        ],
        "text": "Parachutist entangled in object, sequela"
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "abatementDateTime": "2023-06-17",
    "recordedDate": "2023-06-18T15:00:00-04:00",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "note": [
        {
            "text": "Condition note"
        }
    ]
}'
```
    {% endtab %}

    {% tab condition-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Condition"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Condition",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "resolved",
                "display": "Resolved"
            }
        ],
        "text": "Resolved"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed",
                "display": "Confirmed"
            }
        ],
        "text": "Confirmed"
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                }
            ],
            "text": "Encounter Diagnosis"
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                "code": "V97.21XS",
                "display": "Parachutist entangled in object, sequela"
            }
        ],
        "text": "Parachutist entangled in object, sequela"
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "abatementDateTime": "2023-06-17",
    "recordedDate": "2023-06-18T15:00:00-04:00",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "note": [
        {
            "text": "Condition note"
        }
    ]
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="condition-create-response">
{% include create-response.html %}
</div>

<div id="condition-read-request">
{% include read-request.html resource_type="Condition" %}
</div>

<div id="condition-read-response">

  {% tabs condition-read-response %}

    {% tab condition-read-response 200 %}
```json
{
    "resourceType": "Condition",
    "id": "3340c331-d446-4700-9c23-7959bd393f26",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "clinicalStatus":
    {
        "coding":
        [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "resolved",
                "display": "Resolved"
            }
        ],
        "text": "Resolved"
    },
    "verificationStatus":
    {
        "coding":
        [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed",
                "display": "Confirmed"
            }
        ],
        "text": "Confirmed"
    },
    "category":
    [
        {
            "coding":
            [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                }
            ],
            "text": "Encounter Diagnosis"
        }
    ],
    "code":
    {
        "coding":
        [
            {
                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                "code": "V97.21XS",
                "display": "Parachutist entangled in object, sequela"
            }
        ],
        "text": "Parachutist entangled in object, sequela"
    },
    "subject":
    {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter":
    {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "abatementDateTime": "2023-06-17",
    "recordedDate": "2023-06-18T15:00:00-04:00",
    "recorder":
    {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "note":
    [
        {
            "text": "Condition note"
        }
    ]
}
```
    {% endtab %}

    {% tab condition-read-response 401 %}
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

    {% tab condition-read-response 403 %}
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

    {% tab condition-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Condition resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="condition-update-request">

  {% tabs condition-update-request %}

    {% tab condition-update-request curl %}
```shell
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/Condition/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Condition",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "resolved",
                "display": "Resolved"
            }
        ],
        "text": "Resolved"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "entered-in-error",
                "display": "Entered in Error"
            }
        ],
        "text": "Entered in Error"
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                }
            ],
            "text": "Encounter Diagnosis"
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                "code": "V97.21XS",
                "display": "Parachutist entangled in object, sequela"
            }
        ],
        "text": "Parachutist entangled in object, sequela"
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "abatementDateTime": "2023-06-17",
    "recordedDate": "2023-06-18T15:00:00-04:00",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "note": [
        {
            "text": "Condition note"
        }
    ]
}'
```
    {% endtab %}

    {% tab condition-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Condition/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Condition",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "resolved",
                "display": "Resolved"
            }
        ],
        "text": "Resolved"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "entered-in-error",
                "display": "Entered in Error"
            }
        ],
        "text": "Entered in Error"
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                }
            ],
            "text": "Encounter Diagnosis"
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                "code": "V97.21XS",
                "display": "Parachutist entangled in object, sequela"
            }
        ],
        "text": "Parachutist entangled in object, sequela"
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "abatementDateTime": "2023-06-17",
    "recordedDate": "2023-06-18T15:00:00-04:00",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "note": [
        {
            "text": "Condition note"
        }
    ]
}
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="condition-update-response">
{% include update-response.html resource_type="Condition" %}
</div>

<div id="condition-search-request">
{% include search-request.html resource_type="Condition" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="condition-search-response">

  {% tabs condition-search-response %}

    {% tab condition-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Condition?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Condition?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Condition?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Condition",
                "id": "3340c331-d446-4700-9c23-7959bd393f26",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
                        "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
                    }
                ],
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "resolved",
                            "display": "Resolved"
                        }
                    ],
                    "text": "Resolved"
                },
                "verificationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                            "code": "confirmed",
                            "display": "Confirmed"
                        }
                    ],
                    "text": "Confirmed"
                },
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                                "code": "encounter-diagnosis",
                                "display": "Encounter Diagnosis"
                            }
                        ],
                        "text": "Encounter Diagnosis"
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "V97.21XS",
                            "display": "Parachutist entangled in object, sequela"
                        }
                    ],
                    "text": "Parachutist entangled in object, sequela"
                },
                "subject": {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
                },
                "encounter": {
                    "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
                },
                "onsetDateTime": "2023-06-15",
                "abatementDateTime": "2023-06-17",
                "recordedDate": "2023-06-18T15:00:00-04:00",
                "recorder": {
                    "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
                },
                "note": [
                    {
                        "text": "Condition note"
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab condition-search-response 400 %}
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

    {% tab condition-search-response 401 %}
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

    {% tab condition-search-response 403 %}
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
