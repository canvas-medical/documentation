---
title: CoverageEligibilityRequest
sections:
  - type: section
    blocks:
      - type: apidoc
        name: CoverageEligibilityRequest
        article: "a"
        description: >-
          The CoverageEligibilityRequest provides patient and insurance coverage information to an insurer for them to respond, in the form of an CoverageEligibilityResponse, with information regarding whether the stated coverage is valid and in-force and optionally to provide the insurance details of the policy.
        attributes:
          - name: integration_type
            type: string
            required: true
          - name: integration_source
            type: string
            required: true
            description: >-
              The source of integration. This will be hardcoded to `fumage` for this endpoint
          - name: patient_identifier
            type: json
            required: true
            attributes:
              - name: identifier_type
                type: string
                required: true
                description: >-
                  The type of integration. This will be hardcoded to `fumage` for this endpoint
              - name: identifier
                type: string
                required: true
          - name: integration_payload
            type: json
            required: true
            attributes:
              - name: coverage_identifier
                type: string
                required: true
        endpoints: [create]
        create:
          responses: [201, 400]
          example_request: coverage-eligibility-request-create-request
          example_response: coverage-eligibility-request-create-response
---
<div id="coverage-eligibility-request-create-request">
{% tabs create-request %}
{% tab create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/CoverageEligibilityRequest"

payload = {
    "status": "active",
    "purpose": ["benefits"],
    "patient": { "reference": "Patient/9713f5a3c8464a2587912e80bc2dd938" },
    "created": "2021-08-27",
    "insurance": [
        {
            "focal": True,
            "coverage": { "reference": "Coverage/743aa331-2f85-420b-ab10-8a6b7bb6a1cf" }
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
{% tab create-request curl %}
```sh
curl --request POST \
     --url https://fumage-example.canvasmedical.com/CoverageEligibilityRequest \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "status": "active",
  "purpose": [
    "benefits"
  ],
  "patient": {
    "reference": "Patient/9713f5a3c8464a2587912e80bc2dd938"
  },
  "created": "2021-08-27",
  "insurance": [
    {
      "focal": true,
      "coverage": {
        "reference": "Coverage/743aa331-2f85-420b-ab10-8a6b7bb6a1cf"
      }
    }
  ]
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="coverage-eligibility-request-create-response">
{% tabs create-response %}
{% tab create-response 201 %}
```json
null
```
{% endtab %}
{% tab create-response 400 %}
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

