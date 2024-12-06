---
title: Add Physical Exams, Structured Assessments and/or Review of Systems using FHIR QuestionnaireResponse Create 
layout: productupdates
tags: api
date: 2024-07-18
---

When using the QuestionnaireResponse Create endpoint, the command will be inserted into the Patient’s note based on what the use case in charting of the questionnaire is: Questionnaire, Physical Exam, Structured Assessments, Review of Systems

When inserting a command into a billable encounter, if the questionnaire responses include the selection of an answer that has a cpt code included in the Fee schedule, the code will appear in the Note’s billing footer