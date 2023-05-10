---
title: "Appointment"
---
## Apointment Read

### Rescheduled Appointments

We now have some references in the supportingInformation that can give some insight into rescheduled appointments. 

If you see `Previously Rescheduled Appointment` in the supportingInformation, it means that the appointment you are currently reading was created by rescheduling the appointment in that Reference. 
[block:code]
{
  "codes": [
    {
      "code": "{\n\t\"reference\": \"Appointment/fc512e54-a5ce-4046-9101-03df00f5572f\",\n\t\"display\": \"Previously Rescheduled Appointment\"\n}",
      "language": "text"
    }
  ]
}
[/block]
If you see `Rescheduled Replacement Appointment` in the supportingInformation, it means that the appointment you are currently reading is now outdated by a new appointment. 
[block:code]
{
  "codes": [
    {
      "code": "{\n\t\"reference\": \"Appointment/0d4a422d-0d61-47bd-bf84-eade0115e59a\",\n\t\"display\": \"Rescheduled Replacement Appointment\"\n}",
      "language": "text"
    }
  ]
}
[/block]
### Appointment Status

The status of the appointment is mapped from the status dropdown you see on the schedule view of Canvas. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ada195e-Screen_Shot_2022-03-09_at_10.41.58_AM.png",
        "Screen Shot 2022-03-09 at 10.41.58 AM.png",
        722,
        620,
        "#f0f0f0"
      ]
    }
  ]
}
[/block]
The mapping is as follows:
[block:parameters]
{
  "data": {
    "h-0": "Canvas Status",
    "h-1": "FHIR Status",
    "0-0": "Unconfirmed",
    "0-1": "proposed",
    "1-0": "Attempted",
    "1-1": "pending",
    "2-0": "Confirmed",
    "2-1": "booked",
    "3-0": "Arrived",
    "3-1": "arrived",
    "4-0": "Roomed",
    "4-1": "checked-in",
    "5-0": "Exited",
    "5-1": "fulfilled",
    "6-0": "No-showed",
    "6-1": "noshow"
  },
  "cols": 2,
  "rows": 7
}
[/block]
In addition to this dropdown there is the following statuses:
- `cancelled` an appointment will read as cancelled if the appointment was marked as cancelled via the patient chart or if we are reading an appointment that was rescheduled to a different time
- `entered-in-error` an appointment will read as entered-in-error if the appointment was deleted via the patient chart

``` json
{
  "resourceType": "Appointment",
  "id": "94d34e0f-b5c2-4af1-b806-acec8866da18",
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

{
    "resourceType": "Appointment",
    "id": "94d34e0f-b5c2-4af1-b806-acec8866da18",
    "meta": {
        "versionId": "1",
        "lastUpdated": "2021-11-05T19:32:09.539+00:00"
    },
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
    "status": "booked",
    "appointmentType": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "reasonCode": [
      {
        "coding": [
          {
            "system": "internal",
            "code": "0",
            "display": "annual follow up",
            "userSelected": false
          }
        ],
        "text": "Need to check condition annually"
      }
    ],
    "description": "Need to check condition annually",
    "supportingInformation": [
        {
          "reference": "Location/1"
        },
        {
          "reference": "#appointment-meeting-endpoint-1",
          "type": "Endpoint"
        },
        {
          "reference": "Encounter/c08dcf8d-a23c-448f-acc8-1a5832dc9006",
          "type": "Encounter"
        },
        {
          "reference": "Appointment/fc512e54-a5ce-4046-9101-03df00f5572f",
          "display": "Previously Rescheduled Appointment"
        },
        {
          "reference": "Appointment/0d4a422d-0d61-47bd-bf84-eade0115e59a",
          "display": "Rescheduled Replacement Appointment"
        }
    ],
    "start": "2021-03-20T13:30:00.000Z",
    "end": "2021-03-20T14:00:00.000Z",
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
    ]
}
```

## Appointment Search

### Searching using a Date Range

We allow for a start and end date parameter to be sent in the request to allow for range searching. For example if you wanted to find all appointments for a patient between February 20, 2022 and February 24, 2022, you can now make a call using these parameters:
[block:code]
{
  "codes": [
    {
      "code": "{{base_url}}/Appointment?date=ge2022-02-20&date=le2022-02-24&patient=Patient/{{patient_id}}",
      "language": "text"
    }
  ]
}
[/block]
### Creating an Appointment in Canvas

