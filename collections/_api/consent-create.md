---
title: "Consent Create"
slug: "consent-create"
excerpt: "Create a Patient's Consent object in Canvas"
hidden: false
createdAt: "2022-06-08T21:02:20.797Z"
updatedAt: "2022-06-23T00:25:41.008Z"
---
# Updating existing `PatientConsent` objects
A `PatientConsent` is uniquely distinguished by:
1. The patient it's associated with
2. The `ConsentCoding` it's associated with

This Create endpoint acts as a create or update endpoint. If the patient given already has an existing Patient Consent with the given ConsentCoding, this endpoint will update that consent in place and the `id` returned in the response will not be changed. 

# Consent Attributes

This section will outline the following attributes a Create Consent endpoint can ingest. To learn more about the Patient Consent feature in Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/5524511564947-Patient-Consents). Especially useful in that article is how to set up the type of Consents allowed in your instance. That step must be complete before using this endpoint. 

## resourceType [REQUIRED]

This will be hardcoded to `Consent` for this endpoint 
[block:code]
{
  "codes": [
    {
      "code": "\"resourceType\": \"Consent\",",
      "language": "text"
    }
  ]
}
[/block]
## status 

This `status` attribute tells Canvas if the consent for the given patient is accepted or rejected. If not specified, the default will be `active`. Here is the mapping of status from FHIR enum to Canvas:

[block:parameters]
{
  "data": {
    "h-0": "FHIR enum",
    "h-1": "Canvas state",
    "0-0": "active",
    "0-1": "accepted",
    "1-0": "rejected",
    "1-1": "rejected"
  },
  "cols": 2,
  "rows": 2
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "\"status\": \"active\",",
      "language": "text"
    }
  ]
}
[/block]
## scope [REQUIRED]

While this field is required by the FHIR spec, we currently don't process this field in Canvas.  You can just use the example for this field
[block:code]
{
  "codes": [
    {
      "code": "    \"scope\": {\n        \"coding\": [\n            {\n                \"system\": \"http://terminology.hl7.org/CodeSystem/consentscope\",\n                \"code\": \"patient-privacy\"\n            }\n        ]\n    },",
      "language": "text"
    }
  ]
}
[/block]
## category [REQUIRED]

The `category` helps Canvas determine which Consent type you are creating/updating for a patient. We use the `code` or `display` to find the correct coding. So either the `system` and `code` or `system` and `display` need to exactly match what is entered in the Canvas Setting Admin outlined in the Zendesk article above. 

Using this Consent Coding as an example:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/39c9790-Screen_Shot_2022-06-13_at_11.53.02_AM.png",
        "Screen Shot 2022-06-13 at 11.53.02 AM.png",
        891,
        549,
        "#f3f7f9"
      ]
    }
  ]
}
[/block]
Here is the category you would pass in to the endpoint:
[block:code]
{
  "codes": [
    {
      "code": "    \"category\": [\n        {\n            \"coding\": [\n                {\n                    \"system\": \"http://loinc.org\",\n                    \"code\": \"96347-0\",\n                    \"display\": \"Radiology Consent\"\n                }\n            ]\n        }\n    ],",
      "language": "text"
    }
  ]
}
[/block]
## patient [REQUIRED]

This attribute points us to the patient referenced to attach this Consent.
[block:code]
{
  "codes": [
    {
      "code": "    \"patient\": {\n        \"reference\": \"Patient/5350cd20de8a470aa570a852859ac87e\"\n    },",
      "language": "text"
    }
  ]
}
[/block]
## sourceAttachment

If this consent needs an attach PDF document associated with it, you may specify it in this `sourceAttachment` field. The required subfields are as-follows:
1. `sourceAttachment.contentType`: The mimeType of the data. Currently we only support `application/pdf`
2. `sourceAttachment.data`: The data encoded using base64
3. `sourceAttachment.title`: The filename to save within Canvas - this is the filename when downloaded to the user's browser. Duplicate names are allowed

## provision [REQUIRED]

The `provision` attribute is used to capture the consent's effective and expiration date in Canvas. Each date must be in the `YYYY-MM-DD` date format. The provision.period.start_date is required. The provision.end_date can be specifically specified, but if left blank, it will default to the consent's expiration rule. defined in Canvas Settings. 
[block:code]
{
  "codes": [
    {
      "code": "\"provision\": {\n  \"period\": {\n    \"start\": \"2022-05-15\",\n    \"end\": \"2022-10-10\"\n  }\n}",
      "language": "text"
    }
  ]
}
[/block]