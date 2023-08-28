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
          - name: clinicalStatus
            type: json
          - name: verificationStatus
            type: json
          - name: category
            type: json
          - name: code
            type: json
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
          example_response: condition-read-response
          example_request: condition-read-request
        search:
          responses: [200, 401, 403]
          example_response: condition-search-response
          example_request: condition-search-request
        create:
          responses: [201, 401, 403]
          example_response: condition-create-response
          example_request: condition-create-request
        update:
          responses: [200, 401, 403]
          example_response: condition-update-response
          example_request: condition-update-request

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
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 0
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
    "total": 0
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
{
  "Created"
}
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
{ 
  "detail": "Updated"
}
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

