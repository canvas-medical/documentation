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
            description: >-
              The identifier of the payment notice
            type: string
            required: true
          - name: status
            type: string
            required: true
            description: >-
              Required by the FHIR spec. Canvas only supports payments with a status of **active**.
          - name: request
            type: json
            required: true
            description: >-
              A reference to the patient whose balance this payment is being applied to.
            attributes:
                - name: reference
                  type: string
                  required: true
          - name: created
            type: datetime
            required: true
            description: >-
              Required by the FHIR spec. We recommend sending the current datetime on create; however, the value returned by the search interaction will be the creation timestamp of the actual database record.
          - name: payment
            type: json
            required: true
            description: >-
              The `payment` field is required by FHIR, but is not used by Canvas. Canvas recommends sending an empty JSON object.
          - name: recipient
            type: json
            required: true
            description: >-
              The `recipient` field is required by FHIR, but is not used by Canvas. Canvas recommends sending an empty JSON object.
          - name: amount
            type: json
            required: true
            description: >-
              The payment amount.
            attributes:
                - name: value
                  type: decimal
                  description: >-
                    The amount of USD to apply to the patient's balance.
                - name: currency
                  type: code
                  description: >-
                    Only **USD** is supported, and **USD** will be used regardless of what is provided.
          - name: paymentStatus
            type: json
            required: false
            description: >-
              Status of the payment
            attributes:
              - name: coding
                type: array
                description: >-
                  In search responses, there will be a single coding of **paid**.
                attributes:
                  - name: system
                    type: string
                  - name: code
                    type: string
                    description: >-
                      In search responses, the code of **paid** will be noted.
        search_parameters:
          - name: request
            type: string
            description: A reference to the patient whose balance the payment was applied to.
        endpoints: [create, search]
        create:
          description: >-
            Create a PaymentNotice resource.<br><br>
            This endpoint can be used to note a payment that has been collected from a patient and deduct the amount from their balance.<br><br>
            **Don't overpay!** Requests that would bring the account balance negative will be rejected. Example: If a patient owes $5, Canvas would reject a PaymentNotice with a value that is greater than $5.<br><br>
            A created payment notice can be found in Canvas by going to the patient's chart, and clicking the paper icon in the top right corner. The created payment notice will be displayed under receipts. The "Originator" will be automatically set to Canvas Bot.<br><br>
            As payment notices are created, they will be applied to charges in chronological order of creation date, from oldest to newest.
          responses: [201, 400, 401, 403, 405, 422]
          example_request: paymentnotice-create-request
          example_response: paymentnotice-create-response
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
     --url https://fumage-example.canvasmedical.com/PaymentNotice \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "PaymentNotice",
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
'
```
    {% endtab %}

    {% tab paymentnotice-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/PaymentNotice"

payload = {
    "resourceType": "PaymentNotice",
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

<div id="paymentnotice-create-response">
{% include create-response.html %}
</div>

<div id="paymentnotice-search-request">
{% include search-request.html resource_type="PaymentNotice" search_string="request=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="paymentnotice-search-response">

  {% tabs paymentnotice-search-response %}

    {% tab paymentnotice-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
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
    "entry":
    [
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