To learn how to book an appointment in Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360056430014-Appointments). To see how to manage an already scheduled appointment, read this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4408062178963-Appointment-Management).

### Rescheduled Appointments

There may be some insights into appointment rescheduling. This is documented in the [Appointment Read](ref:appointment-read) 

### Appointment Statuses

To understand our mapping of appointment statuses, see [Appointment Read](ref:appointment-read) 
[block:api-header]
{
  "title": "Pagination"
}
[/block]
To paginate appointment search results, use the query param `_count`.
Example:
`GET /Appointment?_count=10` will return the first 10 appointments, along with relative links to see the subsequent pages.
The pages are specified by a combination of `_count` and `_offset`.




## Appointment Create

### Attributes that are pulled into Canvas:

### reasonCode

This field contains the Reason For Visit of the appointment. Where we only accept the first item in the `reasonCode` list. 

If you are taking advantage of our [Structured Reason For Visit Feature](https://canvas-medical.zendesk.com/hc/en-us/articles/4417495811859-Structured-Reason-for-Visit), then you can provide a `coding` where we look up that `code` value in Settings and display the Structure RFV matching that code. If Appointment.reasonCode[0].coding[0].code is not a valid ReasonForVisitSettingCoding in Admin you will get the error `"Structured reason for visit with code {code} does not exist"`

If there is `text` attribute, that will become the free text on the Reason For Visit command. If no text field we use the `description` field. If neither are filled we use `No description given`. If you are using the structured reason for visit feature, this text will display as the `comment` in the command. 

```text
"reasonCode": [{
  "coding": [{
    "system": "INTERNAL"
    "code": "9903",
    "display": "Urgent Visit"
  }],
  "text": "Weekly check-in"
}],
```



### description [deprecated]

**Note**: This field is being deprecated in favor of `reasonCode`. The `text` in reasonCode and this `description` attribute will always match. 

This is free text of the reason for visit for the appointment.  It will automatically populate a `reason for visit` command's within the note for the appointment. If none is given, it defaults to "No description given". 

```text
"description": "Weekly check-in.",
```



### participant [REQUIRED]

This list objects requires 1 entry for a practitioner. An optional 2nd entry may be supplied for a patient.

- The first entry has the `actor.reference` specify \`Practitioner/\<practitioner_id> for the provider. This id can be found through a [Practitioner Search](ref:search).  If \<practitioner_id> is left blank, the practitioner will be set to Canvas Bot by default.
- The second entry has the `actor.reference` specify `Patient/<patient_id>` for the patient this appointment is for. This id can be found through a [Patient Search](ref:patient-search)  

The status attribute is not ingested by Canvas. Canvas stores "accepted" as the status for each participant regardless of the input. You can see this "accepted" status if you perform a read or search for the appointment. 

```text
"participant": [
        {
            "actor": {
                "reference": "Practitioner/dbf184ad28a1408bbed184fc8fd2b029"
            },
            "status": "accepted"
        },
        {
            "actor": {
                "reference": "Patient/5350cd20de8a470aa570a852859ac87e"
            },
            "status": "accepted"
        }
    ]
```



### appointmentType

Canvas supports a variety of appointment types. This table documents the code and code system of the different Appointment types that Canvas has built in. 

| Canvas Appointment Type | Code System              | Code      |
| ----------------------- | ------------------------ | --------- |
| Home Visit              | <http://snomed.info/sct> | 439708006 |
| Telemedicine            | <http://snomed.info/sct> | 448337001 |
| Office Visit            | <http://snomed.info/sct> | 308335008 |
| Lab Visit               | <http://snomed.info/sct> | 31108002  |
| Phone Call              | <http://snomed.info/sct> | 185317003 |

We also allow customers to configure their own Note Type. See this [Zendesk Article](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-) on how to add your own customizable note types. 

There are a few things to note with this field:

1. If `appointmentType` attribute is omitted from the body completely, the note type that has `Is default appointment type` will be used. If your instance has not changed this setting it will be an Office Visit. 

2. If a code that does not exist is passed, you will see a 422 error status with error message `Appointment Create Error: Appointment Type does not exist with system: http://snomed.info/sct and code: {code}`

3. If a code is passed that is not marked as `Is Scheduleable`, you will get a 422 error status with error message `Appointment Create Error: Appointment type must be scheduleable.`

``` json
"appointmentType": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
```



### start [REQUIRED]

The `start` attribute determines the start timestamp of the appointment. It is written in [instance format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required. 

``` json
"start": "2022-03-20T13:30:00.000Z",
```



### end [REQUIRED]

The `end` attribute is used with the start timestamp to determine the duration in minutes of the appointment.  It is written in [instance format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required. 

**Note**: Currently, we do not provide any validation on this end date. If you have an end_date before the start_date, it will result in a negative duration being displayed on the UI. 

``` json
"end": "2022-03-20T14:00:00.000Z",
```



### supportingInformation [REQUIRED]

To specify the Location of the appointment, Canvas reads the information from the SupportingInformation attribute. Use this example below. To get the location id, you can utilize the [Schedule Search](ref:search-1)  endpoint.  This will give you a resource.id like `Location.1-Staff.c2ff4546548e46ab8959af887b563eab` where you can pull out the Location ID - the value displayed after the period - and place it in the reference example below. If your instance only has one practice location, the ID will always be `1`. 

```text
"supportingInformation": [
        {
            "reference": "Location/{{_id}}"
        }
]
```



### status

Currently, Canvas only supports creating an appointment with the status "proposed". Any other input will be ignored. If no status is added it defaults to "proposed". A status can be updated later using the [Appointment Update](ref:appointment-update) endpoint.

### Canvas can receive a custom meeting link for virtual appointments:

The FHIR Appointment API now accepts a custom video meeting link to be passed in that will be utilized on the UI over the default provider's meeting link if the appointment is a telemedicine. 

To do this you would need to add a SupportingInformation `reference` of "#appointment-meeting-endpoint" with a `type` of "Endpoint"

Then you would need to specify the `address` url of the meeting link in a `contained` object along with the `resourceType` = `Endpoint` and the `id` = `appointment-meeting-endpoint`. All other fields are automatically populated by Canvas and are not required. 

See example:

``` json
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
"supportingInformation": [
        {
            "reference": "Location/1"
        },
        {
            "reference": "#appointment-meeting-endpoint",
            "type": "Endpoint"
        }
 ],
```



### (New) Preventing Double Booking in Canvas

> 📘 New
> 
> This feature was released on June 22, 2022. See [release notes](https://canvas-medical.zendesk.com/hc/en-us/articles/7054913090067)

By default, Canvas does not prevent appointments from being created if there is already an existing appointment for that provider. However, we have a config setting to [disable double booking](https://canvas-medical.zendesk.com/hc/en-us/articles/7055640868371).  If double booking is not allowed and the Appointment Create or [Appointment Update](ref:update) request is trying to book an appointment for a given Provider that already has a scheduled appointment at that time, you will see a 422 error status with the following error message returned: 

`This appointment time is no longer available.`

## Appointment Update

This is almost identical to the [Appointment Create](ref:create). The update will only affect fields that are passed in to the body, if any fields are omitted they will be ignored and kept as they are currently set in the Canvas database. 

#### Additional Exceptions to Specific Appointment Update Attributes

### status

Users can pass in any of these supported statuses to the appointment: 
- proposed
- pending
- booked
- arrived
- fulfilled 
- cancelled 
- noshow 
- checked-in

We currently do not support marking an appointment as `entered-in-error` or `waitlist`. See [Appointment Read](ref:appointment-read) for a better understanding of how these FHIR statuses are mapping in Canvas. 

Once an appointment's status is updated to "cancelled" it cannot be changed to a different status. If the status is removed, the update will default to what it was previously set to.

### reasonCode / description 

In the Canvas UI, if the reasonCode / description is changed, it will update the reason for visit on that appointment. The old reason for visit will be marked as entered-in-error, and the text will no longer display. Below is an example of what an appointment's note will look like after changing the description multiple times: 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/33b63c7-Screen_Shot_2022-06-24_at_10.12.52_AM.png",
        "Screen Shot 2022-06-24 at 10.12.52 AM.png",
        1858,
        658,
        "#f9f9f9"
      ],
      "caption": "Updating an appointment's description"
    }
  ]
}
[/block]
The originator and entered-in-error will be set to Canvas Bot, which can be seen if you click on the crossed off "Reason for Visit".

### id 

id is used to identify the specific appointment that is being modified.

### Other attributes

Refer to the [Appointment Create](ref:create) attributes on what can else can be updated per appointment.

