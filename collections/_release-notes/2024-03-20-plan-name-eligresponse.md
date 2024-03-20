---
title: Updates to Coverage Eligibility Response Workflows
date: 2024-03-20 20:00:00
tags: api ui bugfix
layout: productupdates
---

- We have added an extension (active-health-benefit-plan-coverage-description) to FHIR CoverageEligibilityResponse that pulls the plan name from the parsed X12 response. 
- The status of eligibility checks that have failed in ClaimMD with a 400+ error will now be accurately reflected in the UI and API. The outcome in the FHIR CoverageEligibilityRepsponse endpoint will now return `error`.
- We have implemented improved handling when processing eligibility responses from ClaimMD that contain empty quantity fields. 