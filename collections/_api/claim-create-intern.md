---
title: "Claim Create Intern"
slug: "claim-create-intern"
excerpt: "Create a claim for a specific patient"
hidden: true
createdAt: "2022-06-13T16:52:10.231Z"
updatedAt: "2022-11-23T19:16:15.282Z"
---
# Getting the newly-created claim ID.
Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header. You will use this for subsequent requests that reference this claim.

You will be able to see the patient's claim in the Canvas UI by navigating to the patient's chart and further their registration page. See our [help desk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360061238073-Claims). There will also be a Data Import Note on the patient chart inserted in the timeline of the data that matches the `created` attribute. If supportingInfo was specified you will see the matching Reason For Visit specified. To learn more about viewing claims on the Canvas UI, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360061238073-Claims). 

# Attributes that are pulled into Canvas:

## resourceType [REQUIRED]

The only accepted value is:
[block:code]
{
  "codes": [
    {
      "code": "\"resourceType\": \"Claim\",",
      "language": "text"
    }
  ]
}
[/block]
## status [REQUIRED]

While FHIR may support more statuses, the only accepted value Canvas currently supports is "active". Regardless of input, status is set to active upon creation of a claim. Within the Canvas UI, this claim will be added to the coding queue.
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
## type [required]

Canvas currently only accepts one type. It is set to "professional" by default upon creation of the claim.
[block:code]
{
  "codes": [
    {
      "code": "\"type\": {\n  \"coding\": [\n    {\n      \"system\": \"http://hl7.org/fhir/ValueSet/claim-type\",\n      \"code\": \"professional\"\n    }\n  ]\n}",
      "language": "text"
    }
  ]
}
[/block]
## use [required]

While FHIR supports more uses, Canvas will only accept "claim" as the use. 
[block:code]
{
  "codes": [
    {
      "code": "\"use\": \"claim\",",
      "language": "text"
    }
  ]
}
[/block]
## patient [REQUIRED]

The patient field is the Canvas ID of the patient that the claim is being made for. 
[block:code]
{
  "codes": [
    {
      "code": "\"patient\": {\n    \"reference\": \"Patient/865058f6654149bd921264d91519af9e\"\n },",
      "language": "text"
    }
  ]
}
[/block]
## created [REQUIRED] 

When this claim resource was created, formatted like YYYY-MM-DD.  Canvas will use this as the date of service for the claims in this message. In the Canvas UI, the created claim will be titled "Data import on YYY-MM-DD" when created through this endpoint.
[block:code]
{
  "codes": [
    {
      "code": "\"created\": \"2021-08-16\",",
      "language": "text"
    }
  ]
}
[/block]
## provider [REQUIRED] 

Specifying the staff resource for services in the claim. The provider set here is displayed in the claim as both the rendering and referring provider. This can be viewed by clicking the three dots at the top right of the screen and going to the 'edit provider details' item. Canvas supports identifying providers where `type` is one of:
  - `http://hl7.org/fhir/sid/us-npi` where the provider.reference is a US National Provider Identifier.  A Staff record with the referenced NPI must exist in your Canvas instance: 
[block:code]
{
  "codes": [
    {
      "code": "\"provider\": {\n    \"reference\": \"1234567890\",\n    \"type\": \"http://hl7.org/fhir/sid/us-npi\"\n},",
      "language": "text"
    }
  ]
}
[/block]
  - `http://canvasmedical.com` when the reference is a Canvas provider resource id: 
[block:code]
{
  "codes": [
    {
      "code": "\"provider\": {\n    \"reference\": \"Practitioner/4150cd20de8a470aa570a852859ac87e\",\n    \"type\": \"http://canvasmedical.com\"\n},",
      "language": "text"
    }
  ]
}
[/block]
## supportingInfo

 A reason for visit will be saved if `code` = "patientreasonforvisit" and `system` = "http://hl7.org/fhir/ValueSet/claim-informationcategory".  The contents of that iteration's `valueString` will be used.  Only the last element in the list matching this criteria will be used. Use this example as a starting point and update the valueString with your appropriate reason for visit. This field is not required and can be left out of the message if you do not wish to specify a reason for visit. 
[block:code]
{
  "codes": [
    {
      "code": "  \"supportingInfo\": [{\n      \"sequence\": 0,\n      \"category\": {\n          \"coding\": [{\n              \"code\": \"patientreasonforvisit\",\n              \"system\": \"http://hl7.org/fhir/ValueSet/claim-informationcategory\",\n              \"display\": \"Patient Reason for Visit\"\n          }]\n      },\n      \"valueString\": \"This is only...a test\"\n  }],",
      "language": "text"
    }
  ]
}
[/block]
  
