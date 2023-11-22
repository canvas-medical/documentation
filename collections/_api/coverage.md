---
title: Coverage
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Coverage
        article: "a"
        description: >-
          Financial instrument which may be used to reimburse or pay for health care products and services. Includes both insurance and self-payment.<br>
          [https://hl7.org/fhir/R4/coverage.html](https://hl7.org/fhir/R4/coverage.html)
        attributes:
          - name: id
            description: >-
              The identifier of the Coverage
            type: string
          - name: status
            description: >-
              The status of the Coverage<br><br>
              Supported codes for create interactions: **active**, **entered-in-error** 
            type: string
            required: true
          - name: type
            type: json
            description: >-
              Type of coverage, such as medical, workers compensation, self pay, etc.<br><br>
              In order for this value to display on the Canvas UI, the coverage type needs to be configured for the specific payor via our insurer settings.  To get to these settings, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers).
          - name: subscriber
            description: >-
              Who was signed up for or 'owns' the Coverage<br><br>
              Supported resource types: **Patient**
            type: json
            required: true
          - name: subscriberId
            description: >-
              The insurer assigned ID for the subscriber
            type: string
            required: true
          - name: beneficiary
            description: >-
              Who benefits from the coverage; the patient when products or services are provided.<br><br>
              Supported resource types for create interactions are: **Patient**
            type: json
            required: true
          - name: relationship
            type: json
            description: >-
              The relationship of beneficiary (patient) to the subscriber<br><br>
              Supported codes for create interactions are: **child**, **spouse**, **other**, **self**, **injured** with a system of **http://hl7.org/fhir/ValueSet/subscriber-relationship**<br><br>
              A single iteration is supported.
            required: true
          - name: period
            description: >-
              The period during which the Coverage is in force.<br><br>
              A missing start date indicates the start date isn't known - for a create interaction, this will be set to the current date.<br><br>
              A missing end date means the coverage continues to be in force.
            type: json
          - name: payor
            type: array[json]
            description: >-
              Issuer of the policy<br><br>
              Two methods for creating this data are supported:
               - sending an [**Organization**](/api/organization) reference in `payor[0].reference`
               ```json
              "payor": [
                    {
                        "reference": "Organization/6741b035-2846-45b3-b7a3-251f7b7fc728",
                        "type": "Organization",
                        "display": "Medicare Advantage"
                    }
                  ],
               ```
               For **Read/Search**, this **Organization** reference will always be returned.
              <br>
               - sending a `payor[0].identifier.value` corresponding to the Coverage's payor id.  For now, these values can only be found and updated in the [Insurers Admin view](https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers) in Canvas.
               ```json
                "payor": [
                    {
                      "identifier": {
                        "system": "https://www.claim.md/services/era/",
                        "value": "13162"
                      },
                      "display": "1199 National Benefit Fund"
                    }
                  ],
               ```
               <br>

            required: true
          - name: class
            type: json
            description: >-
              Additional coverage classifications.<br><br>
              Supported class types supported for create interactions: **plan**, **subplan**, **group**, **subgroup** with a system of **http://hl7.org/fhir/ValueSet/coverage-class**<br><br>
              Only plan and group are visible in the Canvas UI.
          - name: order
            type: number
            description: >-
              The order in which coverages should be used when adjudicating claims.<br><br>
                For create interactions, this must between 1 and 5, inclusive.<br><br>
                If multiple coverages are created with the same order number, the older one will be bumped down in rank, and the new one will take that rank.<br><br>
                If this leads to multiple coverages being incremented to 5, the oldest (first to be input) of the coverages at this rank will be displayed on the Canvas UI.
        search_parameters:
          - name: _id
            type: string
            description: The Canvas resource identifier of the Coverage
          - name: patient
            type: string
            description: Retrieve coverages for a patient
          - name: subscriberid
            type: string
            description: Retrieve all coverages with a specific subscriberID
        endpoints: [create, read, update, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: coverage-create-request
          example_response: coverage-create-response
        read:
          responses: [200, 401, 403, 404]
          example_request: coverage-read-request
          example_response: coverage-read-response
        update:
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: coverage-update-request
          example_response: coverage-update-response
        search:
          responses: [200, 400, 401, 403]
          example_request: coverage-search-request
          example_response: coverage-search-response
---

<div id="coverage-create-request">
  {% tabs coverage-create-request %}
    {% tab coverage-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Coverage' \
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
    "start": "2021-06-27",
    "end": "2023-06-27"
  },
  "payor": [
    {
      "reference": "Organization/6741b035-2846-45b3-b7a3-251f7b7fc728",
      "type": "Organization",
      "display": "Medicare Advantage"
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

    {% tab coverage-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Coverage"

payload = {
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
  "subscriber": { "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b34" },
  "subscriberId": "1234",
  "beneficiary": { "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b3" },
  "relationship": { 
    "coding": [
      {
        "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
        "code": "self"
      }
    ]
  },
  "period": {
    "start": "2021-06-27",
    "end": "2023-06-27"
  },
  "payor": [
    {
      "reference": "Organization/6741b035-2846-45b3-b7a3-251f7b7fc728",
      "type": "Organization",
      "display": "Medicare Advantage"
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
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

```
    {% endtab %}
    
  {% endtabs %}
</div>

<div id="coverage-create-response">
{% include create-response.html %}
</div>

<div id="coverage-read-request">
{% include read-request.html resource_type="Coverage" %}
</div>

<div id="coverage-read-response">
  {% tabs coverage-read-response %}

    {% tab coverage-read-response 200 %}
```json
{
  "resourceType": "Coverage",
  "id": "a7c6af04-a22f-47bf-9cc8-d41158b2ad62",
  "status": "active",
  "type": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/ValueSet/coverage-type",
        "code": "MILITARY",
        "display": "Military health program"
      }
    ]
  },
  "subscriber": {
    "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd",
    "type": "Patient"
  },
  "subscriberId": "12345",
  "beneficiary": {
    "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd",
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
    "start": "2023-09-19"
  },
  "payor": [
    {
      "reference": "Organization/c152eeb7-f204-4e28-acb5-c7e85390b17e",
      "type": "Organization",
      "display": " Custody Medical Services Program"
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
  ],
  "order": 1
}
```
    {% endtab %}

    {% tab coverage-read-response 401 %}
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

    {% tab coverage-read-response 403 %}
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

    {% tab coverage-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Coverage resource 'c152eeb7-f204-4e28-acb5-c7e85390b17e'"
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
```shell
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/Coverage/<id>' \
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
    "start": "2021-06-27",
    "end": "2023-06-27"
  },
  "payor": [
    {
      "reference": "Organization/6741b035-2846-45b3-b7a3-251f7b7fc728",
      "type": "Organization",
      "display": "Medicare Advantage"
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

    {% tab coverage-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Coverage/<id>"

payload = {
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
  "subscriber": { "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b34" },
  "subscriberId": "1234",
  "beneficiary": { "reference": "Patient/febae9dcb7cf4d88ba27cc552a3f96b3" },
  "relationship": { 
    "coding": [
      {
        "system": "http://hl7.org/fhir/ValueSet/subscriber-relationship",
        "code": "self"
      }
    ]
  },
  "period": {
    "start": "2021-06-27",
    "end": "2023-06-27"
  },
  "payor": [
    {
      "reference": "Organization/6741b035-2846-45b3-b7a3-251f7b7fc728",
      "type": "Organization",
      "display": "Medicare Advantage"
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
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)

```
    {% endtab %}

{% endtabs %}
</div>

<div id="coverage-update-response">
{% include update-response.html resource_type="Coverage" %}
</div>

<div id="coverage-search-request">
{% include search-request.html resource_type="Coverage" search_string="subscriberid=12345&patient=Patient/b3084f7e884e4af2b7e23b1dca494abd" %}
</div>

<div id="coverage-search-response">
{% tabs coverage-search-response %}
{% tab coverage-search-response 200 %}
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 2,
  "link": [
    {
        "relation": "self",
        "url": "/Coverage?subscriberid=12345&patient=Patient%2Fb3084f7e884e4af2b7e23b1dca494abd"
    },
    {
        "relation": "first",
        "url": "/Coverage?subscriberid=12345&patient=Patient%2Fb3084f7e884e4af2b7e23b1dca494abd"
    },
    {
        "relation": "last",
        "url": "/Coverage?subscriberid=12345&patient=Patient%2Fb3084f7e884e4af2b7e23b1dca494abd"
    }
  ],
  "entry": [
    {
      "resource": {
        "resourceType": "Coverage",
        "id": "171a7243-f568-48cb-8052-3f2990dac1cd",
        "status": "entered-in-error",
        "subscriber": {
            "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd",
            "type": "Patient"
        },
        "subscriberId": "11111",
        "beneficiary": {
            "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd",
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
            "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd",
            "type": "Patient"
        },
        "subscriberId": "A1",
        "beneficiary": {
            "reference": "Patient/b3084f7e884e4af2b7e23b1dca494abd",
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
    }
  ]
}
```
{% endtab %}
{% tab coverage-search-response 400 %}
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

    {% tab coverage-search-response 401 %}
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

    {% tab coverage-search-response 403 %}
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
