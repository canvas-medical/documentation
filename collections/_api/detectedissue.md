---
title: DetectedIssue
sections:
  - type: section
    blocks:
      - type: apidoc
        name: DetectedIssue
        article: "a"
        description: >-
          Indicates an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. Drug-drug interaction, Ineffective treatment frequency, Procedure-condition conflict, etc.
          <br><br>[https://www.hl7.org/fhir/R4/detectedissue.html](https://www.hl7.org/fhir/R4/detectedissue.html)<br><br>
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            type: string
            description: The Canvas identifier of the DetectedIssue.
            required_in: update
            exclude_in: create
          - name: identifier
            type: array[json]
            description_for_all_endpoints: >-
              External Ids for this item. <br><br>
              The identifier defines additional identifiers that are able to be stored for an DetectedIssue.
              We can have one external identifier per DetectedIssue.
              <br><br>These identifiers will not be surfaced, but they may help you identify the DetectedIssue in your system if that DetectedIssue was added by external source.
            attributes:
              - name: system
                type: string
                description: The namespace for the identifier value.
              - name: value
                type: string
                description: The value that is unique in the related system.
          - name: status
            type: enum
            description: The status of the DetectedIssue. 
            enum_options:
              - value: registered
              - value: preliminary
              - value: final
              - value: amended
              - value: corrected
              - value: cancelled
              - value: entered-in-error
            required_in: create, update
          - name: code
            description: Identifies the general type of issue identified.
            type: json
            attributes: 
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes: 
                  - name: system
                    description: >-
                      The system url of the coding.
                    enum_options: 
                      - value: https://terminology.hl7.org/CodeSystem/v3-ActCode
                    type: string
                    required_in: create, update
                  - name: code
                    description: >-
                      The code that identifies the general type of issue identified.
                    type: string
                    required_in: create, update
                  - name: display
                    description: >-
                      The display name of the coding
                    type: string
                    exclude_in: create, update
                required_in: create, update
            required_in: create, update
          - name: severity
            type: enum
            description: Indicates the degree of importance associated with the identified issue based on the potential impact on the patient.
            enum_options:
              - value: high
              - value: moderate
              - value: low
          - name: patient
            type: json
            description: The patient for the DetectedIssue record.
            required_in: create, update
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
                required_in: create, update
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
                required_in: create, update
          - name: identifiedDateTime
            type: date
            description: The date or datetime when the detected issue was identified.
            required_in: create, update
          - name: author
            type: json
            description: Individual or device responsible for the issue being raised. For example, a decision support system or a pharmacist conducting a medication review.
            required_in: create, update
            attributes:
              - name: reference
                type: string
                description: The reference string of the author in the format of `"Practitioner/4d789a3d5e794c0eb159a126b48c8b9f"`.
                required_in: create, update
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
                required_in: create, update
          - name: evidence
            type: array[json]
            description: Supporting evidence or manifestations that provide the basis for identifying the detected issue. There must be at least one evidence element with system "http://hl7.org/fhir/sid/icd-10-cm".
            attributes:
              - name: code
                description: "A manifestation that led to the recording of this detected issue."
                type: json
                attributes: 
                  - name: coding
                    description: Code defined by a terminology system.
                    type: array[json]
                    attributes: 
                      - name: system
                        description: >-
                          The system url of the coding.
                        enum_options: 
                          - value: http://hl7.org/fhir/sid/icd-10-cm
                        type: string
                        required_in: create, update
                      - name: code
                        type: string
                        description: 	The code of the Evidence
                        required_in: create, update
                      - name: display
                        description: >-
                          The display name of the coding
                        type: string
                        required_in: create, update
                    required_in: create, update
                required_in: create, update
            required_in: create, update
          - name: detail
            type: string
            description: A textual explanation of the detected issue.
          - name: reference
            type: string
            description: The literature, knowledge-base or similar reference that describes the propensity for the detected issue identified.
          - name: mitigation
            type: array[json]
            description: Indicates an action that has been taken or is committed to reduce or eliminate the likelihood of the risk identified by the detected issue from manifesting.
            attributes:
              - name: id
                type: string
                description: The Canvas identifier of the DetectedIssueMitigation.
                exclude_in: create
              - name: action
                description: "The type of action that has been taken or is committed to reduce or eliminate the likelihood of the risk identified by the detected issue from manifesting."
                type: json
                attributes: 
                  - name: coding
                    description: Code defined by a terminology system.
                    type: array[json]
                    attributes: 
                      - name: system
                        description: >-
                          The system url of the coding.
                        enum_options: 
                          - value: https://schemas.canvasmedical.com/fhir/detectedissue-mitigation-action
                        type: string
                        required_in: create, update
                      - name: code
                        type: enum
                        description: 	Describes the action that was taken or the observation that was made that reduces/eliminates the risk associated with the identified issue.
                        enum_options:
                          - value: valid
                          - value: invalid
                          - value: accepted
                          - value: refuted
                          - value: deferred
                          - value: corrected
                        required_in: create, update
                      - name: display
                        description: >-
                          The display name of the coding
                        type: string
                        exclude_in: create, update
                    required_in: create, update
                required_in: create, update
              - name: date
                type: date
                description: The date or datetime when the mitigation action was taken or committed to be taken.
                required_in: create, update
              - name: author
                type: json
                description: Individual or device responsible for the mitigation action. For example, a decision support system or a pharmacist conducting a medication review.
                attributes:
                  - name: reference
                    type: string
                    description: The reference string of the author in the format of `"Practitioner/4d789a3d5e794c0eb159a126b48c8b9f"`.
                    required_in: create, update
                  - name: type
                    type: string
                    description: Type the reference refers to (e.g. "Practitioner").
                    required_in: create, update
                required_in: create, update
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier for a specific DetectedIssue.
          - name: patient
            description: The patient for the DetectedIssue record in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
          - name: status
            type: string
            description: The status of the DetectedIssue.
            search_options:
              - value: registered
              - value: preliminary
              - value: final
              - value: amended
              - value: corrected
              - value: cancelled
              - value: entered-in-error
          - name: identified
            type: string
            description: Filter by identifiedDateTime. See [Date Filtering](/api/date-filtering) for more information.
        endpoints: [create, read, update, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: detectedissue-create-request
          example_response: detectedissue-create-response
          description: Create an **DetectedIssue**.
        read:
          responses: [200, 401, 403, 404]
          example_request: detectedissue-read-request
          example_response: detectedissue-read-response
          description: Read an **DetectedIssue**.
        update:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: detectedissue-update-request
          example_response: detectedissue-update-response
          description: Update an **DetectedIssue**.
        search:
          responses: [200, 400, 401, 403]
          example_response: detectedissue-search-response
          example_request: detectedissue-search-request
          description: Search an **DetectedIssue**.
---

<div id="detectedissue-create-request">

  {% tabs detectedissue-create-request %}

    {% tab detectedissue-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/DetectedIssue' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
  {
    "resourceType": "DetectedIssue",
    "identifier": [
        {
            "system": "Canvas",
            "value": "d9aefede-da05-4bef-bbf9-63bcf83c806a"
        }
    ],
    "status": "preliminary",
    "code": {
        "coding": [
            {
                "system": "https://terminology.hl7.org/CodeSystem/v3-ActCode", 
                "code": "CODINGGAP"
            }
        ]
    },
    "severity": "moderate",
    "patient": {
        "reference": "Patient/a39cafb9d1b445be95a2e2548e12a787",
        "type": "Patient"
    },
    "identifiedDateTime": "2024-08-10T14:23:08+00:00",
    "author": {
        "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
        "type": "Practitioner"
    },
    "evidence": [
        {
            "code": [
                {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "I23.43",
                            "display": "Code text explanation"
                        }
                    ]
                }
            ]
        }
    ],
    "detail": "Detail for detected issue",
    "reference": "https://example.com",
    "mitigation": [
        {
            "action": {
                "coding": [
                    {
                        "system": "https://schemas.canvasmedical.com/fhir/detectedissue-mitigation-action",
                        "code": "valid"
                    }
                ]
            },
            "date": "2024-08-09T14:23:08+00:00",
            "author": {
                "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
                "type": "Practitioner"
            }
        }
    ]
}'
```
    {% endtab %}
    {% tab detectedissue-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/DetectedIssue"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json",
}

payload = {
    "resourceType": "DetectedIssue",
    "identifier": [
        {
            "system": "Canvas",
            "value": "d9aefede-da05-4bef-bbf9-63bcf83c806a"
        }
    ],
    "status": "preliminary",
    "code": {
        "coding": [
            {
                "system": "https://terminology.hl7.org/CodeSystem/v3-ActCode", 
                "code": "CODINGGAP"
            }
        ]
    },
    "severity": "moderate",
    "patient": {
        "reference": "Patient/a39cafb9d1b445be95a2e2548e12a787",
        "type": "Patient"
    },
    "identifiedDateTime": "2024-08-10T14:23:08+00:00",
    "author": {
        "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
        "type": "Practitioner"
    },
    "evidence": [
        {
            "code": [
                {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "I23.43",
                            "display": "Code text explanation"
                        }
                    ]
                }
            ]
        }
    ],
    "detail": "Detail for detected issue",
    "reference": "https://example.com",
    "mitigation": [
        {
            "action": {
                "coding": [
                    {
                        "system": "https://schemas.canvasmedical.com/fhir/detectedissue-mitigation-action",
                        "code": "valid"
                    }
                ]
            },
            "date": "2024-08-09T14:23:08+00:00",
            "author": {
                "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
                "type": "Practitioner"
            }
        }
    ]
}
```
    {% endtab %}

  {% endtabs %}
</div>

<div id="detectedissue-create-response">
{% include create-response.html %}
</div>

<div id="detectedissue-read-request">
{% include read-request.html resource_type="DetectedIssue" %}
</div>

<div id="detectedissue-read-response">
  {% tabs detectedissue-read-response %}
    {% tab detectedissue-read-response 200 %}
```json
{
    "resourceType": "DetectedIssue",
    "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
    "identifier": [
        {
            "system": "Canvas",
            "value": "d9aefede-da05-4bef-bbf9-63bcf83c806a"
        }
    ],
    "status": "preliminary",
    "code": {
        "coding": [
            {
                "system": "https://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "CODINGGAP",
                "display": "Codinggap"
            }
        ],
        "text": "Codinggap"
    },
    "patient": {
        "reference": "Patient/a39cafb9d1b445be95a2e2548e12a787",
        "type": "Patient"
    },
    "identifiedDateTime": "2024-08-10T14:23:08+00:00",
    "author": {
        "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
        "type": "Practitioner"
    },
    "evidence": [
        {
            "code": [
                {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "I23.43",
                            "display": "Code text explanation"
                        }
                    ]
                }
            ]
        }
    ],
    "detail": "Detail for detected issue",
    "reference": "https://example.com",
    "mitigation": [
        {
            "id": "9a1cfc8c-4ee9-4eb7-9658-a5b0f9576698",
            "action": {
                "coding": [
                    {
                        "system": "https://schemas.canvasmedical.com/fhir/detectedissue-mitigation-action",
                        "code": "valid"
                    }
                ]
            },
            "date": "2024-08-09T14:23:08+00:00",
            "author": {
                "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
                "type": "Practitioner"
            }
        }
    ]
}
```
    {% endtab %}
    {% tab detectedissue-read-response 401 %}
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

    {% tab detectedissue-read-response 403 %}
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

    {% tab detectedissue-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown DetectedIssue resource 'd9aefede-da05-4bef-bbf9-63bcf83c806b'"
      }
    }
  ]
}
```
    {% endtab %}
  {% endtabs %}
</div>

<div id="detectedissue-update-request">

  {% tabs detectedissue-update-request %}

    {% tab detectedissue-update-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/DetectedIssue/d9aefede-da05-4bef-bbf9-63bcf83c806a' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
  {
    "resourceType": "DetectedIssue",
    "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
    "identifier": [
        {
            "system": "Canvas",
            "value": "d9aefede-da05-4bef-bbf9-63bcf83c806a"
        }
    ],
    "status": "preliminary",
    "code": {
        "coding": [
            {
                "system": "https://terminology.hl7.org/CodeSystem/v3-ActCode", 
                "code": "CODINGGAP"
            }
        ]
    },
    "severity": "moderate",
    "patient": {
        "reference": "Patient/a39cafb9d1b445be95a2e2548e12a787",
        "type": "Patient"
    },
    "identifiedDateTime": "2024-08-10T14:23:08+00:00",
    "author": {
        "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
        "type": "Practitioner"
    },
    "evidence": [
        {
            "code": [
                {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "I23.43",
                            "display": "Code text explanation"
                        }
                    ]
                }
            ]
        }
    ],
    "detail": "Detail for detected issue",
    "reference": "https://example.com",
    "mitigation": [
        {
            "id": "9a1cfc8c-4ee9-4eb7-9658-a5b0f9576698",
            "action": {
                "coding": [
                    {
                        "system": "https://schemas.canvasmedical.com/fhir/detectedissue-mitigation-action",
                        "code": "valid"
                    }
                ]
            },
            "date": "2024-08-09T14:23:08+00:00",
            "author": {
                "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
                "type": "Practitioner"
            }
        }
    ]
}'
```
    {% endtab %}
    {% tab detectedissue-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/DetectedIssue/d9aefede-da05-4bef-bbf9-63bcf83c806a"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json",
}

