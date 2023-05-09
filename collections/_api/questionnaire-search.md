---
title: "Questionnaire Search"
slug: "questionnaire-search"
excerpt: "Search for questionnaires"
hidden: false
createdAt: "2021-09-24T01:18:21.963Z"
updatedAt: "2022-06-01T14:52:25.831Z"
---
# Creating a Questionnaire in Canvas

See [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4403561447827-Creating-a-New-Questionnaire) on how to create and upload a questionnaire in Canvas.

# Searching by Questionnaire Code.

We support searching for a Questionnaire by the code attached to the Questionnaire itself 

- `/Questionnaire?identifier=711013002` will return the questionnaire with an identifier of “711013002” when uploaded to Canvas.

# Searching by Question Code

We support searching for Questionnaires that contain a questions with a certain code

- `/Questionnaire?code=456789` will return all questionnaires with a question given a code of “456789” when it was uploaded to Canvas.  Questions can be reused between multiple questionnaires, but any given question code should only appear once within a particular questionnaire.

# Understanding Canvas Questionnaires

## Unique Coding

All questionnaires must have a unique code identifier. 

All response options within a question on a questionnaire must have a unique code. 

## Question Types

Canvas supports 3 different type of questions: 

1. Multi select responses allowed questions are denoted with 
[block:code]
{
  "codes": [
    {
      "code": "\"type\": \"choice\",\n\"repeats\": true,",
      "language": "text"
    }
  ]
}
[/block]
2. Single select response questions are denoted with 
[block:code]
{
  "codes": [
    {
      "code": "\"type\": \"choice\",\n\"repeats\": false,",
      "language": "text"
    }
  ]
}
[/block]
1. Free text responses questions are denoted with 
[block:code]
{
  "codes": [
    {
      "code": "\"type\": \"text\",\n\"repeats\": false,",
      "language": "text"
    }
  ]
}
[/block]
## System 

See [QuestionnaireResponse Create](ref:questionnaireresponse-create) about how the system is mapped internally from Questionnaires uploaded in Canvas.