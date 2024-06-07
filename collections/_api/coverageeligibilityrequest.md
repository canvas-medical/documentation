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
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: status
            type: string
            required_in: create
            description: Describes the state the request is in.
            enum_options:
              - value: active
          - name: purpose
            type: array[string]
            required_in: create
            description: >-
              What information is being requested.<br><br>Supported values: only **["benefits"]** is valid
          - name: patient
            type: json
            required_in: create
            description: Canvas patient resource whom the eligibility request is for.
            attributes:
              - name: reference
                type: string
                required_in: create
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: created
            type: date
            required_in: create
            description: >-
              Creation date, required by the FHIR schema, but unused by Canvas as it will be defaulted to the Canvas ingestion timestamp.<br><br>
              Canvas recommends sending the current datetime in ISO 8601 format.
          - name: insurer
            type: json
            required_in: create
            description: >-
              Coverage issuer, required by the FHIR schema but unused by Canvas because we inherit the issuer directly from the Coverage resource provided.<br><br>
              Canvas recommends setting `insurer` to `{}`.
          - name: insurance
            type: array[json]
            required_in: create
            description: Patient insurance information.<br><br>Canvas requires a single coverage resource identifying the insurance to check eligibility against.
            attributes:
              - value: coverage
                type: json
                required_in: create
                description: Insurance information.
                attributes:
                  - name: reference
                    type: string
                    required_in: create
                    description: The reference string of the coverage in the format of `"Coverage/f7663d7b-13bd-4236-843e-086306aea125"`.
        endpoints: [create]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: coverageeligibilityrequest-create-request
          example_response: coverageeligibilityrequest-create-response
          description: If Claim.MD is set up in your Canvas instance, a creation of a coverage eligibility request will kick off a request to Claim.MD to fetch the eligibility information. Use the returned `id` in the response.headers['location'] attribute to perform a [CoverageEligibilityResponse Search](/api/coverageeligibilityresponse/#search) to see what response Claim.MD returned.
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
