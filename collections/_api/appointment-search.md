---
title: "Appointment Search"
layout: API
---
## Searching using a Date Range

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
## Creating an Appointment in Canvas

To learn how to book an appointment in Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360056430014-Appointments). To see how to manage an already scheduled appointment, read this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4408062178963-Appointment-Management).

## Rescheduled Appointments

There may be some insights into appointment rescheduling. This is documented in the [Appointment Read](ref:appointment-read) 

## Appointment Statuses

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
