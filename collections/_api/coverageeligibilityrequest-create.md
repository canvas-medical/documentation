---
title: "Create Coverage Eligibility Request"
slug: "coverageeligibilityrequest-create"
excerpt: "Create a coverage eligibility request"
hidden: false
createdAt: "2022-06-21T19:44:50.227Z"
updatedAt: "2022-06-28T14:26:35.795Z"
---
# Coverage Eligibility within Canvas

To learn more about coverage eligibility within the Canvas UI, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4408206355603-Patient-Coverages-2-0).

# Getting the newly-created coverage eligibility request ID.
Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header. You will use this for subsequent requests that reference this coverage eligibility request.  Specifically, this resource identifier will be used when searching for the corresponding coverage eligibility response.

# Attributes that are pulled into Canvas:

## status [required]

Status describes the state in which the request is in. Although FHIR accepts other statuses, Canvas currently only accepts `status` = "active". Anything else will be ignored and status will default to 'active'. 
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
## purpose [required]

Purpose indicates what information is being requested. Although FHIR accepts more codes, Canvas currently only supports `purpose` = "benefits". 
[block:code]
{
  "codes": [
    {
      "code": "\"purpose\": [\n   \"benefits\"\n]",
      "language": "text"
    }
  ]
}
[/block]
## patient [required]

Canvas patient resource identifying the patient for the coverage, formatted like "Patient/5350cd20de8a470aa570a852859ac87e". 
[block:code]
{
  "codes": [
    {
      "code": "\"patient\": {\n  \"reference\": \"Patient/9713f5a3c8464a2587912e80bc2dd938\"\n},",
      "language": "text"
    }
  ]
}
[/block]
## insurance [required]
Canvas coverage resource identifying the coverage for this iteration of insurance, formatted like "Coverage/7afeaa26-48e1-43c2-b414-fd8aa9780af1". Coverage is a required field within insurance and must be associated with the patient reference passed in. 

Focal indicates whether the insurance should be used in the request. It is not a required field. It defaults to True. Any other input will be ignored. 

If multiple insurances are added, only the first is ingested by Canvas. 
[block:code]
{
  "codes": [
    {
      "code": "\"insurance\": [\n  {\n    \"focal\": true,\n    \"coverage\": {\n      \"reference\": \"Coverage/743aa331-2f85-420b-ab10-8a6b7bb6a1cf\"\n    }\n  }\n]",
      "language": "text"
    }
  ]
}
[/block]