---
title: Appointment
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Appointment
        article: "a"
        description: >-
          A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s) for a specific date/time. This may result in one or more Encounter(s).<br><br>
          [https://hl7.org/fhir/R4/appointment.html](https://hl7.org/fhir/R4/appointment.html<br><br>)<br><br>
          This may result in one or more [Encounters](/api/encounter).<br><br>
          The appointment resource maps to both [patient appointments](https://canvas-medical.zendesk.com/hc/en-us/articles/360056430014-Appointments) as well as [other events](https://canvas-medical.zendesk.com/hc/en-us/articles/15704289792659-Scheduling-Other-Events-) in Canvas. Instructions for configuring appointment and note types can be found [here](/documentation/appointment-and-note-types).
        attributes:
          - name: id
            type: string
            required: true
            description: >-
              The identifier of the appointment
          - name: contained
            type: array[json]
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
                type: json
              - name: payloadType
                type: array[json]
              - name: address
                type: string
          - name: identifier
            type: array[json]
            description: >-
              External Ids for this item
            create_description: >-
              The identifier list defines additional identifiers that are able to be stored for an appointment.<br><br>These identifiers will not be surfaced on the Patient's chart, but they may help you identify the patient in your system by associating your identifier with the resource's `id`.
            update_description: >-
              The identifier list defines additional identifiers that are able to be stored for an appointment.<br><br>These identifiers will not be surfaced on the Patient's chart, but they may help you identify the patient in your system by associating your identifier with the resource's `id`.<br><br>
              To update an existing `identifier`, include the `id` in the `identifier[x].id` field returned from Read/Search.<br><br>
              The `identifier` section sent in an update will entirely replace existing identifiers currently within the period.start and period.end dates.<br><br>
              If an <code>identifier</code> already exists in the Canvas database and is not included in the Update message, it will be deleted if and only if the period.end date is in the future.
            attributes:
            - name: use
              type: string
            - name: system
              type: string
            - name: value
              type: string
            - name: period
              type: json
          - name: status
            type: string
            description: >-
              The status of the appointment. <br><br> **Canvas to FHIR Mapping**<br>unconfirmed > proposed<br>attempted > pending<br>confirmed > booked<br>arrived > arrived<br>roomed > check-in<br>exited > fulfilled<br>no-showed > noshow<br>cancelled > cancelled<br>deleted > entered-in-error
            create_description:
                Currently, Canvas only supports creating an appointment with the status "proposed". Any other input will be ignored. If no status is added it defaults to "proposed". A status can be updated later using the [Appointment Update](/api/appointment/#update) endpoint.
            update_description: >-
              The update endpoint supports the following statuses: **proposed, pending, booked, arrived, fulfilled, cancelled, noshow, checked-in** <br><br> Canvas currently does not support marking an appointment as entered-in-error or waitlist. See [Appointment Read](/api/appointment/#read) for a better understanding of how these FHIR statuses are mapping in Canvas. <br><br>Once an appointment's status is updated to "cancelled" it cannot be changed to a different status. If the status is removed, the update will default to what it was previously set to.
          - name: appointmentType
            type: json
            description: >-
              The style of appointment or patient that has been booked in the slot (not service type). Canvas supports configurable [apppointment and note types](/documentation/appointment-and-note-types/).
            create_description: >-
              Canvas supports configurable [appointment and note types](/documentation/appointment-and-note-types/). There are a few things to note with this field: <br><br>**1.**If the `appointmentType` attribute is omitted from the body completely, the note type that has `Is default appointment type` will be used (usually Office Visit if unchanged)<br><br>**2.**The `appointmentType` field must contain one coding, and it must be a SNOMED or INTERNAL coding.<br><br>**3.**If a code that does not exist is passed, you will see a 422 error status with error message `Appointment Create Error: Appointment Type does not exist with system: {system} and code: {code}` <br><br>**4.** If a code is passed that is not marked as `Is Scheduleable`, you will get a 422 error status with error message `Appointment Create Error: Appointment type must be scheduleable`.
            update_description: >-
              Canvas supports configurable [appointment and note types](/documentation/appointment-and-note-types/). There are a few things to note with this field: <br><br>**1.**If `appointmentType` attribute is omitted from the body completely, the note type that has `Is default appointment type` will be used (usually Office Visit if unchanged)<br><br>**2.**The `appointmentType` field must contain one coding, and it must be a SNOMED or INTERNAL coding.<br><br>**3.**If a code that does not exist is passed, you will see a 422 error status with error message `Appointment Create Error: Appointment Type does not exist with system: {system} and code: {code}` <br><br>**4.** If a code is passed that is not marked as `Is Scheduleable`, you will get a 422 error status with error message `Appointment Create Error: Appointment type must be scheduleable`.
            attributes:
              - name: coding
                type: array[json]
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
          - name: reasonCode
            type: array[json]
            description: >-
              Coded reason this appointment is scheduled. Canvas supports two ways to specify the reason for vist (RFV): [structured](/documentation/reason-for-visit-setting-codings) and unstructured. Both the `coding` and `text` attributes are used for Structured RFVs, whereas unstructured RFVs only leverage the `text` attribute.
            create_description:
              Canvas only accepts the first item in the reasonCode list.<br><br>

              If you are taking advantage of our [structured reason for visit](/documentation/reason-for-visit-setting-codings) feature, you can provide a `coding` that Canvas can use to look up the `code` value in configured in settings and display the structured RFV matching that code. If `Appointment.reasonCode[0].coding[0].code` is not a valid ReasonForVisitSettingCoding you will get the error "structured reason for visit with code {code} does not exist". <br><br> The `text` attribute maps to the free text Reason For Visit command.  If you are using the structured reason for visit feature, this text will display as the `comment` in the command.  **If you are not using the structured reason for visit feature**, then only `Appointment.reasonCode[0].text` needs to be populated in your message - `coding` should be omitted.
            update_description:
              In the Canvas UI, if the reasonCode / description is changed, it will update the reason for visit on that appointment. The old reason for visit will be marked as entered-in-error, and the text will no longer display. Below is an example of what an appointment's note will look like after changing the description multiple times. The originator and entered-in-error will be set to Canvas Bot, which can be seen if you click on the crossed off "Reason for Visit".<br><br>![api-update-rfv](/assets/images/api-update-rfv.png){:width="80%"}
            attributes:
              - name: coding
                type: array[json]
              - name: text
                type: string
          - name: description [deprecated]
            type: string
            description: >-
              Shown on a subject line in a meeting request, or appointment list.<br><br>
              **Note:** This field is being deprecated in favor of `reasonCode`. The text in `reasonCode` and this description attribute will always match.
          - name: supportingInformation
            type: array[json]
            description: >-
              Additional information to support the appointment. **References** are used to capture information about **rescheduled appointments** and the **location** of the appointment.<br><br>**Rescheduled Appointments**<br>If you see `Previously Rescheduled Appointment` in `supportingInformation`, it means that the appointment you are currently reading was created by rescheduling the appointment in that Reference. If you see `Rescheduled Replacement Appointment` in the `supportingInformation`, it means that the appointment you are currently reading is now outdated by a new appointment.
            create_description:
              You can use a Location reference within the `SupportingInformation` attribute to specify the Location of the appointment. To get the location reference, use the `id` from the [Location Search](/api/location/#search) endpoint.
            attributes:
              - name: reference
                type: string
              - name: type
                type: string
          - name: start
            type: datetime
            description: When appointment is to take place.
            create_description:
              The `start` attribute determines the start timestamp of the appointment. It is written in [instant format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required.
          - name: end
            type: datetime
            description: When appointment is to conclude.
            create_description:
              The end attribute is used with the start timestamp to determine the duration in minutes of the appointment. It is written in [instant format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required. <br><br> ⚠ Currently, Canvas does not provide any validation on this end date. If you have an end_date before the start_date, it will result in a negative duration being displayed on the UI.
          - name: participant
            description: >-
               Participants involved in appointment. Must include at least one entry for a practitioner. An optional 2nd entry may be used for the patient.<br><br>  The `actor.reference`:  `Practitioner/<practitioner_id>` maps to the rendering provider in Canvas.
            create_description:
              This list object requires one entry for a practitioner. An optional 2nd entry may be supplied for the patient.<br><br>   • The first entry has the `actor.reference` specify `Practitioner/<practitioner_id>` for the provider. This id can be found through a [Practitioner Search](/api/practitioner/#search). If `<practitioner_id>` is left blank, the practitioner will be set to Canvas Bot by default. <br>   • The second entry has the `actor.reference` specify `Patient/<patient_id>` for the patient this appointment is for. This id can be found through a [Patient Search](/api/patient/#search). <br><br>Per FHIR,  status is required, but it is not used by Canvas. Canvas recommends sending "active"
            type: array[json]
            attributes:
              - name: actor
                type: json
              - name: status
                required: true
                type: string
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: appointment-type
            type: string
            description: Filter by the code value under appointmentType.coding
          - name: location
            type: string
            description: The location of the appointment
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
            description: The status of the appointment
          - name: _sort
            type: string
            description: Triggers sorting of the results by a specific criteria. Supported values are **date**, **patient** and **practitioner**. Use **-date**, **-patient**, **-practitioner** to sort in descending order.
        endpoints: [create, read, update, search]
        create:
          description: Create an **Appointment**<br><br> **Prevent Double Booking** By default, Canvas does not prevent appointments from being created if there is already an existing appointment for that provider. However, Canvas has a config setting to disable double booking. If double booking is not allowed and the Appointment Create or Appointment Update request is trying to book an appointment for a given Provider that already has a scheduled appointment at that time, you will see a 422 error status with the following error message returned `This appointment time is no longer available.`
          responses: [201, 400, 401, 403, 405, 422]
          example_request: appointment-create-request
          example_response: appointment-create-response
        read:
          description: Read an Appointment
          responses: [200, 401, 403, 404]
          example_request: appointment-read-request
          example_response: appointment-read-response
        update:
          description: Update an **Appointment** This is almost identical to the [Appointment Create](/api/appointment/#create). The update will only affect fields that are passed in to the body, if any fields are omitted they will be ignored and kept as co are currently set in the Canvas database.
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: appointment-update-request
          example_response: appointment-update-response
        search:
          description: Search for an Appointment
          responses: [200, 400, 401, 403]
          example_request: appointment-search-request
          example_response: appointment-search-response
---

<div id="appointment-read-request">
{%  include read-request.html resource_type="Appointment" %}
</div>

<div id="appointment-read-response">
{% tabs appointment-read-response %}

{% tab appointment-read-response 200 %}
```json
{
    "resourceType": "Appointment",
    "id": "621a66fc-9d5c-4de0-97fb-935d611ac176",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint-0",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "identifier": [
        {
            "id": "97b28298-f618-4972-9a6b-d095785587d6",
            "use": "usual",
            "system": "AssigningSystem",
            "value": "test123",
            "period": {
                "start": "2024-01-01",
                "end": "2024-12-31"
            }
        }
    ],
    "status": "proposed",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": false
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "description": "Initial 30 Minute Visit",
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060",
            "type": "Location"
        },
        {
            "reference": "#appointment-meeting-endpoint-0",
            "type": "Endpoint"
        },
        {
            "reference": "Encounter/23668e1a-e914-4eac-885c-1a2a27244ab7",
            "type": "Encounter"
        }
    ],
    "start": "2023-10-24T13:30:00+00:00",
    "end": "2023-10-24T14:00:00+00:00",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                "type": "Practitioner"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d",
                "type": "Patient"
            },
            "status": "accepted"
        }
    ]
}
```
{% endtab %}

{% tab appointment-read-response 401 %}
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

{% tab appointment-read-response 403 %}
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

{% tab appointment-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Appointment resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
{% endtab %}

{% endtabs %}
</div>

<div id="appointment-search-request">
{% include search-request.html resource_type="Appointment" search_string="patient=Patient%2Fa031d1ba40d74aebb8ed716716da05c2&practitioner=Practitioner%2F4150cd20de8a470aa570a852859ac87e" %}
</div>

<div id="appointment-search-response">
{% tabs appointment-search-response %}
{% tab appointment-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
        {
            "relation": "self",
            "url": "/Appointment?patient=Patient%2Fa031d1ba40d74aebb8ed716716da05c2&practitioner=Practitioner%2F4150cd20de8a470aa570a852859ac87e&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Appointment?patient=Patient%2Fa031d1ba40d74aebb8ed716716da05c2&practitioner=Practitioner%2F4150cd20de8a470aa570a852859ac87e&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Appointment?patient=Patient%2Fa031d1ba40d74aebb8ed716716da05c2&practitioner=Practitioner%2F4150cd20de8a470aa570a852859ac87e&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Appointment",
                "id": "f7bb6d7e-1cab-42cd-b3d2-40229e1bede7",
                "contained":
                [
                    {
                        "resourceType": "Endpoint",
                        "id": "appointment-meeting-endpoint-0",
                        "status": "active",
                        "connectionType":
                        {
                            "code": "https"
                        },
                        "payloadType":
                        [
                            {
                                "coding":
                                [
                                    {
                                        "code": "video-call"
                                    }
                                ]
                            }
                        ],
                        "address": "https://url-for-video-chat.example.com?meeting=abc123"
                    }
                ],
                "identifier": [
                  {
                      "id": "97b28298-f618-4972-9a6b-d095785587d6",
                      "use": "usual",
                      "system": "AssigningSystem",
                      "value": "test123",
                      "period": {
                          "start": "2024-01-01",
                          "end": "2024-12-31"
                      }
                  }
                ],
                "status": "proposed",
                "appointmentType":
                {
                    "coding":
                    [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "448337001",
                            "display": "Telemedicine"
                        }
                    ]
                },
                "reasonCode":
                [
                    {
                        "coding":
                        [
                            {
                                "system": "INTERNAL",
                                "code": "INIV",
                                "display": "Initial Visit",
                                "userSelected": false
                            }
                        ],
                        "text": "Initial 30 Minute Visit"
                    }
                ],
                "description": "Initial 30 Minute Visit",
                "supportingInformation":
                [
                    {
                        "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060",
                        "type": "Location"
                    },
                    {
                        "reference": "#appointment-meeting-endpoint-0",
                        "type": "Endpoint"
                    },
                    {
                        "reference": "Encounter/797ccaae-2939-4e8a-9d91-5e9574a11a4e",
                        "type": "Encounter"
                    }
                ],
                "start": "2023-10-24T13:30:00+00:00",
                "end": "2023-10-24T14:00:00+00:00",
                "participant":
                [
                    {
                        "actor":
                        {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner"
                        },
                        "status": "accepted"
                    },
                    {
                        "actor":
                        {
                            "reference": "Patient/a031d1ba40d74aebb8ed716716da05c2",
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
{% tab appointment-search-response 401 %}
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

{% tab appointment-search-response 403 %}
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

<div id="appointment-create-request">
{% tabs appointment-create-request %}

{% tab appointment-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Appointment' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Appointment",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "identifier": [
        {
            "use": "usual",
            "system": "AssigningSystem",
            "value": "test123",
            "period": {
                "start": "2024-01-01",
                "end": "2024-12-31"
            }
        }
    ],
    "status": "proposed",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": false
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060"
        },
        {
            "reference": "#appointment-meeting-endpoint",
            "type": "Endpoint"
        }
    ],
    "start": "2023-10-24T13:30:00.000Z",
    "end": "2023-10-24T14:00:00.000Z",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e"
            },
            "status": "accepted"
        }
    ]
}
'
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
    "resourceType": "Appointment",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "identifier": [
      {
          "use": "usual",
          "system": "AssigningSystem",
          "value": "test123",
          "period": {
              "start": "2024-01-01",
              "end": "2024-12-31"
          }
      }
    ],
    "status": "proposed",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": False
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060"
        },
        {
            "reference": "#appointment-meeting-endpoint",
            "type": "Endpoint"
        }
    ],
    "start": "2023-10-24T13:30:00.000Z",
    "end": "2023-10-24T14:00:00.000Z",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e"
            },
            "status": "accepted"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
{% endtabs %}
</div>

<div id="appointment-create-response">
{% include create-response.html %}
</div>

<div id="appointment-update-request">
{% tabs appointment-update-request %}

{% tab appointment-update-request curl %}
```shell
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/Appointment/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Appointment",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "identifier": [
      {
          "id": "97b28298-f618-4972-9a6b-d095785587d6",
          "use": "usual",
          "system": "AssigningSystem",
          "value": "test123",
          "period": {
              "start": "2024-01-01",
              "end": "2024-12-31"
          }
      }
    ],
    "status": "cancelled",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": false
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060"
        },
        {
            "reference": "#appointment-meeting-endpoint",
            "type": "Endpoint"
        }
    ],
    "start": "2023-10-24T13:30:00.000Z",
    "end": "2023-10-24T14:00:00.000Z",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e"
            },
            "status": "accepted"
        }
    ]
}
'
```
{% endtab %}
{% tab appointment-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Appointment/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Appointment",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "identifier": [
      {
          "id": "97b28298-f618-4972-9a6b-d095785587d6",
          "use": "usual",
          "system": "AssigningSystem",
          "value": "test123",
          "period": {
              "start": "2024-01-01",
              "end": "2024-12-31"
          }
      }
    ],
    "status": "cancelled",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": False
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060"
        },
        {
            "reference": "#appointment-meeting-endpoint",
            "type": "Endpoint"
        }
    ],
    "start": "2023-10-24T13:30:00.000Z",
    "end": "2023-10-24T14:00:00.000Z",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e"
            },
            "status": "accepted"
        }
    ]
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
{% endtabs %}
</div>

<div id="appointment-update-response">
{% include update-response.html resource_type="Appointment" %}
</div>
