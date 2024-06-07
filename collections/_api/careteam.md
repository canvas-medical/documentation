---
title: CareTeam
sections:
  - type: section
    blocks:
      - type: apidoc
        name: CareTeam
        article: "a"
        description: >-
          The Care Team includes all the people and organizations who plan to participate in the coordination and delivery of care for a patient.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-careteam.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-careteam.html)<br><br>
          All patients in Canvas have a CareTeam by default. The identifier for the CareTeam resource for a patient is the same as the patient identifier.
          <br><br>
          See our [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4409741845011-Care-Teams) for information about setting up Care Teams and Care Team Roles in Canvas.
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            required_in: update
            description: The identifier of the CareTeam.
            type: string
          - name: status
            exclude_in: update
            description: >-
              The current state of the care team.
            enum_options:
                - value: proposed
                - value: active
                - value: suspended
                - value: inactive
                - value: entered-in-error
            type: string
          - name: name
            exclude_in: update
            description: Name of the team. <br><br> This will always be set to `Care Team for <patient_last_name>, <patient_first_name>`
            type: string
          - name: subject
            description: Who care team is for.
            type: json
            attributes:
              - name: reference
                type: string
                required_in: update
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
              - name: display
                type: string
                exclude_in: update
                description: Display name of patient in the format `<patient_last_name>, <patient_first_name>`
          - name: participant
            description_for_all_endpoints: >-
              Members of the team.<br><br>
              Canvas only allows practitioners to be members of a patient CareTeam. A practitioner can only have one role on a CareTeam, and only one practitioner can have a given role on a CareTeam. <br><br>
            update_description: >-
              If `participant` is omitted or sent as an empty list, Canvas will inactivate any care team participants it finds for the given subject.
            type: array[json]
            attributes:
                - name: extension
                  type: array[json]
                  read_and_search_description: Canvas uses an extension to display whether a specific participant in a care team is the lead or not.
                  update_description: Canvas supports the ability to mark a participant of a care team as the lead using a specific extension. <br><br>If this extension is omitted, any current care team lead designated in Canvas will stay as the lead. 
                  attributes:
                    - name: url
                      type: string
                      required_in: update
                      description: Reference that defines the content of this object.
                      enum_options:
                      - value: http://schemas.canvasmedical.com/fhir/extensions/careteam-lead
                    - name: valueBoolean
                      type: boolean
                      required_in: update
                      description: Value of extension. If the value is set to `True`, it indicates the specific participant as the lead for this care team. Only one active participant can be the lead of a care team.
                - name: role
                  type: array[json]
                  description: Type of involvement
                  required_in: update
                  attributes:
                    - name: coding
                      required_in: update
                      description: Code defined by a terminology system. <br><br>Needs to match a Care Team Role that is defined in the Settings of the Canvas instance.
                      type: array[json]
                      attributes: 
                        - name: system
                          required_in: update
                          description: The system url of the coding.
                          type: string
                        - name: code
                          required_in: update
                          description: The code of the care team role.
                          type: string
                        - name: display
                          required_in: update
                          description: The display name of the coding.
                          type: string
                - name: member
                  type: json
                  required_in: update
                  description: Who is involved.
                  attributes:
                    - name: reference
                      type: string
                      required_in: update
                      description: The reference string of the member in the format of `"Practitioner/ed1e304acdb847148338c6b0596d93fd"`. 
                    - name: type
                      type: string
                      description: Type the reference refers to (e.g. "Practitioner").
        search_parameters:
          - name: participant
            description: >-
              Who is involved. <br><br>Search to find all patient care teams that with a specific Practitioner member. Use the format `"Practitioner/ed1e304acdb847148338c6b0596d93fd"`
            type: string
          - name: patient
            description: Search for a specific patient's care team in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
          - name: status
            description: Search for care team participants of a patient by a specific status. If a status is not specified to search by, note the `id` in the response batch will end in `.status` for all care teams that are not active statuses.
            type: string
            search_options:
                - value: proposed
                - value: active
                - value: suspended
                - value: inactive
                - value: entered-in-error
        endpoints: [read, update, search]
        read:
          description: Read a CareTeam resource.
          additional_path_parameter_description: The default behavior is to return all active care team participants for the patient. To return care team participants of a different status, add `.status` at the end of the ID (e.g `CareTeam/3e72c07b5aac4dc5929948f82c9afdfd.inactive`).
          responses: [200, 401, 403, 404]
          example_request: careteam-read-request
          example_response: careteam-read-response
        update:
          description: >-
            Update a CareTeam resource.<br><br>
            The CareTeam update endpoint acts as an upsert, so there is no CareTeam `create` endpoint. Any participants included in the payload will be the patient's active care team participants. While any participants no longer included in the payload will be marked as `inactive`.
            <br><br>
            **If-Unmodified-Since Header**:<br>
            Due to a legacy design detail with the CareTeam implementation, there is a specific condition under which inclusion of this header will not produce expected results. In the case where all participants of a CareTeam are removed through the Canvas user interface (i.e. not through the FHIR API), the last modified date for the CareTeam will be equal to the last modified date of the patient record until another participant is added to the CareTeam.<br><br>
            More information about the If-Unmodified-Since header can be found in the [Conditional Requests documentation](/api/conditional-requests/).
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: careteam-update-request
          example_response: careteam-update-response
        search:
          description: Search for CareTeam resources.
          responses: [200, 400, 401, 403]
          example_request: careteam-search-request
          example_response: careteam-search-response
---

<div id="careteam-read-request">
{% include read-request.html resource_type="CareTeam" %}
</div>

<div id="careteam-read-response">

  {% tabs careteam-read-response %}

    {% tab careteam-read-response 200 %}
