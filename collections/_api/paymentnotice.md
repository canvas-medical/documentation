---
title: PaymentNotice
sections:
  - type: section
    blocks:
      - type: apidoc
        name: PaymentNotice
        article: "a"
        description: >-
          This resource provides the status of the payment for goods and services rendered, and the request and response resource references.<br><br>
          [https://hl7.org/fhir/R4/paymentnotice.html](https://hl7.org/fhir/R4/paymentnotice.html)<br><br>
          In Canvas, FHIR PaymentNotice records payments made toward a patient's balance.<br><br>
          See this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/1500001122421-Collect-a-payment) for information about how to collect payments.
        attributes:
          - name: id
            description: The identifier of the payment notice.
            type: string
            required_in: update
            exclude_in: create
          - name: extension
            type: array[json]
            description_for_all_endpoints: Specific FHIR extensions on resources are supported to be able to map some Canvas specific attributes. The copayment extensions contains references to claims used for copayments.
            create_description: If you are not denoting a copayment, then use PaymentNotice without the copayment extension for other type of payments.
            attributes:
              - name: url
                type: string
                required_in: create
                description: Identifies the meaning of the extension
                enum_options:
                  - value: http://schemas.canvasmedical.com/fhir/copayment-claims
              - name: extension
                type: array[json]
                description: A nested extension that contains references to Claims related to copayments.
                create_description: Use this extension to denote and reference a Claim targeted for a copayment. For producing copayments, only a single Claim is accepted.
                attributes:
                  - name: url
                    type: string
                    required_in: create
                    description: Identifies the meaning of the extension.
                    enum_options:
                      - value: claim
                  - name: valueReference
                    type: json
                    required_in: create
                    attributes:
                      - name: reference
                        type: string
                        required_in: create
                        description: The reference string of the [Claim](/api/claim) used for copayments in the format of `"Claim/f0dfefbe-3fe0-4ee7-bd44-636f7be073e9"`.
          - name: status
            type: string
            required_in: create,update
            description: Required by the FHIR spec.
            enum_options: 
                - value: active
          - name: request
            type: json
            required_in: create,update
            description: >-
              A reference to the patient whose balance this payment is being applied to.
            attributes:
                - name: reference
                  type: string
                  required_in: create,update
                  description: The reference string of the patient in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Patient").
          - name: created
            type: datetime
            required_in: create,update
            description: >-
              Required by the FHIR spec. Canvas recommends sending the current date on create; however, the value returned by the search interaction will be the creation timestamp of the actual database record in Canvas.
          - name: payment
            type: json
            required_in: create,update
            description_for_all_endpoints: >-
              The `payment` field is required by FHIR, but is not used by Canvas. 
            create_description: Canvas recommends sending an empty JSON object.
            exclude_attributes_in: create,update
            attributes:
                - name: display
                  exclude_in: create,update
                  description: Text alternative for the resource.
                  enum_options: 
                    - value: unused
          - name: recipient
            type: json
            required_in: create,update
            description_for_all_endpoints: >-
              The `recipient` field is required by FHIR, but is not used by Canvas. 
            create_description: Canvas recommends sending an empty JSON object.
            exclude_attributes_in: create,update
            attributes:
                - name: display
                  exclude_in: create,update
                  description: Text alternative for the resource.
                  enum_options: 
                    - value: unused
          - name: amount
            type: json
            required_in: create,update
            description: >-
              The payment amount.
            attributes:
                - name: value
                  type: decimal
                  description: >-
                    The amount of USD to apply to the patient's balance.
                - name: currency
                  type: code
                  exclude_in: create
                  description: ISO 4217 Currency Code. Only **USD** is supported, and **USD** will be used regardless of what is provided.
                  enum_options:
                    - value: USD
          - name: paymentStatus
            type: json
            exclude_in: create
            description: Issued or cleared Status of the payment.
            attributes:
              - name: coding
                type: array[json]
                description: Code defined by a terminology system. There will be a single coding of **paid**.
                attributes:
                  - name: system
                    type: string
                    enum_options:
                        - value: http://terminology.hl7.org/CodeSystem/paymentstatus
                  - name: code
                    type: string
                    description: >-
                      In search responses, the code of **paid** will be noted.
                    enum_options: 
                        - value: paid
        search_parameters:
          - name: _id
            description: The Canvas-issued unique identifier of the PaymentNotice
            type: string
          - name: request
            type: string
            description: The patient reference associated to the PaymentNotice in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
        endpoints: [create, read, search]
        create:
          description: >-
            Create a PaymentNotice resource.<br><br>
            This endpoint can be used to note a payment that has been collected from a patient and deduct the amount from their balance.<br><br>
            Moreover, this endpoint can be used to denote copayments as well. For that purpose, use the valueReference extension to link the associated Claim for which the copayment is being processed. Adding that extension determines the purpose of action for this endpoint, meaning that it would be treated as a copayment transaction if the Claim reference extension is present.<br><br>
            **Don't overpay!** Requests that would bring the account balance negative will be rejected. Example: If a patient owes $5, Canvas would reject a PaymentNotice with a value that is greater than $5. Balance can only go negative if performing copayments as customers could be charged prior to recieveing a medical service.<br><br>
            A created payment notice can be found in Canvas by going to the patient's chart, and clicking the paper icon in the top right corner. The created payment notice will be displayed under receipts. The "Originator" will be automatically set to Canvas Bot.<br><br>
            As payment notices are created, they will be applied to charges in chronological order of creation date, from oldest to newest.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: paymentnotice-create-request
          example_response: paymentnotice-create-response
        read:
          description: Read a PaymentNotice resource.
          responses: [200, 401, 403, 404]
          example_request: paymentnotice-read-request
          example_response: paymentnotice-read-response
        search:
          description: Search for PaymentNotice resources.
          responses: [200, 400, 401, 403]
          example_request: paymentnotice-search-request
          example_response: paymentnotice-search-response
