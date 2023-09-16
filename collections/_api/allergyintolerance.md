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
        attributes:
          - name: id
            description: >-
              The identifier of the AllergyIntolerance
            type: string
          - name: clinicalStatus
            description: >-
              The clinical status of the allergy or intolerance<br><br>Supported codes for create interactions are: **active**, **inactive**
            type: json
          - name: verificationStatus
            description: >-
              Assertion about certainty associated with the propensity, or potential risk, of a reaction to the identified substance (including pharmaceutical product)<br><br>Supported codes for create interactions are: **confirmed**, **entered-in-error**
            type: json
          - name: type
            description: >-
              Identification of the underlying physiological mechanism for the reaction risk<br><br>Supported codes for create interactions are: **allergy**, **intolerance**
            type: string
          - name: code
            description: >-
              Code that identifies the allergy or intolerance<br><br>Supported codings for create interactions are obtained from the Allergen search endpoint.
            type: json
          - name: patient
            description: >-
              Who the sensitivity is for
            type: json
          - name: encounter
            description: >-
              Encounter when the allergy or intolerance was asserted
            type: json
          - name: onsetDateTime
            description: >-
              When allergy or intolerance was identified
            type: date
          - name: recordedDate
            description: >-
              Date first version of the resource instance was recorded
            type: datetime
          - name: recorder
            description: >-
              Who recorded the sensitivity
            type: json
          - name: lastOccurrence
            description: >-
              Date of last known occurrence of a reaction
            type: date
          - name: note
            description: >-
              Additional text not captured in other fields
            type: array[json]
          - name: reaction
            description: >-
              Adverse Reaction Events linked to exposure to substance<br><br>Supported severity codes for create interactions are: **mild**, **moderate**, **severe**
            type: array[json]
        search_parameters:
          - name: _id
            description: The identifier of the AllergyIntolerance
            type: string
          - name: patient
            description: Who the sensitivity is for
            type: string
        endpoints: [create, read, update, search]
        create:
          description: Create an AllergyIntolerance resource.<br><br>Exactly one FDB coding is required in the `code` field. FDB codings can be obtained from the search endpoint for the (Allergen resource, which is a custom Canvas FHIR resource.<br><br>If `encounter` is provided, the AllergyIntolerance will be added to existing encounter (note). If it is not provided, a new data import note will be created.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: allergyintolerance-create-request
          example_response: allergyintolerance-create-response
        read:
          description: Read an AllergyIntolerance resource.
          responses: [200, 401, 403, 404]
          example_request: allergyintolerance-read-request
          example_response: allergyintolerance-read-response
        update:
          description: Update an AllergyIntolerance resource.<br><br>The only type of AllergyIntolerance update interaction that is supported by Canvas is to mark an existing AllergyIntolerance as **entered-in-error**. No changes to other fields will be processed.
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
     --url https://fumage-example.canvasmedical.com/AllergyIntolerance \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "AllergyIntolerance",
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
{% include create_response.html %}
</div>

<div id="allergyintolerance-read-request">

  {% tabs allergyintolerance-read-request %}

    {% tab allergyintolerance-read-request curl %}
```shell
curl --request GET \
     --url https://fumage-example.canvasmedical.com/AllergyIntolerance/<id>\
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
    {% endtab %}

    {% tab allergyintolerance-read-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/AllergyIntolerance/<id>"

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

<div id="allergyintolerance-read-response">

  {% tabs allergyintolerance-read-response %}

    {% tab allergyintolerance-read-response 200 %}
```json
{
    "resourceType": "AllergyIntolerance",
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
        "text": "Unknown AllergyIntolerance resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
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
     --url https://fumage-example.canvasmedical.com/AllergyIntolerance/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "AllergyIntolerance",
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

  {% tabs allergyintolerance-update-response %}

    {% tab allergyintolerance-update-response 200 %}
```json
null
```
    {% endtab %}

    {% tab allergyintolerance-update-response 400 %}
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

    {% tab allergyintolerance-update-response 401 %}
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

    {% tab allergyintolerance-update-response 403 %}
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

    {% tab allergyintolerance-update-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown AllergyIntolerance resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

    {% tab allergyintolerance-update-response 405 %}
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

    {% tab allergyintolerance-update-response 412 %}
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

    {% tab allergyintolerance-update-response 422 %}
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

<div id="allergyintolerance-search-request">

  {% tabs allergyintolerance-search-request %}

    {% tab allergyintolerance-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/AllergyIntolerance?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0 \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
    {% endtab %}

    {% tab allergyintolerance-search-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/AllergyIntolerance?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0"

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

<div id="allergyintolerance-search-response">

  {% tabs allergyintolerance-search-response %}

    {% tab allergyintolerance-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
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
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "AllergyIntolerance",
                "clinicalStatus":
                {
                    "coding":
                    [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
                },
                "verificationStatus":
                {
                    "coding":
                    [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                            "code": "confirmed",
                            "display": "Confirmed"
                        }
                    ],
                    "text": "Confirmed"
                },
                "type": "allergy",
                "code":
                {
                    "coding":
                    [
                        {
                            "system": "http://www.fdbhealth.com/",
                            "code": "2-15588",
                            "display": "Allergy Medicine"
                        }
                    ],
                    "text": "Allergy Medicine"
                },
                "patient":
                {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
                },
                "encounter":
                {
                    "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
                },
                "onsetDateTime": "2023-06-15",
                "recorder":
                {
                    "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
                },
                "lastOccurrence": "2023-06-17",
                "note":
                [
                    {
                        "text": "AllergyIntolerance note"
                    }
                ],
                "reaction":
                [
                    {
                        "manifestation":
                        [
                            {
                                "coding":
                                [
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
