---
title: Patient
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Patient
        article: "a"
        description: >-
          Demographics and other administrative information about an individual or animal receiving care or other health-related services.
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
          - name: extension
            type: json
            required: true
          - name: identifier
            type: json
            required: false
          - name: active
            type: boolean
            required: false
          - name: name
            type: json
            required: true
          - name: telecom
            type: json
            required: false
            attributes:
              - name: id
                type: string
              - name: extension
                type: array
                attributes:
                  - name: url
                    type: string
                  - name: valueBoolean
                    type: boolean
              - name: system
                type: string
              - name: value
                type: string
              - name: use
                type: string
              - name: rank
                type: string
          - name: gender
            description: >-
              Default: male
            type: string
            required: false
          - name: birthDate
            type: date
            required: false
          - name: deceasedBoolean
            type: boolean
            required: false
          - name: address
            type: json
            required: false
            attributes:
              - name: id
                type: string
              - name: use
                type: string
              - name: type
                type: string
              - name: line
                type: string
              - name: city
                type: string
              - name: state
                type: string
              - name: postalCode
                type: string
              - name: country
                type: string
              - name: period
                type: json
                attributes:
                  - name: start
                    type: date
                  - name: end
                    type: date
          - name: photo
            type: string
            required: false
            attributes:
              - name: url
                type: string
          - name: contact
            type: json
            required: false
            attributes:
              - name: id
                type: string
              - name: name
                type: json
                attributes:
                  - name: text
                    type: string
              - name: relationship
                type: json
                attributes:
                  - name: text
                    type: string
              - name: telecom
                type: json
                attributes:
                  - name: system
                    type: string
                  - name: value
                    type: string
              - name: extension
                type: array
                attributes:
                  - name: url
                    type: string
                  - name: valueBoolean
                    type: boolean
          - name: communication
            type: json
            required: false
            attributes:
              - name: language
                type: json
                attributes:
                  - name: coding
                    type: json
                    attributes:
                      - name: system
                        type: string
                      - name: code
                        type: string
                      - name: display
                        type: string
                  - name: text
                    type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: identifier
            type: string
            description: The Canvas-issued MRN or a saved identifier from an external system
          - name: name
            type: string
            description: Part of a first or last name
          - name: birthdate
            type: date
            description: The patient's birthdate
          - name: sexAtBirth
            type: string
          - name: family
            type: string
            description: Last name
          - name: given
            type: string
            description: First Name
          - name: email
            type: string
            description: Patient email address
          - name: phone
            type: string
            description: Patient phone number, expected to be 10 digits
          - name: active
            type: boolean
            description: By default, both active and inactive patients are returned. Use this parameter to only return active (true) or inactive (false)
          - name: nickname
            type: string
            description: Preferred or alternate name
          - name: hasCareTeamMember
            type: boolean
            description: If true, only return patients that have a care team member
        endpoints: [read, search, create]
        read:
          example_request: patient-read-request
          example_response: patient-read-response
          responses: [200, 400]
        search:
          example_request: patient-search-request
          example_response: patient-search-response
          responses: [200, 400]
        create:
          example_request: patient-create-request
          example_response: patient-create-response
          responses: [200, 400]
        update:  
          example_request: patient-update-request
          example_response: patient-update-response
          responses: [200, 400]
---


<div id="patient-read-request">
{% tabs patient-read-request %}
{% tab patient-read-request python %}
```sh
import requests
import json

url = "{{base_url}}/Patient/797e5f30447545a4823fe1c8ebcd0ba6/"

payload={}
headers = {
  'Content-Type': 'application/fhir+json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```
{% endtab %}
{% tab patient-read-request curl %}
```sh
curl --request GET \
     --url https://fhir-example.canvasmedical.com/Patient/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="patient-read-response">
{% tabs patient-read-response %}
{% tab patient-read-response 200 %}
```json
200 {
  ...
}
```
{% endtab %}
{% tab patient-read-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="patient-search-request">
{% tabs patient-search-request %}
{% tab patient-search-request python %}
```sh
import requests

