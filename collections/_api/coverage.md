---
title: Coverage
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Coverage
        article: "a"
        description: >-
          Financial instrument which may be used to reimburse or pay for health care products and services. Includes both insurance and self-payment.
        attributes:
          - name: id
            description: >-
              The identifier of the coverage
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: status
            description: >-
              The status of the coverage
            type: string
            required: true
          - name: type
            description: >-
              Coverage category such as medical or accident
            type: json
            attributes:
              - name: coding
                type: json
                attributes:
                  - name: system
                    type: string
                    required: true
                  - name: code
                    type: string
                    required: true
                  - name: display
                    type: string
                    required: true
          - name: subscriber
            type: string
            description: >-
              The subscriber to the policy
          - name: subscriberId
            description: >-
              ID assigned to the subscriber
            type: string
            required: true
          - name: beneficiary
            description: >-
              Plan beneficiary
            type: string
          - name: relationship
            type: string
            description: >-
              Beneficiary relationship to the subscriber
            attributes:
              - name: coding
                type: json
                attributes:
                  - name: system
                    type: string
                    required: true
                  - name: code
                    type: string
                    required: true
                  - name: display
                    type: string
              - name: text
                type: string
                required: true
          - name: period
            description: >-
              The effective period of the exception
            type: json
            attributes:
              - name: start
                type: date
                required: true
              - name: end
                type: date
                required: true
          - name: payor
            type: string
            description: >-
              Issuer of the policy
          - name: class
            type: string
            description: >-
              Additional coverage classifications
          - name: order
            type: string
            description: >-
              Relative order of the coverage
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
          - name: subscriberID
            type: string
        endpoints: [search, create, update]
        search:
          responses: [200, 400]
          example_request: coverage-search-request
          example_response: coverage-search-response
        create:
          responses: [201, 400]
          example_request: coverage-create-request
          example_response: coverage-create-response
        update:
          responses: [200, 400]
          example_request: coverage-update-request
          example_response: coverage-update-response
