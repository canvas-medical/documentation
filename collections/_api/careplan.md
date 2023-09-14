---
title: CarePlan
sections:
  - type: section
    blocks:
      - type: apidoc
        name: CarePlan
        article: "a"
        description: >-
          Describes the intention of how one or more practitioners intend to deliver care for a particular patient, group or community for a period of time, possibly limited to care for a specific condition or set of conditions.<br><br>
          [https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-careplan.html](https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-careplan.html)
        attributes:
          - name: id
            description: >-
              The identifier of the CarePlan
            type: string
          - name: status
            description: >-
              Indicates whether the plan is currently being acted upon, represents future intentions or is now a historical record.
            type: string
          - name: intent
            description: >-
              Indicates the level of authority/intentionality associated with the care plan and where the care plan fits into the workflow chain.
            type: string
          - name: category
            description: >-
              Type of plan.
            type: json
          - name: subject
            description: >-
              Who care plan is for.
            type: json
        search_parameters:
          - name: _id
            type: string
            description: The unique Canvas identifier of the CarePlan
          - name: category
            type: string
            description: A category code in the format `system|code`
          - name: patient
            type: string
            description: FHIR resource for a patient
        endpoints: [read, search]
        read:
          description: Read a CarePlan resource.
          responses: [200, 404]
          example_request: care-plan-read-request
          example_response: care-plan-read-response
        search:
          description: Search for CarePlan resources.
          responses: [200, 400]
          example_request: care-plan-search-request
          example_response: care-plan-search-response
---
<div id="care-plan-read-request">
  {% tabs care-plan-read-request %}
    {% tab care-plan-read-request curl %}
    ```shell
    curl --request GET \
         --url https://fumage-example.canvasmedical.com/CarePlan/<id> \
         --header 'Authorization: Bearer <token>' \
         --header 'accept: application/json'
    ```
    {% endtab %}
    {% tab care-plan-read-request python %}
    ```python
    import requests
    
    url = "https://fumage-example.canvasmedical.com/CarePlan/<id>"
    
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

<div id="care-plan-read-response">
  {% tabs care-plan-read-response %}
    {% tab care-plan-read-response 200 %}
      ```json
      {
          "resourceType": "CarePlan",
          "id": "b4190e86-1a63-4010-85fe-5c42b607d2f9",
          "text": {
              "status": "generated",
              "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">CarePlan</div><table class=\"hapiPropertyTable\"><tbody><tr><td>Coding</td><td>{'system': 'http://snomed.info/sct', 'code': '734163000', 'display': 'Care plan'}</td></tr><tr><td>For Patient Name</td><td><span>Cube, Rubik N. (Nick Name)</span></td></tr></tbody></table></div>"
          },
          "status": "active",
          "intent": "plan",
          "category": [
              {
                  "coding": [
                      {
                          "system": "http://hl7.org/fhir/us/core/CodeSystem/careplan-category",
                          "code": "assess-plan"
                      }
                  ]
              },
              {
                  "coding": [
                      {
                          "system": "http://snomed.info/sct",
                          "code": "734163000",
                          "display": "Care plan"
                      }
                  ]
              }
          ],
          "subject": {
              "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
              "type": "Patient"
          }
      }
      ``` 
    {% endtab %}
    {% tab care-plan-read-response 404 %}
      ```json
      {
          "resourceType": "OperationOutcome",
          "issue": [
              {
                  "severity": "error",
                  "code": "not-found",
                  "details": {
                      "text": "Unknown CarePlan resource '7d1ce256fcd7408193b0459650937a07'"
                  }
              }
          ]
      }
      ```
    {% endtab %}
  {% endtabs %}
</div>

<div id="care-plan-search-request">
  {% tabs care-plan-search-request %}
    {% tab care-plan-search-request python %}
      ```python
      import requests

      url = "https://fumage-example.canvasmedical.com/CarePlan?patient=Patient%2F11430ad243f84ad2a47b1267d33ce9b8&category=http%3A%2F%2Fhl7.org%2Ffhir%2Fus%2Fcore%2FCodeSystem%2Fcareplan-category%7Cassess-plan"

      headers = {
          "accept": "application/json",
          "Authorization": "Bearer <token>"
      }

      response = requests.get(url, headers=headers)

      print(response.text)
      ```
    {% endtab %}
    {% tab care-plan-search-request curl %}
      ```sh
      curl --request GET \
          --url 'https://fumage-example.canvasmedical.com/CarePlan?patient=Patient%2F11430ad243f84ad2a47b1267d33ce9b8&category=http%3A%2F%2Fhl7.org%2Ffhir%2Fus%2Fcore%2FCodeSystem%2Fcareplan-category%7Cassess-plan' \
          --header 'Authorization: Bearer <token>' \
          --header 'accept: application/json'
      ```
    {% endtab %}
  {% endtabs %}
</div>

<div id="care-plan-search-response">
  {% tabs care-plan-search-response %}
    {% tab care-plan-search-response 200 %}
      ```json
      {
          "resourceType": "Bundle",
          "type": "searchset",
          "total": 1,
          "link": [
              {
                  "relation": "self",
                  "url": "/CarePlan?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
              },
              {
                  "relation": "first",
                  "url": "/CarePlan?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
              },
              {
                  "relation": "last",
                  "url": "/CarePlan?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
              }
          ],
          "entry": [
              {
                  "resource": {
                      "resourceType": "CarePlan",
                      "id": "b4190e86-1a63-4010-85fe-5c42b607d2f9",
                      "text": {
                          "status": "generated",
                          "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">CarePlan</div><table class=\"hapiPropertyTable\"><tbody><tr><td>Coding</td><td>{'system': 'http://snomed.info/sct', 'code': '734163000', 'display': 'Care plan'}</td></tr><tr><td>For Patient Name</td><td><span>Cube, Rubik N. (Nick Name)</span></td></tr></tbody></table></div>"
                      },
                      "status": "active",
                      "intent": "plan",
                      "category": [
                          {
                              "coding": [
                                  {
                                      "system": "http://hl7.org/fhir/us/core/CodeSystem/careplan-category",
                                      "code": "assess-plan"
                                  }
                              ]
                          },
                          {
                              "coding": [
                                  {
                                      "system": "http://snomed.info/sct",
                                      "code": "734163000",
                                      "display": "Care plan"
                                  }
                              ]
                          }
                      ],
                      "subject": {
                          "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                          "type": "Patient"
                      }
                  }
              }
          ]
      }
      ```
    {% endtab %}
    {% tab care-plan-search-response 400 %}
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
  {% endtabs %}
</div>