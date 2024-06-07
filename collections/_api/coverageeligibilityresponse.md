---
title: CoverageEligibilityResponse
sections:
  - type: section
    blocks:
      - type: apidoc
        name: CoverageEligibilityResponse
        article: "a"
        description: >-
         The CoverageEligibilityResponse resource provides eligibility and plan details from processing a CoverageEligibilityRequest resource. It combines key information from a payor as to whether a Coverage is in-force, and optionally the nature of the Policy benefit details as well as the ability for the insurer to indicate whether the insurance provides benefits for requested types of services or requires preauthorization and if so what supporting information may be required.<br><br>
         [https://hl7.org/fhir/R4/coverageeligibilityresponse.html](https://hl7.org/fhir/R4/coverageeligibilityresponse.html)
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            type: string
            description: The identifier of the coverage eligibility response.
          - name: status
            type: string
            description: Status of the resource.
            enum_options:
              - value: active
              - value: entered-in-error
          - name: purpose
            type: array[string]
            description: Reason for the request, will always be **["benefits"]**
          - name: patient
            type: json
            description: Patient resource the eligibility response is for.
            attributes:
              - name: reference
                type: string
                description: The reference string of the patient in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: created
            type: datetime
            description: Response creation date.
          - name: request
            type: json
            description: CoverageEligibilityRequest reference the elibibility response is for.
            attributes:
              - name: reference
                type: string
                description: The reference string of the request in the format of `"CoverageEligibilityRequest/cd98975b-6cd4-413d-ab65-1fc5eec76762"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "CoverageEligibilityRequest").
          - name: outcome
            type: string
            description: Outcome of the request processing, if an error occurs it will be marked as **"error"** othervise it will be marked as **"complete"**.
            enum_options: 
              - value: error
              - value: complete
          - name: insurer
            type: json
            description:  Coverage issuer.
            attributes:
              - value: identifier
                type: string
                description: Payor ID for the Coverage issuer.
              - value: display
                type: string
                description: Text alternative for the resource.
          - name: insurance
            type: array[json]
            description: >-
              Patient insurance information. This includes the **Coverage** reference, extension for plan name and an array of items containing benefits and authorization details returned from Claim.MD.<br><br>
              The amount of information surfaced here depends on the what the payor supports. Our clearinghouse (Claim.md) performs these eligibility checks, but not all coverages will support real-time eligibility checks. For more information on coverages within Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4408206355603-Patient-Coverages-2-0).
            attributes:
                - name: coverage 
                  description: Insurance information.
                  type: json
                  attributes:
                      - name: reference
                        type: string
                        description: The reference string of the coverage in the format of `"Coverage/4a86f580-e192-489a-a9f0-7c915fc67111"`.
                      - name: type
                        type: string
                        description: Type the reference refers to (e.g. "Coverage").
                - name: extension
                  type: array[json]
                  read_and_search_description: Canvas supports a plan name extension on this resource for read and search interactions.
                  attributes:
                      - name: url
                        type: string
                        description: Reference that defines the content of this object.
                        enum_options:
                          - value: http://schemas.canvasmedical.com/fhir/extensions/active-health-benefit-plan-coverage-description
                      - name: valueString
                        type: string
                        description: The plan name of the insurance.
                - name: item
                  description: Array of items containing benefits and authorization details.
                  type: array[json]
                  attributes:
                    - name: name
                      type: string
                      description: Short name for the benefit
                    - name: unit
                      type: json
                      description: Individual or family.
                      attributes:
                        - name: coding
                          description: Code defined by a terminology system.
                          type: array[json]
                          attributes: 
                            - name: system
                              description: The system url of the coding.
                              enum_options: 
                                - value: http://terminology.hl7.org/CodeSystem/benefit-unit
                              type: string
                            - name: code
                              description: The code of the benefit unit.
                              type: string
                              enum_options:
                                - value: individual
                                - value: family
                            - name: display
                              description: The display name of the coding.
                              type: string
                              enum_options:
                                - value: Individual
                                - value: Family
                        - name: text
                          type: string
                          description: Plain text representation of the concept.
                          enum_options:
                            - value: Individual
                            - value: Family
                    - name: network
                      type: json
                      description: In or out of network.
                      attributes:
                        - name: coding
                          description: Code defined by a terminology system.
                          type: array[json]
                          attributes: 
                            - name: system
                              description: The system url of the coding.
                              enum_options: 
                                - value: http://terminology.hl7.org/CodeSystem/benefit-unit
                              type: string
                            - name: code
                              description: The code of the benefit network.
                              type: string
                              enum_options:
                                - value: in
                                - value: out
                            - name: display
                              description: The display name of the coding.
                              type: string
                              enum_options:
                                - value: In Network
                                - value: Out of Network
                        - name: text
                          type: string
                          description: Plain text representation of the concept.
                          enum_options:
                            - value: In Network
                            - value: Out of Network
                    - name: benefit
                      type: array[json]
                      description: Benefit Summary.
                      attributes:
                        - name: type
                          type: json
                          description: Benefit classification.
                          attributes:
                            - name: text
                              type: string
                              description: Plain text representation of the concept.
                              enum_options:
                                - value: 'Co-Insurance'
                                - value: 'Co-Payment'
                                - value: 'Active Coverage'
                                - value: 'Deductible'
                                - value: 'Out of Pocket (Stop Loss)'
                                - value: 'Limitations'
                                - value: 'Contact following entity for eligibility or benefit information'
                                - value: '<information_type> (Incomplete Information)'
                            - name: allowedString
                              type: string
                              description: Benefits allowed. <br><br>Used for Co-Insurance benefit types.
                            - name: allowedMoney
                              type: json
                              description: Benefits allowed. <br><br>Used for Co-Payment, Deductible, or Out of Pocket benefit types.
                              attributes: 
                                - name: value
                                  type: decimal
                                  description: Numerical value (with implicit precision)
                            - name: allowedUnsignedInt
                              type: unsignedInt
                              description: Benefits allowed. <br><br>Used for Limitations benefit types.
                            - name: usedMoney
                              type: json
                              description: Benefits used. <br><br>Used for Deductible or Out of Pocket benefit types.
                              attributes: 
                                - name: value
                                  type: decimal
                                  description: Numerical value (with implicit precision)
                            - name: usedUnsignedInt
                              type: unsignedInt
                              description: Benefits used. <br><br>Used for Limitations benefit types.


        search_parameters:
          - name: _id
            type: string
            description: The Canvas resource identifier of the CoverageEligibilityResponse.
          - name: patient
            type: string
            description: The patient reference associated with the Coverage Eligibility Response in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
          - name: request
            type: string
            description: The coverage eligibility request reference associated with the Coverage Eligibility Response in the format `"CoverageEligibilityRequest/cd98975b-6cd4-413d-ab65-1fc5eec76762"`.
        endpoints: [read, search]
        read:
          responses: [200, 401, 403, 404]
          example_request: coverageeligibilityresponse-read-request
          example_response: coverageeligibilityresponse-read-response
        search:
          responses: [200, 400, 401, 403]
          example_request: coverageeligibilityresponse-search-request
          example_response: coverageeligibilityresponse-search-response
---

<div id="coverageeligibilityresponse-read-request">
{% include read-request.html resource_type="CoverageEligibilityResponse" %}
</div>

<div id="coverageeligibilityresponse-read-response">
  {% tabs coverageeligibilityresponse-read-response %}

    {% tab coverageeligibilityresponse-read-response 200 %}
```json
{
  "resourceType": "CoverageEligibilityResponse",
  "id": "9ad12f4e-4f35-4f54-8b4f-036516488191",
  "status": "active",
  "purpose": [
      "benefits"
  ],
  "patient": {
      "reference": "Patient/b41c7cda738d440cb55e0e6cb67499a1",
      "type": "Patient"
  },
  "created": "2023-09-19T18:16:39.551617+00:00",
  "request": {
      "reference": "CoverageEligibilityRequest/d7254641-e363-488c-91fa-b93a6170b9e0",
      "type": "CoverageEligibilityRequest"
  },
  "outcome": "complete",
  "insurer": {
      "identifier": "1111",
      "display": "Payer ID: 1111"
  },
  "insurance": [
    {
      "extension": [
        {
          "url": "http://schemas.canvasmedical.com/fhir/extensions/active-health-benefit-plan-coverage-description",
          "valueString": "Humana Gold Plus"
        }
      ],
      "coverage": {
          "reference": "Coverage/4a86f580-e192-489a-a9f0-7c915fc67111",
          "type": "Coverage"
      },
      "item": [
        {
          "network": {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                "code": "in",
                "display": "In Network"
              }
            ],
            "text": "In Network"
          },
          "unit": {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                "code": "individual",
                "display": "Individual"
              }
            ],
            "text": "Individual"
          },
          "benefit": [
            {
              "type": {
                  "text": "Co-Payment"
              },
              "allowedMoney": {
                  "value": 333
              }
            },
            {
              "type": {
                  "text": "Co-Insurance"
              },
              "allowedString": "0.0%"
            }
          ]
        },
        {
          "network": {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                "code": "in",
                "display": "In Network"
              }
            ],
            "text": "In Network"
          },
          "unit": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                  "code": "individual",
                  "display": "Individual"
                }
              ],
              "text": "Individual"
          },
            "benefit": [
              {
                "type": {
                    "text": "Co-Insurance"
                },
                "allowedString": "0.0%"
              },
              {
                "type": {
                    "text": "Co-Insurance"
                },
                "allowedString": "0.0%"
              },
              {
                "type": {
                    "text": "Co-Insurance"
                },
                "allowedString": "0.0%"
              }
            ]
        },
        {
          "benefit": [
            {
              "type": {
                  "text": "Benefit Description (Incomplete information)"
              }
            }
          ]
        },
        {
          "benefit": [
            {
              "type": {
                  "text": "Active Coverage"
              }
            }
          ]
        },
        {
          "network": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                  "code": "in",
                  "display": "In Network"
                }
              ],
              "text": "In Network"
          },
          "benefit": [
            {
              "type": {
                  "text": "Active Coverage"
              }
            },
            {
              "type": {
                  "text": "Primary Care Provider (Incomplete information)"
              }
            },
            {
              "type": {
                  "text": "Benefit Description (Incomplete information)"
              }
            },
            {
              "type": {
                  "text": "Benefit Disclaimer (Incomplete information)"
              }
            }
          ]
        },
        {
          "name": "Dental Care",
          "network": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                  "code": "in",
                  "display": "In Network"
                }
              ],
              "text": "In Network"
          },
          "unit": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                  "code": "individual",
                  "display": "Individual"
                }
              ],
              "text": "Individual"
          },
          "benefit": [
            {
              "type": {
                  "text": "Active Coverage"
              }
            }
          ]
        },
        {
          "name": "Health Benefit Plan Coverage",
          "network": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                  "code": "in",
                  "display": "In Network"
                }
              ],
              "text": "In Network"
          },
          "unit": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                  "code": "individual",
                  "display": "Individual"
                }
              ],
              "text": "Individual"
          },
          "benefit": [
            {
              "type": {
                  "text": "Deductible (Incomplete information)"
              }
            },
            {
              "type": {
                  "text": "Deductible"
              },
              "allowedMoney": {
                  "value": 6900
              },
              "usedMoney": {
                  "value": 0.0
              }
            },
            {
              "type": {
                  "text": "Active Coverage"
              }
            },
            {
              "type": {
                  "text": "Out of Pocket (Stop Loss)"
              },
              "allowedMoney": {
                  "value": 6900
              },
              "usedMoney": {
                  "value": 0.0
              }
            },
            {
              "type": {
                  "text": "Out of Pocket (Stop Loss)"
              },
              "allowedMoney": {
                  "value": 6900
              },
              "usedMoney": {
                  "value": 0.0
              }
            }
          ]
        },
        {
          "name": "Health Benefit Plan Coverage",
          "network": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                  "code": "in",
                  "display": "In Network"
                }
              ],
              "text": "In Network"
          },
          "benefit": [
            {
              "type": {
                  "text": "Benefit Description (Incomplete information)"
              }
            }
          ]
        },
        {
          "name": "Physician Visit - Well",
          "network": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                  "code": "in",
                  "display": "In Network"
                }
              ],
              "text": "In Network"
          },
          "benefit": [
            {
              "type": {
                  "text": "Non-Covered (Incomplete information)"
              }
            }
          ]
        },
        {
          "name": "Professional (Physician) Visit - Office",
          "network": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                  "code": "in",
                  "display": "In Network"
                }
              ],
              "text": "In Network"
          },
          "unit": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                  "code": "individual",
                  "display": "Individual"
                }
              ],
              "text": "Individual"
          },
          "benefit": [
            {
              "type": {
                  "text": "Co-Insurance"
              },
              "allowedString": "0.0%"
            }
          ]
        },
        {
          "name": "Professional (Physician) Visit - Office",
          "network": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                  "code": "in",
                  "display": "In Network"
                }
              ],
              "text": "In Network"
          },
          "benefit": [
            {
              "type": {
                  "text": "Non-Covered (Incomplete information)"
              }
            },
            {
              "type": {
                  "text": "Active Coverage"
              }
            }
          ]
        }
      ]
    }
  ]
}
```
    {% endtab %}

    {% tab coverageeligibilityresponse-read-response 401 %}
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

    {% tab coverageeligibilityresponse-read-response 403 %}
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

    {% tab coverageeligibilityresponse-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown CoverageEligibilityResponse resource 'c152eeb7-f204-4e28-acb5-c7e85390b17e'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="coverageeligibilityresponse-search-request">
{% include search-request.html resource_type="Group" search_string="request=CoverageEligibilityRequest/b41c7cda738d440cb55e0e6cb67499a1" %}
</div>

<div id="coverageeligibilityresponse-search-response">
{% tabs coverageeligibilityresponse-search-response %}
{% tab coverageeligibilityresponse-search-response 200 %}
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 1,
  "entry": [
    {
      "resource": {
        "resourceType": "CoverageEligibilityResponse",
        "id": "9ad12f4e-4f35-4f54-8b4f-036516488191",
        "status": "active",
        "purpose": [
            "benefits"
        ],
        "patient": {
            "reference": "Patient/b41c7cda738d440cb55e0e6cb67499a1",
            "type": "Patient"
        },
        "created": "2023-09-19T18:16:39.551617+00:00",
        "request": {
            "reference": "CoverageEligibilityRequest/d7254641-e363-488c-91fa-b93a6170b9e0",
            "type": "CoverageEligibilityRequest"
        },
        "outcome": "complete",
        "insurer": {
            "identifier": "1111",
            "display": "Payer ID: 1111"
        },
        "insurance": [
          {
            "extension": [
              {
                "url": "http://schemas.canvasmedical.com/fhir/extensions/active-health-benefit-plan-coverage-description",
                "valueString": "Humana Gold Plus"
              }
            ],
            "coverage": {
                "reference": "Coverage/4a86f580-e192-489a-a9f0-7c915fc67111",
                "type": "Coverage"
            },
            "item": [
              {
                "network": {
                  "coding": [
                    {
                      "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                      "code": "in",
                      "display": "In Network"
                    }
                  ],
                  "text": "In Network"
                },
                "unit": {
                  "coding": [
                    {
                      "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                      "code": "individual",
                      "display": "Individual"
                    }
                  ],
                  "text": "Individual"
                },
                "benefit": [
                  {
                    "type": {
                        "text": "Co-Payment"
                    },
                    "allowedMoney": {
                        "value": 333
                    }
                  },
                  {
                    "type": {
                        "text": "Co-Insurance"
                    },
                    "allowedString": "0.0%"
                  }
                ]
              },
              {
                "network": {
                  "coding": [
                    {
                      "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                      "code": "in",
                      "display": "In Network"
                    }
                  ],
                  "text": "In Network"
                },
                "unit": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                        "code": "individual",
                        "display": "Individual"
                      }
                    ],
                    "text": "Individual"
                },
                  "benefit": [
                    {
                      "type": {
                          "text": "Co-Insurance"
                      },
                      "allowedString": "0.0%"
                    },
                    {
                      "type": {
                          "text": "Co-Insurance"
                      },
                      "allowedString": "0.0%"
                    },
                    {
                      "type": {
                          "text": "Co-Insurance"
                      },
                      "allowedString": "0.0%"
                    }
                  ]
              },
              {
                "benefit": [
                  {
                    "type": {
                        "text": "Benefit Description (Incomplete information)"
                    }
                  }
                ]
              },
              {
                "benefit": [
                  {
                    "type": {
                        "text": "Active Coverage"
                    }
                  }
                ]
              },
              {
                "network": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                        "code": "in",
                        "display": "In Network"
                      }
                    ],
                    "text": "In Network"
                },
                "benefit": [
                  {
                    "type": {
                        "text": "Active Coverage"
                    }
                  },
                  {
                    "type": {
                        "text": "Primary Care Provider (Incomplete information)"
                    }
                  },
                  {
                    "type": {
                        "text": "Benefit Description (Incomplete information)"
                    }
                  },
                  {
                    "type": {
                        "text": "Benefit Disclaimer (Incomplete information)"
                    }
                  }
                ]
              },
              {
                "name": "Dental Care",
                "network": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                        "code": "in",
                        "display": "In Network"
                      }
                    ],
                    "text": "In Network"
                },
                "unit": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                        "code": "individual",
                        "display": "Individual"
                      }
                    ],
                    "text": "Individual"
                },
                "benefit": [
                  {
                    "type": {
                        "text": "Active Coverage"
                    }
                  }
                ]
              },
              {
                "name": "Health Benefit Plan Coverage",
                "network": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                        "code": "in",
                        "display": "In Network"
                      }
                    ],
                    "text": "In Network"
                },
                "unit": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                        "code": "individual",
                        "display": "Individual"
                      }
                    ],
                    "text": "Individual"
                },
                "benefit": [
                  {
                    "type": {
                        "text": "Deductible (Incomplete information)"
                    }
                  },
                  {
                    "type": {
                        "text": "Deductible"
                    },
                    "allowedMoney": {
                        "value": 6900
                    },
                    "usedMoney": {
                        "value": 0.0
                    }
                  },
                  {
                    "type": {
                        "text": "Active Coverage"
                    }
                  },
                  {
                    "type": {
                        "text": "Out of Pocket (Stop Loss)"
                    },
                    "allowedMoney": {
                        "value": 6900
                    },
                    "usedMoney": {
                        "value": 0.0
                    }
                  },
                  {
                    "type": {
                        "text": "Out of Pocket (Stop Loss)"
                    },
                    "allowedMoney": {
                        "value": 6900
                    },
                    "usedMoney": {
                        "value": 0.0
                    }
                  }
                ]
              },
              {
                "name": "Health Benefit Plan Coverage",
                "network": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                        "code": "in",
                        "display": "In Network"
                      }
                    ],
                    "text": "In Network"
                },
                "benefit": [
                  {
                    "type": {
                        "text": "Benefit Description (Incomplete information)"
                    }
                  }
                ]
              },
              {
                "name": "Physician Visit - Well",
                "network": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                        "code": "in",
                        "display": "In Network"
                      }
                    ],
                    "text": "In Network"
                },
                "benefit": [
                  {
                    "type": {
                        "text": "Non-Covered (Incomplete information)"
                    }
                  }
                ]
              },
              {
                "name": "Professional (Physician) Visit - Office",
                "network": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                        "code": "in",
                        "display": "In Network"
                      }
                    ],
                    "text": "In Network"
                },
                "unit": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-unit",
                        "code": "individual",
                        "display": "Individual"
                      }
                    ],
                    "text": "Individual"
                },
                "benefit": [
                  {
                    "type": {
                        "text": "Co-Insurance"
                    },
                    "allowedString": "0.0%"
                  }
                ]
              },
              {
                "name": "Professional (Physician) Visit - Office",
                "network": {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/benefit-network",
                        "code": "in",
                        "display": "In Network"
                      }
                    ],
                    "text": "In Network"
                },
                "benefit": [
                  {
                    "type": {
                        "text": "Non-Covered (Incomplete information)"
                    }
                  },
                  {
                    "type": {
                        "text": "Active Coverage"
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    }
  ]
}
```
    {% endtab %}
    {% tab coverageeligibilityresponse-search-response 400 %}
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
    {% tab coverageeligibilityresponse-search-response 401 %}
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
    {% tab coverageeligibilityresponse-search-response 403 %}
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
