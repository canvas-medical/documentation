---
title: "Coverage Create"
slug: "coverage-create"
excerpt: "Create a coverage"
hidden: false
createdAt: "2022-06-21T13:07:59.742Z"
updatedAt: "2022-06-28T14:25:02.468Z"
---
# Getting the newly-created coverage ID.
Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header. You will use this for subsequent requests that reference this coverage.

# Finding created coverages in the Canvas UI:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/a055177-Screen_Shot_2022-06-23_at_11.46.31_AM.png",
        "Screen Shot 2022-06-23 at 11.46.31 AM.png",
        1686,
        284,
        "#f6f6f6"
      ]
    }
  ]
}
[/block]
The above screenshot depicts what a coverage will look like in the UI after it has been created:
- Arrow 1 points to the `order` number. 
- The title that arrow 2 points to comes from what the `payer.code` is mapped to. 
- Arrow 3's text comes from `type`. 
- Arrow 4 points to the `subscriberID`.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/225155b-updatecoverage.png",
        "updatecoverage.png",
        2152,
        1588,
        "#f5f5f5"
      ]
    }
  ]
}
[/block]
The above view can be found by clicking the three dots on the coverage and selecting "View/Update": 
- Arrow 1 points to the field that is filled by the `payor` attribute. 
- Arrow 2 points to the `subscriberId`. 
- Arrow 3 points to a field that is filled if `type.code`= 'group' is included. 
- Arrow 4 shows where the value associated with `type.code`= 'plan' is displayed. 
- The `period` parameter's start and end attributes are displayed here as well (see arrows 5 and 6). 
- Arrow 7 points to the coverage type that is specified via the `type.coding`. In order for this value to display on the Canvas UI, the coverage type needs to be configured for the specific payor via our insurer settings. To get to these settings, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers).
- Finally, arrow 8's selection of patient or other as the subscriber is based on the `relationship` field. If anything other than 'self' is inputted as `relationship.code`, the below screen will show on the Canvas UI within the View/Update Coverage screen:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/08a25a2-Screen_Shot_2022-06-23_at_2.57.38_PM.png",
        "Screen Shot 2022-06-23 at 2.57.38 PM.png",
        1302,
        286,
        "#f9f8f8"
      ]
    }
  ]
}
[/block]
This will autofill the subscriber as the patient in the `subscriber` field, and patient relationship to subscriber will be set as whatever was ingested for `relationship. 


# Attributes that are pulled into Canvas:

## order [required]

The order in which coverages should be used when adjudicating claims. It must be a number 1 through 5. If multiple coverages are created with the same order number, the older one will be bumped down in rank, and the new one will take that rank. If this leads to multiple coverages being incremented to 5, the oldest (first to be inputted) of the coverages at this rank will be displayed on the Canvas UI.
[block:code]
{
  "codes": [
    {
      "code": "\"order\": 1",
      "language": "text"
    }
  ]
}
[/block]
## status [required]

Canvas currently only ingests 'active' and 'entered-in-error' as statuses. If anything else is entered, status will default to active. Status is not displayed on the Canvas UI.
[block:code]
{
  "codes": [
    {
      "code": "\"status\": \"active\"",
      "language": "text"
    }
  ]
}
[/block]
## type

Coverage code category such as medical or accident using values from http://hl7.org/fhir/ValueSet/coverage-type. The coding object contains the following attributes: 

- The `system` URL must match `http://hl7.org/fhir/ValueSet/coverage-type` exactly or the type will be ignored.
- `code` is a required string. If an empty string is entered for the code, the entire type field will be ignored by Canvas. 
- `display` is ignored.

In order for this value to display on the Canvas UI, the coverage type needs to be configured for the specific payor via our insurer settings. To get to these settings, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360062281054-Managing-Insurers).
[block:code]
{
  "codes": [
    {
      "code": "\"type\": {\n        \"coding\": [\n            {\n                \"system\": \"http://hl7.org/fhir/ValueSet/coverage-type\",\n                \"code\": \"MILITARY\",\n                \"display\": \"military health program\"\n            }\n        ]\n }",
      "language": "text"
    }
  ]
}
[/block]
## subscriber [required]