url = "{{base_url}}/Patient?_id=797e5f30447545a4823fe1c8ebcd0ba6"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```
{% endtab %}
{% tab patient-search-request curl %}
```sh
curl --request GET \
     --url https://fhir-example.canvasmedical.com/Patient \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="patient-search-response">
{% tabs patient-search-response %}
{% tab patient-search-response 200 %}
```json
200 {
  ...

}
```
{% endtab %}
{% tab search-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="patient-create-request">
{% tabs patient-create-request %}
{% tab patient-create-request python %}
```sh
import requests

url = "{{base_url}}/Patient"

payload = "{\n    \"resourceType\": \"Patient\",\n    \"extension\": [\n        {\n            \"url\": \"http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex\",\n            \"valueCode\": \"M\"\n        },\n        {\n            \"url\" : \"http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy\",\n            \"extension\": [\n                {\n                    \"url\": \"ncpdp-id\",\n                    \"valueIdentifier\": {\n                        \"value\": \"1123152\",\n                        \"system\": \"http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber\"\n                    }\n                }\n            ]\n        },\n        {\n            \"url\": \"http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity\",\n            \"extension\": [\n                {\n                    \"url\": \"text\",\n                    \"valueString\": \"UNK\"\n                }\n            ]\n        },\n        {\n            \"url\": \"http://hl7.org/fhir/us/core/StructureDefinition/us-core-race\",\n            \"extension\": [\n                {\n                    \"url\": \"text\",\n                    \"valueString\": \"UNK\"\n                }\n            ]\n        },\n        {\n            \"url\": \"http://hl7.org/fhir/StructureDefinition/tz-code\",\n            \"valueCode\": \"America/New_York\"\n        },\n        {\n            \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/clinical-note\",\n            \"valueString\": \"I am a clinical caption from a Create message\"\n        },\n        {\n            \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/administrative-note\",\n            \"valueString\": \"I am an administrative caption from a Create message\"\n        }\n    ],\n    \"identifier\": [\n        {\n            \"use\": \"usual\",\n            \"system\": \"HealthCo\",\n            \"value\": \"s07960990\"\n        }\n    ],\n    \"active\": true,\n    \"name\": [\n        {\n            \"use\": \"official\",\n            \"family\": \"Bahar\",\n            \"given\": [\n                \"Issam\",\n                \"Khuzaimah\"\n            ]\n        },\n        {\n            \"use\": \"nickname\",\n            \"given\": [\n                \"Nick Name\"\n            ]\n        }\n    ],\n    \"telecom\": [\n        {\n            \"system\": \"phone\",\n            \"value\": \"5554320555\",\n            \"use\": \"mobile\",\n            \"rank\": 1\n        },\n        {\n            \"system\": \"email\",\n            \"value\": \"i.k.bahar@example.com\",\n            \"use\": \"work\",\n            \"rank\": 1\n        }\n    ],\n    \"gender\": \"male\",\n    \"birthDate\": \"1949-11-13\",\n    \"address\": [\n        {\n            \"use\": \"home\",\n            \"type\": \"both\",\n            \"text\": \"4247 Murry Street, Chesapeake, VA 23322\",\n            \"line\": [\n                \"4247 Murry Street\"\n            ],\n            \"city\": \"Chesapeake\",\n            \"state\": \"VA\",\n            \"postalCode\": \"23322\"\n        }\n    ],\n    \"contact\": [\n        {\n            \"name\": {\n                \"text\": \"Test Spouse\"\n            },\n            \"relationship\": [\n                {\n                    \"text\": \"Spouse\"\n                }\n            ],\n            \"telecom\": [\n                {\n                    \"system\": \"email\",\n                    \"value\": \"test@me.com\"\n                }\n            ],\n            \"extension\": [\n                {\n                    \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/emergency-contact\",\n                    \"valueBoolean\": true\n                },\n                {\n                    \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information\",\n                    \"valueBoolean\": true\n                }\n            ]\n        },\n        {\n            \"name\": {\n                \"text\": \"Test Mom\"\n            },\n            \"relationship\": [\n                {\n                    \"text\": \"Mom\"\n                }\n            ],\n            \"telecom\": [\n                {\n                    \"system\": \"phone\",\n                    \"value\": \"7177327068\"\n                }\n            ],\n            \"extension\": [\n                {\n                    \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information\",\n                    \"valueBoolean\": true\n                }\n            ]\n        },\n        {\n            \"name\": {\n                \"text\": \"Test Email\"\n            },\n            \"relationship\": [\n                {\n                    \"text\": \"Father\"\n                }\n            ],\n            \"telecom\": [\n                {\n                    \"system\": \"email\",\n                    \"value\": \"test.email@email.test\"\n                }\n            ]\n        }\n    ],\n    \"communication\": [\n        {\n            \"language\": {\n                \"coding\": [\n                    {\n                        \"system\": \"http://hl7.org/fhir/ValueSet/all-languages\",\n                        \"code\": \"en\",\n                        \"display\": \"English\"\n                    }\n                ],\n                \"text\": \"English\"\n            }\n        }\n    ]\n}"

headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
{% endtab %}
{% tab patient-create-request curl %}
```sh
curl --request POST \
     --url https://fhir-example.canvasmedical.com/Patient \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Patient",
  "name": [
    {
      "use": "official",
      "family": "Mark",
      "given": [
        "Isabella",
        "Robel"
      ],
      "prefix": "Mrs.",
      "suffix": "Jr."
    },
    {
      "use": "nickname",
      "given": [
        "Izzy"
      ]
    },
    {
      "use": "maiden",
      "family": "Smith"
    }
  ],
  "birthDate": "1980-11-13"
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="patient-create-response">
{% tabs patient-create-response %}
{% tab patient-create-response 200 %}
```json
200 {
  ...
}
```
{% endtab %}
{% tab patient-create-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="patient-update-request">
{% tabs patient-update-request %}
{% tab patient-update-request curl %}
```sh
curl --request PUT \
     --url https://fhir-example.canvasmedical.com/Patient/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Patient",
  "id": "c9491183c38b4fe793db70c60046db3f",
  "extension": [
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
      "valueCode": "M"
    },
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
      "extension": [
        {
          "url": "text",
          "valueString": "UNK"
        }
      ]
    },
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
      "extension": [
        {
          "valueCoding": {
            "system": "urn:oid:2.16.840.1.113883.6.238",
            "code": "2106-3",
            "display": "White"
          }
        }
      ]
    },
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy",
      "extension": [
        {
          "url": "ncpdp-id",
          "valueIdentifier": {
            "value": "1123152",
            "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber"
          }
        }
      ]
    },
    {
      "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
      "valueCode": "America/New_York"
    },
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
      "valueString": "I am a clinical caption from a Create message"
    },
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
      "valueString": "I am an administrative caption from a Create message"
    }
  ],
  "name": [
    {
      "use": "official",
      "family": "Mark",
      "given": [
        "Jade",
        "Robel"
      ]
    },
    {
      "use": "nickname",
      "given": [
        "Nick Name"
      ]
    }
  ],
  "birthDate": "1980-11-13"
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="patient-update-response">
{% tabs patient-update-response %}
{% tab patient-update-response 200 %}
```json
200 {
  ...
}
```
{% endtab %}
{% tab patient-update-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>