---

<div id="paymentnotice-create-request">

  {% tabs paymentnotice-create-request %}

    {% tab paymentnotice-create-request curl %}
```sh
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/PaymentNotice' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "PaymentNotice",
    "extension": [
        {
            "extension": [
                {
                    "url": "claim",
                    "valueReference": {
                        "reference": "Claim/f0dfefbe-3fe0-4ee7-bd44-636f7be073e9"
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/copayment-claims"
        }
    ],
    "status": "active",
    "request": {
        "reference": "Patient/bc4ec998a49745b488f552bebddf7261"
    },
    "created": "2023-09-12",
    "payment": {},
    "recipient": {},
    "amount": {
        "value": 10.00,
        "currency": "USD"
    }
}'
```
    {% endtab %}

    {% tab paymentnotice-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/PaymentNotice"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "PaymentNotice",
    "extension": [
        {
            "extension": [
                {
                    "url": "claim",
                    "valueReference": {
                        "reference": "Claim/f0dfefbe-3fe0-4ee7-bd44-636f7be073e9"
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/copayment-claims"
        }
    ],
    "status": "active",
    "request": {
        "reference": "Patient/bc4ec998a49745b488f552bebddf7261"
    },
    "created": "2023-09-12",
    "payment": {},
    "recipient": {},
    "amount": {
        "value": 10.00,
        "currency": "USD"
    }
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="paymentnotice-create-response">
{% include create-response.html %}
</div>

<div id="paymentnotice-read-request">
{% include read-request.html resource_type="PaymentNotice" %}
</div>

<div id="paymentnotice-read-response">

  {% tabs paymentnotice-read-response %}

    {% tab paymentnotice-read-response 200 %}
```json
{
    "resourceType": "PaymentNotice",
    "id": "297e160c-8246-4054-8023-554d8e14c8c8",
    "extension": [
        {
            "extension": [
                {
                    "url": "claim",
                    "valueReference": {
                        "reference": "Claim/f0dfefbe-3fe0-4ee7-bd44-636f7be073e9"
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/copayment-claims"
        }
    ],
    "status": "active",
    "request": {
        "reference": "Patient/3f688bb915d04e168dbfa635da4ab259",
        "type": "Patient"
    },
    "created": "2023-10-17T18:27:59.232743+00:00",
    "payment": {
        "display": "Unused"
    },
    "recipient": {
        "display": "Unused"
    },
    "amount": {
        "value": 25.0,
        "currency": "USD"
    },
    "paymentStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/paymentstatus",
                "code": "paid"
            }
        ]
    }
}
```
    {% endtab %}

    {% tab paymentnotice-read-response 401 %}
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

    {% tab paymentnotice-read-response 403 %}
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

    {% tab paymentnotice-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown PaymentNotice resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="paymentnotice-search-request">
{% include search-request.html resource_type="PaymentNotice" search_string="request=Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="paymentnotice-search-response">

  {% tabs paymentnotice-search-response %}

    {% tab paymentnotice-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/PaymentNotice?request=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/PaymentNotice?request=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/PaymentNotice?request=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "PaymentNotice",
                "id": "777094d2-664c-49b9-8926-b17a1b3fff8d",
                "status": "active",
                "request": {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
                    "type": "Patient"
                },
                "created": "2023-09-13T01:10:49.515238+00:00",
                "payment": {
                    "display": "Unused"
                },
                "recipient": {
                    "display": "Unused"
                },
                "amount": {
                    "value": 10.0,
                    "currency": "USD"
                },
                "paymentStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/paymentstatus",
                            "code": "paid"
                        }
                    ]
                }
            }
        },
        {
            "resource": {
                "resourceType": "PaymentNotice",
                "id": "3a2f4045-0591-460c-9bee-592ae7e8eef7",
                "extension": [
                    {
                        "extension": [
                            {
                                "url": "claim",
                                "valueReference": {
                                    "reference": "Claim/f0dfefbe-3fe0-4ee7-bd44-636f7be073e9"
                                }
                            }
                        ],
                        "url": "http://schemas.canvasmedical.com/fhir/copayment-claims"
                    }
                ],
                "status": "active",
                "request": {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
                    "type": "Patient"
                },
                "created": "2023-09-13T01:11:22.767640+00:00",
                "payment": {
                    "display": "Unused"
                },
                "recipient": {
                    "display": "Unused"
                },
                "amount": {
                    "value": 10.0,
                    "currency": "USD"
                },
                "paymentStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/paymentstatus",
                            "code": "paid"
                        }
                    ]
                }
            }
        }
    ]
}
```
    {% endtab %}

    {% tab paymentnotice-search-response 400 %}
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

    {% tab paymentnotice-search-response 401 %}
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

    {% tab paymentnotice-search-response 403 %}
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