Canvas patient resource for the subscriber of the coverage, formatted like "Patient/5350cd20de8a470aa570a852859ac87e". 
[block:code]
{
  "codes": [
    {
      "code": "\"subscriber\": {\n      \"reference\": \"Patient/febae9dcb7cf4d88ba27cc552a3f96b34\"\n },",
      "language": "text"
    }
  ]
}
[/block]
## subscriberId

Value assigned by insurer to identify the subscriber.
[block:code]
{
  "codes": [
    {
      "code": "\"subscriberId\": \"1234\",",
      "language": "text"
    }
  ]
}
[/block]
## beneficiary [required]

Canvas patient resource the coverage should be created for, formatted like "Patient/5350cd20de8a470aa570a852859ac87e". This dictates which patient the coverage is for.
[block:code]
{
  "codes": [
    {
      "code": "\"beneficiary\": {\n        \"reference\": \"Patient/febae9dcb7cf4d88ba27cc552a3f96b3\"\n},",
      "language": "text"
    }
  ]
}
[/block]
## relationship [required]

The beneficiary's relationship to the subscriber from http://hl7.org/fhir/ValueSet/subscriber-relationship.  If more than one value is sent from the ValueSet, the first one in the list will be used. The system must match "http://hl7.org/fhir/ValueSet/subscriber-relationship" exactly. The choices for the relationship code are: 'child', 'spouse', 'other', 'self' and 'injured'. 
[block:code]
{
  "codes": [
    {
      "code": "\"relationship\": {\n   \"coding\": [\n       {\n          \"system\": \"http://hl7.org/fhir/ValueSet/subscriber-relationship\",\n          \"code\": \"self\"\n       }\n   ]\n},",
      "language": "text"
    }
  ]
}
[/block]
## period [required]

`period.start` Indicates when the coverage became active for the patient, formatted as YYYY-MM-DD. This is a required field.
`period.end` Indicates when the coverage was no longer active for the patient, formatted as YYYY-MM-DD. Adding an end date to the period is not required. If it is not entered, it will default to no end date. 
Coverage dates can be viewed in the Canvas UI by clicking the three dots in the top right corner of the coverage and selecting 'View/Update'. 
[block:code]
{
  "codes": [
    {
      "code": "\"period\": {\n    \"start\": \"2021-06-27\"\n    \"end\": \"2023-06-27\"\n},",
      "language": "text"
    }
  ]
}
[/block]
## payor [required]

`payor.identifier`: If more than one is sent, the first one in the list will be used.
         -`value`: The payor id received from a clearinghouse (we use Claim.md).
         -`system`: should be set to "https://www.claim.md/services/era/"
`display`: This field is ignored.
[block:code]
{
  "codes": [
    {
      "code": " \"payor\": [\n    {\n        \"identifier\": {\n            \"system\": \"https://www.claim.md/services/era/\",\n            \"value\": \"AMM03\"\n        },\n        \"display\": \"Independence Blue Cross Blue Shield\"\n    }\n],",
      "language": "text"
    }
  ]
}
[/block]
## class

This list is used to define the plan, subplan, group and subgroup. The example below shows the type attribute for each class. None of these classes are required and can be omitted. The `system` of each coding must match "http://hl7.org/fhir/ValueSet/coverage-class", and the code is one of the four classes. 

The value attribute is a free text field to denote the value for each type.

Subplan and subgroup are stored by Canvas but are not displayed on the Canvas UI.
[block:code]
{
  "codes": [
    {
      "code": "\"class\": [\n     {\n        \"type\": {\n            \"coding\": [\n                 {\n                    \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",\n                    \"code\": \"plan\"\n                 }\n            ]\n       },\n       \"value\": \"Starfleet HMO\"\n     },\n     {\n        \"type\": {\n            \"coding\": [\n                 {\n                    \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",\n                    \"code\": \"subplan\"\n                 }\n            ]\n       },\n       \"value\": \"Stars\"\n     },\n     {\n         \"type\": {\n             \"coding\": [\n                 {\n                     \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",\n                     \"code\": \"group\"\n                 }\n              ]\n         },\n        \"value\": \"Captains Only\"\n      },\n      {\n        \"type\": {\n            \"coding\": [\n                 {\n                    \"system\": \"http://hl7.org/fhir/ValueSet/coverage-class\",\n                    \"code\": \"subgroup\"\n                 }\n            ]\n       },\n       \"value\": \"Subgroup 2\"\n     }\n],",
      "language": "text"
    }
  ]
}
[/block]