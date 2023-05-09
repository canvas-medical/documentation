---
title: "Appointment Read"
layout: api
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
