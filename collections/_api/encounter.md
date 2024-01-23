---
title: Encounter
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Encounter
        article: "a"
        description: >-
          An interaction between a patient and healthcare provider(s) for the purpose of providing healthcare service(s) or assessing the health status of a patient.<br><br>[https://hl7.org/fhir/R4/encounter.html](https://hl7.org/fhir/R4/encounter.html)<br><br><b>Encounter creation in Canvas</b><br><br>An encounter is associated with some of our notes in Canvas. For our default base notes, an encounter will be created with these note types:<br><br>Lab visit<br>Phone visit<br>Telehealth visit<br>Office visit<br>Home Visit<br>In-patient Visit<br><br>Appointment Notes, once checked in, that are for the above visit types will be converted to an encounter.<br><br>See this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360056430014-Appointments) for how to schedule an appointment.<br><br>With our [Configurable Note Types Feature](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083) all custom note types will be associated with an encounter by default.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-encounter.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-encounter.html)
        attributes:
          - name: id
            description: >-
              The identifier of the encounter
            type: string
          - name: extension
            type: array[json]
            description: >-
              Canvas supports a note identifier extension on this resource for read and search interactions. The note identifier can be used with the Canvas Note API.<br>
              <br>
              The `url` for the extension is: **http://schemas.canvasmedical.com/fhir/extensions/note-id**<br>
              <br>
              The `valueId` contains the note identifier.<br>
              <br>
              See the request and response examples for more information.
          - name: identifier
            type: array[json]
            description: >-
              Identifier(s) by which this encounter is known
          - name: status
            type: string
            description: >-
              The status of the encounter. Supported statuses are: **planned**, **cancelled**, **finished**, **in-progress**
          - name: class
            type: json
            description: >-
              Classification of patient encounter
          - name: type
            type: array[json]
            description: >-
              Specific type of encounter
          - name: subject
            type: json
            description: >-
              The patient or group present at the encounter
          - name: participant
            type: array[json]
            description: >-
              List of participants involved in the encounter
          - name: appointment
            type: array[json]
            description: >-
              The appointment that scheduled this encounter
          - name: period
            type: json
            description: >-
              The start and end time of the encounter
          - name: reasonCode
            type: array[json]
            description: >-
              Coded reason the encounter takes place
          - name: reasonReference
            type: array[json]
            description: >-
              Reason the encounter takes place (reference)
          - name: hospitalization
            type: json
            description: >-
              Details about the admission to a healthcare service
          - name: location
            type: array[json]
            description: >-
              List of locations where the patient has been during the encounter
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: appointment
            type: string
            description: >-
              The appointment that scheduled this encounter
          - name: date
            type: string
            description: >-
              The start time of the encounter
          - name: patient
            type: string
            description: >-
              The patient or group present at the encounter
          - name: subject
            type: string
            description: >-
              Encounter subject
        endpoints: [read, search]
        read:
          responses: [200, 401, 403, 404]
          example_response: encounter-read-response
          example_request: encounter-read-request
          description: Read an Encounter resource
        search:
          responses: [200, 400, 401, 403]
          example_response: encounter-search-response
          example_request: encounter-search-request
          description: Search for Encounter resources
---

<div id="encounter-read-request">
{%  include read-request.html resource_type="Encounter" %}
</div>

<div id="encounter-read-response">
{% tabs encounter-read-response %}
{% tab encounter-read-response 200 %}
```json
{
    "resourceType": "Encounter",
    "id": "7720a218-c0bd-4cee-82a2-729bd9c101f3",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "identifier": [
        {
            "id": "7720a218-c0bd-4cee-82a2-729bd9c101f3",
            "system": "http://canvasmedical.com",
            "value": "7720a218-c0bd-4cee-82a2-729bd9c101f3"
        }
    ],
    "status": "in-progress",
    "class": {
        "system": "https://www.hl7.org/fhir/v3/ActEncounterCode/vs.html"
    },
    "type": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "308335008",
                    "display": "Office Visit"
                }
            ]
        }
    ],
    "subject": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "participant": [
        {
            "type": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                            "code": "PART",
                            "display": "Participation"
                        }
                    ]
                }
            ],
            "period": {
                "start": "2022-04-04T05:26:34.711718+00:00"
            },
            "individual": {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                "type": "Practitioner",
                "display": "Canvas Support MD"
            }
        }
    ],
    "period": {
        "start": "2022-04-04T05:26:34.711718+00:00"
    },
    "reasonCode": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "308335008",
                    "display": "Patient encounter procedure (procedure)"
                }
            ]
        }
    ],
    "reasonReference": [
        {
            "reference": "Condition/b06982fa-9bcb-4695-a2f4-09cfdb21f03d",
            "type": "Condition"
        },
        {
            "reference": "Condition/e3df5e12-8ea4-46f8-922e-89a229945ef4",
            "type": "Condition"
        },
        {
            "reference": "Condition/266eae2b-4983-42b7-94ca-1397f80a7968",
            "type": "Condition"
        }
    ],
    "hospitalization": {
        "dischargeDisposition": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/discharge-disposition",
                    "code": "oth",
                    "display": "Other"
                }
            ]
        }
    },
    "location": [
        {
            "location": {
                "reference": "Location/50ea08f9-f4a5-4315-90e3-10d38922daa8",
                "type": "Location"
            }
        }
    ]
}
```
{% endtab %}
{% tab encounter-read-response 401 %}
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
{% tab encounter-read-response 403 %}
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
{% tab encounter-read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown Encounter resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="encounter-search-request">
{% include search-request.html resource_type="Encounter" search_string="patient=Patient/8f19219e36054ea89c4d98c9b258c2f1&date=ge2023-09-15" %}
</div>

<div id="encounter-search-response">
{% tabs encounter-search-response %}
{% tab encounter-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Encounter?patient=Patient%2F8f19219e36054ea89c4d98c9b258c2f1&date=ge2023-09-15&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Encounter?patient=Patient%2F8f19219e36054ea89c4d98c9b258c2f1&date=ge2023-09-15&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Encounter?patient=Patient%2F8f19219e36054ea89c4d98c9b258c2f1&date=ge2023-09-15&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Encounter",
                "id": "06e0ee68-59f8-4899-b906-1298a36870ab",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
                        "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
                    }
                ],
                "identifier": [
                    {
                        "id": "06e0ee68-59f8-4899-b906-1298a36870ab",
                        "system": "http://canvasmedical.com",
                        "value": "06e0ee68-59f8-4899-b906-1298a36870ab"
                    }
                ],
                "status": "finished",
                "class": {
                    "system": "https://www.hl7.org/fhir/v3/ActEncounterCode/vs.html"
                },
                "type": [
                    {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "308335008",
                                "display": "Office Visit"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/8f19219e36054ea89c4d98c9b258c2f1",
                    "type": "Patient"
                },
                "participant": [
                    {
                        "type": [
                            {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                                        "code": "PART",
                                        "display": "Participation"
                                    }
                                ]
                            }
                        ],
                        "period": {
                            "start": "2023-09-20T18:41:54.885110+00:00",
                            "end": "2023-09-20T18:57:47.490741+00:00"
                        },
                        "individual": {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner",
                            "display": "Larry Weed"
                        }
                    }
                ],
                "period": {
                    "start": "2023-09-20T18:41:54.885110+00:00",
                    "end": "2023-09-20T18:57:47.490741+00:00"
                },
                "reasonCode": [
                    {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "308335008",
                                "display": "Patient encounter procedure (procedure)"
                            }
                        ]
                    }
                ],
                "reasonReference": [
                    {
                        "reference": "Condition/82e02680-c37d-4705-876d-b845d85efc20",
                        "type": "Condition"
                    }
                ],
                "hospitalization": {
                    "dischargeDisposition": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/discharge-disposition",
                                "code": "oth",
                                "display": "Other"
                            }
                        ]
                    }
                },
                "location": [
                    {
                        "location": {
                            "reference": "Location/e332ff73-7fa4-4432-abe9-2adc43b1bb2c",
                            "type": "Location"
                        }
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab encounter-search-response 400 %}
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
    {% tab encounter-search-response 401 %}
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

{% tab encounter-search-response 403 %}
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
