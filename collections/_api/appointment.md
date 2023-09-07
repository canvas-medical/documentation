---
title: Appointment
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Appointment
        article: "a"
        description: >-
           [FHIR](https://fhir-ru.github.io/appointment.html): A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s) for a specific date/time. This may result in one or more [Encounters](/api/encounter). <br><br> The appointment resource maps to both [patient appointments](https://canvas-medical.zendesk.com/hc/en-us/articles/360056430014-Appointments) as well as [other events](https://canvas-medical.zendesk.com/hc/en-us/articles/15704289792659-Scheduling-Other-Events-) in Canvas. Instructions for configuring appointment and note types can be found [here](/documentation/appointment-and-note-types).  
        attributes:
          - name: id
            type: string
            required: true
            description: >-
              The identifier of the appointment
          - name: status
            type: string
            description: >-
              The status of the appointment. <br><br> **Canvas to FHIR Mapping**<br>unconfirmed > proposed<br>attempted > pending<br>confirmed > booked<br>arrived > arrived<br>roomed > check-in<br>exited > fulfilled<br>no-showed > noshow<br>cancelled > cancelled<br>deleted > entered-in-error
            create_description:
                Currently, Canvas only supports creating an appointment with the status "proposed". Any other input will be ignored. If no status is added it defaults to "proposed". A status can be updated later using the [Appointment Update](/api/appointment/#update) endpoint.
            update_description: >-
              The update endpoint supports the following statuses: **proposed, pending, booked, arrived, fulfilled, cancelled, noshow, checked-in** <br><br> We currently do not support marking an appointment as entered-in-error or waitlist. See [Appointment Read](/api/appointment/#read) for a better understanding of how these FHIR statuses are mapping in Canvas. <br><br>Once an appointment's status is updated to "cancelled" it cannot be changed to a different status. If the status is removed, the update will default to what it was previously set to.
          - name: appointmentType
            type: string         
            description: >-
              Canvas supports configurable [apppointment and note types](/documentation/appointment-and-note-types/). 
            create_description: >-
              Canvas supports configurable [appointment and note types](/documentation/appointment-and-note-types/). There are a few things to note with this field: <br><br>**1.**If `appointmentType` attribute is omitted from the body completely, the note type that has `Is default appointment type` will be used (usually Office Visit if unchanged)<br><br>**2.**The `appointmentType` field must contain one coding, and it must be a SNOMED or INTERNAL coding.<br><br>**3.**If a code that does not exist is passed, you will see a 422 error status with error message `Appointment Create Error: Appointment Type does not exist with system: {system} and code: {code}` <br><br>**4.** If a code is passed that is not marked as `Is Scheduleable`, you will get a 422 error status with error message `Appointment Create Error: Appointment type must be scheduleable`.
            update_description: >-
              Canvas supports configurable [appointment and note types](/documentation/appointment-and-note-types/). There are a few things to note with this field: <br><br>**1.**If `appointmentType` attribute is omitted from the body completely, the note type that has `Is default appointment type` will be used (usually Office Visit if unchanged)<br><br>**2.**The `appointmentType` field must contain one coding, and it must be a SNOMED or INTERNAL coding.<br><br>**3.**If a code that does not exist is passed, you will see a 422 error status with error message `Appointment Create Error: Appointment Type does not exist with system: {system} and code: {code}` <br><br>**4.** If a code is passed that is not marked as `Is Scheduleable`, you will get a 422 error status with error message `Appointment Create Error: Appointment type must be scheduleable`.
            attributes:
              - name: coding
                type: array
                description: >-
                  The type of appointment
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
          - name: resourceType
            type: string
            required: true  
            description: >-
              The type of resource                
          - name: reasonCode
            type: string
            description: >-
              The reason for the appointment. Canvas supports two ways to specify the reason for vist (RFV): [structured](/documenation/reason-for-visit-codings) and unstructured. Both the `coding` and `text` attributes are used for Structured RFVs, whereas unstructured RFVs only leverage the `text` attribute. 
            create_description: 
              We only accept the first item in the reasonCode list. If you are taking advantage of our [structured reason for visit](/documenation/reason-for-visit-codings) feature,  you can provide a `coding` where we look up that `code` value in settings and display the structured RFV matching that code. If `Appointment.reasonCode[0].coding[0].code` is not a valid ReasonForVisitSettingCoding you will get the error "structured reason for visit with code {code} does not exist". <br><br> The `text` attribute maps to the free text Reason For Visit command.  If you are using the structured reason for visit feature, this text will display as the `comment` in the command. 
            update_description:
              In the Canvas UI, if the reasonCode / description is changed, it will update the reason for visit on that appointment. The old reason for visit will be marked as entered-in-error, and the text will no longer display. Below is an example of what an appointment's note will look like after changing the description multiple times. The originator and entered-in-error will be set to Canvas Bot, which can be seen if you click on the crossed off "Reason for Visit".<br><br>![api-update-rfv](/assets/images/api-update-rfv.png){:width="80%"} 
            attributes:
              - name: coding
                type: string
              - name: text
                type: string
          - name: Description [deprecated]
            type: string
            description: >-
              Note: This field is being deprecated in favor of `reasonCode`. The text in `reasonCode` and this description attribute will always match.
          - name: contained
            type: array
            description: >-
              Used to store links for telehealth appointments. Requires a reference to "#appointment-meeting-endpoint" in the SupportingInformation attribute.
            create_description:
             <b>Custom Meeting Links for Virtual Appointments:</b> You can specify a telehealth meeting link using a SupportingInformation `reference` of "#appointment-meeting-endpoint" with a `type` of "Endpoint".  You would need to specify the `address` url of the meeting link in a contained object along with the `resourceType` = `Endpoint` and the `id` = `appointment-meeting-endpoint`. All other fields are automatically populated by Canvas and are not required.
            update_description:
              <b>Custom Meeting Links for Virtual Appointments:</b> You can specify a telehealth meeting link using a SupportingInformation `reference` of "#appointment-meeting-endpoint" with a `type` of "Endpoint".  You would need to specify the `address` url of the meeting link in a contained object along with the `resourceType` = `Endpoint` and the `id` = `appointment-meeting-endpoint`. All other fields are automatically populated by Canvas and are not required.
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
          - name: supportingInformation
            type: array
            description: >-
              **References** are used to capture information about **rescheduled appointments** and the **location** of the appointment.<br><br>**Rescheduled Appointments**<br>If you see `Previously Rescheduled Appointment` in `supportingInformation`, it means that the appointment you are currently reading was created by rescheduling the appointment in that Reference. If you see `Rescheduled Replacement Appointment` in the `supportingInformation`, it means that the appointment you are currently reading is now outdated by a new appointment.
            create_description:
              You can use a Location reference within the `SupportingInformation` attribute to specify the Location of the appointment,. To get the location id, use the [Schedule Search](api/schedule/#search) endpoint. This will give you a `resource.id` like `Location.1-Staff.c2ff4546548e46ab8959af887b563eab`. The Location ID is the value displayed after the period. If your instance only has one practice location, the ID will always be 1.
            attributes:
              - name: reference
                type: string
              - name: type
                type: string
          - name: start
            type: datetime
            create_description:
              The `start` attribute determines the start timestamp of the appointment. It is written in [instant format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required.
          - name: end
            type: datetime
            create_description:
              The end attribute is used with the start timestamp to determine the duration in minutes of the appointment. It is written in [instant format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required. <br><br> ⚠ Currently, we do not provide any validation on this end date. If you have an end_date before the start_date, it will result in a negative duration being displayed on the UI.
          - name: participant
            descrition: >-
               Must include at least one entry for a practitioner. An optional 2nd entry may be used for the patient.<br><br>  The `actor.reference`:  `Practitioner/<practitioner_id>` maps to the rendering provider in Canvas.
            create_description:
              This list object requires one entry for a practitioner. An optional 2nd entry may be supplied for the patient.<br><br>   • The first entry has the `actor.reference` specify `Practitioner/<practitioner_id>` for the provider. This id can be found through a [Practitioner Search](api/practitioner/#search). If `<practitioner_id>` is left blank, the practitioner will be set to Canvas Bot by default. <br>   • The second entry has the `actor.reference` specify `Patient/<patient_id>` for the patient this appointment is for. This id can be found through a [Patient Search](api/patient/#search). <br><br>Per FHIR,  status is required, but it is not used by Canvas. Canvas recommends sending “active"
            type: array
            attributes:
              - name: actor
                type: string
              - name: status
                required: true
                type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: appointment-type
            type: string
          - name: location
            type: string
          - name: patient
            type: string
            description: A FHIR Patient reference
          - name: practitioner
            type: string
            description: A FHIR Practitioner reference
          - name: date
            type: string
            description: Search based on when the appointment is scheduled (UTC). Uses an operand and a date field in the format YYYY-MM-DD. eq, gt, ge, lt, and le are currently supported operands (eq is assumed if no operand is sent). Two date parameters are accepted to allow for date range searches.  "/Appointment?date=ge2021-09-16"
          - name: status
            type: string
          - name: _count
            type: string
            description: Triggers pagination. This number is used to determine how many results to return at a time.
          - name: _offset
            type: string
            description: The result to start after in the result set when _count is included for pagination. Will be ignored if _count is not included. A 0 offset is assumed if this parameter is not included but _count is included.
          - name: _offset
            type: string
            description: Triggers sorting of the results by a specific criteria. Accepted values are date, patient and practitioner. Use -date, -patient, -practitioner to sort in descending order 
 

        endpoints: [create, read, update, search]
        read:
          description: Read an Appointment
          responses: [200, 404]
          example_request: appointment-read-request
          example_response: appointment-read-response
        search:
          description: Search for an Appointment<br><br>**Pagination**<br>To paginate appointment search results, use the query param _count.<br><br>`GET /Appointment?_count=10` will return the first 10 appointments, along with relative links to see the subsequent pages. The pages are specified by a combination of `_count` and `_offset`.
          responses: [200, 400]
          example_request: appointment-search-request
          example_response: appointment-search-response
        create:
          description: Create an **Appointment**<br><br> **Prevent Double Booking** By default, Canvas does not prevent appointments from being created if there is already an existing appointment for that provider. However, we have a config setting to disable double booking. If double booking is not allowed and the Appointment Create or Appointment Update request is trying to book an appointment for a given Provider that already has a scheduled appointment at that time, you will see a 422 error status with the following error message returned `This appointment time is no longer available.`
          responses: [201, 400]
          example_request: appointment-create-request
          example_response: appointment-create-response
        update:
          description: Update an **Appointment** This is almost identical to the [Appointment Create]/(api/appointment/#create. The update will only affect fields that are passed in to the body, if any fields are omitted they will be ignored and kept as co are currently set in the Canvas database.
          responses: [200, 400]
          example_request: appointment-update-request
          example_response: appointment-update-response
---
<div id="appointment-read-request">
{% tabs appointment-read-request %}
{% tab appointment-read-request python %}
```python
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

{% tab appointment-create-request curl %}
```shell
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
```
{% endtab %}

{% tab appointment-create-request python %}
```python
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
```shell
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


