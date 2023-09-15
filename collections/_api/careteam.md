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
          See our Zendesk [article](https://canvas-medical.zendesk.com/hc/en-us/articles/4409741845011-Care-Teams) for information about setting up Care Teams in Canvas.
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
          - name: _id
            description: The identifier of the CareTeam
            type: string
          - name: participant
            description: Who is involved
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

  {% tabs careteam-read-request %}

    {% tab careteam-read-request curl %}
```shell
curl --request GET \
     --url https://fumage-example.canvasmedical.com/CareTeam/<id>\
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
    {% endtab %}

    {% tab careteam-read-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/CareTeam/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}


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
        "text": "Unknown CareTeam resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
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

  {% tabs careteam-update-response %}

    {% tab careteam-update-response 200 %}
```json
null
```
    {% endtab %}

    {% tab careteam-update-response 400 %}
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

    {% tab careteam-update-response 401 %}
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

    {% tab careteam-update-response 403 %}
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

    {% tab careteam-update-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown CareTeam resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

    {% tab careteam-update-response 405 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-supported",
      "details": {
        "text": "Operation is not supported"
      }
    }
  ]
}
```
    {% endtab %}

    {% tab careteam-update-response 412 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "conflict",
      "details": {
        "text": "Resource updated since If-Unmodified-Since date"
      }
    }
  ]
}
```
    {% endtab %}

    {% tab careteam-update-response 422 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "business-rule",
      "details": {
        "text": "Unprocessable entity"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="careteam-search-request">

  {% tabs careteam-search-request %}

    {% tab careteam-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/CareTeam?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0 \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
    {% endtab %}

    {% tab careteam-search-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/CareTeam?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

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







<div id="care-team-read-request">
{% tabs care-team-read-request %}
{% tab care-team-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/CareTeam/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab care-team-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/CareTeam/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="care-team-read-response">
{% tabs care-team-read-response %}
{% tab care-team-read-response 200 %}
```json
{
    "resourceType": "CareTeam",
    "id": "8ab7cc3c86f54723ba267baf1f906ec7",
    "status": "active",
    "name": "Care Team for Testing, Regression",
    "subject": {
        "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
        "type": "Patient",
        "display": "Testing, Regression"
    },
    "participant": [
        {
            "role": [
                {
                    "coding": [
                        {
                            "system": "INTERNAL",
                            "code": "123",
                            "display": "BFF"
                        }
                    ]
                }
            ],
            "member": {
                "reference": "Practitioner/0f0d694324914fb2ad5a1c03428a43ec",
                "type": "Practitioner",
                "display": "Cecilia Orta DO"
            }
        }
    ]
}
```
{% endtab %}
{% tab care-team-read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown CareTeam resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="care-team-search-request">
{% tabs care-team-search-request %}
{% tab care-team-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/CareTeam?patient=Patient%<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab care-team-search-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/CareTeam?patient=Patient%<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="care-team-search-response">
{% tabs care-team-search-response %}
{% tab care-team-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/CareTeam?id=8ab7cc3c86f54723ba267baf1f906ec7&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/CareTeam?id=8ab7cc3c86f54723ba267baf1f906ec7&_count=10&_offset=0"
        },
        {
            "relation": "next",
            "url": "/CareTeam?id=8ab7cc3c86f54723ba267baf1f906ec7&_count=10&_offset=10"
        },
        {
            "relation": "last",
            "url": "/CareTeam?id=8ab7cc3c86f54723ba267baf1f906ec7&_count=10&_offset=1210"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "CareTeam",
                "id": "8ab7cc3c86f54723ba267baf1f906ec7",
                "status": "active",
                "name": "Care Team for Testing, Regression",
                "subject": {
                    "reference": "Patient/8ab7cc3c86f54723ba267baf1f906ec7",
                    "type": "Patient",
                    "display": "Testing, Regression"
                },
                "participant": [
                    {
                        "role": [
                            {
                                "coding": [
                                    {
                                        "system": "INTERNAL",
                                        "code": "123",
                                        "display": "BFF"
                                    }
                                ]
                            }
                        ],
                        "member": {
                            "reference": "Practitioner/0f0d694324914fb2ad5a1c03428a43ec",
                            "type": "Practitioner",
                            "display": "Cecilia Orta DO"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "CareTeam",
                "id": "999f6fd203d24e26ba95b77ffa7827b6",
                "status": "active",
                "name": "Care Team for Koepp, Sandrine E. (Montana)",
                "subject": {
                    "reference": "Patient/999f6fd203d24e26ba95b77ffa7827b6",
                    "type": "Patient",
                    "display": "Koepp, Sandrine E. (Montana)"
                },
                "participant": [
                    {
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
                            "type": "Practitioner",
                            "display": "Saharsh Patel"
                        }
                    },
                    {
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
                            "type": "Practitioner",
                            "display": "Michael Zimmerman DO"
                        }
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab care-team-search-response 400 %}
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


<div id="care-team-update-request">
{% tabs care-team-update-request %}
{% tab care-team-update-request python %}
```sh
import requests

url = "https://fhir-example.canvasmedical.com/CareTeam/<id>"

payload = {
    "resourceType": "CareTeam",
    "participant": [
        {
            "role": [{ "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "17561000",
                            "display": "Cardiologist"
                        }
                    ] }],
            "member": { "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e" }
        },
        {
            "role": [{ "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "453231000124104",
                            "display": "Primary care provider"
                        }
                    ] }],
            "member": { "reference": "Practitioner/2a6cfdb145c8469b9d935fe91f6b0172" }
        }
    ],
    "subject": { "reference": "Patient/3e72c07b5aac4dc5929948f82c9afdfd" }
}
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
{% tab care-team-update-request curl %}
```sh
curl --request PUT \
     --url https://fhir-example.canvasmedical.com/CareTeam/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "CareTeam",
  "participant": [
    {
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
        "reference": "Practitioner/3640cd20de8a470aa570a852859ac87e"
      }
    },
    {
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
        "reference": "Practitioner/2a6cfdb145c8469b9d935fe91f6b0172"
      }
    }
  ],
  "subject": {
    "reference": "Patient/3e72c07b5aac4dc5929948f82c9afdfd"
  }
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="care-team-update-response">
{% tabs care-team-update-response %}
{% tab care-team-update-response 200 %}
```json
null
```
{% endtab %}
{% tab care-team-update-response 400 %}
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

