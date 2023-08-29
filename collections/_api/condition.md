---
title: Condition
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Condition
        article: "a"
        description: >-
          Get information about a location (via Canvas's practice location)
        attributes:
          - name: id
            description: >-
              The identifier of the patient
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: text
            type: json
            attributes:
              - name: status
                type: string
              - name: div
                type: string
          - name: clinicalStatus
            type: json
            attributes:
              - name: coding
                type: string
              - name: text
                type: string
          - name: verificationStatus
            attributes:
              - name: coding
                type: string
              - name: text
                type: string
            type: json
          - name: category
            type: json
            attributes:
              - name: coding
                type: string
                attributes:
                  - name: system
                    type: string
                  - name: code
                    type: string
                  - name: display
                    type: string
              - name: text
                type: string
          - name: code
            type: json
            attributes:
              - name: coding
                type: string
              - name: text
                type: string
          - name: subject
            type: string
          - name: encounter
            type: string
          - name: onsetDateTime
            type: date
          - name: abatementDateTime
            type: date
          - name: recordedDate
            type: date
          - name: recorder
            type: string
          - name: note
            type: text
        search_parameters:
          - name: id
            description: >-
              The identifier of the patient
            type: string
            required: true
          - name: patient
            type: string
          - name: clinicalStatus
            type: string
          - name: verificationStatus
            type: string
          - name: encounter
            type: string
        endpoints: [read, search, create, update]
        read:
          responses: [200, 401, 403, 404]
          example_request: condition-read-request
          example_response: condition-read-response
        search:
          responses: [200, 401, 403]
          example_request: condition-search-request
          example_response: condition-search-response
        create:
          responses: [201, 401, 403]
          example_request: condition-create-request
          example_response: condition-create-response
        update:
          responses: [200, 401, 403]
          example_request: condition-update-request
          example_response: condition-update-response

---
<div id="condition-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
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
{% tab read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Condition/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="condition-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
{
    "resourceType": "Condition",
    "id": "fb70c078-acef-421e-9454-3fb896aa6c5a",
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Headache, unspecified</div>"
    },
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active",
                "display": "Active"
            }
        ],
        "text": "Active"
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
                "system": "http://snomed.info/sct",
                "code": "404684003",
                "display": "Headache, unspecified"
            },
            {
                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                "code": "R519",
                "display": "Headache, unspecified"
            }
        ],
        "text": "Headache, unspecified"
    },
    "subject": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient",
        "display": "Doe, Jane B."
    },
    "encounter": {
        "reference": "Encounter/0a696348-0782-4fa2-b341-214bf2246393",
        "type": "Encounter"
    },
    "recordedDate": "2022-05-12T17:25:22.117888+00:00",
    "recorder": {
        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
        "type": "Practitioner"
    }
}
```
{% endtab %}
{% tab read-response 401 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
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
{% tab read-response 403 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
      "details": {
        "text": "Authorization failed"
      }
    }
  ]
}
```
{% endtab %}
{% tab read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
      "details": {
        "text": "Resource not found"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="condition-search-request">
{% tabs search-request %}
{% tab search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Condition?patient=Patient%2F<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Condition/<pa> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="condition-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 94,
    "link": [
        {
            "relation": "self",
            "url": "/Condition?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&encounter=Encounter%2F0a696348-0782-4fa2-b341-214bf2246393%22&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Condition?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&encounter=Encounter%2F0a696348-0782-4fa2-b341-214bf2246393%22&_count=10&_offset=0"
        },
        {
            "relation": "next",
            "url": "/Condition?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&encounter=Encounter%2F0a696348-0782-4fa2-b341-214bf2246393%22&_count=10&_offset=10"
        },
        {
            "relation": "last",
            "url": "/Condition?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&encounter=Encounter%2F0a696348-0782-4fa2-b341-214bf2246393%22&_count=10&_offset=90"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Condition",
                "id": "fb70c078-acef-421e-9454-3fb896aa6c5a",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Headache, unspecified</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
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
                            "system": "http://snomed.info/sct",
                            "code": "404684003",
                            "display": "Headache, unspecified"
                        },
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "R519",
                            "display": "Headache, unspecified"
                        }
                    ],
                    "text": "Headache, unspecified"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/0a696348-0782-4fa2-b341-214bf2246393",
                    "type": "Encounter"
                },
                "recordedDate": "2022-05-12T17:25:22.117888+00:00",
                "recorder": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "37ac8f32-4b2f-404c-9306-f9b4fd9c3bd3",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Other mixed anxiety disorders</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
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
                            "system": "http://snomed.info/sct",
                            "code": "404684003",
                            "display": "Other mixed anxiety disorders"
                        },
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "F413",
                            "display": "Other mixed anxiety disorders"
                        }
                    ],
                    "text": "Other mixed anxiety disorders"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/aabf2540-15bd-416b-8554-d24050142090",
                    "type": "Encounter"
                },
                "recordedDate": "2022-05-12T17:29:41.185140+00:00",
                "recorder": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "1689dd36-309a-41c1-a49f-d5790938eb23",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Encounter for screening for depression</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
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
                            "system": "http://snomed.info/sct",
                            "code": "404684003",
                            "display": "Encounter for screening for depression"
                        },
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "Z1331",
                            "display": "Encounter for screening for depression"
                        }
                    ],
                    "text": "Encounter for screening for depression"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/53cfeb02-d41b-407b-9ca0-890874ba9c99",
                    "type": "Encounter"
                },
                "recordedDate": "2022-05-12T17:41:35.990431+00:00",
                "recorder": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "f8888eef-7041-4897-96f1-ae67f13febb7",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Charcot's joint, left ankle and foot</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
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
                            "system": "http://snomed.info/sct",
                            "code": "404684003",
                            "display": "Charcot's joint, left ankle and foot"
                        },
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "M14672",
                            "display": "Charcot's joint, left ankle and foot"
                        }
                    ],
                    "text": "Charcot's joint, left ankle and foot"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/9ba174df-a313-4590-8efe-4c9dad8ea717",
                    "type": "Encounter"
                },
                "recordedDate": "2022-05-12T17:42:26.428692+00:00",
                "recorder": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "15d94a55-988c-4086-901e-3b93386f0ce3",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Burn of second degree of chest wall, initial encounter</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
                },
                "verificationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                            "code": "provisional",
                            "display": "Provisional"
                        }
                    ],
                    "text": "Provisional"
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
                            "system": "http://snomed.info/sct",
                            "code": "404684003",
                            "display": "Burn of second degree of chest wall, initial encounter"
                        },
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "T2121XA",
                            "display": "Burn of second degree of chest wall, initial encounter"
                        }
                    ],
                    "text": "Burn of second degree of chest wall, initial encounter"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/9ba174df-a313-4590-8efe-4c9dad8ea717",
                    "type": "Encounter"
                },
                "recordedDate": "2022-05-12T19:06:44.134324+00:00",
                "recorder": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "e8c7fff3-9766-4ffb-82ee-e227ccd2322e",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Multiple sclerosis</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
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
                            "system": "http://snomed.info/sct",
                            "code": "698626001",
                            "display": "Multiple sclerosis"
                        },
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "G35",
                            "display": "Multiple sclerosis"
                        }
                    ],
                    "text": "Multiple sclerosis"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/95405b74-29b3-41b9-8ae5-3e58b65f8aca",
                    "type": "Encounter"
                },
                "recordedDate": "2022-05-23T14:30:47.820087+00:00",
                "recorder": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "7f19cba5-08db-4919-b99d-8c2d84ef0792",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Headache, unspecified</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
                },
                "verificationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                            "code": "provisional",
                            "display": "Provisional"
                        }
                    ],
                    "text": "Provisional"
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
                            "system": "http://snomed.info/sct",
                            "code": "404684003",
                            "display": "Headache, unspecified"
                        },
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "R519",
                            "display": "Headache, unspecified"
                        }
                    ],
                    "text": "Headache, unspecified"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/8f3d11d8-5820-489f-a791-ba957e972082",
                    "type": "Encounter"
                },
                "recordedDate": "2022-05-25T17:56:43.893112+00:00",
                "recorder": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "252387dd-c8d9-456d-be4e-522a2d6940e2",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Chronic tension-type headache, intractable</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
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
                            "system": "http://snomed.info/sct",
                            "code": "404684003",
                            "display": "Chronic tension-type headache, intractable"
                        },
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "G44221",
                            "display": "Chronic tension-type headache, intractable"
                        }
                    ],
                    "text": "Chronic tension-type headache, intractable"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/ae601c55-77e1-4c27-aaf5-71931594cfe9",
                    "type": "Encounter"
                },
                "recordedDate": "2022-06-06T18:19:42.328213+00:00",
                "recorder": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "54701502-e1f5-4d19-89e8-9339ada36f50",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Screening for diabetes mellitus</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
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
                            "system": "http://snomed.info/sct",
                            "code": "404684003",
                            "display": "Screening for diabetes mellitus"
                        },
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "Z131",
                            "display": "Encounter for screening for diabetes mellitus"
                        }
                    ],
                    "text": "Screening for diabetes mellitus"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/ee75e186-95c5-4d76-a25a-a27309cb4a54",
                    "type": "Encounter"
                },
                "recordedDate": "2022-06-09T16:19:26.302511+00:00",
                "recorder": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "ec2bdea5-caba-4acd-94ee-4997b13ac5cc",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Family history of stroke</div>"
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                            "display": "Active"
                        }
                    ],
                    "text": "Active"
                },
                "verificationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                            "code": "provisional",
                            "display": "Provisional"
                        }
                    ],
                    "text": "Provisional"
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
                            "code": "Z823",
                            "display": "Family history of stroke"
                        }
                    ],
                    "text": "Family history of stroke"
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient",
                    "display": "Doe, Jane B."
                },
                "encounter": {
                    "reference": "Encounter/ee75e186-95c5-4d76-a25a-a27309cb4a54",
                    "type": "Encounter"
                },
                "recordedDate": "2022-06-15T15:30:14.695700+00:00"
            }
        }
    ]
}
```
{% endtab %}
{% tab search-response 401 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
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
{% tab search-response 403 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
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

<div id="condition-create-request">
{% tabs create-request %}
{% tab create-request curl %}
```sh
curl --location 'https://fumage-customer.canvasmedical.com/Condition' \
     --header 'Content-Type: application/fhir+json' \
     --header 'Authorization: Bearer <token>' \
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
{% endtabs %}
</div>

