---
title: ServiceRequest
sections:
  - type: section
    blocks:
      - type: apidoc
        name: ServiceRequest
        article: "a"
        description: >-
          A request for a service to be performed for a patient, such as imaging, laboratory testing, or referral.<br><br>
          [https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-servicerequest.html](https://hl7.org/fhir/us/core/STU6.1/StructureDefinition-us-core-servicerequest.html)<br><br>
          
          ServiceRequest represents multiple Canvas services:
          
          - Imaging orders (e.g., CT, MRI, X-ray) - [Ordering imaging study](https://canvas-medical.help.usepylon.com/articles/2615916315-image-command)
          - Laboratory orders (e.g., hemoglobin/hematocrit) - [Placing a lab order](https://canvas-medical.help.usepylon.com/articles/3065191197-placing-a-lab-order)
          - Referrals (e.g., patient referral to specialist) - [Referring a patient](https://canvas-medical.help.usepylon.com/articles/8339414277-command-referrals)
          
          The ServiceRequest surface reflects these orders via standardized coding:
          
          - `category` uses SNOMED CT to represent the order category (e.g., Imaging, Laboratory procedure, Referral/Evaluation procedure)
          - `code` uses LOINC to represent the requested test/procedure
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the ServiceRequest.
            type: string
          - name: status
            description: A code specifying the state of the ServiceRequest.
            type: string
            enum_options:
              - value: active
              - value: completed
              - value: draft
              - value: entered-in-error
          - name: intent
            description: Indicates the level of authorization/intent for the request. Canvas supports `order` for orders placed by a practitioner.
            type: string
            enum_options:
              - value: order
          - name: category
            description: Categorical classification of the requested service (SNOMED CT). Common examples include Imaging, Laboratory procedure, and Referral/Evaluation procedure.
            type: array[json]
            attributes:
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes:
                  - name: system
                    description: The system URL of the coding.
                    type: string
                    enum_options:
                      - value: http://snomed.info/sct
                  - name: code
                    description: The code value.
                    type: string
                    enum_options:
                      - value: "363679005"
                      - value: "108252007"
                      - value: "386053000"
                  - name: display
                    description: The display name of the coding.
                    type: string
                    enum_options:
                      - value: "Imaging"
                      - value: "Laboratory procedure"
                      - value: "Evaluation procedure (procedure)"
          - name: code
            description: What service is being requested in a coded form (typically LOINC).
            type: json
            attributes:
              - name: coding
                description: Code defined by a terminology system.
                type: array[json]
                attributes:
                  - name: system
                    description: The system URL of the coding.
                    type: string
                    enum_options:
                      - value: http://loinc.org
                  - name: code
                    description: The code value that represents the respective Canvas service/order.
                    type: string
                  - name: display
                    description: The display name of the coding.
                    type: string
          - name: subject
            description: Who/what the service request is for.
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/c4ff2ee2e41b4636b7d37ac7f9297d95"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: occurrencePeriod
            description: The time window during which the service is to occur.
            type: json
            attributes:
              - name: start
                type: datetime
                description: Starting time with inclusive boundary of the requested service period.
              - name: end
                type: datetime
                description: End time with inclusive boundary of the requested service period.
          - name: authoredOn
            description: When the request was authored in Canvas.
            type: datetime
          - name: requester
            description: Who/what is requesting the service (a Practitioner reference).
            type: json
            attributes:
              - name: reference
                type: string
                description: The reference string of the requester in the format of `"Practitioner/5eede137ecfe4124b8b773040e33be14"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Practitioner").
          - name: reasonReference
            description: Reason for the request. References Conditions from Canvas.
            type: array[json]
            attributes:
              - name: reference
                type: string
                description: The reference string of the reason in the format of `"Condition/6700a428-6387-458d-8134-0702851da23c"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Condition").
        search_parameters:
          - name: _id
            description: The identifier of the ServiceRequest.
            type: string
          - name: patient
            description: The patient reference associated to the Service Request in the format `Patient/c4ff2ee2e41b4636b7d37ac7f9297d95`.
            type: string
          - name: authored
            description: Filter by **authoredOn**. See [Date Filtering](/api/date-filtering) for more information.
            type: date
          - name: category
            description: Categorization of the request (SNOMED CT). Filters by `category.coding` code and/or system. You can search by code alone or `system|code`.
            type: string
            search_options:
              - value: "http://snomed.info/sct|363679005"
              - value: "http://snomed.info/sct|108252007"
              - value: "http://snomed.info/sct|386053000"
          - name: code
            description: What is being requested (typically LOINC). Filters by `code.coding` code and/or system. You can search by code alone or `system|code`.
            type: string
        endpoints: [read, search]
        read:
          description: Read a ServiceRequest resource.
          responses: [200, 401, 403, 404]
          example_request: ServiceRequest-read-request
          example_response: ServiceRequest-read-response
        search:
          description: Search for ServiceRequest resources.
          responses: [200, 400, 401, 403]
          example_request: ServiceRequest-search-request
          example_response: ServiceRequest-search-response
---

<div id="ServiceRequest-read-request">
{%  include read-request.html resource_type="ServiceRequest" %}
</div>

<div id="ServiceRequest-read-response">

  {% tabs ServiceRequest-read-response %}

    {% tab ServiceRequest-read-response 200 %}
```json
{
    "resourceType": "ServiceRequest",
    "id": "a47c7b0e-bbb4-42cd-bc4a-df259d148ea1",
    "status": "active",
    "intent": "order",
    "category": [
      {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "363679005",
            "display": "Imaging"
          }
        ]
      }
    ],
    "code": {
      "coding": [
        {
          "system": "http://loinc.org",
          "code": "24627-2",
          "display": "CT Chest"
        }
      ]
    },
    "subject": {
      "reference": "Patient/c4ff2ee2e41b4636b7d37ac7f9297d95",
      "type": "Patient"
    },
    "occurrencePeriod": {
      "start": "2025-10-01T09:00:00+00:00",
      "end": "2025-10-01T09:30:00+00:00"
    },
    "authoredOn": "2025-09-30T19:12:25.073749+00:00",
    "requester": {
      "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
      "type": "Practitioner"
    },
    "reasonReference": [
      {
        "reference": "Condition/6700a428-6387-458d-8134-0702851da23c"
      }
    ]
}
```
    {% endtab %}

    {% tab ServiceRequest-read-response 401 %}
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

    {% tab ServiceRequest-read-response 403 %}
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

    {% tab ServiceRequest-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown ServiceRequest resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="ServiceRequest-search-request">
{% include search-request.html resource_type="ServiceRequest" search_string="patient=Patient/c4ff2ee2e41b4636b7d37ac7f9297d95" %}
</div>

<div id="ServiceRequest-search-response">

  {% tabs ServiceRequest-search-response %}

    {% tab ServiceRequest-search-response 200 %}
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 3,
  "link": [
    {
      "relation": "self",
      "url": "/ServiceRequest?patient=Patient%2Fc4ff2ee2e41b4636b7d37ac7f9297d95&_count=10&_offset=0"
    },
    {
      "relation": "first",
      "url": "/ServiceRequest?patient=Patient%2Fc4ff2ee2e41b4636b7d37ac7f9297d95&_count=10&_offset=0"
    },
    {
      "relation": "last",
      "url": "/ServiceRequest?patient=Patient%2Fc4ff2ee2e41b4636b7d37ac7f9297d95&_count=10&_offset=0"
    }
  ],
  "entry": [
    {
      "resource": {
        "resourceType": "ServiceRequest",
        "id": "bef0e33b-5008-489b-aa32-873b99e1e523",
        "status": "active",
        "intent": "order",
        "category": [
          {
            "coding": [
              {
                "system": "http://snomed.info/sct",
                "code": "363679005",
                "display": "Imaging"
              }
            ]
          }
        ],
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "24627-2",
              "display": "CT Chest"
            }
          ]
        },
        "subject": {
          "reference": "Patient/c4ff2ee2e41b4636b7d37ac7f9297d95",
          "type": "Patient"
        },
        "occurrencePeriod": {
          "start": "2025-10-01T09:00:00+00:00",
          "end": "2025-10-01T09:30:00+00:00"
        },
        "authoredOn": "2025-09-30T19:12:25.073749+00:00",
        "requester": {
          "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
          "type": "Practitioner"
        },
        "reasonReference": [
          {
            "reference": "Condition/6700a428-6387-458d-8134-0702851da23c"
          }
        ]
      }
    },
    {
      "resource": {
        "resourceType": "ServiceRequest",
        "id": "5938a56b-0239-47c5-ad31-703ca5104bb5",
        "status": "draft",
        "intent": "order",
        "category": [
          {
            "coding": [
              {
                "system": "http://snomed.info/sct",
                "code": "108252007",
                "display": "Laboratory procedure"
              }
            ]
          }
        ],
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "4544-3",
              "display": "Hematocrit"
            },
            {
              "system": "http://loinc.org",
              "code": "718-7",
              "display": "Hemoglobin"
            }
          ]
        },
        "subject": {
          "reference": "Patient/c4ff2ee2e41b4636b7d37ac7f9297d95",
          "type": "Patient"
        },
        "occurrencePeriod": {
          "start": "2025-10-01T09:00:00+00:00",
          "end": "2025-10-01T09:30:00+00:00"
        },
        "authoredOn": "2025-09-30T19:12:25.100394+00:00",
        "requester": {
          "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
          "type": "Practitioner"
        },
        "reasonReference": [
          {
            "reference": "Condition/2db04232-de4f-4d59-8066-2e5cee1c2a1d"
          }
        ]
      }
    },
    {
      "resource": {
        "resourceType": "ServiceRequest",
        "id": "db35b108-a9f3-4d70-bc76-4c4800bce005",
        "status": "completed",
        "intent": "order",
        "category": [
          {
            "coding": [
              {
                "system": "http://snomed.info/sct",
                "code": "386053000",
                "display": "Evaluation procedure (procedure)"
              }
            ]
          }
        ],
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "103696004",
              "display": "Patient referral to specialist"
            }
          ]
        },
        "subject": {
          "reference": "Patient/c4ff2ee2e41b4636b7d37ac7f9297d95",
          "type": "Patient"
        },
        "occurrencePeriod": {
          "start": "2025-10-01T09:00:00+00:00",
          "end": "2025-10-01T09:30:00+00:00"
        },
        "authoredOn": "2025-09-30T19:12:25.121629+00:00",
        "requester": {
          "reference": "Practitioner/5eede137ecfe4124b8b773040e33be14",
          "type": "Practitioner"
        },
        "reasonReference": [
          {
            "reference": "Condition/691a6afa-a450-425e-a151-26b20f595efb"
          }
        ]
      }
    }
  ]
}
```
    {% endtab %}

    {% tab ServiceRequest-search-response 400 %}
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

    {% tab ServiceRequest-search-response 401 %}
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

    {% tab ServiceRequest-search-response 403 %}
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