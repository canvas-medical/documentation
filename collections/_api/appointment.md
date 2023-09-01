---
title: Appointment
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Appointment
        article: "a"
        description: >-
         A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s) for a specific date/time. This may result in one or more Encounter(s).
        attributes:
          - name: id
            description: >-
              The identifier of the appointment
            type: string
            required: true
          - name: resourceType
            description: >-
              The type of resource
            type: string
            required: true
          - name: contained
            description: >-
              Additional resources that are contained in the appointment
            type: array
            attributes:
              - name: resourceType
                type: string
              - name: id
                type: string
              - name: status
                type: string
              - name: connectionType
                type: string
              - name: payloadType
                type: string
              - name: address
                type: string
          - name: status
            description: >-
              The status of the appointment
            type: string
          - name: appointmentType
            type: string
            attributes:
              - name: coding
                description: >-
                  The type of appointment
                type: array
                attributes:
                  - name: system
                    description: >-
                      The system of the appointment
                    type: string
                  - name: code
                    description: >-
                      The code of the appointment
                    type: string
                  - name: display
                    description: >-
                      The display of the appointment
                    type: string
          - name: reasonCode
            description: >-
              The reason for the appointment
            type: string
          - name: description
            description: >-
              The description of the appointment
            type: string
          - name: supportingInformation
            type: array
            attributes:
              - name: reference
                type: string
              - name: type
                type: string
          - name: start
            type: datetime
          - name: end
            type: datetime
          - name: participant
            type: array
            attributes:
              - name: actor
                type: string
              - name: status
                type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: appointmentType
            type: string
          - name: location
            type: string
          - name: patient
            type: string
          - name: practitioner
            type: string
          - name: date
            type: string
          - name: status
            type: string
        endpoints: [read, search, create, update]
        read:
          responses: [200, 404]
          example_request: appointment-read-request
          example_response: appointment-read-response
        search:
          responses: [200, 400]
          example_request: appointment-search-request
          example_response: appointment-search-response
        create:
          responses: [201, 400]
          example_request: appointment-create-request
          example_response: appointment-create-response
        update:
          responses: [200, 400]
          example_request: appointment-update-request
          example_response: appointment-update-response
