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
            required: true
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
                type: integer
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
          - name: gender
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
        endpoints: [read, search, create, update]
        read:
          responses: [200, 404]
          example_request: patient-read-request
          example_response: patient-read-response
        search:
          responses: [200, 400]
          example_request: patient-search-request
          example_response: patient-search-response
        create:
          responses: [201, 400]
          example_request: patient-create-request
          example_response: patient-create-response
        update:
          responses: [200, 400]
          example_request: patient-update-request
          example_response: patient-update-response
---


<div id="patient-read-request">
{% tabs patient-read-request %}
{% tab patient-read-request python %}
```sh
import requests
import json

url = "https://fumage-example.canvasmedical.com/Patient/<id>/"

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
     --url https://fumage-example.canvasmedical.com/Patient/<id> \
     --header 'Authorization: Bearer <token>' 
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="patient-read-response">
{% tabs patient-read-response %}
{% tab patient-read-response 200 %}
```json
{
    "resourceType": "Patient",
    "id": "a1197fa9e65b4a5195af15e0234f61c2",
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Rubik<b>Cube</b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>739588251</td></tr><tr><td>Date of birth</td><td><span>1949-11-13</span></td></tr></tbody></table></div>"
    },
    "extension": [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "M"
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
            "valueCodeableConcept": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "446151000124109",
                        "display": "Identifies as male gender (finding)"
                    }
                ],
                "text": "Identifies as male gender (finding)"
            }
        },
        {
            "extension": [
                {
                    "url": "text",
                    "valueString": "UNK"
                }
            ],
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
        },
        {
            "extension": [
                {
                    "url": "text",
                    "valueString": "UNK"
                }
            ],
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity"
        },
        {
            "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
            "valueCode": "America/New_York"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
            "valueString": "Preferred Lab: Labcorp"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
            "valueString": "GI Specialist - Nora Jones MD\nPCP - Robin Williams MD\nNeurologist - Joe Brooks MD"
        },
        {
            "extension": [
                {
                    "url": "ncpdp-id",
                    "valueIdentifier": {
                        "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber",
                        "value": "1123152"
                    }
                },
                {
                    "url": "specialty_type",
                    "valueString": "Retail"
                },
                {
                    "url": "default",
                    "valueBoolean": false
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
            "value": "739588251",
            "assigner": {
                "display": "Canvas Medical"
            }
        },
        {
            "id": "cf62c385-a222-428b-ac86-8fab970d6218",
            "use": "usual",
            "system": "HealthCo",
            "value": "s07960990",
            "period": {
                "start": "1970-01-01",
                "end": "2100-12-31"
            }
        }
    ],
    "active": true,
    "name": [
        {
            "use": "official",
            "family": "Cube",
            "given": [
                "Rubik",
                "NEW NAME"
            ],
            "period": {
                "start": "0001-01-01T00:00:00+00:00",
                "end": "9999-12-31T23:59:59.999999+00:00"
            }
        },
        {
            "use": "nickname",
            "given": [
                "Nick Name"
            ],
            "period": {
                "start": "0001-01-01T00:00:00+00:00",
                "end": "9999-12-31T23:59:59.999999+00:00"
            }
        }
    ],
    "telecom": [
        {
            "id": "a0859714-adb7-4a60-8832-41995c04039a",
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                    "valueBoolean": false
                }
            ],
            "system": "phone",
            "value": "0000000000",
            "use": "mobile",
            "rank": 1
        },
        {
            "id": "051444e4-4f80-4866-b00c-151a38b095a6",
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                    "valueBoolean": false
                }
            ],
            "system": "email",
            "value": "i.k.bahar@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "male",
    "birthDate": "1949-11-13",
    "deceasedBoolean": false,
    "address": [
        {
            "id": "6c54eb4a-8c54-4965-a729-ab9f3223b63d",
            "use": "home",
            "type": "both",
            "line": [
                "4247 Murry Street"
            ],
            "city": "Chesapeake",
            "state": "VA",
            "postalCode": "23322",
            "country": "United States"
        }
    ],
    "photo": [
        {
            "url": "https://d3hn0m4rbsz438.cloudfront.net/avatar1.png"
        }
    ],
    "contact": [
        {
            "id": "91a597d0-65a8-443b-8330-feab2e64ffee",
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
                    "text": "Spouse"
                }
            ],
            "name": {
                "text": "Test Spouse"
            },
            "telecom": [
                {
                    "system": "email",
                    "value": "test@me.com"
                }
            ]
        },
        {
            "id": "81676d04-4b5b-4b34-87a7-7333a74fd82e",
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": false
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": true
                }
            ],
            "relationship": [
                {
                    "text": "Mom"
                }
            ],
            "name": {
                "text": "Test Mom"
            },
            "telecom": [
                {
                    "system": "phone",
                    "value": "7177327068"
                }
            ]
        },
        {
            "id": "e5cecb0f-3fb3-4a16-94d7-6cb51c4fec45",
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": false
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": false
                }
            ],
            "relationship": [
                {
                    "text": "Father"
                }
            ],
            "name": {
                "text": "Test Email"
            },
            "telecom": [
                {
                    "system": "email",
                    "value": "test.email@email.test"
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
}
```
{% endtab %}
{% tab patient-read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown Patient resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
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

url = "https://fumage-example.canvasmedical.com/Patient?_id=797e5f30447545a4823fe1c8ebcd0ba6"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```
{% endtab %}
{% tab patient-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Patient \
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
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Patient?id=797e5f30447545a4823fe1c8ebcd0ba6&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Patient?id=797e5f30447545a4823fe1c8ebcd0ba6&_count=10&_offset=0"
        },
        {
            "relation": "next",
            "url": "/Patient?id=797e5f30447545a4823fe1c8ebcd0ba6&_count=10&_offset=10"
        },
        {
            "relation": "last",
            "url": "/Patient?id=797e5f30447545a4823fe1c8ebcd0ba6&_count=10&_offset=31780"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Patient",
                "id": "cf10ff9d14d0429cb5bb7040611d1a24",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Americus 😸️<b>Ohri</b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>411604721</td></tr><tr><td>Date of birth</td><td><span>1984-09-24</span></td></tr></tbody></table></div>"
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
                        "extension": [
                            {
                                "url": "text",
                                "valueString": "UNK"
                            }
                        ],
                        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
                    },
                    {
                        "extension": [
                            {
                                "url": "text",
                                "valueString": "UNK"
                            }
                        ],
                        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity"
                    },
                    {
                        "extension": [
                            {
                                "url": "ncpdp-id",
                                "valueIdentifier": {
                                    "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber",
                                    "value": "9911557"
                                }
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
                        "value": "411604721",
                        "assigner": {
                            "display": "Canvas Medical"
                        }
                    }
                ],
                "active": true,
                "name": [
                    {
                        "use": "official",
                        "family": "Ohri",
                        "given": [
                            "Americus 😸️"
                        ],
                        "period": {
                            "start": "0001-01-01T00:00:00+00:00",
                            "end": "9999-12-31T23:59:59.999999+00:00"
                        }
                    }
                ],
                "telecom": [
                    {
                        "id": "5a86b61d-dd3b-46ea-94d6-12008f97d38f",
                        "extension": [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                                "valueBoolean": false
                            }
                        ],
                        "system": "email",
                        "value": "test.patient+Americus 😸️.Ohri@canvasmedical.com",
                        "use": "home",
                        "rank": 2
                    }
                ],
                "gender": "female",
                "birthDate": "1984-09-24",
                "deceasedBoolean": false,
                "address": [
                    {
                        "id": "a6a85bff-520f-49d9-a957-4931a1ce67d0",
                        "use": "home",
                        "type": "both",
                        "line": [
                            "1013 Calvan Ave",
                            "Apt 16"
                        ],
                        "city": "Corte Madera",
                        "state": "CA",
                        "postalCode": "94965"
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
            }
        }
    ]
}
```
{% endtab %}
{% tab search-response 400 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
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

<div id="patient-create-request">
{% tabs patient-create-request %}
{% tab patient-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Patient"

payload = "{\n    \"resourceType\": \"Patient\",\n    \"extension\": [\n        {\n            \"url\": \"http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex\",\n            \"valueCode\": \"M\"\n        },\n        {\n            \"url\" : \"http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy\",\n            \"extension\": [\n                {\n                    \"url\": \"ncpdp-id\",\n                    \"valueIdentifier\": {\n                        \"value\": \"1123152\",\n                        \"system\": \"http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber\"\n                    }\n                }\n            ]\n        },\n        {\n            \"url\": \"http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity\",\n            \"extension\": [\n                {\n                    \"url\": \"text\",\n                    \"valueString\": \"UNK\"\n                }\n            ]\n        },\n        {\n            \"url\": \"http://hl7.org/fhir/us/core/StructureDefinition/us-core-race\",\n            \"extension\": [\n                {\n                    \"url\": \"text\",\n                    \"valueString\": \"UNK\"\n                }\n            ]\n        },\n        {\n            \"url\": \"http://hl7.org/fhir/StructureDefinition/tz-code\",\n            \"valueCode\": \"America/New_York\"\n        },\n        {\n            \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/clinical-note\",\n            \"valueString\": \"I am a clinical caption from a Create message\"\n        },\n        {\n            \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/administrative-note\",\n            \"valueString\": \"I am an administrative caption from a Create message\"\n        }\n    ],\n    \"identifier\": [\n        {\n            \"use\": \"usual\",\n            \"system\": \"HealthCo\",\n            \"value\": \"s07960990\"\n        }\n    ],\n    \"active\": true,\n    \"name\": [\n        {\n            \"use\": \"official\",\n            \"family\": \"Bahar\",\n            \"given\": [\n                \"Issam\",\n                \"Khuzaimah\"\n            ]\n        },\n        {\n            \"use\": \"nickname\",\n            \"given\": [\n                \"Nick Name\"\n            ]\n        }\n    ],\n    \"telecom\": [\n        {\n            \"system\": \"phone\",\n            \"value\": \"5554320555\",\n            \"use\": \"mobile\",\n            \"rank\": 1\n        },\n        {\n            \"system\": \"email\",\n            \"value\": \"i.k.bahar@example.com\",\n            \"use\": \"work\",\n            \"rank\": 1\n        }\n    ],\n    \"gender\": \"male\",\n    \"birthDate\": \"1949-11-13\",\n    \"address\": [\n        {\n            \"use\": \"home\",\n            \"type\": \"both\",\n            \"text\": \"4247 Murry Street, Chesapeake, VA 23322\",\n            \"line\": [\n                \"4247 Murry Street\"\n            ],\n            \"city\": \"Chesapeake\",\n            \"state\": \"VA\",\n            \"postalCode\": \"23322\"\n        }\n    ],\n    \"contact\": [\n        {\n            \"name\": {\n                \"text\": \"Test Spouse\"\n            },\n            \"relationship\": [\n                {\n                    \"text\": \"Spouse\"\n                }\n            ],\n            \"telecom\": [\n                {\n                    \"system\": \"email\",\n                    \"value\": \"test@me.com\"\n                }\n            ],\n            \"extension\": [\n                {\n                    \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/emergency-contact\",\n                    \"valueBoolean\": true\n                },\n                {\n                    \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information\",\n                    \"valueBoolean\": true\n                }\n            ]\n        },\n        {\n            \"name\": {\n                \"text\": \"Test Mom\"\n            },\n            \"relationship\": [\n                {\n                    \"text\": \"Mom\"\n                }\n            ],\n            \"telecom\": [\n                {\n                    \"system\": \"phone\",\n                    \"value\": \"7177327068\"\n                }\n            ],\n            \"extension\": [\n                {\n                    \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information\",\n                    \"valueBoolean\": true\n                }\n            ]\n        },\n        {\n            \"name\": {\n                \"text\": \"Test Email\"\n            },\n            \"relationship\": [\n                {\n                    \"text\": \"Father\"\n                }\n            ],\n            \"telecom\": [\n                {\n                    \"system\": \"email\",\n                    \"value\": \"test.email@email.test\"\n                }\n            ]\n        }\n    ],\n    \"communication\": [\n        {\n            \"language\": {\n                \"coding\": [\n                    {\n                        \"system\": \"http://hl7.org/fhir/ValueSet/all-languages\",\n                        \"code\": \"en\",\n                        \"display\": \"English\"\n                    }\n                ],\n                \"text\": \"English\"\n            }\n        }\n    ]\n}"

headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
{% endtab %}
{% tab patient-create-request curl %}
```sh
curl --request POST \
     --url https://fumage-example.canvasmedical.com/Patient \
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
{% tab patient-create-response 201%}
```json
null
```
{% endtab %}
{% tab patient-create-response 400 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
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

<div id="patient-update-request">
{% tabs patient-update-request %}
{% tab patient-update-request python %}
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
  "identifier": [
    {
      "id": "5886041f-35a1-4107-acbb-6a9b31489633",
      "use": "usual",
      "system": "HealthCo",
      "value": "s07960990",
      "period": {
        "start": "1970-01-01",
        "end": "2100-12-31"
      }
    }
  ],
  "active": true,
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
  "telecom": [
    {
      "id": "46c850f4-bf87-47fe-88d1-1eb9883ab095",
      "system": "other",
      "value": "other test",
      "use": "home",
      "rank": 1
    },
    {
      "id": "5e610aac-4627-40b5-bff0-892a7040a0a4",
      "extension": [
        {
          "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
          "valueBoolean": false
        }
      ],
      "system": "phone",
      "value": "5554320555",
      "use": "mobile",
      "rank": 1
    }
  ],
  "gender": "male",
  "birthDate": "1980-11-13",
  "deceasedBoolean": false,
  "address": [
    {
      "id": "81a5c192-5b06-4900-b99d-2ac952b8950c",
      "use": "home",
      "type": "both",
      "line": [
        "4247 Murry Street"
      ],
      "city": "Chesapeake",
      "state": "VA",
      "postalCode": "23322",
      "country": "United States",
      "period": {
        "start": "2022-02-20T21:37:02.748Z"
      }
    }
  ],
  "photo": [
    {
      "data": "R0lGODlhEwARAPcAAAAAAAAA/+9aAO+1AP/WAP/eAP/eCP/eEP/eGP/nAP/nCP/nEP/nIf/nKf/nUv/nWv/vAP/vCP/vEP/vGP/vIf/vKf/vMf/vOf/vWv/vY//va//vjP/3c//3lP/3nP//tf//vf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEAAAEALAAAAAATABEAAAi+AAMIDDCgYMGBCBMSvMCQ4QCFCQcwDBGCA4cLDyEGECDxAoAQHjxwyKhQAMeGIUOSJJjRpIAGDS5wCDly4AALFlYOgHlBwwOSNydM0AmzwYGjBi8IHWoTgQYORg8QIGDAwAKhESI8HIDgwQaRDI1WXXAhK9MBBzZ8/XDxQoUFZC9IiCBh6wEHGz6IbNuwQoSpWxEgyLCXL8O/gAnylNlW6AUEBRIL7Og3KwQIiCXb9HsZQoIEUzUjNEiaNMKAAAA7"
    }
  ],
  "contact": [
    {
      "id": "d29b8687-6aad-4a6c-9979-cdb621380f35",
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
          "text": "Spouse"
        }
      ],
      "name": {
        "text": "Test Spouse"
      },
      "telecom": [
        {
          "system": "email",
          "value": "test@me.com"
        }
      ]
    },
    {
      "id": "6df5fb22-7abc-4086-8584-880a79fed3c0",
      "extension": [
        {
          "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
          "valueBoolean": true
        }
      ],
      "relationship": [
        {
          "text": "Mom"
        }
      ],
      "name": {
        "text": "Test Mom"
      },
      "telecom": [
        {
          "system": "phone",
          "value": "7177327068"
        }
      ]
    },
    {
      "id": "a92aba15-41bd-475c-8e3f-25a7688ffbb2",
      "relationship": [
        {
          "text": "Father"
        }
      ],
      "name": {
        "text": "Test Email"
      },
      "telecom": [
        {
          "system": "email",
          "value": "test.email@email.test"
        }
      ]
    }
  ]
}
'
```
{% endtab %}
{% tab patient-update-request curl %}
```sh
curl --request PUT \
     --url https://fumage-example.canvasmedical.com/Patient/<id> \
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
null
```
{% endtab %}
{% tab patient-update-response 400 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
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
