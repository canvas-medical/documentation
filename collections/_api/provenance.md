---
title: Provenance
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Provenance
        article: "a"
        description: >-
          Provenance of a resource is a record that describes entities and processes involved in producing and delivering or otherwise influencing that resource. Provenance provides a critical foundation for assessing authenticity, enabling trust, and allowing reproducibility. Provenance assertions are a form of contextual metadata and can themselves become important records with their own provenance. Provenance statement indicates clinical significance in terms of confidence in authenticity, reliability, and trustworthiness, integrity, and stage in lifecycle (e.g. Document Completion - has the artifact been legally authenticated), all of which may impact security, privacy, and trust policies.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-provenance.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-provenance.html)
          <br><br>In Canvas a Provenance record is created each time the following data types are create or updated in the Canvas database: 

            - AllergyIntolerance
            - CarePlan
            - CareTeamMembership
            - Condition
            - ConsolidatedImmunization
            - Device
            - DiagnosticReport
            - DocumentReference
            - Goal
            - Observation
            - Patient
            - Prescription
            - Procedure
            - UpdateGoal
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the Provenance.
            type: string
          - name: target
            description: Target Reference(s)
            type: array[json]
            attributes:
                - name: reference
                  type: string
                  description: The reference string of the target in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Patient").
                  enum_options:
                    - value: AllergyIntolerance
                    - value: CarePlan
                    - value: CareTeam
                    - value: Condition
                    - value: Immunization
                    - value: Device
                    - value: DiagnosticReport
                    - value: DocumentReference
                    - value: Goal
                    - value: Observation
                    - value: Organization
                    - value: Patient
                    - value: MedicationRequest
                    - value: Procedure
                    - value: Practitioner
                - name: display
                  type: string
                  description: Text alternative for the resource.
          - name: recorded
            description: When the activity was recorded / updated.
            type: datetime
          - name: location
            type: json
            description: Where the activity occurred, if relevant. Currently, this will always appear as absent data.
            attributes:
                - name: extension
                  type: array[json]
                  attributes:
                    - name: url
                      type: string
                      enum_options: 
                        - value: http://hl7.org/fhir/StructureDefinition/data-absent-reason 
                    - name: valueCode
                      type: string
                      enum_options: 
                        - value: unsupported
          - name: activity
            description: Activity that occurred. Canvas supports a provenance of the record being either created or updated.
            type: json
            attributes:
                - name: coding
                  description: Code defined by a terminology system.
                  type: array[json]
                  required_in: create, update
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      required_in: create, update
                      enum_options: 
                        - value: http://terminology.hl7.org/CodeSystem/v3-DataOperation
                      type: string
                    - name: code
                      description: The code of the activity.
                      required_in: create, update
                      type: string
                      enum_options: 
                        - value: CREATE
                        - value: UPDATE
          - name: agent
            description: Actor involved. <br><br>The agent will be populated by the committer or originator in Canvas as the auther. If neither is found, it will default to the Canvas Organization as the composer. 
            type: array[json]
            attributes:
                - name: type
                  type: json
                  description:
                  attributes:
                      - name: coding
                        description: Code defined by a terminology system.
                        type: array[json]
                        attributes: 
                          - name: system
                            description: The system url of the coding.
                            enum_options: 
                              - value: http://hl7.org/fhir/us/core/CodeSystem/us-core-provenance-participant-type
                              - value: http://terminology.hl7.org/CodeSystem/provenance-participant-type
                            type: string
                          - name: code
                            description: The code.
                            type: string
                            enum_options: 
                              - value: author
                              - value: composer
                          - name: display
                            description: The display name of the coding.
                            type: string
                            enum_options: 
                                - value: Author
                                - value: Composer
                - name: who
                  type: json
                  attributes:
                    - name: reference
                      type: string
                      description: The reference string of who the agent is in the format of `"Practitioner/a39cafb9d1b445be95a2e2548e12a787"`. If the reference is `Organization/00000000-0000-0000-0002-000000000000`, a committer or originator couldn't be found in Canvas as the agent, so Canvas Medical is the default agent.
                    - name: type
                      type: string
                      description: Type the reference refers to (e.g. "Practitioner", "Organization").
                    - name: display
                      type: string
                      description: Text alternative for the resource.
                - name: onBehalfOf
                  type: json
                  description: Who the agent is representing. This will always be the Canvas Medical Organization. 
                  attributes:
                    - name: reference
                      type: string
                      description: The reference string of who the organization is in the format of `"Organization/00000000-0000-0000-0002-000000000000"`.
                    - name: type
                      type: string
                      description: Type the reference refers to (e.g. "Organization").
        search_parameters:
          - name: _id
            description: The identifier of the Provenance.
            type: string
          - name: agent
            description: Search by the agent of the Provenance record in the format `"Practitioner/a39cafb9d1b445be95a2e2548e12a787"` or `Organization/00000000-0000-0000-0002-000000000000`.
            type: string
          - name: patient
            description: Search by records where the target is a specific patient in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
          - name: target
            description: Search by records where the target is a specific patient or observation in the format `Patient/a39cafb9d1b445be95a2e2548e12a787` or `"Observation/920807d3-034b-4423-a65b-980068cb4bd1"`.
            type: string
        endpoints: [read, search]
        read:
          description: Read a Provenance resource.
          responses: [200, 401, 403, 404]
          example_request: provenance-read-request
          example_response: provenance-read-response
        search:
          description: Search for Provenance resources.
          responses: [200, 400, 401, 403]
          example_request: provenance-search-request
          example_response: provenance-search-response