---
<div id="appointment-read-request">
{% tabs appointment-read-request %}
{% tab appointment-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Appointment/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab appointment-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Appointment/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="appointment-read-response">
{% tabs appointment-read-response %}
{% tab appointment-read-response 200 %}
```json
{
    "resourceType": "Appointment",
    "id": "4be5c594-cfbd-4b7c-a047-ee3b06881745",
    "status": "checked-in",
    "appointmentType": {
        "coding": [
            {
                "system": "INTERNAL",
                "code": "INIV",
                "display": "Initial Visit"
            }
        ]
    },
    "reasonCode": [
        {
            "coding": [
                {
                    "system": "Internal",
                    "code": "INIV30",
                    "display": "Initial Visit 30",
                    "userSelected": false
                }
            ]
        }
    ],
    "supportingInformation": [
        {
            "reference": "Location/1",
            "type": "Location"
        },
        {
            "reference": "Encounter/63e2f110-71e2-4b7e-befd-4f9f3317b520",
            "type": "Encounter"
        }
    ],
    "start": "2023-06-06T18:00:00+00:00",
    "end": "2023-06-06T18:30:00+00:00",
    "participant": [
        {
            "actor": {
                "reference": "Practitioner/3a182f42885645e0bc3d608e7c02aad8",
                "type": "Practitioner"
            },
            "status": "accepted"
        },
        {
            "actor": {
                "reference": "Patient/a29eaebb284143ba97c76b01fdb46964",
                "type": "Patient"
            },
            "status": "accepted"
        }
    ]
}
```
{% endtab %}
{% tab appointment-read-response 404 %}
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

<div id="appointment-search-request">
{% tabs appointment-search-request %}
{% tab appointment-search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Appointment?patient=Patient%2F9420c5f6c44e47ec82d7e48f78d5723a&practitioner=Practitioner%2Ffc87cbb2525f4c5eb50294f620c7a15e"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab appointment-search-request curl %}
```sh
curl --request GET \
     --url 'https://fumage-example.canvasmedical.com/Appointment?patient=Patient%2F9420c5f6c44e47ec82d7e48f78d5723a&practitioner=Practitioner%2Ffc87cbb2525f4c5eb50294f620c7a15e' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="appointment-search-response">
{% tabs appointment-search-response %}
{% tab appointment-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 2,
    "link": [
        {
            "relation": "self",
            "url": "/Appointment?date=ge2022-02-24&practitioner=Practitioner%2F3a182f42885645e0bc3d608e7c02aad8&patient=Patient%2Fa29eaebb284143ba97c76b01fdb46964&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Appointment?date=ge2022-02-24&practitioner=Practitioner%2F3a182f42885645e0bc3d608e7c02aad8&patient=Patient%2Fa29eaebb284143ba97c76b01fdb46964&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Appointment?date=ge2022-02-24&practitioner=Practitioner%2F3a182f42885645e0bc3d608e7c02aad8&patient=Patient%2Fa29eaebb284143ba97c76b01fdb46964&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Appointment",
                "id": "4be5c594-cfbd-4b7c-a047-ee3b06881745",
                "status": "checked-in",
                "appointmentType": {
                    "coding": [
                        {
                            "system": "INTERNAL",
                            "code": "INIV",
                            "display": "Initial Visit"
                        }
                    ]
                },
                "reasonCode": [
                    {
                        "coding": [
                            {
                                "system": "Internal",
                                "code": "INIV30",
                                "display": "Initial Visit 30",
                                "userSelected": false
                            }
                        ]
                    }
                ],
                "supportingInformation": [
                    {
                        "reference": "Location/1",
                        "type": "Location"
                    },
                    {
                        "reference": "Encounter/63e2f110-71e2-4b7e-befd-4f9f3317b520",
                        "type": "Encounter"
                    }
                ],
                "start": "2023-06-06T18:00:00+00:00",
                "end": "2023-06-06T18:30:00+00:00",
                "participant": [
                    {
                        "actor": {
                            "reference": "Practitioner/3a182f42885645e0bc3d608e7c02aad8",
                            "type": "Practitioner"
                        },
                        "status": "accepted"
                    },
                    {
                        "actor": {
                            "reference": "Patient/a29eaebb284143ba97c76b01fdb46964",
                            "type": "Patient"
                        },
                        "status": "accepted"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Appointment",
                "id": "f98df7f2-10d4-4738-aaad-bf1e98ee85d3",
                "status": "checked-in",
                "appointmentType": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "448337001",
                            "display": "Telemedicine"
                        }
                    ]
                },
                "reasonCode": [
                    {
                        "coding": [
                            {
                                "system": "Internal",
                                "code": "INIV30",
                                "display": "Initial Visit 30",
                                "userSelected": false
                            }
                        ]
                    }
                ],
                "supportingInformation": [
                    {
                        "reference": "Location/1",
                        "type": "Location"
                    },
                    {
                        "reference": "Encounter/2fb638a3-fae8-47b0-afdb-2d8246da20ed",
                        "type": "Encounter"
                    }
                ],
                "start": "2023-08-22T19:00:00+00:00",
                "end": "2023-08-22T19:30:00+00:00",
                "participant": [
                    {
                        "actor": {
                            "reference": "Practitioner/3a182f42885645e0bc3d608e7c02aad8",
                            "type": "Practitioner"
                        },
                        "status": "accepted"
                    },
                    {
                        "actor": {
                            "reference": "Patient/a29eaebb284143ba97c76b01fdb46964",
                            "type": "Patient"
                        },
                        "status": "accepted"
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab appointment-search-response 400 %}
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

<div id="appointment-create-request">
{% tabs appointment-create-request %}
{% tab appointment-create-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Appointment"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
  {
  "resourceType": "Appointment",
  "reasonCode": "[{       \"coding\": [{         \"system\": \"INTERNAL\"         \"code\": \"9903\",         \"display\": \"Urgent Visit\"       }],         \"text\": \"Weekly check-in\"     }]",
  "description": "Weekly check-in.",
  "participant": [
    {
      "actor": {
        "reference": "Patient/5350cd20de8a470aa570a852859ac87e"
      },
      "status": "accepted"
    },
    {
      "actor": {
        "reference": "Practitioner/dbf184ad28a1408bbed184fc8fd2b029"
      },
      "status": "accepted"
    }
  ],
  "appointmentType": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "448337001",
        "display": "Telemedicine consultation with patient (procedure)"
      }
    ]
  },
  "start": "2022-03-20T13:30:00.000Z",
  "end": "2022-03-20T14:00:00.000Z",
  "supportingInformation": [
    {
      "reference": "Location/1"
    },
    {
      "reference": "#appointment-meeting-endpoint",
      "type": "Endpoint"
    }
  ],
  "contained": [
    {
      "resourceType": "Endpoint",
      "id": "appointment-meeting-endpoint",
      "status": "active",
      "connectionType": {
        "code": "https"
      },
      "payloadType": [
        {
          "coding": [
            {
              "code": "video-call"
            }
          ]
        }
      ],
      "address": "https://url-for-video-chat.example.com?meetingi=abc123"
    }
  ],
  "status": "proposed"
}
'
{
  "resourceType": "Patient",
  "name": [
    {
      "use": "official",
      "family": "Mark",
      "given": [
        "Isabella",
        "Robel"
      ],
      "prefix": "Mrs.",
      "suffix": "Jr."
    },
    {
      "use": "nickname",
      "given": [
        "Izzy"
      ]
    },
    {
      "use": "maiden",
      "family": "Smith"
    }
  ],
  "birthDate": "1980-11-13"
}
}
response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
{% tab appointment-create-request curl %}
```sh
curl --request POST \
     --url https://fumage-example.canvasmedical.com/Appointment \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Appointment",
  "reasonCode": "[{       \"coding\": [{         \"system\": \"INTERNAL\"         \"code\": \"9903\",         \"display\": \"Urgent Visit\"       }],         \"text\": \"Weekly check-in\"     }]",
  "description": "Weekly check-in.",
  "participant": [
    {
      "actor": {
        "reference": "Patient/5350cd20de8a470aa570a852859ac87e"
      },
      "status": "accepted"
    },
    {
      "actor": {
        "reference": "Practitioner/dbf184ad28a1408bbed184fc8fd2b029"
      },
      "status": "accepted"
    }
  ],
  "appointmentType": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "448337001",
        "display": "Telemedicine consultation with patient (procedure)"
      }
    ]
  },
  "start": "2022-03-20T13:30:00.000Z",
  "end": "2022-03-20T14:00:00.000Z",
  "supportingInformation": [
    {
      "reference": "Location/1"
    },
    {
      "reference": "#appointment-meeting-endpoint",
      "type": "Endpoint"
    }
  ],
  "contained": [
    {
      "resourceType": "Endpoint",
      "id": "appointment-meeting-endpoint",
      "status": "active",
      "connectionType": {
        "code": "https"
      },
      "payloadType": [
        {
          "coding": [
            {
              "code": "video-call"
            }
          ]
        }
      ],
      "address": "https://url-for-video-chat.example.com?meetingi=abc123"
    }
  ],
  "status": "proposed"
}
'
{
  "resourceType": "Patient",
  "name": [
    {
      "use": "official",
      "family": "Mark",
      "given": [
        "Isabella",
        "Robel"
      ],
      "prefix": "Mrs.",
      "suffix": "Jr."
    },
    {
      "use": "nickname",
      "given": [
        "Izzy"
      ]
    },
    {
      "use": "maiden",
      "family": "Smith"
    }
  ],
  "birthDate": "1980-11-13"
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="appointment-create-response">
{% tabs appointment-create-response %}
{% tab appointment-create-response 201 %}
```json
null
```
{% endtab %}
{% tab appointment-create-response 400 %}
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

<div id="appointment-update-request">
{% tabs appointment-update-request %}
{% tab appointment-update-request curl %}
```sh
curl --request PUT \
     --url https://fumage-example.canvasmedical.com/Appointment/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Appointment",
  "id": "94d34e0f-b5c2-4af1-b806-acec8866da18",
  "status": "cancelled",
  "appointmentType": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "448337001",
        "display": "Telemedicine consultation with patient (procedure)"
      }
    ]
  },
  "reasonCode": "[{       \"coding\": [{         \"system\": \"INTERNAL\"         \"code\": \"9903\",         \"display\": \"Urgent Visit\"       }],         \"text\": \"Weekly check-in\"     }]",
  "description": "Weekly check-in",
  "start": "2022-03-20T13:30:00.000Z",
  "end": "2022-03-20T14:00:00.000Z",
  "participant": [
    {
      "actor": {
        "reference": "Patient/5350cd20de8a470aa570a852859ac87e"
      },
      "status": "accepted"
    },
    {
      "actor": {
        "reference": "Practitioner/dbf184ad28a1408bbed184fc8fd2b029"
      },
      "status": "accepted"
    }
  ],
  "supportingInformation": [
    {
      "reference": "Location/1"
    },
    {
      "reference": "#appointment-meeting-endpoint",
      "type": "Endpoint"
    }
  ],
  "contained": [
    {
      "resourceType": "Endpoint",
      "id": "appointment-meeting-endpoint",
      "address": "https://url-for-video-chat.example.com?meetingi=abc123"
    }
  ]
}
'

```
{% endtab %}
{% endtabs %}
</div>

<div id="appointment-update-response">
{% tabs appointment-update-response %}
{% tab appointment-update-response 200 %}
```json
null
```
{% endtab %}
{% tab appointment-update-response 400 %}
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


