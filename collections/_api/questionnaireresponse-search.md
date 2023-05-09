---
title: "QuestionnaireResponse Search"
slug: "questionnaireresponse-search"
excerpt: "Search for responses to questionnaires"
hidden: false
createdAt: "2021-09-24T01:29:36.222Z"
updatedAt: "2022-06-01T14:55:02.035Z"
---
Answers for Questionnaire items with `type` = 'text' will be returned as `valueString` answers.  

Answers for Questionnaire items with `type` = 'choice' will be returned as `valueCoding` answers. This could either be a single or multi select choice. See [QuestionnaireResponse Create](ref:questionnaireresponse-create)   to understand the mappings of system's from Canvas to FHIR. 

# Authored Search Param

We support multiple type of searching by date: 
[block:parameters]
{
  "data": {
    "0-0": "eq2021-09-01",
    "0-1": "Search for QuestionnaireResponses anytime during this day",
    "1-0": "ge2021-09-16",
    "1-1": "Search for QuestionnaireResponses on or after this day",
    "2-0": "gt2021-09-16",
    "2-1": "Search for QuestionnaireResponses after this day",
    "3-0": "le2021-10-01",
    "3-1": "Search for QuestionnaireResponses on or before this day",
    "4-0": "lt2021-10-01",
    "4-1": "Search for QuestionaireResponses before this day"
  },
  "cols": 2,
  "rows": 5
}
[/block]
# Creating a Response to a Questionnaire in Canvas

See this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360057544593-Command-Questionnaire) for how to fill out a questionnaire for a patient via the questionnaire command.