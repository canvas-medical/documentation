---
title: CoverageEligibilityRequest
sections:
  - type: section
    blocks:
      - type: apidoc
        name: CoverageEligibilityRequest
        article: "a"
        description: >-
          The CoverageEligibilityRequest provides patient and insurance coverage information to an insurer for them to respond, in the form of an CoverageEligibilityResponse, with information regarding whether the stated coverage is valid and in-force.<br><br>
          [https://hl7.org/fhir/R4/coverageeligibilityrequest.html](https://hl7.org/fhir/R4/coverageeligibilityrequest.html)
        attributes:
          - name: status
            type: string
            required: true
            description: >-
              Describes the state the request is in.<br><br>Supported values: **active**
          - name: purpose
            type: array[string]
            required: true
            description: >-
              What information is being requested.<br><br>Supported values: only **["benefits"]** is valid
          - name: patient
            type: json
            required: true
            description: >-
              Canvas patient resource whom the eligibility request is for
          - name: created
            type: date
            required: true
            description: >-
              Creation date, required by the FHIR schema, but unused by Canvas.<br><br>
              Canvas recommends sending the current datetime in ISO 8601 format.
          - name: insurer
            type: json
            required: true
            description: >-
              Coverage issuer, required by the FHIR schema but unused by Canvas.<br><br>
              Canvas recommends setting `insurer` to `{}`.
          - name: insurance
            type: array[json]
            required: true
            description: >-
              Canvas Coverage resource identifying the insurance to check eligibility against<br><br>
              Supported values: a single iteration containing a **Coverage** resource.<br><br>
              **focal** is not required - all requests are processed as **true**
        endpoints: [create]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: coverageeligibilityrequest-create-request
          example_response: coverageeligibilityrequest-create-response
---

<div id="coverageeligibilityrequest-create-request">
  {% tabs coverageeligibilityrequest-create-request %}
    {% tab coverageeligibilityrequest-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/CoverageEligibilityRequest' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "CoverageEligibilityRequest",
    "status": "active",
    "purpose": [
        "benefits"
    ],
    "patient": {
        "reference": "Patient/9713f5a3c8464a2587912e80bc2dd938"
    },
    "created": "2023-09-19",
    "insurer": {},
    "insurance": [
        {
            "focal": true,
            "coverage": {
                "reference": "Coverage/743aa331-2f85-420b-ab10-8a6b7bb6a1cf"
            }
        }
    ]
}'
```
    {% endtab %}

    {% tab coverageeligibilityrequest-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/CoverageEligibilityRequest"

payload = {
    "resourceType": "CoverageEligibilityRequest",
    "status": "active",
    "purpose": [
        "benefits"
    ],
    "patient": {
        "reference": "Patient/9713f5a3c8464a2587912e80bc2dd938"
    },
    "created": "2023-09-19",
    "insurer": {},
    "insurance": [
        {
            "focal": True,
            "coverage": {
                "reference": "Coverage/743aa331-2f85-420b-ab10-8a6b7bb6a1cf"
            }
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

<div id="coverageeligibilityrequest-create-response">
{% include create-response.html %}
</div>
