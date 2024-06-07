---
title: Goal
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Goal
        article: "a"
        description: >-
          Describes the intended objective(s) for a patient, group or organization<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-goal.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-goal.html)<br><br>
          To learn more about how to create goals within the Canvas UI see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4415222578067-Goals-Command).
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            type: string
            description: The Canvas identifier of the goal.
          - name: lifecycleStatus
            type: enum [ active | completed | entered-in-error ]
            description: >-
              State the goal is in throughout its lifecycle. <br><br>
              - Goals that have been closed using a Close Goal Command will have a staus of `completed`. <br>
              - Goal commands that were entered-in-error will have a status of `entered-in-error`. <br>
              - All goals that are not closed will have the `active` status.
          - name: achievementStatus
            type: json
            description: Describes progress made on goal, from **http://terminology.hl7.org/CodeSystem/goal-achievement**. This correspondes to the `Status` field on the latest committed goal related command.
            attributes:
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes:
                  - name: system
                    description: The system url of the coding.
                    type: string
                    enum_options:
                      - value: http://terminology.hl7.org/CodeSystem/goal-achievement
                  - name: code
                    description: The code.
                    type: string
                    enum_options:
                      - value: in-progress
                      - value: improving
                      - value: worsening
                      - value: no-change
                      - value: achieved
                      - value: sustaining
                      - value: not-achieved
                      - value: no-progress
                      - value: not-attainable
                  - name: display
                    description: The display name of the coding.
                    type: string
          - name: priority
            type: json
            description: >-
              Level of importance associated with the reaching/sustaining goal, from **http://terminology.hl7.org/CodeSystem/goal-priority**. This correspondes to the `Priority` field on the latest committed goal related command.
            attributes:
              - name: system
                description: The system url of the coding.
                type: string
                enum_options:
                  - value: http://terminology.hl7.org/CodeSystem/goal-achievement
              - name: code
                description: The code.
                type: string
                enum_options:
                  - value: high-priority
                  - value: medium-priority
                  - value: low-priority
              - name: display
                description: The display name of the coding.
                type: string
          - name: description
            type: json
            description: Human readable text of the goal.
            attributes:
              - name: text
                type: string
                description: Plain text representation of the concept.
          - name: subject
            type: json
            description: Canvas Patient resource the goal is for.
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: startDate
            type: date
            description: When goal pursuit begins.
          - name: target
            type: array[json]
            description: A single iteration of this field with the **dueDate**, if available. This correspondes to the `Due date` field on the latest committed goal related command.
            attributes:
              - name: dueDate
                type: date
                description:  Reach goal on or before.
          - name: expressedBy
            type: json
            description: Who created the goal, a **Practitioner** resource. This is the committer of the goal command in the patient's chart.
            attributes:
              - name: reference
                type: string
                description: The reference string of the practitioner in the format of `"Practitioner/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
          - name: note
            type: array[json]
            description: Comments about the goal and who wrote them. Notes correspondes to any progress/barriers submitted on any of goal related commands.
            attributes:
              - name: id
                type: string
                description: The Canvas identifier of the goal's note.
              - name: authorReference
                type: json
                description: Individual responsible for the annotation.
                attributes:
                  - name: reference
                    type: string
                    description: The reference string of the practitioner in the format of `"Practitioner/a39cafb9d1b445be95a2e2548e12a787"`.
                  - name: type
                    type: string
                    description: Type the reference refers to (e.g. "Practitioner").
              - name: time
                type: datetime
                description: When the annotation was made.
              - name: text
                type: string
                description:  The annotation - text content.
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier for a specific goal.
          - name: patient
            type: string
            description: Who this goal is intended for in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
        endpoints: [read, search]
        read:
          responses: [200, 401, 403, 404]
          example_request: goal-read-request
          example_response: goal-read-response
        search:
          responses: [200, 400, 401, 403]
          example_request: goal-search-request
          example_response: goal-search-response
---

<div id="goal-read-request">
{% include read-request.html resource_type="Goal" %}
</div>

<div id="goal-read-response">

  {% tabs goal-read-response %}

    {% tab goal-read-response 200 %}
```json
{
  "resourceType": "Goal",
  "id": "e04a62f8-e6ab-46a1-af34-b635f901e37b",
  "lifecycleStatus": "active",
  "achievementStatus": {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/goal-achievement",
          "code": "improving",
          "display": "Improving"
        }
      ]
  },
  "priority": {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/goal-priority",
          "code": "medium-priority",
          "display": "Medium Priority"
        }
      ]
  },
  "description": {
      "text": "Drink more water"
  },
  "subject": {
      "reference": "Patient/f3d750f5d77d403c96baef6a6055c6e7",
      "type": "Patient"
  },
  "startDate": "2022-01-27",
  "target": [
    {
      "dueDate": "2023-09-28"
    }
  ],
  "expressedBy": {
      "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
      "type": "Practitioner"
  },
  "note": [
    {
      "id": "c2a45d52-b3d7-4e57-bb70-2b82b8819305",
      "authorReference": {
          "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
          "type": "Practitioner"
      },
      "time": "2023-09-19T20:50:25.955348+00:00",
      "text": "Patient unable to find time to drink during work hours, shows signs of dehydration and fatigue"
    }
  ]
}
```
    {% endtab %}

    {% tab goal-read-response 401 %}
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

    {% tab goal-read-response 403 %}
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

    {% tab goal-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Goal resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}
  {% endtabs %}
</div>

<div id="goal-search-request">
{% include search-request.html resource_type="Goal" search_string="patient=Patient/f3d750f5d77d403c96baef6a6055c6e7" %}
</div>

<div id="goal-search-response">
  {% tabs goal-search-response %}

    {% tab goal-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link": [
    {
        "relation": "self",
        "url": "/Goal?patient=Patient/f3d750f5d77d403c96baef6a6055c6e7&_count=10&_offset=0"
      },
      {
        "relation": "first",
        "url": "/Goal?patient=Patient/f3d750f5d77d403c96baef6a6055c6e7&_count=10&_offset=0"
      },
      {
        "relation": "last",
        "url": "/Goal?patient=Patient/f3d750f5d77d403c96baef6a6055c6e7&_count=10&_offset=0"
      }
    ],
    "entry": [
      {
        "resource": {
            "resourceType": "Goal",
            "id": "d942b2b6-5c87-4f95-b7d6-51e2355aabf5",
            "lifecycleStatus": "completed",
            "achievementStatus": {
                "coding": [
                  {
                    "system": "http://terminology.hl7.org/CodeSystem/goal-achievement",
                    "code": "improving",
                    "display": "Improving"
                  }
                ]
            },
            "priority": {
                "coding": [
                  {
                    "system": "http://terminology.hl7.org/CodeSystem/goal-priority",
                    "code": "medium-priority",
                    "display": "Medium Priority"
                  }
                ]
            },
            "description": {
                "text": "Eat one veggie a day"
            },
            "subject": {
                "reference": "Patient/f3d750f5d77d403c96baef6a6055c6e7",
                "type": "Patient"
            },
            "startDate": "2022-12-06",
            "expressedBy": {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                "type": "Practitioner"
            },
            "note": [
              {
                "id": "fe2365c7-1a87-43c3-8846-fc26349a8797",
                "authorReference": {
                    "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                    "type": "Practitioner"
                },
                "time": "2022-12-06T17:21:25.172196+00:00",
                "text": "Not going well only eat skittles"
              }
            ]
        }
      },
      {
        "resource": {
            "resourceType": "Goal",
            "id": "730e38b4-afaf-476c-914c-5eb0b2de405d",
            "lifecycleStatus": "active",
            "achievementStatus": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/goal-achievement",
                  "code": "improving",
                  "display": "Improving"
                }
              ]
            },
            "description": {
                "text": "Walk 3 steps each day"
            },
            "subject": {
                "reference": "Patient/f3d750f5d77d403c96baef6a6055c6e7",
                "type": "Patient"
            },
            "startDate": "2023-03-03",
            "expressedBy": {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                "type": "Practitioner"
            }
          }
      }
    ]
}
```
{% endtab %}

{% tab goal-search-response 400 %}
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

    {% tab goal-search-response 401 %}
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

    {% tab goal-search-response 403 %}
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

