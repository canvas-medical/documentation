---
title: PaymentNotice
sections:
  - type: section
    blocks:
      - type: apidoc
        name: PaymentNotice
        article: "a"
        description: >-
          Records of payments made towards a patient's balance.<br><br>
          [https://hl7.org/fhir/R4/paymentnotice.html](https://hl7.org/fhir/R4/paymentnotice.html)
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
        endpoints: [search, create]
        search:
          responses: [200, 401, 403]
          example_request: payment-notice-search-request
          example_response: payment-notice-search-response
        create:
          responses: [201, 400, 401, 403]
          example_request: payment-notice-create-request
          example_response: payment-notice-create-response
---
<div id="payment-notice-search-request">
{% tabs payment-notice-search-request %}
{% tab payment-notice-search-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/PaymentNotice?request=Patient/<patient_id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab payment-notice-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/PaymentNotice?request=Patient/<patient_id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="payment-notice-search-response">
{% tabs payment-notice-search-response %}
{% tab payment-notice-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link": [
        {
            "relation": "self",
            "url": "/PaymentNotice?request=Patient%2Fbc4ec998a49745b488f552bebddf7261&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/PaymentNotice?request=Patient%2Fbc4ec998a49745b488f552bebddf7261&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/PaymentNotice?request=Patient%2Fbc4ec998a49745b488f552bebddf7261&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "PaymentNotice",
                "id": "777094d2-664c-49b9-8926-b17a1b3fff8d",
                "status": "active",
                "request": {
                    "reference": "Patient/bc4ec998a49745b488f552bebddf7261",
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
                    "reference": "Patient/bc4ec998a49745b488f552bebddf7261",
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
{% tab payment-notice-search-response 401 %}
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
{% tab payment-notice-search-response 403 %}
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

<div id="payment-notice-create-request">
{% tabs payment-notice-create-request %}
{% tab payment-notice-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/PaymentNotice"

payload = {
    "resourceType": "PaymentNotice",
    "status": "active",
    "request": {
      "reference": "Patient/bc4ec998a49745b488f552bebddf7261"
    },
    "payment": {},
    "recipient": {},
    "created": "2023-09-12",
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
{% tab payment-notice-create-request curl %}
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
    "payment": {},
    "recipient": {},
    "created": "2023-09-12",
    "amount": {
      "value": 10.00,
      "currency": "USD"
    }
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="payment-notice-create-response">
{% tabs payment-notice-create-response %}
{% tab payment-notice-create-response 201 %}
```json
null
```
{% endtab %}
{% tab payment-notice-create-response 400 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "required",
            "details": {
                "text": "body -> __root__ -> created — field required (type=value_error.missing)"
            }
        },
        {
            "severity": "error",
            "code": "required",
            "details": {
                "text": "body -> __root__ -> status — field required (type=value_error.missing)"
            }
        }
    ]
}
```
{% endtab %}
{% tab payment-notice-create-response 401 %}
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
{% tab payment-notice-create-response 403 %}
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
