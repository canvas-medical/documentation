---
title: "QuestionnaireResponse Create"
slug: "questionnaireresponse-create"
excerpt: "Create a response to a questionnaire"
hidden: false
createdAt: "2021-09-24T01:26:42.510Z"
updatedAt: "2022-10-06T19:11:05.373Z"
---
# Getting the newly-created questionnaire response ID.
Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header. You will use this for subsequent requests that reference this questionnaire response.

# Questionnaire Responses in Canvas

Upon successful creation of a Questionnaire Response, it will show up as a Data import note within the patient chart. It will be inserted into the timeline using the timestamp passed in `authored`. 

# Building a Questionnaire in Canvas

To learn how to build questionnaires in Canvas see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4403561447827-Creating-a-New-Questionnaire). The most important thing when using the Questionnaire Response Create endpoint is to ensure the questionnaire was built with unique codings. 

# Attributes that are pulled into Canvas:

## resourceType [REQUIRED]

This should be hardcoded to `QuestionnaireResponse`
[block:code]
{
  "codes": [
    {
      "code": "\"resourceType\": \"QuestionnaireResponse\"",
      "language": "text"
    }
  ]
}
[/block]
 ## questionnaire [REQUIRED]

Canvas questionnaire resource that the responses are for, formatted like "Questionnaire/ac1da1a4-ccc4-492e-a9e0-7f70a58c2129". You can obtain this id by using our [Questionnaire Search](ref:questionnaire-search) 
[block:code]
{
  "codes": [
    {
      "code": "\"questionnaire\": \"Questionnaire/7291013b-81c6-41b6-9212-6c96b8b44f94\"",
      "language": "text"
    }
  ]
}
[/block]
## subject [REQUIRED] 

Canvas patient resource that the responses are for
[block:code]
{
  "codes": [
    {
      "code": "\"subject\": {\n\t\"reference\": \"Patient/a39cafb9d1b445be95a2e2548e12a787\"\n}",
      "language": "text"
    }
  ]
}
[/block]
## authored

The UTC datetime string for when the questionnaire responses were provided, iso8601 format.
If omitted from the body, the current timestamp at data ingestion will be used 
[block:code]
{
  "codes": [
    {
      "code": "\"authored\": \"2022-03-19T14:54:12.194952+00:00\"",
      "language": "text"
    }
  ]
}
[/block]
## author

 This is a reference to the person that filled out the questionnaire. If this is not included, then the built in automation user, "Canvas Bot" will be used instead. 

It could be a practitioner resource that recorded the questionnaire, formatted like "Practitioner/4150cd20de8a470aa570a852859ac87e".  
[block:code]
{
  "codes": [
    {
      "code": "\"author\": {\n\t\"reference\": \"Practitioner/fc87cbb2525f4c5eb50294f620c7a15e\"\n},",
      "language": "text"
    }
  ]
}
[/block]
We also accept patient authored questionnaires, formatted like (matching the `subject` attribute):
[block:code]
{
  "codes": [
    {
      "code": "\"author\": {\n\t\"reference\": \"Patient/a39cafb9d1b445be95a2e2548e12a787\"\n}",
      "language": "text"
    }
  ]
}
[/block]
# item [REQUIRED]

A list of one or more questions and how they were answered. If a question is omitted it will be left unanswered in Canvas. However, if it is a questionnaire tied to a scoring function, Canvas requires all questions to be answered in order to accurately score the questionnaire. 

Perform a [Questionnaire Search](ref:questionnaire-search) in order to know each question's attributes to fill in below. 

 Each item object in the list should contain:
   - **[Required]** `linkId` A Canvas assigned identifier that uniquely identifies this question in Canvas. This linkId must only occur at most once in the payload.
   - `text` Human readable text of the question.   Not stored but can be helpful to include for troubleshooting.
   - **[Required]** `answer` A list of one or more answers to this question. 
      - If this is for a question where the answer is a free-text field (i.e. Questionnaire item `type` = "text"), then the list will contain a single object containing a `valueString` field with the response text.