---

<div id="provenance-read-request">
{%  include read-request.html resource_type="Provenance" %}
</div>

<div id="provenance-read-response">

  {% tabs provenance-read-response %}

    {% tab provenance-read-response 200 %}
```json
{
    "resourceType": "Provenance",
    "id": "db1631ed-bcd3-4e43-84a1-7e507e8aa44c",
    "target": [
        {
            "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
            "type": "Patient"
        }
    ],
    "recorded": "2023-09-18T14:42:14.981528+00:00",
    "activity": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                "code": "CREATE"
            }
        ]
    },
    "agent": [
        {
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type",
                        "code": "composer",
                        "display": "Composer"
                    }
                ]
            },
            "who": {
                "reference": "Organization/00000000-0000-0000-0002-000000000000",
                "type": "Organization",
                "display": "Canvas Medical"
            },
            "onBehalfOf": {
                "reference": "Organization/00000000-0000-0000-0002-000000000000",
                "type": "Organization"
            }
        }
    ]
}
```
    {% endtab %}

    {% tab provenance-read-response 401 %}
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

    {% tab provenance-read-response 403 %}
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

    {% tab provenance-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Provenance resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="provenance-search-request">
{% include search-request.html resource_type="Provenance" search_string="target=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="provenance-search-response">

  {% tabs provenance-search-response %}

    {% tab provenance-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Provenance?target=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Provenance?target=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Provenance?target=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Provenance",
                "id": "db1631ed-bcd3-4e43-84a1-7e507e8aa44c",
                "target": [
                    {
                        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
                        "type": "Patient"
                    }
                ],
                "recorded": "2023-09-18T14:42:14.981528+00:00",
                "activity": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                            "code": "CREATE"
                        }
                    ]
                },
                "agent": [
                    {
                        "type": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type",
                                    "code": "composer",
                                    "display": "Composer"
                                }
                            ]
                        },
                        "who": {
                            "reference": "Organization/00000000-0000-0000-0002-000000000000",
                            "type": "Organization",
                            "display": "Canvas Medical"
                        },
                        "onBehalfOf": {
                            "reference": "Organization/00000000-0000-0000-0002-000000000000",
                            "type": "Organization"
                        }
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab provenance-search-response 400 %}
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

    {% tab provenance-search-response 401 %}
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

    {% tab provenance-search-response 403 %}
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
