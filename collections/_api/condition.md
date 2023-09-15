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
          - name: id
            description: >-
              The identifier of the Condition
            type: string
          - name: text
            description: Text summary of the Condition, for human interpretation
            type: json
          - name: clinicalStatus
            description: The clinical status of the condition.
            type: json
          - name: verificationStatus
            description: The verification status to support the clinical status of the condition.
            type: json
          - name: category
            description: A category assigned to the condition.
            type: array[json]
          - name: code
            description: Identification of the condition, problem or diagnosis.
            type: json
          - name: subject
            description: Who has the condition
            type: json
          - name: encounter
            description: Encounter created as part of
            type: json
          - name: onsetDateTime
            description: Estimated or actual date
            type: date
          - name: abatementDateTime
            description: When in resolution/remission
            type: date
          - name: recordedDate
            description: Date-time record was first recorded
            type: datetime
          - name: recorder
            description: Who recorded the condition
            type: json
          - name: note
            description: Additional information about the Condition
            type: array[json]
        search_parameters:
          - name: _id
            description: The identifier of the Condition
            type: string
          - name: patient
            description: Who has the condition
            type: string
        endpoints: [create, read, update, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          description: >-
            Create a Condition resource.<br><br>
            This endpoint does not prevent duplicates in the record. **Canvas recommends performing a search prior to adding a new condition** to confirm whether the condition has already been created for the patient.<br><br>
            If `clinicalStatus` is **active**, the Condition will be added as a `Diagnose` command. If it is not **active**, the Condition will be added as a `Past Medical History` command.<br><br>
            If `encounter` is provided, the Condition will be added to existing encounter (note). If it is not provided, a new data import note will be created.
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
            The only type of Condition update interaction that is supported by Canvas is to mark an existing Condition as **entered-in-error**. No changes to other fields will be processed.
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
     --url https://fumage-example.canvasmedical.com/Condition \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Condition",
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
  {% tabs condition-create-response %}
    {% tab condition-create-response 201 %}
```json
null
```
    {% endtab %}

    {% tab condition-create-response 400 %}
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

    {% tab condition-create-response 401 %}
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

    {% tab condition-create-response 403 %}
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

    {% tab condition-create-response 405 %}
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

    {% tab condition-create-response 412 %}
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

    {% tab condition-create-response 422 %}
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

<div id="condition-read-request">

  {% tabs condition-read-request %}

    {% tab condition-read-request curl %}
```shell
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Condition/<id>\
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
    {% endtab %}

    {% tab condition-read-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Condition/<id>"

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

<div id="condition-read-response">

  {% tabs condition-read-response %}

    {% tab condition-read-response 200 %}
```json
{
    "resourceType": "Condition",
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
        "text": "Unknown Condition resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
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
     --url https://fumage-example.canvasmedical.com/Condition/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Condition",
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

  {% tabs condition-update-response %}

    {% tab condition-update-response 200 %}
```json
null
```
    {% endtab %}

    {% tab condition-update-response 400 %}
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

    {% tab condition-update-response 401 %}
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

    {% tab condition-update-response 403 %}
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

    {% tab condition-update-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Condition resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

    {% tab condition-update-response 405 %}
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

    {% tab condition-update-response 412 %}
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

    {% tab condition-update-response 422 %}
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

<div id="condition-search-request">

  {% tabs condition-search-request %}

    {% tab condition-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Condition?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0 \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
    {% endtab %}

    {% tab condition-search-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Condition?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0"

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

<div id="condition-search-response">

  {% tabs condition-search-response %}

    {% tab condition-search-response 200 %}
```json
{
    "link":
    [
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
    "entry":
    [
        {
            "resource":
            {
                "recordedDate": "2023-06-18T15:00:00-04:00",
                "note":
                [
                    {
                        "text": "Condition note"
                    }
                ],
                "category":
                [
                    {
                        "coding":
                        [
                            {
                                "display": "Encounter Diagnosis",
                                "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                                "code": "encounter-diagnosis"
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
                            "display": "Parachutist entangled in object, sequela",
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "V97.21XS"
                        }
                    ],
                    "text": "Parachutist entangled in object, sequela"
                },
                "id": "00a6a9f1-ffdb-4cf8-8e11-f2d6459dec3f",
                "clinicalStatus":
                {
                    "coding":
                    [
                        {
                            "display": "Resolved",
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "resolved"
                        }
                    ],
                    "text": "Resolved"
                },
                "encounter":
                {
                    "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
                },
                "onsetDateTime": "2023-06-15",
                "abatementDateTime": "2023-06-17",
                "verificationStatus":
                {
                    "coding":
                    [
                        {
                            "display": "Confirmed",
                            "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                            "code": "confirmed"
                        }
                    ],
                    "text": "Confirmed"
                },
                "subject":
                {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
                },
                "resourceType": "Condition",
                "recorder":
                {
                    "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
                }
            }
        }
    ],
    "resourceType": "Bundle",
    "total": 1,
    "type": "searchset"
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
