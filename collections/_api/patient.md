---
title: FHIR Patient 
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Patient
        article: "a"
        attributes:
          - name: _id
            description: >-
              The identifier of the patient
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
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
          - name: gender
            description: >-
              Default: male
            type: string
            required: false
          - name: deceased
            type: boolean
            required: false
          - name: address
            type: json
            required: false
          - name: photo
            type: json
            required: false
          - name: contact
            type: json
            required: false
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
          - name: family
            type: string
            description: Last name
          - name: given
            type: string
            description: First Name
          - name: birthdate
            type: date
            description: The patient's birthdate
          - name: gender
            type: string
          - name: nickname
            type: string
            description: Preferred or alternate name
          - name: email
            type: string
            description: Patient email address
          - name: phone
            type: string
            description: Patient phone number, expected to be 10 digits
          - name: active
            type: boolean
            description: By default, both active and inactive patients are returned. Use this parameter to only return active (true) or inactive (false)
        endpoints: [read, search, create, update]
        read:
          responses: [200, 400]
          example_request: example-read-request
          example_response: example-read-response
        search:
          responses: [200, 400]
          example_request: example-search-request
          example_response: example-search-response
        create:
          responses: [201, 400]
          example_request: example-create-request
          example_response: example-create-response
        update:
          responses: [200, 400]
          example_request: example-update-request
          example_response: example-update-response
---
<div id="example-payload-code">
{% tabs payload %}
{% tab payload json %}
```json
some data here
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-read-request">
{% tabs read-request %}
{% tab read-request curl %}
```sh
curl --request GET \
     --url https://fhir-example.canvasmedical.com/Patient/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% tab read-request python %}
```sh
import requests
import json

url = "https://fhir-example.canvasmedical.com/Patient/797e5f30447545a4823fe1c8ebcd0ba6/"

payload={}
headers = {
  'Content-Type': 'application/fhir+json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```
{% endtab %}
{% endtabs %}
</div>

<div id="example-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
200 {
  {
    "resourceType": "Patient",
    "id": "496db9b3dff044448384e0bcba5e67c4",
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Megan<b>Jones</b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>427087947</td></tr><tr><td>Date of birth</td><td><span>1971-07-08</span></td></tr></tbody></table></div>"
    },
    "extension": [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "F"
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
            "valueCodeableConcept": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "446141000124107",
                        "display": "Identifies as female gender (finding)"
                    }
                ],
                "text": "Identifies as female gender (finding)"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/sexual-orientation",
            "valueCode": "20430005"
        },
        {
            "extension": [
                {
                    "url": "ombCategory",
                    "valueCoding": {
                        "system": "urn:oid:2.16.840.1.113883.6.238",
                        "code": "2106-3",
                        "display": "White"
                    }
                },
                {
                    "url": "text",
                    "valueString": "White"
                }
            ],
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
        },
        {
            "extension": [
                {
                    "url": "ombCategory",
                    "valueCoding": {
                        "system": "urn:oid:2.16.840.1.113883.6.238",
                        "code": "2186-5",
                        "display": "Not Hispanic or Latino"
                    }
                },
                {
                    "url": "text",
                    "valueString": "Not Hispanic or Latino"
                }
            ],
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity"
        },
        {
            "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
            "valueCode": "America/Chicago"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
            "valueString": "This is an administrative caption"
        },
        {
            "extension": [
                {
                    "url": "ncpdp-id",
                    "valueIdentifier": {
                        "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber",
                        "value": "3061582"
                    }
                },
                {
                    "url": "specialty_type",
                    "valueString": "Retail~TwentyFourHourStore~SupportsDigitalSignature"
                },
                {
                    "url": "default",
                    "valueBoolean": true
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy"
        }
    ],
    "identifier": [
        {
            "use": "usual",
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                        "code": "MR"
                    }
                ]
            },
            "system": "http://canvasmedical.com",
            "value": "427087947",
            "assigner": {
                "display": "Canvas Medical"
            }
        }
    ],
    "active": true,
    "name": [
        {
            "use": "official",
            "family": "Jones",
            "given": [
                "Megan"
            ],
            "period": {
                "start": "0001-01-01T00:00:00+00:00",
                "end": "9999-12-31T23:59:59.999999+00:00"
            }
        }
    ],
    "telecom": [
        {
            "id": "8e2b867c-6770-4e21-b296-fca8de3803c6",
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                    "valueBoolean": false
                }
            ],
            "system": "email",
            "value": "megan.jones@zahoo.com",
            "use": "home",
            "rank": 1
        },
        {
            "id": "587652b2-c739-4ac2-a44a-7488c060ac11",
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                    "valueBoolean": false
                }
            ],
            "system": "phone",
            "value": "5893263689",
            "use": "home",
            "rank": 1
        }
    ],
    "gender": "female",
    "birthDate": "1971-07-08",
    "deceasedBoolean": false,
    "address": [
        {
            "id": "4c87b7af-2a2e-4cb0-ac84-559ab021780b",
            "use": "home",
            "type": "physical",
            "line": [
                "123 Main St"
            ],
            "city": "Nashville",
            "state": "TN",
            "postalCode": "37206",
            "country": "us"
        }
    ],
    "photo": [
        {
            "url": "https://d3hn0m4rbsz438.cloudfront.net/avatar1.png"
        }
    ],
    "contact": [
        {
            "id": "96f20c90-a631-4ffc-acd4-94d6ee4efd38",
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": true
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": true
                }
            ],
            "relationship": [
                {
                    "text": "Husband"
                }
            ],
            "name": {
                "text": "Kevin Jones"
            },
            "telecom": [
                {
                    "system": "phone",
                    "value": "5555555555"
                },
                {
                    "system": "email",
                    "value": "kj@zahoo.com"
                }
            ]
        }
    ],
    "communication": [
        {
            "language": {
                "coding": [
                    {
                        "system": "urn:ietf:bcp:47",
                        "code": "en",
                        "display": "English"
                    }
                ],
                "text": "English"
            }
        }
    ]
}}
```
{% endtab %}
{% tab read-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-search-request">
{% tabs search-request %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fhir-example.canvasmedical.com/Patient \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
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

<div id="example-create-request">
{% tabs create-request %}
{% tab create-request curl %}
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

<div id="example-create-response">
{% tabs create-response %}
{% tab create-response 201 %}
```json
201 {
  ...
}
```
{% endtab %}
{% tab create-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-update-request">
{% tabs update-request %}
{% tab update-request curl %}
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
'

```
{% endtab %}
{% endtabs %}
</div>

<div id="example-update-response">
{% tabs update-response %}
{% tab update-response 200 %}
```json
200 {
  ...
}
```
{% endtab %}
{% tab update-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>


