---
title: AllergyIntolerance
sections:
  - type: section
    blocks:
      - type: apidoc
        name: AllergyIntolerance
        article: "an"
        description: >-
          Risk of harmful or undesirable, physiological response which is unique to an individual and associated with exposure to a substance.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-allergyintolerance.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-allergyintolerance.html)
          <br><br>
          To learn more about documenting allergies in Canvas see [here](https://canvas-medical.zendesk.com/hc/en-us/articles/360056920593-Document-Allergies).
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the AllergyIntolerance.
            type: string
            required_in: update
            exclude_in: create
          - name: extension
            type: array[json]
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
            required_in: create, update
            description: The clinical status of the allergy or intolerance.
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
                        - value: http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical
                      type: string
                    - name: code
                      description: The code of the clinical status.
                      required_in: create, update
                      type: string
                      enum_options: 
                        - value: active
                        - value: inactive
                    - name: display
                      description: The display name of the coding.
                      exclude_in: create, update
                      type: string
                      enum_options: 
                        - value: Active
                        - value: Inactive
                - name: text
                  description: Plain text representation of the concept.
                  exclude_in: create, update
                  type: string
                  enum_options: 
                    - value: Active
                    - value: Inactive
          - name: verificationStatus
            required_in: create, update
            description: >-
              Assertion about certainty associated with the propensity, or potential risk, of a reaction to the identified substance (including pharmaceutical product).
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
                        - value: http://terminology.hl7.org/CodeSystem/allergyintolerance-verification
                      type: string
                    - name: code
                      description: The code of the verification status.
                      required_in: create, update
                      type: string
                      enum_options: 
                        - value: confirmed
                        - value: entered-in-error
                    - name: display
                      description: The display name of the coding.
                      exclude_in: create, update
                      type: string
                      enum_options: 
                        - value: Confirmed
                        - value: Entered-in-error
                - name: text
                  description: Plain text representation of the concept.
                  exclude_in: create, update
                  type: string
                  enum_options: 
                    - value: Confirmed
                    - value: Entered-in-error
          - name: type
            required_in: create, update
            description: Identification of the underlying physiological mechanism for the reaction risk.
            type: enum [ allergy | intolerance ]
          - name: code
            required_in: create, update
            description_for_all_endpoints: Code that identifies the allergy or intolerance.
            create_description: Supported codings for create interactions are obtained from the [Allergen search endpoint](/api/allergen/#search). At least one coding needs to be an FDB coding. 
            type: json
            attributes:
                - name: coding
                  required_in: create, update
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  attributes: 
                    - name: system
                      required_in: create, update
                      description: The system url of the coding.
                      enum_options: 
                        - value: http://www.fdbhealth.com/
                        - value: http://www.nlm.nih.gov/research/umls/rxnorm
                        - value: http://snomed.info/sct
                      type: string
                    - name: code
                      required_in: create, update
                      description: The code of the allergen.
                      type: string
                    - name: display
                      required_in: create, update
                      description: The display name of the coding.
                      exclude_in: create, update
                      type: string
          - name: patient
            required_in: create, update
            description: Who the sensitivity is for.
            type: json
            attributes:
              - name: reference
                type: string
                required_in: create,update
                description: The reference string of the patient in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: encounter
            description_for_all_endpoints: Encounter when the allergy or intolerance was asserted.
            create_description: >-
                Supply an encounter reference to be able to insert the allergy command into a specific note on the patient's timeline. If no encounter is specified, it will insert into a Data Import note where the DOS is the current time of ingestion.
                <br><br>
                **Canvas does not currently support concurrent creation of resources on the same encounter.** Please avoid issuing concurrent requests that reference the same encounter to this endpoint, or to any other endpoints that reference encounters. It is OK to issue concurrent requests to these endpoints as long as the requests reference different encounters.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the encounter in the format of `"Encounter/086cd6fe-2c94-455d-a53e-6ff1c2652cae"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Encounter").
          - name: onsetDateTime
            description: >-
              When allergy or intolerance was identified.
            type: date
          - name: recordedDate
            exclude_in: create, update
            description: >-
              Date first version of the resource instance was recorded.
            type: datetime
          - name: recorder
            description: >-
              Who recorded the sensitivity. <br><br>In Canvas this will be the originator and committer of the allergy command.
            type: json
            attributes:
              - name: reference
                type: string
                required_in: create,update
                description: The reference string of the practitioner in the format of `"Practitioner/4150cd20de8a470aa570a852859ac87e`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
          - name: lastOccurrence
            description: >-
              Date of last known occurrence of a reaction. <br><br>This date will not appear in the Canvas UI and can only be supplied or read through FHIR.
            type: date
          - name: note
            description: >-
              Additional text not captured in other fields. <br><br>Canvas will display this in the `reaction` field of the allergy command. If there are multiple objects given, they will be separeted by a new line on the UI.
            type: array[json]
            attributes:
                - name: text
                  type: string
                  required_in: create, update
                  description: The annotation - text content. 
          - name: reaction
            description: >-
              Adverse Reaction Events linked to exposure to substance. Only one reaction is supported.
            type: array[json]
            attributes:
                - name: manifestation
                  type: array[json]
                  required_in: create, update
                  description: Clinical symptoms/signs associated with the Event.
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
                              - value: http://terminology.hl7.org/CodeSystem/data-absent-reason
                            type: string
                          - name: code
                            description: The code of the verification status.
                            required_in: create, update
                            type: string
                            enum_options: 
                              - value: unknown
                          - name: display
                            description: The display name of the coding.
                            exclude_in: create, update
                            type: string
                            enum_options: 
                              - value: Unknown
                    - name: text
                      description: Plain text representation of the concept.
                      exclude_in: create, update
                      type: string
                      enum_options: 
                        - value: Unknown
                - name: severity
                  type: string
                  description: Clinical assessment of the severity of the reaction event as a whole.
                  enum_options: 
                    - value: mild
                    - value: moderate
                    - value: severe
        search_parameters:
          - name: _id
            description: The identifier of the AllergyIntolerance.
            type: string
          - name: patient
            description: The patient reference associated to the AllergyIntolerance in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
        endpoints: [create, read, update, search]
        create:
          description: Create an AllergyIntolerance resource.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: allergyintolerance-create-request
          example_response: allergyintolerance-create-response
        read:
          description: Read an AllergyIntolerance resource.
          responses: [200, 401, 403, 404]
          example_request: allergyintolerance-read-request
          example_response: allergyintolerance-read-response
        update:
          description: Update an AllergyIntolerance resource.<br><br>The only type of AllergyIntolerance update interaction that is supported by Canvas is to mark an existing AllergyIntolerance as **entered-in-error** using the `verificationStatus` attribute. No changes to other fields will be processed; however, required fields still need to be supplied.
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: allergyintolerance-update-request
          example_response: allergyintolerance-update-response
        search:
          description: Search for AllergyIntolerance resources.
          responses: [200, 400, 401, 403]
          example_request: allergyintolerance-search-request
          example_response: allergyintolerance-search-response
---

<div id="allergyintolerance-create-request">

  {% tabs allergyintolerance-create-request %}

    {% tab allergyintolerance-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/AllergyIntolerance' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "AllergyIntolerance",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                "code": "active",
                "display": "Active"
            }
        ],
        "text": "Active"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                "code": "confirmed",
                "display": "Confirmed"
            }
        ],
        "text": "Confirmed"
    },
    "type": "allergy",
    "code": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "2-15588",
                "display": "Allergy Medicine"
            }
        ],
        "text": "Allergy Medicine"
    },
    "patient": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "lastOccurrence": "2023-06-17",
    "note": [
        {
            "text": "AllergyIntolerance note"
        }
    ],
    "reaction": [
        {
            "manifestation": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                            "code": "unknown",
                            "display": "Unknown"
                        }
                    ],
                    "text": "Unknown"
                }
            ],
            "severity": "moderate"
        }
    ]
}'
```
    {% endtab %}

    {% tab allergyintolerance-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/AllergyIntolerance"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "AllergyIntolerance",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                "code": "active",
                "display": "Active"
            }
        ],
        "text": "Active"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                "code": "confirmed",
                "display": "Confirmed"
            }
        ],
        "text": "Confirmed"
    },
    "type": "allergy",
    "code": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "2-15588",
                "display": "Allergy Medicine"
            }
        ],
        "text": "Allergy Medicine"
    },
    "patient": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "lastOccurrence": "2023-06-17",
    "note": [
        {
            "text": "AllergyIntolerance note"
        }
    ],
    "reaction": [
        {
            "manifestation": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                            "code": "unknown",
                            "display": "Unknown"
                        }
                    ],
                    "text": "Unknown"
                }
            ],
            "severity": "moderate"
        }
    ]
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="allergyintolerance-create-response">
{% include create-response.html %}
</div>

<div id="allergyintolerance-read-request">
{%  include read-request.html resource_type="AllergyIntolerance" %}
</div>

<div id="allergyintolerance-read-response">

  {% tabs allergyintolerance-read-response %}

    {% tab allergyintolerance-read-response 200 %}
```json
{
    "resourceType": "AllergyIntolerance",
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
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                "code": "active",
                "display": "Active"
            }
        ],
        "text": "Active"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                "code": "confirmed",
                "display": "Confirmed"
            }
        ],
        "text": "Confirmed"
    },
    "type": "allergy",
    "code": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "2-15588",
                "display": "Allergy Medicine"
            }
        ],
        "text": "Allergy Medicine"
    },
    "patient": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "lastOccurrence": "2023-06-17",
    "note": [
        {
            "text": "AllergyIntolerance note"
        }
    ],
    "reaction": [
        {
            "manifestation": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                            "code": "unknown",
                            "display": "Unknown"
                        }
                    ],
                    "text": "Unknown"
                }
            ],
            "severity": "moderate"
        }
    ]
}
```
    {% endtab %}

    {% tab allergyintolerance-read-response 401 %}
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

    {% tab allergyintolerance-read-response 403 %}
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

    {% tab allergyintolerance-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown AllergyIntolerance resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="allergyintolerance-update-request">

  {% tabs allergyintolerance-update-request %}

    {% tab allergyintolerance-update-request curl %}
```shell
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/AllergyIntolerance/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "AllergyIntolerance",
     "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                "code": "active",
                "display": "Active"
            }
        ],
        "text": "Active"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                "code": "entered-in-error",
                "display": "Entered in Error"
            }
        ],
        "text": "Confirmed"
    },
    "type": "allergy",
    "code": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "2-15588",
                "display": "Allergy Medicine"
            }
        ],
        "text": "Allergy Medicine"
    },
    "patient": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "lastOccurrence": "2023-06-17",
    "note": [
        {
            "text": "AllergyIntolerance note"
        }
    ],
    "reaction": [
        {
            "manifestation": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                            "code": "unknown",
                            "display": "Unknown"
                        }
                    ],
                    "text": "Unknown"
                }
            ],
            "severity": "moderate"
        }
    ]
}'
```
    {% endtab %}

    {% tab allergyintolerance-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/AllergyIntolerance/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "AllergyIntolerance",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                "code": "active",
                "display": "Active"
            }
        ],
        "text": "Active"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                "code": "entered-in-error",
                "display": "Entered in Error"
            }
        ],
        "text": "Confirmed"
    },
    "type": "allergy",
    "code": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "2-15588",
                "display": "Allergy Medicine"
            }
        ],
        "text": "Allergy Medicine"
    },
    "patient": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "lastOccurrence": "2023-06-17",
    "note": [
        {
            "text": "AllergyIntolerance note"
        }
    ],
    "reaction": [
        {
            "manifestation": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                            "code": "unknown",
                            "display": "Unknown"
                        }
                    ],
                    "text": "Unknown"
                }
            ],
            "severity": "moderate"
        }
    ]
}
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="allergyintolerance-update-response">
{% include update-response.html resource_type="AllergyIntolerance" %}
</div>

<div id="allergyintolerance-search-request">
{% include search-request.html resource_type="AllergyIntolerance" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="allergyintolerance-search-response">

  {% tabs allergyintolerance-search-response %}

    {% tab allergyintolerance-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/AllergyIntolerance?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/AllergyIntolerance?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/AllergyIntolerance?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "AllergyIntolerance",
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
                            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
                },
                "verificationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                            "code": "confirmed",
                            "display": "Confirmed"
                        }
                    ],
                    "text": "Confirmed"
                },
                "type": "allergy",
                "code": {
                    "coding": [
                        {
                            "system": "http://www.fdbhealth.com/",
                            "code": "2-15588",
                            "display": "Allergy Medicine"
                        }
                    ],
                    "text": "Allergy Medicine"
                },
                "patient": {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
                },
                "encounter": {
                    "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
                },
                "onsetDateTime": "2023-06-15",
                "recorder": {
                    "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
                },
                "lastOccurrence": "2023-06-17",
                "note": [
                    {
                        "text": "AllergyIntolerance note"
                    }
                ],
                "reaction": [
                    {
                        "manifestation": [
                            {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                                        "code": "unknown",
                                        "display": "Unknown"
                                    }
                                ],
                                "text": "Unknown"
                            }
                        ],
                        "severity": "moderate"
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab allergyintolerance-search-response 400 %}
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

    {% tab allergyintolerance-search-response 401 %}
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

    {% tab allergyintolerance-search-response 403 %}
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
