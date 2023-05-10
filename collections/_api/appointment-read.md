---
title: "Appointment Read"
---
## Rescheduled Appointments

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
## Appointment Status

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