---
<div id="coverage-search-request">
{% tabs coverage-search-request %}
{% tab coverage-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Coverage?subscriberid=12345&_count=10&_offset=0&patient=patient"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab coverage-search-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/Coverage?subscriberid=12345&_count=10&_offset=0&patient=patient' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="coverage-search-response">
{% tabs coverage-search-response %}
{% tab coverage-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 4,
    "link": [
        {
            "relation": "self",
            "url": "/Coverage?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Coverage?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Coverage?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Coverage",
                "id": "171a7243-f568-48cb-8052-3f2990dac1cd",
                "status": "entered-in-error",
                "subscriber": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "subscriberId": "NA",
                "beneficiary": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "relationship": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
                            "code": "self",
                            "display": "Self"
                        }
                    ],
                    "text": "18"
                },
                "period": {
                    "start": "2022-01-01"
                },
                "payor": [
                    {
                        "reference": "Organization/9b6709aa-a84e-4070-9a83-7c14dc31a511",
                        "type": "Organization",
                        "display": "AL BCBS"
                    }
                ],
                "order": 2
            }
        },
        {
            "resource": {
                "resourceType": "Coverage",
                "id": "27f42512-23e6-4c17-8569-80e14792b6f8",
                "status": "entered-in-error",
                "subscriber": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "subscriberId": "A1",
                "beneficiary": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "relationship": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
                            "code": "self",
                            "display": "Self"
                        }
                    ],
                    "text": "18"
                },
                "period": {
                    "start": "2022-05-31"
                },
                "payor": [
                    {
                        "reference": "Organization/02211bf5-9ee1-47d1-a1bc-e06bd848e5f3",
                        "type": "Organization",
                        "display": "Kevin Carey Insurance, Inc."
                    }
                ],
                "order": 1
            }
        },
        {
            "resource": {
                "resourceType": "Coverage",
                "id": "3dd99deb-1e4a-445d-96b3-61f985e28bf9",
                "status": "entered-in-error",
                "subscriber": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "subscriberId": "A2",
                "beneficiary": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "relationship": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
                            "code": "self",
                            "display": "Self"
                        }
                    ],
                    "text": "18"
                },
                "period": {
                    "start": "2022-05-31"
                },
                "payor": [
                    {
                        "reference": "Organization/02211bf5-9ee1-47d1-a1bc-e06bd848e5f3",
                        "type": "Organization",
                        "display": "Kevin Carey Insurance, Inc."
                    }
                ],
                "order": 1
            }
        },
        {
            "resource": {
                "resourceType": "Coverage",
                "id": "d8b83404-e149-4883-ae60-0f389b210f53",
                "status": "active",
                "subscriber": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "subscriberId": "84716239",
                "beneficiary": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "relationship": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
                            "code": "self",
                            "display": "Self"
                        }
                    ],
                    "text": "18"
                },
                "period": {
                    "start": "2022-01-01"
                },
                "payor": [
                    {
                        "reference": "Organization/2905dc94-f3f6-4e2f-90a2-1bb286600dc6",
                        "type": "Organization",
                        "display": "Tufts Health Plan"
                    }
                ],
                "order": 1
            }
        }
    ]
}
```
{% endtab %}
{% tab coverage-search-response 400 %}
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

<div id="coverage-create-request">
{% tabs coverage-create-request %}
{% tab coverage-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Coverage"

payload = {
    "resourceType": "\"Coverage\"",
    "order": 1,
    "status": "\"active\"",
    "type": { "coding": [
            {
                "system": "http://hl7.org/fhir/ValueSet/coverage-type",
                "code": "MILITARY",
                "display": "military health program"
            }
        ] },
    "subscriber": { "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b34" },
    "subscriberId": "\"1234\"",
    "beneficiary": { "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b3" },
    "relationship": { "coding": [
            {
                "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
                "code": "self"
            }
        ] },
    "period": "{         \"start\": \"2021-06-27\"       	\"end\": \"2023-06-27\"     }",
    "payor": [
        {
            "identifier": {
                "system": "https://www.claim.md/services/era/",
                "value": "AMM03"
            },
            "display": "Independence Blue Cross Blue Shield"
        }
    ],
    "class": [
        {
            "type": { "coding": [
                    {
                        "system": "http://hl7.org/fhir/ValueSet/coverage-class",
                        "code": "plan"
                    }
                ] },
            "value": "Starfleet HMO"
        },
        {
            "type": { "coding": [
                    {
                        "system": "http://hl7.org/fhir/ValueSet/coverage-class",
                        "code": "subplan"
                    }
                ] },
            "value": "Stars"
        },
        {
            "type": { "coding": [
                    {
                        "system": "http://hl7.org/fhir/ValueSet/coverage-class",
                        "code": "group"
                    }
                ] },
            "value": "Captains Only"
        },
        {
            "type": { "coding": [
                    {
                        "system": "http://hl7.org/fhir/ValueSet/coverage-class",
                        "code": "subgroup"
                    }
                ] },
            "value": "Subgroup 2"
        }
    ]
}
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

```
{% endtab %}
{% tab coverage-create-request curl %}
```sh
curl --request POST \
     --url https://fumage-example.canvasmedical.com/Coverage \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "\"Coverage\"",
  "order": 1,
  "status": "\"active\"",
  "type": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/ValueSet/coverage-type",
        "code": "MILITARY",
        "display": "military health program"
      }
    ]
  },
  "subscriber": {
    "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b34"
  },
  "subscriberId": "\"1234\"",
  "beneficiary": {
    "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b3"
  },
  "relationship": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
        "code": "self"
      }
    ]
  },
  "period": "{         \"start\": \"2021-06-27\"       \t\"end\": \"2023-06-27\"     }",
  "payor": [
    {
      "identifier": {
        "system": "https://www.claim.md/services/era/",
        "value": "AMM03"
      },
      "display": "Independence Blue Cross Blue Shield"
    }
  ],
  "class": [
    {
      "type": {
        "coding": [
          {
            "system": "http://hl7.org/fhir/ValueSet/coverage-class",
            "code": "plan"
          }
        ]
      },
      "value": "Starfleet HMO"
    },
    {
      "type": {
        "coding": [
          {
            "system": "http://hl7.org/fhir/ValueSet/coverage-class",
            "code": "subplan"
          }
        ]
      },
      "value": "Stars"
    },
    {
      "type": {
        "coding": [
          {
            "system": "http://hl7.org/fhir/ValueSet/coverage-class",
            "code": "group"
          }
        ]
      },
      "value": "Captains Only"
    },
    {
      "type": {
        "coding": [
          {
            "system": "http://hl7.org/fhir/ValueSet/coverage-class",
            "code": "subgroup"
          }
        ]
      },
      "value": "Subgroup 2"
    }
  ]
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="coverage-create-response">
{% tabs coverage-create-response %}
{% tab coverage-create-response 201 %}
```json
null
```
{% endtab %}
{% tab coverage-create-response 400 %}
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

<div id="coverage-update-request">
{% tabs coverage-update-request %}
{% tab coverage-update-request curl %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Coverage/_id"

payload = {
    "resourceType": "Coverage",
    "order": 1,
    "status": "active",
    "type": { "coding": [
            {
                "system": "http://hl7.org/fhir/ValueSet/coverage-type",
                "code": "MILITARY",
                "display": "military health program"
            }
        ] },
    "subscriber": { "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b34" },
    "subscriberId": "1234",
    "beneficiary": { "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b3" },
    "relationship": { "coding": [
            {
                "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
                "code": "self"
            }
        ] },
    "period": {
        "start": "2021-08-27",
        "end": "2025-08-27"
    },
    "payor": [
        {
            "identifier": {
                "system": "https://www.claim.md/services/era/",
                "value": "AMM03"
            },
            "display": "Independence Blue Cross Blue Shield"
        }
    ],
    "class": "\"class\": [        {           \"type\": {               \"coding\": [                    {                       \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",                       \"code\": \"plan\"                    }               ]          },          \"value\": \"Starfleet HMO\"        },        {           \"type\": {               \"coding\": [                    {                       \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",                       \"code\": \"subplan\"                    }               ]          },          \"value\": \"Stars\"        },        {            \"type\": {                \"coding\": [                    {                        \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",                        \"code\": \"group\"                    }                 ]            },           \"value\": \"Captains Only\"         },         {           \"type\": {               \"coding\": [                    {                       \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",                       \"code\": \"subgroup\"                    }               ]          },          \"value\": \"Subgroup 2\"        }   ]"
}
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)

```
{% endtab %}
{% tab coverage-update-request curl %}
```sh
curl --request PUT \
     --url https://fumage-example.canvasmedical.com/Coverage/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Coverage",
  "order": 1,
  "status": "active",
  "type": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/ValueSet/coverage-type",
        "code": "MILITARY",
        "display": "military health program"
      }
    ]
  },
  "subscriber": {
    "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b34"
  },
  "subscriberId": "1234",
  "beneficiary": {
    "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b3"
  },
  "relationship": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
        "code": "self"
      }
    ]
  },
  "period": {
    "start": "2021-08-27",
    "end": "2025-08-27"
  },
  "payor": [
    {
      "identifier": {
        "system": "https://www.claim.md/services/era/",
        "value": "AMM03"
      },
      "display": "Independence Blue Cross Blue Shield"
    }
  ],
  "class": "\"class\": [        {           \"type\": {               \"coding\": [                    {                       \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",                       \"code\": \"plan\"                    }               ]          },          \"value\": \"Starfleet HMO\"        },        {           \"type\": {               \"coding\": [                    {                       \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",                       \"code\": \"subplan\"                    }               ]          },          \"value\": \"Stars\"        },        {            \"type\": {                \"coding\": [                    {                        \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",                        \"code\": \"group\"                    }                 ]            },           \"value\": \"Captains Only\"         },         {           \"type\": {               \"coding\": [                    {                       \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",                       \"code\": \"subgroup\"                    }               ]          },          \"value\": \"Subgroup 2\"        }   ]"
}
'

```
{% endtab %}
{% endtabs %}
</div>

<div id="coverage-update-response">
{% tabs coverage-update-response %}
{% tab coverage-update-response 200 %}
```json
null
```
{% endtab %}
{% tab coverage-update-response 400 %}
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