payload = {
    "resourceType": "DetectedIssue",
    "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
    "identifier": [
        {
            "system": "Canvas",
            "value": "d9aefede-da05-4bef-bbf9-63bcf83c806a"
        }
    ],
    "status": "preliminary",
    "code": {
        "coding": [
            {
                "system": "https://terminology.hl7.org/CodeSystem/v3-ActCode", 
                "code": "CODINGGAP"
            }
        ]
    },
    "severity": "moderate",
    "patient": {
        "reference": "Patient/a39cafb9d1b445be95a2e2548e12a787",
        "type": "Patient"
    },
    "identifiedDateTime": "2024-08-10T14:23:08+00:00",
    "author": {
        "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
        "type": "Practitioner"
    },
    "evidence": [
        {
            "code": [
                {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "I23.43",
                            "display": "Code text explanation"
                        }
                    ]
                }
            ]
        }
    ],
    "detail": "Detail for detected issue",
    "reference": "https://example.com",
    "mitigation": [
        {
            "id": "9a1cfc8c-4ee9-4eb7-9658-a5b0f9576698",
            "action": {
                "coding": [
                    {
                        "system": "https://schemas.canvasmedical.com/fhir/detectedissue-mitigation-action",
                        "code": "valid"
                    }
                ]
            },
            "date": "2024-08-09T14:23:08+00:00",
            "author": {
                "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
                "type": "Practitioner"
            }
        }
    ]
}
```
    {% endtab %}

  {% endtabs %}
</div>

<div id="detectedissue-update-response">
{% include create-response.html %}
</div>

<div id="detectedissue-search-request">
{% include search-request.html resource_type="DetectedIssue" search_string="patient=Patient/a39cafb9d1b445be95a2e2548e12a787" %}
</div>

<div id="detectedissue-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
      {
        "relation": "self",
        "url": "/DetectedIssue?patient=Patient%2Fa39cafb9d1b445be95a2e2548e12a787&_count=10&_offset=0"
      },
      {
        "relation": "first",
        "url": "/DetectedIssue?patient=Patient%2Fa39cafb9d1b445be95a2e2548e12a787&_count=10&_offset=0"
      },
      {
        "relation": "last",
        "url": "/DetectedIssue?patient=Patient%2Fa39cafb9d1b445be95a2e2548e12a787&_count=10&_offset=0"
      }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "DetectedIssue",
                "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
                "identifier": [
                    {
                        "system": "Canvas",
                        "value": "d9aefede-da05-4bef-bbf9-63bcf83c806a"
                    }
                ],
                "status": "preliminary",
                "code": {
                    "coding": [
                        {
                            "system": "https://terminology.hl7.org/CodeSystem/v3-ActCode",
                            "code": "CODINGGAP",
                            "display": "Codinggap"
                        }
                    ],
                    "text": "Codinggap"
                },
                "patient": {
                    "reference": "Patient/a39cafb9d1b445be95a2e2548e12a787",
                    "type": "Patient"
                },
                "identifiedDateTime": "2024-08-10T14:23:08+00:00",
                "author": {
                    "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
                    "type": "Practitioner"
                },
                "evidence": [
                    {
                        "code": [
                            {
                                "coding": [
                                    {
                                        "system": "http://hl7.org/fhir/sid/icd-10-cm",
                                        "code": "I23.43",
                                        "display": "Code text explanation"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "detail": "Detail for detected issue",
                "reference": "https://example.com",
                "mitigation": [
                    {
                        "id": "9a1cfc8c-4ee9-4eb7-9658-a5b0f9576698",
                        "action": {
                            "coding": [
                                {
                                    "system": "https://schemas.canvasmedical.com/fhir/detectedissue-mitigation-action",
                                    "code": "valid"
                                }
                            ]
                        },
                        "date": "2024-08-09T14:23:08+00:00",
                        "author": {
                            "reference": "Practitioner/4d789a3d5e794c0eb159a126b48c8b9f",
                            "type": "Practitioner"
                        }
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab detectedissue-search-response 400 %}
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

    {% tab detectedissue-search-response 401 %}
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

    {% tab detectedissue-search-response 403 %}
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

