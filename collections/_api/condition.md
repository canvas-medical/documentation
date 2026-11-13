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
          <aside class="alert alert__wrapper alert__warning" role="alert"><div class="alert__icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 512a256 256 0 1 0 0-512 256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24v112c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zm-32 224a32 32 0 1 1 64 0 32 32 0 1 1-64 0z"/></svg></div><div class="alert__content">The Diagnose command is planned for retirement in a future release, in favor of Assess. An active Condition created through this endpoint is recorded with a Diagnose command, or with an Assess command when your instance records Diagnose as Assess. To move off Diagnose ahead of its retirement, <a href="https://canvas-medical.help.usepylon.com/">contact Canvas Support</a> to turn that on. See <a href="/product-updates/important-dates/">Important Dates</a>.</div></aside>

          A clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.<br><br>
          [https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-condition-encounter-diagnosis.html](https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-condition-encounter-diagnosis.html)<br>
          [https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-condition-problems-health-concerns.html](https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-condition-problems-health-concerns.html)
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
            create_description: If clinicalStatus is active, the Condition is added as a Diagnose command, or as an Assess command when your instance records Diagnose as Assess. If it is not active, the Condition is added as a Past Medical History command.
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
                        - value: relapse
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
                        - value: Relapse
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
                        - value: Relapse
                          exclude_in: create,update
                        - value: Remission
                          exclude_in: create,update
          - name: verificationStatus
            description_for_all_endpoints: The verification status to support the clinical status of the condition.
            read_and_search_description: A `confirmed` status corresponds to a committed condition on the patient's record, whichever command recorded it, including Diagnose, Assess, Add Condition, Past Medical History, or an Assess Coding Gap accepted with Accept and Diagnose. An `entered-in-error` status means the condition, or the command that recorded it, was entered-in-error. A `provisional` condition was added as an `indication` on an Imaging Order, Refer, POC Lab Test, or Lab Order command, in a note or by a plugin, or by a protocol recommendation for a condition the patient doesn't have charted. Indications on Prescribe and Order DME commands don't add conditions.  
            exclude_in: create, update
            type: json
            attributes:
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      enum_options: 
                        - value: http://terminology.hl7.org/CodeSystem/condition-ver-status
                      type: string
                    - name: code
                      description: The code of the clinical status.
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
                  description: >-
                    Identifies where the definition of the code comes from.<br><br>
                    The codes `encounter-diagnosis` and `problem-list-item` are paired with the system `http://terminology.hl7.org/CodeSystem/condition-category`.<br><br>
                    The code `health-concern` is paired with the system `http://hl7.org/fhir/us/core/CodeSystem/condition-category`.<br><br>
                    The codes `sdoh`, `functional-status`, `disability-status`, and `cognitive-status` are paired with the system `http://hl7.org/fhir/us/core/CodeSystem/us-core-category`. Please note that these codings are only optionally included as a secondary codeable concept for problem list items or health concerns.<br><br>
                    A condition can have more than one category. A condition assessed in a note has `encounter-diagnosis`, and also `problem-list-item` when it's on the problem list. The Canvas chart lists an active condition only when its categories include `problem-list-item` or `health-concern`, so include one of them when you create a condition that belongs on the chart. An active condition with `encounter-diagnosis` alone is recorded for a visit and doesn't appear in the chart's Conditions list.
                  type: array[json]
                  required_in: create, update
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      required_in: create, update
                      enum_options: 
                        - value: http://terminology.hl7.org/CodeSystem/condition-category
                        - value: http://hl7.org/fhir/us/core/CodeSystem/condition-category
                        - value: http://hl7.org/fhir/us/core/CodeSystem/us-core-category
                      type: string
                    - name: code
                      description: The category code.
                      required_in: create, update
                      type: string
                      enum_options: 
                        - value: encounter-diagnosis
                        - value: problem-list-item
                        - value: health-concern
                        - value: sdoh
                        - value: functional-status
                        - value: disability-status
                        - value: cognitive-status
                    - name: display
                      description: The display name of the coding.
                      exclude_in: create, update
                      type: string
                      enum_options: 
                        - value: Encounter Diagnosis
                        - value: Problem List Item
                        - value: Health Concern
                        - value: SDOH
                        - value: Functional Status
                        - value: Disability Status
                        - value: Cognitive Status
                - name: text
                  description: Plain text representation of the concept.
                  exclude_in: create, update
                  type: string
                  enum_options: 
                        - value: Encounter Diagnosis
                        - value: Problem List Item
                        - value: Health Concern
                        - value: SDOH
                        - value: Functional Status
                        - value: Disability Status
                        - value: Cognitive Status
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
            create_description: Additional information about the Condition, up to 1,000 characters. This note only appears in the Canvas UI for resolved conditions. When your instance records Diagnose as Assess, the note of an active Condition becomes the Assess narrative.
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
              - value: confirmed
              - value: entered-in-error
              - value: provisional
          - name: category
            description: >-
              The category of the condition. Filters by the code and/or system under `category.coding` attribute. You can search by just the code value or you can search by the system and code in the format `system|code` (e.g. `http://terminology.hl7.org/CodeSystem/condition-category|health-concern`).
            type: string
        endpoints: [create, read, update, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          description: >-
            Create a Condition resource.<br><br>
            If `clinicalStatus` is **active**, the Condition is added as a `Diagnose` command. If it is not **active**, the Condition is added as a `Past Medical History` command.<br><br>
            If an `encounter` or a note ID in the `extension` is provided, the Condition is added to the existing encounter (note). If it is not provided, a new data import note is created.<br><br>
            By default, this endpoint does not prevent duplicates in the record. **Canvas recommends performing a search prior to adding a new condition** to confirm whether the condition has already been created for the patient.<br><br>
            **Recording Diagnose as Assess**<br><br>
            As part of the rollout retiring the Diagnose command, this endpoint records conditions as described below. To use this behavior now, ahead of the rollout, [contact Canvas Support](https://canvas-medical.help.usepylon.com/). It also keeps integrations that resend conditions from adding duplicates, and it changes how plugins' Diagnose commands are recorded; see [Diagnose](/sdk/commands/#diagnose). With it on, creates work as follows:<br><br>
            **A code the patient already has:** If the patient already has an active or resolved condition with the same ICD-10 code, the request returns `422` with the ID of that condition, and nothing is written. Codes are compared ignoring dots and case. Use the existing condition instead of creating another.<br><br>
            **A new active condition:** The Condition is recorded with a committed `Assess` command in the note. The Assess narrative is the Condition's `note` text, and its onset date is `onsetDateTime`. The condition goes on the problem list unless its categories include `encounter-diagnosis`. Plugins receive Assess command events for the command.<br><br>
            **A new resolved condition:** The Condition is added as a `Past Medical History` command, as it is with the setting off.
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
            The only type of Condition update interaction that is supported by Canvas is to mark an existing Condition as **entered-in-error**. No changes to other fields will be processed. All required fields must still be provided, but our FHIR Update will assume a call to the FHIR Condition Update is an intention to mark the condition as entered-in-error.<br><br>
            When your instance records Diagnose as Assess, entering a Condition in error also enters in error the command that recorded it: the `Diagnose`, `Assess`, `Add Condition`, or `Past Medical History` command. This works only when that command is all that references the condition. If another command assesses or resolves the condition, or no such command recorded it, the request returns `422`; enter the condition in error from the patient's chart instead.
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
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5"
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
                    "code": "problem-list-item",
                    "display": "Problem List Item"
                }
            ],
            "text": "Problem List Item"
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
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5"
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
                    "code": "problem-list-item",
                    "display": "Problem List Item"
                }
            ],
            "text": "Problem List Item"
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
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5"
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
                    "code": "problem-list-item",
                    "display": "Problem List Item"
                }
            ],
            "text": "Problem List Item"
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
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5"
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
                    "code": "problem-list-item",
                    "display": "Problem List Item"
                }
            ],
            "text": "Problem List Item"
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
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5"
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
                    "code": "problem-list-item",
                    "display": "Problem List Item"
                }
            ],
            "text": "Problem List Item"
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
{% include search-request.html resource_type="Condition" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0&category=http://terminology.hl7.org/CodeSystem/condition-category|health-concern" %}
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
                        "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5"
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
                                "code": "problem-list-item",
                                "display": "Problem List Item"
                            }
                        ],
                        "text": "Problem List Item"
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
