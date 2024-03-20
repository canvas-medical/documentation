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
          - name: id
            type: string
            description: >-
              The identifier of the coverage eligibility response
          - name: status
            type: string
            description: >-
              Status of the resource<br><br>One of: **active**, **draft**, **entered-in-error**
          - name: purpose
            type: array[string]
            description: Reason for the request, will always be **["benefits"]**
          - name: patient
            type: json
            description: Patient resource the eligibility response is for
          - name: created
            type: datetime
            description: Response creation date
          - name: request
            type: json
            description: CoverageEligibilityRequest reference the elibibility response is for
          - name: outcome
            type: string
            description: Outcome of the request processing, will always be **"complete"**
          - name: insurer
            type: json
            description: >-
              Payor Id for the Coverage issuer
          - name: insurance
            type: array[json]
            description: >-
              Includes the **Coverage** reference, extension for plan name and an array of items containing benefits and authorization details<br><br>
              The amount of information surfaced here depends on the what the payor supports. Our clearinghouse (Claim.md) performs these eligibility checks, but not all coverages will support real-time eligibility checks. For more information on coverages within Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4408206355603-Patient-Coverages-2-0).
            attributes:
                - name: coverage 
                  description: Coverage reference.
                  type: json
                - name: item
                  description: Array of items containing benefits and authorization details.
                  type: array[json]
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
                        description: The valueString field is used for the plan name extension.
        search_parameters:
          - name: _id
            type: string
            description: The Canvas resource identifier of the CoverageEligibilityResponse
          - name: patient
            type: string
            description: The reference to the patient
          - name: request
            type: string
            description: The EligibilityRequest reference
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
