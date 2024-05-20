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
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            required_in: update
            exclude_in: create
            description: The identifier of the Coverage.
            type: string
          - name: status
            type: enum [ active | cancelled ]
            description: The status of the Coverage. <br><br>In Canvas, the status of `active` means it appears in the Patient's Profile page, while a status of `cancelled` means it was removed and no longer appears on the page. Of note, an expired coverage will still show as `active`, so be sure to set/read the `period.end` attribute.
            required_in: create,update
          - name: type
            type: json
            description: >-
              Type of coverage, such as medical, workers compensation, self pay, etc.<br><br>
              In order for this value to display on the Canvas UI, the coverage type needs to be configured for the specific payor via our insurer settings.  To get to these settings, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers).
            attributes:
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    required_in: create,update
                    enum_options: 
                      - value: http://hl7.org/fhir/ValueSet/coverage-type
                    type: string
                  - name: code
                    description: The code of the coverage type.
                    type: string
                    required_in: create,update
                    enum_options:
                       - value: ANNU
                       - value: AUTOPOL
                       - value: CHAR
                       - value: COL
                       - value: CRIME
                       - value: DENTAL
                       - value: DENTPRG
                       - value: DIS
                       - value: DISEASE
                       - value: DRUGPOL
                       - value: EAP
                       - value: EWB
                       - value: ENDRENAL
                       - value: EHCPOL
                       - value: FLEXP
                       - value: GOVEMP
                       - value: HIP
                       - value: HMO
                       - value: HSAPOL
                       - value: HIRISK
                       - value: HIVAIDS
                       - value: IND
                       - value: LIFE
                       - value: LTC
                       - value: MCPOL
                       - value: MANDPOL
                       - value: MENTPOL
                       - value: MENTPRG
                       - value: MILITARY
                       - value: pay
                       - value: POS
                       - value: PPO
                       - value: PNC
                       - value: DISEASEPRG
                       - value: PUBLICPOL
                       - value: REI
                       - value: RETIRE
                       - value: SAFNET
                       - value: SOCIAL
                       - value: SUBSIDIZ
                       - value: SUBSIDMC
                       - value: SUBSUPP
                       - value: SUBPOL
                       - value: SUBPRG
                       - value: SURPL
                       - value: TLIFE
                       - value: UMBRL
                       - value: UNINSMOT
                       - value: ULIFE
                       - value: VET
                       - value: VISPOL
                       - value: CANPRG
                       - value: WCBPOL
                  - name: display
                    description: The display name of the coding.
                    type: string
                    enum_options:
                      - value: Annuity policy
                      - value: Automobile
                      - value: Charity program
                      - value: Collision coverage policy
                      - value: Crime victim program
                      - value: Dental care policy
                      - value: Dental program
                      - value: Disability insurance policy
                      - value: Disease specific policy
                      - value: Drug policy
                      - value: Employee assistance program
                      - value: Employee welfare benefit plan policy
                      - value: End renal program
                      - value: Extended healthcare
                      - value: Flexible benefit plan policy
                      - value: Government employee health program
                      - value: Health insurance plan policy
                      - value: Health maintenance organization policy
                      - value: Health spending account
                      - value: High risk pool program
                      - value: HIV-AIDS program
                      - value: Indigenous peoples health program
                      - value: Life insurance policy
                      - value: Long term care policy
                      - value: Managed care policy
                      - value: Mandatory health program
                      - value: Mental health policy
                      - value: Mental health program
                      - value: Military health program
                      - value: Pay
                      - value: Point of service policy
                      - value: Preferred provider organization policy
                      - value: Property and casualty insurance policy
                      - value: Public health program
                      - value: Public healthcare
                      - value: Reinsurance policy
                      - value: Retiree health program
                      - value: Safety net clinic program
                      - value: Social service program
                      - value: Subsidized health program
                      - value: Subsidized managed care program
                      - value: Subsidized supplemental health program
                      - value: Substance use policy
                      - value: Substance use program
                      - value: Surplus line insurance policy
                      - value: Term life insurance policy
                      - value: Umbrella liability insurance policy
                      - value: Uninsured motorist policy
                      - value: Universal life insurance policy
                      - value: Veteran health program
                      - value: Vision care policy
                      - value: Women's cancer detection program
                      - value: Worker's compensation
              - name: text
                exclude_in: create, update
                type: string
                description: The 2 character code that represents the patient relationship to the insured as defined by CMS.
                enum_options:
          - name: subscriber
            description: Who was signed up for or 'owns' the Coverage.
            type: json
            required_in: create,update
            attributes:
              - name: reference
                type: string
                required_in: create, update
                description: The reference string of the patient subscriber in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: subscriberId
            description: The insurer-assigned ID for the subscriber.
            type: string
            required_in: create,update
          - name: beneficiary
            description: >-
              Who benefits from the coverage; the patient when products or services are provided.
            type: json
            required_in: create,update
            attributes:
              - name: reference
                type: string
                required_in: create, update
                description: The reference string of the patient beneficiary in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: relationship
            type: json
            description: The relationship of beneficiary (patient) to the subscriber.
            required_in: create,update
            attributes:
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                required_in: create,update
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    required_in: create,update
                    enum_options: 
                      - value: http://hl7.org/fhir/ValueSet/subscriber-relationship
                    type: string
                  - name: code
                    description: The code of the relationship.
                    type: string
                    exclude_in: read, search
                    required_in: create,update
                    enum_options:
                      - value: child
                      - value: spouse
                      - value: other
                      - value: self
                      - value: injured
                  - name: code
                    description: The code of the relationship.
                    type: string
                    exclude_in: create, update
                    enum_options:
                      - value: child
                      - value: spouse
                      - value: other
                      - value: self
                      - value: injured
                      - value: parent
                      - value: common
                  - name: display
                    description: The display name of the coding.
                    type: string
              - name: text
                exclude_in: create, update
                type: string
                description: The 2 character code that represents the patient relationship to the insured as defined by CMS.
                enum_options:
                   - value: 18  (Self)
                   - value: 01  (Spouse)
                   - value: 19  (Natural Child, insured has financial responsibility)
                   - value: 43  (Natural Child, insured does not have financial responsibility),
                   - value: 17  (Step Child)
                   - value: 10  (Foster Child)
                   - value: 15  (Ward of the Court)
                   - value: 20  (Employee)
                   - value: 21  (Unknown)
                   - value: 22  (Handicapped Dependent)
                   - value: 39  (Organ donor)
                   - value: 40  (Cadaver donor)
                   - value: 05  (Grandchild)
                   - value: 07  (Niece/Nephew)
                   - value: 41  (Injured Plaintiff)
                   - value: 23  (Sponsored Dependent)
                   - value: 24  (Minor Dependent of a Minor Dependent)
                   - value: 32  (Mother)
                   - value: 33  (Father)
                   - value: 04  (Grandparent)
                   - value: 53  (Life Partner)
                   - value: 29  (Significant Other)
                   - value: G8  (Other)
          - name: period
            description: >-
              The period during which the Coverage is in force.<br><br>
              A missing end date means the coverage continues to be in force.
            create_and_update_description:
              If the start date is missing for a create/update interaction, it will be set to the current date of ingestion.
            type: json
            attributes:
              - name: start
                type: date
                description: Starting time with inclusive boundary
              - name: end
                type: date
                description: End time with inclusive boundary, if not ongoing.
          - name: payor
            type: array[json]
            description_for_all_endpoints: Issuer of the policy.
            create_and_update_description: >-
              Two methods for specifying this data are supported:
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
               A `reference` or `identifier.value` is required in a Create/Update.
            required_in: create,update
            attributes:
              - name: reference
                type: string
                description: The Organization reference to the Coverage's payor in the format "Organization/6741b035-2846-45b3-b7a3-251f7b7fc728"
              - name: type
                description: Type the reference refers to (e.g. "Organization").
                type: string
              - name: display
                description: The display name of the payor.
                type: string
              - name: identifier
                exclude_in: read,search
                type: json
                description: Logical reference, when literal reference is not known. 
                attributes:
                  - name: value
                    type: string
                    required_in: create, update
                    description: The value that is unique. These values can only be found and updated in the [Insurers Admin view](https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers) in Canvas. 
                  - name: system
                    type: string
                    description: The namespace for the identifier value. 
                    enum_options: 
                      - value: https://www.claim.md/services/era/
          - name: class
            type: json
            description: >-
              Additional coverage classifications.<br><br>
              Only plan and group will be visible in the Canvas UI.
            attributes:
              - name: type
                type: json
                required_in: create, update
                description: Type of class such as 'group' or 'plan'.
                attributes:
                  - name: coding
                    description: Identifies where the definition of the code comes from.
                    type: array[json]
                    required_in: create,update
                    attributes: 
                      - name: system
                        description: The system url of the coding.
                        required_in: create,update
                        enum_options: 
                          - value: http://hl7.org/fhir/ValueSet/coverage-class
                        type: string
                      - name: code
                        description: The code of the class. 
                        type: string
                        required_in: create,update
                        enum_options:
                          - value: plan
                          - value: subplan
                          - value: group
                          - value: subgroup
                  - name: value
                    type: string
                    description: Value associated with the type.
          - name: order
            type: number [ 1-5 ]
            required_in: create,update
            description_for_all_endpoints: >-
              The order in which coverages should be used when adjudicating claims.
            create_and_update_description:
                The order must between 1 and 5, inclusive.<br><br>
                If multiple coverages for a patient are created with the same order number, the older one will be bumped down in rank, and the new one will take that rank.<br><br>
                If this leads to multiple coverages being incremented to 5, the oldest (first to be inputted into Canvas) of the coverages at this rank will be displayed on the Canvas UI.
        search_parameters:
          - name: _id
            type: string
            description: The Canvas resource identifier of the Coverage.
          - name: patient
            type: string
            description: Retrieve coverages for a patient in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
          - name: subscriberid
            type: string
            description: Retrieve all coverages with a specific subscriberID
          - name: status
            type: string
            description: Retrieve coverages by a specific status.
            search_options:
              - value: active
              - value: cancelled
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
        "status": "cancelled",
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
        "status": "cancelled",
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
