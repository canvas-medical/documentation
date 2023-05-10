---
title: "Appointment Update"
layout: API
---
This is almost identical to the [Appointment Create](ref:create). The update will only affect fields that are passed in to the body, if any fields are omitted they will be ignored and kept as they are currently set in the Canvas database. 

# Additional Exceptions to Specific Appointment Update Attributes

## status

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

## reasonCode / description 

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

## id 

_id is used to identify the specific appointment that is being modified.

## Other attributes

Refer to the [Appointment Create](ref:create) attributes on what can else can be updated per appointment.
