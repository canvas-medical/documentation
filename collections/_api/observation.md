---
title: Observation
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Observation
        article: "a"
        description: >-
          Measurements and simple assertions made about a patient, device or other subject.
        attributes:
          - name: id
            description: >-
              The identifier of the observation
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: status
            type: string
            required: true
          - name: category
            type: json
            description: >-
              Classification of type of observation
          - name: coding
            type: array
            attributes:
              - name: system
                type: string
                required: true
              - name: code
                type: string
                required: true
              - name: display
                type: string
                required: true
          - name: code
            type: string
            description: >-
              Type of observation (code / type)
          - name: subject
            type: string
            description: >-
              Who and/or what this is about
          - name: effectiveDateTime
            type: date
            description: >-
              Clinically relevant time/time-period for observation
          - name: issued
            type: date
            description: >-
              Date/Time this was made available
          - name: hasMember
            type: string
            description: >-
              Related resource that belongs to the Observation group
          - name: derivedFrom
            type: string
            description: >-
              Related measurements the Observation is made from
          - name: component
            type: string
            description: >-
              Component results
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
          - name: code
            type: string
          - name: category
            type: string
          - name: derived_from
            type: string
          - name: date
            type: array
        endpoints: [read, search, create]
        read:
          responses: [200, 404]
          example_request: observation-read-request
          example_response: observation-read-response
        search:
          responses: [200, 400]
          example_request: observation-search-request
          example_response: observation-search-response
        create:
          responses: [201, 400]
          example_request: observation-create-request
          example_response: observation-create-response

---
<div id="observation-read-request">
{% tabs observation-read-request %}
{% tab observation-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Observation/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab observation-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Observation/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="observation-read-response">
{% tabs observation-read-response %}
{% tab observation-read-response 200 %}
```json
{
    "resourceType": "Observation",
    "id": "43b74793-5de6-435a-871d-8ae2232f3aa0",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital Signs"
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "85353-1"
            }
        ]
    },
    "subject": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "effectiveDateTime": "2022-06-28T20:18:54.141759+00:00",
    "issued": "2022-06-28T20:43:10.465819+00:00",
    "dataAbsentReason": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                "code": "not-performed",
                "display": "Not Performed"
            }
        ]
    },
    "hasMember": [
        {
            "reference": "Observation/40cec197-041f-4db5-bd12-addbfb68c3b3",
            "type": "Observation"
        },
        {
            "reference": "Observation/5fa47fbe-eeb3-43c8-a287-11b18cad40b7",
            "type": "Observation"
        },
        {
            "reference": "Observation/4533ad2e-7ea4-4ae9-8018-301e1b99dcbb",
            "type": "Observation"
        },
        {
            "reference": "Observation/8f2c43eb-feeb-49c8-b509-b67fb1ecca51",
            "type": "Observation"
        },
        {
            "reference": "Observation/6a908edf-f75c-4a40-87cb-347d8a753bae",
            "type": "Observation"
        },
        {
            "reference": "Observation/2966fcba-be4e-4400-bd4a-aa7051ee38c6",
            "type": "Observation"
        },
        {
            "reference": "Observation/89edc763-4129-4d6c-94c7-6a3bcf1c776f",
            "type": "Observation"
        },
        {
            "reference": "Observation/f578d894-cfe2-49c2-88d2-48f5109ceed9",
            "type": "Observation"
        },
        {
            "reference": "Observation/2e368a90-8038-49c4-a26e-ebebdb736269",
            "type": "Observation"
        },
        {
            "reference": "Observation/b93d554a-b54b-4375-b531-e4f6337dc42d",
            "type": "Observation"
        }
    ]
}
```
{% endtab %}
{% tab observation-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Resource not found"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="observation-search-request">
{% tabs observation-search-request %}
{% tab observation-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Observation"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab observation-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Observation \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="observation-search-response">
{% tabs observation-search-response %}
{% tab observation-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link": [
        {
            "relation": "self",
            "url": "/Observation?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Observation?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
        }
        ,
        {
            "relation": "last",
            "url": "/Observation?patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=850"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Observation",
                "id": "43b74793-5de6-435a-871d-8ae2232f3aa0",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "85353-1"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "effectiveDateTime": "2022-06-28T20:18:54.141759+00:00",
                "issued": "2022-06-28T20:43:10.465819+00:00",
                "dataAbsentReason": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                            "code": "not-performed",
                            "display": "Not Performed"
                        }
                    ]
                },
                "hasMember": [
                    {
                        "reference": "Observation/40cec197-041f-4db5-bd12-addbfb68c3b3",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/5fa47fbe-eeb3-43c8-a287-11b18cad40b7",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/4533ad2e-7ea4-4ae9-8018-301e1b99dcbb",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/8f2c43eb-feeb-49c8-b509-b67fb1ecca51",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/6a908edf-f75c-4a40-87cb-347d8a753bae",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/2966fcba-be4e-4400-bd4a-aa7051ee38c6",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/89edc763-4129-4d6c-94c7-6a3bcf1c776f",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/f578d894-cfe2-49c2-88d2-48f5109ceed9",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/2e368a90-8038-49c4-a26e-ebebdb736269",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/b93d554a-b54b-4375-b531-e4f6337dc42d",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "40cec197-041f-4db5-bd12-addbfb68c3b3",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "80339-5",
                            "display": "Note"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
                    "type": "Patient"
                },
                "effectiveDateTime": "2022-06-28T20:18:54.141759+00:00",
                "issued": "2022-06-28T20:43:11.083304+00:00",
                "dataAbsentReason": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                            "code": "not-performed",
                            "display": "Not Performed"
                        }
                    ]
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/43b74793-5de6-435a-871d-8ae2232f3aa0",
                        "type": "Observation"
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab observation-search-response 400 %}
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

<div id="observation-create-request">
{% tabs observation-create-request %}
{% tab observation-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Observation"

payload = {
    "resourceType": "Observation",
    "category": [{ "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital Signs"
                }
            ] }],
    "code": { "coding": [
            {
                "system": "http://loinc.org",
                "code": "29463-7",
                "display": "Weight"
            }
        ] },
    "subject": { "reference": "Patient/ee8672f3497e4a83937b9e71d0a704a5" },
    "effectiveDateTime": "2022-07-29T08:50:24.883809+00:00",
    "valueQuantity": { "value": "50" },
    "derivedFrom": [{ "reference": "Observation/6173fbe8-110e-4a4a-9647-e949f7b1c35e" }],
    "hasMember": [{ "reference": "Observation/2dd1bf81-4cd0-458d-9342-b03decf5188b" }]
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
{% tab observation-create-request curl %}
```sh
curl --request POST \
     --url https://fumage-example.canvasmedical.com/Observation \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Observation",
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "vital-signs",
          "display": "Vital Signs"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "29463-7",
        "display": "Weight"
      }
    ]
  },
  "subject": {
    "reference": "Patient/ee8672f3497e4a83937b9e71d0a704a5"
  },
  "effectiveDateTime": "2022-07-29T08:50:24.883809+00:00",
  "valueQuantity": {
    "value": "50"
  },
  "derivedFrom": [
    {
      "reference": "Observation/6173fbe8-110e-4a4a-9647-e949f7b1c35e"
    }
  ],
  "hasMember": [
    {
      "reference": "Observation/2dd1bf81-4cd0-458d-9342-b03decf5188b"
    }
  ]
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="observation-create-response">
{% tabs observation-create-response %}
{% tab observation-create-response 201 %}
```json
null
```
{% endtab %}
{% tab observation-create-response 400 %}
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

