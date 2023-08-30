---
title: Procedure
sections:
  - type: section
    blocks:
      - type: apidoc
        name: procedure
        article: "a"
        description: >-
         An action that is or was performed on or for a patient. This can be a physical intervention like an operation, or less invasive like long term services, counseling, or hypnotherapy.
         Date Filtering
         We support the following date search modifiers:
          - `ge` Example: `"?date=ge2021-01-01"`
            - Greater than or equal to the date.
          - `gt` Example: `"?date=gt2021-01-01"`
            - Strictly greater than the date.
          - `le` Example: `"?date=le2021-01-01"`
            - Less than or equal to the date.
          - `lt` Example: `"?date=lt2021-01-01"`
            - Strictly less than the date.
          - `eq` Example: `"?date=eq2021-01-01"`
            - Strictly equal to the date.
          For more details, see https://hl7.org/fhir/search.html#prefix
        attributes:
          - name: id
            description: >-
              The identifier of the patient
            type: string
            required: true
          - name: status
            description: >-
              A code specifying the state of the procedure.
            type: string
          - name: code
            description: >-
              A code that identifies the procedure.
            type: string
            attributes:
             - name: coding
               type: array
               attributes:
                 - name: system
                   type: string
                 - name: code
                   type: string
                 - name: display
                   type: string
          - name: subject
            description: >-
              The patient who is the focus of this procedure
            type: string
          - name: performedDateTime
            description: >-
              The date and time the procedure was performed
            type: date
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
            description: The patient who is the focus of this procedure
        endpoints: [read, search]
        read:
          responses: [200, 400, 404]
          example_response: procedure-read-response
          example_request: procedure-read-request
        search:
          responses: [200, 400]
          example_response: procedure-search-response
          example_request: procedure-search-request
---
<div id="procedure-read-request">
{% tabs procedure-read-request %}
{% tab procedure-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Procedure/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab procedure-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/procedure/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="procedure-read-response">
{% tabs procedure-read-response %}
{% tab procedure-read-response 200 %}
```json
{
    "resourceType": "Procedure",
    "id": "9789e57b-a645-4a7a-b0d5-284749bd6fb0",
    "status": "unknown",
    "code": {
        "coding": [
            {
                "system": "http://www.ama-assn.org/go/cpt",
                "code": "20600",
                "display": "joint injection small"
            }
        ]
    },
    "subject": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "performedDateTime": "2022-06-02T18:15:04.332367+00:00"
}
```
{% endtab %}
{% tab procedure-read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown Procedure resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="procedure-search-request">
{% tabs procedure-search-request %}
{% tab procedure-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Procedure?patient=Patient/<patient_id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab procedure-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Procedure?patient=Patient/<patient_id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="procedure-search-response">
{% tabs procedure-search-response %}
{% tab procedure-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 7,
    "link": [
        {
            "relation": "self",
            "url": "/Procedure?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Procedure?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Procedure?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Procedure",
                "id": "9789e57b-a645-4a7a-b0d5-284749bd6fb0",
                "status": "unknown",
                "code": {
                    "coding": [
                        {
                            "system": "http://www.ama-assn.org/go/cpt",
                            "code": "20600",
                            "display": "joint injection small"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "performedDateTime": "2022-06-02T18:15:04.332367+00:00"
            }
        },
        {
            "resource": {
                "resourceType": "Procedure",
                "id": "abf44ce9-a71e-4fc4-8ac7-5b4cf9663b05",
                "status": "unknown",
                "code": {
                    "coding": [
                        {
                            "system": "http://www.ama-assn.org/go/cpt",
                            "code": "99213",
                            "display": "Level 3 outpatient visit for evaluation and management of established patient with problem of low to moderate severity, including expanded history and medical decision making of low complexity - typical time with patient and/or family 15 minutes"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "performedDateTime": "2022-05-26T19:00:00+00:00"
            }
        },
        {
            "resource": {
                "resourceType": "Procedure",
                "id": "41ae8ee6-1967-4ec5-ab96-46b14c7c7e6d",
                "status": "unknown",
                "code": {
                    "coding": [
                        {
                            "system": "http://www.ama-assn.org/go/cpt",
                            "code": "99213",
                            "display": "Level 3 outpatient visit for evaluation and management of established patient with problem of low to moderate severity, including expanded history and medical decision making of low complexity - typical time with patient and/or family 15 minutes"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "performedDateTime": "2022-05-12T17:25:19.752069+00:00"
            }
        },
        {
            "resource": {
                "resourceType": "Procedure",
                "id": "25a213a0-75f7-49bb-96f1-84a6945cd6af",
                "status": "unknown",
                "code": {
                    "coding": [
                        {
                            "system": "http://www.ama-assn.org/go/cpt",
                            "code": "36299",
                            "display": "Unlisted procedure vascular injection"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "performedDateTime": "2022-07-08T15:26:17.380076+00:00"
            }
        },
        {
            "resource": {
                "resourceType": "Procedure",
                "id": "e669ed9a-86d2-4a23-8e20-119bd3fae177",
                "status": "unknown",
                "code": {
                    "coding": [
                        {
                            "system": "http://www.ama-assn.org/go/cpt",
                            "code": "99213",
                            "display": "Level 3 - Established Patient - MAT"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "performedDateTime": "2022-08-29T19:05:09.226366+00:00"
            }
        },
        {
            "resource": {
                "resourceType": "Procedure",
                "id": "feff5126-1679-4a93-ad46-fcd95569d74e",
                "status": "unknown",
                "code": {
                    "coding": [
                        {
                            "system": "unstructured",
                            "display": "99453"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "performedDateTime": "2022-12-06T17:49:05.481491+00:00"
            }
        },
        {
            "resource": {
                "resourceType": "Procedure",
                "id": "8ab210e7-de5c-4343-8e70-5a2268e08d94",
                "status": "unknown",
                "code": {
                    "coding": [
                        {
                            "system": "http://www.ama-assn.org/go/cpt",
                            "code": "99490",
                            "display": "CHRON CARE MANAGEMENT SRVC 20 MIN PER MONTH"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "performedDateTime": "2022-12-06T17:49:45.081073+00:00"
            }
        }
    ]
}
```
{% endtab %}
{% tab procedure-search-response 400 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "invalid",
            "details": {
                "text": "patient must contain a resource identifier"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>
