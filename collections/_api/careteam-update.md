---
title: "CareTeam Update"
slug: "careteam-update"
excerpt: "Update a Patient's Care Team"
hidden: false
createdAt: "2022-06-24T15:38:21.608Z"
updatedAt: "2022-06-28T15:19:51.358Z"
---
The CareTeam update endpoint acts as an upsert, so there is no provided *create* endpoint. If all fields are omitted from the body it will mark any current Care Team Memberships for the current patient as inactive and they will no longer display on the UI or be returned in a Read/Search. 

# CareTeam Body Attributes

## resourceType [required]

This will be hard coded to `CareTeam`
[block:code]
{
  "codes": [
    {
      "code": "\"resourceType\": \"CareTeam\",",
      "language": "text"
    }
  ]
}
[/block]
## subject

Patients can only have one CareTeam, so the CareTeam identifier is the FHIR ID of the patient. Due to this you do not have to specify the `subject` in the body of the request as it is derived from the endpoint _id passed. 
[block:code]
{
  "codes": [
    {
      "code": "\"subject\": {\n    \"reference\": \"Patient/3e72c07b5aac4dc5929948f82c9afdfd\"\n},",
      "language": "text"
    }
  ]
}
[/block]
## participant

Calls to this endpoint expect the full CareTeam to be listed. Any missing CareTeam member will be marked as inactive from the CareTeam and will no longer show up as a member on the Canvas UI. If no participant attribute is added, all existing members of the care team will be marked as inactive and they will no longer display on the UI or be returned in a Read/Search. 

For each participant object you can specify the role and the member. Currently we only support *one role per practitioner* and *one type of role per patient*. We accept the following syntax below where you can specify one role coding (system, code, display) per member. This information should come from the Admin setup of Care Team Roles using this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4409741845011-Care-Teams).
[block:code]
{
  "codes": [
    {
      "code": "\"participant\": [\n        {\n            \"role\": [\n                {\n                    \"coding\": [\n                        {\n                            \"system\": \"http://snomed.info/sct\",\n                            \"code\": \"17561000\",\n                            \"display\": \"Cardiologist\"\n                        }\n                    ]\n                }\n            ],\n            \"member\": {\n                \"reference\": \"Practitioner/3640cd20de8a470aa570a852859ac87e\"\n            }\n        }\n]",
      "language": "text"
    }
  ]
}
[/block]

[block:callout]
{
  "type": "info",
  "body": "Due to a legacy design detail with the CareTeam implementation, there is a specific condition under which inclusion of this header will not produce expected results. In the case where all members of a CareTeam are removed through the Canvas user interface (i.e. not through the FHIR API), the last modified date for the CareTeam will be equal to the last modified date of the patient record until another member is added to the CareTeam.\n\nMore information about the If-Unmodified-Since header can be found in the [Conditional Requests](https://docs.canvasmedical.com/reference/conditional-requests) documentation.",
  "title": "If-Unmodified-Since Header"
}
[/block]