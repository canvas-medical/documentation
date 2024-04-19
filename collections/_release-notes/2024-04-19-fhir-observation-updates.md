---
title: Updates FHIR Observation
date: 2024-04-19
layout: productupdates
tags: api bugfix
---

We've made the following changes to the [FHIR Observation](/api/observation) resource. 
- Observations are now created for all questionnaire responses that have been coded with LOINC or SNOMED as the code system. This includes all responses across all questionnaire types (questionnaires, ROS, PE, structured assessments) We previoulsy only created observations if `Use in Social Determinants` was set to true for responses of questionnaires. 
- `Derived-from` was added as a search param.
- Additional display names were added to various attributes.
- All vitals signs are now supported in FHIR V2. [Read More.](/guides/submit-vitals-via-fhir)

