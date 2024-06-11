---
layout: apipage
title: DiagnosticReport Operations
---

## create-lab-report

Creates a lab report, lab tests, lab values, and a stored PDF in Canvas.

This endpoint is a [FHIR operation](https://hl7.org/fhir/R4/operations.html) and was developed as a convenience method in order to post all data associated with a lab report in a single request. In order to adhere to the FHIR standard, the request structure for creating lab reports is in the  [Parameters](https://hl7.org/fhir/R4/parameters.html) format. This means that an array of named parameter resources makes up the body of the request.

In the example below, the first object in the parameter array is a named parameter called `labReport`. This references a `DiagnosticReport` resource. The `subject` attribute passed here must contain a valid patient reference and the `presentedForm` attribute must contain a base64-encoded string of the report PDF. Only one `labReport` parameter is allowed per payload.

The subsequent parameters in the array must be named `labTestCollection`. These represent the lab tests performed and associated result values. Each `labTestCollection` has a `part` array with `labTest` and `labValue` parameters. Only one `labTest` parameter is allowed per `labTestCollection`. Multiple `labValue` parameters are allowed per `labTestCollection`. Both resources must be represented as `Observation` resources.

To mark a lab value as abnormal, an optional `interpretation` attribute can be added to a `labValue` `Observation` resource. <b>Only abnormal interpretations (`"code": "A"`)</b> are currently supported, and the payload must match the structure shown in the example below.

{% include alert.html type="warning" content="While lab tests can be posted and are visible in the Canvas UI, they are not currently available to be read through the FHIR API. Only lab values can be read through the Observation resource." %}


The bearer token included in requests send to this endpoint must have one of the following scopes:
- `system/DiagnosticReport.create-lab-report`
- `user/DiagnosticReport.create-lab-report`

{% tabs create-lab-report %}
{% tab create-lab-report curl %}
```shell
curl -X POST "https://fumage-example.canvasmedical.com/DiagnosticReport/\$create-lab-report" \
     -H "accept: application/json" \
     -H "Authorization: Bearer <token>" \
     -H "content-type: application/json" \
     -d '{
    "resourceType": "Parameters",
    "parameter":
    [
        {
            "name": "labReport",
            "resource":
            {
                "resourceType": "DiagnosticReport",
                "status": "final",
                "category":
                [
                    {
                        "coding":
                        [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                                "code": "LAB",
                                "display": "Laboratory"
                            }
                        ]
                    }
                ],
                "subject":
                {
                    "reference": "Patient/4cc6fd69f81042a0b6d123e2080a7c1a",
                    "type": "Patient"
                },
                "presentedForm":
                [
                    {
                        "data": "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ZWFtCmVuZG9iago0IDAgb2JqCjw8L1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUwCi9CYXNlRm9udCAvQUFBQUFBK0FyaWFsTVQKL0VuY29kaW5nIC9JZGVudGl0eS1ICi9EZXNjZW5kYW50Rm9udHMgWzEwIDAgUl0KL1RvVW5pY29kZSAxMSAwIFI+PgplbmRvYmoKeHJlZgowIDEyCjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAwMzk3IDAwMDAwIG4gCjAwMDAwMDAxMDggMDAwMDAgbiAKMDAwMDAxMDgxMSAwMDAwMCBuIAowMDAwMDAwMTQ1IDAwMDAwIG4gCjAwMDAwMDA2MDUgMDAwMDAgbiAKMDAwMDAwMDY2MCAwMDAwMCBuIAowMDAwMDAwNzA3IDAwMDAwIG4gCjAwMDAwMDk5MzQgMDAwMDAgbiAKMDAwMDAxMDE2OCAwMDAwMCBuIAowMDAwMDEwNDc4IDAwMDAwIG4gCnRyYWlsZXIKPDwvU2l6ZSAxMgovUm9vdCA3IDAgUgovSW5mbyAxIDAgUj4+CnN0YXJ0eHJlZgoxMDk1MAolJUVPRg==",
                        "contentType": "application/pdf"
                    }
                ],
                "effectiveDateTime": "2024-02-25T14:46:39.219042",
                "code":
                {
                    "coding":
                    []
                }
            }
        },
        {
            "name": "labTestCollection",
            "part":
            [
                {
                    "name": "labTest",
                    "resource":
                    {
                        "resourceType": "Observation",
                        "code":
                        {
                            "text": "Hepatic Function Panel (7)",
                            "coding":
                            [
                                {
                                    "system": "http://loinc.org",
                                    "code": "24325-3",
                                    "display": "Hepatic Function Panel (7)"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "status": "final"
                    }
                },
                {
                    "name": "labValue",
                    "resource":
                    {
                        "resourceType": "Observation",
                        "status": "final",
                        "code":
                        {
                            "coding":
                            [
                                {
                                    "system": "http://loinc.org",
                                    "code": "2885-2",
                                    "display": "Protein, Total"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity":
                        {
                            "value": "9.6",
                            "unit": "g/dL",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange":
                        [
                            {
                                "low":
                                {
                                    "value": "6.0"
                                },
                                "high":
                                {
                                    "value": "8.5"
                                },
                                "text": "6.0-8.5"
                            }
                        ],
                        "interpretation":
                        [
                            {
                                "text": "Abnormal",
                                "coding":
                                [
                                    {
                                        "code": "A",
                                        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                                        "display": "Abnormal"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource":
                    {
                        "resourceType": "Observation",
                        "status": "final",
                        "code":
                        {
                            "coding":
                            [
                                {
                                    "code": "1751-7",
                                    "system": "http://loinc.org",
                                    "display": "Albumin"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity":
                        {
                            "unit": "g/dL",
                            "value": "3.8",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange":
                        [
                            {
                                "low":
                                {
                                    "value": "3.6"
                                },
                                "high":
                                {
                                    "value": "4.6"
                                },
                                "text": "3.6-4.6"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource":
                    {
                        "resourceType": "Observation",
                        "status": "final",
                        "code":
                        {
                            "text": "Bilirubin, Total",
                            "coding":
                            [
                                {
                                    "code": "1975-2",
                                    "system": "http://loinc.org",
                                    "display": "Bilirubin, Total"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity":
                        {
                            "unit": "mg/dL",
                            "value": "0.3",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange":
                        [
                            {
                                "low":
                                {
                                    "value": "0.0"
                                },
                                "high":
                                {
                                    "value": "1.2"
                                },
                                "text": "0.0-1.2"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource":
                    {
                        "resourceType": "Observation",
                        "status": "final",
                        "code":
                        {
                            "text": "Alkaline Phosphatase",
                            "coding":
                            [
                                {
                                    "code": "6768-6",
                                    "system": "http://loinc.org",
                                    "display": "Alkaline Phosphatase"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity":
                        {
                            "unit": "IU/L",
                            "value": "83.6",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange":
                        [
                            {
                                "low":
                                {
                                    "value": "44.0"
                                },
                                "high":
                                {
                                    "value": "121.0"
                                },
                                "text": "44-121"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource":
                    {
                        "resourceType": "Observation",
                        "status": "final",
                        "code":
                        {
                            "text": "AST (SGOT)",
                            "coding":
                            [
                                {
                                    "code": "1920-8",
                                    "system": "http://loinc.org",
                                    "display": "AST (SGOT)"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity":
                        {
                            "unit": "IU/L",
                            "value": "19.4",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange":
                        [
                            {
                                "low":
                                {
                                    "value": "0.0"
                                },
                                "high":
                                {
                                    "value": "40.0"
                                },
                                "text": "0-40"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource":
                    {
                        "resourceType": "Observation",
                        "status": "final",
                        "code":
                        {
                            "text": "ALT (SGPT)",
                            "coding":
                            [
                                {
                                    "code": "1742-6",
                                    "system": "http://loinc.org",
                                    "display": "ALT (SGPT)"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity":
                        {
                            "unit": "IU/L",
                            "value": "13.5",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange":
                        [
                            {
                                "low":
                                {
                                    "value": "0.0"
                                },
                                "high":
                                {
                                    "value": "44.0"
                                },
                                "text": "0-44"
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
'
```

{% endtab %}
{% tab create-lab-report python %}

```python
import requests

url = "https://fumage-example.canvasmedical.com/DiagnosticReport/$create-lab-report"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Parameters",
    "parameter": [
        {
            "name": "labReport",
            "resource": {
                "resourceType": "DiagnosticReport",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                                "code": "LAB",
                                "display": "Laboratory"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/4cc6fd69f81042a0b6d123e2080a7c1a",
                    "type": "Patient"
                },
                "presentedForm": [
                    {
                        "data": "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ZWFtCmVuZG9iago0IDAgb2JqCjw8L1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUwCi9CYXNlRm9udCAvQUFBQUFBK0FyaWFsTVQKL0VuY29kaW5nIC9JZGVudGl0eS1ICi9EZXNjZW5kYW50Rm9udHMgWzEwIDAgUl0KL1RvVW5pY29kZSAxMSAwIFI+PgplbmRvYmoKeHJlZgowIDEyCjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAwMzk3IDAwMDAwIG4gCjAwMDAwMDAxMDggMDAwMDAgbiAKMDAwMDAxMDgxMSAwMDAwMCBuIAowMDAwMDAwMTQ1IDAwMDAwIG4gCjAwMDAwMDA2MDUgMDAwMDAgbiAKMDAwMDAwMDY2MCAwMDAwMCBuIAowMDAwMDAwNzA3IDAwMDAwIG4gCjAwMDAwMDk5MzQgMDAwMDAgbiAKMDAwMDAxMDE2OCAwMDAwMCBuIAowMDAwMDEwNDc4IDAwMDAwIG4gCnRyYWlsZXIKPDwvU2l6ZSAxMgovUm9vdCA3IDAgUgovSW5mbyAxIDAgUj4+CnN0YXJ0eHJlZgoxMDk1MAolJUVPRg==",
                        "contentType": "application/pdf"
                    }
                ],
                "effectiveDateTime": "2024-02-25T14:46:39.219042",
                "code": {
                    "coding": []
                }
            }
        },
        {
            "name": "labTestCollection",
            "part": [
                {
                    "name": "labTest",
                    "resource": {
                        "resourceType": "Observation",
                        "code": {
                            "text": "Hepatic Function Panel (7)",
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "24325-3",
                                    "display": "Hepatic Function Panel (7)"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "status": "final"
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "2885-2",
                                    "display": "Protein, Total"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "value": "9.6",
                            "unit": "g/dL",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "6.0"
                                },
                                "high": {
                                    "value": "8.5"
                                },
                                "text": "6.0-8.5"
                            }
                        ],
                        "interpretation": [
                            {
                                "text": "Abnormal",
                                "coding": [
                                    {
                                        "code": "A",
                                        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                                        "display": "Abnormal"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "coding": [
                                {
                                    "code": "1751-7",
                                    "system": "http://loinc.org",
                                    "display": "Albumin"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "g/dL",
                            "value": "3.8",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "3.6"
                                },
                                "high": {
                                    "value": "4.6"
                                },
                                "text": "3.6-4.6"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "text": "Bilirubin, Total",
                            "coding": [
                                {
                                    "code": "1975-2",
                                    "system": "http://loinc.org",
                                    "display": "Bilirubin, Total"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "mg/dL",
                            "value": "0.3",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "0.0"
                                },
                                "high": {
                                    "value": "1.2"
                                },
                                "text": "0.0-1.2"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "text": "Alkaline Phosphatase",
                            "coding": [
                                {
                                    "code": "6768-6",
                                    "system": "http://loinc.org",
                                    "display": "Alkaline Phosphatase"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "IU/L",
                            "value": "83.6",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "44.0"
                                },
                                "high": {
                                    "value": "121.0"
                                },
                                "text": "44-121"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "text": "AST (SGOT)",
                            "coding": [
                                {
                                    "code": "1920-8",
                                    "system": "http://loinc.org",
                                    "display": "AST (SGOT)"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "IU/L",
                            "value": "19.4",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "0.0"
                                },
                                "high": {
                                    "value": "40.0"
                                },
                                "text": "0-40"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "text": "ALT (SGPT)",
                            "coding": [
                                {
                                    "code": "1742-6",
                                    "system": "http://loinc.org",
                                    "display": "ALT (SGPT)"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "IU/L",
                            "value": "13.5",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "0.0"
                                },
                                "high": {
                                    "value": "44.0"
                                },
                                "text": "0-44"
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
{% endtabs %}

<br>

### Additional JSON Examples

{% tabs create-lab-report-json-examples %}
{% tab create-lab-report-json-examples More than one lab test %}
```json
{
    "resourceType": "Parameters",
    "parameter": [
        {
            "name": "labReport",
            "resource": {
                "resourceType": "DiagnosticReport",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                                "code": "LAB",
                                "display": "Laboratory"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/4cc6fd69f81042a0b6d123e2080a7c1a",
                    "type": "Patient"
                },
                "presentedForm": [
                    {
                        "data": "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ZWFtCmVuZG9iago0IDAgb2JqCjw8L1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUwCi9CYXNlRm9udCAvQUFBQUFBK0FyaWFsTVQKL0VuY29kaW5nIC9JZGVudGl0eS1ICi9EZXNjZW5kYW50Rm9udHMgWzEwIDAgUl0KL1RvVW5pY29kZSAxMSAwIFI+PgplbmRvYmoKeHJlZgowIDEyCjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAwMzk3IDAwMDAwIG4gCjAwMDAwMDAxMDggMDAwMDAgbiAKMDAwMDAxMDgxMSAwMDAwMCBuIAowMDAwMDAwMTQ1IDAwMDAwIG4gCjAwMDAwMDA2MDUgMDAwMDAgbiAKMDAwMDAwMDY2MCAwMDAwMCBuIAowMDAwMDAwNzA3IDAwMDAwIG4gCjAwMDAwMDk5MzQgMDAwMDAgbiAKMDAwMDAxMDE2OCAwMDAwMCBuIAowMDAwMDEwNDc4IDAwMDAwIG4gCnRyYWlsZXIKPDwvU2l6ZSAxMgovUm9vdCA3IDAgUgovSW5mbyAxIDAgUj4+CnN0YXJ0eHJlZgoxMDk1MAolJUVPRg==",
                        "contentType": "application/pdf"
                    }
                ],
                "effectiveDateTime": "2024-02-25T15:10:56.296677",
                "code": {
                    "coding": []
                }
            }
        },
        {
            "name": "labTestCollection",
            "part": [
                {
                    "name": "labTest",
                    "resource": {
                        "resourceType": "Observation",
                        "code": {
                            "text": "Hepatic Function Panel (7)",
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "24325-3",
                                    "display": "Hepatic Function Panel (7)"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "status": "final"
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "2885-2",
                                    "display": "Protein, Total"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "value": "9.6",
                            "unit": "g/dL",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "6.0"
                                },
                                "high": {
                                    "value": "8.5"
                                },
                                "text": "6.0-8.5"
                            }
                        ],
                        "interpretation": [
                            {
                                "text": "Abnormal",
                                "coding": [
                                    {
                                        "code": "A",
                                        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                                        "display": "Abnormal"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "coding": [
                                {
                                    "code": "1751-7",
                                    "system": "http://loinc.org",
                                    "display": "Albumin"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "g/dL",
                            "value": "3.8",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "3.6"
                                },
                                "high": {
                                    "value": "4.6"
                                },
                                "text": "3.6-4.6"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "text": "Bilirubin, Total",
                            "coding": [
                                {
                                    "code": "1975-2",
                                    "system": "http://loinc.org",
                                    "display": "Bilirubin, Total"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "mg/dL",
                            "value": "0.3",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "0.0"
                                },
                                "high": {
                                    "value": "1.2"
                                },
                                "text": "0.0-1.2"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "text": "Alkaline Phosphatase",
                            "coding": [
                                {
                                    "code": "6768-6",
                                    "system": "http://loinc.org",
                                    "display": "Alkaline Phosphatase"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "IU/L",
                            "value": "83.6",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "44.0"
                                },
                                "high": {
                                    "value": "121.0"
                                },
                                "text": "44-121"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "text": "AST (SGOT)",
                            "coding": [
                                {
                                    "code": "1920-8",
                                    "system": "http://loinc.org",
                                    "display": "AST (SGOT)"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "IU/L",
                            "value": "19.4",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "0.0"
                                },
                                "high": {
                                    "value": "40.0"
                                },
                                "text": "0-40"
                            }
                        ]
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "text": "ALT (SGPT)",
                            "coding": [
                                {
                                    "code": "1742-6",
                                    "system": "http://loinc.org",
                                    "display": "ALT (SGPT)"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-01-11T17:37:30.756832+00:00",
                        "valueQuantity": {
                            "unit": "IU/L",
                            "value": "13.5",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "0.0"
                                },
                                "high": {
                                    "value": "44.0"
                                },
                                "text": "0-44"
                            }
                        ]
                    }
                }
            ]
        },
        {
            "name": "labTestCollection",
            "part": [
                {
                    "name": "labTest",
                    "resource": {
                        "resourceType": "Observation",
                        "code": {
                            "text": "Vitamin D, 25-Hydroxy",
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "62292-8",
                                    "display": "Vitamin D, 25-Hydroxy"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-02-25T15:10:56.296677",
                        "status": "final"
                    }
                },
                {
                    "name": "labValue",
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "62292-8",
                                    "display": "Vitamin D, 25-Hydroxy"
                                }
                            ]
                        },
                        "effectiveDateTime": "2024-02-25T15:10:56.296677",
                        "valueQuantity": {
                            "unit": "ng/mL",
                            "value": "41.0",
                            "system": "http://unitsofmeasure.org"
                        },
                        "referenceRange": [
                            {
                                "low": {
                                    "value": "30.0"
                                },
                                "high": {
                                    "value": "100.0"
                                },
                                "text": "30.0-100.0"
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

{% endtab %}
{% tab create-lab-report-json-examples Only report data (no tests or values) %}

```json
{
    "resourceType": "Parameters",
    "parameter": [
        {
            "name": "labReport",
            "resource": {
                "resourceType": "DiagnosticReport",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                                "code": "LAB",
                                "display": "Laboratory"
                            }
                        ]
                    }
                ],
                "subject": {
                    "reference": "Patient/4cc6fd69f81042a0b6d123e2080a7c1a",
                    "type": "Patient"
                },
                "presentedForm": [
                    {
                        "data": "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ZWFtCmVuZG9iago0IDAgb2JqCjw8L1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUwCi9CYXNlRm9udCAvQUFBQUFBK0FyaWFsTVQKL0VuY29kaW5nIC9JZGVudGl0eS1ICi9EZXNjZW5kYW50Rm9udHMgWzEwIDAgUl0KL1RvVW5pY29kZSAxMSAwIFI+PgplbmRvYmoKeHJlZgowIDEyCjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAwMzk3IDAwMDAwIG4gCjAwMDAwMDAxMDggMDAwMDAgbiAKMDAwMDAxMDgxMSAwMDAwMCBuIAowMDAwMDAwMTQ1IDAwMDAwIG4gCjAwMDAwMDA2MDUgMDAwMDAgbiAKMDAwMDAwMDY2MCAwMDAwMCBuIAowMDAwMDAwNzA3IDAwMDAwIG4gCjAwMDAwMDk5MzQgMDAwMDAgbiAKMDAwMDAxMDE2OCAwMDAwMCBuIAowMDAwMDEwNDc4IDAwMDAwIG4gCnRyYWlsZXIKPDwvU2l6ZSAxMgovUm9vdCA3IDAgUgovSW5mbyAxIDAgUj4+CnN0YXJ0eHJlZgoxMDk1MAolJUVPRg==",
                        "contentType": "application/pdf"
                    }
                ],
                "effectiveDateTime": "2024-02-25T15:12:12.837429",
                "code": {
                    "coding": []
                }
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}