```json
{
    "resourceType": "CareTeam",
    "id": "8ab7cc3c86f54723ba267baf1f906ec7",
    "status": "active",
    "name": "Care Team for Amy V. Shaw",
    "subject": {
        "reference": "Patient/example",
        "type": "Patient",
        "display": "Amy V. Shaw"
    },
    "participant": [
        {
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/careteam-lead",
                    "valueBoolean": true
                }
            ],
            "role": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "17561000",
                            "display": "Cardiologist"
                        }
                    ]
                }
            ],
            "member": {
                "reference": "Practitioner/c2ff4546548e46ab8959af887b563eab",
                "display": "Ronald Bone, MD"
            }
        },
        {
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/careteam-lead",
                    "valueBoolean": false
                }
            ],
            "role": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "453231000124104",
                            "display": "Primary care provider"
                        }
                    ]
                }
            ],
            "member": {
                "reference": "Practitioner/fc87cbb2525f4c5eb50294f620c7a15e",
                "display": "Kathy Fielding, MD"
            }
        }
    ]
}
```
    {% endtab %}

    {% tab careteam-read-response 401 %}
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

    {% tab careteam-read-response 403 %}
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

    {% tab careteam-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown CareTeam resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="careteam-update-request">

  {% tabs careteam-update-request %}

    {% tab careteam-update-request curl %}
```shell
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/CareTeam/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "CareTeam",
    "id": "8ab7cc3c86f54723ba267baf1f906ec7",
    "status": "active",
    "name": "Care Team for Amy V. Shaw",
    "subject": {
        "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
        "type": "Patient",
        "display": "Amy V. Shaw"
    },
    "participant": [
        {
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/careteam-lead",
                    "valueBoolean": true
                }
            ],
            "role": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "17561000",
                            "display": "Cardiologist"
                        }
                    ]
                }
            ],
            "member": {
                "reference": "Practitioner/c2ff4546548e46ab8959af887b563eab",
                "display": "Ronald Bone, MD"
            }
        },
        {
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/careteam-lead",
                    "valueBoolean": false
                }
            ],
            "role": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "453231000124104",
                            "display": "Primary care provider"
                        }
                    ]
                }
            ],
            "member": {
                "reference": "Practitioner/fc87cbb2525f4c5eb50294f620c7a15e",
                "display": "Kathy Fielding, MD"
            }
        }
    ]
}'
```
    {% endtab %}

    {% tab careteam-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/CareTeam/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "CareTeam",
    "id": "8ab7cc3c86f54723ba267baf1f906ec7",
    "status": "active",
    "name": "Care Team for Amy V. Shaw",
    "subject": {
        "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
        "type": "Patient",
        "display": "Amy V. Shaw"
    },
    "participant": [
        {
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/careteam-lead",
                    "valueBoolean": True
                }
            ],
            "role": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "17561000",
                            "display": "Cardiologist"
                        }
                    ]
                }
            ],
            "member": {
                "reference": "Practitioner/c2ff4546548e46ab8959af887b563eab",
                "display": "Ronald Bone, MD"
            }
        },
        {
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/careteam-lead",
                    "valueBoolean": False
                }
            ],
            "role": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "453231000124104",
                            "display": "Primary care provider"
                        }
                    ]
                }
            ],
            "member": {
                "reference": "Practitioner/fc87cbb2525f4c5eb50294f620c7a15e",
                "display": "Kathy Fielding, MD"
            }
        }
    ]
}
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="careteam-update-response">
{% include update-response.html resource_type="CareTeam" %}
</div>

<div id="careteam-search-request">
{% include search-request.html resource_type="CareTeam" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="careteam-search-response">

  {% tabs careteam-search-response %}

    {% tab careteam-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/CareTeam?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/CareTeam?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/CareTeam?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "CareTeam",
                "id": "8ab7cc3c86f54723ba267baf1f906ec7",
                "status": "active",
                "name": "Care Team for Amy V. Shaw",
                "subject": {
                    "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
                    "type": "Patient",
                    "display": "Amy V. Shaw"
                },
                "participant": [
                    {
                        "extension": [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/careteam-lead",
                                "valueBoolean": true
                            }
                        ],
                        "role": [
                            {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "17561000",
                                        "display": "Cardiologist"
                                    }
                                ]
                            }
                        ],
                        "member": {
                            "reference": "Practitioner/c2ff4546548e46ab8959af887b563eab",
                            "display": "Ronald Bone, MD"
                        }
                    },
                    {
                        "extension": [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/careteam-lead",
                                "valueBoolean": false
                            }
                        ],
                        "role": [
                            {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "453231000124104",
                                        "display": "Primary care provider"
                                    }
                                ]
                            }
                        ],
                        "member": {
                            "reference": "Practitioner/fc87cbb2525f4c5eb50294f620c7a15e",
                            "display": "Kathy Fielding, MD"
                        }
                    }
                ]
            }
        }, 
        {
            "resource": {
                "resourceType": "CareTeam",
                "id": "8ab7cc3c86f54723ba267baf1f906ec7.inactive",
                "status": "inactive",
                "name": "Care Team for Amy V. Shaw",
                "subject": {
                    "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
                    "type": "Patient",
                    "display": "Amy V. Shaw"
                },
                "participant": [
                    {
                        "extension": [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/careteam-lead",
                                "valueBoolean": false
                            }
                        ],
                        "role": [
                            {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "17561000",
                                        "display": "Cardiologist"
                                    }
                                ]
                            }
                        ],
                        "member": {
                            "reference": "Practitioner/390769eb976546ceaefe2507effcc665",
                            "type": "Practitioner",
                            "display": "Pat Byrnes"
                        }
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab careteam-search-response 400 %}
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

    {% tab careteam-search-response 401 %}
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

    {% tab careteam-search-response 403 %}
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
