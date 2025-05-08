---
title: Bug fix when using FHIR Search parameters that allow for a code|system to be passed
tags: api bugfix
layout: productupdates
date: 2025-05-05
---
Various FHIR endpoints allow for searching by a coding. This release ensures when searching by these codings, it follows the correct FHIR [token](https://www.hl7.org/fhir/R4/search.html#token) logic. This includes the following endpoint search parameters: Appointment.appointment_type, CarePlan.category, DiagnosticReport.category, DiagnosticReport.code, DocumentReference.category, DocumentReference.type, Observation.category, Observation.code, QuestionnaireResponse.questionnaire.code, and QuestionnaireResponse.questionnaire.item.code. 