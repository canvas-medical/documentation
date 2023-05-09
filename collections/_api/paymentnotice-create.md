---
title: "PaymentNotice Create"
slug: "paymentnotice-create"
excerpt: "Note a payment that has been collected from a patient and deduct the amount from their balance."
hidden: false
createdAt: "2022-06-22T15:39:37.898Z"
updatedAt: "2022-06-28T14:39:35.764Z"
---
[block:callout]
{
  "type": "warning",
  "title": "Don't overpay!",
  "body": "Requests that would bring the account balance negative will be rejected.\nExample: If a patient owes $5, we would reject a PaymentNotice with a value >$5."
}
[/block]
# Getting the newly-created payment notice ID.
Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header.

# Finding a created Payment Notice in the Canvas UI

A created payment notice can be found in Canvas by going to the patient's chart, and clicking the paper icon in the top right corner. The created payment notice will be displayed under receipts. The "Originator" will be automatically set to Canvas Bot. 

As payment notices are created, they will be applied to charges in chronological order of creation date, from oldest to newest. 

# Attributes that are pulled into Canvas:

## status [required]

Required by the FHIR spec. Canvas only accepts payments with a status of "active".
[block:code]
{
  "codes": [
    {
      "code": "status\": \"active\"",
      "language": "text"
    }
  ]
}
[/block]
## request [required]

Canvas patient resource whose balance the payment will be applied to, formatted like "Patient/5350cd20de8a470aa570a852859ac87e". 
[block:code]
{
  "codes": [
    {
      "code": "\"request\": {\n   \"reference\": \"Patient/5350cd20de8a470aa570a852859ac87e\"\n}",
      "language": "text"
    }
  ]
}
[/block]
## amount [required]

The value field accepts amount of the payment in US dollars. The currency field is not required. It defaults to "USD" and ignores all other inputs. 
[block:code]
{
  "codes": [
    {
      "code": "\"amount\": {\n  \"value\": 10.00,\n  \"currency\": \"USD\"\n}",
      "language": "text"
    }
  ]
}
[/block]