---
title: "Media"
---

## Media Create
A successful FHIR Media create request will insert a [Visual Exam Finding](https://canvas-medical.zendesk.com/hc/en-us/articles/360057916493-Command-Visual-Exam-Finding) into a new or existing note for the patient.

### Media Attributes:

Canvas accepts a FHIR standard request body, you may refer to [FHIR Media Documentation](https://www.hl7.org/fhir/media.html) to help out in building your Media request. Below is our documentation on how Canvas specifically will use each attribute.

### resourceType [REQUIRED] 

This is hard coded to be `Media` for this endpoint
[block:code]
{
  "codes": [
    {
      "code": "\"resourceType\": \"Media\",",
      "language": "text"
    }
  ]
}
[/block]
### status [REQUIRED]

The FHIR media resource requires inclusion of the status attribute, and Canvas currently recognizes `completed` and `entered-in-error` values for status.
[block:code]
{
  "codes": [
    {
      "code": "\"status\": \"completed\",",
      "language": "text"
    }
  ]
}
[/block]
### subject [REQUIRED]

The subject attribute contains a reference to the patient that the media is a record of. This is a required value. The provided media content will be inserted into the patient's chart.
[block:code]
{
  "codes": [
    {
      "code": "\"subject\": {\n\t\"reference\": \"Patient/610066552b0a42c5a0095a047cf1bff1\"\n},",
      "language": "text"
    }
  ]
}
[/block]
### encounter

The encounter attribute contains a reference to the encounter that is associated with the media. If an encounter is provided, the media will be inserted into the existing note for the encounter. If an encounter is not provided, then a new data import note will be created and the media will be inserted this new note.
[block:code]
{
  "codes": [
    {
      "code": "\"encounter\": {\n\t\"reference\": \"Encounter/302fca5c-9231-4eca-83e7-c62b6ab93ba7\"\n},",
      "language": "text"
    }
  ]
}
[/block]
### operator

The operator attribute contains a reference to the practitioner or patient that generated the media. This will shows up in the Canvas UI when you click the command as the Originator in the tooltip that pops up. 
[block:code]
{
  "codes": [
    {
      "code": "    \"operator\": {\n        \"reference\": \"Practitioner/610066552b0a42c5a0095a047cf1bff1\"\n    },",
      "language": "text"
    }
  ]
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "  \"operator\": {\n        \"reference\": \"Patient/610066552b0a42c5a0095a047cf1bff1\"\n    },",
      "language": "text"
    }
  ]
}
[/block]
### content [REQUIRED]

The content attribute is a JSON object that contains metadata about the content and the content itself. This is a required value. The content object contains three attributes:

- contentType [REQUIRED]: One of these supported MIME content types: `image/heic`, `image/jpeg`, `image/png`
- content [REQUIRED] : Base64 string of the media content
- title: An optional title of the content file
[block:code]
{
  "codes": [
    {
      "code": "\"content\": {\n  \"contentType\": \"image/jpeg\",\n  \"data\": \"QWxsIHlvdXIgYmFzZSBhcmUgYmVsb25nIHRvIHVzCg==\",\n  \"title\": \"Image title\"\n},",
      "language": "text"
    }
  ]
}
[/block]
### note

The note attribute is a JSON array of JSON objects, each of which contains a `text` attribute that contains the text of a comment that will be attached to the inserted media on the UI.
[block:code]
{
  "codes": [
    {
      "code": "\"note\": [\n        {\n            \"text\": \"First note\"\n        },\n        {\n            \"text\": \"Second note\"\n        }\n]",
      "language": "text"
    }
  ]
}
[/block]