## diagnosis [REQUIRED]

This is a list will create the Assessments in Canvas for this claim. Each diagnosis object can include the following:
 - `sequence`:  An incremented number to identify each diagnosis in this message. Each should be unique within the claim message. There must be an item with ` sequence` = 1. 
  - `diagnosisCodeableConcept` is an object to specify the coding of this diagnosis. Currently we take only the first element in the `coding` list where the coding's system is "http://hl7.org/fhir/ValueSet/icd-10". 

If no object in the list matches the coding system string exactly, the Canvas UI will display an empty diagnosis on the patient's chart and 0 diagnoses in the claim view within registration. The code and display fields accept all strings. If more than one diagnosis is added, the request will not be able to be processed. 
[block:code]
{
  "codes": [
    {
      "code": "  \"diagnosis\": [\n    {\n      \"sequence\": 1,\n      \"diagnosisCodeableConcept\": {\n        \"coding\": [\n          {\n            \"code\": \"F411\",\n            \"system\": \"http://hl7.org/fhir/ValueSet/icd-10\",\n            \"display\": \"Generalized anxiety\"\n          }\n        ]\n      }\n    }\n  ],",
      "language": "text"
    }
  ]
}
[/block]
## insurance [REQUIRED]

 Defines what coverages are to be used when adjudicating the claim. For each object in the insurance list you need to specify:
  - `sequence` An incremented number to identify each insurance in this message.  Each should be unique within the claim message. [required]
  - `focal` Boolean to indicate whether this insurance should be used to adjudicate the claim in this message. We will ignore any elements that are False. If focal is not included, it defaults to False.
  - `coverage` Canvas coverage resource identifying the coverage for this iteration of insurance, formatted like "Coverage/7afeaa26-48e1-43c2-b414-fd8aa9780af1" [required]
[block:code]
{
  "codes": [
    {
      "code": "\"insurance\": [\n    {\n      \"sequence\": 1,\n      \"focal\": true,\n      \"coverage\": {\n        \"reference\": \"Coverage/8bafc5c7-36df-440c-b646-100e4b053dc1\"\n      }\n    }\n  ],",
      "language": "text"
    }
  ]
}
[/block]
# item [REQUIRED]

 This is the list of service charges to be used in the claim. For each object in the list you will need to specify:
  - `sequence` An incremented number to identify each item in this message.  Each should be unique within the claim message. [required]
-  `diagnosisSequence` Array with 1 or more `sequence` numbers from the `diagnosis` section to specify which charge is associated with which diagnosis in the claim [required]
  - `productOrService` is an object to specify the coding of the service. We currently only support the first coding where `system` is "http://hl7.org/fhir/us/core/ValueSet/us-core-procedure-code". One valid system coding is required. Code and Display are not required to be added. If they are not included, Canvas's UI will not display a procedure name in the charges view within a specific claim. [required]
  - `modifier` specifies the list of charge modifier codings. Canvas accepts the first element where the coding's `system` is "http://hl7.org/fhir/us/carin-bb/ValueSet/AMACPTCMSHCPCSModifiers". If more than one element is included, the request will not be accepted. Canvas uses the 2 character modifiers from this ValueSet.
  - `quantity` Number of products or services for the claim [required]
  - `unitPrice.value` Cost for each quantity [required]

[block:code]
{
  "codes": [
    {
      "code": "\"item\": [\n    {\n      \"sequence\": 1,\n      \"diagnosisSequence\": [\n        1\n      ],\n      \"productOrService\": {\n        \"coding\": [\n          {\n            \"system\": \"http://hl7.org/fhir/us/core/ValueSet/us-core-procedure-code\",\n            \"code\": \"exam\",\n            \"display\": \"Office visit\"\n          }\n        ]\n      },\n      \"modifier\": [{\n        \"coding\": [\n          {\n            \"system\": \"http://hl7.org/fhir/us/carin-bb/ValueSet/AMACPTCMSHCPCSModifiers\",\n            \"code\": \"21\"\n          }\n        ]\n      }],\n      \"quantity\": 1,\n      \"unitPrice\": {\n        \"value\": 75.00\n      }\n    }\n  ]",
      "language": "text"
    }
  ]
}
[/block]
# Priority [required]

Priority indicates the urgency with which the claim should be processed. Although FHIR supports other priority codes, Canvas currently only accepts priority "normal".
[block:code]
{
  "codes": [
    {
      "code": "\"priority\": {\n    \"coding\": [\n      {\n        \"code\": \"normal\",\n        \"system\": \"http://hl7.org/fhir/ValueSet/process-priority\"\n      }\n    ]\n },",
      "language": "text"
    }
  ]
}
[/block]