<div id="condition-create-response">
{% tabs create-response %}
{% tab create-response 201 %}
```json
  null
```
{% endtab %}
{% tab create-response 400 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "value",
            "details": {
                "text": "body -> encounter -> reference — must contain a resource type and identifier (type=value_error)"
            }
        },
        {
            "severity": "error",
            "code": "value",
            "details": {
                "text": "body -> recorder -> reference — must contain a resource type and identifier (type=value_error)"
            }
        }
    ]
}
```
{% endtab %}
{% tab create-response 401 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
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
{% tab create-response 403 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
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

<div id="condition-update-request">
{% tabs update-request %}
{% tab update-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Condition?patient=Patient%2F<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab update-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Condition/<pa> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="condition-update-response">
{% tabs update-response %}
{% tab update-response 200 %}
```json
null
```
{% endtab %}
{% tab update-response 401 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
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
{% tab update-response 403 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
      "details": {
        "text": "Authorization failed"
      }
    }
  ]
}
```
{% endtab %}
{% tab update-response 405 %}
```json
{
    "detail": "Method Not Allowed"
}
```
{% endtab %}
{% tab update-response 412 %}
```json
{
    "detail": "Predondition Failed"
}
```
{% endtab %}
{% tab update-response 422 %}
```json
{
    "detail": "Unprocessable Entity"
}
```
{% endtab %}
{% endtabs %}
</div>

