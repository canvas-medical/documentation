---
title: QuestionnaireResponse
sections:
  - type: section
    blocks:
      - type: apidoc
        name: QuestionnaireResponse
        article: "a"
        description: >-
          A structured set of questions and their answers. The questions are ordered and grouped into coherent subsets, corresponding to the structure of the grouping of the questionnaire being responded to.<br><br>
          [https://hl7.org/fhir/R4/questionnaireresponse.html](https://hl7.org/fhir/R4/questionnaireresponse.html)<br><br>
          See this [article](https://canvas-medical.help.usepylon.com/articles/7418371785-creating-a-new-questionnaire) for information about how to build questionnaires in Canvas.<br><br>
          Questionnaires can map to four different commands in the Canvas UI depending on what the use case in charting is set to: 

            - [Questionnaire](https://canvas-medical.help.usepylon.com/articles/5651999344-command-questionnaire)
            - [Structured Assessment](https://canvas-medical.help.usepylon.com/articles/8805008571-command-structured-assessment)
            - [Review of Systems](https://canvas-medical.help.usepylon.com/articles/9046024531-command-review-of-systems)
            - [Physical Exam](https://canvas-medical.help.usepylon.com/articles/1745103290-command-physical-exam)

          QuestionnaireResponse resources contain answers to questions in a Questionnaire resource. Use the [Questionnaire search endpoint](/api/questionnaire/#search) to find Questionnaire resources.
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the QuestionnaireResponse.
            type: string
            required_in: update
            exclude_in: create
          - name: extension
            type: array[json]
            description_for_all_endpoints: >-
              Additional content defined by implementations<br><br>
              Canvas supports a note identifier extension on this resource for create, read, update, and search interactions. The note identifier can be used with the [Canvas Note API](/api/note).<br>
               **Important:** For create interactions, Canvas recommends sending the note identifier extension or the Encounter reference, but not both. If both are supplied, they must both refer to the same note.<br>
            read_and_search_description: The Questionnaire permalink is included in the `extension` attribute. This will take you directly to the command in the patient's chart. 
            attributes:
                - name: url
                  type: string
                  required_in: create,update
                  description: >-
                    Reference that defines the content of this object. 
                  enum_options:
                    - value: For permalinks which have a url of `http://schemas.canvasmedical.com/fhir/extensions/questionnaire-permalink`
                      exclude_in: create, update
                    - value: For note identifier we have a url of `http://schemas.canvasmedical.com/fhir/extensions/note-id`
                - name: valueString
                  type: string
                  exclude_in: create, update
                  description: >-
                    The permalink extension will have a `valueString` returned that represents a url. This url will take you to the exact command in the Canvas UI the response is captured. It will look like `https://<customer-identifier>.canvasmedical.com/permalinks/v1/SW50ZXJ2aWV3OjUxOjc1NTU=`
                - name: valueId
                  type: string
                  description: The valueId field is used for the Note extension and will be the note's unique identifier
          - name: questionnaire
            required_in: create,update
            description: >-
              Form being answered.<br><br>
              The `questionnaire` field contains a value that is formatted like a Questionnaire reference, e.g. `Questionnaire/ac1da1a4-ccc4-492e-a9e0-7f70a58c2129`. Questionnaire IDs can be obtained using the [Questionnaire search endpoint](/api/questionnaire/#search).
            type: string
          - name: status
            required_in: create,update
            description: >-
              The position of the questionnaire response within its overall lifecycle.
            enum_options:
              - value: completed
                exclude_in: update
              - value: entered-in-error
                exclude_in: create
            type: string
          - name: subject
            required_in: create,update
            description: The subject of the questions.
            type: json
            attributes:
                - name: reference
                  type: string
                  required_in: create,update
                  description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Patient")
          - name: encounter
            description: >-
              Encounter created as part of.<br><br>
              If `encounter` is provided, the QuestionnaireResponse will be added to the existing encounter (note). If it is not provided, a new data import note will be created. It will be inserted into the timeline using the timestamp passed in `authored`.<br><br>
              **Canvas does not currently support concurrent creation of resources on the same encounter.** Please avoid issuing concurrent requests that reference the same encounter to this endpoint, or to any other endpoints that reference encounters. It is OK to issue concurrent requests to these endpoints as long as the requests reference different encounters.
            type: json
            attributes:
                - name: reference
                  type: string
                  required_in: create,update
                  description: The reference string of the encounter in the format of `"Encounter/cdbd6534-ba0d-4917-a5a6-6a2d46dcf0f7"`
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Encounter")
          - name: authored
            description_for_all_endpoints: >-
              Note datetime of service where the answers are associated with in ISO 8601 format like `"2022-03-19T14:54:12.194952+00:00"`.<br><br>
            create_description: If omitted, the current timestamp will be used.
            type: datetime
          - name: author
            description: >-
              Person who received and recorded the answers.<br><br>
              If omitted, then the built-in automation user **Canvas Bot** will be set as the author.<br><br>
              Supported reference types for create operations are: **Patient**, **Practitioner**
            type: json
            attributes:
                - name: reference
                  type: string
                  required_in: create,update
                  description: The reference string of the author in the format of `"Practitioner/cdbd6534-ba0d-4917-a5a6-6a2d46dcf0f7"`
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Patient", "Practitioner")
          - name: item
            description: >-
              Groups and questions<br><br>
              The `item` attribute contains the answers to the questions in the Questionnaire. The `item` attribute in QuestionnaireResponse corresponds to the `item` attribute in Questionnaire payload, and are related via the `linkId` attribute. If a question's answer is omitted, it will be left unanswered in Canvas. However, if it is a questionnaire tied to a scoring function, Canvas requires all questions to be answered in order to accurately score the Questionnaire.<br><br>
              Each `item` must contain a `linkId` and `answer` attributes. The `answer` attribute is a list of answers for the question referred to by the `linkId`.<br><br>
              Canvas supports the following question formats:<br><br>
              • Free text<br>
              • Single choice<br>
              • Multiple choice<br><br>
              Answers to free text questions are provided as a `valueString`. Answers to single and multiple choice questions are provided as a `valueCoding`. See the request and response examples for more information.<br><br>
              The following mappings show how the FHIR system URI is mapped to the Canvas system (FHIR -> Canvas):<br><br>

                | FHIR system uri                                                        | Canvas system value |
                |------------------------------------------------------------------------|---------------------|
                | http://loinc.org                                                       | LOINC               |
                | http://snomed.info/sct                                                 | SNOMED              |
                | http://canvasmedical.com                                               | CANVAS              |
                | http://www.ama-assn.org/go/cpt                                         | CPT                 | 
                | http://hl7.org/fhir/sid/icd-10                                         | ICD-10              | 
                | http://schemas.{instance-name}.canvasmedical.com/fhir/systems/internal | INTERNAL            |
            type: array[json]
            attributes:
                - name: linkId
                  type: string
                  required_in: create,update
                  description: A Canvas assigned identifier that uniquely identifies this question in Canvas. This linkId must only occur at most once in the payload. You can retrieve this from FHIR Questionnaire Search/Read
                - name: text
                  type: string
                  description: Human readable text of the question. Not stored but can be helpful to include for troubleshooting.
                - name: answer
                  type: array[json]
                  required_in: create,update
                  description: A list of one or more answers to this question.
                  attributes:
                    - value: valueString
                      description: For question where the answer is a free-text field (i.e. Questionnaire item type = "text"), then the list will contain a single object containing a valueString field with the response text.
                    - value: valueCoding
                      description: For a question where the answer is a single or multiple choice selection (i.e. Questionnaire item `type` = "choice" and `repeats` is "false" for single or "true" for multiple), then the list will have one or more ValueCoding objects. You can retrieve these coding options in the Questionnaire Read/Search endpoint.
                      attributes:
                        - name: system
                          description: The system url of the coding.
                          enum_options:
                             - value: http://loinc.org
                             - value: http://snomed.info/sct
                             - value: http://canvasmedical.com
                             - value: http://www.ama-assn.org/go/cpt
                             - value: http://hl7.org/fhir/sid/icd-10
                             - value: http://schemas.{customer_identifier}.canvasmedical.com/fhir/systems/internal
                          type: string
                          required_in: create, update
                        - name: code
                          description: The code of the answer.
                          type: string
                          required_in: create, update
                        - name: display
                          description: The display name of the coding.
                          type: string
                          required_in: create, update
        search_parameters:
          - name: _id
            description: The identifier of the QuestionnaireResponse.
            type: string
          - name: authored
            description: >-
              Filter by the `authored` attribute. See [Date Filtering](/api/date-filtering) for more information.
            type: datetime
          - name: patient
            description: The patient that is the subject of the questionnaire response in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
          - name: questionnaire
            description: The questionnaire the answers are provided for in the format "Questionnaire/7eefd6fc-0000-44c2-8224-d95f0ceaa2fd".
            type: string
          - name: questionnaire.code
            description: Filters by the code and/or system of the associated questionnaire. You can search by just the code value or you can search by the system and code in the format `system|code` (e.g `http://snomed.info/sct|404684003`).
            type: string
          - name: questionnaire.item.code
            description: Filters by the code and/or system of questions in the questionnaire. You can search by just the code value or you can search by the system and code in the format `system|code` (e.g `http://snomed.info/sct|404684003`).
            type: string
          - name: _sort
            description: Triggers sorting of the results by a specific criteria. The results will be in ascending order unless you add a `-` in front to sort in descending order. 
            search_options:
              - value: _id
              - value: authored
            type: string
        endpoints: [create, read, update, search]
        create:
          description: >-
            Create an QuestionnaireResponse resource.
          validation_errors: >-
            **Validation Errors**<br><br>
            *Beware of ambiguous choices!*<br><br>
            If the questionnaire contains a question with identical codings for different choices, Canvas will not know which of the choices were selected. In this case, Canvas will reject the request. For the request to succeed, each question must have a uniquely coded set of choices. Choice codings can be reused across questions, but not within them.If this scenario occurs, you will get the error message: `Question received a response option code: {code} that belongs to more than one option response`<br><br>
            *More Coding Validation*<br><br>
            The system is the `valueCoding` answer needs to match the system that the question specified in the Questionnaire Search Response. If it does not, you will get the error: `Question expects answer of code system {system} but {system} was given`<br><br>
            If a code is passed that does not exist for that question in Canvas, you will get the error: `Question received an invalid response option code: {code}`<br><br>
            *Answer Validation*<br><br>
            For single or free text questions, if more than one answer is provided, you will get the error: `Question of type {type} is expecting at most one answer`<br><br>
            For free text questions, the answer object must include a `valueString` or you will get the error: `Question of type TXT expects a valueString answer`<br><br>
            For single or multiple choice questions, the answer objects must include a `valueCoding` or you will see one of these errors:<br>
            `Question of type SING expects a valueCoding answer`<br>
            `Question of type MULT expects a valueCoding answer`
          responses: [201, 400, 401, 403, 405, 422]
          example_request: questionnaireresponse-create-request
          example_response: questionnaireresponse-create-response
        read:
          description: Read an QuestionnaireResponse resource.
          responses: [200, 401, 403, 404]
          example_request: questionnaireresponse-read-request
          example_response: questionnaireresponse-read-response
        update:
          description: >-
            Update a QuestionnaireResponse resource.<br><br>
            The only type of QuestionnaireResponse update interaction that is supported by Canvas is to mark an existing QuestionnaireResponse as **entered-in-error**. No changes to other fields will be processed.
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: questionnaireresponse-update-request
          example_response: questionnaireresponse-update-response
        search:
          description: Search for QuestionnaireResponse resources.
          responses: [200, 400, 401, 403]
          example_request: questionnaireresponse-search-request
          example_response: questionnaireresponse-search-response
---

<div id="questionnaireresponse-create-request">

  {% tabs questionnaireresponse-create-request %}

    {% tab questionnaireresponse-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/QuestionnaireResponse' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "QuestionnaireResponse",
    "id": "e76e44b4-4e68-4f72-b1c3-1de528a3bb2a",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "questionnaire": "Questionnaire/7eefd6fc-0000-44c2-8224-d95f0ceaa2fd",
    "status": "completed",
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/ffa0bd44-997f-4ad4-8782-1a6c0ef01f1c",
        "type": "Encounter"
    },
    "authored": "2022-12-19T18:11:20.914260+00:00",
    "author": {
        "reference": "Practitioner/9cdb7a92d6614dcfa7948f2143a9f8e8",
        "type": "Practitioner"
    },
    "item": [
        {
            "linkId": "e2e5ddc3-a0ec-4a1b-9c53-bf2e2e990fe1",
            "text": "Tobacco status",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "8517006",
                        "display": "Former user"
                    }
                }
            ]
        },
        {
            "linkId": "d210dc3a-3427-4f58-8707-3f38393a8416",
            "text": "Tobacco type",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722496004",
                        "display": "Cigarettes"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722498003",
                        "display": "eCigarette"
                    }
                }
            ]
        },
        {
            "linkId": "a656c6c8-ecea-403f-a430-f80899f26914",
            "text": "Tobacco comment",
            "answer": [
                {
                    "valueString": "Yep"
                }
            ]
        }
    ]
}'
```
    {% endtab %}

    {% tab questionnaireresponse-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/QuestionnaireResponse"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "QuestionnaireResponse",
    "id": "e76e44b4-4e68-4f72-b1c3-1de528a3bb2a",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "questionnaire": "Questionnaire/7eefd6fc-0000-44c2-8224-d95f0ceaa2fd",
    "status": "completed",
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/ffa0bd44-997f-4ad4-8782-1a6c0ef01f1c",
        "type": "Encounter"
    },
    "authored": "2022-12-19T18:11:20.914260+00:00",
    "author": {
        "reference": "Practitioner/9cdb7a92d6614dcfa7948f2143a9f8e8",
        "type": "Practitioner"
    },
    "item": [
        {
            "linkId": "e2e5ddc3-a0ec-4a1b-9c53-bf2e2e990fe1",
            "text": "Tobacco status",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "8517006",
                        "display": "Former user"
                    }
                }
            ]
        },
        {
            "linkId": "d210dc3a-3427-4f58-8707-3f38393a8416",
            "text": "Tobacco type",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722496004",
                        "display": "Cigarettes"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722498003",
                        "display": "eCigarette"
                    }
                }
            ]
        },
        {
            "linkId": "a656c6c8-ecea-403f-a430-f80899f26914",
            "text": "Tobacco comment",
            "answer": [
                {
                    "valueString": "Yep"
                }
            ]
        }
    ]
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="questionnaireresponse-create-response">
{% include create-response.html %}
</div>

<div id="questionnaireresponse-read-request">
{%  include read-request.html resource_type="QuestionnaireResponse" %}
</div>

<div id="questionnaireresponse-read-response">

  {% tabs questionnaireresponse-read-response %}

    {% tab questionnaireresponse-read-response 200 %}
```json
{
    "resourceType": "QuestionnaireResponse",
    "id": "e76e44b4-4e68-4f72-b1c3-1de528a3bb2a",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/questionnaire-permalink",
            "valueString": "https://example.canvasmedical.com/permalinks/v1/YWJjZGVmZ2hpamtsbW5vcHFycwo"
        }
    ],
    "questionnaire": "Questionnaire/7eefd6fc-0000-44c2-8224-d95f0ceaa2fd",
    "status": "completed",
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/ffa0bd44-997f-4ad4-8782-1a6c0ef01f1c",
        "type": "Encounter"
    },
    "authored": "2022-12-19T18:11:20.914260+00:00",
    "author": {
        "reference": "Practitioner/9cdb7a92d6614dcfa7948f2143a9f8e8",
        "type": "Practitioner"
    },
    "item": [
        {
            "linkId": "e2e5ddc3-a0ec-4a1b-9c53-bf2e2e990fe1",
            "text": "Tobacco status",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "8517006",
                        "display": "Former user"
                    }
                }
            ]
        },
        {
            "linkId": "d210dc3a-3427-4f58-8707-3f38393a8416",
            "text": "Tobacco type",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722496004",
                        "display": "Cigarettes"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722498003",
                        "display": "eCigarette"
                    }
                }
            ]
        },
        {
            "linkId": "a656c6c8-ecea-403f-a430-f80899f26914",
            "text": "Tobacco comment",
            "answer": [
                {
                    "valueString": "Yep"
                }
            ]
        }
    ]
}
```
    {% endtab %}

    {% tab questionnaireresponse-read-response 401 %}
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

    {% tab questionnaireresponse-read-response 403 %}
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

    {% tab questionnaireresponse-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown QuestionnaireResponse resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="questionnaireresponse-update-request">

  {% tabs questionnaireresponse-update-request %}

    {% tab questionnaireresponse-update-request curl %}
```shell
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/QuestionnaireResponse/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "QuestionnaireResponse",
    "id": "e76e44b4-4e68-4f72-b1c3-1de528a3bb2a",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "questionnaire": "Questionnaire/7eefd6fc-0000-44c2-8224-d95f0ceaa2fd",
    "status": "entered-in-error",
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/ffa0bd44-997f-4ad4-8782-1a6c0ef01f1c",
        "type": "Encounter"
    },
    "authored": "2022-12-19T18:11:20.914260+00:00",
    "author": {
        "reference": "Practitioner/9cdb7a92d6614dcfa7948f2143a9f8e8",
        "type": "Practitioner"
    },
    "item": [
        {
            "linkId": "e2e5ddc3-a0ec-4a1b-9c53-bf2e2e990fe1",
            "text": "Tobacco status",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "8517006",
                        "display": "Former user"
                    }
                }
            ]
        },
        {
            "linkId": "d210dc3a-3427-4f58-8707-3f38393a8416",
            "text": "Tobacco type",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722496004",
                        "display": "Cigarettes"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722498003",
                        "display": "eCigarette"
                    }
                }
            ]
        },
        {
            "linkId": "a656c6c8-ecea-403f-a430-f80899f26914",
            "text": "Tobacco comment",
            "answer": [
                {
                    "valueString": "Yep"
                }
            ]
        }
    ]
}'
```
    {% endtab %}

    {% tab questionnaireresponse-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/QuestionnaireResponse/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "QuestionnaireResponse",
    "id": "e76e44b4-4e68-4f72-b1c3-1de528a3bb2a",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "questionnaire": "Questionnaire/7eefd6fc-0000-44c2-8224-d95f0ceaa2fd",
    "status": "entered-in-error",
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
        "type": "Patient"
    },
    "encounter": {
        "reference": "Encounter/ffa0bd44-997f-4ad4-8782-1a6c0ef01f1c",
        "type": "Encounter"
    },
    "authored": "2022-12-19T18:11:20.914260+00:00",
    "author": {
        "reference": "Practitioner/9cdb7a92d6614dcfa7948f2143a9f8e8",
        "type": "Practitioner"
    },
    "item": [
        {
            "linkId": "e2e5ddc3-a0ec-4a1b-9c53-bf2e2e990fe1",
            "text": "Tobacco status",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "8517006",
                        "display": "Former user"
                    }
                }
            ]
        },
        {
            "linkId": "d210dc3a-3427-4f58-8707-3f38393a8416",
            "text": "Tobacco type",
            "answer": [
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722496004",
                        "display": "Cigarettes"
                    }
                },
                {
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": "722498003",
                        "display": "eCigarette"
                    }
                }
            ]
        },
        {
            "linkId": "a656c6c8-ecea-403f-a430-f80899f26914",
            "text": "Tobacco comment",
            "answer": [
                {
                    "valueString": "Yep"
                }
            ]
        }
    ]
}
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="questionnaireresponse-update-response">
{% include update-response.html resource_type="QuestionnaireResponse" %}
</div>

<div id="questionnaireresponse-search-request">
{% include search-request.html resource_type="QuestionnaireResponse" search_string="patient=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="questionnaireresponse-search-response">

  {% tabs questionnaireresponse-search-response %}

    {% tab questionnaireresponse-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/QuestionnaireResponse?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/QuestionnaireResponse?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/QuestionnaireResponse?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "QuestionnaireResponse",
                "id": "e76e44b4-4e68-4f72-b1c3-1de528a3bb2a",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
                        "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/questionnaire-permalink",
                        "valueString": "https://example.canvasmedical.com/permalinks/v1/YWJjZGVmZ2hpamtsbW5vcHFycwo"
                    }
                ],
                "questionnaire": "Questionnaire/7eefd6fc-0000-44c2-8224-d95f0ceaa2fd",
                "status": "completed",
                "subject": {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
                    "type": "Patient"
                },
                "encounter": {
                    "reference": "Encounter/ffa0bd44-997f-4ad4-8782-1a6c0ef01f1c",
                    "type": "Encounter"
                },
                "authored": "2022-12-19T18:11:20.914260+00:00",
                "author": {
                    "reference": "Practitioner/9cdb7a92d6614dcfa7948f2143a9f8e8",
                    "type": "Practitioner"
                },
                "item": [
                    {
                        "linkId": "e2e5ddc3-a0ec-4a1b-9c53-bf2e2e990fe1",
                        "text": "Tobacco status",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "8517006",
                                    "display": "Former user"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "d210dc3a-3427-4f58-8707-3f38393a8416",
                        "text": "Tobacco type",
                        "answer": [
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "722496004",
                                    "display": "Cigarettes"
                                }
                            },
                            {
                                "valueCoding": {
                                    "system": "http://snomed.info/sct",
                                    "code": "722498003",
                                    "display": "eCigarette"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "a656c6c8-ecea-403f-a430-f80899f26914",
                        "text": "Tobacco comment",
                        "answer": [
                            {
                                "valueString": "Yep"
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
```
    {% endtab %}

    {% tab questionnaireresponse-search-response 400 %}
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

    {% tab questionnaireresponse-search-response 401 %}
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

    {% tab questionnaireresponse-search-response 403 %}
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
