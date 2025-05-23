---
title: Immunization
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Immunization
        article: "a"
        description: >-
          Describes the event of a patient being administered a vaccine or a record of an immunization as reported by a patient, a clinician or another party.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-immunization.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-immunization.html)<br><br>

          In Canvas, Immunization records are recorded using either the [Immunization Statement Commmand](https://canvas-medical.help.usepylon.com/articles/1379672479-command-immunization-statement) or the [Immunize Command](https://canvas-medical.help.usepylon.com/articles/4155771468-command-immunize).
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            type: string
            description: The Canvas identifier of the immunization.
            required_in: update
            exclude_in: create
          - name: extension
            type: array[json]
            description_for_all_endpoints: Canvas supports a note identifier extension on this resource. The note identifier can be used with the [Canvas Note API](/api/note).
            create_description: Canvas recommends sending the note identifier extension or the Encounter reference, but not both. If both are supplied, they must both refer to the same note. If neither is specified, it will insert into a Data Import note where the DOS is the current time of ingestion.
            attributes:
              - name: url
                type: string
                description: Identifies the meaning of the extension
                enum_options:
                  - value: http://schemas.canvasmedical.com/fhir/extensions/note-id
                required_in: create, update
              - name: valueId
                type: string
                description: The valueId field is used for the Note extension and will be the note's unique identifier.
                required_in: create, update
          - name: status
            type: enum [ completed | entered-in-error | not-done ]
            description: The status of the immunization.
            enum_options:
              - value: completed
                exclude_in: update
              - value: entered-in-error
                exclude_in: create
              - value: not-done
                exclude_in: create, update
            required_in: create, update
          - name: statusReason
            type: json
            description: A coding for reason not given, if recorded - omitted otherwise.
            exclude_in: create, update
            attributes:
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    type: string
                    enum_options:
                      - value: http://terminology.hl7.org/CodeSystem/v3-ActReaso
                  - name: code
                    description: The code.
                    type: string
                  - name: display
                    description: The display name of the coding.
                    type: string
          - name: vaccineCode
            type: json
            description: Coding for the administered vaccine.
            required_in: create, update
            attributes:
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                required_in: create, update
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    type: string
                    required_in: create, update
                    enum_options:
                      - value: http://hl7.org/fhir/sid/cvx
                      - value: http://www.ama-assn.org/go/cpt
                      - value: unstructured
                  - name: code
                    description: The code.
                    type: string
                    required_in: create, update
                  - name: display
                    description: The display name of the coding.
                    type: string
          - name: patient
            type: json
            description: The patient who received the immunization.
            required_in: create, update
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
                required_in: create, update
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: encounter
            type: json
            description: The encounter related to the provided Note in the extension of this resource.
            create_description: >-
              Supply an encounter reference to be able to insert the command into a specific note on the patient's timeline. If no encounter is specified, it will insert into a Data Import note where the DOS is the current time of ingestion.
              <br><br>
              **Canvas does not currently support concurrent creation of resources on the same encounter.** Please avoid issuing concurrent requests that reference the same encounter to this endpoint, or to any other endpoints that reference encounters. It is OK to issue concurrent requests to these endpoints as long as the requests reference different encounters. 
            attributes:
              - name: reference
                type: string
                description: The reference string of the encounter in the format of `"Encounter/76028e14e77a47f4b95149bf5b7400bb"`.
                required_in: create, update
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Encounter").
          - name: occurrenceDateTime
            type: date
            description: The date or datetime the immunization was administered or reported to have been administered.
            required_in: create, update
          - name: primarySource
            type: boolean
            required_in: create, update
            description_for_all_endpoints: Whether the immunization was administered by a primary source.
            read_and_search_description: >-
              - **true** indicates that the immunization was administered within the clinic. To document immunizations like these, use an [Immunize Command](https://canvas-medical.help.usepylon.com/articles/4155771468-command-immunize).<br><br>
              - **false** indicates that the immunization was administered outside the clinic. To document this immunizations like these, use an [Immunization Statement Command](https://canvas-medical.help.usepylon.com/articles/1379672479-command-immunization-statement).
            create_description: On create accepts only **false**.
          - name: note
            description: >-
              Additional text not captured in other fields. <br><br>Canvas will display this in the `comment` field of the immunization statement command. If there are multiple objects given, they will be separeted by a new line on the UI.
            type: array[json]
            attributes:
                - name: text
                  type: string
                  description: The annotation - text content. 
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier for a specific immunization.
          - name: patient
            description: The patient for the vaccination record in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
        endpoints: [create, read, update, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: immunization-create-request
          example_response: immunization-create-response
          description: Immunization records created through this endpoint will be stored in an Immunization Statement command on the patient's chart. There currently is no support to create an Immunize command with this endpoint.
        read:
          responses: [200, 401, 403, 404]
          example_request: immunization-read-request
          example_response: immunization-read-response
        update:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: immunization-update-request
          example_response: immunization-update-response
          description: Update an Immunization resource.<br><br>The only type of Immunization update interaction that is supported by Canvas is to mark an existing Immunization Statement as **entered-in-error** using the `status` attribute. No changes to other fields will be processed; however, required fields still need to be supplied.
        search:
          responses: [200, 400, 401, 403]
          example_response: immunization-search-response
          example_request: immunization-search-request
---

<div id="immunization-create-request">

  {% tabs immunization-create-request %}

    {% tab immunization-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Immunization' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
  {
    "resourceType": "Immunization",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "eb754467-c8fc-4eac-9f36-2f46a510b48f"
        }
    ],
    "status": "completed",
    "vaccineCode": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/cvx",
                "code": "110"
            },
            {
                "system": "http://www.ama-assn.org/go/cpt",
                "code": "90723"
            }
        ]
    },
    "patient": {
        "reference": "Patient/4d789a3d5e794c0eb159a126b48c8b9f",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/76028e14-e77a-47f4-b951-49bf5b7400bb"
    },
    "occurrenceDateTime": "2024-10-04",
    "primarySource": false,
    "note": [
      {
        "text": "First Dose"
      }
    ]
  }'