[block:code]
{
  "codes": [
    {
      "code": "\"item\": [\n\t{\n  \t\"linkId\": \"24178e3c-c67c-4524-bcb1-522aef068795\",\n  \t\"text\": \"This is question #3\",\n  \t\"answer\": [\n  \t\t{\n  \t\t\t\"valueString\": \"This is a free text response\"\n  \t\t}\n  \t]\n  }\n ]",
      "language": "text"
    }
  ]
}
[/block]
      - If this is for a question where the answer is a single or multiple choice selection (i.e. Questionnaire item `type` = "choice" and `repeats` is "false" for single or "true" for multiple), then the list will have one or more objects containing:
        -  **[Required]** `code` Value that can uniquely identify this answer within the associated `system`
        -  **[Required]** `display` Text of answer that was selected
        -  **[Required]** `system` Coding system where the `code` comes from

Currently we only support specific system's in Canvas through our FHIR endpoints. Here is the mapping of system uri in FHIR to systems in Canvas
[block:parameters]
{
  "data": {
    "0-0": "http://loinc.org",
    "1-0": "http://snomed.info/sct",
    "2-0": "http://canvasmedical.com",
    "3-0": "http://www.ama-assn.org/go/cpt",
    "4-0": "http://hl7.org/fhir/sid/icd-10",
    "0-1": "LOINC",
    "1-1": "SNOMED",
    "2-1": "CANVAS",
    "3-1": "CPT",
    "4-1": "ICD-10",
    "5-0": "http://schemas.<instance_name>.canvasmedical.com/fhir/systems/internal",
    "5-1": "INTERNAL",
    "h-0": "FHIR System URI",
    "h-1": "Canvas System (uploaded via google sheet)"
  },
  "cols": 2,
  "rows": 6
}
[/block]
Example of a single select answer:
[block:code]
{
  "codes": [
    {
      "code": "    \"item\": [\n        {\n            \"linkId\": \"c79da8bd-d20e-4f56-909f-f3dabae7f64f\",\n            \"text\": \"This is question #1\",\n            \"answer\": [\n                {\n                  \"valueCoding\": {\n                    \"system\": \"http://schemas.training.canvasmedical.com/fhir/systems/internal\",\n                    \"code\": \"10101-1\",\n                    \"display\": \"Single select response #1\"\n                  }\n                }\n            ]\n        }\n   ]",
      "language": "text"
    }
  ]
}
[/block]
Example of a multiple response allowed:
[block:code]
{
  "codes": [
    {
      "code": "\"item\": [\n\t{\n    \"linkId\": \"f25af10f-5d26-42a8-90a1-d86c2b363600\",\n    \"text\": \"This is question #2\",\n    \"answer\": [\n      {\n        \"valueCoding\": {\n          \"system\": \"http://schemas.training.canvasmedical.com/fhir/systems/internal\",\n          \"code\": \"10102-1\",\n          \"display\": \"Multi select response #1\"\n      \t}\n      },\n      {\n        \"valueCoding\": {\n          \"system\": \"http://schemas.training.canvasmedical.com/fhir/systems/internal\",\n          \"code\": \"10102-2\",\n          \"display\": \"Multi select response #2\"\n        }\n      }              \n    ]\n  }\n]",
      "language": "text"
    }
  ]
}
[/block]
# Validation
[block:callout]
{
  "type": "warning",
  "title": "Beware of ambiguous choices!",
  "body": "If the questionnaire you are responding to contains a question with identical codings for different choices, we won't know which of the choices were made. In this case, we'll reject the request. To avoid this, make sure each question has a uniquely coded set of choices. You can re-use choice codings across questions, but not within them.\n\nYou will know this occurred when you see the message:\n`Question received a response option code: {coding['code']} that belongs to more than one option response`"
}
[/block]

[block:callout]
{
  "type": "warning",
  "title": "More Coding Validation",
  "body": "The system is the ValueCoding answer needs to match the system that the question specified in the Questionnaire Search Response. If it does not you will see the message:\n`Question expects answer of code system {system} but {coding['code_system']} was given`\n\nIf a code is passed that does not exist for that question in Canvas, you will see the following message:\n`Question received an invalid response option code: {coding['code']}`"
}
[/block]

[block:callout]
{
  "type": "warning",
  "title": "Answer Validation",
  "body": "For single or free text questions, if the length of `answer` is greater than one, you will see the message \n`Question of type {_type} is expecting at most one answer`\n\nFor free text questions, the answer object needs to include ValueString or you will see this message:\n`Question of type TXT expects a valueString answer`\n\nFor single or multi select questions, the answer object(s) need to include ValueCoding or you will see:\n`Question of type {_type} expects a valueCoding answer`"
}
[/block]