---
title: "Appointment Create"
slug: "appointment-create"
excerpt: "Book an appointment with a provider in Canvas. If the appointment specifies a patient, then upon successful creation you will see the appointment on the Calendar view and within the Patient's Chart. An appointment is always created with a status of booked in FHIR (Confirmed in Canvas)."
hidden: false
createdAt: "2021-05-14T03:04:07.331Z"
updatedAt: "2023-04-19T17:35:25.527Z"
---
# Attributes that are pulled into Canvas:

## reasonCode

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



## description [deprecated]

**Note**: This field is being deprecated in favor of `reasonCode`. The `text` in reasonCode and this `description` attribute will always match. 

This is free text of the reason for visit for the appointment.  It will automatically populate a `reason for visit` command's within the note for the appointment. If none is given, it defaults to "No description given". 

```text
"description": "Weekly check-in.",
```



## participant [REQUIRED]

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



# appointmentType

Canvas supports a variety of appointment types. This table documents the code and code system of the different Appointment types that Canvas has built in. 

| Canvas Appointment Type | Code System              | Code      |
| :---------------------- | :----------------------- | :-------- |
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

```text
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



# start [REQUIRED]

The `start` attribute determines the start timestamp of the appointment. It is written in [instance format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required. 

```text
"start": "2022-03-20T13:30:00.000Z",
```



# end [REQUIRED]

The `end` attribute is used with the start timestamp to determine the duration in minutes of the appointment.  It is written in [instance format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required. 

**Note**: Currently, we do not provide any validation on this end date. If you have an end_date before the start_date, it will result in a negative duration being displayed on the UI. 

```text
"end": "2022-03-20T14:00:00.000Z",
```



## supportingInformation [REQUIRED]

To specify the Location of the appointment, Canvas reads the information from the SupportingInformation attribute. Use this example below. To get the location id, you can utilize the [Schedule Search](ref:search-1)  endpoint.  This will give you a resource.id like `Location.1-Staff.c2ff4546548e46ab8959af887b563eab` where you can pull out the Location ID - the value displayed after the period - and place it in the reference example below. If your instance only has one practice location, the ID will always be `1`. 

```text
"supportingInformation": [
        {
            "reference": "Location/{{_id}}"
        }
]
```



## status

Currently, Canvas only supports creating an appointment with the status "proposed". Any other input will be ignored. If no status is added it defaults to "proposed". A status can be updated later using the [Appointment Update](ref:appointment-update) endpoint.

# Canvas can receive a custom meeting link for virtual appointments:

The FHIR Appointment API now accepts a custom video meeting link to be passed in that will be utilized on the UI over the default provider's meeting link if the appointment is a telemedicine. 

To do this you would need to add a SupportingInformation `reference` of "#appointment-meeting-endpoint" with a `type` of "Endpoint"

Then you would need to specify the `address` url of the meeting link in a `contained` object along with the `resourceType` = `Endpoint` and the `id` = `appointment-meeting-endpoint`. All other fields are automatically populated by Canvas and are not required. 

See example:

```text
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



# (New) Preventing Double Booking in Canvas

> 📘 New
> 
> This feature was released on June 22, 2022. See [release notes](https://canvas-medical.zendesk.com/hc/en-us/articles/7054913090067)

By default, Canvas does not prevent appointments from being created if there is already an existing appointment for that provider. However, we have a config setting to [disable double booking](https://canvas-medical.zendesk.com/hc/en-us/articles/7055640868371).  If double booking is not allowed and the Appointment Create or [Appointment Update](ref:update) request is trying to book an appointment for a given Provider that already has a scheduled appointment at that time, you will see a 422 error status with the following error message returned: 

`This appointment time is no longer available.`