```
    {% endtab %}
    {% tab immunization-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Immunization"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json",
}

payload = {
    "resourceType": "Immunization",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "eb754467-c8fc-4eac-9f36-2f46a510b48f"
        }
    ],
    "status": "completed",
    "vaccineCode": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/cvx",
                "code": "110"
            },
            {
                "system": "http://www.ama-assn.org/go/cpt",
                "code": "90723"
            }
        ]
    },
    "patient": {
        "reference": "Patient/4d789a3d5e794c0eb159a126b48c8b9f",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/76028e14-e77a-47f4-b951-49bf5b7400bb"
    },
    "occurrenceDateTime": "2024-10-04",
    "primarySource": False,
    "note": [
      {
        "text": "First Dose"
      }
    ]
}
```
    {% endtab %}

  {% endtabs %}
</div>

<div id="immunization-create-response">
{% include create-response.html %}
</div>

<div id="immunization-read-request">
{% include read-request.html resource_type="Immunization" %}
</div>

<div id="immunization-read-response">
  {% tabs immunization-read-response %}
    {% tab immunization-read-response 200 %}
```json
{
  "resourceType": "Immunization",
  "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
  "extension": [
    {
        "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
        "valueId": "eb754467-c8fc-4eac-9f36-2f46a510b48f"
    }
  ],
  "status": "completed",
  "vaccineCode": {
      "coding": [
        {
          "system": "http://hl7.org/fhir/sid/cpt",
          "code": "91306",
          "display": "Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) (coronavirus disease [COVID-19]) vaccine, mRNA-LNP, spike protein, preservative free, 50 mcg/0.25 mL dosage, for intramuscular use"
        },
        {
          "system": "http://hl7.org/fhir/sid/cvx",
          "code": "207",
          "display": "COVID-19, mRNA, LNP-S, PF, 100 mcg/0.5mL dose or 50 mcg/0.25mL dose"
        }
      ]
  },
  "patient": {
      "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
      "type": "Patient"
  },
  "encounter": {
    "reference": "Encounter/76028e14-e77a-47f4-b951-49bf5b7400bb"
  },
  "occurrenceDateTime": "2022-05-26T18:55:34.629659+00:00",
  "primarySource": false,
  "note": [
    {
      "text": "First Dose"
    }
  ]
}
```
    {% endtab %}
    {% tab immunization-read-response 401 %}
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

    {% tab immunization-read-response 403 %}
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

    {% tab immunization-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Immunization resource 'd9aefede-da05-4bef-bbf9-63bcf83c806b'"
      }
    }
  ]
}
```
    {% endtab %}
  {% endtabs %}
</div>

<div id="immunization-update-request">

  {% tabs immunization-update-request %}

    {% tab immunization-update-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Immunization/d9aefede-da05-4bef-bbf9-63bcf83c806a' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
  {
    "resourceType": "Immunization",
    "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "eb754467-c8fc-4eac-9f36-2f46a510b48f"
        }
    ],
    "status": "entered-in-error",
    "vaccineCode": {
        "coding": [
            {
              "system": "http://hl7.org/fhir/sid/cpt",
              "code": "91306",
              "display": "Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) (coronavirus disease [COVID-19]) vaccine, mRNA-LNP, spike protein, preservative free, 50 mcg/0.25 mL dosage, for intramuscular use"
            },
            {
              "system": "http://hl7.org/fhir/sid/cvx",
              "code": "207",
              "display": "COVID-19, mRNA, LNP-S, PF, 100 mcg/0.5mL dose or 50 mcg/0.25mL dose"
            }
        ]
    },
    "patient": {
        "reference": "Patient/4d789a3d5e794c0eb159a126b48c8b9f",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/76028e14-e77a-47f4-b951-49bf5b7400bb"
    },
    "occurrenceDateTime": "2024-10-04",
    "primarySource": False,
    "note": [
      {
        "text": "First Dose"
      }
    ]
  }'
```
    {% endtab %}
    {% tab immunization-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Immunization/d9aefede-da05-4bef-bbf9-63bcf83c806a"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json",
}

