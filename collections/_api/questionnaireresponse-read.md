---
title: "QuestionnaireResponse Read"
slug: "questionnaireresponse-read"
excerpt: "Find a specific QuestionnaireResponse by its resource id"
hidden: false
createdAt: "2021-09-24T01:31:05.566Z"
updatedAt: "2022-03-20T15:36:15.164Z"
---
Answers for Questionnaire items with `type` = 'text' will be returned as `valueString` answers.  

Answers for Questionnaire items with `type` = 'choice' will be returned as `valueCoding` answers. This could either be a single or multi select choice. See [QuestionnaireResponse Create](ref:questionnaireresponse-create)   to understand the mappings of system's from Canvas to FHIR.