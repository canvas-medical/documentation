---
layout: api
title: "Allergy Interolerace Read"
categories: cat1 cat2
tags: tag1 tag2
request_sample: It may be difficult to display code blocks in front-matter
---

## POST: https://fhir-example.canvasmedical.com/Appointment
Book an appointment with a provider in Canvas. If the appointment specifies a patient, then upon successful creation you will see the appointment on the Calendar view and within the Patient's Chart. An appointment is always created with a status of booked in FHIR (Confirmed in Canvas).

### Attributes that are pulled into Canvas:
#### reasonCode
This field contains the Reason For Visit of the appointment. Where we only accept the first item in the reasonCode list.

If you are taking advantage of our Structured Reason For Visit Feature, then you can provide a coding where we look up that code value in Settings and display the Structure RFV matching that code. If Appointment.reasonCode[0].coding[0].code is not a valid ReasonForVisitSettingCoding in Admin you will get the error "Structured reason for visit with code {code} does not exist"

If there is text attribute, that will become the free text on the Reason For Visit command. If no text field we use the description field. If neither are filled we use No description given. If you are using the structured reason for visit feature, this text will display as the comment in the command.

```
"reasonCode": [{
  "coding": [{
    "system": "INTERNAL"
    "code": "9903",
    "display": "Urgent Visit"
  }],
  "text": "Weekly check-in"
}],
```