payload = {
    "resourceType": "Immunization",
    "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "eb754467-c8fc-4eac-9f36-2f46a510b48f"
        }
    ],
    "status": "entered-in-error",
    "vaccineCode": {
        "coding": [
            {
              "system": "http://hl7.org/fhir/sid/cpt",
              "code": "91306",
              "display": "Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) (coronavirus disease [COVID-19]) vaccine, mRNA-LNP, spike protein, preservative free, 50 mcg/0.25 mL dosage, for intramuscular use"
            },
            {
              "system": "http://hl7.org/fhir/sid/cvx",
              "code": "207",
              "display": "COVID-19, mRNA, LNP-S, PF, 100 mcg/0.5mL dose or 50 mcg/0.25mL dose"
            }
        ]
    },
    "patient": {
        "reference": "Patient/4d789a3d5e794c0eb159a126b48c8b9f",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/76028e14-e77a-47f4-b951-49bf5b7400bb"
    },
    "occurrenceDateTime": "2024-10-04",
    "primarySource": False,
    "note": [
      {
        "text": "First Dose"
      }
    ]
}
```
    {% endtab %}

  {% endtabs %}
</div>

<div id="immunization-update-response">
{% include create-response.html %}
</div>

<div id="immunization-search-request">
{% include search-request.html resource_type="Immunization" search_string="patient=Patient/4d9c4a797b8c4a58872017e7a19a474e" %}
</div>

<div id="immunization-search-response">
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
        "url": "/Immunization?patient=Patient%2F4d9c4a797b8c4a58872017e7a19a474e&_count=10&_offset=0"
      },
      {
        "relation": "first",
        "url": "/Immunization?patient=Patient%2F4d9c4a797b8c4a58872017e7a19a474e&_count=10&_offset=0"
      },
      {
        "relation": "last",
        "url": "/Immunization?patient=Patient%2F4d9c4a797b8c4a58872017e7a19a474e&_count=10&_offset=0"
      }
    ],
    "entry": [
      {
        "resource": {
          "resourceType": "Immunization",
          "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
          "extension": [
            {
              "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
              "valueId": "eb754467-c8fc-4eac-9f36-2f46a510b48f"
            }
          ],
          "status": "completed",
          "vaccineCode": {
            "coding": [
              {
                "system": "http://hl7.org/fhir/sid/cpt",
                "code": "91306",
                "display": "Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) (coronavirus disease [COVID-19]) vaccine, mRNA-LNP, spike protein, preservative free, 50 mcg/0.25 mL dosage, for intramuscular use"
              },
              {
                "system": "http://hl7.org/fhir/sid/cvx",
                "code": "207",
                "display": "COVID-19, mRNA, LNP-S, PF, 100 mcg/0.5mL dose or 50 mcg/0.25mL dose"
              }
            ]
          },
          "patient": {
              "reference": "Patient/4d9c4a797b8c4a58872017e7a19a474e",
              "type": "Patient"
          },
          "encounter": {
            "reference": "Encounter/76028e14-e77a-47f4-b951-49bf5b7400bb"
          },
          "occurrenceDateTime": "2021-12-01",
          "primarySource": false
        }
      },
      {
        "resource": {
          "resourceType": "Immunization",
          "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
          "extension": [
            {
              "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
              "valueId": "eb754467-c8fc-4eac-9f36-2f46a510b48f"
            }
          ],
          "status": "completed",
          "vaccineCode": {
            "coding": [
              {
                  "system": "http://www.ama-assn.org/go/cpt",
                  "code": "90715",
                  "display": "TDAP VACCINE 7 YRS/> IM"
              },
              {
                  "system": "http://hl7.org/fhir/sid/cvx",
                  "code": "115",
                  "display": "Tdap"
              }
            ]
          },
          "patient": {
              "reference": "Patient/4d9c4a797b8c4a58872017e7a19a474e",
              "type": "Patient"
          },
          "encounter": {
            "reference": "Encounter/76028e14-e77a-47f4-b951-49bf5b7400bb"
          },
          "occurrenceDateTime": "2021-12-01",
          "primarySource": false,
          "note": [
            {
              "text": "First Dose"
            }
          ]
        }
      }
    ]
}
```
{% endtab %}
{% tab immunization-search-response 400 %}
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

    {% tab immunization-search-response 401 %}
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

    {% tab immunization-search-response 403 %}
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

