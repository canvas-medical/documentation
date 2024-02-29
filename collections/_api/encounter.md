---
title: Encounter
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Encounter
        article: "a"
        description: >-
          An interaction between a patient and healthcare provider(s) for the purpose of providing healthcare service(s) or assessing the health status of a patient.<br><br>[https://hl7.org/fhir/R4/encounter.html](https://hl7.org/fhir/R4/encounter.html)<br><br>

          <b>Encounter creation in Canvas</b><br><br>
          An encounter is associated with some of our notes in Canvas. For our default base notes, an encounter will be created with these note types: <br><br>
          - Lab visit <br>
          - Phone visit <br>
          - Telehealth visit <br>
          - Office visit <br>
          - Home Visit <br>
          - In-patient Visit <br><br>

          With our [Configurable Note Types Feature](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083) all custom note types will be associated with an encounter by default.<br><br>

          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-encounter.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-encounter.html)
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the encounter.
            type: string
          - name: extension
            type: array[json]
            read_and_search_description: Canvas supports a note identifier extension on this resource for read and search interactions. The note identifier can be used with the [Canvas Note API](/api/note).
            attributes:
                - name: url
                  type: string
                  description: Reference that defines the content of this object.
                  enum_options:
                    - value: http://schemas.canvasmedical.com/fhir/extensions/note-id
                - name: valueId
                  type: string
                  description: The valueId field is used for the Note extension and will be the note's unique identifier.
          - name: identifier
            type: array[json]
            description: Identifier(s) by which this encounter is known. 
            attributes:
                - name: id 
                  description: The identifier of the encounter.
                  type: string
                - name: system
                  description: The namespace for the identifier value.
                  type: string
                  enum_options:
                    - value: http://canvasmedical.com
                - name: value
                  description: The value that is unique.
                  type: string
          - name: status
            type: enum [ planned | cancelled | finished | in-progress ]
            description: >-
              The status of the encounter. <br><br>
              - A `planned` encounter is an Appointment note that has not been check-in. <br>
              - A `cancelled` encounter is either 1) an Appointment that was cancelled or no-showed or 2) a Note that was deleted from the patient's chart. <br>
              - A `finished` encounter is a Note that has been locked at least once. Notes that are in an unlocked/ammended state, will have a finished status; however, they will not have a period.end datetime. <br>
              - An `in-progress` encounter is a note that has not yet been locked. 
          - name: class
            type: json
            description: Classification of patient encounter.
            attributes:
                - name: system
                  type: string
                  description: Identity of the terminology system.
                  enum_options: 
                    - value: https://www.hl7.org/fhir/v3/ActEncounterCode/vs.html
                - name: code
                  type: string
                  description: Symbol in syntax defined by the system.
                - name: display
                  type: string
                  description: Representation defined by the system.
          - name: type
            type: array[json]
            description: Specific type of encounter. <br><br>
                In Canvas this will represent the Note Type the encounter is associated with. If the Note is in a `planned` status, the coding will correspond to Canvas' appointment note type until the note is checked-in and converted to the scheduled note type. 
            attributes: 
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      type: string
                    - name: code
                      description: The code.
                      type: string
                    - name: display
                      description: The display name of the coding.
                      type: string
          - name: subject
            type: json
            description: The patient or group present at the encounter. 
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: participant
            type: array[json]
            description: List of participants involved in the encounter.
            attributes:
                - name: type
                  type: array[json]
                  description: Role of participant in encounter.
                  attributes:
                    - name: coding
                      description: Identifies where the definition of the code comes from.
                      type: array[json]
                      attributes: 
                        - name: system
                          description: The system url of the coding.
                          type: string
                          enum_options: 
                            - value: http://terminology.hl7.org/CodeSystem/v3-ParticipationType
                        - name: code
                          description: The code.
                          type: string
                          enum_options: 
                            - value: PART
                        - name: display
                          description: The display name of the coding.
                          type: string
                          enum_options:
                            - value: Participant
                - name: period
                  type: json
                  description: Period of time during the encounter that the participant participated
                  attributes: 
                    - name: start
                      type: datetime
                      description: Starting time with inclusive boundary.
                    - name: end
                      type: datetime
                      description: End time with inclusive boundary, if not ongoing.
                - name: individual
                  type: json
                  description: Persons involved in the encounter other than the patient.
                  attributes: 
                    - name: reference
                      type: string
                      description: The reference string of the participant in the format of `"Practitioner/4150cd20de8a470aa570a852859ac87e"`.
                    - name: type
                      type: string
                      description: Type the reference refers to (e.g. "Practitioner").
                    - name: display
                      type: string
                      description: Text alternative for the resource (e.g Credendialed name of the Practitioner).
          - name: appointment
            type: array[json]
            description: The appointment that scheduled this encounter if applicable. If an appointment was rescheduled at any point within the Canvas UI, there may be multiple appointments in this array.
            attributes: 
                - name: reference
                  type: string
                  description: The reference string of the appointment in the format of `"Appointment/79f99d7d-2e55-41ec-8e39-01bd9408aacf"`.
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Appointment").
          - name: period
            type: json
            description: The start and end time of the encounter. <br><br>
                Appointment notes in Canvas will not have a period until the note is checked-in. <br><br>Encounter notes will not have period.end datetime until the note is locked/signed. <br><br>Notes that are in an unlocked/ammended state, will not have a period.end datetime until relocked/signed.
            attributes: 
                - name: start
                  type: datetime
                  description: Starting time with inclusive boundary.
                - name: end
                  type: datetime
                  description: End time with inclusive boundary, if not ongoing.
          - name: reasonCode
            type: array[json]
            description: Coded reason the encounter takes place.
            attributes: 
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      type: string
                      enum_options: 
                        - value: http://snomed.info/sct
                    - name: code
                      description: The code.
                      type: string
                      enum_options: 
                        - value: 308335008
                    - name: display
                      description: The display name of the coding.
                      type: string
                      enum_options:
                        - value: Patient encounter procedure (procedure)
          - name: reasonReference
            type: array[json]
            description: >-
              Reason the encounter takes place (reference). <br><br>

              In Canvas this represents any encounters that were diagnosed, assessed, or indicated during the encounter.
            attributes: 
                - name: reference
                  type: string
                  description: The reference string of the condition in the format of `"Condition/e8921649-ec92-46b5-b663-8a4097c10513"`.
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Condition").
          - name: hospitalization
            type: json
            description: Details about the admission to a healthcare service.
            attributes: 
                - name: coding
                  description: Identifies where the definition of the code comes from.
                  type: array[json]
                  attributes: 
                    - name: system
                      description: The system url of the coding.
                      type: string
                      enum_options: 
                        - value: http://terminology.hl7.org/CodeSystem/discharge-disposition
                    - name: code
                      description: The code.
                      type: string
                      enum_options: 
                        - value: oth
                    - name: display
                      description: The display name of the coding.
                      type: string
                      enum_options:
                        - value: Other
          - name: location
            type: array[json]
            description: List of locations where the patient has been during the encounter.
            attributes:
                - name: location
                  type: json
                  description: Location the encounter takes place.
                  attributes: 
                      - name: reference
                        type: string
                        description: The reference string of the location in the format of `"Location/3c01c6ea-b7dc-4109-9d1c-1cf4ba7c211e"`.
                      - name: type
                        type: string
                        description: Type the reference refers to (e.g. "Location").
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier for a specific encounter.
          - name: appointment
            type: string
            description: The appointment that scheduled this encounter in the format `Appointment/6e5234c4-2dd0-495d-98cf-ad04add1316e`.
          - name: date
            type: string
            description: Filter by period.start time. See [Date Filtering](/api/date-filtering) for more information.
          - name: patient
            type: string
            description: The patient or group present at the encounter in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
          - name: subject
            type: string
            description: Encounter subject in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`. 
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
            "url": "/Encounter?patient=Patient/8f19219e36054ea89c4d98c9b258c2f1&date=ge2023-09-15&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Encounter?patient=Patient/8f19219e36054ea89c4d98c9b258c2f1&date=ge2023-09-15&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Encounter?patient=Patient/8f19219e36054ea89c4d98c9b258c2f1&date=ge2023-09-15&_count=10&_offset=0"
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
        },
        {
            "resourceType": "Encounter",
            "id": "f7663d7b-13bd-4236-843e-086306aea125",
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
                    "valueId": "8c83a639-05c0-43e8-a39b-8b99ea75d7d2"
                }
            ],
            "identifier": [
                {
                    "id": "f7663d7b-13bd-4236-843e-086306aea125",
                    "system": "http://canvasmedical.com",
                    "value": "f7663d7b-13bd-4236-843e-086306aea125"
                }
            ],
            "status": "planned",
            "class": {
                "system": "https://www.hl7.org/fhir/v3/ActEncounterCode/vs.html"
            },
            "type": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "185418009",
                            "display": "Method appointment made"
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
                    "individual": {
                        "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                        "type": "Practitioner",
                        "display": "Canvas Support MD"
                    }
                }
            ],
            "appointment": [
                {
                    "reference": "Appointment/65463607-866c-4c6f-812f-bf8616a5f755",
                    "type": "Appointment"
                },
                {
                    "reference": "Appointment/6e5234c4-2dd0-495d-98cf-ad04add1316e",
                    "type": "Appointment"
                }
            ],
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
                        "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060",
                        "type": "Location"
                    }
                }
            ]
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
