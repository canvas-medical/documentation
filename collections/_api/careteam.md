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
          See our Zendesk [article](https://canvas-medical.zendesk.com/hc/en-us/articles/4409741845011-Care-Teams) for information about setting up Care Teams and Care Team Roles in Canvas.
        attributes:
          - name: id
            description: >-
              The identifier of the CareTeam<br><br>
              The default behavior is to return all active care team memberships for the patient. To return care team members of a different status, add `.status` at the end of the ID. Example: **3e72c07b5aac4dc5929948f82c9afdfd.inactive**
            type: string
          - name: status
            description: >-
              The current state of the care team<br><br>Supported codes for update interactions are: **proposed**, **active**, **suspended**, **inactive**
            type: string
          - name: name
            description: Name of the team, such as crisis assessment team
            type: string
          - name: subject
            description: Who care team is for
            type: json
          - name: participant
            description: >-
              Members of the team<br><br>
              Canvas only allows practitioners to be members of a patient CareTeam. A practitioner can only have one role on a CareTeam, and only one practitioner can have a given role on a CareTeam.
            type: array[json]
        search_parameters:
          - name: participant
            description: >-
              Who is involved<br><br>Supported reference types: <b>Practitioner</b>
            type: string
          - name: patient
            description: Who care team is for	
            type: string
          - name: status
            description: The current state of the care team	
            type: string
        endpoints: [read, update, search]
        read:
          description: Read a CareTeam resource.
          responses: [200, 401, 403, 404]
          example_request: careteam-read-request
          example_response: careteam-read-response
        update:
          description: >-
            Update a CareTeam resource.<br><br>
            The CareTeam update endpoint acts as an upsert, so there is no CareTeam `create` endpoint.<br><br>
            **If-Unmodified-Since Header**:<br><br>
            Due to a legacy design detail with the CareTeam implementation, there is a specific condition under which inclusion of this header will not produce expected results. In the case where all members of a CareTeam are removed through the Canvas user interface (i.e. not through the FHIR API), the last modified date for the CareTeam will be equal to the last modified date of the patient record until another member is added to the CareTeam.<br><br>
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
    "subject":
    {
        "reference": "Patient/example",
        "type": "Patient",
        "display": "Amy V. Shaw"
    },
    "participant":
    [
        {
            "role":
            [
                {
                    "coding":
                    [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "17561000",
                            "display": "Cardiologist"
                        }
                    ]
                }
            ],
            "member":
            {
                "reference": "Practitioner/c2ff4546548e46ab8959af887b563eab",
                "display": "Ronald Bone, MD"
            }
        },
        {
            "role":
            [
                {
                    "coding":
                    [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "453231000124104",
                            "display": "Primary care provider"
                        }
                    ]
                }
            ],
            "member":
            {
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
     --url https://fumage-example.canvasmedical.com/CareTeam/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "CareTeam",
    "id": "8ab7cc3c86f54723ba267baf1f906ec7",
    "status": "active",
    "name": "Care Team for Amy V. Shaw",
    "subject":
    {
        "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
        "type": "Patient",
        "display": "Amy V. Shaw"
    },
    "participant":
    [
        {
            "role":
            [
                {
                    "coding":
                    [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "17561000",
                            "display": "Cardiologist"
                        }
                    ]
                }
            ],
            "member":
            {
                "reference": "Practitioner/c2ff4546548e46ab8959af887b563eab",
                "display": "Ronald Bone, MD"
            }
        },
        {
            "role":
            [
                {
                    "coding":
                    [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "453231000124104",
                            "display": "Primary care provider"
                        }
                    ]
                }
            ],
            "member":
            {
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
    "subject":
    {
        "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
        "type": "Patient",
        "display": "Amy V. Shaw"
    },
    "participant":
    [
        {
            "role":
            [
                {
                    "coding":
                    [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "17561000",
                            "display": "Cardiologist"
                        }
                    ]
                }
            ],
            "member":
            {
                "reference": "Practitioner/c2ff4546548e46ab8959af887b563eab",
                "display": "Ronald Bone, MD"
            }
        },
        {
            "role":
            [
                {
                    "coding":
                    [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "453231000124104",
                            "display": "Primary care provider"
                        }
                    ]
                }
            ],
            "member":
            {
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
{% include search-request.html resource_type="AllergyIntolerance" search_string="patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="careteam-search-response">

  {% tabs careteam-search-response %}

    {% tab careteam-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
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
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "CareTeam",
                "id": "8ab7cc3c86f54723ba267baf1f906ec7",
                "status": "active",
                "name": "Care Team for Amy V. Shaw",
                "subject":
                {
                    "reference": "Patient/example",
                    "type": "Patient",
                    "display": "Amy V. Shaw"
                },
                "participant":
                [
                    {
                        "role":
                        [
                            {
                                "coding":
                                [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "17561000",
                                        "display": "Cardiologist"
                                    }
                                ]
                            }
                        ],
                        "member":
                        {
                            "reference": "Practitioner/c2ff4546548e46ab8959af887b563eab",
                            "display": "Ronald Bone, MD"
                        }
                    },
                    {
                        "role":
                        [
                            {
                                "coding":
                                [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "453231000124104",
                                        "display": "Primary care provider"
                                    }
                                ]
                            }
                        ],
                        "member":
                        {
                            "reference": "Practitioner/fc87cbb2525f4c5eb50294f620c7a15e",
                            "display": "Kathy Fielding, MD"
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
